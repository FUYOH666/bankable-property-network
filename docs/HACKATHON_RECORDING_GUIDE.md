# Hackathon Recording Guide — AttestRWA

> Record a clean, jury-ready demo of AttestRWA in 60–90 seconds, fully
> self-contained on your laptop — no testnet ETH faucet, no Vercel, no
> Render. The Anvil fork inherits **real Base Sepolia bytecode** for the
> EAS protocol at the canonical address `0x4200…0021`, so every
> attestation in the demo runs through the same code that production
> would, just on a local chain.
>
> Two recording paths are offered. Pick **A** if you want a cinematic
> wallet/UI flow; pick **B** if you want a 100% reliable terminal-only
> recording. **B is recommended for the hackathon submission** because it
> has zero browser/wallet variables.

## What you need installed

| Tool | Why | Check |
|------|-----|-------|
| Foundry (`forge`, `cast`, `anvil`) 1.7+ | Dev fork + Solidity build | `forge --version` |
| `uv` 0.5+ | Backend Python runtime | `uv --version` |
| `pnpm` 9+ (only for path A) | Web dev server | `pnpm --version` |
| Screen recorder | macOS: `Cmd+Shift+5`. Linux: `obs-studio`. Windows: `Win+Alt+R`. | — |
| Microphone (optional) | Voiceover. Or add captions in post-production. | — |

If any of those are missing: `CONTRIBUTING.md` § "Quick start" has the
install commands.

## One-time prep (do this once before recording, ~2 minutes)

```bash
# From the repo root
./scripts/dev-chain.sh        # boots Anvil fork + registers EAS schema
./scripts/deploy-contracts.sh # deploys MockUSDC + SettlementEscrow
```

You should see two summary blocks ending with addresses like
`0xeba5CEc…F6d4` (MockUSDC) and `0x54D49628…1D8` (SettlementEscrow). Keep
that terminal open.

If anything goes wrong, run `./scripts/stop-demo-mode.sh` and start over.

---

## Path A — Cinematic UI + wallet recording (≈90 seconds)

Slightly more complex; one wallet-config step required.

### A.0 — Configure MetaMask once

1. Open MetaMask → top-left network selector → **Add network manually**.
2. Fill:
   - Network name: `AttestRWA dev (Base Sepolia fork)`
   - RPC URL: `http://127.0.0.1:8545`
   - Chain ID: `84532`
   - Currency symbol: `ETH`
   - Block explorer: leave empty
3. Save and select that network.
4. Import the **buyer** test account: MetaMask → **Import account**:
   - Private key: `0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d`
   - This is Anvil default account #1, public test key, never use on mainnet.

### A.1 — Boot everything in one terminal command

```bash
./scripts/demo-mode.sh
```

End-of-output prints a `DEMO READY` block with URLs. Wait for it.

### A.2 — Open the screen for recording

- Browser tab 1: `http://127.0.0.1:3000/rwa-settlement-live`
- Browser tab 2 (optional): `http://127.0.0.1:8080/api/frame/attest?decision=approve`
- Terminal pinned at the bottom of the screen showing `demo-mode.sh` summary.

### A.3 — Recording sequence (90 seconds, six beats)

| t (s) | Beat | What you do | What viewer sees |
|------|------|-------------|------------------|
| 0–8  | Title  | Hold on the hero (`/`) page. | Big "AttestRWA" logo, hook line. |
| 8–18 | Connect | Click the rainbow **Connect** button → MetaMask → choose imported buyer account. | Wallet badge appears top-right. |
| 18–28| Happy 1 | Pick the **happy** scenario card. Click **1 · Mint mUSDC**, **2 · Approve**, **3 · Deposit**. | Activity log scrolls; buyer balance briefly drops to 0 after deposit. |
| 28–42| Happy 2 | Click **4 · Trigger attester**. After ~3 s, the right card flips green to APPROVE. Click **5 · Release**. | Decision card shows VERIFIED, payee balance jumps to 580 mUSDC. |
| 42–62| Reject  | Pick the **reject** scenario. Click 1→2→3→4 again. Decision card flips red to REJECTED. Click **5 · Refund**. | Buyer balance restored. Activity log shows reason `payee_not_verified`. |
| 62–82| Proof   | Switch to terminal. Run `cast code 0x4200000000000000000000000000000000000021 --rpc-url $DEV_RPC_URL \| wc -c` and `curl -s http://localhost:8080/attest/healthz`. | Numbers proving real EAS bytecode + healthy attester. |
| 82–90| Outro   | Hold on the live screen with both attestation UIDs visible. | Voiceover: "Open source, Apache-2.0, github.com/FUYOH666/attestrwa". |

### A.4 — Voiceover lines (read while recording)

