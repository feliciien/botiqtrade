import { Metadata } from "next";
import { Band, PageHero, PageShell, SectionHeading, TextCard } from "@/components/site-shell";
import { partnerBoundaries } from "../site-data";

export const metadata: Metadata = {
  title: "Partners",
  description:
    "BoltIQ partner pilots for audit, reporting, risk governance, telemetry schemas, MT5 automation reliability, and trading operations workflows.",
};

const deliverables = [
  {
    title: "Schema comparison",
    body: "Compare BoltIQ telemetry with a partner model without sharing production code, credentials, or live account access.",
  },
  {
    title: "Trade truth ledger",
    body: "Define the canonical event model for decision, command, risk, order, fill, position, close, and attribution records.",
  },
  {
    title: "Risk attribution report",
    body: "Classify whether a loss came from strategy, execution, spread, session, manual action, data gap, or rule breach.",
  },
];

export default function PartnersPage() {
  return (
    <PageShell>
      <PageHero
        eyebrow="Partner program"
        title="Technical-fit pilots before deeper collaboration."
        body="BoltIQ is open to serious partners in auditability, risk reporting, MT5 automation, operational monitoring, and trading governance."
      />
      <Band>
        <SectionHeading
          eyebrow="Boundaries"
          title="The first pilot is sanitized by design."
          body="The goal is to test architectural value without creating security, broker, account, or IP risk."
        />
        <div className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {partnerBoundaries.map((boundary) => (
            <div key={boundary} className="rounded-lg border border-stone-200 bg-white p-5 text-sm font-semibold text-stone-900 shadow-sm">
              {boundary}
            </div>
          ))}
        </div>
      </Band>
      <Band tone="dark">
        <div className="grid gap-5 md:grid-cols-3">
          {deliverables.map((item) => (
            <TextCard key={item.title} title={item.title} body={item.body} />
          ))}
        </div>
      </Band>
      <Band>
        <SectionHeading
          eyebrow="Contact"
          title="Propose measurable value, not access."
          body="For partnership conversations, send a short technical note, demo pack, schema sample, and the exact module you believe can improve BoltIQ."
        />
        <a
          href="mailto:feliciien@gmail.com?subject=BoltIQ%20partner%20pilot"
          className="mt-8 inline-flex rounded-full bg-stone-950 px-6 py-3 text-sm font-semibold text-white transition hover:bg-stone-800"
        >
          Contact the founder
        </a>
      </Band>
    </PageShell>
  );
}
