# Client Book dashboards

Four single-file browser dashboards for a securities-finance client book, plus the launch pad that holds them. Each opens empty; press **Load Demo Data** to load a synthetic book. Every institution, client, RM and amount in this folder is fictional.

| File | What it does | Demo data |
|---|---|---|
| [`dashboards-hub.html`](dashboards-hub.html) | Launch pad: all four dashboards in one file, each opened in its own tab | — |
| [`client-book-deck-builder-v41.html`](client-book-deck-builder-v41.html) | Master build: provider and receiver exposure, peer benchmarking with significance tests, guided explore, deck export to PDF / PPTX / your own template | 1,100 rows, 24 months, built in |
| [`../../demo/`](../../demo/) | Client-facing release (build 32): exposure monitoring and branded deck export | same rows, built in |
| [`emea-aged-receivables.html`](emea-aged-receivables.html) | Aged receivables by RM and age bucket, unbilled revenue, monthly deck with history chart, fee-schedule tracker slide, RM directory; Excel and PowerPoint export | built in; the source files are in [`data/aged-receivables/`](data/aged-receivables/) and can be loaded through **Update data** |
| [`lender-borrower.html`](lender-borrower.html) | No-install exposure explorer: drop a CSV, filter lenders and borrowers | built in; CSV in [`data/lender-borrower/`](data/lender-borrower/) |

To open a dashboard, download the HTML file and open it in a browser. No install, no server, no network calls.
