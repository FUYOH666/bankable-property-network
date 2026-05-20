"use client";

import { useDemoFetch } from "../lib/use-demo-fetch";

type FeedSnapshot = {
  last_updated: string;
  authorized_payees: string[];
  units_available_count: number;
  sample_unit: { unit_type: string; price_thb: number };
  payment_terms: { booking_deposit_pct: number; installment_months: number };
  installment_schedule_summary: string;
};

type KnowledgeGap = {
  agent_claimed_payee: string;
  developer_authorized_payee: string;
  status: string;
  note: string;
};

type Channel = {
  id: string;
  label: string;
  status: string;
};

type HubPayload = {
  developer: string;
  project: string;
  source_of_truth: string;
  feed_snapshot: FeedSnapshot;
  knowledge_vs_agent_gap: KnowledgeGap;
  consumption_model: string;
  channel_roadmap: Channel[];
  ai_stack: {
    retrieval: string;
    generation: string;
    fallback: string;
  };
  prior_art: {
    project: string;
    reference_url: string;
  };
  pitch_line: string;
};

export function DeveloperKnowledgeHub() {
  const { data: payload, error, loading } = useDemoFetch<HubPayload>("/api/demo/developer-knowledge-hub");

  if (error) {
    return (
      <div className="card dev-knowledge-hub">
        <h2>Developer Knowledge Hub</h2>
        <p>
          Hub unavailable: <code>{error}</code>
        </p>
      </div>
    );
  }

  if (loading || !payload) {
    return (
      <div className="card dev-knowledge-hub">
        <h2>Developer Knowledge Hub</h2>
        <p>Loading verified developer knowledge from FastAPI...</p>
      </div>
    );
  }

  const gapTone = payload.knowledge_vs_agent_gap.status === "mismatch_detected" ? "red" : "green";

  return (
    <div className="card dev-knowledge-hub">
      <div className="eyebrow">Upstream · Verified Developer Knowledge Layer</div>
      <h2>Developer Knowledge Hub</h2>
      <p className="vision-lead">{payload.pitch_line}</p>
      <p className="vision-note">Consumption model: {payload.consumption_model.replaceAll("_", " ")}</p>

      <div className="vision-grid">
        <article className="vision-card">
          <h3>Developer Source Of Truth</h3>
          <p>
            <strong>{payload.developer}</strong> · {payload.project}
          </p>
          <p>Source: {payload.source_of_truth}</p>
          <p>Last updated: {payload.feed_snapshot.last_updated}</p>
          <p>
            Authorized payee: <strong>{payload.feed_snapshot.authorized_payees.join(", ")}</strong>
          </p>
          <p>
            Sample unit: {payload.feed_snapshot.sample_unit.unit_type} ·{" "}
            {(payload.feed_snapshot.sample_unit.price_thb / 1_000_000).toFixed(1)}M THB
          </p>
          <p>
            Deposit: {payload.feed_snapshot.payment_terms.booking_deposit_pct}% · Installments:{" "}
            {payload.feed_snapshot.payment_terms.installment_months} months
          </p>
          <p>{payload.feed_snapshot.installment_schedule_summary}</p>
        </article>

        <article className="vision-card">
          <h3>Agent Distortion Gap</h3>
          <p>
            <span className={`status ${gapTone}`}>{payload.knowledge_vs_agent_gap.status.replaceAll("_", " ")}</span>
          </p>
          <p>Agent claimed payee: {payload.knowledge_vs_agent_gap.agent_claimed_payee}</p>
          <p>Developer authorized: {payload.knowledge_vs_agent_gap.developer_authorized_payee}</p>
          <p>{payload.knowledge_vs_agent_gap.note}</p>
        </article>

        <article className="vision-card">
          <h3>Channel Roadmap</h3>
          {payload.channel_roadmap.map((channel) => (
            <p key={channel.id}>
              <span className="status amber">{channel.status}</span> <strong>{channel.label}</strong>
            </p>
          ))}
          <p className="vision-note">
            Prior art:{" "}
            <a href={payload.prior_art.reference_url} target="_blank" rel="noreferrer">
              {payload.prior_art.project}
            </a>
          </p>
        </article>

        <article className="vision-card">
          <h3>AI Stack</h3>
          <p>{payload.ai_stack.retrieval}</p>
          <p>{payload.ai_stack.generation}</p>
          <p>{payload.ai_stack.fallback}</p>
        </article>
      </div>
    </div>
  );
}
