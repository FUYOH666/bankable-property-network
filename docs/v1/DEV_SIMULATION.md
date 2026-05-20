# Dev Simulation — Full Local AttestRWA Stack

> One-command full simulation of the AttestRWA on-chain flow. No faucet,
> no testnet ETH, no manual schema registration on easscan. Everything
> happens on a **local Anvil fork of Base Sepolia**, which inherits real
> EAS protocol bytecode at the canonical addresses.
>
> When you want public visibility (BaseScan, Dune, Farcaster) for the
> hackathon submission, the same scripts switch to real Base Sepolia by
> flipping a single environment variable (`DEV_FORK_URL` →
> `DEV_RPC_URL=https://sepolia.base.org`). One faucet request (60 seconds)
> is the only manual step needed at that point.

## What's simulated

| Layer | Simulation | Reality |
|-------|------------|---------|
| EVM | Anvil node | Same EVM rules as Base Sepolia |
| EAS protocol | **Real bytecode forked from Base Sepolia** at `0x4200…0021` and `0x4200…0020` | Behaves identically — no mocking |
| Stablecoin | Mock USDC deployed by us (Week 2) | Same ERC-20 interface as canonical USDC |
| Wallet | Anvil default account #0 (10000 ETH preloaded) | Equivalent to a funded EOA |
| Block production | 2-second blocks (configurable) | Realistic UX timing |
| Chain ID | 84532 (Base Sepolia) | Same |
| Gas pricing | Inherits forked state, cheap | Same as Base Sepolia |

## What's not simulated (yet)

- Public BaseScan visibility (only on real testnet — Week 3 switch).
- Public EAS Scan visibility (only on real testnet).
- Dune dashboard population (needs real testnet indexer).
- Farcaster Frame (works on local URL, but viral effect needs public URL).

## Quickstart

```bash
# 1. One-time foundry install
curl -L https://foundry.paradigm.xyz | bash
source ~/.zshenv      # or open a new terminal
foundryup

# 2. Start dev chain + register schema (idempotent)
./scripts/dev-chain.sh

# Output ends with a status block:
#   RPC URL          : http://127.0.0.1:8545
#   Chain ID         : 84532
#   EAS address      : 0x4200000000000000000000000000000000000021
#   SchemaRegistry   : 0x4200000000000000000000000000000000000020
#   Schema UID       : 0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96
#   Attester address : 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266

# 3. (Later weeks) Use cast / forge / API against http://127.0.0.1:8545

# 4. Stop when done
./scripts/stop-dev-chain.sh
```

## Architecture

```text
+------------------------+        +------------------------+
| Buyer wallet (Anvil 1) |        | Attester (Anvil 0)     |
| 10000 ETH              |        | 10000 ETH, signs EAS   |
+----------+-------------+        +-----------+------------+
           |                                  |
           | sends Mock USDC                  | writes attestation
           v                                  v
+---------------------------------------------------------+
| Anvil node (fork of Base Sepolia, port 8545)            |
|                                                          |
|  +----------------+      +------------------------+      |
|  | SettlementEscrow|<-->| EAS @ 0x4200…0021      |      |
|  | (Week 2 deploy)|     | SchemaRegistry @ …0020  |      |
|  +----------------+     +------------------------+      |
+---------------------------------------------------------+
           ^                                  ^
           | watches events                   | queries
           |                                  |
+----------+-------------+        +-----------+------------+
| Next.js single screen  |        | FastAPI attester       |
| (wagmi/viem)           |        | EAS client + RAG + DSL |
+------------------------+        +------------------------+
```

## Anvil default accounts (test mnemonic)

> Mnemonic: `test test test test test test test test test test test junk`
> **PUBLIC TEST KEY — never deploy with these on mainnet.**

| # | Address | Role in AttestRWA |
|---|---------|-------------------|
| 0 | `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266` | **Attester** (signs EAS attestations) |
| 1 | `0x70997970C51812dc3A010C7d01b50e0d17dc79C8` | **Buyer** (deposits Mock USDC) |
| 2 | `0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC` | **Developer treasury** (receives released funds) |
| 3 | `0x90F79bf6EB2c4f870365E785982E1f101E93b906` | **Wrong payee** (`SRL Holding 2026` — for reject demo) |
| 4 | `0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65` | **Compliance officer** (manual escalation, future) |
| 5–9 | … | Reserved for future scenarios |

