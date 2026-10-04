# SIPP long series, 1996-2024: IRA + 401(k) withdrawals by age (combined accounts)

Built 2026-10-04 from Census public-use SIPP files (www2.census.gov/programs-surveys/sipp/data/datasets/). Feeds report Figures 17-18.

## Pieces
| Years | Source | Withdrawal item | Balances |
|---|---|---|---|
| 1996-2004, 2008-2010 | 1996, 2001, 2004, 2008 panels: core waves + Assets & Liabilities topical modules (1996 w3/6/9/12, 2001 w3/6/9, 2004 w3/6, 2008 w4/7/10) | TPPNDIST, monthly person distributions from IRA, Keogh, 401k (ISS code 42), summed over the 12 months of the three core waves ending at the module | TALRB + TALKB + TALTB, "as of the last day of the reference period" (end of window) |
| 2014-2019 (bridge) | 2014 panel waves 2-4 (ref 2014-16); SIPP 2018-2020 (ref 2017-19) | ERET_LUMPSUM: any lump sum or regular distribution from a retirement plan (IRAs, 401k AND DB pensions pooled; asked at 59+). 2014 panel = yes/no; 2018-2020 = lump/regular/both/none | TIRAKEOVAL + TTHR401VAL |
| 2021-2024 | SIPP 2022-2025 (from `../sipp/`) | EIRA_INC_YN / ETHR_INC_YN and amounts | TIRAKEOVAL + TTHR401VAL (Dec 31) |
No usable items: 2005-2007 (no asset modules after 2004 panel w6), 2011-2013 (2008 panel had no later asset modules; 2014 panel w1 has no item), 2020 (SIPP 2021 asked retired owners only).

## Scripts (run from this folder; raw files go to /tmp, outside the shared folder)
- `scripts/extract.py` -> `data/sipp_hist_persons.parquet` (761k person-wave rows) + `/tmp/sipph/reps_*.parquet`.
  **1996 core layout:** Census now serves re-edited longitudinal `l96puwN` files whose layout is NOT the posted `sip96wNd.asc` dictionaries. Positions come from NBER `data.nber.org/sipp/1996/sip96l1.dct` (same for waves 1-12), verified against data. 2001-2008 use Census dictionaries (match the .sas files).
- `scripts/extract_2014.py` -> `data/sipp2014_dec.parquet` (reads 5 GB csvs in 20k-row chunks; 200k chunks get OOM-killed).
- `scripts/tabulate.py` -> `output/sipp_hist_long.csv`, `output/sipp_hist_windows.csv` (window dates, labels, attrition).
- `scripts/bridge.py` -> `output/sipp_bridge_long.csv`.
- `scripts/combine.py` -> `output/sipp_combined_long.csv` (both eras, identical definitions, with SEs). Needs 2018-2025 replicate weights in `/tmp/sipp/reps` (rebuild with `../sipp/scripts/extract.py` `extract_rw`).
- `scripts/capture.py` -> `output/sipp_balance_capture_vs_ici.csv`.
- `data/cpi_u_annual.csv` (FRED CPIAUCNS annual means; not used in the final measures).

## Definitions
Person level; holders = combined balance > 0 at end of window/year; old panels require all 12 months present (91-97% of holders). Year label for old panels = calendar year of the one December inside the 12-month window (2008 panel: label 2008 = Sep 2008-Nov 2009, 2009 = Sep 2009-Nov 2010 incl. waived Dec 2009). Incidence = withdrawers per 100 holders. Rate = withdrawals / end balance. `rate_below_p85` drops holders above the 85th percentile of combined balance among holders 60+ that year (all topcoded old-panel cases are above it). SEs: Fay BRR 4/R (R = 108 for 1996/2001, 120 for 2004/2008, 240 for 2014+).

## Findings
- Incidence 75+: 67-80 per 100 (1996-2004), 55-67 (2008 panel, overlapping 2009 waiver), 74-86 (2021-24). 70-74: 62-71 (1996-2000) -> 51-59 (2021-24) as first RMD moved 70.5 -> 72 -> 73.
- 60-64: 10-15 old vs 13-17 new; 65-69: 18-22 vs 25-28. 55-59: ~1 vs 6-8, so the old monthly item misses one-off withdrawals (inferred); compare from 60 up only.
- Bridge jumps 8-12 points at the 2017 rewording; dropping DB-pension people lowers it by at most 6 points.
- **Rates are not comparable across eras.** Old panels capture 44-62% of ICI IRA assets and 33-79% of DC (DC coverage doubled 1996-2005); new files 88-109% and 119-153%. Old-era rates are probably overstated and their decline partly coverage. Age pattern is robust.
