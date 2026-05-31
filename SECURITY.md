# Security Policy

AttestRWA is hackathon-stage infrastructure with no professional audit yet.
We take security seriously and welcome responsible disclosure.

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | yes (testnet only) |
| 0.5.x   | archived; see `archive/v0.5/` for historical context |

## Threat model and current audit posture

The full threat model, the Slither audit posture (0 findings at low /
medium / high), the Foundry coverage matrix, the wallet-trust assumptions,
and the deferred items (HSM keys, multi-sig attester, formal STRIDE,
external Trail of Bits scope) live in
[`docs/SECURITY.md`](docs/SECURITY.md). Please read that document first
before reporting an issue.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for a security problem.

Two preferred channels:

1. Open a private GitHub Security Advisory:
   <https://github.com/FUYOH666/attestrwa/security/advisories/new>.
   This is the fastest path and gives us a coordinated-disclosure surface.
2. Email the project maintainer (see the GitHub profile at
   <https://github.com/FUYOH666>) with the subject line
   `attestrwa security: <one-line summary>`.

Include where reasonable:

- Affected component (contracts, attester service, web UI, scripts).
- The exact commit hash or release tag.
- A minimal reproduction (Foundry test, cast command, curl, etc.).
- The on-chain artefacts if relevant (tx hash, attestation UID — never
  private keys).
- Your suggested severity (informational / low / medium / high / critical).

## Our response process

- We aim to acknowledge new reports within 72 hours.
- For valid findings, we will agree on a fix window and a coordinated
  disclosure date. Up to 90 days for non-critical issues; faster for
  critical ones.
- Once the fix lands, we credit you in the corresponding `CHANGELOG.md`
  entry unless you ask to remain anonymous.

## Bug bounty

AttestRWA does **not** currently run a formal bug bounty. This will
change once we begin a regulated bank-attester pilot (see
`docs/ROADMAP.md` Q4 2026). Until then, please report responsibly out of
goodwill; we will reciprocate with credit and rapid fixes.

## Out of scope

- Mainnet exploits. We have not deployed to mainnet by design.
- Issues that require already-compromised private keys (e.g. "if you
  steal the attester key you can sign bogus attestations" — yes, that is
  why revocation exists, see `docs/SECURITY.md` T1).
- Vulnerabilities in upstream EAS, OpenZeppelin, or web3.py — please
  report those to the upstream project.
- DoS via spamming `MockUSDC.mint` on testnet — it is intentionally
  open-mint for demo purposes.
