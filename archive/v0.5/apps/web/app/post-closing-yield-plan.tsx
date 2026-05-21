"use client";

import { useDemoFetch } from "../lib/use-demo-fetch";

type RentalMode = {
  status: string;
  note: string;
};

type Manager = {
  id: string;
  name: string;
  verified_by_platform: boolean;
  units_managed: number;
  average_occupancy_pct: number;
  complaint_rate: string;
  management_fee_pct: number;
  specialization: string;
};

type YieldPlanPayload = {
  after_purchase: {
    recommended_rental_model: string;
    short_term_rental: string;
    verified_manager_available: boolean;
    estimated_net_yield: string;
    yield_breakdown: {
      conservative_pct: number;
      base_pct: number;
      optimistic_pct: number;
      display_range: string;
    };
    rental_income_account: string;
    next_action: string;
  };
  legal_rental_mode: {
    long_term_lease: RentalMode;
    expat_rental_3_12m: RentalMode;
    short_term_under_30_days: RentalMode;
    serviced_apartment_hotel_model: RentalMode;
    juristic_person_restriction: string;
  };
  recommended_manager: Manager;
  bank_value: {
    pitch_line: string;
  };
};

function modeTone(status: string): string {
  if (status === "allowed" || status === "likely_allowed") {
    return "green";
  }
  if (status === "requires_verification") {
    return "amber";
  }
  return "red";
}

export function PostClosingYieldPlan() {
  const { data: payload, error, loading } = useDemoFetch<YieldPlanPayload>("/api/demo/post-closing-yield-plan");

  if (error) {
    return (
      <div className="card yield-plan">
        <h2>Post-Closing Yield Plan</h2>
        <p>
          Vision screen unavailable: <code>{error}</code>
        </p>
        <p>Start the FastAPI service to show the strategic extension after Closing Passport.</p>
      </div>
    );
  }

  if (loading || !payload) {
    return (
      <div className="card yield-plan">
        <h2>Post-Closing Yield Plan</h2>
        <p>Loading Bankable Property &amp; Yield OS vision from FastAPI...</p>
      </div>
    );
  }

  const rentalModes = [
    { label: "Long-term lease", mode: payload.legal_rental_mode.long_term_lease },
    { label: "3–12 month expat rental", mode: payload.legal_rental_mode.expat_rental_3_12m },
    { label: "Short-term under 30 days", mode: payload.legal_rental_mode.short_term_under_30_days },
    { label: "Serviced apartment / hotel model", mode: payload.legal_rental_mode.serviced_apartment_hotel_model },
  ];

  const verifiedTone = payload.recommended_manager.verified_by_platform ? "green" : "amber";
  const verifiedLabel = payload.recommended_manager.verified_by_platform ? "platform verified" : "verification pending";

  return (
    <div className="card yield-plan">
      <div className="eyebrow">Strategic Extension · Bankable Property &amp; Yield OS</div>
      <h2>Post-Closing Yield Plan</h2>
      <p className="vision-lead">
        Purchase is not the end of the deal. It is the start of the asset lifecycle. After Closing Passport, the bank
        can help turn verified property into a compliant, professionally managed income asset.
      </p>

      <div className="vision-grid">
        <article className="vision-card">
          <h3>After Purchase</h3>
          <p>
            <strong>Recommended model:</strong> {payload.after_purchase.recommended_rental_model}
          </p>
          <p>
            <strong>Short-term rental:</strong> {payload.after_purchase.short_term_rental}
          </p>
          <p>
            <strong>Estimated net yield:</strong>{" "}
            <span className="status green">{payload.after_purchase.estimated_net_yield}</span>
          </p>
          <p>
            Breakdown: {payload.after_purchase.yield_breakdown.conservative_pct}% conservative ·{" "}
            {payload.after_purchase.yield_breakdown.base_pct}% base · {payload.after_purchase.yield_breakdown.optimistic_pct}%
            optimistic
          </p>
          <p>
            <strong>Rental income account:</strong> {payload.after_purchase.rental_income_account}
          </p>
          <p>
            <strong>Next action:</strong> {payload.after_purchase.next_action}
          </p>
        </article>

        <article className="vision-card">
          <h3>Legal Rental Mode</h3>
          {rentalModes.map((item) => (
            <p key={item.label}>
              <span className={`status ${modeTone(item.mode.status)}`}>{item.mode.status.replaceAll("_", " ")}</span>{" "}
              <strong>{item.label}</strong> · {item.mode.note}
            </p>
          ))}
          <p className="vision-note">{payload.legal_rental_mode.juristic_person_restriction}</p>
        </article>

        <article className="vision-card">
          <h3>Verified Manager</h3>
          <p>
            <strong>{payload.recommended_manager.name}</strong>
          </p>
          <p>
            {payload.recommended_manager.units_managed} units · {payload.recommended_manager.average_occupancy_pct}%
            occupancy · {payload.recommended_manager.management_fee_pct}% fee
          </p>
          <p>{payload.recommended_manager.specialization}</p>
          <span className={`status ${verifiedTone}`}>{verifiedLabel}</span>
        </article>
      </div>

      <p className="vision-close">{payload.bank_value.pitch_line}</p>
    </div>
  );
}
