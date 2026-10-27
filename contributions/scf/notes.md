# SCF 1989-2022: contributions to DC plans and IRAs

Everything here comes from SCF public microdata (Federal Reserve Board). Script: `scripts/scf_contrib.py` (variable maps in `scripts/scf_vars.py`). Outputs: `output/scf_contrib_long.csv` (all measures and groups, 2,960 rows), `output/scf_contrib_headline.csv` (the headline subset), and `output/scf_contrib_diagnostics.csv` (QA checks per wave). Columns in the long files: year, measure, group, estimate, se, n, note. **n** is the number of unweighted sample cases in the statistic's base, from implicate 1. Each point estimate pools all 5 implicates and is weighted. The **SE** is the replicate-weight SE: bootstrap variance across 999 replicate weights on implicate 1, plus (1+1/5) times the between-implicate variance. The method follows `scf/scripts/scf_analysis.py`. Replicate weights exist for every wave, so SEs cover **1989-2022** (the minimum asked for was 2004-2022).

Run: `python3 -I contributions/scf/scripts/scf_contrib.py` (about 5 minutes). The script needs the 1989-2001 files unzipped in `/tmp/scfraw/x/` (see Sources).

## Findings (estimate, SE in parentheses)

**1. Share contributing to a DC plan at a current job.** The SCF only asks this for current-job plans of the respondent or spouse/partner.

| | 1989 | 1992 | 1995 | 1998 | 2001 | 2004 | 2007 | 2010 | 2013 | 2016 | 2019 | 2022 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| All families: has a current-job DC plan, % | 23.7 (0.7) | 25.0 | 30.0 | 33.7 | 34.5 | 33.2 | 34.6 | 31.5 | 31.0 | 32.2 | 33.0 | 33.8 (0.6) |
| All families: contributing, % | 18.0 (0.6) | 19.7 (0.7) | 25.0 (0.6) | 29.2 (0.7) | 29.8 (0.7) | 28.8 (0.7) | 30.9 (0.7) | 27.9 (0.5) | 27.1 (0.5) | 28.7 (0.4) | 29.7 (0.5) | 31.3 (0.6) |
| Working-age families (head 25-64, working): contributing, % | 28.9 (0.9) | 31.0 (1.1) | 38.1 (0.9) | 44.0 (1.0) | 43.6 (1.0) | 42.3 (0.9) | 44.5 (0.9) | 42.4 (0.7) | 41.8 (0.8) | 43.5 (0.6) | 45.5 (0.8) | 48.1 (0.9) |
| Take-up, families with a DC plan, % | 75.9 (1.6) | 78.5 | 83.2 | 86.6 | 86.3 | 86.7 | 89.3 | 88.4 | 87.5 | 89.0 | 90.0 | 92.4 (0.7) |
| Take-up, workers with a DC plan, % | 74.8 (1.5) | 77.0 (1.1) | 82.0 (0.9) | 84.4 (0.8) | 84.9 (0.9) | 85.2 (0.9) | 87.9 (0.8) | 87.8 (0.6) | 86.5 (0.7) | 88.3 (0.6) | 90.0 (0.5) | 90.2 (0.8) |
| Broad take-up, workers with a plan or eligible for an offered DC plan, % | n.a. | n.a. | 67.4 (1.1) | 70.8 (1.0) | 70.1 (1.1) | 69.8 (0.9) | 72.1 (1.1) | 72.5 (0.7) | 70.0 (0.9) | 72.4 (0.7) | 73.1 (0.8) | 74.7 (1.0) |

- The share of families contributing rose in the 1990s, from 18% in 1989 to 30% in 2001. It then stayed flat at 27-31% through 2022. The 2010-2013 dip follows the recession. The 2010 change to two detailed plans per person cannot explain much of it, because it affects under 2% of plan holders (see Method breaks). Among working-age families with a working head, the share went from 29% to 48%, and 2022 is the series high.
- Take-up among workers who already hold a current-job DC account rose steadily, from 75% in 1989 to 90% in 2022. The broader take-up measure also counts eligible workers who are not in any plan. It rose less, from 67% in 1995 to 75% in 2022.
- By head age, the 2022 contributing shares (all families) are: 25-34 41.8%, 35-44 43.9%, 45-54 48.6%, 55-64 34.9%. In 1989 they were 21.6%, 29.7%, 27.7% and 16.6%.
- By income quartile in 2022: Q1 6.4%, Q2 19.8%, Q3 40.2%, Q4 58.5%. In 1989: 2.1%, 9.5%, 23.9%, 36.3%.

