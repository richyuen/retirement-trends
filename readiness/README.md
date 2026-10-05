# Retirement readiness and coverage gaps

Who has a retirement account or a DB pension before retirement (SCF 1989-2022), how big near-retirees' accounts are relative to their income, what the best-known "at risk" index says (CRR National Retirement Risk Index), the case that the crisis is overstated, and what workers say about their own confidence (EBRI Retirement Confidence Survey, Fed SHED). Built 2026-10-05. SCF numbers are our own tabulations of the Fed's public files already in `../scf/raw/`; everything else is read from documents saved in `raw/`.

## Findings

1. **About a third of working-age households have no retirement account and no DB pension, and that share has hardly moved in 30 years.** Households with a head aged 25-64 that have any retirement account (IRA/Keogh or DC plan) or DB coverage: 64.9% (1989), 69.1% (2001, the peak), 63.2% (2019), 66.5% (2022, SE 0.8). Account ownership alone rose from 44.5% (1989) to 59.6% (2001) and has stayed at 55-59% since (59.1% in 2022, SE 0.8). DB coverage fell from 43.8% to 23.9% (2019), then 28.3% in 2022 (see caveats). So the shift from DB to DC changed the type of coverage much more than its reach. [`output/c1..c3_*_by_age.csv`]

   | Households, head 25-64 (%) | 1989 | 1995 | 2001 | 2007 | 2013 | 2019 | 2022 |
   |---|---|---|---|---|---|---|---|
   | Any retirement account | 44.5 | 52.7 | 59.6 | 58.5 | 54.7 | 54.9 | 59.1 |
   | DB plan (current job or vested from past job) | 43.8 | 36.2 | 30.6 | 28.1 | 25.5 | 23.9 | 28.3 |
   | Account or DB | 64.9 | 67.7 | 69.1 | 66.1 | 63.2 | 63.2 | 66.5 |
   | Neither | 35.1 | 32.3 | 30.9 | 33.9 | 36.8 | 36.8 | 33.5 |

2. **Near-retirees (55-64) have lost coverage since the mid-2000s.** Account or DB coverage was 71-77% from 1989 to 2007 (75.9% in 2004, SE 1.4) and fell to 66.3% in 2019 (SE 1.3) and 67.8% in 2022 (SE 1.6). Accounts alone peaked at 63.5% (2004) and were 57.0% in 2022 (SE 1.7). DB coverage at 55-64 fell from 52.7% (1989) to 35.3% (2022). This group's DB losses were no longer made up by new accounts.

3. **Near-retiree account balances are now about 1.3 times income for holders, up from about half in 1989. Across all 55-64 households, though, the typical balance is under a quarter of a year's income.** Median of each household's ratio of retirement-account balance to prior-year family income, head 55-64:
   - **Holders only**: 0.47 (1989), 0.89 (1998), 1.16 (2007), 1.24 (2019), 1.27 (2022, SE 0.13). Over 1989-2007 the rise is DC plans maturing. It has been flat since 2007.
   - **All households (non-holders count as 0)**: 0.00 (1989, when fewer than half had an account), 0.35 (2007), 0.13 (2019), 0.19 (2022, SE 0.06). The all-household median has *fallen* since 2007 because fewer 55-64 households hold an account.
   - **Share with balances of at least one year's income**: 12.8% (1989), 33.7% (2007), 30.2% (2019), 32.7% (2022, SE 1.6).
   - In dollars (2022 $, shown only for scale): median holder balance $185,000 in 2022 vs $55,000 in 1989; median family income for the group was $82,000 in 2022.
   [`output/n_*_5564.csv`]

