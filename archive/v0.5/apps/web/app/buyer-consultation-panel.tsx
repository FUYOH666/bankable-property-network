"use client";

import { FormEvent, useState } from "react";

import { getApiBaseUrl } from "../lib/api-base-url";

type ConsultPayload = {
  reply: string;
  retrieval_mode: string;
  tools_used: string[];
  safety_note: string;
};

type ChatLine = {
  role: "user" | "assistant";
  text: string;
};

export function BuyerConsultationPanel() {
  const [lines, setLines] = useState<ChatLine[]>([
    {
      role: "assistant",
      text: "Buyer Consultation (synthetic demo). Ask about payee mismatch, SWIFT/USDT/cash routes, or prelaunch vs tier-1 supply. I cite API facts — banks decide on bankable rails.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [meta, setMeta] = useState<{ mode: string; tools: string[] } | null>(null);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    const message = input.trim();
    if (!message || loading) return;

    setInput("");
    setError(null);
    setLines((prev) => [...prev, { role: "user", text: message }]);
    setLoading(true);

    try {
      const response = await fetch(`${getApiBaseUrl()}/api/consult/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: "web-demo",
          message,
          channel: "web",
        }),
      });
      if (!response.ok) {
        throw new Error(`API returned ${response.status}`);
      }
      const payload = (await response.json()) as ConsultPayload;
      setLines((prev) => [...prev, { role: "assistant", text: payload.reply }]);
      setMeta({ mode: payload.retrieval_mode, tools: payload.tools_used });
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Consultation request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card consult-panel">
      <h2>Buyer Consultation (Web Fallback)</h2>
      <p>
        Same consultation API as the WhatsApp bridge — template fallback when LM Studio is offline. Synthetic facts
        only; never approves deposits.
      </p>
      <div className="consult-log" aria-live="polite">
        {lines.map((line, index) => (
          <div className={`consult-line ${line.role}`} key={`${line.role}-${index}`}>
            <strong>{line.role === "user" ? "You" : "Consultant"}:</strong> {line.text}
          </div>
        ))}
        {loading ? <div className="consult-line assistant">Consultant is typing…</div> : null}
      </div>
      {error ? <p className="error">{error}</p> : null}
      {meta ? (
        <p className="muted">
          Mode: {meta.mode} · Tools: {meta.tools.join(", ")}
        </p>
      ) : null}
      <form className="consult-form" onSubmit={onSubmit}>
        <input
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask about cash route, payee mismatch, or Shadow Bay prelaunch…"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
