# Debt and housing wealth among older households

How much debt older households carry and what kind, how heavy it is relative to income and assets, how many own their home and still owe on it, how much of their wealth is home equity, how much of the nation's household debt older borrowers now hold, and how reverse mortgages have moved. Built 2026-10-05 from public sources only: SCF microdata (already on disk in `scf/raw/`), the Fed's published SCF tables, the New York Fed Household Debt and Credit report, Census CPS/HVS, HUD/FHA and CFPB. The 2022 SCF is the latest wave; SCF 2025 is due late 2026.

Ties in with report Section 13: housing is 36.1% of 65+ spending in the CE (2024; `spending/README.md`, finding 4). A mortgage payment is part of that.

## Findings

1. **Far more older households carry debt than a generation ago. The rise is steepest at 75+.**
   - SCF, share of households with any debt, by age of the reference person:

     | Any debt (%) | 1989 | 2001 | 2004 | 2016 | 2019 | 2022 (SE) |
     |---|---|---|---|---|---|---|
     | 55-64 | 70.8 | 75.6 | 76.3 | 77.1 | 77.4 | **77.2** (1.4) |
     | 65-74 | 49.7 | 56.8 | 58.8 | 70.1 | 70.0 | **64.8** (1.6) |
     | 75+ | 21.0 | 29.2 | 40.3 | 49.8 | 51.4 | **53.4** (2.1) |
     | 65+ | 37.8 | 43.2 | 49.4 | 61.1 | 62.1 | **59.9** (1.2) |

   - The rate for 55-64 barely moved. The share of the 75+ who owe money went from 1 in 5 to more than half.
   - At 65-74 the share peaked in 2016-2019 (70%) and fell back in 2022 (64.8%). Pandemic-era paydowns are one likely reason; the SCF cannot show why.
   - [`output/scf_t1_any_debt_pct.csv`]

2. **Mortgages are the main reason. More than a third of older homeowners still owe on their home.**
   - Share of households with debt secured by the primary residence (mortgage, HELOC or home-equity loan):
     - 65-74: 21.8% (1989), peak 42.9% (2007), 32.2% (2022).
     - 75+: 6.3% (1989), 27.6% (2022).
     - 55-64: 37.0%, then 48.4%.
     - [`scf_t2`]
   - Among **homeowners**, the share still carrying home-secured debt:

     | Owners with home debt (%) | 1989 | 2001 | 2004 | 2013 | 2019 | 2022 (SE) |
     |---|---|---|---|---|---|---|
     | 55-64 | 46.2 | 58.9 | 64.4 | 65.8 | 62.4 | **62.2** (1.8) |
     | 65-74 | 28.1 | 38.8 | 39.5 | 49.2 | 48.0 | **42.3** (2.0) |
     | 75+ | 9.0 | 12.4 | 22.0 | 24.8 | 33.6 | **34.0** (2.3) |
     | 65+ | 20.7 | 26.4 | 30.4 | 38.5 | 41.8 | **38.6** (1.4) |

   - Balances are larger too. Median home debt among 65+ owners who have it rose from $20,800 (1989) to $101,200 (2022), in 2022 dollars. [`scf_t10`, `scf_t14`]
   - The NY Fed credit-bureau data agree: mortgage plus HELOC is **80.2%** of the debt held by borrowers 70+ (2026Q2, five listed products), against 78.5% at 60-69 and 77.7% at 50-59.

3. **Credit-card debt is up too, but less dramatically.**
   - Share carrying a card balance after the last payment:
     - 65-74: 27.1% (1989), 33.9% (2022), with a peak of 42.1% in 2016.
     - 75+: 10.1% (1989), 29.8% (2022).
     - 55-64: 32.9%, then 44.3%.
   - [`scf_t3`]