4. **The gap by income is very large.** For near-retirees in the bottom income quartile, 15.6% held an account and 26.3% had an account or DB in 2022 (SE 3.0). The share with an account or DB *fell* from 35-47% in 1989-2007 to 20-29% in 2013-2022. Their median balance-to-income ratio is 0 in every wave. In the top quartile, 94.7% held an account in 2022, the median ratio across all households was 1.60 (SE 0.22), and 61.1% had at least a year's income saved (bottom quartile 7.4%).

   | Head 55-64, 2022 | Q1 (lowest) | Q2 | Q3 | Q4 (highest) |
   |---|---|---|---|---|
   | Any account (%) | 15.6 | 46.2 | 70.4 | 94.7 |
   | Account or DB (%) | 26.3 | 60.7 | 86.0 | 97.0 |
   | Median balance/income, all households | 0.00 | 0.00 | 0.69 | 1.60 |
   | Median balance/income, holders | 1.43* | 0.75 | 1.26 | 1.79 |
   | Balance at least 1x income (%) | 7.4 | 18.5 | 43.0 | 61.1 |

   \*Bottom-quartile holders are few (SE 0.46); don't read the holder ratio for Q1 as a level.
   Among all working-age households (25-64), account ownership was 20.6% in the bottom quartile and 90.8% in the top in 2022. In 2001 the shares were 22.4% and 88.6%, so the gap is about as wide as it was then. [`output/c5_*_2564_by_inc.csv`]

5. **The racial gap in ownership has not narrowed.** Head 25-64, any retirement account, 2022: White non-Hispanic 67.7% (SE 1.2), Black non-Hispanic 43.1% (2.6), Hispanic 29.5% (2.1). In 2004 the shares were 63.9%, 40.1% and 27.9%. The White-Black gap was 19-29 points in 2004-2022 and the White-Hispanic gap 30-38 points. Including DB coverage narrows the White-Black gap (74.3% vs 55.9% in 2022), so Black households more often have DB coverage without an account (we did not test why; public-sector employment is a plausible reason). It does not narrow the Hispanic gap (36.4%). Race is the SCF respondent's, in Fed categories. [`output/c5_*_by_race.csv`]

6. **CRR's National Retirement Risk Index: 39% of working-age households were "at risk" in 2022, the lowest since the Index began. Before that it was about half.** Version 2.0 series (IB 24-5, Feb 2024): 42% (2004), 41% (2007), 51% (2010), 51% (2013), 48% (2016), 47% (2019), 39% (2022). The original method went back to 1983, at 31% (1983), 30% (1989), 38% (2001) and 53% (2010) (IB 18-1). The vintages are not comparable, so they should not be spliced. [`output/p1_crr_nrri.csv`]
   - Of the 8-point drop from 2019 to 2022, CRR attributes 5.1 points to house prices (real home prices +22%), 1.6 to new pandemic saving and 1.0 to stock gains. Annuity rates contributed -0.2 and lower reverse-mortgage limits +0.5.
   - CRR calls 39% a lower bound: the Index assumes everyone takes a reverse mortgage, few people do, and house prices were about 14% above trend.
   - By group, 2019 -> 2022: renters 74 -> 72%, homeowners 34 -> 24%; no plan 68 -> 65%, DC only 42 -> 35%, DB 21 -> 13%; low-income third 71 -> 64%, high 32 -> 23%. [`output/p2_crr_nrri_subgroups.csv`]

7. **How the NRRI works** (IB 24-5, IB 23-10, IB 23-23):
   - **Projection.** For each SCF household aged 30-59, CRR projects retirement income at claiming ages of 62, 66 and 67 for the low-, middle- and high-income thirds. This counts Social Security (from estimated earnings histories), DB pensions (as reported), and all financial and 401(k)/IRA assets plus home equity (via a reverse mortgage), all converted into an inflation-indexed annuity. Assets at retirement come from the stable median wealth-to-income ratios by age in the 1983-2022 SCFs.
   - **Target.** Each household's target replacement rate comes from a consumption-smoothing model: the same consumption before and after retirement, allowing for lower taxes, no more saving, and paid-off mortgages.
   - **At risk.** A household is "at risk" if its projected replacement rate falls more than 10% below its target. The NRRI is the share of households at risk.
   - **Version 2.0 (2023)** added the varying claiming ages, projections from medians instead of means, cohort-specific DC accumulation, separate non-mortgage debt, and hundreds of target cells instead of 12. The headline stayed "roughly half" through 2019.

