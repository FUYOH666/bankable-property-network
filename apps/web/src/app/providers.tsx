"use client";

import "@rainbow-me/rainbowkit/styles.css";

import {RainbowKitProvider, getDefaultConfig, lightTheme} from "@rainbow-me/rainbowkit";
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {ReactNode, useState} from "react";
import {WagmiProvider, http} from "wagmi";
import {baseSepolia} from "wagmi/chains";

import {ATTESTRWA} from "@/lib/contracts";

const wagmiConfig = getDefaultConfig({
  appName: "AttestRWA",
  projectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID ?? "attestrwa-demo",
  chains: [baseSepolia],
  transports: {
    [baseSepolia.id]: http(
      ATTESTRWA.chainId === baseSepolia.id
        ? (process.env.NEXT_PUBLIC_RPC_URL ?? "http://127.0.0.1:8545")
        : undefined,
    ),
  },
  ssr: true,
});

export function Providers({children}: {children: ReactNode}) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <WagmiProvider config={wagmiConfig}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider theme={lightTheme({accentColor: "#1abc9c"})} modalSize="compact">
          {children}
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
