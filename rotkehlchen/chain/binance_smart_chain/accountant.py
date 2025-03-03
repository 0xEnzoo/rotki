from typing import TYPE_CHECKING

from rotkehlchen.chain.evm.accounting.aggregator import EVMAccountingAggregator

if TYPE_CHECKING:
    from rotkehlchen.user_messages import MessagesAggregator

    from .node_inquirer import BinanceSmartChainInquirer


class BinanceSmartChainAccountingAggregator(EVMAccountingAggregator):

    def __init__(
            self,
            node_inquirer: 'BinanceSmartChainInquirer',
            msg_aggregator: 'MessagesAggregator',
    ) -> None:
        super().__init__(
            node_inquirer=node_inquirer,
            msg_aggregator=msg_aggregator,
            modules_path='rotkehlchen.chain.binance_smart_chain.modules',
        )
