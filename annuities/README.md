# Annuities and lifetime income

How many older households own annuities and whether that is changing, how often retirement balances are turned into lifetime income (the "annuity puzzle"), what the stock and sales of annuities look like, and what the SECURE Acts changed. Built 2026-10-05.

The core numbers come from public sources: the Fed's SCF microdata (our tabulation), CPS ASEC (from the cps/ thread's output), the Fed Financial Accounts (Z.1), BLS NCS plan provisions, EBRI, CRR, and statute and regulation text. Four sources are flagged where they are used:
- TIAA administrative data (recordkeeper data, via an NBER/SSA paper).
- A GAO citation of an industry survey.
- LIMRA sales figures relayed by the trade press (industry).
- FRTIB board minutes for the TSP.

**Overall: data on who annuitizes is thin. Ownership is solid; actual annuitization choices are weak.**

## Findings

1. **Few older households hold annuities, and the share is falling.** SCF, households by age of the reference person, 2004-2022 (consistent questions; SEs from 999 bootstrap replicates plus implicate variance):

   | % of households | 2004 | 2007 | 2010 | 2013 | 2016 | 2019 | 2022 |
   |---|---|---|---|---|---|---|---|
   | 65+, any annuity (income or assets, excl. job pensions) | **16.1** (SE 1.2) | 14.5 | 13.2 | 10.9 | 13.3 | 12.2 | **11.4** (SE 0.7) |
   | 65+, cash-value (deferred-type) annuity | 13.2 | 11.2 | 10.8 | 8.7 | 10.2 | 9.0 | 8.4 |
   | 65+, non-cashable (income-type) annuity | 3.8 | 3.5 | 3.3 | 3.0 | 3.5 | 3.4 | 3.6 |
   | 65+, received annuity income last year | 9.8 | 8.8 | 8.0 | 6.7 | 8.7 | 8.3 | 7.2 |
   | 55-64, any annuity | **10.1** (SE 1.0) | 7.1 | 8.0 | 6.4 | 6.3 | 5.9 | **6.5** (SE 0.9) |

   - The fall from 2004 to 2022 is statistically clear:
     - 65+: -4.8 points, z about 3.5.
     - 55-64: -3.7 points, z about 2.7.
   - The fall is almost all in **cash-value (accumulation) annuities**.
   - **Income-type annuities, the kind that insure longevity, are flat at about 3-4% of 65+ households.** At 55-64 they are 1.3-2.4%.
   - Among all households, any-annuity ownership fell from 7.2% to 4.8%.
   - [`output/scf_annuity_ownership_by_age.csv`, `scf_annuity_ownership_se.csv`]

2. **Households that do own annuities hold a sizeable share of their savings in them. In aggregate, annuities are a small slice of older households' wealth.**
   - Among 65+ holders, the median cash value was about **$93k-$134k (2022 $) in 2007-2022** ($100,000 in 2022).
   - That is a median **22-30% of the holder's financial assets** in 2010-2022 (22.6% in 2022).
   - Across all 65+ households, cash-value annuities were 3.4-4.9% of financial assets in 2004-2016, then 2.9% (2019) and **1.6% (2022)**. The 2022 figure is partly a denominator effect, since financial assets rose.
   - The share of 65+ holders who bought their annuity with a payout from a past-job pension rose:
     - 26% (2004) to 34-45% (2007-2019), and 38% (2022).
     - Each wave has only about 150-200 holder households (152 in 2004, 180 in 2010), so read this as a direction rather than a precise trend.

3. **The person-level survey agrees: about 6% of people 65+ receive annuity income, flat since 2019.**
   - CPS ASEC, updated processing:

     | ASEC year | 65+ | 60-64 |
     |---|---|---|
     | 2019 | 6.6% | 1.2-1.5% (2019-2026) |
     | 2022 | 6.0% | |
     | 2026 | 6.2% | |

   - Among 75-79s, 6.2-8.9% received annuity income in 2019-2026.
   - Do not compare with years before 2014. The redesign raised the 65+ figure from 0.38% to 4.84% within ASEC 2014 (cps/README breaks).
   - The SCF household figure (7.2%, 2022) and the CPS person figure (6.0%) are consistent.
   - [`output/cps_pct_receiving_annuity_income.csv`]

