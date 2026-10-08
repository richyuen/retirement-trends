# Working after retirement, unconditional on account withdrawals (CPS ASEC 2010-2026)

Built 2026-10-08 for Richard's question "do we have stats on working part time after retirement, unconditional on withdrawals?". Before this, the project had part-time work only **by age** (BLS LN series, finding 5 in `README.md`: 38.3% of employed 65+ usually part time in 2025), and work status only **among account holders** (`scf_6064/`). Nothing measured work among retired people as such.

## Definition
- **Retired** = received Social Security as a retired worker in the prior calendar year (`SS_YN`=1 and `RESNSS1` or `RESNSS2` = 1 "retired"), aged 62+ at the March interview. It does not use account withdrawals, so it is unconditional on them. Withdrawers (`DST_YN`=1) vs non-withdrawers is shown separately as a contrast (2019+ only, updated processing).
- **Working now** = employed in the March reference week (`PEMLR` 1-2). **Part time** = usually part time (`PRWKSTAT` 6-10), the BLS "usually full/part time" split; full time = `PRWKSTAT` 2-5.
- **Worked last year** (same year as the benefit) = `WORKYN`=1; part time = usual hours `HRSWK` < 35.
- Weight `MARSUPWT`. SEs (2019-2026) from the 160 replicate weights in each Census zip; 2010-2018 legacy files have no SEs here (sample sizes are similar, so SEs are similar).

## Results (% of Social Security retirees 62+, March)
| ASEC year | 2010 | 2015 | 2019 | 2021 | 2024 | 2026 | SE 2026 |
|---|---|---|---|---|---|---|---|
| Working | 12.7 | 13.1 | 13.2 | 10.8 | 12.3 | 11.7 | 0.24 |
| Working part time | 7.4 | 7.6 | 7.9 | 5.6 | 7.7 | 7.1 | 0.21 |
| Working full time | 5.3 | 5.5 | 5.3 | 5.2 | 4.6 | 4.6 | 0.17 |
| Part-time share of those working | 58.4 | 58.3 | 60.0 | 52.0 | 62.4 | 60.4 | 1.2 |
| Worked at all in prior year | 16.4 | 16.6 | 16.6 | 14.7 | 15.6 | 15.0 | 0.28 |

1. **About 1 in 8 Social Security retirees works, and about 6 in 10 of those work part time.** In March 2026, 11.7% were employed: 7.1% part time, 4.6% full time. Over the prior year 15.0% worked at some point. This has been flat since 2010 apart from the COVID dip (ASEC 2021), and full-time work has edged down (5.3% -> 4.6%).
2. **By age (2026):** 62-64 12.6% working (9.5% part time); 65-69 18.8% (10.6%); 70-74 15.0% (8.7%); 75+ 6.4% (4.2%). By sex: men 14.2% (7.6% part time), women 9.6% (6.6%); 69% of working women retirees are part time vs 54% of men.
3. **Withdrawals make little difference.** In 2026, 10.4% (SE 0.6) of retirees with account withdrawals were working vs 12.0% (0.3) without; part time 7.2% vs 7.0%. Working withdrawers are more often part time (69% vs 58% of those working). The gap is mainly fewer full-time workers among withdrawers (3.2% vs 5.0%), consistent with RMD-age withdrawers being older.
4. **Retirees vs everyone 65+.** Among all people 65+ (retired or not), 18.3% were working in March 2026 and 39.4% of those part time, matching BLS's annual figures (19.1% LFPR, 38.3% part time in 2025). Retirees work less but are much more often part time. People 62+ not getting SS retirement benefits work at 48%, and only 18% of those workers are part time. Inferred, not decomposed: the rise in older full-time work (BLS finding 5) is mostly among people who have not claimed yet.

## Caveats
- **Selection from later claiming.** As claiming shifts later (see `README.md` finding 7), the people who claim early are increasingly those who have stopped working. This is why working among 62-64 retirees fell from 19.8% (2010) to 12.6% (2026). Read trends for the retiree group with that in mind; levels are the cleaner result.
- The definition misses people retired from a career job who have not claimed Social Security, and counts people who claimed but never retired. Self-described "partial retirement" (the HRS measure) is not in the CPS; HRS is blocked here.
- March reference week, not an annual average. Prior-year work and benefit receipt refer to the same calendar year, but the person may have worked before claiming within that year.
- 2014 uses the traditional 5/8 file. The labor-force and SS-reason items are not affected by the 2014 and 2019 ASEC income changes (the series has no step at either).

## Files
- `scripts/cps_work_after_retirement.py RAW_DIR` (downloads the Census files if missing; raw files ~1.5 GB, not kept).
- `output/cps_work_after_retirement.csv`: long table, `asec_year`, `income_year`, `group`, `measure`, `value`, `se`, `n`. Groups: `ss_retired_62+`, `ss_retired_65+`, by age band and sex, withdrawer/non-withdrawer (2019+), `not_ss_retired_62+`, `all_62+`, `all_65+`.
