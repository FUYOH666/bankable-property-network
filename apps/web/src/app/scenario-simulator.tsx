"use client";

import { useEffect, useMemo, useState } from "react";

type Scenario = {
  id: string;
  capital_status: string;
  property_status: string;
  agent_status: string;
  route_decision: string;
  closing_passport: string;
};

type ScenarioRun = {
  id: string;
  capital_status: string;
  property_risk: string;
  agent_risk: string;
  route_decision: string;
  bank_action: string;
  closing_passport_status: string;
  closing_passport_hash: string | null;
  buyer: { profile: string; expected_status: string };
  project: { name: string; status: string; risk_level: string; notes: string };
  agent: { name: string; status: string; risk_level: string; commission_disclosure: string };
  evidence_preview: { included: string[]; excluded_sensitive_fields: string[]; privacy_note: string };
  retrieval_mode?: string;
  retrieval_fallback_reason?: string | null;
  retrieved_evidence?: Array<{
    document_id: string;
    kind: string;
    score: number;
    rerank_score: number | null;
    excerpt: string;
    source_path: string;
  }>;
  rag_trace: Array<{ kind: string; document_id: string; reason: string }>;
};

import { getApiBaseUrl } from "../lib/api-base-url";

const labels: Record<string, string> = {
  "swift-clean-route": "SWIFT clean",
  "usdt-mixed-route": "USDT mixed",
  "cash-red-route": "Cash/P2P red",
  "mixed-capital-route": "Mixed capital",
  "developer-suspicious-route": "Suspicious developer",
  "agent-risk-route": "Agent risk",
  "prelaunch-off-platform-route": "Prelaunch off-platform",
  "tier-one-landmark-route": "Tier-1 Landmark",
};

export function ScenarioSimulator() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedId, setSelectedId] = useState("swift-clean-route");
  const [run, setRun] = useState<ScenarioRun | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function loadScenarios() {
      try {
        const response = await fetch(`${getApiBaseUrl()}/api/scenarios`);
        if (!response.ok) {
          throw new Error(`Scenario list returned ${response.status}`);
        }
        const data = (await response.json()) as { scenarios: Scenario[] };
        if (!cancelled) {
          setScenarios(data.scenarios);
        }
      } catch (caught) {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : "Unable to load scenarios");
        }
      }
    }

    void loadScenarios();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function runScenario() {
      try {
        const response = await fetch(`${getApiBaseUrl()}/api/scenarios/${selectedId}/rag-run`);
        if (!response.ok) {
          throw new Error(`Scenario run returned ${response.status}`);
        }
        const data = (await response.json()) as ScenarioRun;
        if (!cancelled) {
          setRun(data);
          setError(null);
        }
      } catch (caught) {
        if (!cancelled) {
          setError(caught instanceof Error ? caught.message : "Unable to run scenario");
        }
      }
    }

    void runScenario();

    return () => {
      cancelled = true;
    };
  }, [selectedId]);

  const selectedScenario = useMemo(
    () => scenarios.find((scenario) => scenario.id === selectedId),
    [scenarios, selectedId],
  );

  return (
    <section className="card">
      <div className="eyebrow">Scenario simulator</div>
      <h2>Run SWIFT, USDT, Cash/P2P And Risk Scenarios</h2>
      <p>
        Choose a synthetic scenario and see how capital status, property risk, agent risk, bank action, RAG trace, and
        Closing Passport outcome change.
      </p>

      {error ? (
        <p>
          Simulator unavailable: <code>{error}</code>
        </p>
      ) : null}

      <div className="scenario-picker">
        {scenarios.map((scenario) => (
          <button
            className={scenario.id === selectedId ? "scenario-button active" : "scenario-button"}
            key={scenario.id}
            onClick={() => setSelectedId(scenario.id)}
            type="button"
          >
            {labels[scenario.id] ?? scenario.id}
          </button>
        ))}
      </div>

      {selectedScenario && run ? (
        <div className="scenario-panels">
          <article className="mini-panel">
            <h3>Buyer</h3>
            <p>{run.buyer.profile}</p>
            <p>
              Capital: <span className={`status ${statusClass(run.capital_status)}`}>{run.capital_status}</span>
            </p>
          </article>
          <article className="mini-panel">
            <h3>Bank</h3>
            <p>{run.project.name}</p>
            <p>Route: {run.route_decision}</p>
            <p>
              Action: <span className={`status ${actionClass(run.bank_action)}`}>{run.bank_action}</span>
            </p>
          </article>
          <article className="mini-panel">
            <h3>Compliance</h3>
            <p>Property risk: {run.property_risk}</p>
            <p>Agent risk: {run.agent_risk}</p>
            <p>Evidence excludes: {run.evidence_preview.excluded_sensitive_fields.join(", ")}.</p>
          </article>
          <article className="mini-panel">
            <h3>Closing Passport</h3>
            <p>Status: {run.closing_passport_status}</p>
            {run.closing_passport_hash ? <code>{run.closing_passport_hash}</code> : <p>No passport for red route.</p>}
          </article>
          <article className="mini-panel wide">
            <h3>Retrieved Evidence</h3>
            <p>
              Mode: <strong>{run.retrieval_mode ?? "deterministic_trace"}</strong>
              {run.retrieval_fallback_reason ? ` · fallback: ${run.retrieval_fallback_reason}` : ""}
            </p>
            {(run.retrieved_evidence ?? []).map((item) => (
              <div className="evidence-row" key={item.document_id}>
                <p>
                  <strong>{item.document_id}</strong> · {item.kind} · score{" "}
                  {item.rerank_score ?? item.score}
                </p>
                <p>{item.excerpt}</p>
              </div>
            ))}
          </article>
          <article className="mini-panel wide">
            <h3>RAG Trace</h3>
            {run.rag_trace.map((item) => (
              <p key={`${item.kind}-${item.document_id}`}>
                <strong>{item.kind}</strong>: {item.document_id} · {item.reason}
              </p>
            ))}
          </article>
        </div>
      ) : (
        <p>Loading scenario run...</p>
      )}
    </section>
  );
}

function statusClass(status: string) {
  if (status === "green") {
    return "green";
  }
  if (status === "red") {
    return "red";
  }
  return "amber";
}

function actionClass(action: string) {
  if (action === "approve") {
    return "green";
  }
  if (action === "reject" || action === "escalate") {
    return "red";
  }
  return "amber";
}
