"use client";

import { getApiBaseUrl } from "../lib/api-base-url";
import { useDemoFetch } from "../lib/use-demo-fetch";

type SimulationPayload = {
  steps: Array<{
    id: string;
    actor: string;
    title: string;
    detail: string;
  }>;
  evidence_preview: {
    included: string[];
    excluded_sensitive_fields: string[];
    privacy_note: string;
  };
  closing_passport: {
    evidence_pack_hash: string;
  };
};

export function GuidedDealSimulation() {
  const { data: payload, error, loading } = useDemoFetch<SimulationPayload>("/api/demo/guided-simulation");

  if (error) {
    return (
      <section className="card">
        <h2>Guided Deal Simulation</h2>
        <p>
          Simulation unavailable: <code>{error}</code>
        </p>
        <p>Start the FastAPI service to run the live buyer → bank → compliance workflow.</p>
      </section>
    );
  }

  if (loading || !payload) {
    return (
      <section className="card">
        <h2>Guided Deal Simulation</h2>
        <p>Loading live workflow from FastAPI...</p>
      </section>
    );
  }

  return (
    <section className="card">
      <div className="eyebrow">Live user simulation</div>
      <h2>Buyer → Bank → Compliance → Passport</h2>
      <div className="timeline">
        {payload.steps.map((step) => (
          <article className="timeline-item" key={step.id}>
            <span className="status amber">{step.actor}</span>
            <h3>{step.title}</h3>
            <p>{step.detail}</p>
          </article>
        ))}
      </div>
      <h3>Evidence Preview</h3>
      <p>Included: {payload.evidence_preview.included.join(", ")}.</p>
      <p>Excluded: {payload.evidence_preview.excluded_sensitive_fields.join(", ")}.</p>
      <p>{payload.evidence_preview.privacy_note}</p>
      <p>Closing Passport hash:</p>
      <code>{payload.closing_passport.evidence_pack_hash}</code>
      <p>
        <a className="button-link" href={`${getApiBaseUrl()}/api/demo/evidence-pack`} target="_blank" rel="noreferrer">
          Open Evidence Pack JSON
        </a>
      </p>
    </section>
  );
}
