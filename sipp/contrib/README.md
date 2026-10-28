# SIPP workplace-plan contributions, ref years 2020-2024 (2026-10-28)

Source: SIPP 2021-2025 public-use files (Census), December record, WPFINWGT. Universe: ages 18-64 with earnings in all 12 months (EARN_YR = sum of monthly TPEARN > 0).
Items: EMJOB_401 (has 401k/403b/TSP from main employer), ESCNTYN_401 / TSCNTAMT_401 (own contributions), EECNTYN_401 / TECNTAMT_401 (employer contributions).
Main-employer plans only. No item for personal IRA contributions; ESCNTYN_IRA is employer-provided IRAs (SEP/SIMPLE) only. SIPP 2018-2020 files (ref 2017-2019) lack these items.
% of pay = contribution / annual earnings (TPEARN, all jobs), contributors with earnings >= $1,000, capped at 100%. Amounts topcoded. No SEs (point estimates only).
Scripts: ex.py (download + extract to scratch parquet, zips deleted), tab.py. Output: sipp_dc_contrib_2020_2024.csv.