4. **Debt is larger relative to income, but small relative to assets. The share with heavy payment burdens has not risen.**
   - Median debt among older debtors, 2022 dollars:

     | Age | 1989 | 2022 |
     |---|---|---|
     | 55-64 | $21,900 | **$90,000** |
     | 65-74 | $11,500 | **$45,000** |
     | 75+ | $6,800 | **$36,000** |

     [`scf_t4`]
   - Aggregate debt-to-income (total debt / total income of the group):
     - 65-74: 23.8% (1989), 61.7% (2022).
     - 75+: 10.2% (1989), 46.9% (2022).
     - Among 75+ debtors, the median debt-to-income ratio went from 13.7% to 52.0% (SE 12.3).
     - [`scf_t5`, `scf_t6`]
   - Aggregate debt-to-assets (the Fed's leverage ratio) is still low:
     - 65-74: 2.8% (1989), 4.7% (2022), peaking at 7.8% in 2010.
     - 75+: 1.1% (1989), 3.0% (2022).
     - 55-64: 6.8%, then 7.8%.
     - [`scf_t7`]
   - Debt payments above 40% of income, as a share of debtors:
     - 65-74: 8.7% (1989), 9.8% (2022), with a peak of 18.1% in 1998.
     - 75+: 14.1% (1989), 8.4% (2022).
     - 55-64: 8.4%, then 10.7%.
     - No upward trend at any age. [`scf_t8`]
   - Fed Table 18 (published) adds two series:
     - Aggregate payments as a share of income rose: 65-74 from 5.3% to 7.6%; 75+ from 2.2% to 5.4%.
     - Debtors 60+ days late on any payment: 75+ from 1.2% to 2.6%; 65-74 from 3.3% to 3.6% (1989 to 2022).
     - [`output/fed_table18_payment_ratios_by_age.csv`]
   - Reading: more older households owe money, and they owe more relative to income. But for most of them, payments are a modest and stable share of income, and debt is small next to their assets.

5. **Older borrowers now hold a quarter of US household debt, double their 1999 share. That is faster growth than their share of households.**
   - NY Fed Consumer Credit Panel/Equifax, share of total debt balances by borrower age:
     - 60+: **11.4%** (1999Q4), 20.4% (2012Q4), 23.1% (2019Q4), **24.5%** (2026Q2).
     - 70+: **3.6%**, then **9.7%**. The 70+ share is still rising: 8.0% (2019) and 9.0% (2025).
     - 60-69: 7.7%, peaked at 15.6% (2015), and has been 14.3-14.8% since 2020.
     - Both 60+ and 70+ hit their series highs in 2026Q1 (24.8% and 9.9%).
   - Over a similar span, the share of US households headed by someone 60+ rose from 26.6% (1999) to 37.9% (2025) (Census HVS Table 12). The debt share more than doubled while the household share rose by about two-fifths.
   - In nominal dollars, 60+ balances went from $0.55T (1999Q1) to $4.59T (2026Q2), out of $18.8T.
   - 2026Q2, share of each product's balances held by borrowers 60+:

     | Product | Held by 60+ |
     |---|---|
     | HELOC | 39.8% |
     | Credit card | 30.4% |
     | Mortgage | 25.3% |
     | Auto | 21.3% |
     | Student loans | 10.5% |

   - Borrowers 60+ took 15.6% of mortgage origination dollars in 2025 (9.6% in 2000; peak 18.5% in 2013 and 2021).
   - [`output/nyfed_*.csv`]

6. **Homeownership at 65+ is high and steady, about 79%. It is falling just before retirement.**
   - Census CPS/HVS annual rates by age of householder:

     | Homeownership (%) | 1982 | 1990 | 2000 | 2004 | 2010 | 2016 | 2022 | 2025 |
     |---|---|---|---|---|---|---|---|---|
     | 55-64 | 80.0 | 79.3 | 80.3 | 81.7 | 79.0 | 75.0 | 75.1 | **75.9** |
     | 65-74 (65-69 / 70-74) | 77.9 / 75.2 | 80.0 / 78.4 | 83.0 / 82.6 | 83.2 / 83.4 | 81.6 / 82.4 | 79.0 / 81.7 | 78.8 / 80.2 | **78.5 / 80.6** |
     | 75+ | 71.0 | 72.3 | 77.7 | 78.8 | 78.9 | 77.0 | 78.6 | **77.4** |
     | 65+ | 74.4 | 76.3 | 80.4 | **81.1** | 80.5 | 78.8 | 79.1 | **78.6** |
     | All | 64.8 | 63.9 | 67.4 | 69.0 | 66.9 | 63.4 | 65.8 | 65.2 |

   - The quarterly 65+ rate was 78.6% in 2026Q2. The national rate was 65.0%. [`output/hvs_homeownership_by_age_*.csv`]
   - The SCF agrees: 65+ owners were 74.5% (1989), 83.3% (2004) and 78.2% (2022, SE 0.7). [`scf_t9`]
   - The 55-64 drop (81.7% in 2004 to 75-76%) points to cohorts entering retirement less often as owners than today's retirees did.

7. **Home equity is about half of a typical older owner's net worth, but only a fifth of older households' total wealth.**
   - Among 65+ homeowners with positive net worth, the median household's home equity is **51.4%** of its net worth (2022, SE 1.9). It was 56.5% in 1989 and 43.1% at a 2016 low. For 75+ owners it is 56.8%. [`scf_t12`]
   - Aggregated over all 65+ households, home equity is **19.1%** of net worth (2022), down from 24.5% (1989) and 27.2% (2004). Financial assets (retirement accounts, stocks) held by wealthier households dominate the total. [`scf_t11`]
   - Median home equity of 65+ owners was **$250,000** in 2022 (2022 dollars), against $115,300 in 1989 and $197,100 in 2019. Much of that is the 2020-22 price run-up. [`scf_t13`]

8. **Reverse mortgages are a niche product, and it has shrunk.**
   - FHA HECM endorsements (fiscal years, HUD FY2025 Annual Report Table B-26):
     - **114,425 in FY2009**, falling to 48,329 in FY2018.
     - A refinance-driven bump to 64,472 in FY2022, when 45% were HECM-to-HECM refinances.
     - **26,502 in FY2024 and 28,149 in FY2025.**
   - Per 1,000 homeowner households headed by someone 65+, that is **6.1 in 2009 and 0.9 in 2025** (our calculation with HVS owner counts).
   - Average borrower age rose from 71.8 (FY2013) to 75.3 (FY2025).
   - HMDA, which covers all reporting lenders, including proprietary (non-FHA) reverse mortgages, counted reverse-mortgage originations of 33k (2018), 59k (2021 and 2022) and **25k (2023)** (CFPB 2023 Mortgage Market Activity and Trends, Table 1E).
   - So fewer than 1 in 1,000 older homeowners take a new reverse mortgage in a year. Home equity is mostly tapped by selling, through HELOCs, or not at all.
   - [`output/hecm_endorsements_fy2009_2025.csv`, `hmda_reverse_originations_2018_2023.csv`]

## Method
- **SCF** (`scripts/scf_debt_housing.py`)
  - Fed summary extracts `scf/raw/rscfpYYYY.dta` for 1989-2022, in 2022 dollars. The script reuses `scf/scripts/scf_analysis.py` (read, estimate, replicate weights) without changing it.
  - Variables follow the Fed's `bulletin.macro.txt`:
    - HDEBT: any debt.
    - HMRTHEL: mortgage, HELOC or home-equity loan on the primary residence.
    - HCCBAL: credit-card balance after the last payment.
    - DEBT, INCOME, ASSET, NETWORTH, HOUSES, MRTHEL, HOMEEQ (= HOUSES − MRTHEL).
    - HOUSECL = 1: homeowner.
    - PIR40: total payments / monthly income > 0.4.
  - Groups are the age of the reference person at interview.
  - Ratios:
    - "Aggregate" = sum over households / sum over households.
    - "Median ... among debtors" = weighted median of each household's ratio.
    - The home-equity share median is among owners with positive net worth.
  - Point estimates pool the 5 implicates. SEs (2004+) use 999 bootstrap replicate weights on implicate 1 plus 1.2 × the between-implicate variance, as in `scf/`. Before 2004 there are no SEs, because the replicate files were not downloaded.
  - Runtime is about 6 minutes.
- **Check against the Fed** (`scripts/check_vs_fed_tables.py`)
  - All 252 comparable cells match the Fed's published historical tables (2022 dollars). That covers 3 ages × 12 waves for any debt, home-secured debt, credit-card balance, median debt, leverage, payments > 40% and homeownership.
  - Largest gaps: 0.005 points on percentages and $479 on a median (0.008%). [`output/check_vs_fed_tables.csv`]
- **NY Fed** (`scripts/nyfed_debt_by_age.py`): Page 20 (debt by age, 1999Q1-2026Q2), Page 21 (product by age), and Page 23 (mortgage originations by age, summed over complete years). Shares use the sum of the six age groups. Borrowers with an unknown birth year are excluded, so the sum is within 0.1% of the Page 3 total.
- **Census** (`scripts/census_hvs_homeownership.py`)
  - HVS Table 12 (households and owners by age, annual 1982-2025): rate = owners / households.
  - Where a year has both an original and a revised column (1993 and 2002 population-control revisions), the revised value is used. Spot check: 2004 65+ = 81.1%, the published figure.
  - Table 19 gives quarterly rates for 1994Q1-2026Q2.
- **Reverse mortgages** (`scripts/hecm_reverse_mortgages.py`)
  - HUD Tables B-26 and B-31 are transcribed in the script and checked row by row against the PDF text (17/17 rows).
  - The rate per 1,000 divides fiscal-year endorsements by calendar-year 65+ owner households.

## Sources
- Federal Reserve Board, Survey of Consumer Finances public data and the Fed's `bulletin.macro.txt`: https://www.federalreserve.gov/econres/scfindex.htm (files in `scf/raw/`).
- Federal Reserve Board, SCF 2022 historical tables, real (2022 $), Tables 9, 12, 13 and 18: https://www.federalreserve.gov/econres/files/scf2022_tables_public_real_historical.xlsx (`raw/`).
- Federal Reserve Bank of New York, Quarterly Report on Household Debt and Credit, August 2026 (2026Q2) data file: https://www.newyorkfed.org/medialibrary/interactives/householdcredit/data/xls/HHD_C_Report_2026Q2.xlsx (`raw/`). Landing page: https://www.newyorkfed.org/microeconomics/hhdc
- U.S. Census Bureau, CPS/Housing Vacancy Survey historical tables 12 and 19: https://www.census.gov/housing/hvs/data/histtabs.html (`raw/hvs_histtab12.xlsx`, `raw/hvs_histtab19.xlsx`).
- HUD/FHA, Annual Report to Congress Regarding the Financial Status of the FHA Mutual Mortgage Insurance Fund, FY2025, Tables B-26 and B-31: https://www.hud.gov/sites/dfiles/Housing/documents/2025FHAAnnualReportMMIFund.pdf (`raw/`).
- CFPB, 2023 Mortgage Market Activity and Trends (December 2024), Table 1E: https://files.consumerfinance.gov/f/documents/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf (`raw/`).
- Context: `spending/README.md` (CE budget share for housing).

## Caveats
- **SCF unit and age.** The unit is the household (SCF "family"), classed by the age of the reference person. A couple with a 66-year-old head and a 60-year-old spouse counts as 65-74.
- **SCF small cells.**
  - The 75+ cells rest on smaller samples: SEs are about 2 points on shares and up to 12 points on median debt-to-income.
  - Pre-2004 waves have no SEs here.
  - The 2004 75+ figures look high for any debt and home debt (40.3% and 18.7%, against 31.4% and 13.9% in 2007). Read that wave's 75+ figures as noisy, not a peak.
- **Credit-card measure.** `HCCBAL` counts balances still owed after the last payment. Convenience users who pay in full are not counted.
- **Home equity share.** The aggregate share and the median household's share answer different questions. Don't mix them. Net worth here excludes DB pension and Social Security wealth, so home equity's share of total retirement resources is lower than shown.
- **NY Fed data.**
  - These are individuals with a credit file, by the borrower's age. How joint accounts are split between co-borrowers was not checked.
  - The SCF is households by the head's age, so the two are not comparable in levels.
  - The NY Fed file has no population counts by age. The HVS household-share comparison uses 60+ householders, which is not the same as 60+ individuals with credit files. Treat it as context, not a per-capita rate.
  - Dollar balances are nominal; the shares are unaffected.
- **Census HVS.**
  - 2025 annual figures and 2025Q4 cover 11 months or 2 months only: October 2025 was not collected because of the funding lapse.
  - Population-control revisions in 1993 and 2002 cause small level shifts.
  - HVS and SCF homeownership definitions differ slightly. Both put 65+ at 78-79% in 2022.
- **Reverse mortgages.**
  - HUD counts are fiscal years (October-September). The 2009-2025 series is what this report contains; earlier years were not verified, so they are dropped.
  - The refinance share above is our count-based figure (10.9% in FY2025). HUD's text quotes 12.26%, which is an MCA-dollar share (Exhibit I-32). Don't mix the two.
  - HECM borrowers can be 62-64, so "per 1,000 owner households 65+" is an approximate scale measure, not a take-up rate.
  - The HUD table's adjustable/fixed product columns look mislabeled in FY2009, so they are not used.
  - HMDA reverse-mortgage counts include HECMs and proprietary loans from HMDA reporters only. The latest CFPB report with this table covers 2023; no 2024 edition was found on consumerfinance.gov.
- **Not verified / dropped.**
  - The often-quoted "share of 65+ debtors in bankruptcy/collections" and pre-2009 HECM volume (no source opened).
  - The CFPB's older reverse-mortgage reports (2012 Report to Congress, advertising spotlights). They are listed at https://www.consumerfinance.gov/data-research/research-reports/ but were not needed for volumes.
  - Per-capita debt by age (no population denominator in the NY Fed file).

## Files
- `scripts/scf_debt_housing.py` → `output/scf_debt_housing_long.csv` (all stats × year × group, with SEs) and wide tables `output/scf_t1..t14_*.csv` (each with `_se` columns; groups 55-64, 65-74, 75+, 65+, all). Since 2026-10-27 these include 2025, plus `output/scf_payment_ratios_long.csv` (Table 18 payment measures, 1989-2025).
- `scripts/check_vs_fed_tables.py` → `output/check_vs_fed_tables.csv`, `output/fed_table18_payment_ratios_by_age.csv`.
- `scripts/nyfed_debt_by_age.py` → `output/nyfed_debt_share_by_age_quarterly.csv`, `nyfed_debt_share_by_age_annual_q4.csv`, `nyfed_product_by_age_2026q2.csv`, `nyfed_mortgage_orig_share_by_age_annual.csv`.
- `scripts/census_hvs_homeownership.py` → `output/hvs_homeownership_by_age_annual.csv`, `hvs_homeownership_by_age_quarterly.csv`, `hvs_share_households_head_60plus.csv`.
- `scripts/hecm_reverse_mortgages.py` → `output/hecm_endorsements_fy2009_2025.csv`, `output/hmda_reverse_originations_2018_2023.csv`.
- Re-run all from the project root: `for s in scf_debt_housing check_vs_fed_tables nyfed_debt_by_age census_hvs_homeownership hecm_reverse_mortgages; do python3 debt_housing/scripts/$s.py; done`

## SCF 2025 added (2026-10-27)
SCF 2025 (fieldwork 2025, released by the Fed 9 Oct 2026) is added to `scripts/scf_debt_housing.py`, following `scf/README.md` ("SCF 2025 added"). Everything above this section still describes 1989-2022 and is unchanged.
- **Method.** Same Fed variables. `bulletin.macro.txt` (2025 vintage) defines HDEBT, HMRTHEL, HCCBAL, DEBT, MRTHEL, HOUSES, HOMEEQ, HOUSECL, INCOME, ASSET, PIRTOTAL, PIR40, TPAY and LATE60 exactly as the 2022 vintage does. The late-payment question (X3005) has the same wording. The 2025 extract is in 2025 dollars (checked: HOUSES equals the nominal X-variable sum). Its dollar variables are multiplied by 4376/4789 (`TO_2022USD` in `scf/scripts/scf_analysis.py`), so all dollar figures stay in **2022 dollars**. To restate in 2025 dollars, multiply by 1.094. SEs as before: 999 replicate weights on implicate 1 plus 1.2 × the between-implicate variance.
- **Pre-2025 outputs are unchanged.** All 1989-2022 rows of `scf_debt_housing_long.csv` and `scf_t1..t14` are identical to the previous run. `check_vs_fed_tables.csv` is byte-identical (still 252/252 cells).
- **Not checked against the Fed for 2025.** The Fed's 2025 historical tables are not on disk, and nothing was downloaded. Every 2025 cell is our own tabulation. Re-run `check_vs_fed_tables.py` once `scf2025_tables_public_real_historical.xlsx` is in `raw/` (sheet names and the 2025 dollar base will need updating).
- **New file:** `output/scf_payment_ratios_long.csv`. It holds the Fed Table 18 payment measures (aggregate payments/income, median payments/income among debtors, > 40%, 60+ days late) for every wave, with SEs. For 1989-2022 all 144 cells match the published Table 18 within 0.05 points (the table's rounding). This lets the Table 18 series in finding 4 run to 2025.

2022 → 2025, households by age of the reference person (SE in parentheses; dollars in 2022 dollars):

| | 55-64 | 65-74 | 75+ | 65+ |
|---|---|---|---|---|
| Any debt (%) [`scf_t1`] | 77.2 (1.4) → **81.4** (1.4) | 64.8 (1.6) → **67.7** (1.6) | 53.4 (2.1) → **52.3** (2.3) | 59.9 (1.2) → **60.8** (1.3) |
| Debt secured by home, all households (%) [`scf_t2`] | 48.4 (1.5) → 48.0 (1.5) | 32.2 (1.7) → **37.2** (1.6) | 27.6 (1.9) → 26.2 (2.2) | 30.2 (1.1) → 32.2 (1.2) |
| Owners still owing on home (%) [`scf_t10`] | 62.2 (1.8) → 65.2 (1.7) | 42.3 (2.0) → **46.6** (1.9) | 34.0 (2.3) → 31.8 (2.6) | 38.6 (1.4) → **39.8** (1.5) |
| Median home debt, owners with it [`scf_t14`] | $125,000 (5,700) → $148,000 (9,000) | $110,000 (6,200) → $109,700 (9,400) | $90,000 (13,200) → $92,300 (12,000) | $101,200 (5,400) → **$104,200** (7,700) |
| Credit-card balance (%) [`scf_t3`] | 44.3 (1.6) → 49.4 (2.0) | 33.9 (1.6) → 37.8 (1.8) | 29.8 (2.0) → 27.6 (2.2) | 32.1 (1.2) → 33.2 (1.5) |
| Median debt, debtors [`scf_t4`] | $90,000 (8,500) → $92,300 (6,900) | $45,000 (6,800) → $49,300 (4,600) | $36,000 (9,100) → $30,200 (6,100) | $40,900 (3,700) → $42,900 (4,100) |
| Aggregate debt / income (%) [`scf_t5`] | 75.5 (4.0) → 81.8 (4.2) | 61.7 (4.6) → 64.6 (4.6) | 46.9 (4.4) → 44.3 (4.1) | 56.3 (3.4) → 55.9 (2.9) |
| Median debt / income, debtors (%) [`scf_t6`] | 94.2 (6.6) → 86.3 (5.9) | 64.3 (6.7) → 73.3 (9.5) | 52.0 (12.3) → 54.4 (12.5) | 60.6 (5.7) → 64.1 (7.2) |
| Aggregate debt / assets (%) [`scf_t7`] | 7.8 (0.4) → 7.9 (0.4) | 4.7 (0.4) → 4.5 (0.4) | 3.0 (0.3) → 2.8 (0.3) | 4.0 (0.3) → 3.7 (0.2) |
| Payments > 40% of income, debtors (%) [`scf_t8`] | 10.7 (1.3) → 11.1 (1.5) | 9.8 (1.4) → 10.0 (1.4) | 8.4 (1.8) → **14.3** (2.4) | 9.3 (1.1) → 11.7 (1.3) |
| Aggregate payments / income (%) [Table 18 measure] | 9.3 (0.5) → 10.4 (0.5) | 7.6 (0.5) → 8.9 (0.6) | 5.4 (0.5) → 6.3 (0.6) | 6.8 (0.4) → 7.8 (0.4) |
| Median payments / income, debtors (%) | 14.6 (0.8) → 14.9 (1.1) | 11.7 (1.1) → 14.0 (0.8) | 10.8 (0.6) → 12.9 (1.9) | 11.4 (0.5) → 13.8 (0.8) |
| Debtors 60+ days late (%) | 6.2 (0.8) → **9.0** (1.4) | 3.6 (0.8) → **7.3** (1.1) | 2.6 (1.0) → **5.1** (1.4) | 3.2 (0.7) → **6.5** (0.9) |
| Homeowner (%) [`scf_t9`] | 77.8 (1.0) → **73.6** (1.1) | 76.1 (1.1) → 79.8 (1.1) | 81.0 (1.4) → 82.3 (1.5) | 78.2 (0.7) → **80.9** (0.6) |
| Median home equity, owners [`scf_t13`] | $232,000 (13,500) → $265,000 (14,800) | $252,000 (10,300) → $270,500 (16,100) | $230,000 (14,700) → $274,100 (11,300) | $250,000 (8,700) → **$274,100** (8,600) |
| Home equity / net worth, median owner (%) [`scf_t12`] | 48.0 (2.6) → 40.4 (2.1) | 46.0 (2.5) → 49.2 (2.6) | 56.8 (2.9) → 56.9 (2.2) | 51.4 (1.9) → **52.1** (2.0) |
| Home equity / net worth, aggregate (%) [`scf_t11`] | 19.3 (0.8) → 17.6 (0.7) | 18.5 (1.1) → 18.9 (0.9) | 20.0 (1.3) → 21.0 (1.2) | 19.1 (0.8) → **19.9** (0.7) |

Payment rows without a `scf_t` tag are from `scf_payment_ratios_long.csv`.

What 2025 shows:
- **Any debt at 65+ is flat at about 60%:** 37.8% (1989), 59.9% (2022), 60.8% (2025). The 2022 → 2025 change is within one SE. The 65-74 rate partly recovered from its 2022 dip (64.8 → 67.7, against 70.0 in 2019). The 75+ rate held at 52-53%. The 55-64 rate rose to 81.4%, its highest after 2007 (81.8).
- **Older owners still owing on their home:** 38.6% → 39.8% at 65+, not a significant change. 65-74 rose back to 46.6% (2019: 48.0). Median home debt at 65+ is $104,200 (about $114,000 in 2025 dollars), against $101,200, within the SE.
- **Payment burdens rose, mainly at 75+, and lateness doubled.**
  - At 75+, debtors paying more than 40% of income went from 8.4% to 14.3% (SE 2.4). That is back in the 1989-2007 range (12-22%), not a series high.
  - Aggregate payments as a share of income rose at every age (65-74: 7.6% → 8.9%; 75+: 5.4% → 6.3%).
  - Debtors 60+ days late on any payment roughly doubled at every age. 65-74 reached 7.3%, the highest of any wave (previous high 6.1% in 2010). 75+ reached 5.1% (1995: 5.4%).
  - One likely reason (not tested): the 2022 wave fell in the federal student-loan payment pause and a period of low delinquency, and repayment restarted in late 2023.
  - Debt is still small next to assets (65-74: 4.5%; 75+: 2.8%).
- **Homeownership (SCF):** 80.9% at 65+ (2022: 78.2%), about 2 points above the HVS 2025 rate (78.6%). At 55-64 it fell to 73.6% (77.8%), the lowest of any SCF wave, consistent with the HVS decline before retirement.
- **Home equity:** the median 65+ owner's home equity rose to $274,100 in 2022 dollars, or about $300,000 in 2025 dollars ($250,000 in 2022). It is still about half of the median older owner's net worth (52.1%) and a fifth of aggregate 65+ net worth (19.9%).
- **Report chart series** (Figure 45, any debt): 2025 values are 55-64 **81.4**, 65-74 **67.7**, 75+ **52.3** (SEs 1.4, 1.6, 2.3). `report/` was not edited.

2025 caveats:
- The 2025 questionnaire reworked the education-loan section (more program and consolidation detail, paid-off loans added). The Fed's DEBT definition did not change, but student-loan reporting may not be fully comparable with 2022.
- The 2025 75+ payment-burden and lateness cells rest on small samples (SEs 1.4-2.4 points). Medians at 75+ have SEs of $6,000-12,000.
- 2025 dollar figures depend on the CPI ratio 4376/4789. The Fed's own 2025 real tables use 2025 dollars, so compare dollar cells only after converting.
- The 2019 55-64 any-debt value is 77.35% in `scf_t1`. The findings table above prints 77.4 and report Figure 45 uses 77.3, both from the same number. That is pre-existing and was not changed.
