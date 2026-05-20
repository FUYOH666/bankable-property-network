// AttestRWA — on-chain ABIs + addresses used by the wallet-connect UI.
//
// Addresses default to the dev-fork deployment captured by
// scripts/deploy-contracts.sh. Override via NEXT_PUBLIC_* env on Vercel
// once the real Base Sepolia deploy lands.

import {Address} from "viem";

export const ATTESTRWA = {
  chainId: Number(process.env.NEXT_PUBLIC_CHAIN_ID ?? "84532"),
  mockUsdc: (process.env.NEXT_PUBLIC_MOCK_USDC_ADDRESS ??
    "0xeba5CEc9257045Df0B44eA784F9a7Fa07DeeF6d4") as Address,
  escrow: (process.env.NEXT_PUBLIC_ESCROW_ADDRESS ??
    "0x54D4962847bf85AB71a1Fc984510dc12D3feA1D8") as Address,
  attester: (process.env.NEXT_PUBLIC_ATTESTER_ADDRESS ??
    "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266") as Address,
  schemaUid: (process.env.NEXT_PUBLIC_EAS_SCHEMA_UID ??
    "0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96") as `0x${string}`,
  attesterApi: process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8080",
  basescanBaseUrl: process.env.NEXT_PUBLIC_BASESCAN_URL ?? "https://sepolia.basescan.org",
  easScanBaseUrl: process.env.NEXT_PUBLIC_EAS_SCAN_URL ?? "https://base-sepolia.easscan.org",
} as const;

// Minimal ABIs (only what the UI needs)

export const mockUsdcAbi = [
  {
    type: "function",
    stateMutability: "nonpayable",
    name: "mint",
    inputs: [
      {name: "to", type: "address"},
      {name: "amount", type: "uint256"},
    ],
    outputs: [],
  },
  {
    type: "function",
    stateMutability: "nonpayable",
    name: "approve",
    inputs: [
      {name: "spender", type: "address"},
      {name: "amount", type: "uint256"},
    ],
    outputs: [{name: "", type: "bool"}],
  },
  {
    type: "function",
    stateMutability: "view",
    name: "balanceOf",
    inputs: [{name: "owner", type: "address"}],
    outputs: [{name: "", type: "uint256"}],
  },
  {
    type: "function",
    stateMutability: "view",
    name: "allowance",
    inputs: [
      {name: "owner", type: "address"},
      {name: "spender", type: "address"},
    ],
    outputs: [{name: "", type: "uint256"}],
  },
] as const;

export const escrowAbi = [
  {
    type: "function",
    stateMutability: "nonpayable",
    name: "deposit",
    inputs: [
      {name: "dealId", type: "bytes32"},
      {name: "payee", type: "address"},
      {name: "token", type: "address"},
      {name: "amount", type: "uint256"},
      {name: "deadline", type: "uint64"},
    ],
    outputs: [],
  },
  {
    type: "function",
    stateMutability: "nonpayable",
    name: "release",
    inputs: [
      {name: "dealId", type: "bytes32"},
      {name: "attestationUid", type: "bytes32"},
    ],
    outputs: [],
  },
  {
    type: "function",
    stateMutability: "nonpayable",
    name: "refund",
    inputs: [
      {name: "dealId", type: "bytes32"},
      {name: "attestationUid", type: "bytes32"},
    ],
    outputs: [],
  },
  {
    type: "function",
    stateMutability: "view",
    name: "getDeal",
    inputs: [{name: "dealId", type: "bytes32"}],
    outputs: [
      {
        name: "",
        type: "tuple",
        components: [
          {name: "buyer", type: "address"},
          {name: "payee", type: "address"},
          {name: "token", type: "address"},
          {name: "amount", type: "uint256"},
          {name: "deadline", type: "uint64"},
          {name: "released", type: "bool"},
          {name: "refunded", type: "bool"},
        ],
      },
    ],
  },
  {
    type: "event",
    name: "Deposited",
    anonymous: false,
    inputs: [
      {indexed: true, name: "dealId", type: "bytes32"},
      {indexed: true, name: "buyer", type: "address"},
      {indexed: true, name: "payee", type: "address"},
      {indexed: false, name: "token", type: "address"},
      {indexed: false, name: "amount", type: "uint256"},
      {indexed: false, name: "deadline", type: "uint64"},
    ],
  },
  {
    type: "event",
    name: "SettlementReleased",
    anonymous: false,
    inputs: [
      {indexed: true, name: "dealId", type: "bytes32"},
      {indexed: true, name: "payee", type: "address"},
      {indexed: false, name: "amount", type: "uint256"},
      {indexed: false, name: "attestationUid", type: "bytes32"},
    ],
  },
  {
    type: "event",
    name: "SettlementRefunded",
    anonymous: false,
    inputs: [
      {indexed: true, name: "dealId", type: "bytes32"},
      {indexed: true, name: "buyer", type: "address"},
      {indexed: false, name: "amount", type: "uint256"},
      {indexed: false, name: "reason", type: "string"},
    ],
  },
] as const;

export interface AttestResponse {
  decision: "approve" | "reject";
  deal_id: `0x${string}`;
  capital_class: number;
  payee_verified: boolean;
  reasons: string[];
  rule_results: {rule_id: string; passed: boolean; explanation: string}[];
  taint: {
    wallet: string;
    capital_class: number;
    signals: string[];
    explanation: string;
  } | null;
  evidence_hash: `0x${string}`;
  expires_at: number;
  attestation_uid: `0x${string}` | null;
  tx_hash: `0x${string}` | null;
  block_number: number | null;
  gas_used: number | null;
  chain_id: number | null;
  eas_explorer_url: string | null;
  explanation: string;
}

export const DEMO_SCENARIOS = {
  happy: {
    label: "Happy path — Bangkok Landmark, verified payee, green capital",
    developerId: "developer-bangkok-landmark",
    payee: "0x976EA74026E726554dB657fA54763abd0C3a0aa9" as Address,
    amount: 580_000_000n, // 580 USDC (6 decimals)
    expected: "approve" as const,
  },
  rejectPayee: {
    label: "Reject — instructed payee impostor SRL Holding 2026",
    developerId: "siam-riverside-living",
    payee: "0x90F79bf6EB2c4f870365E785982E1f101E93b906" as Address,
    amount: 280_000_000n,
    expected: "reject" as const,
  },
} as const;

export type ScenarioKey = keyof typeof DEMO_SCENARIOS;
