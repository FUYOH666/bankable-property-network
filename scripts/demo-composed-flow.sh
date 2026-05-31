#!/usr/bin/env bash
# Composed flow demo: mock eligibility check + AttestRWA settlement E2E.
#
# Step 1 — eligibility layer (mock; swap for Shibui isVerified in production)
# Step 2 — standard ./scripts/e2e_rwa_flow.sh (deposit → attest → release)
#
# Requires dev chain + deployed contracts. Idempotent with e2e_rwa_flow.

set -euo pipefail

export PATH="$HOME/.foundry/bin:$PATH"

BUYER=0x70997970C51812dc3A010C7d01b50e0d17dc79C8

log() { printf '\n\033[1;35m[composed]\033[0m %s\n' "$*" >&2; }

log "Layer 1 — eligibility (mock): isVerified($BUYER) → true"
log "  Production: EntEthAlliance/rnd-rwa-erc3643-eas EASClaimVerifier.isVerified"
log "  See examples/composed-eligibility-settlement/ and docs/rfc/0001-*.md"

log "Layer 2 — settlement attestation (AttestRWA E2E)…"
exec "$(dirname "$0")/e2e_rwa_flow.sh"
