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
- `scripts/scf_debt_housing.py` → `output/scf_debt_housing_long.csv` (all stats × year × group, with SEs) and wide tables `output/scf_t1..t14_*.csv` (each with `_se` columns; groups 55-64, 65-74, 75+, 65+, all).
- `scripts/check_vs_fed_tables.py` → `output/check_vs_fed_tables.csv`, `output/fed_table18_payment_ratios_by_age.csv`.
- `scripts/nyfed_debt_by_age.py` → `output/nyfed_debt_share_by_age_quarterly.csv`, `nyfed_debt_share_by_age_annual_q4.csv`, `nyfed_product_by_age_2026q2.csv`, `nyfed_mortgage_orig_share_by_age_annual.csv`.
- `scripts/census_hvs_homeownership.py` → `output/hvs_homeownership_by_age_annual.csv`, `hvs_homeownership_by_age_quarterly.csv`, `hvs_share_households_head_60plus.csv`.
- `scripts/hecm_reverse_mortgages.py` → `output/hecm_endorsements_fy2009_2025.csv`, `output/hmda_reverse_originations_2018_2023.csv`.
- Re-run all from the project root: `for s in scf_debt_housing check_vs_fed_tables nyfed_debt_by_age census_hvs_homeownership hecm_reverse_mortgages; do python3 debt_housing/scripts/$s.py; done`
