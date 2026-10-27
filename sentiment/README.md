# Consumer sentiment and retirement contributions

Built 2026-10-26 for Richard's question: are consumer sentiment and retirement plan contributions correlated or cointegrated?

## Short answer

**No meaningful relationship.** Contributions as a share of wages follow a slow structural trend (more people contributing, auto-enrollment, the DB-to-DC shift), and sentiment does not move them in any reliable way.

1. **Levels are negatively correlated, but that is spurious.** Employee DC contributions rose from 1.5% of wages (1984) to 5.0% (2025) while sentiment drifted down (annual average 98 in 1984, 58 in 2025, near its record low). Level correlation is -0.45 for employee DC and -0.53 for employer DC (BEA, 1984-2025), but the level regressions have Durbin-Watson statistics of 0.1-0.3, the textbook sign of a spurious regression between trending series.
2. **No cointegration.** Cointegration needs two series that both wander without a fixed mean (I(1)) and share a stable long-run link. Sentiment is a bounded index: over 1960-2025 the ADF test is borderline (p = 0.06) and KPSS does not reject stationarity. Results by specification (`tests_annual.csv`, ICS, full samples):
   - **Engle-Granger, contributions on sentiment, constant only:** no rejection for any DC series (BEA employee DC p = 0.79). It rejects only for the Form 1040 IRA deduction share (p < 0.001), which is itself stationary (ADF p < 0.001).
   - **Engle-Granger with a trend:** rejects for BEA employer DC (0.010), Form 5500 DC incl. rollovers (0.021), Form 1040 (0.010) and W-2 deferrals (p < 0.001, but only 13 years, too short to trust).
   - **Engle-Granger with sentiment as the dependent variable:** rejects for BEA employee DC (0.041), BEA employer DC (0.032) and IRS IRA dollars (p < 0.001), consistent with sentiment being close to stationary on its own.
   - **Johansen, constant only:** rejects r = 0 only for IRS IRA dollars (27.1 vs 15.5) and Form 1040 (20.4); BEA employee DC 7.9 vs 15.5.
   - **Johansen, constant and trend:** rejects r = 0 for BEA employee DC (22.3 vs 18.4), BEA employer DC (20.5), Form 5500 participant (29.1) and Form 5500 DC incl. rollovers (23.2). But in all four the r <= 1 test also rejects (6.5-6.9 vs 3.8; employer DC 4.5), i.e. Johansen picks rank 2, which means each series is stationary around a trend on its own rather than the two sharing a stochastic trend. The estimated long-run vector also puts almost no weight on sentiment (about 0.005 or less per index point).

   So the rejections that appear come from individual series being (near) trend-stationary, or from a short sample, not from a shared trend between contributions and sentiment. For Form 5500 participant contributions the single-series ADF with trend does not itself reject (p = 0.20, 25 years), so that attribution rests on the Johansen rank-2 result. No specification gives a consistent, economically sensible long-run relationship; the levels relationship is negative (contributions up, sentiment down).
3. **Year-to-year changes: at most a weak, same-year link for contributions people choose themselves; none for employers.**
   - Employee DC contributions (BEA, 1985-2025): r = 0.26 (p = 0.10); 0.31 (p = 0.06) leaving out 2020-21. In a regression controlling for the change in unemployment (Newey-West SEs), a 10-point rise in sentiment goes with +0.03 percentage points of wages that year (p = 0.002). That is small: the typical yearly change is +0.09 pts, sentiment's typical yearly move is about 8 points, and sentiment explains about 10% of the year-to-year variation.
   - Share of taxpayers contributing to an IRA (IRS, 2000-2021): r = 0.21 (p = 0.38); 0.53 (p = 0.03) leaving out 2020-21. Only 17-19 years.
   - Employer DC contributions (BEA and Form 5500): no link (r = -0.08 to -0.25, not significant). Employer matches and nonelective contributions follow plan formulas and payroll, not mood.
   - Form 5500 participant contributions, IRS IRA dollars, Form 1040 IRA deduction share, and W-2 deferrals: no reliable link.
4. **Sentiment does not lead contributions.** Correlations of contribution changes with sentiment changes one or two years earlier are near zero, and Granger tests (1 lag) find no predictive power in either direction (BEA employee DC: p = 0.65 sentiment-to-contributions, 0.93 the other way).
5. **Multiple testing:** of 66 year-over-year correlations (11 series x 3 sentiment measures x 2 samples), 4 have p < 0.05, about what chance alone would give (3.3). The employee DC result is the one that holds up across sentiment measures and samples, and it is small.

Interpretation (judgment, not tested): DC contributions are set once (a deferral percentage, often a default under auto-enrollment) and then run on autopilot, which is what the contribution-rate research found (median employee rate 6% in every SCF wave; see `../contributions/README.md`). Mood would show up mainly at the margins people actively choose, such as whether to make an IRA contribution this year, and that is where the weak positive signs appear.

