import { createClient } from "viem";
import { createConfig, http } from "wagmi";
import {
  anvil,
  arbitrum,
  arbitrumGoerli,
  base,
  baseSepolia,
  mainnet,
  optimism,
  optimismGoerli,
  sepolia,
} from "wagmi/chains";
import { coinbaseWallet, injected, walletConnect } from "wagmi/connectors";

export const config = createConfig({
  chains: [
    anvil,
    mainnet,
    sepolia,
    arbitrum,
    arbitrumGoerli,
    optimismGoerli,
    optimism,
    base,
    baseSepolia,
  ],
  connectors: [
    injected(),
    coinbaseWallet(),
    walletConnect({ projectId: import.meta.env.VITE_WC_PROJECT_ID }),
  ],
  client({ chain }) {
    return createClient({ chain, transport: http() });
  },
});

declare module "wagmi" {
  interface Register {
    config: typeof config;
  }
}
