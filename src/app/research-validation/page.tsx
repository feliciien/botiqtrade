import { Metadata } from "next";
import { Band, PageHero, PageShell, SectionHeading } from "@/components/site-shell";
import { validationStages } from "../site-data";

export const metadata: Metadata = {
  title: "Research Validation",
  description:
    "BoltIQ research validation uses offline mining, controlled MT5 smoke tests, walk-forward checks, no-go reports, and promotion gates.",
};

const buriedFamilies = [
  "frequency_probe / native_auto reuse unless independently revalidated",
  "hour-union overfitting without non-hour evidence",
  "families that fail June control before July/August expansion",
  "candidates dependent on one oversized report or narrow window",
];

export default function ResearchValidationPage() {
  return (
    <PageShell>
      <PageHero
        eyebrow="Research validation"
        title="A research system that is allowed to say no."
        body="BoltIQ treats no-go reports, buried hypotheses, and failed robustness checks as part of the product, not as embarrassing artifacts to hide."
      />
      <Band>
        <SectionHeading
          eyebrow="Gate sequence"
          title="More runtime is earned, not assumed."
          body="Each stage answers one question. If the answer is weak, the family is paused or buried before broader MT5 runs consume time."
        />
        <div className="mt-10 space-y-4">
          {validationStages.map((stage, index) => (
            <article key={stage.stage} className="grid gap-4 rounded-lg border border-stone-200 bg-white p-6 shadow-sm md:grid-cols-[120px_1fr]">
              <div className="text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700">
                Gate {String(index + 1).padStart(2, "0")}
              </div>
              <div>
                <h2 className="text-2xl font-semibold text-stone-950">{stage.stage}</h2>
                <p className="mt-2 text-sm font-semibold text-emerald-800">{stage.decision}</p>
                <p className="mt-3 text-base leading-7 text-stone-600">{stage.evidence}</p>
              </div>
            </article>
          ))}
        </div>
      </Band>
      <Band tone="dark">
        <div className="grid gap-12 lg:grid-cols-[0.9fr_1.1fr]">
          <SectionHeading
            eyebrow="No-go discipline"
            title="Rejected branches remain visible."
            body="A serious trading operation needs memory. Re-testing the same fragile family is avoided unless new independent evidence exists."
            tone="dark"
          />
          <div className="grid gap-3">
            {buriedFamilies.map((item) => (
              <div key={item} className="border-l-2 border-amber-300 bg-white/[0.07] px-5 py-4 text-sm font-medium text-stone-100">
                {item}
              </div>
            ))}
          </div>
        </div>
      </Band>
    </PageShell>
  );
}
