# Brief — `scanovich.ai/seablockchainweek/` landing

> **For:** the agent / engineer who maintains `website-scanovich.ai`
> (separate repository at `~/development/ScanovichAI/website-scanovich.ai`).
> **Goal:** build a single static landing page at the URL
> `https://scanovich.ai/seablockchainweek/` that presents AttestRWA to
> SEA Blockchain Week 2026 jury and to follow-up investors / banks.
> **Tone:** institutional. We aim for the perception of a
> billion-dollar-class infrastructure company, not a crypto retail
> token launch.

## What AttestRWA is (one paragraph)

AttestRWA is the **Settlement Attestation Layer for RWA** — an on-chain
compliance bridge that turns bank verification rules into machine-
verifiable EAS (Ethereum Attestation Service) attestations, so that
stablecoin payments for real-world assets release only when the deal is
bank-grade. We do not tokenize property. We do not run our own KYC. We
do not issue our own stablecoin. We are the missing primitive between
RWA tokenization platforms (Centrifuge, Maple, RealT, Ondo, Polytrade)
and regulated banks. Live demo runs on Base Sepolia (forked locally
during the hackathon). License: Apache-2.0. Repository:
`github.com/FUYOH666/bankable-property-network`.

## Audience for this landing

1. **Hackathon jury** — SEA Blockchain Week 2026 panel. They scan the
   page in 30–60 seconds; the hero must land the wedge in one breath.
2. **Banks and regulated structures** — could become attesters in our
   roadmap. They need to see seriousness, audit posture, no token
   marketing.
3. **RWA tokenization platforms** — could become consumers of our
   attestations. They need to see composability and an open schema.
4. **Hiring / partnership inbound** — quick proof we are credible.

The page is **not** for retail crypto users.

## Brand voice and tone

- Calm, factual, infrastructural. Think Stripe / Modern Treasury / Tier
  1 banking partnership pages, not Uniswap-style maximalism.
- No emojis. No exclamation marks. No moonshots vocabulary.
- Numbers, addresses, and `monospace` text are part of the visual
  language — they signal substance.
- Mention "bank", "compliance", "settlement", "audit" liberally. Avoid
  "DeFi", "ape", "to the moon", "rugproof" entirely.
- One pitch line that should appear at least twice on the page:
  > "We do not tokenize property. We tokenize the fact that a bank
  > verified the deal."

## Visual direction (tech-agnostic)

- **Palette:** dark canvas (something between `#071015` and `#0b1220`),
  warm desaturated accents (`#1abc9c`-ish teal for confirmations,
  `#fbbf24`-ish amber for watch-states, `#fb7185`-ish red sparingly for
  reject states). High contrast typography. No gradients on text.
- **Typography:** modern grotesque sans for headings (e.g. Inter, Söhne,
  Geist), monospace for technical lines (e.g. JetBrains Mono, Berkeley
  Mono). Generous line-height. Headings under 60 chars.
- **Layout:** single page, max content width ~1180 px. Lots of white
  (well, dark) space. No carousels, no parallax stunts.
- **Imagery:** SVG-only. No stock photos, no founder portraits, no
  glowing crystals. Hash strings and contract addresses as decorative
  elements are encouraged.
- **Motion:** at most a single subtle fade-in per scroll section.
  Anything more is noise.

## URL structure

- Primary URL: `https://scanovich.ai/seablockchainweek/`
- Trailing slash matters; rewrite rules so `/seablockchainweek` →
  `/seablockchainweek/` (301).
- Sub-routes (optional, if static-site supports it):
  - `/seablockchainweek/security/` — could mirror `docs/SECURITY.md`.
  - `/seablockchainweek/comparison/` — could mirror `docs/COMPARISON.md`.
  - `/seablockchainweek/architecture/` — could mirror `docs/ARCHITECTURE.md`.
  These are optional and not required for the hackathon submission.

If the existing `scanovich.ai` site has a sectioned layout (Header /
Body / Footer with shared navigation), the AttestRWA pages should opt
out of the global header and footer where possible — the seablockchainweek
landing is a fully self-contained demo page; jury attention drops
sharply with shared navigation noise.

## Page structure (one scroll, six blocks)

### Block 1 — Hero (above the fold)

Top-left: small mark `AttestRWA · v1.0.0`. Optional small lockup
"Project of Aleksandr Mordvinov · SEA Blockchain Week 2026".

Centred:

