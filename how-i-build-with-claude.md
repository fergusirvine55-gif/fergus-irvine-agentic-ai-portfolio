# How I build with Claude

The setup behind this repo: environments, a governance layer, a method for agents, and tests that get a vote. Real files, real numbers.

## 1. Environments

- Desktop app, Code tab: sessions filed in groups per project, forked for side quests, split side by side when two need watching.
- CLI for headless and scripted runs.
- Claude in Chrome for real websites. Each form engine's quirks (Ashby, Greenhouse, Lever, Workable, Teamtailor, Rippling, Comeet) are written down after the first pass.
- Cloud sessions for overnight research: start from a pushed branch, read a brief, leave a pull request. They never report back.
- Contabo VPS (12 vCPU, 47 GB, Ubuntu) running headless Claude Code for agent fleets. Launched with setsid and nohup, followed by log. Mac is master: rsync in, rsync out, nothing edited remotely. Remote Control on, so a run is steerable from a phone.
- Local Workflow runs cap at about six parallel agents on an eight-core Mac.

## 2. Governance

- CLAUDE.md, a rules folder and skills hold the standing orders.
- A UserPromptSubmit hook injects the launch-card rule on every prompt. Before any agent run: three configurations (optimal, economical, faster), each with models, effort, agent count, parallelism, phases, where each group runs, share of the five-hour and weekly limits, any file downloads, and a finishing time. No defaults carried over; a model near its limit stays on the card, marked. Nothing launches until I type go.
- Pre-launch checks: VPS load, running sessions, disk, memory, the live usage meter. Meter read again after the run; the difference goes in the reply.
- run-wf-strict.sh refuses to start without a model and an effort level. acceptEdits plus an allow-list: installs and deletes in; sudo, apt, ssh and git push out; never a permission bypass.
- The app's auto-mode classifier refuses some actions. I keep its refusals and take the commands myself.
- Bot bait is left alone and flagged. No agent submits a form, sends mail or creates an account.

## 3. Control map

- 125 controls across ten layers (CLAUDE.md, rules, hooks, settings, plugins, memory, connectors, skills, sessions, VPS) inventoried; 16 conflicts found; published as a one-screen dashboard.
- About 700 plugins inventoried with a keep-or-defer decision and hook and MCP flags. The ones that broke agent runs are off by setting, with a dated backup of the settings file.

## 4. Running agents

- Finders write to disk; an independent verifier re-checks; one judge decides. A reply is an acknowledgement; the file is the result.
- Long agents checkpoint every ten items. Workflow resume reuses finished agents.
- Recent runs: 51 agents on the VPS for a shipping feasibility study. 18 agents over 82 sources, about 1.2M tokens. 8 agents in git worktrees, 25 to 30 minutes each. 16 readers over 486 video frames, after a pilot in which the chosen model read 329 of 329 rows exactly. 7 agents, 44 minutes, 709 tool calls, 2.28M tokens; the verifier reported 126 claims: 100 confirmed, 10 corrected, 11 unverified, 5 in conflict.
- Briefs are files: output schema, paths, what the agent may not do, the file-save rules the card promised. Cloud briefs carry everything, because a cloud session cannot ask. Scoring cards carry version numbers; when a prompt and the card disagree, the card wins.
- Lean chains: combined reviewers, one judge, refute-and-repair in one pass, no calibration round.
- Context is the cost. One image per message cost about 4M tokens per 30 images; ten images per message cut it to about 380k. That line is now in every reader brief.

## 5. An organisation of agents

- A maritime startup concept has six single-voice advisors (founder coach, head of engineering, principal integrations engineer, cyber and compliance officer, marine UI architect, chief of staff), each fronting a council; fifteen councils, all agent files. Fan-out goes through a consult-advisor skill, never agents calling agents.
- Gated method: numbered documents, architecture decision records, a schema check in CI, a live-source check (369 sources: 340 live, 7 unreachable, 0 wrong).
- No agent keeps its seat until it beats plain Claude on a real maritime case I write. 32 load; the review recommended 5 for the first task and parked the rest.

## 6. Tests and statistics

