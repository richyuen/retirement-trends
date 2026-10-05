# Health care costs in retirement

Out-of-pocket (OOP) health spending for people 65+ in MEPS 1996-2024: its level, its share of income, and how concentrated it is. Also the Medicare Part B premium against the average Social Security benefit (1980-2026, projected to 2035), IRMAA reach, total health spending per person 65+ (CMS NHE 2002-2020), and public alternatives to Fidelity's lifetime estimate. Built 2026-10-05. This builds on `spending/README.md`, which found that health care is a flat 12-14% of 65+ spending in the CE, while insurance premiums grew from 42% to about 66-70% of that health spending. Nothing here repeats the CE.

## Findings

1. **Typical OOP spending on care (premiums excluded) is lower in real terms than in 1996, and much lower than at its 2004 peak. The burden is now concentrated in a minority.** MEPS, people 65+, 2024 dollars (CPI-U):

   | | 1996 | 2004 | 2010 | 2019 | 2024 |
   |---|---|---|---|---|---|
   | Mean OOP per person | $1,639 | $2,584 | $1,681 | $1,965 | $1,958 |
   | Median OOP | $838 | $1,513 | $928 | $746 | $644 |
   | OOP as % of all their care spending | 16.7% | 18.7% | 11.8% | 12.3% | 12.4% |
   | Top 10% of 65+ spenders' share of all 65+ OOP | 45.7% | 40.7% | 44.4% | 55.3% | 57.7% |
   | Aggregate OOP / aggregate personal income of 65+ | 4.8% | 6.7% | 3.9% | 3.9% | 3.9% |
   | Share of 65+ in families with OOP > 10% of family income | 18.1% | 29.8% | 16.8% | 14.3% | 13.3% |
   | ... > 20% of family income | 7.7% | 13.9% | 7.3% | 6.9% | 6.6% |

   - OOP rose through 2004 and dropped when Medicare Part D began in 2006. The share of 65+ with OOP above 10% of family income fell from 27.3% (2005) to 22.7% (2006) and 19.2% (2007).
   - The median kept falling after 2010 while the mean recovered, so the burden became more skewed. The top 10% of spenders paid 40-46% of all 65+ OOP in 1996-2010 and 55-59% in 2019-2024. The top half paid 94.9% in 2024.
   - The share of people 65+ with no OOP at all rose from about 4-5% (2001-2006) to 9.4% (2024).
   - Sampling error is small. For example, SE of the >10% share is 0.6-1.1 points and SE of the aggregate income share is 0.1-0.3 points.
   - Even now, people 65+ face a high family burden about twice as often as people under 65 (13.3% vs 6.2% above 10% in 2024).

   [`output/meps_oop_65plus.csv`, `output/meps_oop_by_age.csv`]

2. **Premiums are the part that grew, and MEPS leaves them out.** The Part B standard premium grew 2.8% a year in real terms from 1990 to 2025. Over the same years the average Social Security retired-worker benefit grew 1.2% a year (3.2% vs 1.3% for 2000-2025).

   | % of average OASI retired-worker benefit | 1985 | 1995 | 2005 | 2010 | 2020 | 2025 | 2026 | 2035 (proj.) |
   |---|---|---|---|---|---|---|---|---|
   | Part B standard premium | 3.7% | 7.1% | 8.6% | 10.0% | 9.9% | 9.5% | 10.1% | n/a |
   | Avg Part B + D premiums | 3.6% | 7.1% | 8.6% | 12.6% | 12.1% | 10.7% | 11.5% | 16.1% |
   | Avg Part B + D premiums + cost sharing | 8.6% | 15.5% | 18.5% | 28.7% | 26.4% | 25.8% | 26.6% | 32.4% |

   - The Trustees' own text says B+D premiums are "about 12 percent" of the average benefit in 2026 and premiums plus cost sharing "about 27 percent", rising to about 21% and 41% by 2100.
   - The premium share roughly doubled between 1990 and 2010 and has been flat at about 9.5-10.5% since.
   - Average SMI (Part B+D) benefits were 8% of the average Social Security benefit in 1970, 35% in 2005 and 56% in 2026, and are projected at 70% in 2035.
   - Behind the premium increases: the premium is pegged to about 25% of Part B cost (Table III.C2), and the 2006 Part D launch added a premium.
   - Hold-harmless years: most enrollees paid less than the standard premium in 2010-2011 (held at $96.40) and 2016-2017 (held at $104.90, then about +$4), so the standard-premium share overstates what most people paid in those years. [Medicare Trustees Report 2026, Tables III.C2, V.E2 and Figure II.F2 data; `output/medicare_partb_vs_ss.csv`]