4. **The "annuity puzzle": when a lump sum is allowed, most people take it.** Evidence, strongest first:
   - **DB plans (EBRI Issue Brief 381, Banerjee 2013; plan administrative records, 2005-2010; not nationally representative):**
     - Annuitization was **98.8%** in plans with no lump-sum option (2010).
     - It was **44.3%** in traditional DB plans with unrestricted lump sums, and **22.3%** in cash-balance plans with unrestricted lump sums.
     - Pooled 2005-2010, workers aged 50-75 with 5+ years' tenure and $5,000+ annuitized at 65.8%, but only **27.3%** where lump sums were unrestricted.
     - Plan rules, not preferences alone, drive the rate.
   - **How common lump sums are in DB plans (BLS NCS, private industry):** 34% (2014), 36% (2017), 23% (2019) and 36% (2022) of traditional DB participants had a lump-sum option. The 2019 dip looks like sampling noise.
   - **DC plans rarely offer an annuity:**
     - BLS NCS: **22% (2014), 12% (2017), 14% (2019), 11% (2022)** of savings-and-thrift (401(k)-type) participants had an annuity distribution option. Compare 89% with lump sum and 43% with installments in 2022.
     - GAO-26-107536 (March 2026) cites an industry survey: "nearly 7 percent" of 401(k)/profit-sharing **plans** offered an in-plan annuity in 2023, and about 17% were considering one.
     - The NCS figure counts participants and the GAO figure counts plans, so the two do not conflict.
     - Neither shows growth since the SECURE Act.
   - **When DC money can be annuitized, take-up has fallen [TIAA administrative data, recordkeeper; NBER RDRC NB19-10, Brown, Poterba & Richardson 2019]:**
     - TIAA's DC participants once had to annuitize.
     - The share of first-time income claimants choosing a life annuity fell from **54% (2000) to 19% (2017)**.
     - Over the same period, the share taking only RMDs rose from **9% to 58%**.
     - Among those first claiming income after 70, annuitization fell from 37% to **6%**.
     - The authors' linear probability model attributes most of the 35-point drop to two factors: lower interest rates ("a decline of about 19 percent" in the probability of annuitizing) and later first claims ("another 14 percent").
   - **Older HRS evidence (secondary, cited in CRR WP 2015-9):**
     - Only 7% of HRS respondents who retired from a DC plan converted it to an annuity (Hurd & Panis 2006).
     - Under 8% of Americans 70+ received private annuity income in 2006 (Pashchenko 2010).
     - We did not open the originals.
   - **TSP (FRTIB board minutes, Sept 2024):**
     - Participants put "about 175 million dollars towards annuities" in Jan-Aug 2024, "almost equal to the total purchased last year".
     - Staff added that "not many TSP participants purchase annuities".

5. **The puzzle is smaller once Social Security and DB pensions are counted.** Bosworth, Burtless & Alalouf (CRR WP 2015-9; CPS and SCF, 1982-2009) find:
   - About **two-thirds** of the income of families headed by someone 62+ is annuitized (Social Security, pensions, annuities).
   - The share was not lower in 2009 than in earlier survey years. That is "little evidence" that the DB-to-DC shift had yet cut annuitized income.
   - In the bottom quintile it is 81% (CPS) to 88% (SCF).
   - So the people with little annuitized income are mainly higher-income families with large DC/IRA balances.

6. **Annuity reserves are large in dollars and steady as a share of wealth. Their share of IRAs has halved. [Fed Z.1, Sept 2026 release]**
   - Life insurers' annuity reserves (individual and allocated group, deferred and payout, incl. variable separate accounts and IRA annuities) were **$4.83 trillion at end-2025**. That compares with $1.38T in 2000 and $2.32T in 2010.
   - As a share of household financial assets: 4.0-4.3% (2000-2010), drifting down to **3.4% (2025)**.
   - As a share of all pension entitlements (DB, DC and annuities): about 12-14%, slightly rising.
   - **IRA assets held as annuities at life insurers fell from 11.1% of all IRA assets (2005) to 5.0% (2025)** ($927B of $18.7T). IRA money has moved into funds faster than into annuities.
   - Net inflows to annuity reserves were $108-132B a year in 2022-2024 (2.6-3.1% of reserves) but only $12B in 2025. The flows are volatile; see caveats.
   - [`output/z1_annuity_reserves.csv`]

