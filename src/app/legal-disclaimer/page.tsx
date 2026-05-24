import { Metadata } from "next";
import { Band, PageHero, PageShell } from "@/components/site-shell";

export const metadata: Metadata = {
  title: "Legal Disclaimer",
  description:
    "BoltIQ Trade legal disclaimer for technology, research, risk, simulated performance, and financial-advice boundaries.",
};

export default function LegalDisclaimerPage() {
  return (
    <PageShell>
      <PageHero
        eyebrow="Legal disclaimer"
        title="Technology and research, not financial advice."
        body="BoltIQ Trade is presented as trading infrastructure and research governance. It is not a solicitation, investment recommendation, or promise of performance."
      />
      <Band>
        <div className="max-w-4xl space-y-6 text-base leading-8 text-stone-700">
          <p>
            Nothing on this website is financial advice, investment advice, a trading
            recommendation, a solicitation, or a promise of performance. Trading foreign
            exchange, commodities, indices, cryptocurrencies, and derivatives involves
            substantial risk and can result in loss of capital.
          </p>
          <p>
            Backtests, simulations, telemetry examples, research reports, and validation
            workflows are not guarantees of future results. Past or simulated performance
            does not guarantee future performance.
          </p>
          <p>
            Any automated system should be evaluated under strict risk controls, broker
            rules, prop-firm rules, and applicable regulations before live deployment.
            BoltIQ emphasizes auditability, risk governance, and controlled validation
            precisely because automated trading systems can fail.
          </p>
        </div>
      </Band>
    </PageShell>
  );
}