## Charts

- `output/fig1_levels.png`: sentiment, employee DC and employer DC (% of wages), 1984-2025, as three panels.
- `output/fig2_changes.png`: year-to-year changes in employee and employer DC contributions against changes in sentiment.

## Data

| Series | Source | Years | Unit |
|---|---|---|---|
| Michigan Index of Consumer Sentiment (ICS), current conditions (ICC), expectations (ICE) | University of Michigan Surveys of Consumers, https://www.sca.isr.umich.edu/files/tbmics.csv, tbqics.csv, tbmiccice.csv (downloaded 2026-10-26) | monthly 1978-2026, quarterly 1960-1977 | index (1966Q1 = 100) |
| Unemployment rate (control) | BLS via FRED UNRATE | 1948-2026 | % |
| Employee DC contributions (household DC contributions, all sectors) | BEA NIPA, `../contributions/admin/output/bea_nipa_pension_contrib.csv` | 1984-2025 | % of all wages |
| Employer DC; employer DB+DC | BEA NIPA, same file | 1984-2025; 1960-2025 | % of private wages |
| DC participant, employer, total incl. rollovers | DOL Form 5500 (`dol_dc_contrib_by_source.csv`, `dol_e13_contributions_by_type.csv`) | 1999-2023; 1975-2023 | % of private wages |
| IRA contributions; taxpayers contributing | IRS SOI (`ira_contributions_by_type.csv`) | 2000-2021 (2003 missing) | % of wages; % of taxpayers |
| Returns with IRA deduction | IRS SOI Form 1040 (`f1040_ira_keogh_deduction_long.csv`) | 1987-2023 | % of returns |
| W-2 elective deferrals; earners deferring | IRS SOI W-2 (`w2_deferrals_totals.csv`) | 2008-2020 | % of wages; % of earners |
| Quarterly check: employer contributions for pension and insurance funds (B040RC); personal saving rate (A072RC) | BEA NipaDataQ.txt | 1960Q1-2026Q2 | % of wages; % of disposable income |

Annual sentiment is the calendar-year average of the monthly index (quarterly survey average before 1978).

**Conference Board Consumer Confidence Index:** its site is reachable but the history is proprietary (only the latest reading is public, 88.6 in August 2026), so it was not used. The OECD US consumer confidence series on FRED stops in January 2024 and was saved to `raw/` but not used.

## Why the tests are annual

The coordinator suggested BEA NIPA quarterly data. BEA publishes the DC/DB pension split only annually (Tables 6.11D, 7.8, 7.22-7.25). The only quarterly series is B040RC, employer contributions for pension **and insurance** funds, which is mostly employer health insurance, and BEA's quarterly figures for these supplements are largely interpolated from annual data. It was run as a check (`tests_quarterly.csv`): no relationship in changes (r = -0.05 to -0.13, not significant). The quarterly personal saving rate shows a negative same-quarter correlation with sentiment, but it comes entirely from 2020-21 (sentiment fell while saving jumped); leaving those quarters out, nothing remains.

Annual samples are short (13-66 years), so tests have low power: the results rule out a strong relationship, not a very small one.

## Method

`scripts/analyze.py`, for each contribution series and each of ICS, ICE, ICC, with and without 2020-21:
1. Unit roots: ADF (levels with trend for contributions, with constant for sentiment; differences) and KPSS.
2. Pearson correlations in levels, linearly detrended levels, and first differences; Spearman in differences. Differences across missing years or method breaks are dropped (IRS 2003 gap; IRS IRA series stop at 2021 because of the TY2022 SOI method break; Form 1040 starts 1987 after the 1986 tax reform).
3. Lead/lag correlations of differences, k = -2..+2 years (quarterly: -4..+4).
4. OLS of the change in contributions on the change in sentiment (same year and lagged one year), with and without the change in unemployment; Newey-West SEs (2 lags annual, 4 quarterly). Coefficients are reported per 10-point change in sentiment. Newey-West p-values are optimistic in samples under ~25 years.
5. Granger causality (1 lag) in differences, both directions.
6. Engle-Granger (constant; constant + trend; both directions) and Johansen trace test (r = 0, constant and trend, 1 lagged difference).

Detrended-level correlations are reported but not relied on: removing a linear trend leaves highly autocorrelated residuals, so their p-values overstate significance.

## Files