- H1: `Settlement Attestation Layer for RWA`
- Subhead (≤ 22 words): `On-chain compliance bridge. Stablecoin payments for real-world assets release only when the deal is bank-grade.`
- Two primary CTAs side by side:
  - Primary: **Watch 60-second demo** → links to the hosted unlisted
    YouTube / Vimeo video URL (placeholder for now; insert when
    available).
  - Secondary: **Open the source** → links to `https://github.com/FUYOH666/bankable-property-network`.
- A single line of monospace metadata under the CTAs:
  - `EAS schema · 0x1f64ec96…f33aff   Base Sepolia · chain 84532   License · Apache-2.0`

### Block 2 — The wedge (the only argument we make)

Three short paragraphs, no bullet points yet:

1. RWA stablecoin settlements are growing 8× year-over-year in 2026.
2. Tokenization is solved. Compliance is not. Banks have no on-chain
   primitive to participate as verifiers.
3. AttestRWA is that primitive: a 10-field EAS schema plus a
   programmable escrow contract, wired to an off-chain attester service
   that runs bank verification rules.

End with the bold line:
> "We do not tokenize property. We tokenize the fact that a bank
> verified the deal."

### Block 3 — How it works (one mermaid-style diagram, four labeled steps)

Render either as a static SVG or as an inline mermaid graph. Steps:

1. **Buyer wallet** sends stablecoin to `SettlementEscrow`.
2. **Off-chain attester** runs Property Shield, capital classification,
   compliance DSL.
3. **EAS attestation** is signed and broadcast on-chain.
4. **Escrow** verifies the attestation against the pinned schema and
   the trusted attester whitelist; on `payeeVerified=true` and
   `capitalClass<2`, releases to the verified payee. Otherwise, the
   buyer can refund.

### Block 4 — Proof (audit posture)

A grid of four small cards, each with a single number plus a short
verb:

| Card | Number | Caption |
|---|---|---|
| Foundry tests | **33 / 33** | Unit, fuzz, invariants — green on every push. |
| Backend tests | **62 / 62** | Pytest covers attester, taint, DSL, frame. |
| Slither findings | **0** | Low / medium / high severity, fail-on=medium in CI. |
| Gas budget | **118,733** | `release()` max gas, under the 120k target. |