**IRA contributions.** The SCF asks about them only in **2016, 2019 and 2022**, and the answers cover the prior calendar year (2015, 2018, 2021).

| | 2016 | 2019 | 2022 |
|---|---|---|---|
| All families: any member contributed to an IRA, % | 9.0 (0.4) | 7.8 (0.3) | 10.2 (0.4) |
| Working-age families: contributed to an IRA, % | 12.8 (0.6) | 10.2 (0.4) | 14.2 (0.7) |
| IRA holders who contributed, % | 29.9 (1.0) | 30.7 (1.0) | 33.0 (1.2) |
| Median family IRA contribution among contributors, nominal $ | 5,000 | 4,200 | 5,500 |
| All families: contributing to DC (current) or IRA (prior year), % | 33.7 (0.5) | 33.5 (0.5) | 36.3 (0.6) |
| All families: contributing to both, % | 3.9 | 4.0 | 5.2 |
| Working-age families: DC or IRA, % | 50.3 (0.7) | 49.7 (0.8) | 54.2 (0.8) |

**2. Contribution rates as % of pay.** Base: workers (respondent or spouse) who currently make employee contributions to a current-job DC plan. Each worker's rates are summed over their detailed plans.

| | 1989 | 1992 | 1995 | 1998 | 2001 | 2004 | 2007 | 2010 | 2013 | 2016 | 2019 | 2022 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Employee, median | 6.0 (0.2) | 6.0 (0.1) | 6.0 (0.1) | 6.0 (0.0) | 6.0 (0.0) | 6.0 (0.2) | 6.0 (0.4) | 5.0 (0.4) | 5.0 (0.8) | 6.0 (0.0) | 6.0 (0.0) | 6.0 (0.1) |
| Employee, mean | 7.4 (0.3) | 8.7 (0.4) | 7.2 | 7.5 | 7.7 | 7.9 | 7.1 | 6.8 | 6.9 | 7.2 | 7.3 | 7.6 (0.2) |
| Employee, mean with each rate capped at 25% | 7.2 | 7.6 | 7.1 | 7.4 | 7.7 | 7.8 | 7.0 | 6.7 | 6.8 | 7.1 | 7.2 | 7.3 |
| Employer, median (0 if employer pays nothing) | 3.0 | 3.0 | 4.0 | 3.0 | 3.9 | 4.0 | 3.0 | 3.0 | 3.0 | 4.0 | 4.0 | 4.0 |
| Employer, mean | 5.0 (0.4) | 6.0 (0.3) | 5.2 | 4.5 | 4.7 | 4.5 | 3.8 | 3.7 | 3.9 | 4.3 | 4.2 | 4.1 (0.1) |
| Contributors whose employer also contributes, % | 78.5 | 78.1 | 82.5 | 81.3 | 84.4 | 85.1 | 83.0 | 81.0 | 84.4 | 84.9 | 86.9 | 85.4 |
| Total (employee + employer), median | 10.0 | 10.0 | 10.0 | 10.0 | 11.0 | 11.0 | 10.0 | 9.0 | 10.0 | 10.0 | 10.0 | 10.0 |
| Total, mean | 12.5 | 14.6 | 12.4 | 11.8 | 12.3 | 12.4 | 11.0 | 10.5 | 10.8 | 11.5 | 11.6 | 11.8 |

- The median employee rate has stayed at **6% of pay** in almost every wave since 1989. The exception is 5% in 2010 and 2013. Contribution rates are heaped at whole percents (2004 onward, the public file rounds them to whole percents), so the medians move in whole-point steps and their bootstrap SEs can come out as 0.
- Mean rates go up with age. Workers 55-64 averaged 8.8% in 2022, against 6.7% for workers 25-34. They also go up with income: 8.8% in income Q4 against 5.2% in Q1 in 2022.
- Employer contributions per contributor fell. The mean was 5.0-6.0% of pay in 1989-1995 and 3.7-4.3% from 2007 on. The share of contributors who get any employer money rose slightly, from 78% to 85%.