> **0–8 s:** "AttestRWA — Settlement Attestation Layer for RWA. We turn
> bank verification rules into machine-verifiable on-chain attestations."
>
> **8–18 s:** "Connecting a buyer wallet to the local Base Sepolia fork.
> The EAS protocol bytecode here is forked from production."
>
> **18–28 s:** "Happy path — Bangkok Landmark deal, verified payee. Mint
> mock USDC, approve escrow, deposit."
>
> **28–42 s:** "The attester service signs an EAS SettlementApproval
> attestation on-chain. Escrow verifies it against the pinned schema, the
> trusted attester whitelist, the payee, the capital class — and
> releases."
>
> **42–62 s:** "Reject path — agent points to an impostor payee, SRL
> Holding 2026. The attester signs the attestation with payeeVerified
> false. Escrow refuses release. Buyer is refunded."
>
> **62–82 s:** "All of this against the canonical EAS contract. No mocks.
> Foundry tests, slither clean, 62 backend tests — all passing on every
> commit."
>
> **82–90 s:** "Open source, Apache-2.0. AttestRWA — composable
> compliance for RWA settlements."

---

## Path B — Terminal-only recording (≈60 seconds, recommended)

100% reliable. No wallet, no browser. Two `e2e_*.sh` scripts narrate
themselves with coloured `[ok]` markers.

### B.1 — Boot everything in one command

```bash
./scripts/demo-mode.sh
```

Wait for `DEMO READY`. Now the chain is up and contracts are deployed.

### B.2 — Recording sequence (60 seconds)

| t (s) | Beat | Command to type | What viewer sees |
|------|------|-----------------|------------------|
| 0–6  | Title | _(no command — voiceover only)_ | Terminal prompt with the bold "DEMO READY" block from `demo-mode.sh`. |
| 6–8  | Pose | `cat .dev-chain.state | grep ESCROW` | One line printing the live escrow address. |
| 8–28 | Happy E2E | `./scripts/e2e_rwa_flow.sh` | The 5-step flow with green `[ok]` markers, ending with `Payee final bal: 580000000`. |
| 28–48| Reject E2E | `./scripts/e2e_rwa_reject.sh` | The reject flow ending with `Buyer balance: 280000000 (refunded)`. |
| 48–55| Proof | `cast code 0x4200000000000000000000000000000000000021 --rpc-url http://127.0.0.1:8545 | wc -c` | Number `4121` — proves real EAS bytecode is live on the fork. |
| 55–60| Outro | `git log --oneline --decorate -8` | Eight commits ending at `tag: v1.0.0`. |

### B.3 — Voiceover lines (timed)

> **0–6 s:** "AttestRWA — Settlement Attestation Layer for RWA. The full
> stack runs on a local Anvil fork of Base Sepolia. The EAS protocol at
> this address is the real one, forked from production."
>
> **6–28 s:** "Happy path. Buyer deposits 580 mock USDC. Off-chain
> attester service decides, signs, broadcasts an EAS SettlementApproval
> attestation. Escrow verifies and releases to the verified Bangkok
> Landmark payee."
>
> **28–48 s:** "Reject path. Agent points to an impostor — SRL Holding
> 2026. Attester signs with payeeVerified false. Escrow refuses release.
> Buyer refund through the attester-signed reject branch."
>
> **48–55 s:** "Four kilobytes of real EAS bytecode at the canonical Base
> address. No mocks."
>
> **55–60 s:** "Open source. Apache-2.0. github.com/FUYOH666/
> attestrwa."

### B.4 — One-liner backup (if anything misbehaves mid-recording)

```bash
./scripts/stop-demo-mode.sh && ./scripts/demo-mode.sh && ./scripts/e2e_rwa_flow.sh && ./scripts/e2e_rwa_reject.sh
```

That single line resets and replays both flows in ~90 seconds. If
recording goes south, run it once into a clean terminal and capture in
one take.

---

## Hand-off checklist before submission

- [x] `./scripts/demo-mode.sh` starts cleanly on the recording machine.
- [x] `./scripts/e2e_rwa_flow.sh` exits 0.
- [x] `./scripts/e2e_rwa_reject.sh` exits 0.
- [x] Recording uploaded: <https://youtube.com/shorts/BipB2qPzZz0>
      (YouTube Shorts, vertical 1738×1942, 85 s, English captions
      toggle-able from `docs/recording-subtitles.srt`).
- [x] Video URL added to `README.md` hero.
- [x] CHANGELOG entry mentions the recorded run + UIDs.
- [x] No real private keys in the recording (Anvil default test
      accounts only, public mnemonic, never use on mainnet).

## Known limitations to call out (transparency)

- Demo runs on a local Anvil fork. Real Base Sepolia deploy is gated on
  one Alchemy / Coinbase faucet step that we will run after submission.
- Mock Chainalysis taint signals: the wallet-taint module uses synthetic
  data from `data/synthetic/rwa/wallets.json`. Production replaces this
  with Chainalysis / TRM Labs.
- Attester key in the demo is the public Anvil test key. Production
  attesters keep their key in an HSM.
- Mainnet deploy is intentionally not in this version — see
  `docs/ROADMAP.md` § "Q4 2026 — first bank attester pilot".

These are not weaknesses — they are deliberate non-goals for the
hackathon stage and are documented across the repo.

## If you only have 30 seconds

Record only **B.1 + B.3**:

```bash
./scripts/demo-mode.sh && ./scripts/e2e_rwa_flow.sh && ./scripts/e2e_rwa_reject.sh
```

That one terminal capture, with a 30-second voiceover summarising the
hook + happy + reject + non-goals, is enough for SEA Blockchain Week
jury sieve rounds. Anything longer is bonus.
