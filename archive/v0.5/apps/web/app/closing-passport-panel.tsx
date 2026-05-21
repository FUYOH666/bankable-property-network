"use client";

import { useDemoFetch } from "../lib/use-demo-fetch";

type CapitalSource = {
  status: string;
  reason?: string;
};

type Route = {
  id: string;
  label: string;
  recommended: boolean;
  risk: string;
  conditions: string[];
};

type ClosingPassportPayload = {
  case_id: string;
  evidence_pack_hash: string;
  attestation: {
    buyer_bankability_checked: boolean;
    developer_risk_reviewed: boolean;
    settlement_route_approved: boolean;
    escrow_conditions_generated: boolean;
    approver_role: string;
  };
};

type DemoPayload = {
  property_shield: {
    risk_level: string;
    flags: string[];
  };
  capital_bankability_map: Record<string, CapitalSource>;
  routes: Route[];
  recommended_route: Route;
  bank_counter_offer: {
    product: string;
    offer: string;
    buyer_value: string;
    bank_value: string;
  };
  closing_passport: ClosingPassportPayload;
  infrastructure_context: {
    failure_mode: string;
    root_cause: string;
    narrative_role: string;
    primary_customer: string;
  };
};

const capitalLabels: Record<string, string> = {
  "src-bank-dubai": "Dubai bank funds",
  "src-usdt": "Stablecoin balance",
  "src-p2p": "P2P cash-like route",
};

function statusTone(status: string): string {
  if (status === "green") {
    return "green";
  }
  if (status === "red") {
    return "red";
  }
  return "amber";
}

export function ClosingPassportPanel() {
  const { data: payload, error, loading } = useDemoFetch<DemoPayload>("/api/demo/closing-passport");

  if (loading) {
    return (
      <div className="card closing-passport-panel">
        <h2>Settlement Flow</h2>
        <p>Loading Property Shield, capital map, routes, and Closing Passport from FastAPI...</p>
      </div>
    );
  }

  if (error || !payload) {
    return (
      <div className="card closing-passport-panel">
        <h2>Settlement Flow</h2>
        <p>
          API payload unavailable: <code>{error ?? "unknown error"}</code>
        </p>
        <p>Start the FastAPI service to show live settlement data.</p>
      </div>
    );
  }

  return (
    <div className="card closing-passport-panel">
      <div className="eyebrow">Core MVP · Bankable Property OS</div>
      <h2>Settlement Flow</h2>
      <p className="vision-lead">
        Infrastructure context: {payload.infrastructure_context.failure_mode.replaceAll("_", " ")} · primary customer:{" "}
        {payload.infrastructure_context.primary_customer.replaceAll("_", " ")}
      </p>

      <div className="vision-grid">
        <article className="vision-card">
          <h3>Property Shield</h3>
          <p>
            Risk level: <span className={`status ${statusTone(payload.property_shield.risk_level === "high" ? "red" : "amber")}`}>{payload.property_shield.risk_level}</span>
          </p>
          {payload.property_shield.flags.map((flag) => (
            <p key={flag}>
              <span className="status red">{flag.replaceAll("_", " ")}</span>
            </p>
          ))}
        </article>

        <article className="vision-card">
          <h3>Capital Bankability Map</h3>
          {Object.entries(payload.capital_bankability_map).map(([sourceId, source]) => (
            <p key={sourceId}>
              <span className={`status ${statusTone(source.status)}`}>{source.status}</span>{" "}
              <strong>{capitalLabels[sourceId] ?? sourceId}</strong>
              {source.reason ? ` · ${source.reason}` : ""}
            </p>
          ))}
        </article>

        <article className="vision-card">
          <h3>Route Comparison</h3>
          {payload.routes.map((route) => (
            <div key={route.id} className="route-row">
              <p>
                <span className={`status ${route.recommended ? "green" : route.risk === "high" ? "red" : "amber"}`}>
                  {route.recommended ? "recommended" : route.risk}
                </span>{" "}
                <strong>{route.label}</strong>
              </p>
              <p>{route.conditions[0]}</p>
            </div>
          ))}
        </article>

        <article className="vision-card">
          <h3>Bank Counter-Offer</h3>
          <p>
            <strong>{payload.bank_counter_offer.product}</strong>
          </p>
          <p>{payload.bank_counter_offer.offer}</p>
          <p>{payload.bank_counter_offer.bank_value}</p>
        </article>

        <article className="vision-card wide">
          <h3>Closing Passport</h3>
          <p>Evidence pack hash:</p>
          <code>{payload.closing_passport.evidence_pack_hash}</code>
          <p>
            Attestation: bankability checked · developer reviewed · route approved · escrow conditions generated · approver{" "}
            {payload.closing_passport.attestation.approver_role}
          </p>
          <p>Contains status metadata only. No passports, contracts, bank statements, or personal data on-chain.</p>
        </article>
      </div>
    </div>
  );
}
