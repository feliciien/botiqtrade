import { Metadata } from "next";
import { Band, PageHero, PageShell, SectionHeading, TextCard } from "@/components/site-shell";

export const metadata: Metadata = {
  title: "Investors",
  description:
    "Investor overview for BoltIQ Trade: founder-led trading operations infrastructure focused on MT5 automation, risk governance, auditability, and research systems.",
};

const investorAngles = [
  {
    title: "Infrastructure before alpha claims",
    body: "BoltIQ is positioned as an operations and governance layer around automated trading, not as a public profit-promise product.",
  },
  {
    title: "Founder-operated feedback loop",
    body: "The same system supports live monitoring, research governance, deployment logs, and post-trade audit, keeping product learning close to real operations.",
  },
  {
    title: "Expandable SaaS surface",
    body: "Risk reporting, trade truth ledgers, audit packs, partner pilots, and owner dashboards can become standalone commercial modules.",
  },
];

export default function InvestorsPage() {
  return (
    <PageShell>
      <PageHero
        eyebrow="Investors"
        title="A trading operations layer with institutional discipline."
        body="BoltIQ's commercial path is strongest where automated trading teams need auditability, risk governance, monitoring, and research discipline."
      />
      <Band>
        <SectionHeading
          eyebrow="Data room"
          title="The investor discussion should start with governance evidence."
          body="The right review package includes the partner brief, valuation dossier, architecture overview, sanitized telemetry examples, and validation/no-go methodology."
        />
        <div className="mt-10 grid gap-5 md:grid-cols-3">
          {investorAngles.map((angle) => (
            <TextCard key={angle.title} title={angle.title} body={angle.body} />
          ))}
        </div>
        <a
          href="mailto:feliciien@gmail.com?subject=BoltIQ%20investor%20brief"
          className="mt-8 inline-flex rounded-full bg-stone-950 px-6 py-3 text-sm font-semibold text-white transition hover:bg-stone-800"
        >
          Request investor brief
        </a>
      </Band>
    </PageShell>
  );
}
