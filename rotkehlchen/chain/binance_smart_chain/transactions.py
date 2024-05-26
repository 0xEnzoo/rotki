from typing import TYPE_CHECKING

from rotkehlchen.chain.evm.transactions import EvmTransactions

if TYPE_CHECKING:
    from rotkehlchen.db.dbhandler import DBHandler

    from .node_inquirer import BinanceSmartChainInquirer


class BinanceSmartChainTransactions(EvmTransactions):

    def __init__(
            self,
            binance_smart_chain_inquirer: 'BinanceSmartChainInquirer',
            database: 'DBHandler',
    ) -> None:
        super().__init__(evm_inquirer=binance_smart_chain_inquirer, database=database)
