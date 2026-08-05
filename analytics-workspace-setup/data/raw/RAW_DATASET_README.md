# SellerSignal — Raw (Messy) Dataset for Data Cleaning Practice

The `raw_*.csv` files are deliberately dirty versions of your original clean
dataset (`sellers.csv`, `orders.csv`, `returns.csv`, `reviews.csv`). Every
issue below was injected on purpose, seeded (`random_state`) so it's
reproducible — nothing is solved for you, this is the input, not the answer.

**Do not use `seller_monthly_metrics.csv` as a shortcut** — it's already
aggregated from the clean source and will hide most of what you're supposed
to practice cleaning. Work from the four `raw_*.csv` files.

## What's in each lesson

**Dataset Profiling (2.16)** — run `.info()`, `.isnull().sum()`,
`.duplicated().sum()`, `.describe()` on all four raw files before touching
anything. Note null counts, dtype mismatches, and row counts vs. the clean
originals (66 vs 60 sellers, 43,185 vs 43,125 orders, etc. — the gap is your
injected duplicates).

**Data Dictionary (2.17)** — `data_dictionary.csv` gives you the *expected*
type and business meaning for every column, plus notes on what's been messed
with. Use it as your reference, not as something to hand in as-is — your
mentor likely wants you to produce your own version reflecting what you
actually find.

**Missing Values (2.18)** — nulls injected in: `sellers.region` (~10%),
`orders.customer_id` (~1.5%), `returns.return_reason` (~4%),
`reviews.review_text` and `reviews.review_date` (~1–2%). Decide per column:
drop, impute (mode/median/"Unknown"), or leave-and-flag — and justify why
based on what the column means.

**Data Type Enforcement (2.19)** — `orders.order_value` is a mix of plain
floats and `"$1,234.56"` strings; a few rows are negative. `reviews.rating`
is a mix of `5`, `"5 stars"`, `"5/5"`, `"5.0"`. `orders.order_date` and
`sellers.join_date` mix `YYYY-MM-DD`, `MM/DD/YYYY`, and `DD-Mon-YYYY`. All
need parsing to proper numeric/date dtypes before anything downstream works.

**Duplicate Detection (2.20)** — exact duplicate rows injected in all four
tables. `sellers` also has **near-duplicates**: same seller, different name
formatting (trailing whitespace, punctuation stripped, appended `_DUP` on
`seller_id`) — these won't be caught by `.duplicated()` alone and need a
fuzzy/normalized-name match.

**String Cleaning (2.21)** — `sellers.category` and `returns.return_status`
have inconsistent casing, stray whitespace, and label variants (e.g.
`"Completed"` / `"COMPLETED"` / `" complete"`). Normalize before any
`.groupby()` — as-is, these will silently split into extra fake categories.

**Date/Time Transformation (2.22)** — once `order_date` and `join_date` are
parsed to real dates (see 2.19), extract whatever features your pipeline
needs (day of week, seller tenure at time of order, etc.).

**Outlier Detection (this lesson)** — three separate outlier situations, each
suited to a different handling strategy:
- `orders.order_value`: ~25 rows are genuine extreme-but-valid high-value
  orders ($1,500–$4,500 vs. a normal range of roughly $10–$150) → **cap**
  candidates.
- `orders.quantity`: 8–9 bulk orders of 150–500 units vs. normal 1–4 →
  decide cap vs. flag depending on whether bulk orders are legitimate
  business or noise.
- `orders.order_value` negatives (12 rows) and `returns.refund_amount`
  negatives (5 rows) or refunds exceeding the original order value (10
  rows) → these are **invalid**, not just extreme — remove candidates, not
  cap candidates. Compute Z-score and IQR bounds on the cleaned numeric
  column and compare which method flags which rows.
- `reviews.sentiment_score` has 15 rows outside the valid [-1, 1] range
  (5.0, -8.1, etc.) → clear pipeline-glitch outliers, remove or clip to
  valid range.

Build a cleaning log (column, method, action, count, reasoning) as you go —
that's the actual deliverable this lesson is asking for, not just clean data.

**Correlation & Relationship Analysis (this lesson)** — use the *cleaned*
`seller_monthly_metrics.csv` (after you've rebuilt it from your cleaned raw
tables, or the existing aggregated version) for this part — correlation
needs numeric, aggregated data, not raw transaction rows.

- `avg_return_rate` vs `avg_rating` vs `avg_sentiment_score`: rating and
  sentiment correlate at r ≈ 0.96 — nearly redundant, good example for
  feature selection (keep the more interpretable one).
- **The trap:** `avg_response_time_hours` (new column) correlates with
  `return_rate` at **r ≈ 0.87** — strong enough that it's tempting to
  conclude "slow seller responses cause returns." Check what it correlates
  with `total_orders` (it doesn't, r ≈ 0.04) before concluding anything.
  The real story: both `avg_response_time_hours` and `return_rate` are
  symptoms of the same underlying thing — a seller's operational quality
  declining in a given month — not one causing the other. This is the
  `number_of_support_tickets` trap from the lesson, rebuilt into this
  dataset on purpose.

Compute both Pearson and Spearman on the numeric columns, plot the heatmap,
and write down — in words — which of the three causal directions (A→B, B→A,
confound) is most plausible for the response-time/return-rate pair, and why.
