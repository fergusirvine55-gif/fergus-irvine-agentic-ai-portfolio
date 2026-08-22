# Fergus Irvine — AI Builder Portfolio

fergusirvine95@gmail.com · [LinkedIn](https://www.linkedin.com/in/fergus-irvine2203)

Enterprise Product and Account Management in financial services who builds agentic AI systems daily, not occasionally. This repo is evidence: projects, their test suites, and what they actually proved.

## How I work with agentic AI

- **Multi-agent fan-out** — decomposing research, review, and validation work across parallel agents rather than running everything serially through one context.
- **Falsification-first** — trying to disprove my own ideas before trusting them. A model or strategy earns confidence by surviving an attempt to kill it, not by sounding plausible.
- **Evidence-before-assertion** — never claiming something works without running it. Every project below is backed by a test suite, and the numbers are the numbers whether or not they're flattering.
- **Fail-closed, test-driven** — systems default to safe/off, not to "probably fine." Gates and checks block progression until an artifact explicitly proves the previous stage passed.

## Projects

| Project | What it is | Built with agentic AI | Scale / proof |
|---|---|---|---|
| **Client Book Dashboard & Deck Builder** | Single-file HTML tool for a global bank's collateral/exposure reporting workflow. Pure client-side (SheetJS/xlsx.js) — no backend, no data leaves the browser. | Yes | Handles ~100k-row / 70MB spreadsheet extracts, ~49s parse time; 123- and 37-assertion test modules. Live demo included, see below. |
| **Merck & Co / Pandion Therapeutics Acquisition Model** | Full-scope M&A acquisition model reconstructing Merck's $1.85bn acquisition of Pandion Therapeutics (Feb 2021), built entirely from public filings (SEC, press releases). | Partial — core 17-tab workbook built manually; documentation, deal book and methodology guide AI-assisted. | 17-tab integrated model (rNPV, sum-of-parts, comps, precedents, football field, S&U, ASC 805 PPA, accretion/dilution, pro forma, synergies, sensitivity, scenarios, error checks) — 751 live formulas, zero errors. Includes a 6-slide IB-style deal book and a 5-page methodology guide — see [`/merck-pandion-ma-model`](./merck-pandion-ma-model). |
| **Trade Advisor** | Personal multi-horizon trade decision-support web app, live on the web. | Yes | 18-agent research workflow (~1.2M tokens) over an 82-source registry; 17-check safety suite; live execution gated behind 8 independent checks, off by default. |
| **equity-advisor** | Python CLI for equity research and recommendations. | Yes | 115 test functions across 31 files; coverage deliberately driven from 79% to 85% before the live-recommendation gate was allowed to activate. |
| **algo-trader-v3** | Systematic trading bot as a five-stage gated pipeline: Hypothesis → Signal R&D → Build → Paper/Incubation → Live. | Yes | 129 tests, 28 architecture decision records; a hook-enforced rule blocks stage advancement unless the upstream gate artifact exists and reads PASS. Kill-scoreboard: 10+ candidate trading edges tested and killed before reaching capital. |
| **Football Predictor** | Soccer match outcome (win/draw/loss) prediction engine. | Yes | 196 tests; RPS 0.2018 on unseen data across 15 leagues / 34,903 matches — genuinely skillful, and the project's own conclusion is that no exploitable edge exists against efficient betting markets. |
| **ETF Investment Simulator** | Offline Monte Carlo investment simulator built for a friend, comparing 36 funds across UK brokers. | Yes | 100,000 simulation paths in a browser Web Worker, no server; built-in warnings against survivorship and recency bias in the underlying assumptions. |

## Live demo

See [`/demo`](./demo) for a working version of the Client Book Dashboard & Deck Builder with synthetic sample data — no real data of any kind. Click "Load Demo Data" to populate it instantly.

**Live version: https://fergusirvine55-gif.github.io/fergus-irvine-agentic-ai-portfolio/demo/**

## Merck & Co / Pandion Therapeutics deal documents

See [`/merck-pandion-ma-model`](./merck-pandion-ma-model) for the full package: [acquisition model workbook](./merck-pandion-ma-model/Merck_Pandion_Acquisition_Model.xlsx), [IB-style deal book](./merck-pandion-ma-model/Deal_Book.pptx), [methodology & user guide](./merck-pandion-ma-model/Methodology_and_User_Guide.pdf), and [license](./merck-pandion-ma-model/README_and_License.pdf). Reconstructed entirely from public information (SEC filings, press releases) — not investment advice, not affiliated with either company.

## What this proves

- Quantitative rigor isn't theoretical — deal mathematics and multi-agent research pipelines are the same discipline applied to different domains.
- Agentic AI fluency here means shipped, tested systems with governance built into the tooling (hooks, gates, kill-scoreboards) — not prompting as a party trick.
- Honest reporting of negative results (Football Predictor) matters as much as positive ones — the value is in the process being trustworthy, not in every project "winning."
- Enterprise relationship experience plus hands-on technical build capability is an uncommon combination: someone who can sit in front of a client and also ship the system underneath the conversation.
