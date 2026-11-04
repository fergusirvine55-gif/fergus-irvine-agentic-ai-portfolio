# How I build with Claude

This page is the setup behind everything else in this repo. I run Claude the way an engineering team runs a platform: an environment layer, a governance layer, a method for agents, and a test discipline that gets a vote. Each section names real files and real numbers so a reader can check it against the projects.

## 1. Environments

Four places, one working style.

The desktop app's Code tab is home. Sessions are filed in sidebar groups per project, forked when a side quest turns up, and split side by side when two of them need watching at once. The CLI covers headless runs and anything scripted. Claude in Chrome takes the browser when the work is a real website: it drives forms end to end, and the quirks of each form engine (Ashby, Greenhouse, Lever, Workable, Teamtailor, Rippling, Comeet) are written down after the first pass so the second pass is faster. Cloud sessions take the overnight research. They start from a pushed branch, read a brief, and leave a pull request, because they never report back.

The fourth place is a Contabo VPS: 12 vCPU, 47 GB of RAM, Ubuntu, with headless Claude Code logged in to my plan. Agent fleets run there rather than on the laptop, for two reasons. A desktop plugin hook once killed subagents mid-run, and a sleeping Mac kills everything. On the VPS a run is launched with setsid and nohup, detached from the SSH call, and followed through its log. The Mac stays master: inputs are pushed with rsync, outputs pulled back, nothing is edited remotely. Remote Control is on for every session that touches the VPS, so a run can be steered from my phone.

Local runs still happen for anything small. The Workflow tool manages about six parallel agents on an eight-core Mac, which is enough for a verification pass or a batch of readers.

## 2. The governance layer

Claude does not get to decide how much of my plan it spends.

A global CLAUDE.md, a rules folder and a set of skills hold the standing orders. One of them is a UserPromptSubmit hook that fires on every prompt and injects the launch-card rule. Before any agent, plan or workflow starts I see three configurations, optimal, economical and faster, each with its own models, effort levels, agent counts, parallelism, phases, where each group runs (local, cloud, VPS or a mix), the share of the five-hour and weekly limits it will use, whether any agent will download files, and a finishing time as a clock time. Every field is chosen fresh for the task. There are no defaults and no rules of thumb carried over from the last run, and a model at risk of its weekly limit stays on the card marked as such instead of being dropped silently. Nothing launches until I type go.

Pre-launch checks run with the card: VPS uptime, how many headless sessions are already running, disk, memory, and the live usage meter read from the app rather than from any cached file. The meter is read again when the run ends and the difference goes in the reply. A forecast that is never checked against the bill is a guess.

The VPS runner, run-wf-strict.sh, refuses to start without a model and an effort level. Permissions are acceptEdits plus an explicit allow-list: read, write, text tools, installs and deletes are in; sudo, apt, ssh and git push are out; a permission bypass is never used. On the Mac the auto-mode classifier adds its own refusals and I keep them. When it declined to merge a pull request without review, the fix was to hand me the commands.

Two more standing rules. Anything aimed at bots ("click here if you are not a computer") is left alone and flagged. And no agent submits a form, sends an email or creates an account; those happen from the main session, with me watching.

## 3. The control map

When the configuration grew past what I could hold in my head, I inventoried it. The control map lists 125 controls across ten layers (CLAUDE.md, rules, hooks, settings, plugins, memory, connectors, skills, sessions, VPS), found 16 conflicts between them, and publishes the lot as a one-screen dashboard. A second inventory covers about 700 plugins, each with a keep-or-defer decision and a note of whether it carries a hook or an MCP server. The plugins that had interfered with agent runs were switched off by setting, with a dated backup of the settings file before each change.

## 4. How agents are run

The shape of a run is the same whether it has three agents or fifty-one.

Finders do the reading and write to disk. An independent verifier re-checks what they claim. A judge, one multi-lens pass rather than a chain of critics, decides. An agent's reply is an acknowledgement; the file on disk is the result, and if the file is missing the agent did nothing. Long agents checkpoint every ten items so a run that hits a limit resumes where it stopped, and the Workflow tool's resume keeps finished agents' results instead of paying for them twice.