Use Anvil cli to print full list with private keys:

```bash
# When dev-chain.sh runs, head of /tmp/attestrwa-anvil.log shows all 10
# addresses with their private keys. Keep that file out of git.
head -100 /tmp/attestrwa-anvil.log
```

## State file

`scripts/dev-chain.sh` writes a `.dev-chain.state` file in the repo root
with all the addresses, UIDs, and the dev attester key. **This file is
gitignored.** Source it from any script:

```bash
source .dev-chain.state
echo "$EAS_SCHEMA_UID_SETTLEMENT_APPROVAL"
```

## Smoke test (manual)

After starting the dev chain, you can manually attest a settlement using
`cast`:

```bash
source .dev-chain.state

# Compose EAS attestation data (10 fields, packed as ABI encoded payload)
DATA=$(cast abi-encode \
  "f(bytes32,address,address,address,uint256,uint8,bytes32,string,uint64,bool)" \
  0x1111111111111111111111111111111111111111111111111111111111111111 \
  "$ATTESTER_ADDRESS" \
  0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC \
  0x0000000000000000000000000000000000000000 \
  500000000000 \
  0 \
  0x2222222222222222222222222222222222222222222222222222222222222222 \
  TH \
  $(($(date +%s) + 86400)) \
  true)

# Submit attestation via EAS.attest((SchemaUID, (recipient, expiration,
# revocable, refUID, data, value)))
echo "Submitting attestation…"
# (full call composed in Week 2 attester service — left as a placeholder
# here because cast doesn't natively encode complex struct args)
```

For the full attestation submission flow with structured arguments, see
`apps/api/src/app/services/eas_client.py` (Week 2 implementation).

## Switching to real Base Sepolia (Week 3 production deploy)

When the contracts and UI are stable, switch from local fork to real
testnet:

```bash
# 1. Stop the local fork
./scripts/stop-dev-chain.sh

# 2. Generate a fresh attester wallet (production-style, never commit)
cast wallet new
# Save the address + private key in .env (NOT .env.example)

# 3. Fund the attester wallet on real Base Sepolia
#    https://www.alchemy.com/faucets/base-sepolia
#    https://faucet.quicknode.com/base/sepolia

# 4. Register the schema on real Base Sepolia EAS
cast send 0x4200000000000000000000000000000000000020 \
  "register(string,address,bool)" \
  "bytes32 dealId, address attester, address payeeAddress, address tokenAddress, uint256 amount, uint8 capitalClass, bytes32 evidenceHash, string jurisdiction, uint64 expiresAt, bool payeeVerified" \
  0x0000000000000000000000000000000000000000 \
  true \
  --rpc-url https://sepolia.base.org \
  --private-key $REAL_ATTESTER_PRIVATE_KEY

# 5. Read the Schema UID from the Registered event (or from easscan UI)
# 6. Update .env with REAL Schema UID and REAL attester address
# 7. Deploy SettlementEscrow.sol + MockUSDC.sol against the real network
#    (forge script script/Deploy.s.sol --rpc-url https://sepolia.base.org --broadcast --verify)
# 8. Submit hackathon URLs with public BaseScan + EAS Scan links
```

The entire codebase (contracts, attester service, UI) is RPC-agnostic — it
reads `DEV_RPC_URL` from `.env`. So this switch is a one-line
configuration change plus the manual faucet step.

## Reset the dev chain

To start fresh (e.g. test re-registration, new deploy):

```bash
./scripts/stop-dev-chain.sh
./scripts/dev-chain.sh
```

State on the fork is ephemeral — every restart re-syncs from real Base
Sepolia state at the current block.

## Why this beats faucet + easscan UX

| Pain on real testnet | Solution on dev chain |
|----------------------|------------------------|
| Faucet rate-limits, captchas | Anvil default accounts have 10000 ETH |
| Schema registration via UI requires wallet popup | `cast send` from CLI in one shot |
| Block confirmation latency (~2–10 s) | Local 2 s blocks, deterministic |
| Network errors during demo | Zero dependency on external RPC |
| Re-runnable demo | Restart chain → reset state in 8 seconds |

The trade-off: nothing is publicly visible until the Week 3 real-testnet
switch. We accept that — development velocity is worth more than
intermediate public visibility.
