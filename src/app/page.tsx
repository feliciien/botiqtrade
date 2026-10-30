import Image from "next/image";
import Link from "next/link";
import {
  operatingPrinciples,
  platformModules,
  proofPoints,
  riskControls,
  validationStages,
} from "./site-data";
import { Band, PageShell, SectionHeading, TextCard } from "@/components/site-shell";

export default function Home() {
  return (
    <PageShell>
      <section className="relative min-h-[88vh] overflow-hidden bg-[#07100d] px-5 pb-16 pt-28 text-white sm:px-8">
        <Image
          src="/assets/boltiq-command-center.png"
          alt="BoltIQ command center interface for MT5 execution, risk guardrails, research, AI committee, mobile monitoring, and owner dashboard modules."
          fill
          priority
          className="object-cover opacity-44"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-[#07100d]/72" />
        <div className="relative mx-auto flex min-h-[72vh] max-w-7xl flex-col justify-end">
          <p className="mb-5 max-w-max border border-emerald-200/30 px-3 py-2 text-xs font-semibold uppercase tracking-[0.28em] text-emerald-100">
            BoltIQ Trade research portal
          </p>
          <h1 className="max-w-5xl text-5xl font-semibold leading-[0.98] tracking-normal sm:text-7xl lg:text-8xl">
            Trading operations infrastructure, not a black-box bot.
          </h1>
          <p className="mt-7 max-w-3xl text-lg leading-8 text-stone-100 sm:text-xl">
            BoltIQ connects MT5 execution, prop-firm risk governance, audit trails,
            research validation, AI-assisted context, and owner monitoring into one
            command layer.
          </p>
          <p className="mt-5 max-w-3xl text-base leading-7 text-emerald-100">
            Official BoltIQ Markets website:{" "}
            <a href="https://boltiqmarkets.com/" className="font-semibold underline underline-offset-4 hover:text-white">
              boltiqmarkets.com
            </a>
            {" "}— browse MT5 products, developer services and research demos. This research portal is not a broker and does not accept customer trading deposits.
          </p>
          <div className="mt-9 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/partners"
              className="rounded-full bg-emerald-300 px-6 py-3 text-center text-sm font-semibold text-stone-950 transition hover:bg-emerald-200"
            >
              Partner with BoltIQ
            </Link>
            <Link
              href="/investors"
              className="rounded-full border border-white/35 px-6 py-3 text-center text-sm font-semibold text-white transition hover:bg-white/10"
            >
              Request investor brief
            </Link>
            <Link
              href="/research-validation"
              className="rounded-full border border-white/20 px-6 py-3 text-center text-sm font-semibold text-white transition hover:bg-white/10"
            >
              View research governance
            </Link>
          </div>
        </div>
      </section>

      <Band>
        <div className="grid gap-4 md:grid-cols-4">
          {operatingPrinciples.map((item) => (
            <div
              key={item}
              className="rounded-lg border border-stone-200 bg-white p-5 text-sm font-semibold text-stone-900 shadow-sm"
            >
              {item}
            </div>
          ))}
        </div>
      </Band>

      <Band>
        <div id="platform" className="scroll-mt-28">
          <SectionHeading
            eyebrow="Platform"
            title="One command center for the trading operation."
            body="Execution, risk, research, mobile monitoring, and owner decisions are connected into a single operating layer designed for visibility before autonomy."
          />
          <div className="mt-12 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {platformModules.map((module) => (
              <TextCard
                key={module.title}
                kicker={module.kicker}
                title={module.title}
                body={module.body}
              />
            ))}
          </div>
        </div>
      </Band>

      <Band tone="dark">
        <div className="grid gap-12 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
          <SectionHeading
            eyebrow="Proof, not promises"
            title="Research-first growth, capital-first execution."
            body="BoltIQ is designed to improve through evidence. Best-case backtests are not treated as deployment proof unless the family survives controlled validation and risk review."
            tone="dark"
          />
          <div className="grid gap-4 sm:grid-cols-2">
            {proofPoints.map((point) => (
              <article
                key={point.label}
                className="rounded-lg border border-white/12 bg-white/[0.06] p-6"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-emerald-200">
                  {point.label}
                </p>
                <div className="mt-4 text-3xl font-semibold text-white">{point.value}</div>
                <p className="mt-3 text-sm leading-6 text-stone-300">{point.detail}</p>
              </article>
            ))}
          </div>
        </div>
      </Band>

      <Band>
        <div className="grid gap-12 lg:grid-cols-[1fr_1fr]">
          <div>
            <SectionHeading
              eyebrow="Risk governance"
              title="Designed to stop rule breaches before chasing returns."
              body="The live posture favors hard locks, exposure caps, and operator visibility over uncontrolled scaling."
            />
            <div className="mt-8 grid gap-3 sm:grid-cols-2">
              {riskControls.map((control) => (
                <div
                  key={control}
                  className="border-l-2 border-emerald-600 bg-white px-4 py-3 text-sm font-medium text-stone-800 shadow-sm"
                >
                  {control}
                </div>
              ))}
            </div>
          </div>
          <div>
            <SectionHeading
              eyebrow="Validation workflow"
              title="A candidate earns more runtime only after surviving the previous gate."
              body="The system explicitly records why a family advances, holds, or gets buried."
            />
            <div className="mt-8 space-y-4">
              {validationStages.map((stage) => (
                <article key={stage.stage} className="rounded-lg border border-stone-200 bg-white p-5 shadow-sm">
                  <h3 className="text-lg font-semibold text-stone-950">{stage.stage}</h3>
                  <p className="mt-2 text-sm font-medium text-emerald-800">{stage.decision}</p>
                  <p className="mt-2 text-sm leading-6 text-stone-600">{stage.evidence}</p>
                </article>
              ))}
            </div>
          </div>
        </div>
      </Band>

      <Band tone="dark">
        <div className="grid gap-8 lg:grid-cols-[1fr_0.8fr] lg:items-center">
          <div>
            <p className="mb-4 text-sm font-semibold uppercase tracking-[0.24em] text-emerald-200">
              Founder-led build
            </p>
            <h2 className="max-w-4xl text-4xl font-semibold tracking-normal text-white sm:text-6xl">
              Build the future of auditable trading infrastructure.
            </h2>
            <p className="mt-6 max-w-3xl text-lg leading-8 text-stone-300">
              BoltIQ is open to technical partnerships, audit and reporting pilots,
              investor conversations, and strategic product discussions where measurable
              value and clear boundaries come first.
            </p>
          </div>
          <div className="flex flex-col gap-3">
            <Link
              className="rounded-full bg-emerald-300 px-6 py-3 text-center text-sm font-semibold text-stone-950 transition hover:bg-emerald-200"
              href="/partners"
            >
              Start a technical-fit pilot
            </Link>
            <Link
              className="rounded-full border border-white/25 px-6 py-3 text-center text-sm font-semibold text-white transition hover:bg-white/10"
              href="/investors"
            >
              Request the investor data room
            </Link>
          </div>
        </div>
      </Band>
    </PageShell>
  );
}
