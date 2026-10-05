# Gap-fill A: log (2026-10-05)

Task gapA. I edited `notes/coverage_state_autoira.md` (sections 1, 2, 3 and 4, plus chart table G). New outputs: `output/irs_w2_deferral_participation.csv` and `output/irs_form8881_credit_claims.csv`. Raw copies are in `raw/gapA/`.

## 1. BLS NCS DC-only series, 2010–2026: closed (no gaps found)
- I re-downloaded `nb.series` and `nb.data.1.AllData` from https://download.bls.gov/pub/time.series/nb/ and checked all 306 values (6 groups × access/participation/take-up × 17 years, period A01 = March) against `output/bls_ncs_access_participation.csv`. There were **0 mismatches and 0 missing cells**. Every row's `source_url` already names its series IDs, so the CSV was not changed.
- Series IDs (private industry, DC): access `NBU22000000000000{sc}28312`; participation `NBU29000000000000{sc}26313`; take-up `NBU29000000000000{sc}32314`. Subcells: 00 all, 01 <100, 02 <50, 25 full-time, 26 part-time, 56 lowest 25% wage. The extract is in `raw/gapA/bls_nb_dc_series_check.csv`.
- DC-only rows for 2008–2009 are not in nb (the series begin in 2010), and the March 2009 release (Table 1) gives only "all retirement".

## 2. Does NCS count state auto-IRAs? Partly closed
There is no explicit BLS statement. The closest definitions (quoted in the notes §3) point to exclusion: payroll-deduction IRAs are "not treated as an employer-sponsored retirement plan" and sit under "Other retirement benefits", and employee-only plans are distinguished from DC plans. One open ambiguity: the current DC type list names IRAs. Next step: email NCSInfo@bls.gov.

## 3. IRS W-2 deferral participation: closed (for TY2008–2020)
- `output/irs_w2_deferral_participation.csv` has 351 rows: all, by age (8 bands) and by nominal wage bins, TY2008–2020. Percentages are Computed from IRS SOI Table 3.C and 3.A counts.
- Headline: the share with any elective deferral went from 34.7% (2008) and 33.5% (2010) to 42.8% (2020). Under-26s went from 12.1% to 20.8%. Within wage bins the rise is small (1–4 points), so wage drift explains part of it.
- Not published: TY2021+ (the latest SOI release, January 2026, covers TY2020). W-2 forms are not counted directly; the unit is taxpayers on filed returns.
- NBER w32843 reports no national trend, only a pooled 2008–17 participation of 65.1% in its large-employer sample. This is quoted in the notes.

## 4. Form 8881 claim counts: partly closed
- SOI corporation line-item estimates give Form 3800 Part III line 1j (Form 8881) for **C corporations only**: 216 returns (2009), 115 (2010), 418 (2012), 523 (2013), 435 (2014), 225 (2015), 88? (2016, suspect), 53 (2017), 457 (2018), suppressed (2020), 476 (2021), 729 / $741K (2022). There were also 724 Forms 8881 filed in TY2022.
- SOI states that pass-through credits are "passed through to individual tax returns, and thus are excluded" from these estimates. Pub. 4801 (individual, TY2023) does not show the line.
- The all-entity figure is still only the academic one: about 18,000 firms (5.5%) in 2023. No Treasury or JCT series was found.

## 5. Illinois opt-out and Pew: Illinois closed, Pew partly closed
- Illinois: the "Effective Opt-Out Rate" was 36.94% (Dec 2025), which confirms the 37% figure. From June 2026 (the rebrand to My Illinois Savings), the dashboard shows an "Opt-out Rate" of 25.3–26.3% with no explanation, most likely a new definition. The notes line was corrected.
- Pew April 2026: the primary page, its Wayback copy and the trade-press copies are all blocked (403 or connection reset). A second independent search extract matches the existing numbers and adds the state increases (0.9–5.9 points; California fell). It is still flagged as partially unverified.

## 6. DOL 2023 participant-count change: closed (by inference)
- The final rule (88 FR, Feb 24 2023) estimated that 18,699 of 86,744 large DC plans would file as small.
- The 2023 Bulletin has no note on the change and sizes plans by total participants at year end. Large DC plans rose 4.6% in 2023 rather than falling about 20%.
- So the "+15.7% small DC plans 2019–2023" finding stands. This is inferred from the numbers; DOL makes no explicit statement.

## Still open
- An explicit BLS ruling on auto-IRAs.
- W-2 deferral data for TY2021+ (needed to see SECURE 2.0-era years).
- An all-entity Form 8881 series.
- Pew primary page text.
- The definition behind Illinois' June 2026 opt-out change.
