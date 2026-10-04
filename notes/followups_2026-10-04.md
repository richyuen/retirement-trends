# Follow-up analyses, 2026-10-04 (SIPP, IRS refresh, SCF 60-64, CPS finishing)

Four analyses Richard asked for after the microdata cross-check. Each folder's README has method, sources, SEs and caveats. Nothing in report/, output/ or CLAUDE.md was changed; candidate report edits are listed at the end for the thread that owns the report.

## 1. SIPP 2018-2025 (reference years 2017-2024) -> sipp/
- Person level, Census public files, 240 replicate weights. IRA vs DC withdrawals are asked separately only from SIPP 2021 (ref 2020) on; 2017-2019 lumps IRA, DC and DB together and is not comparable. SIPP 2021 asked retired owners only, so 2020 comparisons use a retired-only series.
- Incidence per 100 IRA holders (2021-2023): about 12 at 60-64, 19-25 at 65-69, 50-56 at 70-74, 74-80 at 75-79, 77-83 at 80+.
- Withdrawal rate, all holders (IRA+DC): 2.3-2.7% at 60+, 1.2-1.7% at 60-69, 3.7-4.1% at 70+. Withdrawers only: 5.4-5.7% dollar-weighted at 60+, median 5.1-5.6%.
- RMD age move is sharp by single year of age: at age 72, 64-67 per 100 withdrew in 2020-2022, then 37 (2023) and 30 (2024). The 2020 waiver lowers 75+ incidence by 10-20 points; the withdrawers-only rate does not move (same as SCF 2009).
- Fits SCF (all-holder 2.2-3.1%, withdrawers 5.2-6.9%). Before 70 it matches Poterba-Venti-Wise (about 1.9%); 70+ is lower (3.7-4.1% vs about 5.8%).
- Validation: ownership within 0.3 pt of Census wealth tables 2022-2023. Against IRS, SIPP captures 76-83% of IRA holders 60+, 55-63% of withdrawers, 47-68% of dollars.
- Caveat: 2024 topcode ($1.09M) inflates 2024 rates (3.7% / 8.2%); with Census's median topcode value they are 2.3% / 5.2% (sensitivity version included).

## 2. IRS SOI refresh -> irs/
- Rollover flag resolved: ICI $669.8B and IRS $635.9B are the same cell (TY2022 Table 1, traditional rollovers) from IRS's first TY2022 release (Feb 2025) and the June 4 2026 re-release under a revised method. ICI's current Q2 2026 data shows 635.9. Use $635.9B traditional / $664.3B all types. The original Feb 2025 file could not be fetched; the link rests on ICI's citation, its dates and matching cells.
- New caveat: IRS calls 2022-23 "a new series", a method break at 2022. Age-level figures barely move; Roth withdrawals jump $5.7B -> $23.8B.
- Form 1040 line 4a gross IRA distributions TY2022 = $497.47B (17.36M returns; Pub 4801 Rev. 12-2024 p.16). SOI withdrawals vs 1040: 2019 -0.87%, 2020 -2.19%, 2021 -0.69%, 2022 +3.05%, 2023 +1.93%. "Within about 2%" fails for 2022. Adding Roth conversions overshoots by 3.6-10.4%, which argues against conversions being inside withdrawals.
- TY2024 IRA tables not yet released. No revisions: all 720 cells of js_559 and 240 of js_563 match current IRS files.

## 3. Why 60-64 SCF withdrawals fell -> scf_6064/
- Incidence did not fall (15.6 -> 15.0 per 100 holders, 2003/06 vs 2018/21); the dollar rate did (1.58% -> 0.69%). Large draws (10%+ of balance) fell 7.7 -> 3.3 per 100.
- Most of the fall (-0.78 of -0.88 pt) is pension-account payouts and rests on a few households (one 2006 household = 41% of 60-64 dollars). Trimming each wave's top 3 withdrawers leaves 0.83 -> 0.49 (SE 0.14). IRA part barely moved.
- Composition (reweighted to early mix) explains -0.28 of the trimmed -0.34 but only a quarter of the headline fall: more 60-64 holders working (70 -> 77%), fewer on Social Security (26 -> 15%), more money in current-job DC plans (holders with one 48 -> 62%). Roth, education, marriage, DB coverage explain essentially nothing. Thin cells: suggestive.

## 4. CPS ASEC finishing -> cps/ (README updated)
- SEs (Census replicate weights, 4/160 formula): about 0.3 pt at 65+, 0.4-0.8 by age band, 2019-2026. The 2020 dip at 70-74 (23.1 -> 16.1) is clear (z = -8); 70-74 stays 4.6-6 pt below 2019 in every year 2022-2026; 75-79 rise vs 2019 is marginal (z = 2.2); 65+ overall unchanged 2019-2026.
- Pandemic entropy-balanced weights lower 65+ shares by 0.2-0.8 pt; 70-74 dip becomes 22.3 -> 15.8.
- 2026 65+ population jump explained: ASEC 2026 uses Vintage 2025 controls (2020 Census base). About 1.65M of the 3.7M jump is new controls, about 2.1M aging. Shares move by at most 0.05 pt.

## Candidate report edits (for the report thread)
- Replace the open rollover flag with the resolution; add the 2022 IRS method-break caveat.
- Data note: 1040 comparison now covers 2019-2023, with 2022 at +3.05%.
- Section 10: add SIPP rates (all holders vs withdrawers) next to SCF and the old SIPP study; add the age-72 single-year RMD chart.
- Replace "falling rates at 60-64" with the scf_6064 explanation (incidence flat; dollar fall is concentrated, partly composition).
- CPS: add SEs/significance, the pandemic-weight check, and the 2026 population-control note.