- Suites: 196 tests (football), 129 (trading), 115 in 31 files (equity), 123 and 37 assertions (bank dashboards).
- Trading pipeline: a hook blocks a stage until the previous gate's artefact reads PASS; a kill scoreboard records 10+ edges killed before capital. Equity coverage pushed from 79 to 85 percent before the live gate opened.
- Football: ranked probability score 0.2018 on 34,903 matches across 15 leagues; conclusion, no edge against the market. ETF simulator: 100,000 Monte Carlo paths with survivorship and recency warnings in its own inputs.
- Prospecting model: pre-registered, held-out random controls, blind re-score, twelve measured limitations; one corrected the alpha from 0.095 to 0.317.
- Bank dashboards: paired t, Pearson, trend t, F and Granger-style tests, Benjamini-Hochberg adjusted. Demo figures matched to a Python recomputation to the cent.
- Tools trialled first: Vision OCR read 91.6% of characters and 64% of rows; an AI reader made 0 misreads in 165 rows, so it got the job. Grading 2,867 records: a 100-point rubric over bge-small similarity, 8 reviewer agents on near-threshold cases, a critic that measured about 72% precision; its findings became rules and the run was repeated.

## 7. Building

- Bank tools are single HTML files because that is what a bank desktop opens. SheetJS in a Web Worker, hand-drawn SVG, html2canvas, an in-house PPTX ZIP writer. 100k rows, 70 MB, about 49 seconds, nothing leaves the browser.
- Python pipelines: FMCSA records through the Socrata API, SAFER and SMS parsers, pre-scoring.
- Web apps: Vite, React, Express and Postgres on Render; a FastAPI sidecar when a web app needs the Python valuation engine.
- Claude artifacts with a shared database and per-user state: one holds about 3,550 documents and takes approvals from a phone; another keeps notes, flashcards and highlights per viewer. Desktop and iPhone layouts in one artifact; version and update time in the title.
- Claude Code owns analysis, Claude Design owns the page. A 185,000-word design guide with build cards and a 99-row hashed cut ledger took a client pack from 41,000 words to a 16-minute read under budget gates and a cold-reader test. A validator runs 80-plus checks over dashboard copy.

## 8. Connectors and tools

Gmail, Calendar, Drive and Chrome over MCP. The GitHub CLI. Public company APIs to refresh a 2,867-row research database. The FMCSA catalogue on data.transportation.gov (138 datasets) and SEC EDGAR. Whisper for local transcription. sentence-transformers in a pinned venv (torch 2.2.2; newer wheels skip Intel Macs). A Swift Vision tool for frame extraction. JavaScriptCore to syntax-check every script block in a 7,000-line HTML file. Scheduled tasks for a twice-daily inbox sweep.

## 9. GitHub

- One branch per task, created with an explicit base, so a shared checkout left on someone else's branch cannot leak into mine.
- Draft pull requests, stacked when they depend on each other, merge order in the description.
- Decision ids and version tags on plan repositories: one went v0.4.0 to v0.5.0 across thirteen pull requests in a week. 28 ADRs on the trading pipeline.
- HANDOVER.md, STATE.md and RUN-LOG.md in every project, so a fresh session starts from the file.
- Clones outside iCloud, which corrupts git indexes. Originals holding real data stay in a folder that is never published; public files are scanned first, down to spreadsheet contents.

## 10. Terminal

zsh with SSH aliases. Launches detach with setsid and nohup and redirect all three streams, or the SSH call hangs. Process counts use anchored patterns, after a loose pkill once killed the remote shell. Untrusted downloads are read with python3 -I from a separate directory. Timestamps come from date, after a log once ran an hour fast. Scratch files live in a per-session scratchpad that gets purged, so anything worth keeping is copied into the project first.

## 11. Briefs and writing

Output schema first, then paths, then rules, then context. Verifier output becomes three lists, safe, caution and do not say, that feed the next brief. Every outward text, this page included, gets a pass that flags machine-prose patterns, quotes each one, rewrites and audits the rewrite. Plans ship as one document; research stays on file. Memory is one fact per file with front matter, an index, and a why and how-to-apply on every correction.

## 12. Scorecards

Launch card before a run. Usage card after it, before and after readings. Kill scoreboard on the trading pipeline. Fact-check card: confirmed, corrected, unverified, in conflict. Live-source card: found, unreachable, wrong. Pilot card that picks a model on a scored sample before the job starts. Consistency check that re-runs a model's own tests after every change (46 of 48 passed, zero defects, last run). History check that confirms none of 91 recorded corrections has reverted (89 hold, none undone).

Claude run like infrastructure: observable, governed, tested, and cheap enough to use every day.
