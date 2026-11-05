# Client Book dashboards

Four single-file browser dashboards for a securities-finance client book at a global bank, plus the launch pad that holds them. One master build; three releases deployed across the bank's global footprint, in monthly use by dozens of relationship managers and client-service staff over a book of hundreds of counterparties. Everything in this folder is synthetic: open a file and press Load Demo Data.

No install, no server, no network call, no admin rights. Parsing, charts, statistics and PDF or PPTX export all run inside the browser, which is why the family reaches any desk without an IT ticket.

| Dashboard | Does | Deployment | Build | Open |
|---|---|---|---|---|
| Client Book Deck Builder | Exposure monitoring, peer benchmark with significance tests, explore surface, deck production | Master; the three below are cut from it | v41 | [client-book-deck-builder-v41.html](client-book-deck-builder-v41.html) |
| Client Exposure Dashboard | Monitoring and branded deck export for client meetings | Global | 32 | [live demo](https://fergusirvine55-gif.github.io/fergus-irvine-agentic-ai-portfolio/demo/) |
| EMEA Aged Receivables Dashboard | Receivables by relationship manager and age bucket, unbilled revenue, monthly deck, fee-schedule tracker | Global | v1 | [emea-aged-receivables.html](emea-aged-receivables.html) |
| No-install Exposure Explorer | CSV in; lenders and borrowers ranked and filtered | Global, fallback | 1 | [lender-borrower.html](lender-borrower.html) |
| Launch pad | All four in one file, each in its own tab | | | [dashboards-hub.html](dashboards-hub.html) |

Download a file and open it in a browser, or use the site links. Synthetic source data is in [data/](data/).

## 1. Client Book Deck Builder, master v41

One HTML file, about 7,000 lines, zero dependencies. Four jobs on one surface:

- Monitor: provider and receiver exposure by counterparty, market, product, instrument, region, legal entity and reuse. KPI strip, Top-N charts, balance over time, pivot tables with month-on-month and year-on-year tinting, status cohorts (has, had but zero now, never had).
- Benchmark: a client against similar entities, a chosen peer group and the book. Up to 13 factors scored 0 to 100 and blended; size on a log scale; mix as distribution overlap; 12-month growth, volatility, co-movement; overweight and underweight labels with explicit thresholds.
- Explain: five questions, each with its own tiles: what drove the change, who has or has held it, what moves with it, does anything lead it, trend and stability. Confidence chip on every answer.
- Produce: tiles become a deck. Up to 20 pages, quad layouts, drag-and-drop tiles, page geometry read from a dropped .pptx or .pdf. Export PDF, PPTX, or slides injected into the user's own template by an in-house ZIP writer (CRC32, DEFLATE) that preserves slide ids, relationship ids and media numbering.

### Statistics, re-run on every data load

| Method | Used in | Assumes |
|---|---|---|
| Paired t-test, client vs peer growth gaps | Peers & Benchmark | Near-normal paired differences; months treated as independent |
| Pearson on monthly % changes | What moves with it | Linear association; outlier-sensitive |
| Linear-trend t-test | Trend and stability | Linear trend, independent residuals |
| Up-month vs down-month sensitivity | Behaviour factors | Enough months of each sign |
| F-test on volatility | Behaviour factors | Normal monthly changes |
| Granger-style lead-lag | Does anything lead it | Stationary series, chosen lag; precedence, not cause |
| Benjamini-Hochberg adjustment | All of the above | Controls the false-discovery rate across the tests shown; chips strong, moderate, weak, none |
| HHI, top-N and top-5 share | Concentration | Shares within the chosen dimension |
| MoM and YoY, 12-month baseline (first month when fewer, labelled) | Change metrics | |
| z-score of monthly change, flags at 2σ | Unusual months | Near-normal changes in the window |
| Share of variance per contributor, plus correlation with the total | Driver attribution | Additive contributions |

The client-facing release carries the descriptive set only.

### Engineering

- SheetJS parses .xlsx, .xls and .csv in a Web Worker, 50,000 rows a chunk; schema detected on load; market names normalised.
- Twelve chart and table types in hand-rolled SVG; html2canvas for export; print-safe; aria labels on controls.
- Per-user profiles persist every filter, tile, selection, layout and annotation; undo and redo.
- Data-stamp strip with a per-month row-count audit that catches duplicated or malformed months.
- 100,000 rows, 70 MB, in about 49 seconds.
- Builds: 32 first client-facing release; 38 and 39 benchmarking and explore; 41 tile clones, editable labels, a filter panel on every tab.

Demo data: 1,100 rows over 24 months, built in.

## 2. Client Exposure Dashboard, build 32

The client-facing release of the master, deployed globally. Same monitoring surface and deck builder; the inferential statistics are held back. 123- and 37-assertion test modules. Dozens of relationship managers and client-service staff across every region use it each month to turn the extract into client decks, in place of pivots and slides built by hand. Sanitised, it is this repo's live demo.

## 3. EMEA Aged Receivables Dashboard, v1

The same pattern pointed at billing and collections across EMEA, deployed globally; finance, billing and collections staff and the relationship managers use it every month. Aged balances by relationship manager and bucket, unbilled revenue, a monthly deck with a history chart, a fee-schedule tracker (new, changed, carried, done) and a relationship-manager directory. Excel and PPTX export; Update data loads the month's files through its own parsers.

Demo: 12 synthetic source files in [data/aged-receivables](data/aged-receivables/) (eight monthly extracts, a BI export, a scope workbook, two tracker months), run through the parsers and matched to a Python recomputation to the cent.

## 4. No-install Exposure Explorer

The earliest and lightest build, 490 KB. CSV in; KPIs, lender and borrower rankings, filter, search, reset. Deployed globally as the fallback. Demo CSV of 2,400 rows in [data/lender-borrower](data/lender-borrower/), checked against Python.

## Checks before publication

- Every demo figure recomputed in Python and matched in the browser: KPIs, rankings, filters, age buckets, relationship-manager totals, history chart, tracker changes.
- Excel and PPTX exports run; no console errors.
- Every file, spreadsheet contents and embedded payloads included, scanned for the bank's name, old passwords and real names.
