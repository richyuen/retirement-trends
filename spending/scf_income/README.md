# Sources of retirement income and funding, older households (SCF 1989-2022 + official series)

Built 2026-10-04. Re-run (about 3 minutes plus downloads):

```
SCF_OLD_DIR=/some/cache python3 spending/scf_income/scripts/scf_income_sources.py   # -> output/scf_income_long.csv
python3 spending/scf_income/scripts/scf_income_tables.py                             # -> output/t1..t6 wide tables
python3 spending/scf_income/scripts/official_series.py                               # -> output/official_*.csv (BLS, FRED/BEA, Fed DFA)
```
Needs pandas, numpy, pyreadstat. 2004-2022 SCF files are read in place from `scf/raw/`. The 1989-2001 full public files and replicate weights (not in `scf/raw/`) are downloaded from federalreserve.gov/econres/files/ (`scf89s`, `scf92s`, `scf95s`, `scf98s`, `scf01s` and `*rw1s` zips, about 1.1 GB) into `$SCF_OLD_DIR` (default `/tmp/scf_old`), not into the project folder.

## Files
- `output/scf_income_long.csv`: every SCF statistic, all waves and groups (`all`, `55-64`, `65+`, `65-74`, `75+`), with SE and case count.
- `output/t1_share_of_aggregate_income.csv`: each source's share of the group's total income.
- `output/t2_share_of_aggregate_income_excl_capital_gains.csv`: the same shares with capital gains left out of the total.
- `output/t3_pct_households_with_income_from.csv`: % of households with any income from each source.
- `output/t4_typical_household_shares_and_ss_reliance.csv`: the average of each household's own source shares, and the % of households getting at least 50% / 90% of income from Social Security.
- `output/t5_networth_composition.csv`: % of aggregate net worth held as retirement accounts, home equity, other financial assets, other nonfinancial assets and other debt.
- `output/t6_db_vs_dc_coverage.csv`: % with DB (receiving now, or a current-job or expected future DB benefit), % with DC/IRA accounts, and the four-way split DB only / DC only / both / neither.
- `output/official_published_figures.csv`: hand-entered published numbers (CRS, SSA, Census). Each row has its source, table and URL, plus a `verified_from_document` flag.
- `output/official_bls_lfpr.csv`: CPS labor force participation, 65+ (LNU01300097) and 55-64 (LNU01300095). Annual average of the monthly not-seasonally-adjusted values.
- `output/official_bea_ss_benefits.csv`: BEA NIPA Social Security benefits (FRED W823RC1) and that amount as % of personal income (PI).
- `output/official_fed_dfa_pensions_by_age.csv`: Fed Distributional Financial Accounts by age (Q4 of each year plus the latest quarter). Gives DB and DC pension entitlements as % of assets.

In every table the column is the SCF **survey year**. Income questions cover the **previous calendar year** (`income_year` = survey year - 1).

## Method
- Unit: household (SCF "family"). Age is that of the reference person at interview. Dollar amounts are in 2022 dollars (Fed summary extract).
- The Fed summary extract supplies the income components (bulletin.macro.txt): `WAGEINC`=X5702, `BUSSEFARMINC`=X5704+X5714, `INTDIVINC`=X5706+X5708+X5710, `KGINC`=X5712, `SSRETINC`=X5722 (+`PENACCTWD` from 2004), `TRANSFOTHINC`=X5716+X5718+X5720+X5724.
- **Splitting Social Security from pensions.** X5722 ("Social Security or other pensions, annuities, or other disability or retirement programs", codebook 2022) is one combined amount. I split it for each household in proportion to the *current* annualized amounts reported in the interview:
  - Social Security: X5306/X5307 and X5311/X5312.
  - Regular pension/annuity/disability payments: grid amounts X5318, X5326, X5334, X5418 (plus X5426 and X5434 through 2007), and the remaining-plans items X6804 (1998-2001) and X6958 (2004+), each with its frequency code. Frequencies are converted with the Fed's MCONV macro.

  If X5722 > 0 but both current amounts are zero, the amount is reported as `sspen_unalloc`. This is 0.0-1.1% of 65+ income.