7. **Sales are at records, but almost all of it is accumulation products, not lifetime income. [LIMRA, industry]**
   - 2025 individual annuity sales were **$461.3B**, a record (LIMRA survey via PlanAdviser, Feb 12 2026).
   - Mix:

     | Product | Share of 2025 sales |
     |---|---|
     | Fixed-rate deferred | 34.8% |
     | Fixed indexed | 27.8% |
     | RILA | 17.3% |
     | Traditional variable | 14.1% |
     | Single-premium immediate (SPIA) | 3.0% ($14.0B) |
     | Deferred income (DIA) | 1.0% ($4.8B) |
     | Not itemised | 1.9% |

   - **Income annuities are about 4% of sales.** High sales therefore do not mean more annuitization. They fit the SCF picture (finding 1): cash-value annuities are a savings vehicle, while income annuities are a flat ~3-4% niche.
   - [`output/limra_2025_sales_mix_INDUSTRY.csv`]

8. **Policy: SECURE (2019) and SECURE 2.0 (2022) lowered the barriers. There is little evidence yet of effects.** [`output/policy_lifetime_income_timeline.csv`]
   - **Safe harbor for choosing an insurer** (SECURE Sec. 204, ERISA 404(e)). In 2025 DOL removed the older 2008 regulatory safe harbor as unnecessary.
     - Evidence: in-plan annuities are still offered by about 7% of plans (2023, industry survey via GAO), and 11% of 401(k)-type participants had an annuity option in the 2022 NCS (14% in 2019).
     - **No measurable increase.**
   - **Lifetime income illustration** (SECURE Sec. 203; DOL interim final rule 85 FR 59132, applicable Sept 18 2021).
     - At least once every 12 months, statements must show the balance as a single-life and a joint-and-survivor monthly annuity.
     - The illustration assumes age 67 and the 10-year Treasury rate.
     - **We found no study of its effect on annuity purchases** (searched CRR, NBER, EBRI). The rule is still an interim final rule.
   - **Portability of in-plan lifetime income** (SECURE Sec. 109): no data on use.
   - **QLAC limits:**
     - 2014 regulations: lesser of $125,000 or 25% of the account; payments must start by 85.
     - $145,000 in 2022.
     - SECURE 2.0 Sec. 202 raised it to $200,000 and repealed the 25% cap (contracts from Dec 29 2022).
     - $210,000 for 2025 and 2026 (IRS Notices 2023-75, 2024-80, 2025-67).
     - **No public count of QLACs.** Form 1098-Q exists but SOI does not tabulate it. Deferred-income annuities, which include QLACs, are about 1% of sales (LIMRA, above).
   - **TSP:** the TSP Modernization Act (H.R. 3031, 2017; House Report 115-343) removed the rule that bought an annuity for participants who made no withdrawal election by the deadline. Annuity purchases there remain small (finding 4).

**What is solid vs weak**
- **Solid:**
  - SCF ownership levels and the 2004-2022 decline (finding 1).
  - CPS receipt of about 6% at 65+.
  - Z.1 stocks.
  - BLS NCS option availability.
  - Statute and regulation text.
- **Moderate:**
  - EBRI DB annuitization rates (good administrative data, but a limited set of plans and 2005-2010).
  - TIAA trend (good administrative data, but one recordkeeper serving higher education and non-profits, where annuitization was historically the default).
- **Weak:**
  - The share of DC participants who actually choose an annuity, nationally. There is no public national source; the best we have is HRS-based "about 7%", second-hand.
  - Any effect of the SECURE/SECURE 2.0 lifetime-income provisions. Untested.
  - LIMRA sales (industry, relayed by trade press).

