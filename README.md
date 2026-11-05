# Fergus Irvine

Builds the tools a bank client book runs on. Runs agent fleets on Claude Code.

`London · financial services · ex-navigation officer · Claude Code · Python · JS`

fergusirvine95@gmail.com · [LinkedIn](https://www.linkedin.com/in/fergus-irvine2203) · [Site](https://fergusirvine55-gif.github.io/fergus-irvine-agentic-ai-portfolio/)

Relationship manager at a global bank; I ship the dashboards and deck builders my desk uses. Seven years at sea before that. All data here is synthetic and checked against an independent recomputation.

## Start here

| If you run | Start with |
|---|---|
| Sales, account or partnerships teams | [Deck Builder demo](demo/) · [Merck / Pandion model](merck-pandion-ma-model/) |
| Solutions, deployment, forward-deployed | [Master build v41](projects/client-book-dashboards/client-book-deck-builder-v41.html) · [How I build with Claude](how-i-build-with-claude.md) |
| Product or strategy | [Peers and Explore tabs, v41](projects/client-book-dashboards/client-book-deck-builder-v41.html) · [Football Predictor: no edge](#personal-quant-and-decision-systems) |

## Projects

### Financial services

Built inside a global bank's securities-finance business: one master, three production releases, all synthetic here (the launch pad holds all four). Plus a deal model from public filings.

| Project | What | Stack | Proof | Links |
|---|---|---|---|---|
| Client Book Deck Builder, master v41 `demo` | Exposure analytics and deck builder. 13-factor peer benchmark, five-question explore surface, decks exported into the user's own PPTX template. | single-file HTML · SheetJS in a Web Worker · hand-rolled SVG · html2canvas · in-house PPTX ZIP writer | 7,014 lines, zero dependencies. 100k rows / 70 MB in ~49 s. t, F, trend and Granger-style tests, BH-adjusted. 41 builds. | [Open](projects/client-book-dashboards/client-book-deck-builder-v41.html) · [Project page](projects/client-book-dashboards/) · [Launch pad](projects/client-book-dashboards/dashboards-hub.html) |
| Client Exposure Dashboard, build 32 `live` | Client-facing release of the master: monitoring and branded deck export. Deployed globally; dozens of RMs and client-service staff use it monthly. | single-file HTML · SheetJS · SVG · html2canvas | 123- and 37-assertion test modules. Sanitised, it is this repo's live demo. | [Live demo](https://fergusirvine55-gif.github.io/fergus-irvine-agentic-ai-portfolio/demo/) · [Project page](projects/client-book-dashboards/) |
| EMEA Aged Receivables Dashboard, v1 `demo` | Receivables by RM and age bucket, unbilled revenue, monthly deck, fee-schedule tracker. Deployed globally to EMEA finance, billing and collections. | single-file HTML · SheetJS · SVG · Excel and PPTX export | Demo from 12 synthetic source files; every figure matched a Python recomputation to the cent. | [Open](projects/client-book-dashboards/emea-aged-receivables.html) · [Source data](projects/client-book-dashboards/data/aged-receivables/) |
| No-install Exposure Explorer `demo` | Drop a CSV; rank and filter lenders and borrowers. Earliest, lightest build; the global fallback. | single-file HTML, 490 KB · CSV | 2,400-row demo CSV; KPIs and rankings matched to Python. | [Open](projects/client-book-dashboards/lender-borrower.html) · [Demo CSV](projects/client-book-dashboards/data/lender-borrower/) |
| Merck & Co / Pandion acquisition model `live` | M&A model of a $1.85bn biotech acquisition from public filings: rNPV, SOTP, comps, precedents, PPA, accretion and dilution, synergies, scenarios. | Excel, 17 tabs · PPTX deal book · PDF guide | 751 live formulas, zero errors. Workbook by hand; documents AI-assisted. | [Folder](merck-pandion-ma-model/) · [Workbook](merck-pandion-ma-model/Merck_Pandion_Acquisition_Model.xlsx) |

### Personal quant and decision systems

Code is being prepared for release after a secrets scan. Figures are from the suites as they stand.

| Project | What | Stack | Proof | Links |
|---|---|---|---|---|
| Trade Advisor `in prep` | Multi-horizon trade decision support with outcome scoring and gated execution. | Vite + React · Express · Postgres on Render · FastAPI sidecar | 18-agent research run, 82 sources, ~1.2M tokens. 17-check safety suite. Live execution off by default behind 8 checks. |  |
| equity-advisor `in prep` | Equity research CLI; the valuation engine inside Trade Advisor. | Python · pytest | 115 tests in 31 files. Coverage 79% to 85% before the live gate opened. |  |
| algo-trader-v3 `in prep` | Trading pipeline in five gated stages: hypothesis, signal research, build, paper, live. | Python · hook-enforced gates · ADRs | 129 tests, 28 ADRs. A hook blocks stage advance until the prior gate reads PASS. 10+ edges killed before capital. |  |
| Football Predictor `in prep` | Win, draw, loss model. | Python · pytest | 196 tests. RPS 0.2018 on unseen data, 15 leagues, 34,903 matches. Conclusion: no edge against the market. |  |
| ETF Investment Simulator `in prep` | Monte Carlo comparison of 36 funds across UK brokers. | single-file HTML · Web Worker | 100,000 paths in the browser. Survivorship and recency warnings built in. |  |

### In preparation

Sanitised versions of this autumn's work, each landing as its own page.

- AI for ship operators: feasibility study from a 51-agent research run.
- Command-and-control AI layer for passenger ships: concept and gated method.
- Records-first prospecting: method and scoring rubric.
- Enterprise account plan template (private-credit manager, firm removed).
- Meeting-prep workspace demo on a fictional company.
- Target-account research pipeline on synthetic data: API ingest, classifier, embedding tiers, live dashboard.

## How I build with Claude

- Contabo VPS (12 vCPU, 47 GB) runs headless Claude Code for agent fleets. Mac is master; cloud sessions take overnight research.
- A hook forces a launch card before any agent run: three configurations, models and effort chosen fresh, usage share and finishing time. Nothing runs until I type go.
- Finders write to disk, a verifier re-checks, one judge decides. Briefs are files with an output schema.
- 196 / 129 / 115 tests; hook-enforced gates; kill scoreboard; pre-registration and held-out controls.
- Branch per task, draft PRs with a merge order, ADRs, HANDOVER and STATE files in every project.

Full page: [how-i-build-with-claude.md](how-i-build-with-claude.md)

## Repo map

```
.
├── demo/                              live demo, build 32
├── projects/client-book-dashboards/   four dashboards, launch pad, synthetic data
├── merck-pandion-ma-model/            workbook, deal book, guide
├── how-i-build-with-claude.md         setup page
├── portfolio.json                     source of README.md and index.html
└── build/build_portfolio.py           python3 build/build_portfolio.py
```

## Run locally

```bash
git clone https://github.com/fergusirvine55-gif/fergus-irvine-agentic-ai-portfolio.git
cd fergus-irvine-agentic-ai-portfolio
python3 -m http.server 8000
```

Open http://localhost:8000/ for the site, or any dashboard file directly. Edit portfolio.json, then run the build script.

## What this proves

- Deal maths and agent pipelines are one discipline: claim, test, number.
- Governance lives in the tooling: launch cards, hooks, gates, allow-lists, kill scoreboards.
- Negative results get published. The model that found no edge goes first.

---

v3 · 5 Nov 2026 · generated from [`portfolio.json`](portfolio.json) by [`build/build_portfolio.py`](build/build_portfolio.py)
