from typing import TYPE_CHECKING

from rotkehlchen.chain.evm.tokens import EvmTokens
from rotkehlchen.constants.assets import A_BNB
from rotkehlchen.types import ChecksumEvmAddress

if TYPE_CHECKING:
    from rotkehlchen.db.dbhandler import DBHandler

    from .node_inquirer import BinanceSmartChainInquirer


class BinanceSmartChainTokens(EvmTokens):

    def __init__(self, database: 'DBHandler', binance_smart_chain_inquirer: 'BinanceSmartChainInquirer') -> None:
        super().__init__(database=database, evm_inquirer=binance_smart_chain_inquirer)

    # -- methods that need to be implemented per chain
    def _per_chain_token_exceptions(self) -> set[ChecksumEvmAddress]:
        return {A_BNB.resolve_to_evm_token().evm_address}
