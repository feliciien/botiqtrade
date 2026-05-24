export const navItems = [
  { label: "Platform", href: "/#platform" },
  { label: "Risk", href: "/risk-governance" },
  { label: "Research", href: "/research-validation" },
  { label: "Partners", href: "/partners" },
  { label: "Investors", href: "/investors" },
];

export const operatingPrinciples = [
  "No profit promises",
  "No black-box claims",
  "No live access in partner pilots",
  "Risk gates before scale",
];

export const platformModules = [
  {
    kicker: "01 / Execution",
    title: "MT5 supervision",
    body: "Terminal health, account connectivity, trade permissions, live exports, EA decisions, spread, ATR, sessions, and blockers stay visible.",
  },
  {
    kicker: "02 / Risk",
    title: "Prop-firm guardrails",
    body: "Daily drawdown, total exposure, risk per trade, portfolio caps, emergency mode, safe mode, and manual-trade guardrails are first-class controls.",
  },
  {
    kicker: "03 / Audit",
    title: "Trade truth ledger",
    body: "Commands, risk snapshots, decision reasons, order comments, lineage tokens, deployment events, and closed-trade context are preserved for review.",
  },
  {
    kicker: "04 / Research",
    title: "Gate-based validation",
    body: "Offline mining, MT5 smoke tests, sensitivity matrices, walk-forward windows, no-go reports, and promotion blockers keep research disciplined.",
  },
  {
    kicker: "05 / Intelligence",
    title: "Owner decision support",
    body: "AI-assisted briefs translate telemetry into risk, execution, operations, compliance, and research context without hiding the final decision.",
  },
  {
    kicker: "06 / Monitoring",
    title: "Mobile command layer",
    body: "Owner dashboard, Telegram briefs, iPhone and Watch workflows prioritize actionable status over noisy alerts.",
  },
];

export const riskControls = [
  "Daily loss hard lock",
  "Challenge safe mode",
  "Max trades per day",
  "Max portfolio risk",
  "Manual-trading guard",
  "Emergency stop and close-managed flags",
  "News-window blocking",
  "Spread, margin, and permission gates",
];

export const validationStages = [
  {
    stage: "Offline ledger mining",
    decision: "Find hypotheses without spending MT5 runtime.",
    evidence: "Trade-level provenance, family de-duplication, hour and non-hour regime checks.",
  },
  {
    stage: "Smoke test",
    decision: "Verify mechanics before monthly validation.",
    evidence: "Telemetry token, order comment lineage, dashboard reconstruction, compile health.",
  },
  {
    stage: "Controlled MT5 window",
    decision: "Run only the smallest useful date window.",
    evidence: "June-only, JJA-only, or guard-vs-control tests before broader expansion.",
  },
  {
    stage: "Promotion gate",
    decision: "Accept, hold, or bury the family.",
    evidence: "Profit factor, drawdown, data quality, coverage, stress proxy, Monte Carlo, and no-go report.",
  },
];

export const proofPoints = [
  {
    label: "Current live build",
    value: "Telemetry lineage",
    detail: "Clean EX5 deployment with trade-comment token verification.",
  },
  {
    label: "Risk policy cap",
    value: "0.5%",
    detail: "Hard per-trade policy cap, with challenge-safe sizing tighter in live mode.",
  },
  {
    label: "Validation posture",
    value: "No-go aware",
    detail: "Rejected families are documented instead of hidden behind best-case curves.",
  },
  {
    label: "Data horizon",
    value: "5Y objective",
    detail: "Custom-tick robustness remains the target gate before scale.",
  },
];

export const partnerBoundaries = [
  "Sanitized JSON/CSV/Markdown samples only",
  "No broker credentials",
  "No MT5 account access",
  "No production access",
  "No live trading access",
  "No source-code exchange by default",
  "No secrets",
];