**3. Aggregate flows as % of wages.** Annualized current contributions divided by annualized current main-job pay.

| | 1989 | 1992 | 1995 | 1998 | 2001 | 2004 | 2007 | 2010 | 2013 | 2016 | 2019 | 2022 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Employee DC contributions, % of all employees' pay | 2.8 (0.2) | 3.3 (0.2) | 3.1 (0.1) | 3.4 (0.1) | 3.8 (0.1) | 4.2 (0.3) | 3.9 (0.2) | 3.7 (0.1) | 3.7 (0.1) | 4.0 (0.1) | 4.0 (0.1) | 4.3 (0.2) |
| Employee + employer, % of all employees' pay | 5.4 | 6.0 | 5.8 | 5.7 | 6.5 | 7.0 | 6.5 | 6.4 | 6.1 | 6.7 | 6.7 | 6.9 |
| Employee, % of covered workers' pay | 6.6 | 7.5 | 6.3 | 6.7 | 7.1 | 7.8 | 7.0 | 6.6 | 6.6 | 6.9 | 6.9 | 7.2 |
| Employer, % of covered workers' pay | 6.2 | 6.4 | 5.4 | 4.6 | 5.1 | 5.1 | 4.5 | 4.8 | 4.2 | 4.6 | 4.7 | 4.3 |
| Employee + employer, % of covered workers' pay | 12.8 | 14.0 | 11.7 | 11.2 | 12.2 | 12.8 | 11.5 | 11.5 | 10.8 | 11.5 | 11.6 | 11.5 |

IRA contributions (prior calendar year) as a share of prior-year family wage and salary income (X5702): 0.8% in 2016, 0.6% in 2019, 0.8% in 2022. DC (employee and employer, current) plus IRA (prior year), as a share of prior-year wage income: 7.5%, 7.6%, 8.0%. This mixes reference periods; see the definitions.

**What stands out**
- Since 1989, DC contribution flows have grown mostly because more workers contribute (wider coverage and higher take-up), not because contributors save more. Employee rates per contributor are flat at a median of 6% and a mean of about 7-8%. The employee flow relative to all employees' pay rose by half, from 2.8% to 4.3%. Employer money per covered worker fell: from 6.2% of covered pay in 1989 to 4.3% in 2022.
- The 1989-1992 employer figures are high (mean 5-6%). Account plans in those years still included many employer-funded profit-sharing and money-purchase plans with no employee contribution. That same mix explains the lower take-up (75%).
- Families with any IRA contribution (8-10%) are a small group next to DC contributors (28-31%). In dollars, IRA contributions are under 1% of wages, against about 7% for DC.

## Definitions

- **Family** is the SCF primary economic unit. **Head** is the SCF reference person, and family age bands use the head's AGE from the summary extract. **Working-age families** have a head aged 25-64 with OCCAT1 in (1, 2), meaning the head works for someone else or is self-employed.
- **Current-job DC (account-type) plan** follows the Fed's DCPLANCJ logic in `bulletin.macro.txt`, applied to the detailed current-job pension grid of the respondent and spouse/partner:
  - 2004-2022: a plan slot whose account balance is > 0 or is coded -1 ("nothing").
  - 1989-2001: plan type is 2 (account) or 3 (combination).
  - Our family share matches the Fed's DCPLANCJ exactly in 1989-1998. From 2001 on it runs 0.7-1.8 points lower, because DCPLANCJ also counts account plans from the current job that already pay benefits, and those cannot receive contributions (see diagnostics).