3. **IRMAA (income-related Part B premium) reaches a growing minority.**
   - The share of Part B enrollees paying it was 4.3% in 2010 and 5.7% in 2015. It was 8.0% in 2025 (5.1M people, $14.1B above the standard premium) and is estimated at 9.4% in 2026 (6.1M, $18.8B).
   - The intermediate projection is 10.8% by 2029.
   - The thresholds ($109k single / $218k joint in 2026) were frozen in 2011-2019 and are indexed after that.
   - Payer counts are from Table V.E3 and enrollment from Table V.B3. The 2026 enrollment is a Trustees estimate.

   [`output/medicare_irmaa.csv`]

4. **Total health spending per person 65+ is about 2.4 times that of working-age adults, and Medicare pays half of it.** CMS NHE personal health care, people 65+:
   - Per person: $13,406 (2002) and $22,356 (2020) nominal, or $23,376 and $27,096 in 2024 dollars. Real growth was 0.8% a year (0.56% a year for 2002-2018, before COVID).
   - The 65+ share of all personal health care spending was 34.6% (2002) and 36.9% (2020). CMS's 2020 highlights give the 65+ share of the population as 17%.
   - Ratio of per-person spending to ages 19-64: 3.3 (2002), 2.4 (2020).
   - Payer mix for 65+ in 2020: Medicare 50.2% (46.7% in 2002, before Part D), OOP 13.2% (17.1% in 2002).
   - NHE OOP per person 65+ fell from $3,996 to $3,588 (2024 dollars, 2002 to 2020).
   - Nursing homes are 24-30% of 65+ OOP in NHE. That is a main reason NHE OOP is about twice MEPS OOP, since MEPS excludes institutions and undercounts.
   - The NHE age tables stop at 2020 (released 2023).

   [`output/nhe_65plus.csv`]

5. **Measures that include premiums and long-term care show a much larger burden than MEPS. These are KFF analyses of CMS MCBS data (non-profit, not a recordkeeper):**
   - 2022, all Medicare beneficiaries incl. Medicare Advantage and facility residents: average OOP including premiums was $6,330. That is 11% of average per-capita total income and 39% of per-capita Social Security income. One in 4 spent at least 21% of income, and 1 in 10 at least 39%. The burden is 22% at 85+ vs 9% at 65-74, and 34% for incomes of $10k or less vs 7% above $50k (KFF, Aug 2025).
   - 2016, traditional Medicare only: average $5,460. Premiums were 42% of it and services 58%. Long-term care facilities were the largest service item ($1,014). The median beneficiary spent 12% of income, and the top quarter at least 23% (KFF, Nov 2019).
   - 2000-2010, traditional Medicare: total OOP grew 3.7% a year, with premiums at 5.8% a year vs services at 2.4%. Growth slowed after Part D (5.0% a year 2000-06, 1.8% 2006-10). The 2010 premium share was 42%, the mean $4,734, and the top 10% averaged $19,236 (KFF chartbook, 2014).

6. **Lifetime cost: public and non-recordkeeper alternatives to the Fidelity number.**

   | Source | Type | What it covers | Estimate |
   |---|---|---|---|
   | Jones, De Nardi, French, McGee & Kirschner, Richmond Fed *Economic Quarterly* 2018 (NBER w24599) | Academic, Federal Reserve; HRS + MCBS | OOP + Medicaid-paid spending incl. nursing homes and insurance premiums; households age 70 (cohort turning 70 in 1992); 2014 dollars; PV at 3% real | Mean over $122,000. Top 5% above $330,000, top 1% above $640,000. Couples at median income in good health: about $150,000 (top 5% above $380,000). OOP alone is about 20% below the OOP+Medicaid total. Medicaid covers 57% of lifetime costs at the bottom of the income distribution and 21% at the top. |
   | EBRI Issue Brief, Mar 2026 (2025 costs) | Non-profit research institute (not a recordkeeper); simulation | Savings at 65 for premiums (Medigap or MA, Part D) + drug costs; **excludes long-term care, dental, vision** | Medigap couple: $267k (50% chance) / $405k (90%). MA couple: $135k / $203k. Single man Medigap $120k / $212k, woman $146k / $252k. High-drug-cost couple $469k (90%). |
   | Fidelity Retiree Health Care Cost Estimate, Jul 2026 | **Recordkeeper estimate (private)** | One 65-year-old, Original Medicare + Part D, no employer coverage; **excludes long-term care, OTC, most dental** | $185,500 per person (up 7.5% from 2025). 45% is Part B+D premiums, 48% other medical costs, 7% drugs. The 2026 release gives no couple figure. |

   Read across the sources: Fidelity and EBRI are savings targets for premiums and Medicare cost sharing only. Jones et al. is a distribution of realized spending that includes nursing homes. In all three, the tail risk (nursing homes, long lives) is several times the mean.

