# The decline of defined-benefit (DB) pensions

How far private-sector DB pensions have shrunk, how many of the plans that remain are closed or frozen, why state and local government DB coverage is different, and what this means for households and retirees. Built 2026-10-05 from public sources: DOL Form 5500 tables, the BLS Employee Benefits Survey (EBS) and National Compensation Survey (NCS), PBGC data tables, and SCF microdata. Every number is a percentage unless marked otherwise (Richard's preference). Counts appear only where they show scale. This folder overlaps with `spending/` (retiree income) and `dc_stay/` (Form 5500 source files). Those numbers are reused here, not recomputed.

## Findings

1. **The "38% in 1980" figure checks out. "~15% today" is out of date: it is about 9% now.** The figure measures private wage and salary workers who are active participants in a DB plan.

   | Year | DOL Form 5500 (published 1980-99, own extension) | PBGC-insured actives, % of private wage & salary workers | BLS NCS, private industry DB participation |
   |---|---|---|---|
   | 1980 | **38.4** (DOL) / 37.7 (own) | **37.0** | - |
   | 1990 | 27.7 / 27.3 | 29.6 | - |
   | 1999-2000 | 20.6 (1999, DOL) / 19.9 (2000) | 20.7 (2000) | 21 (1999), 19 (2000) |
   | 2010 | 14.3 | 15.6 | 19 |
   | 2015 | 11.5 | 12.0 | 16 |
   | 2020 | 9.4 | 10.0 | 11 |
   | 2022-23 | **8.2** (2023) | **8.7** (2022) | 11 (2023) |
   | 2026 | - | - | **9** (March 2026; also 9 in 2025) |

   - The 38% comes from DOL's Table E4 in the *Abstract of 1999 Form 5500 Annual Reports*. In 1980, 28% of private wage and salary workers were in a DB plan only and 11% in both a DB and a DC plan. The underlying counts, (21,861k + 8,239k) / 78,349k, give 38.4%. The DB-only share fell to 7% by 1999, while DC-only rose from 8% to 29%.
   - DOL stopped publishing this table after 1999. I extended it with Form 5500 active DB participants (historical Table E7) divided by CPS private wage and salary workers. Over 1980-1999 my series is within 0.7 points of DOL's published figure every year.
   - The PBGC series (Table S-23) is independent and gives the same picture: **37.0% (1980) to 8.7% (2022)**. Single-employer plans: 28.8% to 5.7%. Multiemployer (union) plans: 8.2% to 3.0%.
   - "About 15%" matches around 2010: 14-16% on all three measures.
   - [`output/dol_form5500_db_dc.csv`, `output/dol_e4_1980_1999.csv`, `output/pbgc_insured.csv`, `output/bls_ebs_ncs_db_dc.csv`]

2. **DB plans now hold a small share of the private pension system.** All figures are DOL Form 5500 historical tables E1, E4 and E7:

   | | 1975 | 1980 | 1990 | 2000 | 2010 | 2023 |
   |---|---|---|---|---|---|---|
   | DB % of private pension plans | 33.2 | 30.3 | 15.9 | 6.6 | 6.6 | 5.5 |
   | DB % of all participants (incl. retirees, separated) | 74.2 | 65.6 | 50.5 | 40.3 | 31.9 | 18.9 |
   | DB % of active participants | 70.8 | 61.4 | 42.6 | 30.4 | 19.0 | 10.3 |
   | Actives as % of a DB plan's participants | 82.5 | 79.2 | 67.5 | 53.4 | 41.5 | 37.7 |

   - The number of DB plans peaked at 175,143 in 1983 and was down to 46,233 by 2023, a drop of 74%. Most of that drop was small plans, between 1985 and 2000.
   - Active DB participants peaked in 1980 at 30.1M. By 2023 they were down to 11.1M, a drop of 63%.
   - Total DB participants kept rising until 2008 (42.3M), because retirees and separated vested participants were still building up. They fell to 29.3M by 2023 (-31%).
   - Fewer than 4 in 10 DB participants are now working for the sponsor. The rest are retirees or people who left with a vested benefit.

3. **The fall shows up in BLS employer surveys as well, starting in the early 1980s.** These are BLS EBS and NCS data, % of workers participating:
   - **Private medium and large establishments: 84% in DB (1980-82) to 50% (1997).** DC participation in the same establishments rose from 53% (1985) to 57% (1997).
   - Small private establishments (<100 workers): 20% (1990) to 15% (1996).
   - All private industry: 21% (1999), 20% (2006), 19% (2010), **9% (2025, 2026)**.
   - Private DB access went from 20% (2010) to 14% (2025-26).
   - Private DB take-up (participants / workers with access) fell from 91% to 68%. That fits plans being closed to new hires: newer employees work where a plan exists but cannot join it.
   - Private DC participation rose from 36% (1999) to 41% (2010) and 49-50% (2024-26).
   - NCS data have a gap in 2007-2009: the database series start in 2010, and bls.gov is blocked from here. The EBS AP series run 1999-2006.
   - [`output/bls_ebs_ncs_db_dc.csv`]

4. **About half of the active workers still in single-employer DB plans are in plans that are closed or frozen.** PBGC Tables S-26 and S-27, premium filings, single-employer plans:

   | Plan year | Plans with any accrual or participation freeze | Hard-frozen plans | Actives in hard-frozen plans | Actives in frozen plans (hard or partial) | Actives in any closed or frozen plan |
   |---|---|---|---|---|---|
   | 2008 | 27.9 | 21.0 | 8.3 | 17.5 | 26.9 |
   | 2012 | 40.4 | 30.5 | 13.7 | 26.9 | 39.3 |
   | 2016 | 34.4 | 25.7 | 21.3 | 38.6 | 49.9 |
   | 2022 | 31.3 | 23.7 | **20.8** | 43.0 | **54.5** |

   - "Closed or frozen" means hard-frozen, partially frozen, or still accruing but closed to new entrants. The share of active participants in plans that are fully open fell from 73.1% (2008) to **45.5% (2022)**.
   - The share of plans frozen peaked in 2012 and then eased. Many frozen plans were terminated, which takes them out of the denominator.
   - BLS NCS gives a similar picture for private DB participants:
     - Only 78% were in open plans in 2010, falling to **57% in 2025** (63% in March 2026).
     - The hard-frozen share went from 9% (2014) to 19% (2025) and 15% (2026).
     - NCS dropped its 2010-2013 "frozen" breakdown in 2014. [`output/pbgc_freeze.csv`, `output/bls_ncs_db_freeze.csv`]

5. **The PBGC-insured system is shrinking through terminations and risk transfers, not through plan failures.**
   - Single-employer insured plans: 112,208 (1985 peak) to 35,373 (2000) to **22,196 (2025)**, down 80% from the peak.
   - Insured participants peaked at 34.5M in 2004 and fell to **18.4M by 2025 (-47%)**. Almost all of that drop (-15.0M of -16.2M) came after 2011.
   - Standard (fully funded) terminations ran at about 1,100-1,900 a year, between 3.7% and 7.9% of insured plans each year over 2000-2024 (my ratio, fiscal-year terminations over plan-year counts). The rate rose to **2,121 (9.6%) in FY2025**, the highest since 2000.
   - Distress terminations taken over by PBGC fell from 74-193 a year in 2000-2010 to 11-26 a year in 2022-2025.
   - Partial risk transfers (lump-sum windows and annuity purchases) removed **3.71M participants** from PBGC protection in 2016-2023 (Table S-49). That is about 12% of the 29.8M insured in 2015 (my ratio).
   - The participant mix has aged:
     - Single-employer actives went from 77.6% of participants (1980) to 32.6% (2022).
     - Retirees went from 16.0% to 39.8%.
     - Separated vested went from 6.4% to 27.7%.
   - Multiemployer plans held steady at about 10.4-11.2M participants (2009-2025). Their active share fell from 75.9% (1980) to 34.4% (2022). [`output/pbgc_insured.csv`]

6. **State and local government DB coverage has barely moved.**
   - The BLS EBS put state and local DB participation at **93% (1987)** and 90% (1998). NCS gives **79% (2010) and 74-75% (2014-2026)**, with access steady at 83-86%. EBS and NCS are different surveys, so compare within each.
   - DC participation is 15-20% and is mostly a supplement: 81% participate in some retirement plan.
   - So DB is now mainly a public-sector benefit. **75% of state and local workers participate in a DB plan, against 9% of private workers** (NCS March 2026).
   - About half of state and local DB participants are in plans the NCS classes as "closed to new entrants, all participants still accrue": 60% (2014) and 50% (2026). Only 40-49% are in open plans, and there are almost no hard freezes.
     - I read this as tier changes: old tiers are closed and new hires go into a new, usually less generous tier. This is inference, not something BLS states.
     - The 2010-2011 values (91% open) are on an earlier classification and are not comparable. [`output/bls_ebs_ncs_db_dc.csv`, `output/bls_ncs_db_freeze.csv`]

7. **Households (SCF 1989-2022): DB coverage on a current job fell mostly before 2000 and has been flat since.** Here an "employee household" is one whose reference person works for someone else. The SCF includes government workers, so levels sit above the private-only figures. SE in brackets; bootstrap replicate weights plus imputation variance.

   | % with DB on a current job (head or spouse) | 1989 | 1995 | 2001 | 2007 | 2013 | 2019 | 2022 |
   |---|---|---|---|---|---|---|---|
   | Employee households, all ages | 42.0 (1.2) | 28.6 (1.0) | 27.6 (1.0) | 25.8 (1.0) | 22.8 (0.6) | 23.1 (0.7) | 25.3 (0.9) |
   | under 35 | 25.9 (1.7) | 16.2 (1.2) | 13.1 (1.2) | 12.4 (1.3) | 12.4 (1.0) | 13.8 (1.0) | 17.6 (1.6) |
   | 35-44 | 51.8 (2.0) | 29.5 (1.5) | 26.8 (1.6) | 23.3 (1.4) | 17.8 (1.2) | 22.8 (1.4) | 24.7 (1.6) |
   | 45-54 | 58.8 (2.4) | 38.4 (2.2) | 37.4 (1.6) | 33.0 (1.8) | 24.6 (1.3) | 24.4 (1.4) | 28.5 (2.1) |
   | 55-64 | 52.2 (3.4) | 42.6 (2.9) | 43.9 (2.4) | 40.0 (2.4) | 34.4 (1.8) | 30.8 (1.6) | 31.8 (2.2) |
   | **DC on a current job, all ages** | 38.1 (1.1) | 47.2 (0.9) | 50.8 (1.0) | 50.5 (0.9) | 48.1 (0.7) | 50.8 (0.8) | 53.0 (0.9) |

   - "DB only, no DC" on the current job fell from 24.3% to 11.1% of employee households (1989 to 2022). "DC only" rose from 20.4% to 38.8%.
   - The 2019-2022 uptick at younger ages is within about 2-3 SEs and may reflect the public-sector mix. Treat it as flat, not a reversal.
   - DB from a current job or expected from a past job, all households aged 55-64 (the next retirees): **52.7% (1989) to 35.3% (2022)**. This matches `spending/scf_income` t6: 52.7% to 37.2%, a slightly broader definition that adds households receiving a pension now.
   - [`output/scf_db_coverage_long.csv`]

8. **Retirees: DB income is shrinking slowly, because today's retirees earned their benefits decades ago.** These figures are reused from `spending/` and `cps/`, not recomputed.
   - CPS ASEC, persons 65+, DB pensions as a share of aggregate income:
     - **19.2% (1997 income) to 17.5% (2012)** on the traditional questions.
     - **16.6% (2018) to 13.7% (2025)** on updated processing, excluding interest credited inside retirement accounts.
     - The often-quoted "19.2% to 12.7%" spans a series break, so quote the two segments.
   - DB receipt at 65+: 25.6% on the redesigned questions to 24.7% (2026). At 65-69 it fell **22.9% (2019) to 18.3% (2026)**. At 80+ it is steady at about 28% (`cps/README.md` finding 5).
   - SCF, 65+ households: pensions/annuities were 10.0% of income in 2022, against 12.9-18.7% in 1989-2010. "DB only" households fell from 38.6% to 21.6%. "Receiving a pension now" stays at 44-52% (`spending/scf_income`).
   - The pipeline in findings 1-7 says receipt will keep falling as cohorts with 13-25% current-job DB coverage at ages 35-54 retire. That is an inference, not a projection anyone has published here.

## Method

- **DOL Form 5500.** `scripts/build_series.py` parses tables E1 (plans), E4 (participants) and E7 (active participants), columns "Total Plans: Total / DB / DC". The source is `../dc_stay/raw/hist.txt`, a pdftotext copy of `../dc_stay/raw/private-pension-plan-bulletin-historical-tables-and-graphs.pdf` (DOL EBSA, *Private Pension Plan Bulletin Historical Tables and Graphs 1975-2023*, Sep 2025 v1.0). Table E4 for 1980-1999 is parsed from `../dc_stay/raw/abstracts/abs1999.txt` (*Abstract of 1999 Form 5500 Annual Reports*). Both files were downloaded by the dc_stay thread; dol.gov is 403 from here.
- **Own extension of DOL Table E4.** DOL's 1980 DB total (21,861k + 8,239k = 30,100k) equals E7 active DB participants exactly, so DOL's measure is E7 active DB / private wage and salary workers.
  - Denominator: annual average of monthly, not seasonally adjusted, CPS series. LNU02032189 (employed, nonagricultural private wage and salary) + LNU02032184 (agricultural wage and salary) + LNU03032229 (unemployed, private nonag wage and salary). DOL's footnote says its denominator includes the unemployed.
  - My denominator is within -1.3% to +1.9% of DOL's (E&E vintages), and the ratio matches within 0.7 points in every year 1980-1999.
- **PBGC.** S-20, S-21, M-4, M-5 and S-3 come from the 2024 Pension Insurance Data Tables. S-22, S-23, S-26, S-27, M-6, S-44 and S-49 come from the 2023 tables, because the 2024 workbook and PDF leave them out even though its listing names them. S-23's denominator is CPS *employed* private wage and salary workers.
- **BLS.** EBS: `download.bls.gov/pub/time.series/eb/`, series `EBU{DBINC000000,DCINC000000,ALLRET00000}{ML,SM,SL,AP}`. NCS: `download.bls.gov/pub/time.series/nb/`, ownership 1/2/3, all industries/occupations, provisions 290-292 (DB access/participation/take-up), 312-314 (DC), 319-321 (any), 298/387/388/389/299 (open/frozen status, % of DB participants). The series list is in `raw/bls_nb_selected_series.csv`. NCS values are March of each year.
- **SCF.** `scripts/scf_db_coverage.py` uses the Fed summary extract flags DBPLANCJ, DCPLANCJ, DBPLANT and OCCAT1 (`../scf/raw/bulletin.macro.txt`). Point estimates pool the 5 implicates. SEs come from the 999 bootstrap replicate weights on implicate 1, plus 1.2 x the between-implicate variance, the same method as `scf/` and `spending/scf_income/`. Replicate files for 1989-2001 were fetched from federalreserve.gov into scratch, not stored here.
- Run: `python3 db_pensions/scripts/build_series.py` (seconds), then `python3 db_pensions/scripts/scf_db_coverage.py` (~10 min).

## Sources

- DOL EBSA, *Private Pension Plan Bulletin Historical Tables and Graphs 1975-2023* (Sep 2025), Tables E1, E4, E7: https://www.dol.gov/sites/dolgov/files/EBSA/researchers/statistics/retirement-bulletins/private-pension-plan-bulletin-historical-tables-and-graphs.pdf (copy in `../dc_stay/raw/`)
- DOL PWBA, *Abstract of 1999 Form 5500 Annual Reports*, Table E4 "Estimated Private Wage and Salary Worker Participation Rates Under DB and DC Plans, 1980-1999" (copy in `../dc_stay/raw/abstracts/abs1999.pdf`)
- PBGC, *Pension Insurance Data Tables* 2023 and 2024: https://www.pbgc.gov/sites/default/files/documents/2023-pension-data-tables.xlsx, https://www.pbgc.gov/sites/default/files/documents/2024-pension-data-tables.xlsx (+ .pdf), index https://www.pbgc.gov/prac/data-books (copies in `raw/`)
- BLS Employee Benefits Survey database: https://download.bls.gov/pub/time.series/eb/ (copies in `raw/eb.*`)
- BLS National Compensation Survey benefits database: https://download.bls.gov/pub/time.series/nb/. `nb.data.1.AllData` is 45MB and not kept; the extract is in `raw/bls_nb_selected_series_data.csv`.
- BLS CPS labor force statistics: https://download.bls.gov/pub/time.series/ln/ln.data.1.AllData (not kept; extract of 4 series in `raw/bls_ln_private_wage_salary.txt`)
- Federal Reserve, Survey of Consumer Finances 1989-2022 summary extracts (`../scf/raw/rscfpYYYY.dta`) and replicate weights: https://www.federalreserve.gov/econres/scfindex.htm
- Reused, not recomputed: `../spending/README.md`, `../spending/scf_income/output/t6_db_vs_dc_coverage.csv`, `../cps/README.md`.

## Caveats

- **Form 5500 counts are plan participations, not people.** A worker in two DB plans counts twice; this is rare for DB and common for DC. Because of this I do not headline the DC active share of wage and salary workers (71.7% in 2023, inflated by double counting and by definition changes).
- **Form 5500 definition changes** are listed in the DOL appendices:
  - 2005: active participants widened to include eligible non-contributors (mostly DC).
  - 2009-2013: small-plan 5500-SF filers counted everyone as active.
  - 2014: participation counting changed.
  - 2015: DB/DC classification revised.
  - 2017: multiple-employer plans split out.
  - The DB series are smooth across these, but read year-to-year moves loosely.
- **"Active" in Form 5500 and PBGC means currently employed by the sponsor, not accruing.** By 2022, 20.8% of PBGC single-employer actives were in hard-frozen plans that accrue nothing. So "8-9% of private workers in a DB plan" overstates the share still earning new DB benefits.
- **Three measures, three denominators.**
  - DOL: employed + unemployed private wage and salary workers.
  - PBGC: employed only.
  - NCS: private nonfarm establishment workers, excluding the self-employed.
  - NCS 2023 is 11% against 8.2-8.7% from administrative data. Read trends within each measure.
- **EBS 1979-1989 medium/large establishments** covered only firms above size cutoffs (50/100/250 workers by industry), excluded most service industries before 1988 and full-time workers only. So "84% in 1980" applies to that universe, not to all private workers.
- **NCS frozen-plan categories.**
  - Private "open" (78% in 2010 to 63% in 2026) is not continuous across 2013/2014: the breakdown changed.
  - Provisions 804/805 ("open/not open to new employees", 2014-2022) disagree with 298 in 2022 (37% vs 59% open) and are left out of the findings. They are kept in the CSV.
  - The state and local "closed" share is my reading of the "soft frozen, all still accrue" category.
- **SCF.**
  - DBPLANCJ also flags pensions "from the current job" that are being received. Before 2001 all such plans are assumed to be DB. This makes 65+ and non-worker estimates unusable: 65+ jumps from 2.5% in 1989 to 35-49% after 1995, a definitional effect. Only employee households and ages under 65 are reported, and the 1989/1992 levels should be treated cautiously.
  - Respondents may report cash-balance plans as DC. The SCF cannot separate private from public employers in the public file.
- **PBGC standard-termination rate** divides fiscal-year terminations by plan-year insured plan counts, so treat it as approximate.

## Dropped or unverifiable

- **"About 15%" as the current figure:** dropped. Every current source gives 8-11%. 15% matches about 2010.
- **NCS private DB participation 2007-2009:** not filled. The database series start in 2010 and the bls.gov PDF bulletins are blocked from here.
- **A DOL-published DB/DC wage-and-salary participation table after 1999:** none found in the 2000-2023 abstracts on disk. My extension replaces it.
- **Pension-risk-transfer dollar volumes (LIMRA):** industry source, not used. PBGC's participant counts are used instead.
- **SSA *Income of the Population 55+* DB receipt series:** ssa.gov is blocked. CPS figures from `cps/` are used instead.
