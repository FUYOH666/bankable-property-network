# Contributing to AttestRWA

Thanks for considering a contribution. AttestRWA is bank-grade
infrastructure — small, composable, well-tested changes win.

## Quick start

```bash
# 1. Foundry toolchain (forge / cast / anvil)
curl -L https://foundry.paradigm.xyz | bash
source ~/.zshenv
foundryup

# 2. Python toolchain (uv 0.5+)
curl -LsSf https://astral.sh/uv/install.sh | sh
cd apps/api && uv sync

# 3. Optional: Node toolchain for the web app (pnpm 9+)
corepack enable && corepack prepare pnpm@latest --activate
cd apps/web && pnpm install

# 4. Spin up the local dev fork + register the EAS schema
./scripts/dev-chain.sh

# 5. Deploy MockUSDC + SettlementEscrow against the dev fork
./scripts/deploy-contracts.sh

# 6. Run the end-to-end happy path against the dev fork
./scripts/e2e_rwa_flow.sh
```

## Verification you must run before opening a PR

```bash
# Contracts
cd contracts
forge build
forge test --gas-report
slither src/SettlementEscrow.sol \
  --solc-remaps "@openzeppelin/contracts/=lib/openzeppelin-contracts/contracts/ @eas/=lib/eas-contracts/contracts/ forge-std/=lib/forge-std/src/" \
  --filter-paths "lib/" --exclude-low --exclude-informational
cd ..

# Backend
cd apps/api && uv run pytest -q && cd ../..

# End-to-end smokes
./scripts/e2e_rwa_flow.sh
./scripts/e2e_rwa_reject.sh
```

PR template checkboxes will ask you to confirm each of these passed.

## Commit conventions

Roughly Conventional Commits, with `feat`, `fix`, `refactor`,
`docs`, `chore`, `release`, `test`, `ci`. Add a scope when useful, e.g.
`feat(v1/w2.2)` or `fix(escrow)`.

Pivot-era commits use `feat(v1/wX.Y)` to make the weekly slice obvious.
Hold to the same shape for incoming PRs unless there's a good reason.

## What we will and won't accept

Welcome:

- Foundry tests, fuzz, invariants on `SettlementEscrow.sol`
- Slither / static-analysis improvements
- Compliance DSL rule packs as YAML files in `data/synthetic/policies/`
- Backend hardening, schema validation, better error messages
- Documentation: clearer threat model, more comparison data, more
  jurisdictional notes
- Real wallet-taint provider adapters (Chainalysis / TRM Labs / Hexagate)

Not welcome (per `docs/ROADMAP.md` non-goals):

- Token launches, yield products, our own stablecoin
- Property tokenization or on-chain title transfer
- KYC providers (we integrate, we don't build)
- Mainnet deploys without an external audit
- Marketing-only PRs that add no functional change

## Security

If you find a security issue, please follow [`SECURITY.md`](SECURITY.md)
and do **not** open a public issue. We respect responsible disclosure.

## Code style

- Solidity 0.8.26, optimizer 1M runs, NatSpec on every external/public
  function. See `contracts/foundry.toml`.
- Python 3.12, `uv` only (no raw `pip`), `logging` not `print`. See
  `apps/api/pyproject.toml`.
- TypeScript strict mode on the web app.
- Markdown linted via inspection during review.

## License

By contributing, you agree your changes are licensed under
[Apache-2.0](LICENSE) like the rest of the project.
