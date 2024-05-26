import logging
from typing import TYPE_CHECKING

from rotkehlchen.chain.evm.decoding.base import BaseDecoderTools
from rotkehlchen.chain.evm.decoding.decoder import EVMTransactionDecoder
from rotkehlchen.constants.assets import A_BNB
from rotkehlchen.logging import RotkehlchenLogsAdapter
from rotkehlchen.types import ChecksumEvmAddress

if TYPE_CHECKING:
    from rotkehlchen.chain.binance_smart_chain.node_inquirer import BinanceSmartChainInquirer
    from rotkehlchen.chain.binance_smart_chain.transactions import BinanceSmartChainTransactions
    from rotkehlchen.db.dbhandler import DBHandler

logger = logging.getLogger(__name__)
log = RotkehlchenLogsAdapter(logger)


class BinanceSmartChainTransactionDecoder(EVMTransactionDecoder):

    def __init__(
            self,
            database: 'DBHandler',
            binance_smart_chain_inquirer: 'BinanceSmartChainInquirer',
            transactions: 'BinanceSmartChainTransactions',
    ):
        super().__init__(
            database=database,
            evm_inquirer=binance_smart_chain_inquirer,
            transactions=transactions,
            value_asset=A_BNB.resolve_to_asset_with_oracles(),
            event_rules=[],
            misc_counterparties=[],
            base_tools=BaseDecoderTools(
                database=database,
                evm_inquirer=binance_smart_chain_inquirer,
                is_non_conformant_erc721_fn=self._is_non_conformant_erc721,
                address_is_exchange_fn=self._address_is_exchange,
            ),
        )

    # -- methods that need to be implemented by child classes --

    @staticmethod
    def _is_non_conformant_erc721(address: ChecksumEvmAddress) -> bool:  # pylint: disable=unused-argument
        return False

    @staticmethod
    def _address_is_exchange(address: ChecksumEvmAddress) -> str | None:  # pylint: disable=unused-argument
        return None