8. **The counter-view: the "crisis" depends on how the target is set and which income data are used.**
   - **Scholz, Seshadri & Khitatrakun (NBER WP 10260, 2004; JPE 2006).** They solve a life-cycle model for each HRS household in 1992 (born 1931-41) and find that "fewer than 20 percent of households have less wealth than their optimal targets." For those below target, the deficit "is generally small."
   - **Biggs & Schieber (National Affairs, Summer 2014).** Studies that find a crisis use a wage-indexed lifetime-earnings denominator, which for SSA's medium earner is 35% above final-five-year earnings. They also rely on CPS income data that miss most retirement-plan income. In 2008, SSA's CPS-based figures showed $228B from pensions and individual plans for Social Security beneficiaries, 40% of the $568B in IRS data. Of that, IRA withdrawals were $5.6B in the CPS figures vs $111B in IRS data. Their critique also covers CRR, which uses the wage-indexed denominator, and NIRS, which applies Fidelity's average-earner savings milestones to everyone.
   - **Administrative tax data (Brady & Bass, IRS SOI Joint Research Program paper, Dec 2024; authors are at the Investment Company Institute, a fund-industry association, not a recordkeeper).** Using 2016 tax data, median spendable income does not drop at retirement ages: it was $32,800 at age 70 vs $32,300 at 61. Also, 70%+ of people aged 71-91 receive DB/DC/IRA income directly or through a spouse, "much higher" than household surveys show.
   - **CRR's reply (Munnell, Rutledge & Webb, CRR WP 2014-16).**
     - The optimistic results rest on two assumptions: households accept consumption that declines in retirement, and they cut spending when children leave.
     - Applying those assumptions to the NRRI for people in their 50s in 2004 cuts the share at risk from 35% to 11.5%, close to Scholz-Seshadri's 8%. For 1992, the two approaches already agreed: 19% (NRRI) vs 16%.
     - CRR also argues that the wealth-to-income ratio by age has not risen even though people live longer, Social Security replacement is lower, and DB has shifted to DC.
   - **Bottom line for the report.** The two camps largely agree on the facts (coverage, balances). They disagree on the target (consumption smoothing vs optimal decline) and on how much home equity and unreported plan income to count. Both sides agree the shortfall is concentrated among low-income households and those without plans.

9. **Self-assessed confidence has swung with markets but sits at a level similar to the early 1990s.** In the EBRI/Greenwald RCS, the share of workers "very or somewhat confident" of having enough money to live comfortably in retirement was:
   - 73% in 1993, 70% in 2007, then a low of 49% in 2011 (51-55% in 2012-2014);
   - back to 72-73% in 2021-2022, then 64% (2023), 68% (2024), 67% (2025) and 61% (2026, the lowest since 2017);
   - "very confident" only: 13% (2009, 2011, 2013) to 29% (2021), and 21% in 2026.
   - Retirees are more confident: 73% in 2026, down from 78% in 2025 and 80% in 2021.
   - Workers with any plan (DC, IRA or DB) are about twice as likely to be confident as those without: 70% vs 32% in 2026.
   - The Fed's SHED (a federal source) gives a lower, steadier picture: 35% of non-retirees thought their retirement saving was on track in 2025. The range since 2017 was 31% (2022) to 40% (2021). By income: 7% (under $25k) vs 59% ($100k+). By race: White 43%, Black 23%, Hispanic 24%. [`output/p3_ebri_rcs_worker_confidence.csv`, `output/p4_fed_shed_on_track.csv`]

**Ties to the rest of the project.** The fall in 55-64 coverage (finding 2) and the low bottom-quartile ownership (finding 4) mean that the withdrawal behaviour studied in Sections 4-11 describes the roughly 57% of near-retiree households with an account. The other 43% will rely on Social Security (Section 18) and any DB pension. The tax-data critique (finding 8) is the same CPS under-reporting issue the project documents in Section 13 (`spending/`) and `cps/`.