Some numbers from recent runs. A 51-agent research run on the VPS for a shipping feasibility study. An 18-agent research workflow over an 82-source registry for Trade Advisor, about 1.2 million tokens. Eight parallel agents, each in its own git worktree, finishing the US half of a market dataset in 25 to 30 minutes apiece. Sixteen reader agents transcribing 486 frames of a screen recording, after a pilot in which the chosen model read 329 of 329 rows exactly and the cheaper one did not. A seven-agent company-research run (44 minutes, 709 tool calls, 2.28 million tokens) whose verifier reported 126 claims: 100 confirmed, 10 corrected, 11 unverified, 5 in conflict. The corrected and unverified ones became a do-not-say list for the meeting.

Briefs are files. A BRIEF.md states the output schema, the paths, what the agent may not do, and the file-save rules the launch card promised. Cloud sessions get a shared brief, a profile file, their own numbered brief and a folder of prior work, because they cannot ask. When a brief and a scoring card disagree, the card wins; cards carry version numbers and a history.

Chains stay lean: combined reviewers, one judge, refute-and-repair in a single pass, no calibration round. The most expensive lesson in the setup was the cost of context. An agent re-reads everything it has seen at every step, so a reader fed one image per message cost about four million tokens per thirty images. Sending ten images in one message and asking for ten transcripts in the next cut that to about 380 thousand. That instruction is now in every reader brief.

## 5. An organisation of agents

A maritime startup concept of mine has a founding organisation made of agent files: six single-voice advisors (a founder coach, a head of engineering, a principal integrations engineer, a cyber and compliance officer, a lead marine UI architect, a chief of staff), each fronting a council, fifteen councils in all. Fan-out goes through a consult-advisor skill from the main session rather than agents calling agents. The repo runs a gated method: numbered documents, architecture decision records, a schema check in CI, and a live-source check that visited 369 sources and found 340 live, 7 unreachable and 0 wrong. No agent keeps its seat until it beats plain Claude on a real maritime case I write myself. Thirty-two agents load; the organisation review recommended five for the first real task and parked the rest until a gate needs them.

## 6. Testing and statistics

A claim without a test is a draft.

The code projects carry suites: 196 tests on the football predictor, 129 on the trading pipeline, 115 across 31 files on the equity tool, and two assertion modules (123 and 37 checks) on the bank dashboards. The trading pipeline goes further. A hook blocks a stage from advancing unless the previous gate's artefact exists on disk and reads PASS, and a kill scoreboard records the ten-plus candidate edges tested and killed before any reached capital. Coverage on the equity tool was pushed from 79 to 85 percent before its live-recommendation gate was allowed to switch on.

Statistics get the same treatment. The football model is scored by ranked probability score on 34,903 matches across 15 leagues (0.2018 on unseen data) and its conclusion is that no exploitable edge exists against the betting market. The ETF simulator runs 100,000 Monte Carlo paths in a browser worker and warns about survivorship and recency bias in its own inputs. A prospecting model for a sales campaign was pre-registered, tested against held-out random controls, re-scored blind, and given a register of twelve measured limitations with impact tests; one of them corrected the model's own alpha from 0.095 to 0.317. The bank dashboards carry paired t-tests, Pearson correlation, trend t-tests, an F-test on volatility and Granger-style lead-lag tests, all reported with Benjamini-Hochberg adjusted p-values, and when the demos were rebuilt every figure was recomputed in Python and matched in the browser to the cent.

Tools get trialled before they get trusted. For reading code out of a video, Apple's Vision OCR scored 91.6 percent of characters and 64 percent of rows exact; an AI reader on the same crops made no misreads in 165 rows across four blind tests, so the reader got the job. For grading 2,867 records against a set of reference cases, a 100-point rubric over bge-small embedding similarity was checked by eight reviewer agents on the near-threshold cases and then by a critic that measured the first pass at about 72 percent precision. The critic's findings became new rules and the run was repeated.

## 7. Building

The bank tools are single HTML files because that is what a bank desktop will open. SheetJS parses the extract in a Web Worker in 50,000-row chunks, the charts are hand-drawn SVG, html2canvas rasterises tiles for export, and an in-house library writes a byte-safe ZIP (CRC32, DEFLATE) to inject slides into whatever PPTX template the user dropped in. A 100,000-row, 70 MB extract parses in about 49 seconds with nothing leaving the browser.

