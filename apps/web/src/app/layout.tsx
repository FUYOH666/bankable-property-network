import type {Metadata} from "next";
import "./globals.css";

import {Providers} from "./providers";

export const metadata: Metadata = {
  title: "AttestRWA — Settlement Attestation Layer for RWA",
  description:
    "On-chain compliance bridge that turns bank verification rules into machine-verifiable EAS attestations, so stablecoin payments for real-world assets release only when the deal is bank-grade.",
  openGraph: {
    title: "AttestRWA",
    description:
      "Settlement Attestation Layer for RWA on Base Sepolia (EAS + programmable escrow).",
    type: "website",
  },
};

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
