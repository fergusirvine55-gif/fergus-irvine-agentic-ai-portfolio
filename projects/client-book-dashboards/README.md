# Client Book dashboards

Four single-file browser dashboards for a securities-finance client book at a global bank, plus the launch pad that holds them. One master build and three production releases deployed across the bank's global footprint. Everything in this folder runs on synthetic data: open any file, press Load Demo Data, and every institution, client, relationship manager and amount you see is fictional.

Nothing to install, no server, no network call, no admin rights. Each file opens on a locked-down bank desktop and does every byte of the work inside the browser: parsing the monthly extract, drawing the charts, running the statistics, and exporting the deck as PDF, as standalone PPTX, or as slides injected into the user's own PPTX template. That is why the family reaches any desk in the bank without an IT ticket.

| Dashboard | What it does | Deployment | Build | Open |
|---|---|---|---|---|
| Client Book Dashboard & Deck Builder (master) | Exposure monitoring, peer benchmarking with significance tests, a guided explore surface, deck production | The master build; the three releases below are cut from it | v41 | [client-book-deck-builder-v41.html](client-book-deck-builder-v41.html) |
| Client-facing release | Exposure monitoring and branded deck export for client meetings | Global | build 32 | [live demo](https://fergusirvine55-gif.github.io/fergus-irvine-agentic-ai-portfolio/demo/) |
| EMEA Aged Receivables Dashboard | Aged receivables by relationship manager and age bucket, unbilled revenue, the monthly deck, a fee-schedule tracker | Global | v1 | [emea-aged-receivables.html](emea-aged-receivables.html) |
| No-install exposure explorer | Drop a CSV, rank and filter lenders and borrowers, read the book | Global, kept as the fallback where the full build is not an option | 1 | [lender-borrower.html](lender-borrower.html) |
| Launch pad | All four in one file, each opening in its own tab | | | [dashboards-hub.html](dashboards-hub.html) |

Open any dashboard by downloading the file and opening it in a browser, or through the site links above.

## What it proves

Three things. I know the buyer's world from the inside: counterparty exposure, client reporting cycles, and desktop estates that allow nothing to be installed. I ship analytics products with real statistics in them, and this one went through 41 builds on the way. And I build the deployment artefact myself, around the constraints the client has, rather than describing one for somebody else to build.

## 1. Client Book Dashboard & Deck Builder, master build v41

The master build and the source of every other dashboard in the family. One HTML file of about 7,000 lines with no external dependency. It gives one surface for four jobs.

Monitor. Bilateral securities-financing exposure between collateral providers and receivers at counterparty, market, product, instrument, region, legal-entity and reuse (rehypothecation) granularity. A KPI strip, Top-N charts for counterparties and markets, balance over time with layer-by and split-by, pivot and summary tables with month-on-month and year-on-year tinting, and status cohorts: has a balance, had one but holds zero now, never had one.

Benchmark. A client against similar entities, a chosen peer group and the rest of the book. Up to 13 similarity factors, each scored 0 to 100 and blended into a weighted score. Balance size is compared on a log scale, so $2bn against $1bn is close and $2bn against $20m is not. Mix factors measure distribution overlap by instrument, security type, market, product, region, legal entity and reuse; behaviour factors cover 12-month growth, the volatility of monthly changes and co-movement. Bars show what each factor contributed, and overweight and underweight labels carry explicit thresholds.

Explain. Five analyst questions, each with its own tile set: what drove the change, who has or has held it, what moves with it, does anything lead it, and how stable is the trend. Every answer carries a confidence chip.

Produce. Any set of live tiles becomes a branded deck. Up to twenty pages, portrait or landscape, quad layouts with resizable splitters, drag-and-drop tiles that can be duplicated and relabelled, and page geometry read from a dropped .pptx or .pdf template. Export is PDF, standalone PPTX, or slides injected into the user's own template by an in-house merge library that writes a byte-safe ZIP (CRC32, DEFLATE) and preserves slide ids, relationship ids, media numbering and namespace prefixes.

### Statistics, run on every data load

| Method | Where it is used | What it assumes |
|---|---|---|
| Paired t-test on monthly growth gaps between the client and the comparison group | Peers & Benchmark confidence chips | Paired differences close to normal, or enough months; months treated as independent, so autocorrelation can flatter significance |
| Pearson correlation of monthly percentage changes | Explore, "what moves with it" | A linear association between changes, sensitive to outliers |
| Linear-trend t-test on each series | Trend and stability | A linear trend inside the window, independent residuals |
| Up-month against down-month sensitivity | Behaviour factors | Enough months of each sign |
| F-test on volatility | Behaviour factors | Normal monthly changes; the F-test is sensitive to departures |
| Granger-style lead-lag test | Explore, "does anything lead it" | Stationary series and a chosen lag; a lead is precedence, not cause |
| Benjamini-Hochberg false-discovery adjustment | Every inferential result | Controls the expected false-discovery rate across the family of tests shown; chips read strong, moderate, weak or none |
| Herfindahl-Hirschman index, top-N and top-5 share | Concentration | Shares of balance within the chosen dimension |
| Month-on-month and year-on-year change, with a first-month baseline when fewer than 13 months are loaded | Change metrics | The baseline rule is labelled in the UI |
| z-score of monthly change, flags at two standard deviations | Unusual months, deep-linked to the drivers view | Monthly changes close to normal inside the window |
| Share of variance explained per contributor, plus correlation with the total change | Driver attribution | Additive contributions; overlapping drivers share credit |

Tests re-run whenever data is loaded and on demand from a Re-run analysis button. The client-facing release carries the descriptive set only.

### Engineering

SheetJS parses .xlsx, .xls and .csv off the main thread in a Web Worker, in 50,000-row chunks, with the column schema detected on load and market names normalised. Twelve chart and table types are drawn as hand-rolled SVG with no charting library, so the file stays self-contained and prints cleanly. html2canvas rasterises tiles for export. Per-user profiles persist every filter, tile, selection, layout and annotation, with undo and redo. A data-stamp strip shows rows, month range and bad months, and opens a per-month row-count audit that catches duplicated or malformed months. A 100,000-row, 70 MB extract parses in about 49 seconds. Internal field names stay as the feed sends them while the interface labels them Receiver and Provider, the convention in securities financing.

Build 32 was the first production client-facing release. Builds 38 and 39 added and then refactored the benchmarking and explore tabs. Build 41 added independent tile clones, editable labels and a filter panel on every tab.

Demo data: 1,100 rows over 24 months, built in.

## 2. Client-facing release, build 32

The branded, client-ready release of the master, deployed globally, and the version counterparty decks come from. Same monitoring surface, same deck builder, with the inferential statistics held back for the client-facing cut. Two assertion modules (123 and 37 checks) back it. Sanitised, it is the live demo of this repo: open it, press Load Demo Data, tick some tiles, build a deck.

## 3. EMEA Aged Receivables Dashboard, v1

The same build pattern pointed at a second problem: aged receivables, which is billing and collections, across EMEA, with the monthly deck produced through the same export pipeline. Deployed globally. It shows aged balances by relationship manager and age bucket, unbilled revenue, a monthly deck with a history chart, a fee-schedule tracker slide that lists what is new, changed, carried and done each month, and a relationship-manager directory. Excel and PowerPoint export. Update data loads the month's source files through the dashboard's own parsers.

The demo was built from twelve synthetic source files in [data/aged-receivables](data/aged-receivables/): eight monthly unpaid-invoice extracts, a BI export, a scope workbook and two months of the fee-schedule tracker. They were run through the dashboard's own parsers and checked against an independent Python recomputation. The aged total, nine buckets, eight relationship managers, unbilled past due, eight history points and the tracker's new, changed, carried and done counts all match to the cent.

## 4. No-install exposure explorer

The lightweight, portable member of the family and the earliest build: a CSV-based lender and borrower exposure explorer that any desktop can open, deployed globally and kept as the fallback where the full build is not an option. Drop a CSV, read the KPIs, rank lenders and borrowers, filter, search, reset. The demo CSV of 2,400 rows is in [data/lender-borrower](data/lender-borrower/), and every KPI and ranking was checked against a Python recomputation.

## Checks before publication

Every figure in the demos was recomputed independently in Python and matched in the browser: KPIs, rankings, filters, age buckets, relationship-manager totals, the history chart and the tracker changes. Excel and PowerPoint exports were run with no console errors. Every file, including the spreadsheet contents and the launch pad's embedded payloads, was scanned for the bank's name, old passwords and real names before it was committed.

## Files

| File | Contents |
|---|---|
| [dashboards-hub.html](dashboards-hub.html) | Launch pad holding all four dashboards |
| [client-book-deck-builder-v41.html](client-book-deck-builder-v41.html) | Master build v41 |
| [../../demo/](../../demo/) | Client-facing release, build 32 (the live demo) |
| [emea-aged-receivables.html](emea-aged-receivables.html) | EMEA Aged Receivables Dashboard v1 |
| [lender-borrower.html](lender-borrower.html) | No-install exposure explorer |
| [data/](data/) | Synthetic source files for the receivables dashboard and the explorer |