Everything else uses whichever stack fits. Python for data pipelines: public carrier records through the FMCSA Socrata API, SAFER and SMS parsers, pre-scoring. Vite, React, Express and Postgres on Render for the web apps, with a FastAPI sidecar when a web app needs the Python valuation engine. Research dashboards are published as Claude artifacts with a shared database and per-user state: one holds about 3,550 documents and takes approvals from my phone, another keeps notes, flashcards and highlights per viewer. Every dashboard ships in a desktop and an iPhone layout inside one artifact, and carries its version and update time in the title.

Presentation has its own owner. Claude Code owns the analysis and Claude Design owns the page. A design guide of about 185,000 words, with build cards per section and a 99-row hashed cut ledger, governed a client pack that was cut from 41,000 words to a 16-minute read under budget gates and a cold-reader test. A validator runs more than eighty checks over dashboard copy, one of them a scrub for person, vendor and tool names.

## 8. Connectors, APIs and tools

Gmail, Google Calendar, Google Drive and Chrome through MCP. The GitHub CLI for everything git-hosted. Public company APIs for refreshing a 2,867-row research database. The FMCSA catalogue on data.transportation.gov (138 datasets) and SEC EDGAR for primary records. Whisper for transcribing podcast episodes locally. sentence-transformers in a pinned venv (torch 2.2.2, because newer wheels do not ship for an Intel Mac). A Swift Vision tool for frame extraction. JavaScriptCore for syntax-checking every script block in a 7,000-line HTML file. Scheduled tasks for a twice-daily inbox sweep into a tracking dashboard.

## 9. GitHub practice

One branch per task, created with an explicit base, so a shared checkout left on somebody else's branch cannot leak into mine. Draft pull requests, stacked when they depend on each other, with the merge order written in the description. Decision ids and semantic version tags on the plan repositories; one went from v0.4.0 to v0.5.0 across thirteen pull requests in a week. Every project carries HANDOVER.md, STATE.md and RUN-LOG.md so a fresh session, or a fresh person, starts from the file and not from memory. Architecture decision records wherever a choice was made, 28 of them on the trading pipeline. Clones live outside iCloud, which corrupts git indexes. Original source files that held real data stay in a folder that is never published, and anything that goes public is scanned first, down to the contents of the spreadsheets, for the bank's name, old passwords and real names.

## 10. Terminal

zsh, with SSH aliases for the VPS. Launches detach with setsid and nohup and redirect all three streams, because without the redirects the SSH call hangs. Process counts use anchored patterns, after a loose pkill once killed the remote shell. Untrusted downloads are read with python3 -I from a separate directory so a planted module cannot be imported. Timestamps come from date, after a log once ran an hour fast. Scratch files live in a per-session scratchpad that gets purged, so anything worth keeping is copied into the project before the session ends.

## 11. Prompting and writing

I write briefs the way I would write a work order for a contractor who cannot phone me: output schema first, then paths, then the rules, then the context. The verifier's output becomes three lists, safe, caution and do not say, that feed the next brief. Every outward text, from a client letter to this page, goes through a pass that flags the patterns of machine prose, quotes each one, rewrites, and audits the rewrite. Plans and frameworks ship as one main document; research and review reports stay on file. Memory is a folder of small files with front matter and an index, one fact per file, and each feedback note carries why it exists and how to apply it, so the next session inherits the correction instead of repeating the mistake.

## 12. Scorecards

The launch card before a run. The usage card after it, with the before and after readings. The kill scoreboard on the trading pipeline. The fact-check card: confirmed, corrected, unverified, in conflict. The live-source card: found, unreachable, wrong. The pilot card that picks a model for a job on a scored sample before the job starts. The consistency check that re-runs a model's own tests after every change (46 of 48 passed, zero defects, on the last run) and the history check that confirms none of 91 recorded corrections has quietly reverted (89 hold, none undone).

## What this adds up to

A commercial operator who runs Claude like infrastructure: observable, governed, tested, and cheap enough to use every day.
