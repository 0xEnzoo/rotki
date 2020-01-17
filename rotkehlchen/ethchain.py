import logging
import os
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from eth_utils.address import to_checksum_address
from web3 import HTTPProvider, Web3

from rotkehlchen.assets.asset import EthereumToken
from rotkehlchen.fval import FVal
from rotkehlchen.logging import RotkehlchenLogsAdapter
from rotkehlchen.typing import ChecksumEthAddress
from rotkehlchen.utils.misc import from_wei, request_get_dict
from rotkehlchen.utils.serialization import rlk_jsonloads

logger = logging.getLogger(__name__)
log = RotkehlchenLogsAdapter(logger)

DEFAULT_ETH_RPC_TIMEOUT = 10


class Ethchain():
    def __init__(
            self,
            ethrpc_endpoint: str,
            attempt_connect: bool = True,
            eth_rpc_timeout: int = DEFAULT_ETH_RPC_TIMEOUT,
    ) -> None:
        self.web3: Web3 = None
        self.rpc_endpoint = ethrpc_endpoint
        self.connected = False
        self.eth_rpc_timeout = eth_rpc_timeout
        if attempt_connect:
            self.attempt_connect(ethrpc_endpoint)

    def __del__(self) -> None:
        if self.web3:
            del self.web3

    def attempt_connect(
            self,
            ethrpc_endpoint: str,
            mainnet_check: bool = True,
    ) -> Tuple[bool, str]:
        message = ''
        if self.rpc_endpoint == ethrpc_endpoint and self.connected:
            # We are already connected
            return True, 'Already connected to an ethereum node'

        if self.web3:
            del self.web3

        try:
            parsed_eth_rpc_endpoint = urlparse(ethrpc_endpoint)
            if not parsed_eth_rpc_endpoint.scheme:
                ethrpc_endpoint = f"http://{ethrpc_endpoint}"
            provider = HTTPProvider(
                endpoint_uri=ethrpc_endpoint,
                request_kwargs={'timeout': self.eth_rpc_timeout},
            )
            self.web3 = Web3(provider)
        except requests.exceptions.ConnectionError:
            log.warning('Could not connect to an ethereum node. Will use etherscan only')
            self.connected = False
            return False, f'Failed to connect to ethereum node at endpoint {ethrpc_endpoint}'

        if self.web3.isConnected():
            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(dir_path, 'data', 'token_abi.json'), 'r') as f:
                self.token_abi = rlk_jsonloads(f.read())

            # Also make sure we are actually connected to the Ethereum mainnet
            synchronized = True
            msg = ''
            if mainnet_check:
                chain_id = self.web3.eth.chainId
                if chain_id != 1:
                    message = (
                        f'Connected to ethereum node at endpoint {ethrpc_endpoint} but '
                        f'it is not on the ethereum mainnet. The chain id '
                        f'the node is in is {chain_id}.'
                    )
                    log.warning(message)
                    self.connected = False
                    return False, message

                if self.web3.eth.syncing:  # pylint: disable=no-member
                    current_block = self.web3.eth.syncing.currentBlock  # pylint: disable=no-member
                    latest_block = self.web3.eth.syncing.highestBlock  # pylint: disable=no-member
                    synchronized, msg = self.is_synchronized(current_block, latest_block)
                else:
                    current_block = self.web3.eth.blockNumber  # pylint: disable=no-member
                    latest_block = self.query_eth_highest_block()
                    if latest_block is None:
                        return False, 'Could not query latest block from blockcypher.'
                    synchronized, msg = self.is_synchronized(current_block, latest_block)

            if not synchronized:
                return False, msg

            self.connected = True
            log.info(f'Connected to ethereum node at {ethrpc_endpoint}')
            return True, ''
        else:
            log.warning('Could not connect to an ethereum node. Will use etherscan only')
            self.connected = False
            message = f'Failed to connect to ethereum node at endpoint {ethrpc_endpoint}'

        # If we get here we did not connnect
        return False, message

    def is_synchronized(self, current_block: int, latest_block: int) -> Tuple[bool, str]:
        """ Validate that the ethereum node is synchronized
            within 20 blocks of latest block

        Returns a tuple (results, message)
            - result: Boolean for confirmation of synchronized
            - message: A message containing information on what the status is. """
        message = ''
        if current_block < (latest_block - 20):
            message = (
                'Found ethereum node but it is out of sync. Will use etherscan.'
            )
            log.warning(message)
            self.connected = False
            return False, message

        return True, message

    def set_rpc_endpoint(self, endpoint: str) -> Tuple[bool, str]:
        """ Attempts to set the RPC endpoint for the ethereum client.

        Returns a tuple (result, message)
            - result: Boolean for success or failure of changing the rpc endpoint
            - message: A message containing information on what happened. Can
                       be populated both in case of success or failure"""
        result, message = self.attempt_connect(endpoint)
        if result:
            log.info('Setting ETH RPC endpoint', endpoint=endpoint)
            self.ethrpc_endpoint = endpoint
        return result, message

    @staticmethod
    def query_eth_highest_block() -> Optional[int]:
        """ Attempts to query blockcypher for the block height

        Returns the highest blockNumber"""

        url = 'https://api.blockcypher.com/v1/eth/main'
        log.debug('Querying ETH highest block', url=url)
        eth_resp = request_get_dict(url)

        if 'height' not in eth_resp:
            return None
        block_number = int(eth_resp['height'])
        log.debug('ETH highest block result', block=block_number)
        return block_number

    def get_eth_balance(self, account: ChecksumEthAddress) -> FVal:
        if not self.connected:
            log.debug(
                'Querying etherscan for account balance',
                sensitive_log=True,
                eth_address=account,
            )
            eth_resp = request_get_dict(
                'https://api.etherscan.io/api?module=account&action=balance&address=%s'
                % account,
            )
            if eth_resp['status'] != 1:
                raise ValueError('Failed to query etherscan for accounts balance')
            amount = FVal(eth_resp['result'])

            log.debug(
                'Etherscan account balance result',
                sensitive_log=True,
                eth_address=account,
                wei_amount=amount,
            )
            return from_wei(amount)
        else:
            wei_amount = self.web3.eth.getBalance(account)  # pylint: disable=no-member
            log.debug(
                'Ethereum node account balance result',
                sensitive_log=True,
                eth_address=account,
                wei_amount=wei_amount,
            )
            return from_wei(wei_amount)

    def get_multieth_balance(
            self,
            accounts: List[ChecksumEthAddress],
    ) -> Dict[ChecksumEthAddress, FVal]:
        """Returns a dict with keys being accounts and balances in ETH"""
        balances = {}

        if not self.connected:
            if len(accounts) > 20:
                new_accounts = [accounts[x:x + 2] for x in range(0, len(accounts), 2)]
            else:
                new_accounts = [accounts]

            for account_slice in new_accounts:
                log.debug(
                    'Querying etherscan for multiple accounts balance',
                    sensitive_log=True,
                    eth_accounts=account_slice,
                )

                eth_resp = request_get_dict(
                    'https://api.etherscan.io/api?module=account&action=balancemulti&address=%s' %
                    ','.join(account_slice),
                )
                if eth_resp['status'] != 1:
                    raise ValueError('Failed to query etherscan for accounts balance')
                eth_accounts = eth_resp['result']

                for account_entry in eth_accounts:
                    amount = FVal(account_entry['balance'])
                    # Etherscan does not return accounts checksummed so make sure they
                    # are converted properly here
                    checksum_account = to_checksum_address(account_entry['account'])
                    balances[checksum_account] = from_wei(amount)
                    log.debug(
                        'Etherscan account balance result',
                        sensitive_log=True,
                        eth_address=account_entry['account'],
                        wei_amount=amount,
                    )

        else:
            for account in accounts:
                amount = FVal(self.web3.eth.getBalance(account))  # pylint: disable=no-member
                log.debug(
                    'Ethereum node balance result',
                    sensitive_log=True,
                    eth_address=account,
                    wei_amount=amount,
                )
                balances[account] = from_wei(amount)

        return balances

    def get_multitoken_balance(
            self,
            token: EthereumToken,
            accounts: List[ChecksumEthAddress],
    ) -> Dict[ChecksumEthAddress, FVal]:
        """Return a dictionary with keys being accounts and value balances of token
        Balance value is normalized through the token decimals.
        """
        balances = {}
        if self.connected:
            token_contract = self.web3.eth.contract(  # pylint: disable=no-member
                address=token.ethereum_address,
                abi=self.token_abi,
            )

            for account in accounts:
                log.debug(
                    'Ethereum node query for token balance',
                    sensitive_log=True,
                    eth_address=account,
                    token_address=token.ethereum_address,
                    token_symbol=token.decimals,
                )
                token_amount = FVal(token_contract.functions.balanceOf(account).call())
                if token_amount != 0:
                    balances[account] = token_amount / (FVal(10) ** FVal(token.decimals))
                log.debug(
                    'Ethereum node result for token balance',
                    sensitive_log=True,
                    eth_address=account,
                    token_address=token.ethereum_address,
                    token_symbol=token.symbol,
                    amount=token_amount,
                )
        else:
            for account in accounts:
                log.debug(
                    'Querying Etherscan for token balance',
                    sensitive_log=True,
                    eth_address=account,
                    token_address=token.ethereum_address,
                    token_symbol=token.symbol,
                )
                resp = request_get_dict(
                    'https://api.etherscan.io/api?module=account&action='
                    'tokenbalance&contractaddress={}&address={}'.format(
                        token.ethereum_address,
                        account,
                    ))
                if resp['status'] != 1:
                    raise ValueError(
                        'Failed to query etherscan for {} token balance of {}'.format(
                            token.symbol,
                            account,
                        ))
                token_amount = FVal(resp['result'])
                if token_amount != 0:
                    balances[account] = token_amount / (FVal(10) ** FVal(token.decimals))
                log.debug(
                    'Etherscan result for token balance',
                    sensitive_log=True,
                    eth_address=account,
                    token_address=token.ethereum_address,
                    token_symbol=token.symbol,
                    amount=token_amount,
                )

        return balances

    def get_token_balance(
            self,
            token: EthereumToken,
            account: ChecksumEthAddress,
    ) -> FVal:
        res = self.get_multitoken_balance(token=token, accounts=[account])
        return res.get(account, FVal(0))

    def get_block_by_number(self, num: int) -> Optional[Dict[str, Any]]:
        if not self.connected:
            return None

        return self.web3.eth.getBlock(num)  # pylint: disable=no-member