- `scripts/build_data.py` -> `output/annual_panel.csv`, `output/quarterly_panel.csv`
- `scripts/analyze.py` -> `output/tests_annual.csv`, `output/leadlag_annual.csv`, `output/tests_quarterly.csv`, `output/leadlag_quarterly.csv`
- `scripts/charts.py` -> `output/fig1_levels.png`, `output/fig2_changes.png`
- `raw/`: Michigan files, FRED UNRATE / UMCSENT / OECD confidence, and the BEA quarterly extract (`nipa_q_extract.csv`, from https://apps.bea.gov/national/Release/TXT/NipaDataQ.txt)

Run order: `python3 -I scripts/build_data.py && python3 -I scripts/analyze.py && python3 -I scripts/charts.py` (needs pandas, statsmodels, scipy, matplotlib).

Column guide for `tests_*.csv`: `r_*`/`p_*` correlations and p-values; `reg_*` regression without the unemployment control, `reg_ctrl_*` with it (`_b_dx_per10` = change in contributions per 10-point sentiment rise, same year; `_dxl1` = previous year); `eg_p_*` Engle-Granger p-values; `johansen_trace_r0_*` and `johansen_trace_r1_*` (r <= 1) with 5% critical values `johansen_cv5_*`; `adf_p_*`, `kpss_p_*` unit-root tests (KPSS p-values are bounded at 0.01-0.10).

## Income cohorts (added 2026-10-26)

Richard asked whether income cohorts show anything different. They don't: no income group's contributions move reliably with its own sentiment. Script `scripts/cohorts.py` -> `output/cohort_sentiment_annual.csv`, `cohort_panel_w2.csv`, `cohort_panel_scf.csv`, `cohort_tests.csv`.

- **Sentiment by income:** Michigan ICS for the bottom, middle and top third of family income (data.sca.isr.umich.edu demographic tables, Table 1a, monthly from Dec 1979; `raw/umich_ics_income_*.xls`). Top minus bottom: 8.1 (1980), 20.3 (2000), 11.3 (2019), 1.4 (2022), 11.1 (2025).
- **IRS W-2 deferrals by wage third, 2008-2020** (bins split pro rata at the tercile boundaries; individual wage earners, nominal bins). Earners deferring: bottom 8.4% -> 14.2%, middle 35.0% -> 44.9%, top 60.8% -> 69.4%. Change correlations with own-third sentiment: -0.04 to 0.22 for participation; deferrals % of wages -0.19 to 0.04 except top third -0.53 (p = 0.08), which is 2020 alone (0.01 without it).
- **SCF by family income quartile, 13 waves 1989-2025** (Q1 paired with bottom-third sentiment, Q2-Q3 middle, Q4 top): change correlations -0.22 to 0.50, none significant (n = 12).
- **Panels with period fixed effects** (does a group whose sentiment falls more than others' cut more?): W-2 +0.18 pts deferring per 10 pts (HC1 p = 0.70, permutation p = 0.76); SCF +0.9 pts contributing (p = 0.46, perm 0.54) and +0.23 pts of wages in employee DC (p = 0.33, perm 0.32). HC1 SEs plus a within-period permutation test; cluster SEs were dropped because 3-4 income groups are too few clusters (they had given a misleading p = 0.04 once 2025 was added).
- **Saver's Credit (low-income marker), 2002-2023:** r = 0.37 with bottom-third sentiment changes (p = 0.10).
- **Aggregate series vs each third's sentiment:** BEA employee DC 0.18 (bottom), 0.25 (middle), 0.25 (top); no third fits better.

**SCF 2025 (added 2026-10-27):** the 2022-2025 change is the one wave where the income groups' sentiment split (bottom third 60.0 -> 53.6, top third 61.4 -> 64.7), and employee DC contributions moved in the predicted direction (Q1 1.25% -> 0.99% of wages, Q4 5.43% -> 6.11%). It raises the pooled employee-DC coefficient from +0.09 to +0.23 per 10 points, still not significant. Q1 families contributing were flat (6.4% -> 6.5%).

The full write-up is a Claude Doc: https://claude.ai/artifact/Byw2yfRUJe5aNt7U3VbBiy

## SCF cohort table (added 2026-10-27)

`output/scf_cohort_contrib_vs_sentiment.csv` (built by `scripts/scf_cohort_table.py`) puts the SCF income-cohort series and sentiment in one table: one row per wave (1989-2025) and family income quartile, 52 rows. Columns: families contributing to a current-job DC plan (% of families), take-up among families with a DC plan (%), employee and employer DC contributions (% of current main-job pay), each with its replicate-weight SE; `n_families` is the unweighted sample count (the SCF oversamples high-wealth families, so Q4 has the most cases); the matched Michigan sentiment (`ics_own_group`: Q1 = bottom third, Q2-Q3 = middle, Q4 = top) plus all three thirds and all respondents. DC items are current at the interview in the survey year; quartiles use prior-year family income; sentiment is the survey year's calendar average.
