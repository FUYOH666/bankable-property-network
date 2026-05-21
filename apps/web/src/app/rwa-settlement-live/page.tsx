"use client";

import {ConnectButton} from "@rainbow-me/rainbowkit";
import {useEffect, useMemo, useState} from "react";
import {Address, formatUnits, keccak256, stringToBytes} from "viem";
import {useAccount, usePublicClient, useReadContract, useWalletClient} from "wagmi";

import {
  ATTESTRWA,
  AttestResponse,
  DEMO_SCENARIOS,
  ScenarioKey,
  escrowAbi,
  mockUsdcAbi,
} from "@/lib/contracts";

type Step = "idle" | "mint" | "approve" | "deposit" | "attest" | "release" | "refund" | "done";

type LogEntry = {ts: number; tone: "info" | "ok" | "warn" | "err"; text: string};

function shorten(value: string, head = 8, tail = 6): string {
  if (!value) return "—";
  if (value.length <= head + tail + 2) return value;
  return `${value.slice(0, head)}…${value.slice(-tail)}`;
}

function generateDealId(scenarioKey: ScenarioKey, account?: Address): `0x${string}` {
  const salt = `${scenarioKey}-${account ?? "anon"}-${Date.now()}-${Math.random()}`;
  return keccak256(stringToBytes(salt));
}

const FALLBACK_DEADLINE = 60 * 60 * 24; // 24 h

