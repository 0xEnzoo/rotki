import { Blockchain } from '@rotki/common/lib/blockchain';
import { EvmTokenKind } from '@rotki/common/lib/data';

const BtcChains = [Blockchain.BTC, Blockchain.BCH] as const;
const RestChains = [
  Blockchain.KSM,
  Blockchain.DOT,
  Blockchain.AVAX,
  Blockchain.OPTIMISM,
  Blockchain.POLYGON_POS,
  Blockchain.ARBITRUM_ONE,
  Blockchain.BASE,
  Blockchain.GNOSIS,
  Blockchain.SCROLL,
  Blockchain.ZKSYNC_LITE,
  Blockchain.BINANCE_SMART_CHAIN,
] as const;

export type BtcChains = (typeof BtcChains)[number];

export type RestChains = (typeof RestChains)[number];

export function isBtcChain(chain: string): chain is BtcChains {
  return BtcChains.includes(chain as any);
}

export function isRestChain(chain: string): chain is RestChains {
  return RestChains.includes(chain as any);
}

export function isBlockchain(chain: string): chain is Blockchain {
  return Object.values(Blockchain).includes(chain as any);
}

export interface EvmTokenData {
  identifier: EvmTokenKind;
  label: string;
}

export const evmTokenKindsData: EvmTokenData[] = [
  {
    identifier: EvmTokenKind.ERC20,
    label: 'ERC20',
  },
  {
    identifier: EvmTokenKind.ERC721,
    label: 'ERC721',
  },
];
