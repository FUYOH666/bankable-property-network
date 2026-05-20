const outcomes = [
  { label: "SWIFT clean", result: "approve", tone: "green", detail: "FET-ready escrow and Closing Passport generated." },
  { label: "USDT mixed", result: "conditional", tone: "amber", detail: "Wallet review and conversion evidence required." },
  { label: "Cash/P2P", result: "reject", tone: "red", detail: "Unsupported cash-like route, no normal passport." },
  { label: "Suspicious developer", result: "escalate", tone: "red", detail: "Green capital, but payee authority blocks release." },
];

const roadmap = ["24h demo", "2w pilot", "6w bank pilot", "3m regulated pilot", "6m multi-bank network"];

export function PitchScreen() {
  return (
    <section className="pitch-screen">
      <div className="eyebrow">Pitch Screen · Money infrastructure narrative</div>
      <h2>Bank-Grade Money Infrastructure For Thailand Property</h2>
      <p className="pitch-lead">
        Thailand&apos;s property market runs on developer-paid commissions with no professional entry barrier. Bankable
        Property OS gives banks and regulated structures the operating layer to control settlement flow — and buyers
        benefit as a side effect.
      </p>

      <div className="pitch-grid">
        <article className="pitch-card">
          <h3>Structural Problem</h3>
          <p>
            Commission-driven intermediaries enter deals without skill verification. Visa rules, FET, ownership limits,
            and payee authority go unchecked. Money moves off bankable rails.
          </p>
        </article>
        <article className="pitch-card">
          <h3>Money OS Solution</h3>
          <p>
            Banking anchors verify participants, classify capital, route settlement, control escrow, and preserve
            privacy-safe evidence. AI scales review; compliance officers approve.
          </p>
        </article>
        <article className="pitch-card">
          <h3>Brand Alignment</h3>
          <p>
            Kingdom brand promise expects institutional-grade settlement. This infrastructure closes the gap between
            brand and market reality — traceable inflows, verified paths, fewer grey routes.
          </p>
        </article>
        <article className="pitch-card">
          <h3>Developer Knowledge Hub</h3>
          <p>
            Developer ERP feed is the source of truth for inventory, payee, and installments. Verified agencies consume
            facts from the hub — they do not invent terms to capture commission faster.
          </p>
        </article>
        <article className="pitch-card">
          <h3>Why Developers Join</h3>
          <p>
            Off-platform prelaunch sales hide permit and payee gaps — buyers lose deposits before banks can intervene.
            On-network tier-1 feeds expose inventory, authorized payees, and escrow-ready paths before the first buyer
            arrives.
          </p>
        </article>
        <article className="pitch-card">
          <h3>Social Bonus</h3>
          <p>
            Buyers avoid irreversible deposits to wrong entities and receive bankable routes instead of ad hoc agent
            instructions — a side effect of infrastructure, not the primary mission.
          </p>
        </article>
      </div>

      <div className="pitch-grid">
        {outcomes.map((outcome) => (
          <article className="pitch-card" key={outcome.label}>
            <h3>{outcome.label}</h3>
            <span className={`status ${outcome.tone}`}>{outcome.result}</span>
            <p>{outcome.detail}</p>
          </article>
        ))}
      </div>

      <div className="pitch-grid">
        <article className="pitch-card">
          <h3>Bank Value</h3>
          <p>Capture high-value flow, onboard affluent clients, reduce risk, sell escrow/compliance packages, extend to yield.</p>
        </article>
        <article className="pitch-card">
          <h3>AI Layer</h3>
          <p>
            Qdrant, embeddings, reranker, schema-bound LLM explainability. AI scales evidence review — it does not
            autonomously move money.
          </p>
        </article>
        <article className="pitch-card">
          <h3>Web3 Use</h3>
          <p>Metadata-only evidence attestation. No property tokenization, no sensitive data on-chain.</p>
        </article>
      </div>

      <div className="roadmap-strip">
        {roadmap.map((item) => (
          <span key={item}>{item}</span>
        ))}
      </div>
    </section>
  );
}