- **Contributing** means the respondent or spouse answers "yes" to "Do you make contributions to this plan?" for an account-type slot. Code 3, "yes, but not currently" (2004+), counts as not contributing. Plans already paying benefits are excluded by the SCF skip logic.
- **Take-up (families)** = contributing families / families with a current-job DC plan. **Take-up (workers)** is the same ratio at the person level.
- **Broad take-up (1995+)** = contributors / (plan holders + eligible non-participants). An eligible non-participant answered X4137/X4737 = 1 ("eligible") and was offered a plan of an account kind (X6708-X6711 / X6713-X6716 checked, or X6712 / X6717 in ESOP, SEP/SIMPLE, DC/TIAA-CREF, money purchase, other salary reduction, or other account). The SCF skips the eligibility questions for workers who are already in any plan, such as DB-only participants. Those workers' unused DC options are therefore missed, which biases broad take-up upward.
- **Employee % of pay**: the SCF percent variable (percent × 100). The Fed converts dollar answers to percents using the wage at X4112/X4712. When the percent is missing, we compute it as the annualized dollar amount (amount × frequency) divided by annual pay. Annual pay is X4112 × frequency X4113 (spouse X4712/X4713); hourly pay uses hours × weeks. In 2004+, a current answer of "varies" (-5) is replaced by the last-year questions. Rates are summed across a worker's detailed plans.
- **Employer % of pay** uses the same logic with the employer variables. The SCF fills both the percent and the dollar amount when the employer reports a match rate. Where the employer does not contribute, the rate is 0. Employer rates are missing for 1989-2001 combination plans (type 3), which have no employer questions. Missing employer rates affect 4.8-8.4% of contributors in 1989-2001 and under 1.1% from 2004 on. Those workers are dropped from employer and total rate statistics.
- **Aggregates**: sum of annualized employee (and employer) dollars, over workers with positive current main-job pay, divided by the sum of annualized current main-job pay. The denominator is either all respondent and spouse employees ("all employees' pay") or only those with a current-job DC plan ("covered workers' pay"). Self-employed and no-pay plan holders (0.3-1.4% of contributors in the waves checked: 1989, 1995, 2004, 2010, 2022) are excluded from both sides. Contributions on plans beyond the detailed slots are not captured.
- **IRA contributions (2016+)**: X6791/X6793/X6795 ("Did you / your spouse / other family members make any contributions to these accounts in <prior year>? Please do not include rollovers or cashouts") and amounts X6792/X6794/X6796. The amounts are family totals in nominal dollars. "IRA holder" means IRAKH > 0 at interview.
- Weighting: the summary-extract WGT (already divided by 5) is merged onto the full X-variable file by Y1 (X1 in 1989).

## Variables by wave (verified in the codebooks)

| Waves | Plan slots (R; spouse) | Type / account test | Employee: contributes, %, $, frequency | Employer: contributes, %, $, frequency | Notes |
|---|---|---|---|---|---|
| 1989-2001 | 3 per person: X4200, X4300, X4400; X4800, X4900, X5000 (X4n..) | X4n03: 1 formula, 2 account, 3 both | Account (type 2): X4n22, X4n23, X4n24, X4n25. Combination (type 3): X4n05, X4n06, X4n07, X4n08 | X4n18, X4n19, X4n20, X4n21 (type 2 only) | Balance X4n26 (type 2), X4n04 (type 3); plans beyond 3: X4436/X5036 balance only |
| 2004-2007 | 3 per person: X11000, X11100, X11200; X11300, X11400, X11500 (b) | Type b+0/b+1 (2004 codes, e.g. 5 = 401(k)); account test: balance b+32 > 0 or -1 | b+40 (1 yes, 3 yes not currently, 5 no), b+41, b+42, b+43; last year b+44 to b+46 | b+47, b+48 (how: match/% of pay/$), b+49 % of pay, b+50 match rate, b+51, b+52; last year b+53 to b+57 | Remaining plans: X11259/X11559 balance only |
| 2010-2022 | 2 per person: X11000, X11100; X11300, X11400 | X11000 = "money accumulates in an account" yes/no; X11001 type; account test as above | same offsets | same offsets | Remaining plans X11259/X11559 |
| All | Ages X14 / X19; work X4105 / X4705; pay X4112 + X4113 / X4712 + X4713; hours X4110, X4111 / X4710, X4711; plan count X4201 / X4801; eligibility X4137 / X4737; offered kinds X6708-X6712 / X6713-X6717 (1995+); family wage income X5702 | | | | |
| 2016-2022 | IRA contributions X6791-X6796 | | | | Prior calendar year |

