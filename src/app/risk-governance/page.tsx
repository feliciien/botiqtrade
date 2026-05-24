import { Metadata } from "next";
import { Band, PageHero, PageShell, SectionHeading, TextCard } from "@/components/site-shell";
import { riskControls } from "../site-data";

export const metadata: Metadata = {
  title: "Risk Governance",
  description:
    "BoltIQ risk governance for daily drawdown, prop-firm guardrails, manual-trading controls, emergency locks, and audit-ready trading operations.",
};

const policies = [
  {
    title: "Hard controls remain non-bypassable",
    body: "Daily loss, drawdown, broker permission, emergency stop, safe mode, and account-level risk locks are treated as hard controls, not preferences.",
  },
  {
    title: "Manual action is audit context",
    body: "Manual actions can document intent, approve workflow, reduce risk, or stop exposure. They do not override hard safety gates.",
  },
  {
    title: "Live risk stays below research ambition",
    body: "Research may explore aggressive candidates, but live deployment is restricted by tighter trade count, exposure, news, and drawdown limits.",
  },
];

export default function RiskGovernancePage() {
  return (
    <PageShell>
      <PageHero
        eyebrow="Risk governance"
        title="The risk engine is the product boundary."
        body="BoltIQ is designed around prop-firm survival, account protection, and explicit audit trails before any attempt to scale a strategy."
      />
      <Band>
        <SectionHeading
          eyebrow="Live controls"
          title="Controls that stop the system before the account breaks rules."
          body="Risk governance is visible, repeatable, and reviewable. The owner should know why trading is blocked before exposure is added."
        />
        <div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {riskControls.map((control) => (
            <div key={control} className="rounded-lg border border-stone-200 bg-white p-5 text-sm font-semibold text-stone-900 shadow-sm">
              {control}
            </div>
          ))}
        </div>
      </Band>
      <Band tone="dark">
        <div className="grid gap-5 md:grid-cols-3">
          {policies.map((policy) => (
            <TextCard key={policy.title} title={policy.title} body={policy.body} />
          ))}
        </div>
      </Band>
    </PageShell>
  );
}