## Method
- **Data**: Fed SCF summary extracts `rscfpYYYY.dta` for 1989-2022 (12 waves), read from `../scf/raw/`. Dollars are as the Fed publishes them in the extracts, i.e. 2022 dollars (checked by the scf/ thread). Unit: SCF "family" (household), classified by the reference person's age at interview.
- **Definitions** follow the Fed's `bulletin.macro.txt`:
  - account = `RETQLIQ > 0` (IRA/Keogh, DC on the current job, DC from past jobs, account plans already paying out);
  - DB = `DBPLANT = 1` (head or spouse/partner has a DB plan on a current job, or a pension from a past job to be received in the future);
  - DC on current job = `DCPLANCJ`;
  - income = `INCOME` (total family income in the calendar year before the survey);
  - race = `RACECL4`.
- **Balance-to-income**: `RETQLIQ / INCOME` for each household with positive income. We report the weighted median of these ratios (all households and holders only), the share with ratio of at least 1, and, as a check, the ratio of the median balance to the median income among holders (1.43 in 2022; `n_ratio_of_medians_holders_5564.csv`). Income quartiles are weighted cut points of `INCOME` within each age group and wave.
- **Estimation**: the 5 implicates are pooled with the extract's `WGT`. Standard errors (2004-2022 only) come from the 999 bootstrap replicate weights on implicate 1 plus 1.2 x the between-implicate variance. The helper functions are imported unchanged from `../scf/scripts/scf_analysis.py`. There are no SEs for 1989-2001 because replicate weights for those waves are not on disk.
- **Scripts**: `scripts/scf_readiness.py` -> `output/scf_readiness_long.csv` (every estimate, SE and household count; about 35 s). `scripts/scf_tables.py` -> wide `c*`/`n*` tables. `scripts/build_published.py` -> `p1-p4` CSVs typed from the saved source documents, each row naming its file.
- **Published series**: CRR values come from figure labels in the briefs. RCS values come from each year's Fact Sheet #1 headline text (2013, 2015-2026). For 1993-2011 and 2012-2014, the very and somewhat bar labels were summed, using the 2011, 2012 and 2014 fact sheets (checked against the rendered page images). SHED values come from the 2025 report's Figure 26 labels; the 2022-2025 values are confirmed by the text.

## Caveats
- **SCF coverage is a household measure**: one covered spouse covers the household. It is not the same as worker participation rates (BLS NCS, CPS), which are lower.
- **DB coverage in 2022 rose 4-5 points at ages 25-54.** Both components rose: current-job DB went from 20.3% to 22.9% and past-job pensions from 3.6% to 5.4% (all 25-64). We could not tell whether this is real (e.g., public-sector hiring) or a questionnaire effect. Treat 2019 -> 2022 DB and "account or DB" changes with care. Before 2001, current-job plans already paying benefits are all counted as DB (Fed note in `bulletin.macro.txt`).
- **DB coverage excludes DB pensions already in payment**, which matters for a few 55-64 households.
- **Balances exclude** DB values, Social Security wealth, home equity and other savings, so they understate total resources (the point of finding 8). Income is one year's total family income and can be unusual in any one year. Ratios for bottom-quartile holders and 55-64 race cells before 2010 rest on small samples (`n_hh_*` columns; e.g., Hispanic 55-64 had 20-31 households per wave before 2010). We report race only for 25-64 in the text.
- **NRRI**: the original, revised and Version 2.0 series differ by method and cannot be spliced. The 2022 drop is driven by house prices and assumes reverse mortgages. In IB 24-5, CRR also cites a Vanguard study (industry) finding at least 70% would fall short when housing is excluded. We have not opened that study, so it is not used as a finding.
- **RCS** is an industry-sponsored annual survey (EBRI/Greenwald) of about 1,000 workers and 1,000 retirees (2026: 1,007 workers, n shown in each fact sheet). Values from different vintages differ by up to 1 point (1993: 73% in the 2011 sheet, 74% in the 2026 chart), and our 1993-2014 sums of rounded parts can be off by 1. Years 1994-1995, 1997-2000 are not in the files we opened, so they are left out rather than read from an unlabeled chart line. We did not check survey-mode changes.
- **SHED** asks non-retirees an unprompted "on track" question; it is not comparable in level with the RCS.
- **Counter-view sources** are an NBER working paper (the 2006 JPE version was not opened), a policy-magazine article, and an IRS SOI joint-research paper by ICI authors. The SSA and CBO replacement-rate work could not be reached (ssa.gov, cbo.gov blocked), so it is not used.

