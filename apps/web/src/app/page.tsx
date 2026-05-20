import { ClosingPassportPanel } from "./closing-passport-panel";
import { DeveloperKnowledgeHub } from "./developer-knowledge-hub";
import { GuidedDealSimulation } from "./guided-deal-simulation";
import { PitchScreen } from "./pitch-screen";
import { PostClosingYieldPlan } from "./post-closing-yield-plan";
import { ScenarioSimulator } from "./scenario-simulator";
import { SupplierContrastDemo } from "./supplier-contrast-demo";

const demoSteps = [
  "Supplier Contrast compares off-platform prelaunch (permit gaps) vs tier-1 on-network developer feed.",
  "Developer Knowledge Hub compares agent payee instruction against developer ERP feed.",
  "Property Shield flags payee mismatch, urgency, and missing buyer protection.",
  "Capital Bankability Map classifies funds as green, amber, or red.",
  "Route Comparison rejects direct deposit and recommends bankable escrow.",
  "Bank Counter-Offer routes settlement through verified escrow.",
  "Compliance approves the controlled route.",
  "Closing Passport hashes the evidence pack without exposing sensitive data.",
  "Post-Closing Yield Plan previews long-term asset operations on bank rails.",
];

export default function Page() {
  return (
    <main>
      <section className="hero">
        <div className="eyebrow">Synthetic demo data · SEABW · Bankable Property Network</div>
        <h1>Bankable Property Network</h1>
        <p>
          Bank-grade money infrastructure for Thailand property. Bankable Property OS gives banks and regulated
          structures control over settlement flow — buyer protection is the social bonus when infrastructure works.
        </p>
      </section>

      <PitchScreen />

      <section className="grid">
        <SupplierContrastDemo />
      </section>

      <section className="grid">
        <DeveloperKnowledgeHub />
      </section>

      <section className="grid">
        <div className="card">
          <h2>Anchor Case</h2>
          <p>
            Illustration of infrastructure failure: money is about to move through an unverified path on a 12M THB
            Bangkok condo. Commission-driven intermediary, payee mismatch, deposit pressure — not a buyer competence
            story.
          </p>
          <span className="status red">Unverified settlement path</span>
        </div>
        <div className="card">
          <h2>Primary Customer</h2>
          <p>
            Banking anchor and regulated money-serving structures. This is not a listing marketplace — it is the
            operating layer that captures flow, controls escrow, and preserves audit-ready evidence.
          </p>
        </div>
        <div className="card">
          <h2>Web3 Use</h2>
          <p>
            We do not tokenize the property. We tokenize the evidence of a verified settlement process through a
            metadata-only attestation.
          </p>
        </div>
      </section>

      <section className="grid">
        <ClosingPassportPanel />
      </section>

      <section className="grid">
        <PostClosingYieldPlan />
      </section>

      <GuidedDealSimulation />

      <ScenarioSimulator />

      <section className="grid steps">
        {demoSteps.map((step) => (
          <div className="card step" key={step}>
            <h3>{step}</h3>
          </div>
        ))}
      </section>
    </main>
  );
}
