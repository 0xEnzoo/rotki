import logging
from typing import TYPE_CHECKING, Literal, cast

from eth_typing import BlockNumber

from rotkehlchen.chain.constants import DEFAULT_EVM_RPC_TIMEOUT
from rotkehlchen.chain.evm.contracts import EvmContracts
from rotkehlchen.chain.evm.node_inquirer import EvmNodeInquirer
from rotkehlchen.chain.evm.types import string_to_evm_address
from rotkehlchen.constants.assets import A_BNB
from rotkehlchen.fval import FVal
from rotkehlchen.greenlets.manager import GreenletManager
from rotkehlchen.logging import RotkehlchenLogsAdapter
from rotkehlchen.types import ChainID, ChecksumEvmAddress, EVMTxHash, SupportedBlockchain

from .constants import (
    ARCHIVE_NODE_CHECK_ADDRESS,
    ARCHIVE_NODE_CHECK_BLOCK,
    ARCHIVE_NODE_CHECK_EXPECTED_BALANCE,
    BINANCE_SMART_CHAIN_ETHERSCAN_NODE,
    BINANCE_SMART_CHAIN_ETHERSCAN_NODE_NAME,
    PRUNED_NODE_CHECK_TX_HASH,
)
from .etherscan import BinanceSmartChainEtherscan

if TYPE_CHECKING:
    from rotkehlchen.db.dbhandler import DBHandler

logger = logging.getLogger(__name__)
log = RotkehlchenLogsAdapter(logger)


class BinanceSmartChainInquirer(EvmNodeInquirer):

    def __init__(
            self,
            greenlet_manager: GreenletManager,
            database: 'DBHandler',
            rpc_timeout: int = DEFAULT_EVM_RPC_TIMEOUT,
    ) -> None:
        etherscan = BinanceSmartChainEtherscan(
            database=database,
            msg_aggregator=database.msg_aggregator,
        )
        contracts = EvmContracts[Literal[ChainID.BINANCE_SMART_CHAIN]](chain_id=ChainID.BINANCE_SMART_CHAIN)
        super().__init__(
            greenlet_manager=greenlet_manager,
            database=database,
            etherscan=etherscan,
            blockchain=SupportedBlockchain.BINANCE_SMART_CHAIN,
            etherscan_node=BINANCE_SMART_CHAIN_ETHERSCAN_NODE,
            etherscan_node_name=BINANCE_SMART_CHAIN_ETHERSCAN_NODE_NAME,
            contracts=contracts,
            rpc_timeout=rpc_timeout,
            contract_multicall=contracts.contract(string_to_evm_address('0xcA11bde05977b3631167028862bE2a173976CA11')),
            contract_scan=contracts.contract(string_to_evm_address('0xd752085e287752a692b1ce5ec38943ee7e082c8c')),
            native_token=A_BNB.resolve_to_crypto_asset(),
        )
        self.etherscan = cast(BinanceSmartChainEtherscan, self.etherscan)

    # -- Implementation of EvmNodeInquirer base methods --

    def query_highest_block(self) -> BlockNumber:
        block_number = self.etherscan.get_latest_block_number()
        log.debug('Binance Smart Chain highest block result', block=block_number)
        return BlockNumber(block_number)

    def _get_pruned_check_tx_hash(self) -> EVMTxHash:
        return PRUNED_NODE_CHECK_TX_HASH

    def _get_archive_check_data(self) -> tuple[ChecksumEvmAddress, int, FVal]:
        return (
            ARCHIVE_NODE_CHECK_ADDRESS,
            ARCHIVE_NODE_CHECK_BLOCK,
            ARCHIVE_NODE_CHECK_EXPECTED_BALANCE,
        )
