# Dune Queries — AttestRWA

Copy-paste queries for the public `attestrwa-public` Dune Analytics
dashboard. Each query is parameterized for **Base Sepolia (chainId 84532)
or Base mainnet (chainId 8453)**; change the network selector in the Dune
UI.

> Status: ready to paste once contracts are deployed to a public network.
> Until then, run them against the `dune.eas` decoded tables (already
> available on Dune for any EAS chain).

## 1. Attestations per day (SettlementApproval schema)

```sql
SELECT
  date_trunc('day', evt_block_time) AS day,
  COUNT(*) AS attestation_count
FROM eas_v1.eas_evt_attested
WHERE schema_uid = 0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96
GROUP BY 1
ORDER BY 1 DESC
LIMIT 30
```

## 2. Approvals vs rejections by reason

```sql
WITH decoded AS (
  SELECT
    uid,
    attester,
    evt_block_time,
    -- SettlementApproval encoding: 10 fields
    -- bytes32 dealId, address attester, address payeeAddress, address tokenAddress,
    -- uint256 amount, uint8 capitalClass, bytes32 evidenceHash, string jurisdiction,
    -- uint64 expiresAt, bool payeeVerified
    bytea_to_int256(substring(data, 1, 32)) AS deal_id_int,
    bytea_to_int256(substring(data, 161, 32)) AS capital_class,
    bytea_to_int256(substring(data, 289, 32)) AS payee_verified_int
  FROM eas_v1.eas_evt_attested
  WHERE schema_uid = 0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96
)
SELECT
  CASE
    WHEN payee_verified_int = 1 AND capital_class < 2 THEN 'approve'
    WHEN payee_verified_int = 0 THEN 'reject_payee'
    WHEN capital_class >= 2 THEN 'reject_capital'
    ELSE 'reject_other'
  END AS decision,
  COUNT(*) AS n
FROM decoded
GROUP BY 1
ORDER BY n DESC
```

## 3. Top attesters by attestation count

```sql
SELECT
  attester,
  COUNT(*) AS attestations,
  MIN(evt_block_time) AS first_attested_at,
  MAX(evt_block_time) AS last_attested_at
FROM eas_v1.eas_evt_attested
WHERE schema_uid = 0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96
GROUP BY 1
ORDER BY 2 DESC
LIMIT 20
```

## 4. USDC volume released through SettlementEscrow

```sql
SELECT
  date_trunc('day', evt_block_time) AS day,
  SUM(CAST(amount AS DOUBLE) / 1e6) AS usdc_released
FROM source_settlement_escrow_evt_settlementreleased
GROUP BY 1
ORDER BY 1 DESC
```

> Replace `source_settlement_escrow_evt_settlementreleased` with the
> decoded table that Dune generates after the contract is submitted to
> Dune's contract submission flow.

## 5. Refunds by reason

```sql
SELECT
  reason,
  COUNT(*) AS n,
  SUM(CAST(amount AS DOUBLE) / 1e6) AS usdc_refunded
FROM source_settlement_escrow_evt_settlementrefunded
GROUP BY 1
ORDER BY 2 DESC
```

## 6. Average attestation-to-release latency

```sql
WITH attestations AS (
  SELECT
    uid,
    bytea_to_int256(substring(data, 1, 32)) AS deal_id,
    evt_block_time AS attested_at
  FROM eas_v1.eas_evt_attested
  WHERE schema_uid = 0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96
),
releases AS (
  SELECT
    CAST(deal_id AS NUMERIC) AS deal_id,
    evt_block_time AS released_at
  FROM source_settlement_escrow_evt_settlementreleased
)
SELECT
  AVG(EXTRACT(EPOCH FROM (r.released_at - a.attested_at))) AS avg_latency_seconds
FROM attestations a
JOIN releases r ON a.deal_id = r.deal_id
```

## Dashboard layout

When publishing `attestrwa-public`, suggest this widget order:

1. Hero: Attestations per day (line chart, query 1).
2. Decision split (donut, query 2).
3. Top attesters (table, query 3).
4. USDC volume released (bar chart, query 4).
5. Refunds by reason (bar chart, query 5).
6. Avg latency (single-number scorecard, query 6).
