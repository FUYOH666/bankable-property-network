export default function Page() {
  return (
    <main>
      <section className="hero">
        <div className="eyebrow">v1.0.0 · Settlement Attestation Layer for RWA</div>
        <h1>AttestRWA</h1>
        <p>
          On-chain compliance bridge that turns bank verification rules into machine-verifiable attestations, so
          stablecoin payments for real-world assets release only when the deal is bank-grade.
        </p>
        <p>
          <a className="button-link" href="/rwa-settlement-live">Open the live settlement demo</a>
        </p>
      </section>

      <section className="grid">
        <div className="card">
          <h2>Status</h2>
          <p>
            Hackathon-ready. Live settlement demo with wallet connect, programmable escrow on Base Sepolia (dev fork),
            EAS attestations, approve + reject E2E scripts, and an 85-second recorded walkthrough.
          </p>
          <p>
            Repository: <a href="https://github.com/FUYOH666/bankable-property-network">FUYOH666/bankable-property-network</a>
            (public, branch <code>main</code>).
          </p>
        </div>

        <div className="card">
          <h2>On-chain artefacts (dev fork of Base Sepolia)</h2>
          <ul>
            <li>
              <strong>SettlementEscrow.sol:</strong>
              <code>0x54D4962847bf85AB71a1Fc984510dc12D3feA1D8</code>
            </li>
            <li>
              <strong>MockUSDC.sol:</strong>
              <code>0xeba5CEc9257045Df0B44eA784F9a7Fa07DeeF6d4</code>
            </li>
            <li>
              <strong>EAS Schema UID:</strong>
              <code>0x1f64ec96216b0381dc4443b7378c57485f2217656537e8ea36f0b23af047cc96</code>
            </li>
            <li>
              <strong>EAS contract:</strong>
              <code>0x4200000000000000000000000000000000000021</code>
            </li>
            <li>
              <strong>Attester EOA (dev):</strong>
              <code>0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266</code>
            </li>
          </ul>
        </div>

        <div className="card">
          <h2>What we&apos;re building</h2>
          <ul>
            <li>Programmable settlement escrow on Base Sepolia (Foundry, fuzz tests, slither-clean).</li>
            <li>On-chain EAS attestations as the compliance primitive.</li>
            <li>Off-chain attester service with RAG-assisted evidence review (FastAPI + Qdrant + BGE).</li>
            <li>Single-screen wallet-connect demo flow.</li>
            <li>Farcaster Frame for viral distribution; Dune dashboard for public on-chain metrics.</li>
          </ul>
        </div>

        <div className="card">
          <h2>Pivot story</h2>
          <p>
            We started as B2B bank-grade settlement infrastructure for Thailand property. Before SEABW 2026 we ran a
            market check and saw that RWA&apos;s real bottleneck in 2026 is not tokenization — it&apos;s compliance. We
            pivoted to a web3-native attestation primitive and shipped the full stack in roughly four hours of
            AI-assisted development.
          </p>
          <p>
            See <code>archive/v0.5/</code> for the previous generation. We kept what mattered (payee verification,
            capital classification, RAG, FastAPI+Next.js base, 64 pytest baseline), killed what didn&apos;t.
          </p>
        </div>
      </section>
    </main>
  );
}
