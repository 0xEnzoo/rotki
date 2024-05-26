from rotkehlchen.chain.evm.types import NodeName, WeightedNode, string_to_evm_address
from rotkehlchen.constants import ONE
from rotkehlchen.fval import FVal
from rotkehlchen.types import SupportedBlockchain, Timestamp, deserialize_evm_tx_hash

BINANCE_SMART_CHAIN_ETHERSCAN_NODE_NAME = 'binance smart chain etherscan'
BINANCE_SMART_CHAIN_GENESIS = Timestamp(1598664248)
BINANCE_SMART_CHAIN_ETHERSCAN_NODE = WeightedNode(
    node_info=NodeName(
        name=BINANCE_SMART_CHAIN_ETHERSCAN_NODE_NAME,
        endpoint='',
        owned=False,
        blockchain=SupportedBlockchain.BINANCE_SMART_CHAIN,
    ),
    weight=ONE,
    active=True,
)

ARCHIVE_NODE_CHECK_ADDRESS = string_to_evm_address('0x41bc0ead8466c6f6430a2bbbdeabf368cbd5fdf5')
ARCHIVE_NODE_CHECK_BLOCK = 406672
ARCHIVE_NODE_CHECK_EXPECTED_BALANCE = FVal('0.098')

PRUNED_NODE_CHECK_TX_HASH = deserialize_evm_tx_hash('0xde5b5e84ea807d2122cf279b203ea82ca070c2329c7cd29a3ef00dc8fa4b4d73')  # noqa: E501