Right under the grid, a one-line link: "Full audit posture →
[`docs/SECURITY.md`](https://github.com/FUYOH666/bankable-property-network/blob/main/docs/SECURITY.md)".

### Block 5 — On-chain artefacts (the technical evidence)

Two sub-blocks side by side on desktop, stacked on mobile:

**Dev (Anvil fork of Base Sepolia)**

```text
EAS contract       0x4200000000000000000000000000000000000021
SchemaRegistry     0x4200000000000000000000000000000000000020
Schema UID         0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96
SettlementEscrow   0x54D4962847bf85AB71a1Fc984510dc12D3feA1D8
MockUSDC           0xeba5CEc9257045Df0B44eA784F9a7Fa07DeeF6d4
Attester EOA       0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
```

**Real Base Sepolia (deferred — see Roadmap)**

A short note: "Real-testnet deploy is one env var flip
(`DEV_RPC_URL=https://sepolia.base.org`); the schema UID is
deterministic and stays identical."

### Block 6 — Where this sits (mini comparison)

Six-column horizontal table or a small grid showing where AttestRWA
slots between tokenization platforms and banks. Use the data in
`docs/COMPARISON.md` § "At a glance" — pick three rows that matter most:

- "Asset tokenization" — they do, we don't.
- "Programmable compliance bridge" — only us.
- "Bank-attester model" — only us.

Right below: a single sentence — "We are the layer above tokenization
and below bank rails." Link to the full comparison page.

### Block 7 — Roadmap (one horizontal strip, four pills)

`Now (testnet)` → `Q3 2026 (first exchange pilot)` → `Q4 2026 (first
bank attester pilot, ASEAN)` → `2027 (mainnet, multi-jurisdiction)`.

Each pill clickable to anchor on the same page or to
`docs/ROADMAP.md` on GitHub.

### Block 8 — Footer

Three-column footer:

- **Source code** — repo URL.
- **Docs** — link list to PRODUCT_THESIS, ARCHITECTURE, ATTESTATION_SCHEMA,
  SECURITY, COMPARISON, ROADMAP on GitHub.
- **Contact** — `aleksandr@scanovich.ai` (or whatever email the user
  prefers); GitHub `@FUYOH666`.

Closing line, monospace, dim:
`Apache-2.0  ·  No tokens issued  ·  No mainnet deploy yet  ·  Hackathon submission`.

## SEO and metadata

- `<title>`: `AttestRWA — Settlement Attestation Layer for RWA · SEA Blockchain Week 2026`
- `<meta name="description">`: `On-chain compliance bridge for stablecoin real-world-asset settlements. EAS attestations + programmable escrow on Base Sepolia.`
- OpenGraph: `og:image` should be a 1200×630 PNG that mirrors the hero
  card. Until a custom image is produced, the SVG generated by
  `apps/api/src/app/services/farcaster_frame.py` (the `status_svg`
  function with `decision="approve"`) is a fully usable substitute —
  render it once, export to PNG.
- Twitter card: `summary_large_image`.
- `<meta name="theme-color">`: match the dark canvas (`#071015`).
- Canonical URL: `https://scanovich.ai/seablockchainweek/`.

## Technical hints (only if useful)

- The existing scanovich.ai site is, presumably, a deployed Next.js or
  static site. Keep this page additive: do not refactor the wider
  navigation just for this submission.
- If the site framework is Next.js: a single static MDX or TSX page
  under `app/seablockchainweek/page.tsx` is enough. Static-export
  friendly — no server requirement.
- If it is plain HTML: one HTML file under
  `static/seablockchainweek/index.html` plus shared CSS is fine.
- Page weight target: < 200 KB (excluding the OG PNG).

## Don'ts (please respect)

- Do not pretend the project is funded, partnered, or audited by names
  it is not (no SCB / Sansiri / Coinbase / Base team logos as
  endorsement).
- Do not put a token logo, presale, airdrop, or "join community"
  block. We don't have any of those.
- Do not include a wallet-connect button on this landing — the wallet
  flow lives at `localhost:3000/rwa-settlement-live` (or, post-deploy,
  on the Vercel URL). The landing only **announces** the demo; it does
  not run it.
- Do not auto-play any video or audio.
- Do not include AI-generated portrait / character imagery; we sell
  infrastructure, not personality.

## Deliverables checklist

- [ ] Page live at `https://scanovich.ai/seablockchainweek/` (trailing
      slash redirected).
- [ ] All eight content blocks present, in order.
- [ ] OG image renders correctly when the URL is shared on Twitter /
      Telegram.
- [ ] Lighthouse perf ≥ 95, accessibility ≥ 95, SEO ≥ 95 on mobile.
- [ ] All links to GitHub resolve (after the repo is flipped to public
      tomorrow).
- [ ] Video URL placeholder (Block 1 primary CTA) wired up to the final
      hosted recording when it is ready.
- [ ] Page survives Twitter Card validator and Facebook OG debugger.

## Source assets you can pull from

| Asset | Where |
|---|---|
| Pivot story copy | `docs/PRODUCT_THESIS.md` § "Pivot context" |
| Comparison data | `docs/COMPARISON.md` § "At a glance" |
| On-chain artefact list | `README.md` § "What's on-chain" |
| Roadmap dates | `docs/ROADMAP.md` |
| Hero hook + outro lines | `docs/DEMO_SCRIPT.md` |
| OG image SVG (use `decision=approve`) | `apps/api/src/app/services/farcaster_frame.py` § `status_svg(...)` |
| Repo description | `https://api.github.com/repos/FUYOH666/bankable-property-network` (will be public from tomorrow) |

## Timeline

- **Tonight / tomorrow morning:** the agent writing this page works in
  parallel to AttestRWA submission. Page can ship before the demo
  recording is uploaded; insert the recording URL last.
- **Before the hackathon submission cut-off:** page must be live at the
  canonical URL with all links resolving.

## Out of scope for this brief

- We are not asking for analytics, A/B testing, marketing automation,
  CRM, or pixel tracking on this landing.
- We are not asking for a separate brand book or design system. Use the
  existing scanovich.ai shell where possible; deviate only where this
  brief explicitly calls for it.
- Translations (Thai / Russian) are nice-to-have; English-only is
  acceptable for the hackathon submission.

## Final tone reminder

The reader of this page should walk away thinking: "These people would
be comfortable in a Goldman Sachs financial-infrastructure boardroom."
Plain, sharp, factual, and unmistakably composable on-chain. That is the
deliverable.