7. **How this connects to the existing report.**
   - S13: the CE health share is flat because falling OOP on care (finding 1) offsets rising premiums (finding 2). This matches CE's premium share rising to 66-70%. In KFF/MCBS, premiums were 42% of beneficiaries' total OOP in both 2010 and 2016.
   - S14 (longevity): costs rise steeply with age. MEPS mean OOP in 2019 was $1,681 at 65-74 and $3,277 at 85+ (2024 dollars). Jones et al. find that a household still alive at 90 will on average spend more than $113,000 more.
   - S4-S10: withdrawals in the oldest groups partly fund this.

## Method

- **MEPS-HC** (AHRQ), Full Year Consolidated files 1996-2024 (HC-012 to HC-256), civilian non-institutionalized population.
  - Variables used:
    - OOP = `TOTSLF` (payments by self/family for all care in the year)
    - total = `TOTEXP`
    - weight `PERWT{yy}F` (1996: `WTDPER96`)
    - age = `AGE{yy}X` (end of year, falling back to `AGELAST`)
    - person income `TTLP{yy}X` (1996-97: `TTLPNX`)
    - design vars `VARSTR`/`VARPSU` (within-year)
  - Family burden = summed OOP of the CPS-defined family (`DUID` × `CPSFAMID`) ÷ family income.
    - Family income is `FAMINC{yy}` where it exists (2007+), and the sum of members' `TTLP` before that. Where both exist, they agree for 96-98% of persons.
    - Persons whose family has income ≤ 0 and any OOP count as high-burden, following the usual MEPS burden convention.
  - "Aggregate OOP / aggregate personal income" is the ratio of weighted totals for people 65+.
  - Top-share = share of weighted OOP held by the top x% of people 65+ ranked by OOP.
  - SEs are Taylor linearization with the within-year strata/PSU (means and ratios only; no SEs for percentiles or top shares).
  - Dollars are converted to 2024 dollars with CPI-U annual averages (BLS `CUUR0000SA0`).
  - Validation: the pipeline reproduces MEPS Statistical Brief #126 (2003) exactly for all persons with expenses: mean OOP $707, median $254, 19.4% above $1,000, 8.4% above $2,000. For 65+ it gives $1,563 vs the brief's $1,547, probably a different age variable.
- **Medicare Trustees Report 2026** (CMS):
  - Part B standard premium from Table III.C2 and V.E2.
  - Average OASI retired-worker benefit, average B+D premium, premium + cost sharing and average SMI benefit (monthly, constant dollars) from the Figure II.F2 data sheet in the "expanded and supplementary tables and figures" zip.
  - That sheet's title says "constant 2024 dollars", but the report text says 2025. For 1985-2005 (Part B only), the implied deflator matches CPI-U with a 2025 base within 1.4%, so 2025 it is.
  - The nominal Part B premium is put into the same 2025 dollars with CPI-U. For 2026 that uses the mean of Jan-Aug 2026, which has a small effect.
  - IRMAA share = Table V.E3 payers ÷ Table V.B3 Part B enrollment.
- **CMS NHE by age and sex** (2002-2020, released 2023): payer × service × age aggregates and per-capita tables. Population 65+ is implied as aggregate ÷ per-capita.

Rebuild (from `health_costs/`):

```
MEPS_CACHE=/tmp/meps_cache sh scripts/fetch_meps.sh               # ~330MB of zips, kept outside the project
MEPS_CACHE=/tmp/meps_cache python3 scripts/extract_meps.py         # -> raw/meps_slim/ (20MB, slim person files)
python3 scripts/meps_analysis.py                                    # -> output/meps_oop_65plus.csv, meps_oop_by_age.csv
python3 scripts/medicare_premiums.py                                # -> output/medicare_partb_vs_ss.csv, medicare_irmaa.csv
python3 scripts/nhe_age.py                                          # -> output/nhe_65plus.csv
```

Needs pandas, numpy, pyreadstat, openpyxl.

## Sources (all opened; copies in `raw/`)