- **Account withdrawals** (`acctwd`) = Fed `PENACCTWD`: IRA withdrawals plus annualized withdrawals from account-type pensions. They are a separate source only from 2004. Before 2004 the SCF folded them into X5724 "other" (codebook 2022 note at X5725) or into X5722 regular payments. `share_agg_comparable_other_plus_acctwd` gives the pre-2004 definition for all waves.
- `transfers` = X5716+X5718+X5720 (unemployment/workers' compensation, child support/alimony, TANF/SNAP/SSI). `other` = X5724.
- **Outlier fix.** A few public-file records carry an X5724 "other income" far above the household's own total X5729. Examples: 1992 cases with $1.7M other income and $11k-57k total income, which pushed the 1992 65+ "other" share to 10.7%. Headline `other` is therefore capped at total income minus the other components. Uncapped values are in `share_agg_other_raw_uncapped`. This lowers other income for 65+ from $139B to $8B in 1992 and $56B to $9B in 1989, with only small effects from 2001 on.
- "Aggregate share" = the group's total from a source / the group's total of all components (capital gains and business losses can be negative). "Typical household share" = the average of each household's own clipped share, over households with positive income. The SS reliance cutoffs use the same per-household share.
- **DB coverage** = receiving a non-account pension now (current amount > 0), or Fed `DBPLANT` (DB on a current job or a pension from a past job expected in the future). DC/IRA = Fed `RETQLIQ` > 0.
- **SEs**: 999 bootstrap replicate weights (wt1b x mm) on implicate 1, plus 1.2 x the between-implicate variance. This is the same as `scf/scripts/scf_analysis.py`, now applied to every wave 1989-2022.
- **Checks**: all-household ownership of retirement accounts is 50.5% (2019) and 54.3% (2022). This matches the Fed's 2023 Bulletin and `scf/README.md`.

## Key findings: SCF, households with head 65+ (SE in parentheses; income years 1988 to 2021)
1. **Earnings are a bigger source, Social Security a slightly smaller one.**
   - Wages: 15.0% (2.5) of aggregate 65+ income in SCF 1989, 20-25% from 1998 on, 21.9% (1.6) in 2022.
   - Households with wage income: 20.6% (1.4) in 1989, 29-31% in 2010-2022.
   - This matches BLS 65+ labor force participation: 11.8% (1989), 12.9% (2000), 17.3% (2010), 20.2% (2019), 18.9% (2021, post-COVID dip), 19.5% (2024).
   - Social Security: 23.2% (2.6) of aggregate income in 1989, a peak of 30.6% (1.0) in 2004, then 20.2% (0.9) in 2022. Excluding capital gains: 25.4%, 31.8%, 23.6%.
2. **Retirement plan income.**
   - Regular pensions and annuities: 10.0% (0.6) of 65+ income in 2022, against 12.9-18.7% in 1989-2010.
   - Account withdrawals: rose from 5.0% (0.6) in 2004 to 8.0% (0.6) in 2022.
   - Households drawing from accounts: 21.3% (1.4) in 2004 and 28.3% (1.3) in 2022. Among 75+ households: 20.2% to 37.2%.
   - Households with pension income: 43.3% (1.3) in 2022, against about 49-52% in 2004-2013.
3. **Asset income is down, capital gains are volatile.** Interest and dividends were 21.0% (3.0) of 65+ income in 1989 and 7.6% (0.5) in 2022. Households with any interest or dividends fell from 60.4% to 36.1%. Capital gains ranged from 1.8% (2010) to 16.8% (2007) and 14.2% (2022).
4. **For the typical household, Social Security is still about half.** The average household's own Social Security share is 52.0% (1.5) in 1989, 49.1% (1.0) in 2022; its pension + withdrawal share is 16.0% then 20.7%. Households with at least 50% of income from Social Security: 54.3% (2.3) in 1989, 44.3% (1.4) in 2019, 46.2% (1.5) in 2022. At least 90%: 15-25%, 17.3% (1.3) in 2022. By age in 2022, 75+ households are more reliant than 65-74 households: 55.8% vs 39.1% at the 50% cutoff.
5. **Balance sheet: from DB to DC.**
   - Retirement accounts: 3.5% (0.6) of 65+ net worth in 1989, 15.2% (1.3) in 2022. Home equity: 24.5% then 19.1%.
   - 65+ households with a DC/IRA account: 20.3% (1.4) in 1989, 47.1% (1.5) in 2022. For 75+: 6.3% to 41.8%.
   - Among all 65+ households, DB coverage (receiving now or expected) has stayed about 46-55%: 46.0% (1.4) in 2022.
   - Among 55-64 households (the next retirees), DB coverage fell from 52.7% (2.2) to 37.2% (1.8).
   - 65+ households: "DB only" fell from 38.6% to 21.6%, "DC only" rose from 6.6% to 22.7%, "both" rose from 13.7% to 24.3%, "neither" fell from 41.1% to 31.3%.

## Official and administrative series (output/official_*.csv)
- **CRS RL33387 Table 7** (CPS, persons 65+, share of aggregate income):

  | Source | 1980 | 2008 |
  |---|---|---|
  | Social Security | 42.8% | 39.0% |
  | Earnings | 15.9% | 26.0% |
  | Asset income | 22.4% | 12.8% |
  | Pensions | 15.3% | 19.5% |

- **SSA Income of the Population 55 or Older, 2014, Table 10.1** (aged units 65+, CPS, 2014): Social Security 33.2%, earnings 32.2%, government pensions 7.9%, private pensions/annuities incl. IRA/401(k) 12.8%, assets 9.7%. Social Security is 22.9% at 65-69 and 46.1% at 80+, and 80.7% in the bottom income quintile vs 15.4% in the top (Table 10.5).
- SSA's Income of the Aged Chartbook 1962 shares were dropped (2026-10-04): ssa.gov returns 403 to this environment, no other copy was found, and the only source was a search summary. For the long view use CRS RL33387 Table 7 above (1968/1980-2008, verified). The Table 10.1 figures above were read from a copy of SSA's Section 10 PDF hosted at sanders.senate.gov/wp-content/uploads/sect10.pdf.
- **Bee & Mitchell (2017), Census SEHSD WP 2017-39**: CPS ASEC linked to IRS 1099-R and SSA records, 2012.
  - Median income of 65+ households: $44,400 in the records vs $33,800 in the survey (+30%). The gap was 20% in 1990.
  - Poverty rate, 65+: 6.9% vs 9.1%.
  - The CPS captures 48% of 65+ retirement income. Retirement income is 34% of their total income in the records.
  - Social Security's share of aggregate income falls from 39% to 31% using the records.
  - 46% of people who receive retirement income do not report it in the survey.
  - Share receiving retirement income: survey 40% (1990) and 36% (2012); records 45% and 61%.
  - Reliance (Table 10, p.60). SSA-style aged units that are SS beneficiaries: at least 50% of income from SS 64.4% survey vs 50.4% records; at least 90%: 35.5% vs 18.1% (SEs 0.4-0.5). Persons 65+ in beneficiary families (family income): 55.5% vs 42.2%; 26.2% vs 12.2%.
- **Bee, Dushi, Mitchell & Trenkamp (2024), CES WP 24-32**: redesigned 2016 CPS, 2015 income, persons 65+.

  | Measure | CPS survey | CPS linked to SSA + IRS |
  |---|---|---|
  | Pensions incl. DC withdrawals, share of income | 23.6% | 33.2% (largest source) |
  | Social Security, share of income | 35.0% | 31.4% |
  | Earnings, share of income | 30.4% | 24.1% |
  | Rely on Social Security for at least 50% | 52.5% | 41.7% (HRS 49.1%) |
  | Rely on Social Security for at least 90% | 25.6% | 13.7% (HRS 20.5%) |
  | Poverty rate | 8.8% | 6.4% |

  Aggregate income is 20% higher with the linked records.
- **Dushi, Trenkamp, Bee & Mitchell (2025), J. Pension Economics & Finance 24(1):95-122** (doi 10.1017/S1474747224000039; published version of CES WP 24-32; abstract read on cambridge.org): 53% of elderly beneficiaries in the CPS ASEC and 49% in the HRS rely on Social Security for the majority of their income vs 42% in the administrative data; elderly poverty 8.8% (CPS), 7.4% (HRS), 6.4% (admin).
- Dushi, Iams & Trenkamp (2017, SSB 77(2)) and SSA's *Basic Facts* fact sheet were dropped (2026-10-04): both are hosted only on ssa.gov, which blocks this environment, so they could not be read. The 2024/2025 papers above, by the same SSA authors, replace them.
- **BEA (FRED W823RC1 / PI)**: Social Security benefits were 4.97% of personal income in 1990, 5.50% in 2010, 5.61% in 2019 and 5.96% in 2025.
- **Fed DFA by age** (DB and DC pension entitlements, % of assets):
  - DB entitlements for 70+ households: 11.9% (1989), 12.5% (2019), 7.9% (2025 Q4).
  - DC as a share of DB + DC: 4.6% to 24.1% for 70+, and 16.3% to 47.6% for 55-69 (1989 to 2025).
  - DFA "DC" excludes IRAs; they sit in equities, mutual funds and other assets.

## Caveats
- **SCF income definitions change.**
  - Account withdrawals are separate only from 2004. Before that they sit in "other" or in X5722.
  - Pension grid amounts exclude account-type plans from 2001 (X6461) but include them in 1989-1998.
  - The pension-grid layout changed in 2004 and 2010.
  - The 2001 to 2004 jumps in pension and DB shares are partly definitional. Compare 2004-2022 for withdrawals, and treat 1989-2001 as a separate era for pensions.
- **The Social Security/pension split is modeled**, from current monthly amounts applied to prior-year totals. Amounts withheld for Medicare premiums and people who start benefits mid-year add noise. X5301 counts SSI and Railroad Retirement as Social Security, and X5722 excludes SSI.
- **The SCF oversamples the wealthy**, so aggregate shares are dominated by high-income households. That makes the SCF Social Security share (20-31%) lower than in the CPS (33-40%) and business/capital-gains shares higher. CPS/SSA tables also exclude capital gains and use different units (aged units or persons, not households). Use the typical-household shares and percent-with measures for the "typical retiree".
- **Capital gains** (X5712) are realized gains in a single year and swing with markets: 2007 (2006 gains) and 2022 (2021 gains) are high, 2010 is low. Use t2 (excluding capital gains) for trends.
- **Survey vs administrative records.** Surveys miss about half of retirement income (Bee & Mitchell 2017; CES 2024). The SCF asks about IRA and plan withdrawals directly, which likely helps, but is not validated against 1099-R. All survey reliance figures are probably overstated.
- **Other data limits.**
  - 1989 has only 730 households aged 65+ in implicate 1, so SEs for 1989 cells are large (e.g. business share 17.5, SE 6.6).
  - Public-file disclosure edits mean components need not sum to X5729. See the outlier fix above.
  - The BLS 2025 average uses 11 months; October 2025 was not published.

## SCF 2025 added (2026-10-27)
SCF 2025 (released by the Fed 9 Oct 2026; income year 2024) added to `scf_income_long.csv` and t1-t6 (new `2025` and `2025_se` columns). The `official_*.csv` files were not touched. Earlier waves are unchanged: 2004-2022 were recomputed and match the previous outputs exactly (max difference 0), and every pre-2025 row of every output file is byte-identical. The 1989-2001 files are not cached here and nothing was downloaded, so those rows were carried over from the previous output. That is what the new `SCF_WAVES` option does: `SCF_WAVES=2004,2007,2010,2013,2016,2019,2022,2025 python3 spending/scf_income/scripts/scf_income_sources.py`, then `scf_income_tables.py`.
- **Variables checked.** The Fed's income definitions (`WAGEINC`, `BUSSEFARMINC`, `INTDIVINC`, `KGINC`, `SSRETINC`, `TRANSFOTHINC`, `PENACCTWD`, `INCOME`) and `RETQLIQ` and `DBPLANT` are unchanged in the 2025 `bulletin.macro.txt`. In `codebk2025.txt`, the X5701-X5729 income questions and the whole "current benefits from pensions" section (X5313-X5435, X6958) match 2022 except for the year. New in 2025, and not used here so that the series stays comparable: X7972/X7979 (Social Security amount received by *other* family members; for 65+ households about 1.3% of the reference person's and spouse's Social Security dollars, 2.5% of households), X9360-X9365 (type of welfare in X5720), and X7792/X7793 (support received from relatives or friends, not part of X5729).
- **Dollars.** The 2025 summary extract is in 2025 dollars. Its dollar variables are multiplied by 4376/4789 (the Fed's CPI bases, as in `scf/scripts/scf_analysis.py`), so every wave stays in 2022 dollars. The implied 2024-income to 2022-dollar factor is 0.938. Shares do not depend on this; only the `mean_*_2022usd` rows do. SEs use the same method as before (999 replicate weights from `p25_rw1.dta` plus 1.2 x the between-implicate variance). 2025 has 1,280 households 65+ in implicate 1.
- **Check.** All-household ownership of retirement accounts is 54.88% (2025), matching the Fed's 2025 historic table 6 and `scf/README.md`.

Headlines, households 65+, SCF 2022 -> 2025 (income years 2021 -> 2024; SE in parentheses):

| Measure | 2022 | 2025 |
|---|---|---|
| Account withdrawals, % of aggregate income (t1) | 8.0 (0.6) | 9.5 (0.7) |
| ... excluding capital gains (t2) | 9.3 (0.7) | 10.5 (0.8) |
| % of households drawing on an account (t3) | 28.3 (1.3) | 29.7 (1.3) |
| ... 75+ | 37.2 (2.2) | 40.6 (2.2) |
| ... 65-74 | 21.7 (1.5) | 20.8 (1.5) |
| Social Security share, average household (t4) | 49.1 (1.0) | 46.2 (0.9) |
| % with at least 50% of income from Social Security | 46.2 (1.5) | 42.7 (1.4) |
| % with at least 90% from Social Security | 17.3 (1.3) | 13.0 (1.1) |
| ... at least 50%, 75+ / 65-74 | 55.8 / 39.1 | 49.1 / 37.5 |
| Pension + withdrawal share, average household | 20.7 (0.8) | 21.2 (0.8) |
| Aggregate share (t1): wages | 21.9 (1.6) | 21.2 (1.4) |
| business | 15.8 (1.1) | 14.8 (1.0) |
| interest and dividends | 7.6 (0.5) | 8.4 (0.6) |
| capital gains | 14.2 (1.6) | 9.0 (1.2) |
| Social Security | 20.2 (0.9) | 22.7 (0.7) |
| Social Security, excluding capital gains (t2) | 23.6 (0.9) | 25.0 (0.7) |
| pensions/annuities | 10.0 (0.6) | 11.9 (0.7) |
| account withdrawals | 8.0 (0.6) | 9.5 (0.7) |
| transfers / other | 0.9 / 1.4 | 0.6 / 1.9 |
| % with wage income (t3) | 29.0 (1.0) | 32.2 (1.1) |
| % with pension income (t3) | 43.3 (1.3) | 43.3 (1.5) |
| Retirement accounts, % of net worth (t5) | 15.2 (1.3) | 19.2 (1.0) |
| Home equity, % of net worth | 19.1 (0.8) | 19.9 (0.8) |
| DB coverage, receiving or expected (t6) | 46.0 (1.4) | 46.1 (1.5) |
| DC/IRA account | 47.1 (1.5) | 47.0 (1.4) |
| DB only / DC only | 21.6 / 22.7 (1.1 / 1.2) | 24.0 / 24.9 (1.3 / 1.2) |
| Both / neither | 24.3 / 31.3 (1.2 / 1.4) | 22.1 / 29.1 (1.3 / 1.2) |
| 55-64: DB coverage / DC/IRA | 37.2 (1.8) / 57.0 (1.7) | 37.3 (2.1) / 63.1 (1.6) |
| Mean income, 2022$ | $128.8k (5.1k) | $120.8k (3.6k) |

What 2025 shows:
- **Account withdrawals reached a series high** of 9.5% of 65+ income, rising every wave since 2004 (5.0%). The share of households drawing on an account is about the same as in 2022 (+1.4, about 0.8 SE of the difference). The rise is at 75+ (40.6%, a series high), not at 65-74, which is consistent with the RMD age moving to 73.
- **Reliance on Social Security fell to series lows.** The average household's Social Security share is 46.2%, at least 50% reliance is 42.7%, and at least 90% reliance is 13.0% (the lowest wave; 15.5-25.0% in 1989-2022; -4.3 points, about 2.5 SE). This is despite Social Security's *aggregate* share rising, from 20.2% to 22.7%. That rise is mostly the drop in capital gains (14.2% -> 9.0%; 2021 gains were unusually high); excluding capital gains it is 23.6% -> 25.0%. More households had wages (32.2%, the highest wave) and account withdrawals, so fewer depend almost entirely on Social Security.
- **Pensions recovered slightly**, from 10.0% to 11.9% of income, but the % with pension income is flat at 43.3%. Retirement accounts rose to 19.2% of 65+ net worth, the highest wave, after the 2023-25 market gains.
- **DB vs DC for 65+ households is little changed.** "DC only" (24.9%) still exceeds "DB only" (24.0%), as it did in 2022, and both rose by less than 2 SE. Among 55-64 households DB coverage is flat at 37%, and DC/IRA ownership rose to 63.1% from 57.0%.
- **Report charts:** none of the report's charts uses a series from this folder. The income-share chart (`incshare`) is CPS, and the SCF coverage, debt and annuity charts come from other folders. The report *text* cites the 2022 SCF figures above (withdrawals 5.0% -> 8.0%, 21.3% -> 28.3% drawing, 75+ 20.2% -> 37.2%, 49.1% Social Security share, net worth 3.5% -> 15.2%, DB only / DC only). `report/` was not edited.
- **Caveats for 2025.** The SS/pension split is still modeled from the reference person's and spouse's current amounts (X7972 is left out; see above). Withdrawals are 2024 dollars, while the balance-sheet items are at the 2025 interview. 2024 capital gains are lower than 2021's, which raises every other aggregate share. Use t2 or the household-level measures to compare 2022 and 2025.
