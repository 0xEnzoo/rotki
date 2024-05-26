from typing import TYPE_CHECKING

from rotkehlchen.chain.evm.manager import EvmManager

from .accountant import BinanceSmartChainAccountingAggregator
from .decoding.decoder import BinanceSmartChainTransactionDecoder
from .tokens import BinanceSmartChainTokens
from .transactions import BinanceSmartChainTransactions

if TYPE_CHECKING:

    from .node_inquirer import BinanceSmartChainInquirer


class BinanceSmartChainManager(EvmManager):

    def __init__(
            self,
            node_inquirer: 'BinanceSmartChainInquirer',
    ) -> None:
        transactions = BinanceSmartChainTransactions(
            binance_smart_chain_inquirer=node_inquirer,
            database=node_inquirer.database,
        )
        super().__init__(
            node_inquirer=node_inquirer,
            transactions=transactions,
            tokens=BinanceSmartChainTokens(
                database=node_inquirer.database,
                binance_smart_chain_inquirer=node_inquirer,
            ),
            transactions_decoder=BinanceSmartChainTransactionDecoder(
                database=node_inquirer.database,
                binance_smart_chain_inquirer=node_inquirer,
                transactions=transactions,
            ),
            accounting_aggregator=BinanceSmartChainAccountingAggregator(
                node_inquirer=node_inquirer,
                msg_aggregator=transactions.msg_aggregator,
            ),
        )
        self.node_inquirer: BinanceSmartChainInquirer  # just to make the type specific