## Method
- **SCF** (`scripts/scf_annuities.py`, `scripts/scf_annuity_se.py`). Uses the summary extracts `../scf/raw/rscfpYYYY.dta` (2022 dollars) and the full public files `pYYi6.dta` (2004+), read-only.
  - Age is the reference person's age. The 5 implicates are pooled.
  - Variable definitions:
    - "Any annuity" = X6815=1 ("receive income from or have assets in an annuity? Please do not include job pensions").
    - Cash-value = ANNUIT>0 (Fed definition: X6577 cash-in value, 2004+).
    - Non-cashable = X6815=1 and (X6576=5 or X6579=1).
    - Income received = X6578>0 or X6580>0.
    - Bought with pension payout = X6575=1.
  - % of financial assets uses FIN.
  - SEs: 999 bootstrap replicate weights (wt1bK x mmK, implicate 1) plus 1.2 x between-implicate variance, as in `../scf/`.
  - Expected benefit form for current-job plans (X11000-X11413, plans with a choice; account vs no-account plan) is tabulated in `output/scf_pension_benefit_choice.csv`. **It is not used in the findings** (see caveats).
- **CPS** (`scripts/bls_cps_tables.py`): reshapes `../cps/output/asec_retirement_income_by_age.csv`. `pct_annuity` = RET_SC 6 (legacy) / ANN_YN=1 (updated). Persons, MARSUPWT.
- **Z.1** (`scripts/z1_annuity_reserves.py`): Q4 levels from `raw/z1_csv_files_2026-09-10.zip`. Net flows are the sum of the four unadjusted quarterly FU series.
- **BLS NCS**: series NBU2190000000000002{887,888,889,896,925} and NBU2200000000000002{R08,R23,S14-S18}, % of participants in that plan type with the provision. The rows were extracted from the NB flat files (`raw/bls_nb_*.tsv`).
- **LIMRA mix and policy table**: `scripts/limra_mix_and_policy.py`.

## Sources
- Federal Reserve, Survey of Consumer Finances 1989-2022, https://www.federalreserve.gov/econres/scfindex.htm (files in `../scf/raw/`; `bulletin.macro.txt` for ANNUIT; codebooks 2004/2010/2016/2022).
- Census CPS ASEC via `../cps/` (README there has file URLs).
- Federal Reserve, Financial Accounts of the United States Z.1, release 2026-09-10, https://www.federalreserve.gov/releases/z1/current/z1_csv_files.zip ; L.116 footnote "Annuity reserves held by life insurance companies, excluding unallocated contracts held by pension funds", https://www.federalreserve.gov/Releases/Z1/20260319/html/l116.htm (`raw/z1_L116_2026-03-19.htm`).
- BLS National Compensation Survey, https://download.bls.gov/pub/time.series/nb/ (nb.series, nb.data.1.AllData, nb.provision).
- Banerjee, S. (2013), "Annuity and Lump-Sum Decisions in Defined Benefit Plans: The Role of Plan Rules", EBRI Issue Brief 381, https://www.ebri.org/content/annuity-and-lump-sum-decisions-in-defined-benefit-plans-the-role-of-plan-rules-5151 (summary page saved; full PDF not downloadable).
- Brown, Poterba & Richardson (2019), "Recent Trends in Retirement Income Choices at TIAA", NBER RDRC NB19-10, https://www.nber.org/sites/default/files/2020-04/NB19-10%20Brown%2C%20Richardson%2C%20Poterba.pdf **[recordkeeper data]**.
- Bosworth, Burtless & Alalouf (2015), "Do Retired Americans Annuitize Too Little?", CRR WP 2015-9, https://crr.bc.edu/wp-content/uploads/2015/06/wp_2015-9.pdf.
- GAO-26-107536 (March 2026), https://files.gao.gov/reports/GAO-26-107536/index.html (read via WebFetch; gao.gov blocks downloads) **[cites an industry survey]**.
- FRTIB board minutes, Sept 2024, https://www.frtib.gov/meeting_minutes/2024/2024Sept.pdf.
- House Report 115-343 (TSP Modernization Act, H.R. 3031), https://www.govinfo.gov/content/pkg/CRPT-115hrpt343/html/CRPT-115hrpt343-pt1.htm.
- LIMRA U.S. Individual Annuity Sales Survey, as reported by PlanAdviser (E. Rueda, 2026-02-12), https://www.planadviser.com/us-annuities-reach-record-461b-in-sales-in-2025/ **[industry; read via WebFetch, site blocks downloads]**.
- SECURE Act (P.L. 116-94) Secs. 109, 203, 204, https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm.
- SECURE 2.0 (P.L. 117-328 Div. T) Sec. 202, https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm (via `../dc_policy/notes/provisions.md`).
- DOL IFR, Pension Benefit Statements-Lifetime Income Illustrations, 85 FR 59132, https://www.govinfo.gov/content/pkg/FR-2020-09-18/html/2020-17476.htm.
- Treasury/IRS, Longevity Annuity Contracts final rule, 79 FR 37633, https://www.govinfo.gov/content/pkg/FR-2014-07-02/html/2014-15524.htm.
- IRS Notices 2021-61, 2023-75, 2024-80, 2025-67, https://www.irs.gov/pub/irs-drop/ (n-21-61.pdf etc.).
- DOL direct final rule removing 29 CFR 2550.404a-4 (1 Jul 2025), as recorded in `../dc_policy/notes/stay_in_plan_leakage.md`.