export default function RwaSettlementLivePage() {
  const {address, isConnected} = useAccount();
  const publicClient = usePublicClient();
  const {data: walletClient} = useWalletClient();

  const [scenarioKey, setScenarioKey] = useState<ScenarioKey>("happy");
  const scenario = DEMO_SCENARIOS[scenarioKey];

  const [dealId, setDealId] = useState<`0x${string}` | null>(null);
  const [step, setStep] = useState<Step>("idle");
  const [busy, setBusy] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [attestation, setAttestation] = useState<AttestResponse | null>(null);

  const log = (entry: Omit<LogEntry, "ts">) =>
    setLogs((prev) => [{ts: Date.now(), ...entry}, ...prev].slice(0, 60));

  // Live balances
  const {data: buyerBalance, refetch: refetchBuyer} = useReadContract({
    address: ATTESTRWA.mockUsdc,
    abi: mockUsdcAbi,
    functionName: "balanceOf",
    args: address ? [address] : undefined,
    query: {enabled: Boolean(address), refetchInterval: 4000},
  });

  const {data: payeeBalance, refetch: refetchPayee} = useReadContract({
    address: ATTESTRWA.mockUsdc,
    abi: mockUsdcAbi,
    functionName: "balanceOf",
    args: [scenario.payee],
    query: {refetchInterval: 4000},
  });

  // Reset dealId when scenario changes
  useEffect(() => {
    setDealId(null);
    setAttestation(null);
    setStep("idle");
  }, [scenarioKey]);

  const ensureDealId = () => {
    if (dealId) return dealId;
    const fresh = generateDealId(scenarioKey, address);
    setDealId(fresh);
    log({tone: "info", text: `Generated dealId ${shorten(fresh)}`});
    return fresh;
  };

  const requireWallet = () => {
    if (!walletClient || !publicClient || !address) {
      log({tone: "err", text: "Connect a wallet that holds Base Sepolia gas first."});
      return null;
    }
    return {walletClient, publicClient, address};
  };

  const handleMint = async () => {
    const ctx = requireWallet();
    if (!ctx) return;
    setBusy(true);
    setStep("mint");
    try {
      const hash = await ctx.walletClient.writeContract({
        address: ATTESTRWA.mockUsdc,
        abi: mockUsdcAbi,
        functionName: "mint",
        args: [ctx.address, scenario.amount],
      });
      log({tone: "info", text: `mint tx ${shorten(hash)} pending…`});
      await ctx.publicClient.waitForTransactionReceipt({hash});
      log({tone: "ok", text: `Minted ${formatUnits(scenario.amount, 6)} mUSDC to buyer`});
      await refetchBuyer();
    } catch (err) {
      log({tone: "err", text: `mint failed: ${(err as Error).message}`});
    } finally {
      setBusy(false);
    }
  };

  const handleApprove = async () => {
    const ctx = requireWallet();
    if (!ctx) return;
    setBusy(true);
    setStep("approve");
    try {
      const hash = await ctx.walletClient.writeContract({
        address: ATTESTRWA.mockUsdc,
        abi: mockUsdcAbi,
        functionName: "approve",
        args: [ATTESTRWA.escrow, scenario.amount],
      });
      await ctx.publicClient.waitForTransactionReceipt({hash});
      log({tone: "ok", text: `Approved escrow to pull ${formatUnits(scenario.amount, 6)} mUSDC`});
    } catch (err) {
      log({tone: "err", text: `approve failed: ${(err as Error).message}`});
    } finally {
      setBusy(false);
    }
  };

  const handleDeposit = async () => {
    const ctx = requireWallet();
    if (!ctx) return;
    const id = ensureDealId();
    setBusy(true);
    setStep("deposit");
    try {
      const deadline = BigInt(Math.floor(Date.now() / 1000) + FALLBACK_DEADLINE);
      const hash = await ctx.walletClient.writeContract({
        address: ATTESTRWA.escrow,
        abi: escrowAbi,
        functionName: "deposit",
        args: [id, scenario.payee, ATTESTRWA.mockUsdc, scenario.amount, deadline],
      });
      await ctx.publicClient.waitForTransactionReceipt({hash});
      log({tone: "ok", text: `Deposited into escrow under dealId ${shorten(id)}`});
      await refetchBuyer();
    } catch (err) {
      log({tone: "err", text: `deposit failed: ${(err as Error).message}`});
    } finally {
      setBusy(false);
    }
  };

  const handleAttest = async () => {
    if (!dealId || !address) {
      log({tone: "err", text: "Deposit first to fix a dealId, then attest."});
      return;
    }
    setBusy(true);
    setStep("attest");
    try {
      const resp = await fetch(`${ATTESTRWA.attesterApi}/attest/settlement`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          deal_id: dealId,
          buyer_wallet: address,
          payee_wallet: scenario.payee,
          token_address: ATTESTRWA.mockUsdc,
          amount_base_units: Number(scenario.amount),
          developer_id: scenario.developerId,
          jurisdiction: "TH",
          buyer_kyc_tier: 3,
          expires_in_seconds: FALLBACK_DEADLINE,
        }),
      });
      if (!resp.ok) {
        throw new Error(`attester returned ${resp.status}`);
      }
      const body = (await resp.json()) as AttestResponse;
      setAttestation(body);
      log({tone: body.decision === "approve" ? "ok" : "warn", text: `Attester decided ${body.decision}`});
      if (body.attestation_uid) {
        log({tone: "ok", text: `EAS attestation UID ${shorten(body.attestation_uid)}`});
      }
    } catch (err) {
      log({tone: "err", text: `attest failed: ${(err as Error).message}`});
    } finally {
      setBusy(false);
    }
  };

  const handleRelease = async () => {
    const ctx = requireWallet();
    if (!ctx || !dealId || !attestation?.attestation_uid) {
      log({tone: "err", text: "Need a valid attestation UID before release."});
      return;
    }
    setBusy(true);
    setStep("release");
    try {
      const hash = await ctx.walletClient.writeContract({
        address: ATTESTRWA.escrow,
        abi: escrowAbi,
        functionName: "release",
        args: [dealId, attestation.attestation_uid],
      });
      await ctx.publicClient.waitForTransactionReceipt({hash});
      log({tone: "ok", text: `Release tx ${shorten(hash)} confirmed`});
      await refetchPayee();
      setStep("done");
    } catch (err) {
      log({tone: "err", text: `release failed (expected on reject scenario): ${(err as Error).message}`});
    } finally {
      setBusy(false);
    }
  };

  const handleRefund = async () => {
    const ctx = requireWallet();
    if (!ctx || !dealId) {
      log({tone: "err", text: "No active dealId."});
      return;
    }
    setBusy(true);
    setStep("refund");
    try {
      const uid = attestation?.attestation_uid ?? "0x0000000000000000000000000000000000000000000000000000000000000000";
      const hash = await ctx.walletClient.writeContract({
        address: ATTESTRWA.escrow,
        abi: escrowAbi,
        functionName: "refund",
        args: [dealId, uid as `0x${string}`],
      });
      await ctx.publicClient.waitForTransactionReceipt({hash});
      log({tone: "ok", text: `Refund tx ${shorten(hash)} confirmed`});
      await refetchBuyer();
      setStep("done");
    } catch (err) {
      log({tone: "err", text: `refund failed: ${(err as Error).message}`});
    } finally {
      setBusy(false);
    }
  };

  const decisionTone = useMemo(() => {
    if (!attestation) return "muted";
    if (attestation.decision === "approve") return "approve";
    return "reject";
  }, [attestation]);

  return (
    <main className="live">
      <header className="live-header">
        <div>
          <div className="eyebrow">AttestRWA · live settlement</div>
          <h1>RWA settlement, attested on-chain</h1>
          <p>
            Connect a wallet, pick a scenario, walk the same 5-step flow that
            <code> scripts/e2e_rwa_flow.sh</code> and <code>e2e_rwa_reject.sh</code> exercise.
          </p>
        </div>
        <ConnectButton showBalance={false} accountStatus="full" chainStatus="full" />
      </header>

      <section className="scenarios">
        <h2>Pick a scenario</h2>
        <div className="scenario-grid">
          {(Object.keys(DEMO_SCENARIOS) as ScenarioKey[]).map((key) => (
            <button
              key={key}
              type="button"
              className={`scenario ${key === scenarioKey ? "is-active" : ""}`}
              onClick={() => setScenarioKey(key)}
              disabled={busy}
            >
              <strong>{DEMO_SCENARIOS[key].label}</strong>
              <div className="scenario-meta">
                <span>developer = {DEMO_SCENARIOS[key].developerId}</span>
                <span>amount = {formatUnits(DEMO_SCENARIOS[key].amount, 6)} mUSDC</span>
                <span>payee = {shorten(DEMO_SCENARIOS[key].payee)}</span>
                <span>expected decision = {DEMO_SCENARIOS[key].expected}</span>
              </div>
            </button>
          ))}
        </div>
      </section>

      <section className="actions">
        <h2>Walk the flow</h2>
        <div className="action-row">
          <button type="button" onClick={handleMint} disabled={!isConnected || busy}>1 · Mint mUSDC</button>
          <button type="button" onClick={handleApprove} disabled={!isConnected || busy}>2 · Approve escrow</button>
          <button type="button" onClick={handleDeposit} disabled={!isConnected || busy}>3 · Deposit</button>
          <button type="button" onClick={handleAttest} disabled={!dealId || busy}>4 · Trigger attester</button>
          <button type="button" onClick={handleRelease} disabled={!attestation?.attestation_uid || busy}>5 · Release</button>
          <button type="button" onClick={handleRefund} disabled={!dealId || busy}>5 · Refund</button>
        </div>
        <small className="hint">
          Step 5 — Release goes through on the happy scenario, reverts on the reject scenario; then Refund returns funds to you with the attester-signed reject as audit trail.
        </small>
      </section>

      <section className="status">
        <div className="card">
          <h3>Buyer balance</h3>
          <p className="big">{address ? `${formatUnits((buyerBalance as bigint | undefined) ?? 0n, 6)} mUSDC` : "wallet not connected"}</p>
          <small>{address ? shorten(address) : "—"}</small>
        </div>
        <div className="card">
          <h3>Payee balance</h3>
          <p className="big">{formatUnits((payeeBalance as bigint | undefined) ?? 0n, 6)} mUSDC</p>
          <small>{shorten(scenario.payee)}</small>
        </div>
        <div className={`card decision decision-${decisionTone}`}>
          <h3>Attester decision</h3>
          <p className="big">{attestation ? attestation.decision.toUpperCase() : "—"}</p>
          {attestation && (
            <ul>
              <li>payee verified = {String(attestation.payee_verified)}</li>
              <li>capital class = {attestation.capital_class}</li>
              <li>evidence hash {shorten(attestation.evidence_hash)}</li>
              {attestation.attestation_uid && (
                <li>
                  attestation UID {shorten(attestation.attestation_uid)}
                  <br />
                  <a href={`${ATTESTRWA.easScanBaseUrl}/attestation/view/${attestation.attestation_uid}`} target="_blank" rel="noreferrer">view on EAS Scan</a>
                </li>
              )}
              {attestation.tx_hash && (
                <li>
                  attest tx <a href={`${ATTESTRWA.basescanBaseUrl}/tx/${attestation.tx_hash}`} target="_blank" rel="noreferrer">{shorten(attestation.tx_hash)}</a>
                </li>
              )}
            </ul>
          )}
        </div>
      </section>

      {attestation && (
        <section className="rules">
          <h3>Compliance rule results</h3>
          <ul>
            {attestation.rule_results.map((rule) => (
              <li key={rule.rule_id} className={rule.passed ? "rule-pass" : "rule-fail"}>
                <strong>{rule.rule_id}:</strong> {rule.explanation}
              </li>
            ))}
          </ul>
          {attestation.reasons.length > 0 && (
            <>
              <h4>Reasons</h4>
              <ul>
                {attestation.reasons.map((r, idx) => (
                  <li key={idx}>{r}</li>
                ))}
              </ul>
            </>
          )}
        </section>
      )}

      <section className="logs">
        <h3>Activity log</h3>
        <ul>
          {logs.length === 0 && <li className="log-empty">Activity will appear here.</li>}
          {logs.map((entry) => (
            <li key={entry.ts} className={`log-${entry.tone}`}>
              <code>{new Date(entry.ts).toLocaleTimeString()}</code> · {entry.text}
            </li>
          ))}
        </ul>
        <small>
          Status: <strong>{step}</strong> · dealId {dealId ? shorten(dealId) : "none yet"}
        </small>
      </section>
    </main>
  );
}