Codebook locations:
- 2022: X11040-X11057 at lines 24779-25640 of `scf/raw/codebk2022.txt`; X6791-X6796 at about line 17967.
- 2001: X4203-X4226 at lines 16447-17330 of `raw/codebk2001.txt`.
- 1989: questions R20-R32 at lines 6733-7115 of `raw/codebk89.txt`.

1989 percents are coded "to 2 decimal places". In the data they share the same ×100 scale as later waves; the 1989 median is 600 = 6%.

**IRA contribution question: not present before 2016.** Searches for IRA contribution items found none in codebk89, 92, 95, 98, 2001, 2004, 2007, 2010 and 2013. The full files for 2004-2013 have no X6791. In 1998-2001, X6791 means something else: the purpose of a pension loan.

## Method breaks

1. **2004 pension module redesign** (1989-2001 vs 2004+). Before 2004, respondents classified each plan from a show card as formula, account or both. In 2004-2007 they chose among regular payments / account / both plus named plan types. From 2010 the opening question is whether "money accumulates in an account" (X11000). The account test changes with the module: plan type before 2004, balance from 2004 on. The contribution question gained a "yes, but not currently" option (2004+), and employer contributions are asked as match / percent of pay / dollar amount (2004+).
2. **Detailed plans per person cut from 3 to 2 in 2010.** Plan holders with more plans than detailed slots are under 0.8% before 2004, about 0.1% in 2004-2007 and 1.2-1.7% from 2010 (diagnostics). Contributions to those extra plans are not observed, so rates and aggregates are slightly understated from 2010.
3. **Combination plans (1989-2001)**: employee contributions come from the formula-plan question (X4n05). There is no employer information for these plans.
4. **Disclosure rounding**: from 2004 the public file rounds percent variables to whole points (bottom-coded at 1, top-coded at 99). Before 2004, the public data are not rounded to whole points: some medians are non-integer, for example 5.4. Medians before and after 2004 are therefore not fully comparable at decimal precision.
5. **1992 outliers**: a few reported or converted employee rates reach 50-100% of pay; the 1992 99th percentile is 100%. This inflates the 1992 means (8.7% employee, 14.6% total). The capped-at-25% means (7.6% and 12.7%) are more comparable across waves.
6. **IRA timing**: the IRA items cover the calendar year before the survey, while DC items are current at interview. The "DC or IRA" share and the combined aggregate therefore mix reference periods.
7. Aggregates use current main-job pay of the respondent and spouse only. Contributions by other family members, and second jobs, are not covered.

## Sources