## Sources
- Federal Reserve Board, Survey of Consumer Finances public data and summary extracts 1989-2022: `https://www.federalreserve.gov/econres/scfindex.htm` (files in `../scf/raw/`; definitions in `../scf/raw/bulletin.macro.txt`).
- Yin, Chen & Munnell, "The National Retirement Risk Index: An Update from the 2022 SCF," CRR IB 24-5, Feb 2024: `https://crr.bc.edu/wp-content/uploads/2024/02/IB_24-5.pdf`
- Yin, Chen & Munnell, "The National Retirement Risk Index: Version 2.0," CRR IB 23-10, May 2023: `https://crr.bc.edu/wp-content/uploads/2023/05/IB_23-10_.pdf`
- Yin, Chen & Munnell, "The National Retirement Risk Index with Varying Claiming Ages," CRR IB 23-23, Nov 2023: `https://crr.bc.edu/wp-content/uploads/2023/11/IB_23-23.pdf`
- Munnell, Hou & Sanzenbacher, "National Retirement Risk Index Shows Modest Improvement in 2016," CRR IB 18-1, Jan 2018: `https://crr.bc.edu/wp-content/uploads/2018/01/IB_18-1.pdf`
- Munnell, Chen & Siliciano, "The National Retirement Risk Index: An Update from the 2019 SCF," CRR IB 21-2, Jan 2021: `https://crr.bc.edu/wp-content/uploads/2021/01/IB_21-2.pdf`
- Munnell, Rutledge & Webb, "Are Retirees Falling Short? Reconciling the Conflicting Evidence," CRR WP 2014-16: `https://crr.bc.edu/wp-content/uploads/2014/11/wp_2014-16.pdf`
- Scholz, Seshadri & Khitatrakun, "Are Americans Saving 'Optimally' for Retirement?" NBER WP 10260, Jan 2004: `https://www.nber.org/system/files/working_papers/w10260/w10260.pdf` (published in the Journal of Political Economy, 2006)
- Biggs & Schieber, "Is There a Retirement Crisis?" National Affairs, Summer 2014: `https://www.nationalaffairs.com/publications/detail/is-there-a-retirement-crisis` (saved html + txt)
- Brady & Bass, "A Day in the Life Cycle: Using Tax Data to Measure Changes in Income by Age," IRS SOI, Dec 2024 draft: `https://www.irs.gov/pub/irs-soi/24rpchangesincomebyage.pdf`
- EBRI/Greenwald Research, Retirement Confidence Survey Fact Sheet #1, 2011-2026: index at `https://www.ebri.org/retirement/retirement-confidence-survey` (yearly pages `.../YYYY-survey-results`); 2026: `https://www.ebri.org/docs/default-source/rcs/2026-rcs/rcs_26-fs-1_confid.pdf`
- Federal Reserve Board, Economic Well-Being of U.S. Households in 2025 (May 2026): `https://www.federalreserve.gov/publications/files/2025-report-economic-well-being-us-households-202605.pdf` (Figure 26, Tables 28-29)

## Files
- `scripts/scf_readiness.py`, `scripts/scf_tables.py`, `scripts/build_published.py`
- `output/scf_readiness_long.csv` (all SCF estimates, SEs, n); `c1-c4` coverage by age; `c5_*` coverage by race and income quartile (25-64 and 55-64); `n_*_5564.csv` near-retiree balances and ratios by income quartile; `p1-p4` published series (NRRI, NRRI subgroups, RCS, SHED)
- `raw/crr/`, `raw/ebri/`, `raw/fed/`, `raw/other/` source PDFs with `pdftotext` extracts
