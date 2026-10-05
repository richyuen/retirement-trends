# Gap-fill C: leakage and stay-in-plan gaps (task gapC, 2026-10-05)

What this pass closed in `notes/stay_in_plan_leakage.md`, `output/irs_early_distribution_penalty.csv`, `output/irs_form5329_part1.csv` and `raw/stayinplan/build_penalty_series.py`. Full citations are in `stay_in_plan_leakage.md` (search for "gapC"). New raw files: `raw/stayinplan/96in33ar.xls`, `97in33.xls`, `98in33ar.xls`-`01in33ar.xls`; `raw/gapC/` (FRTIB 2015-2019 behavior report, two TIGTA reports).

## 1. TY2023 Form 5329 Part I anomaly: diagnosed, not fixable

### Takeaway
The $133.0B (line 1) and $110.8B (line 2) are exactly what SOI printed ([Pub 4801 Rev. 6-2026, pp.131-132](https://www.irs.gov/pub/irs-pdf/p4801.pdf)). Units are thousands, and lines 3 and 4 reconcile. The 2023 instructions added no new exception code. No aggregate (gross IRA or pension distributions, Table 3.3 penalty tax) moves with it. The average excepted amount per excepting return goes from $15.2K to $146.9K (Computed). Most likely a heavily weighted sample outlier or a data-capture error. Lines 1-2 for TY2023 stay excluded; lines 3-4 are fine.

### Cited findings
- Re-extraction, reconciliation and the instruction comparison ([i5329 2023](https://www.irs.gov/pub/irs-prior/i5329--2023.pdf) vs [2022](https://www.irs.gov/pub/irs-prior/i5329--2022.pdf)) are in `stay_in_plan_leakage.md` §1.
- The Table 3.3 file `23in33ar.xls` does not carry Form 5329 lines; the anomaly is only in Pub 4801.

### Evidence verdict
Cause documented. It is an SOI estimate problem, not ours. TY2024 (not released; `24in33ar.xls` returns 404) will show whether it persists.

### Gaps
SOI has published no errata, and no coefficient of variation is given for the line.

## 2. CARES coronavirus-related distributions (Form 8915-E)

### Takeaway
No IRS, SOI, Treasury or TIGTA tabulation of Form 8915-E counts or amounts exists. I checked Pub 4801 TY2020/21, Pub 1304 TY2020/21, the SOI CARES page (which covers only Economic Impact Payments) and TIGTA 2021-16-044 (via oversight.gov), which itself relies on Fidelity, Vanguard and TSP figures. CRDs therefore can't be expressed as a share of returns or of IRA/pension distributions from government tables. The usable government figures remain TSP (2.8% of participants) and Derby et al. (JCT, IRS sample). New: TIGTA 2024-100-065 (TY2021) shows 6.2M taxpayers with code-1-type early distributions, half of whom (3.1M, Computed 50%) neither paid the 10% tax nor filed Form 5329. The SOI penalty series therefore understates early-withdrawal incidence.

### Evidence verdict
CARES effect remains strong (SOI penalty drop plus JCT). A CRD share from IRS data is not available.

### Gaps
GAO-24-103577's "6 percent took a CRD" is still unverified (files.gao.gov returns 403).

## 3. Penalty series extended to TY1996

### Takeaway
The earlier note was wrong that TY1996-2001 tables lack the column; it sits in a lower panel. The series now runs 1996-2023. Returns paying the tax: 2.85% (1996) → 3.51% (2001) → 3.76% (2002). Tax per $100 of taxable IRA and pension distributions was 0.74-0.80 in 1996-2002. Around the 2005 EGTRRA auto-rollover rule: 3.72% / 3.59% / 3.72% (2004/05/06), no break. Form 5329 Part I is extended back to TY2003 (lines 3-4) and TY2009 (all lines). The excepted share of dollars rose from 24% (2009) to 35-40% (2017-22).

### Evidence verdict
EGTRRA 2005: no visible aggregate effect, which is expected given the small balances involved. Weak evidence either way.

### Gaps
Nothing before TY1996 is online at irs.gov. A TPC snippet ("2.3 percent in 1993") is unverified.

## 4. Auto-portability after Oct 2025

### Takeaway
The DOL final rule (RIN 1210-AC21) has been at OIRA since 14 Sep 2026, "Pending Review" ([reginfo.gov](https://www.reginfo.gov/public/do/eoReviewSearch?rin=1210-AC21)); it is not in the Federal Register as of 5 Oct 2026. PSN reports over 42,000 completed transfers by 24 Jul 2026 [industry], up from 16,700 in Oct 2025. Computed: 12.4% of DOL's one-year baseline; the run-rate is about 10% of the projected annual flow. Vanguard: 7% of its plans had adopted by YE2025.

### Evidence verdict
Still weak. Volume is growing but there is no independent cash-out evaluation.

## 5. Hardship withdrawals and loans: government series (TSP)

### Takeaway
FRTIB administrative data give an annual series for FERS participants, 2015-2025. Hardship withdrawals: 3.3, 3.2, 3.5, 3.3, 3.7, 2.9, 4.0, 2.1, 3.1, 3.8, **4.9%**. Loans: 8.5, 8.7, 8.8, 8.5, 8.6, 7.1, 7.0, 6.6, 8.3, 8.5, **9.5%**. Both are at series highs in 2025, the same direction as Vanguard's 2% to 6%. Sources: FRTIB Participant Behavior and Demographics reports and the TSP Annual Report 2025, Fig. 9 (URLs in the main note, chart-ready table E2). Form 5500 has no hardship field.

### Evidence verdict
Moderate evidence that hardship use rose in 2023-25 in a large government plan, not only in recordkeeper data. It is not attributable to any one law, since the TSP did not adopt BBA-style easing in the same way.

## 6. Force-out $7,000

### Takeaway
I found no DOL, GAO or academic before/after evidence through 5 Oct 2026. Vanguard [recordkeeper/industry]: plans using the $7,000 rollover fell from 57% (2024) to 54% (2025), and $5,000 plans from 29% to 25%. Preservation among separating participants with $1,000-4,999 was 61-62% in 2024-25, against 66% for Vanguard 2023 as used in DOL's RIA. So there is no sign the higher limit raised preservation.

### Evidence verdict
None or weak. Status unchanged.

## Chart-ready series
See `stay_in_plan_leakage.md` chart-ready A (now 1996-2023), B (2004-2023), E2 (TSP hardship and loans, new) and G (auto-portability, updated).
