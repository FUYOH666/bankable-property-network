# EAS Schema — `SettlementApproval`

> Defines the on-chain primitive that AttestRWA writes when a regulated
> attester approves a real-world-asset settlement. Lives in the
> [Ethereum Attestation Service (EAS)](https://attest.org) registry on
> **Base Sepolia** (testnet) → **Base mainnet** (production).

## 1. Schema definition (canonical)

```text
bytes32 dealId,
address attester,
address payeeAddress,
address tokenAddress,
uint256 amount,
uint8 capitalClass,
bytes32 evidenceHash,
string jurisdiction,
uint64 expiresAt,
bool payeeVerified
```

### Field semantics

| Field | Type | Meaning | Source |
|-------|------|---------|--------|
| `dealId` | `bytes32` | Deterministic deal identifier: `keccak256(propertyId, buyerWallet, amount, nonce)` | Computed off-chain, anchored on-chain |
| `attester` | `address` | EOA of the regulated attester (bank, regulator, network operator) | Signs the attestation |
| `payeeAddress` | `address` | Verified developer / counterparty wallet that may receive escrowed funds | From `data/synthetic/developers/*.json::authorizedPayees[]` |
| `tokenAddress` | `address` | ERC-20 stablecoin used for settlement (Mock USDC in demo) | Set at escrow deployment |
| `amount` | `uint256` | Settlement amount in token base units (USDC has 6 decimals) | Locked at escrow deposit |
| `capitalClass` | `uint8` | Wallet taint classification: `0 = green`, `1 = amber`, `2 = red` | `wallet_taint.py` (mock Chainalysis) |
| `evidenceHash` | `bytes32` | `keccak256` of off-chain evidence pack JSON (RAG citations, policy refs, decision log) | Computed by attester before signing |
| `jurisdiction` | `string` | ISO 3166-1 alpha-2 country code (`TH`, `SG`, etc.) | From deal context |
| `expiresAt` | `uint64` | Unix timestamp after which escrow rejects release on this attestation | Default: `now + 24h` |
| `payeeVerified` | `bool` | `true` iff `payeeAddress ∈ developerFeed[propertyId].authorizedPayees` | Property Shield logic |

### Why these fields

- **`dealId` + `payeeVerified` together** is the central anti-rug primitive:
  even a valid attester signature cannot bypass the developer-feed check.
- **`capitalClass`** lets escrow refuse a release for `red`-tainted buyer
  wallets without revealing private taint sources on-chain.
- **`evidenceHash`** lets compliance auditors verify the full evidence
  pack post-event without that data ever touching the chain (privacy-safe).
- **`expiresAt`** prevents replay of stale attestations across long-lived
  escrow contracts.
- **`jurisdiction`** allows compliance-DSL rules to fork by country.

## 2. Registration on Base Sepolia (manual, Week 0)

Schema registration is a one-time on-chain action. It requires:

- Attester EOA with Base Sepolia ETH (faucet: <https://www.alchemy.com/faucets/base-sepolia>)
- Access to the EAS UI on Base Sepolia: <https://base-sepolia.easscan.org/schema/create>

### Steps

1. **Generate the attester EOA** (do this once, on a clean wallet, store the
   private key in `.env` — never commit):

   ```bash
   cast wallet new
   # Output:
   #   Address: 0xATTESTER_ADDRESS
   #   Private key: 0xATTESTER_PRIVATE_KEY
   ```

   Add to `.env`:

   ```env
   ATTESTER_ADDRESS=0xATTESTER_ADDRESS
   ATTESTER_PRIVATE_KEY=0xATTESTER_PRIVATE_KEY
   ```

   Update `.env.example` with placeholder values only.

2. **Fund the attester EOA** on Base Sepolia (Alchemy faucet or
   <https://faucet.quicknode.com/base/sepolia>). Minimum: 0.01 ETH.

3. **Open the EAS schema creator** for Base Sepolia:
   <https://base-sepolia.easscan.org/schema/create>

4. **Paste the schema string** (single line, fields separated by commas):

   ```text
   bytes32 dealId, address attester, address payeeAddress, address tokenAddress, uint256 amount, uint8 capitalClass, bytes32 evidenceHash, string jurisdiction, uint64 expiresAt, bool payeeVerified
   ```

5. **Resolver:** leave empty (no custom resolver for v1).

6. **Revocable:** `true` (let attester revoke a wrong attestation; escrow
   checks `attestation.revocationTime == 0` before release).

7. **Sign and submit.** Network fee: a few cents in testnet ETH.

8. **Copy the resulting Schema UID** (looks like
   `0xa1b2c3...`) and save it to `.env`:

   ```env
   EAS_SCHEMA_UID_SETTLEMENT_APPROVAL=0x...
   ```

   Also update:

   - `docs/v1/README_DRAFT.md` → table "What's on-chain"
   - `docs/v1/ATTESTATION_SCHEMA.md` → this file, section 3 below

## 3. Live registration data

### 3a. Dev simulation (Anvil fork of Base Sepolia, port 8545)

Registered automatically by `scripts/dev-chain.sh`. The UID is deterministic
because EAS computes it from the schema string + resolver + revocable
arguments. Every fresh fork re-registers and yields the same UID.

| Field | Value |
|-------|-------|
| Network | Anvil fork of Base Sepolia (chainId 84532) |
| RPC URL | `http://127.0.0.1:8545` |
| EAS contract | `0x4200000000000000000000000000000000000021` (canonical) |
| SchemaRegistry contract | `0x4200000000000000000000000000000000000020` (canonical) |
| Schema UID | `0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96` |
| Resolver | `0x0000000000000000000000000000000000000000` (none) |
| Revocable | `true` |
| Registered by (dev attester) | `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266` (Anvil acc 0) |
| First registration tx (fork) | `0x371377c21cbe776533f6b04acb13e243f17205aeca21b0cb8c69a7f488734fbe` |
| First registration block | `41754039` |
| Gas used | `259,210` |
| Verified | `getSchema(uid)` readback ✓ |
| EAS UI on real testnet | <https://base-sepolia.easscan.org/schema/view/0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96> (will resolve once registered on real Base Sepolia in Week 3) |

### 3b. Real Base Sepolia (Week 3)

To be filled when the Week 3 real-testnet deploy happens. Schema string,
resolver, and revocable flag are identical to §3a, so the UID will be the
same `0x1f64ec96…` (deterministic).

| Field | Value |
|-------|-------|
| Network | Base Sepolia (real, chainId 84532) |
| RPC URL | `https://sepolia.base.org` |
| Schema UID | `0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96` (expected — same as dev) |
| Registered by | _(real attester EOA, generated in Week 3)_ |
| Tx hash | _(to be filled)_ |
| Block number | _(to be filled)_ |

If a different party has already registered this exact schema on real Base
Sepolia, the `register()` call will revert with `AlreadyExists()` — that
is a success path for us: we simply reuse the existing UID.

## 4. How AttestRWA writes attestations

```python
from app.services.eas_client import EASClient

client = EASClient(
    chain_id=84532,
    rpc_url=settings.base_sepolia_rpc_url,
    eas_contract="0x4200000000000000000000000000000000000021",
    schema_uid=settings.eas_schema_uid_settlement_approval,
    attester_private_key=settings.attester_private_key,
)

attestation_uid = client.attest(
    recipient="0x0000000000000000000000000000000000000000",  # public attestation
    data={
        "dealId": deal_id,
        "attester": settings.attester_address,
        "payeeAddress": developer_authorized_payee,
        "tokenAddress": mock_usdc_address,
        "amount": amount_in_usdc_base_units,
        "capitalClass": 0,  # green
        "evidenceHash": evidence_hash,
        "jurisdiction": "TH",
        "expiresAt": int(time.time()) + 86400,
        "payeeVerified": True,
    },
    revocable=True,
    expiration_time=int(time.time()) + 86400,
)
```

The escrow contract reads this attestation by `dealId` and verifies:

```solidity
function release(bytes32 dealId, bytes32 attestationUid) external {
    Attestation memory a = eas.getAttestation(attestationUid);
    require(a.schema == EAS_SCHEMA_UID_SETTLEMENT_APPROVAL, "wrong schema");
    require(a.revocationTime == 0, "revoked");
    require(a.expirationTime > block.timestamp, "expired");

    (
        bytes32 attDealId, address attester, address payeeAddress, address tokenAddress,
        uint256 amount, uint8 capitalClass, /* evidenceHash */, /* jurisdiction */,
        /* expiresAt */, bool payeeVerified
    ) = abi.decode(a.data, (bytes32, address, address, address, uint256, uint8, bytes32, string, uint64, bool));

    require(attDealId == dealId, "deal mismatch");
    require(trustedAttesters[attester], "untrusted attester");
    require(payeeVerified, "payee not verified");
    require(capitalClass < 2, "capital red");

    deals[dealId].released = true;
    IERC20(tokenAddress).transfer(payeeAddress, amount);
    emit SettlementReleased(dealId, payeeAddress, amount, attestationUid);
}
```

## 5. Threat model (Week 3 will expand in `SECURITY.md`)

| Threat | Mitigation |
|--------|------------|
| Attester key compromise | Revocation (`eas.revoke`); escrow re-checks `revocationTime == 0` |
| Replay of old attestation on new deal | `dealId` is bound; attestation `dealId` must equal call-site `dealId` |
| Front-running release tx | Escrow `release()` checks deal ownership; only buyer or attester can trigger |
| Wrong payee in developer feed | Out of scope: developer feed is upstream SSOT; integrity assumed (production = signed feed) |
| Sanction list drift | `capitalClass` snapshot is at attestation time; `expiresAt` bounds drift window (24h default) |
| Schema impostor | Escrow hard-pins `EAS_SCHEMA_UID_SETTLEMENT_APPROVAL` constant |

## 6. References

- EAS docs: <https://docs.attest.org>
- EAS Base Sepolia explorer: <https://base-sepolia.easscan.org>
- EAS contract addresses: <https://docs.attest.org/docs/quick--start/contracts>
- Base Sepolia faucet: <https://www.alchemy.com/faucets/base-sepolia>
