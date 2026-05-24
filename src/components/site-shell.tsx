import Image from "next/image";
import Link from "next/link";
import { navItems } from "@/app/site-data";

export function Header() {
  return (
    <header className="fixed left-0 right-0 top-0 z-50 border-b border-white/10 bg-[#07100d]/88 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4 sm:px-8">
        <Link href="/" className="flex items-center gap-3" aria-label="BoltIQ Trade home">
          <Image src="/assets/boltiq-mark.svg" alt="" width={34} height={34} priority />
          <div>
            <div className="text-sm font-semibold uppercase tracking-[0.24em] text-white">
              BoltIQ Trade
            </div>
            <div className="text-xs text-emerald-100/70">Risk-first trading infrastructure</div>
          </div>
        </Link>
        <nav className="hidden items-center gap-7 text-sm text-stone-200 md:flex">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="transition hover:text-white">
              {item.label}
            </Link>
          ))}
        </nav>
        <a
          href="mailto:feliciien@gmail.com?subject=BoltIQ%20Trade%20technical%20discussion"
          className="rounded-full border border-emerald-300/35 px-4 py-2 text-sm font-medium text-emerald-50 transition hover:border-emerald-200 hover:bg-emerald-200/10"
        >
          Founder contact
        </a>
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-stone-200 bg-stone-50">
      <div className="mx-auto grid max-w-7xl gap-8 px-5 py-10 text-sm text-stone-600 sm:px-8 lg:grid-cols-[1.2fr_0.8fr]">
        <div>
          <div className="mb-3 flex items-center gap-3">
            <Image src="/assets/boltiq-mark.svg" alt="" width={32} height={32} />
            <span className="font-semibold uppercase tracking-[0.2em] text-stone-950">
              BoltIQ Trade
            </span>
          </div>
          <p className="max-w-3xl leading-6">
            BoltIQ Trade is a technology and research project. Nothing on this website is
            financial advice, investment advice, a solicitation, or a promise of performance.
            Trading foreign exchange, commodities, indices, cryptocurrencies, and derivatives
            involves substantial risk.
          </p>
        </div>
        <div className="flex flex-col gap-2 lg:items-end">
          <a className="text-stone-950 hover:underline" href="mailto:feliciien@gmail.com">
            feliciien@gmail.com
          </a>
          <a
            className="text-stone-950 hover:underline"
            href="https://github.com/feliciien"
            target="_blank"
            rel="noreferrer"
          >
            GitHub @feliciien
          </a>
          <Link className="text-stone-950 hover:underline" href="/legal-disclaimer">
            Legal disclaimer
          </Link>
          <span className="pt-2 text-xs text-stone-500">&copy; 2026 BoltIQ Trade</span>
        </div>
      </div>
    </footer>
  );
}

export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-stone-50 text-stone-950">
      <Header />
      {children}
      <Footer />
    </main>
  );
}

export function PageHero({
  eyebrow,
  title,
  body,
}: {
  eyebrow: string;
  title: string;
  body: string;
}) {
  return (
    <section className="bg-[#07100d] px-5 pb-16 pt-32 text-white sm:px-8">
      <div className="mx-auto max-w-7xl">
        <p className="mb-5 text-sm font-semibold uppercase tracking-[0.28em] text-emerald-200">
          {eyebrow}
        </p>
        <h1 className="max-w-4xl text-4xl font-semibold leading-[1.03] tracking-normal sm:text-6xl">
          {title}
        </h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-stone-200">{body}</p>
      </div>
    </section>
  );
}

export function SectionHeading({
  eyebrow,
  title,
  body,
  tone = "light",
}: {
  eyebrow: string;
  title: string;
  body: string;
  tone?: "light" | "dark";
}) {
  return (
    <div className="max-w-3xl">
      <p
        className={
          tone === "dark"
            ? "mb-3 text-sm font-semibold uppercase tracking-[0.24em] text-emerald-200"
            : "mb-3 text-sm font-semibold uppercase tracking-[0.24em] text-emerald-700"
        }
      >
        {eyebrow}
      </p>
      <h2
        className={
          tone === "dark"
            ? "text-3xl font-semibold tracking-normal text-white sm:text-5xl"
            : "text-3xl font-semibold tracking-normal text-stone-950 sm:text-5xl"
        }
      >
        {title}
      </h2>
      <p
        className={
          tone === "dark"
            ? "mt-5 text-base leading-7 text-stone-300 sm:text-lg"
            : "mt-5 text-base leading-7 text-stone-600 sm:text-lg"
        }
      >
        {body}
      </p>
    </div>
  );
}

export function TextCard({
  kicker,
  title,
  body,
}: {
  kicker?: string;
  title: string;
  body: string;
}) {
  return (
    <article className="rounded-lg border border-stone-200 bg-white p-6 shadow-sm">
      {kicker ? (
        <p className="mb-4 text-xs font-semibold uppercase tracking-[0.22em] text-emerald-700">
          {kicker}
        </p>
      ) : null}
      <h3 className="text-xl font-semibold tracking-normal text-stone-950">{title}</h3>
      <p className="mt-3 text-sm leading-6 text-stone-600">{body}</p>
    </article>
  );
}

export function Band({ children, tone = "light" }: { children: React.ReactNode; tone?: "light" | "dark" }) {
  return (
    <section className={tone === "dark" ? "bg-[#07100d] px-5 py-20 text-white sm:px-8" : "bg-stone-50 px-5 py-20 sm:px-8"}>
      <div className="mx-auto max-w-7xl">{children}</div>
    </section>
  );
}
