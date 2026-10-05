# Retirement spending and sources of retirement income (trends)

Built 2026-10-04 for Richard's follow-up question on retirement spending patterns and sources of retirement funding. Three parts, each with its own README (method, sources with URLs, full tables, caveats):

| Folder | Source | Years | What it answers |
|---|---|---|---|
| `ce/` | BLS Consumer Expenditure Survey, LABSTAT `cx` series by age of reference person; CPI-U `CUUR0000SA0`; published panel research | 1984-2024 | How spending changes with age and over time, budget mix, pandemic, spending vs income |
| `cps_income/` | CPS ASEC public-use files straight from Census (no IPUMS), persons 65+ and SSA-style aged units, replicate-weight SEs | income years 1997-2025 (ASEC 1998-2026) | Share of income from each source, % receiving, Social Security reliance |
| `scf_income/` | SCF public files 1989-2022 (income = prior year), replicate-weight SEs; official series (CRS, SSA via mirror, Census Bee & Mitchell, BEA, Fed DFA, BLS LFPR) | 1989-2022 | Income mix incl. wealthy, balance sheet (DB vs DC), admin-data corrections |

Percentages throughout (Richard's preference). Dollars in 2024$ (CE) or 2022$ (SCF).

## Spending (ce/)
1. **Older households spend more in real terms than they used to, and closer to pre-retirement levels.** Real spending per consumer unit 1984 -> 2024: +37% at 65-74, +66% at 75+, +20% at 55-64 (`ce/output/t1_total_spending_by_age.csv`, BLS `CXUTOTALEXPLB04xxM`). 75+ spending rose from 47.5% to 65.7% of the 55-64 level; 65-74 from 67.7% to 76.9%.
2. **Most of the drop with age is smaller households.** Per person, 65-74 and 75+ spend 89-90% of what 55-64s do (2024). Following synthetic cohorts (55-64 -> 65-74 -> 75+), spending per CU falls to ~82% after 10 years and ~68% after 20, but per person stays ~97% (`t5_pseudo_cohorts.csv`).
3. **Panel research finds real declines of roughly 1-2.8% a year after 65** (Hurd/Rohwedder/Hudomiet NBER w30460, 2022: -1.9%/yr singles, -2.8%/yr couples; Blanchett 2014 "spending smile" -1%/yr; CRR IB 21-21: ~0.8%/yr, less for the wealthy). EBRI (Banerjee 2015): median -12.5% by 3-4 years after retirement, but 46% of households spent more. J.P. Morgan's 2026 Guide to Retirement (Chase transaction data, cross-section) finds average real spending falls by more than 30% from 60 to 85, as reported by PLANADVISER (17 Dec 2025) and Financial Planning (29 Dec 2025); the Guide PDF itself was not retrievable.
4. **Budget mix (65+, 1988 -> 2024):** housing 32.1% -> 36.1% (75+: 39.4%); food 14.9% -> 12.9%; apparel 4.4% -> 2.0%; health care roughly flat at 12-14% (peak 14.0% in 2020, 12.7% in 2024), but within it insurance premiums rose from 42% to ~66-70% while drugs fell after Medicare Part D.
5. **Pandemic:** 65+ real spending fell to 93.6% of 2019 in 2020, was back to ~100 by 2022 and 99.7 in 2024. The mix hasn't returned: food away from home 86 and apparel 75 (2019 = 100) vs shelter 108.5 (75+: 124) in 2024.
6. **Older households spend most of their income:** 65+ spending = 91% of pre-tax income in 2024 (75+: ~100%; 55-64: 70%); about 100% of after-tax income since 2014.

## Income sources (cps_income/, scf_income/)
**Persons 65+, CPS ASEC, share of aggregate income (%)** (`cps_income/output/income_share_65plus_wide.csv`; SEs 0.3-0.55 in 2026)

| Source | 1997 inc. (A) | 2012 inc. (A) | 2018 inc. (C) | 2025 inc. (C) |
|---|---|---|---|---|
| Earnings | 16.8 | 30.2 | 29.0 | 27.2 |
| Social Security | 40.5 | 37.6 | 32.0 | 32.3 |
| DB pensions | 19.2 | 17.5 | 15.9 | 12.7 |
| Annuities | 0.3 | 0.3 | 2.0 | 2.0 |
| Retirement-account withdrawals | 0.2 | 0.8 | 7.0 | 7.6 |
| Asset income | 19.9 | 10.5 | 11.2 | 15.1 |

Series A = traditional questions, C = updated processing; do not compare levels across A/B/C (breaks measured within one year in `cps_income/README.md`). From 2019 on, asset income includes interest credited inside 401(k)/IRAs (6.8% of 2025 income); excluding it, 2018 -> 2025: SS 33.4 -> 34.7, DB 16.6 -> 13.7 (-2.9, SE 0.4), withdrawals 7.3 -> 8.1 (+0.8, SE 0.4).

1. **Work became a major source, then plateaued.** Earnings' share roughly doubled from 1997 to 2012 (16.8% -> 30.2%) and has been ~27-31% since, tracking 65+ labor force participation (BLS: 11.9% in 1998, 20.2% peak 2019, 19.1% 2025). SCF agrees: wages 15.0% (1989) -> 21.9% (2022 survey) of 65+ household income; households with wages 20.6% -> 29.0%. CE agrees: wages 20.9% (1988) -> 35.3% (2024) of 65+ CU income.
2. **DB pensions are shrinking; account withdrawals are replacing them.** CPS DB share 19.2% -> 12.7%; DB receipt at 65-69 22.9% (2019) -> 18.3% (2026) per `cps/README.md`. SCF account withdrawals 5.0% (2003 inc.) -> 8.0% (2021 inc.) of 65+ income, households drawing 21.3% -> 28.3% (75+: 20.2% -> 37.2%); pensions/annuities fell to 10.0% in 2022 from 13-19%. Balance sheet: retirement accounts 3.5% -> 15.2% of 65+ net worth (1989 -> 2022); 65+ "DB only" households 38.6% -> 21.6%, "DC only" 6.6% -> 22.7%; DB coverage of 55-64s fell 52.7% -> 37.2% (`scf_income/output/t5_*, t6_*`). Fed DFA: DC share of DB+DC pension wealth at 55-69 went 16% -> 48% (1989-2025, excl. IRAs).
3. **Social Security is still the largest single source for the typical retiree.** It is ~32% of aggregate 65+ income in CPS (2025) but about half of income for the median SCF household (52.0% -> 49.1%). Receipt is 81% of people 65+, though at 65-69 it fell from 83.8% (1998) to 64.4% (2026) as claiming moved later. BEA: SS benefits rose from 4.97% (1990) to 5.96% (2025) of personal income.
4. **Survey data overstate reliance on Social Security.** CPS aged beneficiary units getting >=50% / >=90% of income from SS: 58.3% / 31.9% (2025 income; SE 0.4), down from ~64% / 30-36% mostly at the questionnaire breaks. With linked IRS/SSA records:
   - Bee & Mitchell 2017 (Census SEHSD WP 2017-39, Table 10; 2012 income), SSA-style aged beneficiary units: >=50% falls from 64.4% (survey) to 50.4% (records), >=90% from 35.5% to 18.1%. Persons 65+ in beneficiary families: 55.5% -> 42.2% and 26.2% -> 12.2%.
   - Bee, Dushi, Mitchell & Trenkamp 2024 (CES WP 24-32; 2015 income, redesigned CPS), persons 65+: >=50% 52.5% -> 41.7%, >=90% 25.6% -> 13.7%. With admin data, pensions incl. DC withdrawals (33.2%) overtake Social Security (31.4%) as the largest source of 65+ income; the survey gives 23.6% vs 35.0%. The peer-reviewed version (J. Pension Economics & Finance 24(1), 2025) gives majority-of-income reliance of 53% (CPS) and 49% (HRS) vs 42% (admin), and poverty 8.8% / 7.4% / 6.4%.

## How the sources compare
- Social Security share of 65+ income: CPS 32% (2025), CE 37-38%, SCF ~20% (aggregate, weighted toward the wealthy; ~24% excl. capital gains), admin-linked 31% (2015). Differences are unit and coverage, not trend: all three surveys show earnings rising and SS/DB pension falling as shares.
- Surveys capture only about half of retirement-plan income (Bee & Mitchell 2017: CPS 48%, 46% of recipients don't report it; IRA distributions "rarely reported"). Read **trends within a consistent series**, not levels; levels of pension + withdrawal income are understated and SS/earnings shares overstated.

## Verification status (updated 2026-10-04, final)
Every number above traces to a document read in full or in part; `scf_income/output/official_published_figures.csv` has 90 rows, all `verified_from_document = yes`.
- **Read from a copy, not the original host:** SSA *Income of the Population 55 or Older, 2014*, Table 10.1/10.5, from the Section 10 PDF hosted at sanders.senate.gov (ssa.gov blocks this environment). J.P. Morgan's ">30% from 60 to 85" from two trade-press reports of the 2026 Guide.
- **Dropped because they exist only on blocked hosts:** SSA Income of the Aged Chartbook 1962 shares (use CRS RL33387 Table 7, 1968/1980-2008, instead); Dushi, Iams & Trenkamp 2017 (Social Security Bulletin 77(2)); SSA *Basic Facts* admin-linked reliance figures; a secondary summary of Hurd & Rohwedder's "Spending Trajectories" rates (RAND and the Michigan center block this environment; the Wharton PRC slides by the same authors are used instead). The admin-linked replacements are by the same SSA authors (Dushi, Trenkamp) and were read in full.
- **Resolved:** the ASEC 2023 dip in interest credited inside retirement accounts. Recipiency is unchanged and the mean among reporters halves, matching the 2022 market fall (S&P 500 -19.4%); inferred, not confirmed by Census (`cps_income/README.md`, caveat 2). Use the exclRINT tables for trends.

## Remaining limits (not closable from here)
- SCF splits of SS vs pensions are modeled from current-benefit amounts (X5722 has no split); SCF withdrawals separate only from 2004.
- CPS: ASEC 1998 is the earliest March file Census posts; the 2014 and 2019 breaks mean levels are compared only within a series. SSA-style aged units are the household-type unit; a householder-65+ unit was not built because the aged unit is what SSA and Bee & Mitchell use.
- CE: cross-sectional, 75+ excludes institutions, income imputed from 2004 and redesigned 2013.
- HRS (CAMS panel spending) not used directly because the HRS site is blocked; published HRS-based results are cited instead.