- MEPS-HC FYC files: `https://meps.ahrq.gov/mepsweb/data_files/pufs/h{NN}ssp.zip` (1996-2016) and `.../pufs/h{NNN}/h{NNN}dta.zip` (2017-2024). The file list is at https://meps.ahrq.gov/data_stats/download_data_files.jsp. Not stored (about 330MB in total); slim extracts are in `raw/meps_slim/`.
- MEPS Statistical Brief #126 (2003 OOP), https://meps.ahrq.gov/data_files/publications/st126/stat126.shtml (`raw/meps_docs/stat126.html`).
- MEPS 2018 FYC documentation (HC-209), on the redesign break: https://meps.ahrq.gov/data_stats/download_data/pufs/h209/h209doc.shtml (`raw/meps_docs/`).
- 2026 Medicare Trustees Report: https://www.cms.gov/oact/tr/2026 (PDF), pp. 40-41, 83-84, 189-190, 207-209 (`raw/medicare_trustees/tr2026.pdf`, text excerpts in `tr2026_table_excerpts.txt`).
- Trustees expanded tables and figures: https://www.cms.gov/files/zip/2026-expanded-supplementary-tables-figures.zip
- CMS NHE by age and sex: https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/age-and-sex (CSV zip, tables zip, highlights PDF, methodology PDF in `raw/nhe_age/`).
- BLS CPI-U: https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems (`raw/bls/`).
- KFF, "Health Costs Consume a Large Portion of Income for Millions of People with Medicare" (Ochieng, Cubanski, Neuman, Damico, Aug 21 2025): https://www.kff.org/medicare/health-costs-consume-a-large-portion-of-income-for-millions-of-people-with-medicare/
- KFF, "How Much Do Medicare Beneficiaries Spend Out of Pocket on Health Care?" (Cubanski et al., Nov 4 2019): https://www.kff.org/medicare/issue-brief/how-much-do-medicare-beneficiaries-spend-out-of-pocket-on-health-care/
- KFF, "How Much Is Enough? Out-of-Pocket Spending Among Medicare Beneficiaries: A Chartbook" (Jul 2014): https://files.kff.org/attachment/how-much-is-enough-out-of-pocket-spending-among-medicare-beneficiaries-a-chartbook-report
- Jones, De Nardi, French, McGee, Kirschner, "The Lifetime Medical Spending of Retirees," Richmond Fed *Economic Quarterly* 104(3), 2018: https://www.richmondfed.org/-/media/RichmondFedOrg/publications/research/economic_quarterly/2018/q3/jones.pdf
- EBRI Issue Brief, "Projected Savings Medicare Beneficiaries Need for Health Expenses in Retirement up Again in 2025" (Spiegel & Fronstin, Mar 5 2026), summary page https://www.ebri.org/content/projected-savings-medicare-beneficiaries-need-for-health-expenses-in-retirement-up-again-in-2025 and press release (Mar 11 2026). Figures are from EBRI's own summary and press release, which agree; the 16-page PDF was not downloaded.
- Fidelity 2026 Retiree Health Care Cost Estimate, press release dated Jul 21 2026, read from Fidelity's own alumni newsroom: https://alumni.fidelity.com/news/11553433

## Caveats

- **What OOP means differs by source.** MEPS `TOTSLF` excludes all premiums and institutional (nursing-home) residents. KFF/MCBS includes premiums and facility residents. NHE includes nursing homes but not premiums. Jones et al. (HRS) include premiums and nursing homes. Don't compare levels across sources; compare trends within one.
- **MEPS breaks:**
  - 2018 is the first year fully on the redesigned CAPI instrument. AHRQ warns of possible effects on trend analysis. Mean OOP 65+ jumps from $1,733 (2017) to $1,959 (2018), and under-65 rises similarly, so treat 1996-2017 and 2018-2024 as separate eras for levels.
  - The 2020-21 COVID years have lower response.
  - MEPS undercounts spending compared with NHE (CMS publishes a MEPS-NHE reconciliation; not used here).
- **Medicare premium shares** use the average OASI retired-worker benefit, which the Trustees chose. Individuals vary, and most beneficiaries have other income (the Trustees say similar conclusions hold for total income). The standard premium overstates what most paid in hold-harmless years (2010-11, 2016-17). The 1980 Part B premium is for the 12 months ending June 1980.
- **NHE by age** is every two years, ends in 2020, and 2020 includes COVID provider relief funds allocated by payer.
- **Recordkeeper vs public.** Fidelity is a recordkeeper estimate, shown only for comparison. EBRI is a non-profit research institute whose members include financial firms. Jones et al. and the CMS/AHRQ data are public or academic. Fidelity's earlier "$300k+ per couple" figure is not in the 2026 release (individual only) and was not verified here.

## Dropped or not reachable

- **ssa.gov average-benefit tables (blocked).** Replaced by the Trustees' Figure II.F2 average OASI benefit series, which is the same concept and comes from the official CMS file.
- **MCBS microdata directly (data.cms.gov PUF).** Not analyzed; MCBS results are taken from KFF's published analyses.
- **MEPS interactive summary tables (meps.ahrq.gov/mepstrends returns 401).** Microdata used instead.
- **EBRI full PDF.** Not opened; the figures come from EBRI's summary and press release, which agree.
- **The search-snippet figure "Medigap couple $366,000 at 90%".** Dropped: EBRI's own 2026 pages say $405,000. Where $366,000 comes from was not checked.
- **The KFF 2018 projection report URL.** It redirected to the 2025 page; that report was not used.