## Caveats
- **SCF break before 2004:**
  - 1998-2001 ANNUIT uses X6820. 1989-1995 is the Fed's pro-rata split of a combined "other managed assets" item.
  - The 65+ cash-value share jumps from 8.2% (2001) to 13.2% (2004) when the variable changes. That is most likely a questionnaire change, not a real rise.
  - Use 2004-2022 for trends. The 1989-2001 rows in the CSV are context only.
- **SCF annuity definition:**
  - X6815 excludes job pensions.
  - Annuities held inside IRAs may be reported with IRAs rather than here.
  - "Non-cashable" is a proxy for income annuities. Some deferred products also can't be cashed, and annuitized contracts with a residual value can be.
  - The SCF unit is the household (reference person's age); CPS counts persons.
- **SCF expected benefit choice (dropped from findings):**
  - 63-76% of 50+ respondents with an account-type current-job plan said their plan offers "regular payments for as long as you live", and 33-42% said they expect to choose that.
  - That is far above BLS's 11-22% availability. Respondents probably confuse installments, cash-balance plans or DB plans with account features.
  - Kept in the CSV for transparency only.
- **Z.1:**
  - "Pension entitlements" of life insurers includes group (allocated) annuities bought by pension plans (e.g. pension risk transfer), as well as individual annuities. It is a stock that includes market-value variable annuities, not a measure of annuitization.
  - Values revise: the Sept 2026 release has 2024 = $4,585B against $4,537B in the March 2026 L.116.
  - Net flows are affected by offshore reinsurance accounting and are volatile (2021: -$35B). Don't read single years.
- **TIAA and EBRI** data come from administrative records of particular plans and recordkeepers, not national samples.
- **NCS** values are rounded whole percentages from a sample; year-to-year moves of a few points (e.g. DB lump-sum 23% in 2019) may be noise.

## Dropped or unreachable
- **IRS annuity income:** Form 1040 lines 5a/5b combine "pensions and annuities". There is no public SOI split of private annuity income or of Form 1099-R by distribution type, and no SOI tabulation of Form 1098-Q (QLACs).
- **LIMRA primary releases** (paywalled/private), PSCA (blocked), GAO PDFs (403; text read via WebFetch), ICI (403), bls.gov pages (403; flat files used).
- **TSP:**
  - An FRTIB 2015 memo said to report "1% initiated an annuity purchase" among 2012 separators. The link is dead (404), so the figure is not used.
  - The search-snippet figure "$182M in 2023" is not in the minutes text, so it is not used.
- **HRS** (blocked): Hurd & Panis and Pashchenko figures are second-hand via CRR.
- **Benartzi, Previtero & Thaler (2011, JEP)** returned 403; not used.
- **DB lump-sum election rates after 2010:** no public national source found. Sibling DB-pension work may cover PBGC/Form 5500 angles.