- SCF index: https://www.federalreserve.gov/econres/scfindex.htm. Wave pages: https://www.federalreserve.gov/econres/scf_1989.htm, scf_1992.htm, scf_1995.htm, scf_1998.htm, scf_2001.htm.
- 1989-2001 full public data (Stata), downloaded 2026-10-06 to `/tmp/scfraw` (outside the shared folder because of size; unzipped to `/tmp/scfraw/x`): https://www.federalreserve.gov/econres/files/scf89s.zip (p89i6.dta), scf92s.zip (p92i4.dta), scf95s.zip (p95i6.dta), scf98s.zip (p98i6.dta), scf01s.zip (p01i6.dta).
- 1989-2001 replicate weights: https://www.federalreserve.gov/econres/files/scf89rw1s.zip, scf92rw1s.zip, scf95rw1s.zip, scf98rw1s.zip, scf2001rw1s.zip.
- Codebooks in `contributions/scf/raw/`: https://www.federalreserve.gov/econres/files/codebk89.txt, codebk92.txt, codebk95.txt, codebk98.txt, codebk2001.txt, codebk2007.txt, codebk2013.txt, codebk2019.txt. Also `scf/raw/` codebk2004, 2010, 2016 and 2022.
- 2004-2022 full files, replicate weights and summary extracts (rscfp1989-2022): `scf/raw/`, downloaded by earlier project work from the same Fed site. Summary-variable definitions: `scf/raw/bulletin.macro.txt` (https://www.federalreserve.gov/econres/files/bulletin.macro.txt).

## SCF 2025 added (2026-10-27)

Source: `scf/raw/p25i6.dta`, `p25_rw1.dta`, `rscfp2025.dta`, `codebk2025.txt` (Fed release of 9 Oct 2026; 4,367 families, 21,800 implicate records). `scf_vars.py` now has 2025 in `WAVES` and `IRA_WAVES`; nothing else in the method changed. Units are unchanged: shares and rates are % (no CPI step needed); the IRA median is **nominal** dollars of the prior year (2024), as for earlier waves. The summary-extract INCOME and IRAKH are in 2025 dollars, but they are only used for within-wave income quartiles and IRAKH > 0, so no adjustment applies.

**Codebook check (2022 vs 2025).** Every X-variable the scripts use keeps its number, question and codes: the current-job plan grid X11000-X11057 / X11100- / X11300- / X11400- (balance b+32, employee b+40 to b+46, employer b+47 to b+57), plan counts X4201/X4801, eligibility X4137/X4737, offered kinds X6708-X6717 (same codes 7, 9, 10, 11, 13, 16), work and pay X4105/X4106/X4110-X4113 (and spouse), ages X14/X19, wage income X5702, IRA contributions X6791-X6796. The only text changes are reference years (2021 -> 2024) and the plan-type label in X11001 ("traditional pension" is now "defined benefit (DB) pension"; not used in the account test). None of the used variables is on the codebook's "removed since 2022" list; new items there (for example X4142/X4742 telework) are not pension items. The Fed's DCPLANCJ code in `bulletin.macro.txt` is the same as in the 2022 vintage. So there is no break in 2025.

**Re-run check.** The 1989-2001 full files are not on disk (`/tmp/scfraw/x` is gone), so the run covered 2004-2025 (`python3 -I` on `scf_contrib.run([2004, ..., 2025])`). All 1,850 rows for 2004-2022 (estimate, SE, n, note) and the 2004-2022 diagnostics match the previous output exactly (max difference 0). The 2025 rows (310 long, 16 headline, 1 diagnostics) were appended to the existing 1989-2022 files; every pre-2025 line of `scf_contrib_long.csv`, `scf_contrib_headline.csv` and `scf_contrib_diagnostics.csv` is byte-identical to before. The previous files are kept outside the shared folder. To rerun everything with no year arguments, the 1989-2001 files must be downloaded again (see Sources).

**2025 next to 2022 (estimate, SE).** Base and definitions as in the tables above; DC items are current at interview (2025), IRA items cover calendar 2024.

| | 2022 | 2025 |
|---|---|---|
| All families: has a current-job DC plan, % | 33.8 (0.6) | 34.8 (0.7) |
| All families: contributing to a current-job DC plan, % | 31.3 (0.6) | 32.2 (0.7) |
| Working-age families (head 25-64, working): contributing, % | 48.1 (0.9) | 49.2 (1.1) |
| Take-up, families with a DC plan, % | 92.4 (0.7) | 92.5 (0.7) |
| Take-up, workers with a DC plan, % | 90.2 (0.8) | 91.7 (0.6) |
| Broad take-up, workers with a plan or eligible, % | 74.7 (1.0) | 76.3 (1.0) |
| Employee % of pay, median | 6.0 (0.1) | 6.0 (0.0) |
| Employee % of pay, mean | 7.6 (0.2) | 8.0 (0.2) |
| Employee mean, rates capped at 25% | 7.3 (0.1) | 7.6 (0.1) |
| Employer % of pay, median | 4.0 (0.5) | 4.0 (0.0) |
| Employer % of pay, mean | 4.1 (0.1) | 4.3 (0.1) |
| Contributors whose employer also contributes, % | 85.4 (1.1) | 86.7 (0.9) |
| Total % of pay, median / mean | 10.0 / 11.8 (0.2) | 10.0 / 12.3 (0.2) |
| Employee DC contributions, % of all employees' pay | 4.3 (0.2) | 4.8 (0.15) |
| Employee + employer, % of all employees' pay | 6.9 (0.2) | 7.8 (0.2) |
| Employee + employer, % of covered workers' pay | 11.5 (0.3) | 12.3 (0.3) |
| All families: any member contributed to an IRA (prior year), % | 10.2 (0.4) | 9.7 (0.5) |
| Working-age families: contributed to an IRA, % | 14.2 (0.7) | 12.8 (0.6) |
| IRA holders who contributed, % | 33.0 (1.2) | 31.9 (1.1) |
| Median family IRA contribution, nominal $ (2021 / 2024) | 5,500 (541) | 5,200 (406) |
| IRA contributions, % of prior-year family wage income | 0.8 (0.04) | 0.7 (0.04) |
| All families: contributing to DC or IRA, % | 36.3 (0.6) | 36.6 (0.8) |
| All families: contributing to both, % | 5.2 (0.3) | 5.3 (0.3) |
| Working-age families: DC or IRA, % | 54.2 (0.8) | 53.9 (1.2) |
| DC (ee + er) + IRA, % of prior-year wage income | 8.0 (0.2) | 8.5 (0.2) |

By head age (all families contributing to DC, 2022 -> 2025): 25-34 41.8 -> 40.4, 35-44 43.9 -> 46.9, 45-54 48.6 -> 46.7, 55-64 34.9 -> 39.9. By income quartile: Q1 6.4 -> 6.5, Q2 19.8 -> 21.2, Q3 40.2 -> 43.4, Q4 58.5 -> 57.8. Mean employee rate by worker age: 25-34 6.7 -> 6.5, 35-44 6.7 -> 8.2, 45-54 7.8 -> 8.6, 55-64 8.8 -> 9.0.

What 2025 shows and what looks odd:
- Shares contributing and take-up edged up to new series highs, but each 2022 -> 2025 change is within about one combined SE (contributing families +1.0 pt, working-age +1.1 pt, worker take-up +1.5 pt).
- **The employee flow jumped**: 4.3% -> 4.8% of all employees' pay (difference about 2 combined SEs), and employee + employer 6.9% -> 7.8%, the highest of any wave. The rise comes from both more contributors (person-level contributors rose from 39% to 43% of employees with pay) and a higher dollar rate among contributors (employee dollars / contributors' pay 7.7% -> 8.2%). Some of the jump may come from the 2022 denominator: 2022 has a heavier top tail of pay, where few contribute in proportion to pay (top 1% of employees held 12.7% of pay in 2022, 11.3% in 2025; mean pay rose 4.5% 2022 -> 2025 while median pay rose 11%). The median employee rate stays at 6%.
- The mean employee rate (7.6 -> 8.0) and the age 35-44 mean (6.7 -> 8.2) rose; the capped mean rose less (7.3 -> 7.6), and the share of contributors at 15%+ of pay was 10.6% (2022) and 10.8% (2025), so this is not a few outliers. A possible reason (not tested) is SECURE 2.0 (auto-escalation, higher limits), but the survey does not identify auto-enrollment.
- IRA contribution measures fell slightly (families 10.2% -> 9.7%; median nominal $5,500 -> $5,200) although the IRA limit rose from $6,000 (2021) to $7,000 (2024). The changes are within about one SE; 2022 (2021 contributions) was itself a high year.
- **Data-handling differences, not definitions**: in 2025 no contributor has the employer percent coded -1 ("nothing") or -2 ("cannot convert") while the employer contributes, and no employee percent is coded -2; in 2022 there were a few such records. This is consistent with missing employer rates among contributors falling from 0.7% to 0.06% (diagnostics). The effect on rates is negligible.
- The gap between the Fed's DCPLANCJ and our current-job DC share widened to 2.2 pts (37.1% vs 34.8%; 1.5 pts in 2022). As before, DCPLANCJ also counts current-job account plans already paying benefits, which cannot receive contributions; no plan we count is outside DCPLANCJ. Plan holders with more plans than detailed slots: 1.8% (1.7% in 2022).
- Some median SEs are 0 or jump (employer median SE 0.0 in 2025 vs 0.5 in 2022; total median 0.5 vs 0.1) because rates are heaped at whole percents.
