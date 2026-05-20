"use client";

import { useDemoFetch } from "../lib/use-demo-fetch";

type TrackPayload = {
  track: string;
  developer: string;
  project: string;
  scenario_id: string;
  headline: string;
  risk_summary: string;
  permit_status?: string;
  eia_status?: string;
  sales_status?: string;
  network_status?: string;
  marketing_payee_claimed?: string;
  reputation_tier?: string;
  bank_action: string;
  closing_passport_status: string;
  supply_risk_signals: string[];
  feed_snapshot?: {
    permit_status?: string;
    eia_status?: string;
    authorized_payees?: string[];
    license_sales_entity?: string;
  };
  scenario_run?: {
    property_risk: string;
    route_decision: string;
  };
};

type ContrastPayload = {
  pitch_line: string;
  off_platform: TrackPayload;
  on_network: TrackPayload;
};

function toneForAction(action: string): "green" | "amber" | "red" {
  if (action === "approve") return "green";
  if (action === "conditional") return "amber";
  return "red";
}

function statusLine(track: TrackPayload): string[] {
  if (track.track === "without_network") {
    return [
      "Checking construction permit… pending",
      "Developer feed not on network — agent claims payee",
      "Bank blocks bankable route until permit verified",
    ];
  }
  return [
    "Developer feed matched on network",
    "Construction permit issued · EIA cleared",
    "Authorized payee verified · Closing Passport ready",
  ];
}

function TrackColumn({ track, variant }: { track: TrackPayload; variant: "off" | "on" }) {
  const tone = toneForAction(track.bank_action);
  const lines = statusLine(track);

  return (
    <article className={`supplier-track supplier-track-${variant}`}>
      <div className="eyebrow">{variant === "off" ? "Without Network" : "With Network"}</div>
      <h3>{track.developer}</h3>
      <p className="supplier-project">{track.project}</p>
      <p className="supplier-headline">{track.headline}</p>
      <p className="supplier-summary">{track.risk_summary}</p>

      <ul className="supplier-status-lines">
        {lines.map((line) => (
          <li key={line}>{line}</li>
        ))}
      </ul>

      <dl className="supplier-facts">
        {track.permit_status && (
          <>
            <dt>Permit</dt>
            <dd>{track.permit_status}</dd>
          </>
        )}
        {track.eia_status && (
          <>
            <dt>EIA</dt>
            <dd>{track.eia_status}</dd>
          </>
        )}
        {track.sales_status && (
          <>
            <dt>Sales</dt>
            <dd>{track.sales_status}</dd>
          </>
        )}
        {track.feed_snapshot?.authorized_payees && (
          <>
            <dt>Authorized payee</dt>
            <dd>{track.feed_snapshot.authorized_payees[0]}</dd>
          </>
        )}
        {track.marketing_payee_claimed && (
          <>
            <dt>Agent claimed payee</dt>
            <dd>{track.marketing_payee_claimed}</dd>
          </>
        )}
        <dt>Bank action</dt>
        <dd>
          <span className={`status ${tone}`}>{track.bank_action}</span>
        </dd>
        <dt>Closing Passport</dt>
        <dd>
          <span className={`status ${track.closing_passport_status === "generated" ? "green" : "red"}`}>
            {track.closing_passport_status.replaceAll("_", " ")}
          </span>
        </dd>
      </dl>

      {track.supply_risk_signals.length > 0 && (
        <div className="supplier-signals">
          {track.supply_risk_signals.map((signal) => (
            <span className="signal-chip" key={signal}>
              {signal.replaceAll("_", " ")}
            </span>
          ))}
        </div>
      )}
    </article>
  );
}

export function SupplierContrastDemo() {
  const { data: payload, error, loading } = useDemoFetch<ContrastPayload>("/api/demo/supplier-contrast");

  if (error) {
    return (
      <div className="card supplier-contrast">
        <h2>Supplier Contrast · Off-Platform vs Tier-1</h2>
        <p>
          Contrast demo unavailable: <code>{error}</code>
        </p>
      </div>
    );
  }

  if (loading || !payload) {
    return (
      <div className="card supplier-contrast">
        <h2>Supplier Contrast · Off-Platform vs Tier-1</h2>
        <p>Loading developer supply contrast from FastAPI...</p>
      </div>
    );
  }

  return (
    <section className="card supplier-contrast">
      <div className="eyebrow">Developer Supply · Why join before buyers arrive</div>
      <h2>Off-Platform Risk vs Tier-1 Verified</h2>
      <p className="vision-lead">{payload.pitch_line}</p>

      <div className="supplier-columns">
        <TrackColumn track={payload.off_platform} variant="off" />
        <TrackColumn track={payload.on_network} variant="on" />
      </div>
    </section>
  );
}
