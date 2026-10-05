# Coverage expansion: state auto-IRA mandates and federal small-employer measures — is it working?

Task: stateira. Compiled 2026-10-04. Scope: state auto-IRA mandates; SECURE Act 2019 §101 (pooled employer plans, PEPs), §104/§105 (startup and auto-enrollment credits); SECURE 2.0 §102 (bigger startup credit plus employer-contribution credit); long-term part-time (LTPT) eligibility (SECURE §112 / SECURE 2.0 §125).

Files produced:
- `dc_policy/output/bls_ncs_access_participation.csv`: BLS NCS private-industry access, participation and take-up, 2003–2026, for "all retirement" and "defined contribution" plans, by group (444 rows).
- `dc_policy/raw/stateira/`: CRI dashboard data as of 2026-08-31 (`cri_state_autoira_dashboard_2026-08-31.tsv`, `cri_funded_accounts_history.tsv`, `cri_assets_history.tsv`); CalSavers snapshot PDF (2026-08-31); OregonSaves dashboard PDF (2026-07-31); NCS establishments-offering series (`ncs_establishments_offering.csv`); the CSV build script (`build_bls_csv.py`).

Labels: "Computed" means I derived the figure, and the inputs are shown. "[recordkeeper/industry]" marks non-government, non-academic data. "Unverified" means I could not confirm it from a primary document.

---

## 1. State auto-IRA programs: size, participation, contribution rates, leakage

### Takeaway
As of 31 Aug 2026, 15 state auto-IRA programs held $3.39B in 1.41M funded accounts across 404,101 registered employers (Georgetown CRI). Growth is accelerating. Funded accounts rose from 109k (Dec 2019) to 635k (Dec 2022) to 1.16M (Dec 2025). Among workers who are auto-enrolled, about two-thirds to three-quarters do not opt out at first. On contribution rates, the average saver puts in about 5–7% of pay, but balances are small: the median CalSavers balance is $704. Leakage is large. About 32% of all CalSavers contributions and about 41% of all OregonSaves contributions have already been withdrawn (Computed). Employer compliance is still partial.

### Cited findings
- **All programs (CRI, 31 Aug 2026):** "Across all 15 programs as of 08/31/2026: 3.393 Billion Total; 404,101 Employers Registered; 1,413,435 Funded Accounts." Including the MA CORE voluntary MEP, the total is $3.474B and 1,416,426 funded accounts. Source: [Georgetown CRI, State Program Performance Data – Current Year (Datawrapper pLCDn v34 dataset), data as of 2026-08-31](https://cri.georgetown.edu/states/state-data/current-year/) (raw: https://datawrapper.dwcdn.net/pLCDn/34/dataset.csv).
- **Per-program figures (CRI, 31 Aug 2026):** assets $M / registered employers / funded accounts / avg contribution rate / avg balance:
  - CalSavers: 1,950.3 / 282,576 / 662,734 / 5.2% / $2,943
  - My Illinois Savings (formerly Illinois Secure Choice; rebranded June 2026): 372.0 / 27,883 / 177,847 / 6.9% / $2,092
  - OregonSaves: 531.5 / 36,566 / 158,783 / 7.0% / $3,347
  - MyCTSavings: 77.9 / 7,647 / 48,403 / 4.7% / $1,609
  - MarylandSaves: 37.5 / 6,692 / 20,578 / 5.9% / $1,822
  - Colorado SecureSavings: 248.0 / 18,717 / 118,839 / 5.8% / $2,087
  - MERIT (Maine): 38.4 / 3,213 / 22,149 / 5.7% / $1,734
  - RetirePathVA: 36.0 / 2,898 / 29,650 / 5.5% / $1,214
  - Delaware EARNS: 14.2 / 2,134 / 10,839 / 5.5% / $1,312
  - RetireReadyNJ: 28.5 / 1,618 / 32,529 / 3.2% / $878
  - VermontSaves: 9.8 / 2,740 / 7,940 / 5.4% / $1,233
  - NEST (Nevada): 21.5 / 3,498 / 25,918 / 5.0% / $831
  - New York Secure Choice: 22.2 / 6,382 / 79,757 / 3.2% / $278
  - Minnesota Secure Choice: 3.8 / 977 / 14,727 / 5.0% / $257
  - RISavers: 1.6 / 560 / 2,742 / 5.0% / $593
  - Source: same CRI dataset. NJ and NY use a 3% default rate, which explains their 3.2% averages. CRI cautions: "Programs are not identical, and these variations will contribute to differences in performance."
- **CalSavers (8/31/2026 snapshot):**
  - Accounts and employers: funded accounts 662,734; payroll-contributing accounts 794,973; "Effective Opt-Out Rate 34.43%" (34.87% at 5/31/2026; 35.19% at 3/31/2026).
  - Balances and contributions: total assets $1,950,268,841; average funded balance $2,943; **median funded balance $704**; average contribution rate 5.24% (median 5.00%); average monthly contribution $203 (median $151).
  - Withdrawals: "Amount of Withdrawals $675,647,142" against "Total Contributions Amount $2,091,719,418". Accounts with a full withdrawal: 205,784; with a partial withdrawal: 41,864. "Withdrawal Rate** 25.89%", where "**Withdrawal Rate is calculated as Accounts with a full withdrawal as a percent of Payroll Contributing Accounts."
  - Employer status: registered 282,576; exempt 268,571; started payroll deductions 79,795; "Facilitated Deductions in last 90 days" 51,485. Estimated eligible employers across all waves: 981,982. Employer response rate 56.13% (Wave 4, deadline 12/31/2025: 49.36%).
  - 43.5% of funded accounts hold $0.01–$500.
  - Source: [CalSavers Participation & Funding Snapshot as of 8/31/2026, CA State Treasurer](https://www.treasurer.ca.gov/sites/default/files/calsavers/August_2026_Participation_Snapshot_Report.pdf).
  - **Computed:**
    - Participation among auto-enrolled = 100 − 34.43 = **65.6%**.
    - Withdrawals as % of cumulative contributions = 675.6/2,091.7 = **32.3%**.
    - Funded ÷ payroll-contributing accounts = 662,734/794,973 = 83.4%.
    - Employers that have started payroll deductions ÷ estimated eligible employers = 79,795/981,982 = **8.1%**. Registered ÷ estimated eligible = 28.8%; exempt (already have a plan, etc.) ÷ estimated eligible = 27.3%. Caveat: "estimated eligible" is the count of employers sent notices, so it overstates the true eligible pool.
- **OregonSaves (7/31/2026 dashboard):**
  - Accounts: total funded accounts 156,691; payroll-contributing accounts 207,787; accounts with a withdrawal 78,045.
  - Money: total contributions $639,303,076; total withdrawals −$262,631,601; assets $515,896,002.
  - Rates and balances: "Average Savings Rate (Funded Accounts) 7.0%"; average funded balance $3,292; median monthly contribution $152. "Opt-Out Rate (0-30), since inception 26.5%", defined as "accounts that have opted out in the first 30 days by the total number of unique savers ever registered."
  - Employers: registered 36,136; "Actively Submitting Payroll (Past 3 Months)" 8,525; exempted 51,415.
  - Source: [OregonSaves Program Monthly Dashboard as of July 31, 2026, Oregon Treasury](https://www.oregon.gov/treasury/Upward-Oregon/Shared%20Documents/Board-Meeting-Minutes/Program-Reports/2026/2026-07-Program-Report-OregonSaves-Monthly.pdf).
  - **Computed:** withdrawals ÷ contributions = 262.6/639.3 = **41.1%**. Accounts with a withdrawal ÷ payroll-contributing accounts = 37.6%. Employers actively remitting ÷ registered = 23.6%. The 30-day participation rate = 100 − 26.5 = 73.5%, which overstates the longer-run rate (see §2).
- **Illinois (verified 2026-10-05 from the Treasurer's monthly dashboard PDFs):** the old "Effective Opt-Out Rate" was **36.94%** at 31 Dec 2025 (37.11% in Nov 2025; 50,341 shown beside it) and 36.93% in May 2026, so the 37% figure is confirmed for 2025. From the June 2026 dashboard (the month of the rebrand to My Illinois Savings) the line is relabelled "Opt-out Rate" and drops to **25.34%** (June), 25.48% (July) and **26.27% (August 2026)**. The dashboards give no definition or explanation, so the June drop is most likely a change of definition, not of behaviour; do not compare across it. Other August 2026 figures: 177,847 funded accounts, average contribution rate 6.93%, full-withdrawal rate 26.53%, $372.0M assets. Sources: [Secure Choice Monthly Dashboard, December 2025](https://illinoistreasurer.gov/wp-content/uploads/2026/01/Secure-Choice-Monthly-Dashboard_December-2025.pdf); [May 2026](https://illinoistreasurer.gov/wp-content/uploads/2026/06/Secure-Choice-Monthly-Dashboard_May-2026.pdf); [June 2026](https://illinoistreasurer.gov/wp-content/uploads/2026/07/Secure-Choice-Monthly-Dashboard_June-2026.pdf); [My Illinois Savings Monthly Dashboard, August 2026](https://illinoistreasurer.gov/wp-content/uploads/2026/09/My-Illinois-Savings-Monthly-Dashboard_August-2026.pdf) (copies in `raw/gapA/`).
- **Earlier OregonSaves evidence (CRR):** "Participation in OregonSaves ranges from 48 to 67 percent." "Twenty percent of employees with balances in September 2018 made at least one pre-retirement withdrawal." Withdrawal incidence was 32% among workers who left their employer versus 17% among those who stayed. Source: [Quinby, Munnell, Hou, Belbase & Sanzenbacher, "Participation and Pre-Retirement Withdrawals in Oregon's Auto-IRA," CRR WP 2019-15, Nov 2019](https://crr.bc.edu/participation-and-pre-retirement-withdrawals-in-oregons-auto-ira/).

### Evidence verdict
**Moderate–strong evidence that the programs expand access and produce real (if small) saving.** The direction is positive. Results are weaker on retirement adequacy because balances are small, about a third to two-fifths of contributions leak out, and employer compliance is incomplete.

### Gaps
- No program publishes participation as a share of all workers covered by the mandate, so the denominators differ: Oregon counts savers ever registered; CalSavers uses an "effective" opt-out rate.
- No consistent cross-state opt-out series exists.
- Withdrawals are not split by reason (hardship, job change, account closure).
- Employer non-compliance (firms that neither register nor certify an exemption) is only partly observable.

---

## 2. Academic evidence on participation, crowd-in, credits and leakage

### Takeaway
The best causal evidence comes from IRS/Treasury microdata (Bloomfield, Goodman, Rao & Slavov, JPubE 2025). It finds that state mandates induce about 17% of treated firms to start their own employer plan, with no meaningful crowd-out. Employer plans account for 30–45% of the mandates' total effect on firm offerings. OregonSaves studies show broad access but high opt-out among the lowest paid: "about half" opt out within 12 months and about 70% stop contributing by opt-out or job turnover. The federal startup credit is barely used. Only about 1% (pre-2020) to 5.5% (2023) of eligible firms claim it, so it has likely had "a limited impact on new ESRP formation."

### Cited findings
- **Crowd-in from state mandates (tax microdata).** "we estimate that about 17% of treated firms have been induced to offer an ESRP by these policies… This effect is large considering that, for employers, establishing and maintaining an ESRP is more costly than utilizing the state-facilitated IRAs." "We find that ESRPs account for between 30% (Oregon) and 45% (Connecticut) of the total effect." The paper finds no economically significant effect on plan terminations ("stops plan"). Among compliers, about 22% chose SIMPLE IRAs. Source: [Bloomfield, Goodman, Rao & Slavov, "State Auto-IRA Policies and Firm Behavior: Lessons from Administrative Tax Data," NBER WP 32817, Aug 2024 rev. Apr 2025; published J. Public Economics vol. 247 (2025)](https://www.nber.org/papers/w32817). An earlier version reported "at least 30,000 firms have been induced to offer an ESRP" ([NBER WP 32817, Aug 2024 version, CRI copy](https://cri.georgetown.edu/wp-content/uploads/2026/03/Why-Do-Emplyers-Establish-Retirement-Savings-Plans.pdf)).
- **CRR summary of that study.** "the share of firms offering their own retirement plans increased by 5.7 to 8.7 percentage points relative to the same-sized firms in control states… no evidence exists of any major shift towards fewer employer plans." Descriptively, treated firms' offer rate went from 35.2% two years before to 49.1% one year after; control firms went from 38.8% to 41.2%. Source: [Bloomfield, Rao & Slavov, "How Do State Auto-IRAs Affect Adoption of Employer Plans?" CRR Issue in Brief 25-25, Dec 2025](https://crr.bc.edu/wp-content/uploads/2025/12/IB_25-25.pdf).
- **Earlier Form 5500 and CPS study.** "these policies increase an individual's probability of working for a firm with an ESRP by 6-9 percent and of being included in the ESRP by 8-13 percent. At the firm level… the probability of establishing a new ESRP by 41-44 percent, and the number of ESRP participants by 6 percent." CRR describes the magnitude as about +0.8 pp on a 54% base for firms, and +1.1 pp on a 37% base for worker participation. Sources: [Bloomfield, Lee, Philbrick & Slavov, "How Do Firms Respond to State Retirement Plan Mandates?" NBER WP 31398, Jun 2023 rev. Jun 2024](https://www.nber.org/papers/w31398); [Munnell, "Auto-IRA Programs Encourage Firms to Establish Their Own Plans," CRR, Jan 17 2024](https://crr.bc.edu/auto-ira-programs-encourage-firms-to-establish-their-own-plans/).
- **Pew, descriptive Form 5500 analysis (Apr 2026).** Nationally, "the share of all private retirement plans that were new fell from 10.1% to 9.1% from 2022 to 2023." In auto-IRA states, new plans made up 9.1% (VA) to 18.4% (CO) of all plans in 2023, and "all states saw an increase in the share of new plans… immediately following implementation." A second, independent search extract (2026-10-05) gives the same numbers and adds that year-on-year increases in the new-plan share "ranged from 0.9% in Virginia and Maryland to 5.9% in Colorado," with California the exception (a decrease after a 2022 surge). This is descriptive, not causal. The Pew page, its Wayback copy, and the NAPA/ASPPA/PSCA write-ups all returned 403 or connection resets from here, so the figures are **consistent across two search extracts but not read from the primary page (partially unverified)**. Source: [Pew, "States With Automated Retirement Savings Programs See Growth in New Private Plans," Apr 16 2026](https://www.pew.org/en/research-and-analysis/issue-briefs/2026/04/states-with-automated-retirement-savings-programs-see-growth-in-new-private-plans).
- **OregonSaves participation and leakage (Chalmers, Mitchell, Reuter & Zhong).** All of the following are quoted from the paper's highlights:
  - "about half of these workers opt out of the program within 12 months, and around 70% either opt out or experience job turnover, ending their contributions."
  - "overall opt-out rates are high (50+%), particularly for the lowest-paid."
  - "Workers' average effective contribution rate is 4.7% of pay for those who contribute… but it is only 1.3% when averaged across all eligible employees."
  - "Around 10% of OregonSaves accounts are closed each year, and around a third of all contributions through December 2023 were withdrawn."
  - "Employees exposed to OregonSaves for the second or third time are approximately three percentage points less likely to opt out."
  - Source: [Chalmers, Mitchell, Reuter & Zhong, "Will State-Based Retirement Savings Plans Boost Retirement Saving? New Evidence from OregonSaves," June 11 2024 version](https://www.jonreuter.com/research/ORSP_202406.pdf); published as "New evidence on the efficacy of state-based retirement programs: The case of OregonSaves," [J. Public Economics 246 (2025), doi:10.1016/j.jpubeco.2025.105379](https://www.sciencedirect.com/science/article/abs/pii/S0047272725000775). An earlier version reported an average balance of $754 in April 2020 ([NBER WP 28469](https://www.nber.org/papers/w28469)).
- **Startup and auto-enrollment credits (Form 8881, §45E).** "only 1 percent (pre-policy expansion) to 5.5 percent (post-policy expansion) of apparently eligible firms claim the credit." "no more than 5 percent of eligible firms—approximately 18,000 firms—claimed the credit in 2023." "the Section 45E credit has likely had a limited impact on new ESRP formation." "most firms only claim the credit for one year despite being eligible to do so for up to three years." By component, the auto-enrollment credit was "about 15% of the total credit" in 2020–22; in 2023 the new employer-contribution credit (SECURE 2.0 §102) was "71% of the 2023 total credit." Source: [Bloomfield, Goodman, Ramnath & Slavov, "How Do Tax Incentives Influence Employer Decisions to Offer Retirement Benefits?" CRI WP 2025-02, Jul 2025 (NBER WP 34043)](https://cri.georgetown.edu/wp-content/uploads/2025/07/Bloomfield-Goodman-Ramnath-Slavov-2025-Georgetown-CRI.pdf).
- **Crowd-in is not driven by avoiding auto-enrollment.** Bloomfield et al. compare 2023 cohorts (whose new plans fall under SECURE 2.0's mandatory auto-enrollment rule) with California 2022. The start-plan effect was 11.1 pp in CO vs 9.6 pp in CA, and 8.1 pp in CT vs 9.9 pp in CA. The authors conclude "the desire to avoid automatic enrollment does not appear to be a major driver" ([NBER WP 32817](https://www.nber.org/papers/w32817), Table 9).

### Evidence verdict
- **State mandates:** strong causal evidence (quasi-experimental, using administrative tax data) that they raise employer-plan offering. There is no crowd-out, and coverage gains go beyond the auto-IRA programs themselves.
- **Auto-IRA saving outcomes:** moderate evidence that they produce saving, mainly short-horizon saving with heavy leakage.
- **Federal §45E startup credits:** strong evidence of very low take-up (1–5.5%) and so weak evidence of any effect on plan formation.

### Gaps
- IRS SOI publishes Form 8881 counts only for **C corporations** (Form 3800 Part III line 1j in the corporation line-item estimates): about 115–730 returns a year, 2009–2022 (729 returns, $741K in TY2022; 476 in 2021; 457 in 2018). Pass-through credits (S corps, partnerships, sole proprietors, the main claimants) are excluded, and individual line-item estimates (Pub. 4801) do not show the line. See `output/irs_form8881_credit_claims.csv`. So the all-entity series still comes only from the IRS-data academic study (about 18,000 firms in 2023).
- No JCT ex-post evaluation.
- No causal study yet of SECURE 2.0 §102 (2023+) on plan starts.
- Published crowd-in estimates use data only through 2023.

---

## 3. National coverage trend (BLS NCS, private industry, March reference)

### Takeaway
Private-industry access to any retirement plan rose from 67% (2019) to 72% (2024–2026). DC access rose from 64% to 70%. Gains were largest at establishments with fewer than 50 workers (50% to 55%) and among the lowest-paid quarter (43% to 52% in 2024, then 48% in 2026). But participation barely moved: 52% (2019) versus 52–53% (2023–2026). Take-up fell from 77% to 72%, so newly covered workers are joining less often. Part-time access peaked at 47% in 2024–25 and fell to 44% in March 2026. Part-time take-up fell to 46%, the lowest in the series.

### Cited findings
- Private industry, all retirement plans, access/participation/take-up:
  - 2019: 67/52/77
  - 2024: 72/53/73
  - 2025: 72/53/73
  - 2026: 72/52/72
  - DC only: 64/47/74 in 2019 and 70/49/70 in 2026.
  - Source: [BLS NCS database (nb), series NBU29000000000000028319 / …26320 / …32321 and NBU22000000000000028312 / NBU29000000000000026313 / …32314](https://download.bls.gov/pub/time.series/nb/), downloaded 2026-10-04 (file dated 9/25/2026).
- Establishments with <50 workers, all retirement: 50/36/72 (2019) → 55/38/70 (2024) → 55/37/67 (2026). With 50–99 workers: 67/46/69 (2019) → 72/46/63 (2026). Source: same database, subcells 02 and 04.
- **Payroll-deduction IRA access** (the closest NCS concept to an auto-IRA) has been flat: 4–6% of private workers, 2012–2022 (series NBU25100000000000033381; discontinued after 2022). **Does NCS count state auto-IRAs?** BLS publishes no explicit statement (checked 2026-10-05: NCS glossary, Q&A page, Handbook of Methods, MLR/Beyond the Numbers lists). The closest definitions point to **no**:
  - The current glossary puts payroll-deduction IRAs under "Other retirement benefits", not DB or DC plans: "Payroll deduction IRA. This plan is established by the employer on behalf of the employee, but with no employer contributions… the employee authorizes a payroll deduction by the employer. As long as the employer's involvement is minimal, the plan is not treated as an employer-sponsored retirement plan" ([NCS Glossary of Employee Benefit Terms, modified Sep 26 2026](https://www.bls.gov/ebs/publications/national-compensation-survey-glossary-of-employee-benefit-terms.htm)). A state auto-IRA (Roth IRA, no employer contribution, employer only remits payroll deductions) fits this description.
  - The glossary also lists "Savings with no employer contributions" (401(k)/403(b)/457 arrangements with no employer money) under "Other retirement benefits", with its own access series (provision 361: 18% of private workers in 2010, 11% in 2026). BLS said in 2009: "Technically, these plans are defined contribution plans, but because they do not include employer funds, the NCS distinguishes these plans from more traditional defined contribution plans" ([TED, Mar 12 2009](https://www.bls.gov/opub/ted/2009/mar/wk2/art04.htm)). The 2009 glossary defined DC plans as plans "that specify the level of employer contributions" ([NCS glossary, July 2009](https://www.bls.gov/ebs/publications/pdf/national-compensation-survey-glossary-of-employee-benefit-terms-2008-2009.pdf)).
  - Caveat: the current glossary's DC type list includes "individual retirement accounts (IRA, including traditional and Roth)", so the boundary is not fully clear. To settle it, ask BLS (NCSInfo@bls.gov).
  - Implication: NCS most likely **excludes** auto-IRA coverage, so it would understate gains in mandate states. The firm-sponsored plans that mandates crowd in (§2) are counted.
- **Method break:** the March 2009 release says "The NCS has broadened the definition of access to retirement benefits." Private access jumps from 61% (2008) to 67% (2009) with participation unchanged at 51%. Pre-2009 rows in the CSV are flagged as not strictly comparable. Source: [BLS, Employee Benefits in the United States, March 2009 (USDL news release)](https://www.bls.gov/news.release/archives/ebs2_07282009.htm). 2003 figures are "Recalculated" ([BLS Bulletin 2573](https://www.bls.gov/ebs/publications/pdf/bulletin-2573-january-2005-employee-benefits-in-private-industry-in-the-united-states-2002-2003.pdf)). For 2003–2005 the take-up rate is Computed as participation ÷ access from rounded published figures.
- Share of private establishments offering retirement benefits: 47% (2010) → 51% (2019) → 54% (2021) → 52% (2024); for <50-worker establishments, 44% → 48% → 52% → 49%. Source: nb series NBU29000000000000027370 and …0227370, saved in `raw/stateira/ncs_establishments_offering.csv`.

- **IRS W-2 administrative data show national deferral participation rising, unlike NCS.** The share of taxpayers with W-2 wages who made an elective deferral (box 12 codes D, E, F, G, H, S, AA, BB, EE) went from 34.7% (TY2008) and 33.5% (2010) to 37.6% (2015), 41.7% (2018), 42.2% (2019) and **42.8% (2020)**. The share with the box-13 retirement-plan indicator or a deferral went from 49.4% to 53.6%. By age, under-26s went from 12.1% to 20.8% and ages 26–34 from 33.6% to 44.4%: the largest gains are among young workers, the group auto-enrollment affects most. Within nominal wage bins the gains are smaller (for example, $30–40K: 42.7% to 44.1%; $50–75K: 59.3% to 60.7%), so part of the aggregate rise reflects nominal wage growth pushing workers into higher bins. 2020 also reflects COVID job losses among low earners. The data cover private and public employers, and filers only. Source: [IRS SOI, Form W-2 Statistics, Table 3.C, TY2008–2018 (18inallw2.xls), TY2019 (19in03w2all.xlsx), TY2020 (20in03w2all.xlsx)](https://www.irs.gov/statistics/soi-tax-stats-individual-information-return-form-w2-statistics); **Computed** percentages are in `output/irs_w2_deferral_participation.csv`. TY2021+ not yet published (the TY2020 tables are dated January 2026).
- **Census-IRS linked W-2 study (NBER w32843, Choukhmane, Colmenares, O'Dea, Rothbaum & Schmidt, Aug 2024 rev. Jun 2026)** does not report a national participation trend. Its pooled 2008–2017 large-employer (Form 5500-linked) sample shows a "Participation dummy" of 65.1% (Table 1), and it cites NCS 2017: full-time civilian workers "68% have access to, and 48% participate in a DC plan" ([NBER w32843](https://www.nber.org/papers/w32843)).

### Evidence verdict
**Moderate evidence that access is expanding**, concentrated in small firms and low-wage jobs, which fits a contribution from state mandates, SECURE credits and PEPs. **NCS shows no rise in participation rates, but IRS W-2 data do:** the share of wage earners deferring rose about 8 points from 2010 to 2020, most among under-35s. The two sources differ in unit (jobs vs. tax-filing persons), sector (private only vs. all employers) and measure (participation as BLS defines it vs. any positive deferral), so the W-2 rise is **moderate evidence** that participation grew nationally as auto-enrollment spread, partly offset by nominal wage-bin drift. NCS is descriptive, so these changes cannot be attributed to any one policy.

### Gaps
- NCS does not break results out by state, so mandate and non-mandate states cannot be compared.
- Sampling error is large for subcells; year-to-year changes of 1–3 pp are often not significant.
- Possible questionnaire changes after 2020 were not checked.

---

## 4. Small-plan formation (Form 5500) and pooled employer plans

### Takeaway
DOL Form 5500 counts show DC plan formation accelerated after 2019. Total DC plans grew 1–2% a year in 2016–2019, then 2.7% (2021), 5.0% (2022) and 4.7% (2023). Plans with fewer than 100 participants are about 88% of DC plans and grew 15.7% from 2019 to 2023, versus 5.5% from 2015 to 2019 (Computed). The timing fits state mandate waves (CA 2022) and SECURE 2.0 credits (2023), but the DOL data do not attribute causes; Bloomfield et al. and Pew supply the attribution evidence. PEPs grew fast from a small base: 81 filings (2021) → 269 (2023), 1.16M participants, $11.8B in assets and 39,446 participating employers (96.6% with fewer than 100 employees) in 2023.

### Cited findings
- Number of DC plans, total / with <100 participants:
  - 2019: 686,809 / 600,165
  - 2020: 700,034 / 613,290
  - 2021: 718,736 / 630,423
  - 2022: 754,862 / 663,107
  - 2023: 790,610 / 694,637
  - Source: [DOL EBSA, Private Pension Plan Bulletin Historical Tables and Graphs 1975–2023, Sept 2025, Tables E1 and E2](https://www.dol.gov/agencies/ebsa/researchers/statistics/retirement-bulletins/private-pension-plan-bulletins) (local copy `dc_stay/raw/hist.txt`). Excludes one-participant plans.
- Participants in small (<100) DC plans: 12.51M (2019) → 14.27M (2023), +14.0% (Computed). Source: Table E5.
- **Caveat:** starting with 2023 filings, DOL changed the participant-count rule for the small/large-plan threshold (count only participants with account balances). That can move plans into the "small" category for filing purposes. DOL's rule estimated the effect (2020 filings as a proxy): "Using the current definitions of large and small plans, there are 86,744 large defined contribution plans and 613,290 small… [the new methodology] yields estimated 68,057 large and 631,976 small defined contribution plans," i.e. "18,699 large plans would be redefined and file as small plans" ([DOL/IRS/PBGC, Annual Reporting and Disclosure final rule, 88 FR, Feb 24 2023](https://www.govinfo.gov/content/pkg/FR-2023-02-24/html/2023-02652.htm)). The 2023 Private Pension Plan Bulletin (Jan 2026, v1.1) has no appendix or note on the change and tabulates size by "Total Participants… as of the end of the plan year" ([PPB Abstract of 2023 Form 5500 Annual Reports](https://www.dol.gov/sites/dolgov/files/ebsa/researchers/statistics/retirement-bulletins/private-pension-plan-bulletins-abstract-2023.pdf), Tables A1(a)/(b)). **Computed check:** if the bulletin had switched to the filing threshold, about 19,000 DC plans (about 20% of large plans) would have moved from large to small in 2023. Instead, DC plans with 100+ participants **rose** from 91,755 (2022) to 95,973 (2023), +4.6%, while those under 100 rose 4.8% (663,107 to 694,637), the same pace as 2022 (+5.2%). The bulletin's size classes therefore appear unaffected, and the "+15.7% small DC plans 2019–2023" finding is **not an artifact of the counting change**. This is inferred from the numbers; DOL makes no explicit statement.
- **Pooled plan providers (Form PR):** 31 registered (2020); 88 (2021); 119 (2022); 143 (2023); 167 (2024). Only 71 of the 143 registered in 2023 were operating a PEP. Source: [DOL EBSA, 2026 Pooled Employer Plan Bulletin, Tables I.1 and III.1](https://www.dol.gov/agencies/ebsa/researchers/statistics/retirement-bulletins/pooled-employer-plan-bulletin/2026).
- **PEP Form 5500 filings and size:**
  - 2021: 81 PEPs; 179k participants; $1.53B assets.
  - 2022: 190 PEPs; 618k participants; $4.97B assets.
  - 2023: 269 PEPs (244 active); 1.155M participants; $11.76B assets.
  - 2023 employers: 39,446 unique participating employers (Schedule MEP), median 7 per PEP; "96.6% had under 100 employees."
  - Sources: [DOL 2025 PEP Bulletin](https://www.dol.gov/agencies/ebsa/researchers/statistics/retirement-bulletins/pooled-employer-plan-bulletin/2025); 2026 PEP Bulletin. **Computed:** PEP participants were about 1.2% of 2023 DC participants (1.155M ÷ about 95M; the DC participant total is approximate and **unverified** for 2023).

### Evidence verdict
- **Plan formation:** moderate evidence of faster small-plan formation after 2019. It is consistent with policy effects but not, from DOL data alone, attributable to them.
- **PEPs:** moderate evidence of take-off, but they are still small relative to the market.

### Gaps
- DOL does not publish counts of new plans by year. A new-plan series needs Form 5500 microdata (first-filing indicator) or the Pew and Bloomfield datasets.
- 2024 Form 5500 aggregates are not yet in the bulletin.
- No causal study of PEPs' effect on coverage.

---

## 5. Long-term part-time (LTPT) eligibility

### Takeaway
There is no direct evaluation yet. SECURE's 3-year LTPT rule first produced eligible employees in 2024. SECURE 2.0's 2-year rule took effect for plan years beginning in 2025, with eligibility from 1 Jan 2025 or 2026 depending on service years. NCS part-time access rose from 39% (2019) to 47% (2024–2025), then fell to 44% in March 2026. Part-time DC take-up fell to 41% (2026), so any LTPT-driven access gain is not visible yet as higher participation. LTPT employees need not be auto-enrolled or receive a match, so low take-up is expected.

### Cited findings
- Part-time private workers, all retirement access/participation/take-up:
  - 2019: 39/22/57
  - 2023: 44/22/51
  - 2024: 47/24/51
  - 2025: 47/23/49
  - 2026: 44/20/46
  - DC only, 2026: 41/17/41.
  - Source: [BLS NCS nb series NBU29000000000002628319 / …2626320 / …2632321; NBU22000000000002628312](https://download.bls.gov/pub/time.series/nb/).
- Full-time workers: access 77% (2019) → 81% (2026); participation 61% → 62% (same source).
- LTPT rules: SECURE 2.0 cut the service requirement from three consecutive years of 500+ hours to two, effective 2025. Employer contributions are not required. Source: [IRS/industry summaries, e.g., Fidelity plan sponsor note](https://sponsor.fidelity.com/pspublic/pca/psw/public/library/manageplans/long_part_time_ee_eligible_to_participate.html) [recordkeeper/industry].
- I found no recordkeeper survey that quantifies LTPT enrollment; Vanguard How America Saves 2026 has no LTPT statistics [recordkeeper/industry].

### Evidence verdict
**No direct evidence; weak indirect evidence.** Part-time access rose through 2025, but participation did not, and both access and participation fell in 2026.

### Gaps
- NCS cannot isolate workers who are LTPT-eligible.
- Recordkeeper data on LTPT enrollment are needed.
- Many plans already let part-timers in, which limits the rule's reach.

---

## Chart-ready series

### A. BLS NCS, private industry, all retirement plans (%, March)
Full series: `output/bls_ncs_access_participation.csv`. Source: https://download.bls.gov/pub/time.series/nb/; pre-2009 rows come from BLS bulletins and news releases.

| Year | Access | Participation | Take-up | Source |
|---|---|---|---|---|
| 2003 | 57 | 49 | 86 (Computed) | https://www.bls.gov/ebs/publications/pdf/bulletin-2573-january-2005-employee-benefits-in-private-industry-in-the-united-states-2002-2003.pdf |
| 2005 | 60 | 50 | 83 (Computed) | https://www.bls.gov/ebs/publications/pdf/employee-benefits-in-private-industry-in-the-united-states-march-2005.pdf |
| 2007 | 61 | 51 | 84 | https://www.bls.gov/ebs/publications/pdf/employee-benefits-in-private-industry-in-the-united-states-march-2007.pdf |
| 2008 | 61 | 51 | 83 | https://www.bls.gov/news.release/archives/ebs2_08072008.htm |
| 2009 (break) | 67 | 51 | 77 | https://www.bls.gov/news.release/archives/ebs2_07282009.htm |
| 2010 | 65 | 50 | 76 | nb |
| 2013 | 64 | 49 | 76 | nb |
| 2016 | 66 | 50 | 76 | nb |
| 2019 | 67 | 52 | 77 | nb |
| 2020 | 67 | 51 | 76 | nb |
| 2021 | 68 | 51 | 75 | nb |
| 2022 | 69 | 52 | 75 | nb |
| 2023 | 70 | 53 | 75 | nb |
| 2024 | 72 | 53 | 73 | nb |
| 2025 | 72 | 53 | 73 | nb |
| 2026 | 72 | 52 | 72 | nb |

### B. NCS access to any retirement plan by group (%)
Source: nb.

| Year | <50 workers | 50–99 | 100+ | Part-time | Lowest 25% wage |
|---|---|---|---|---|---|
| 2010 | 47 | 64 | 81 | 39 | 40 |
| 2015 | 46 | 66 | 84 | 37 | 40 |
| 2019 | 50 | 67 | 84 | 39 | 43 |
| 2021 | 52 | 70 | 85 | 41 | 44 |
| 2023 | 53 | 71 | 86 | 44 | 48 |
| 2024 | 55 | 70 | 89 | 47 | 52 |
| 2025 | 55 | 71 | 88 | 47 | 49 |
| 2026 | 55 | 72 | 87 | 44 | 48 |

### C. State auto-IRA programs, all states combined (CRI)
Source: https://cri.georgetown.edu/states/state-data/historical-trends/ (Datawrapper 3qNsH v23 and 9D4fC v28). Totals are Computed as sums across states.

| Date | Funded accounts | Assets ($M) |
|---|---|---|
| Dec 2018 | 26,385 | 11.4 |
| Dec 2019 | 108,945 | 54.8 |
| Dec 2020 | 263,764 | 160.1 |
| Dec 2021 | 429,663 | 407.9 |
| Dec 2022 | 635,395 | 641.9 |
| Dec 2023 | 822,360 | 1,204.1 |
| Dec 2024 | 978,715 | 1,828.2 |
| Dec 2025 | 1,159,942 | 2,695.4 |
| Aug 2026 | 1,413,435 | 3,393.2 |

### D. Auto-IRA participation and leakage indicators (%)

| Program | Opt-out (as defined) | Participation (Computed = 100 − opt-out) | Withdrawals ÷ cumulative contributions (Computed) | As of | Source |
|---|---|---|---|---|---|
| CalSavers | 34.4 (effective) | 65.6 | 32.3 | 2026-08-31 | https://www.treasurer.ca.gov/sites/default/files/calsavers/August_2026_Participation_Snapshot_Report.pdf |
| OregonSaves | 26.5 (0–30 days) | 73.5 | 41.1 | 2026-07-31 | https://www.oregon.gov/treasury/Upward-Oregon/Shared%20Documents/Board-Meeting-Minutes/Program-Reports/2026/2026-07-Program-Report-OregonSaves-Monthly.pdf |
| OregonSaves (12-month, academic) | ~50 | ~50 | ~33 (through Dec 2023) | 2024 | https://www.jonreuter.com/research/ORSP_202406.pdf |

### E. DOL Form 5500: number of DC plans (excludes one-participant plans)
Source: DOL Private Pension Plan Bulletin Historical Tables 1975–2023, Tables E1 and E2, https://www.dol.gov/agencies/ebsa/researchers/statistics/retirement-bulletins/private-pension-plan-bulletins.

| Year | Total DC plans | YoY % (Computed) | DC plans <100 participants | YoY % (Computed) |
|---|---|---|---|---|
| 2016 | 656,241 | 1.2 | 574,772 | 1.1 |
| 2017 | 662,829 | 1.0 | 580,315 | 1.0 |
| 2018 | 675,007 | 1.8 | 590,254 | 1.7 |
| 2019 | 686,809 | 1.7 | 600,165 | 1.7 |
| 2020 | 700,034 | 1.9 | 613,290 | 2.2 |
| 2021 | 718,736 | 2.7 | 630,423 | 2.8 |
| 2022 | 754,862 | 5.0 | 663,107 | 5.2 |
| 2023 | 790,610 | 4.7 | 694,637 | 4.8 |

### F. Pooled employer plans (DOL)
Sources: https://www.dol.gov/agencies/ebsa/researchers/statistics/retirement-bulletins/pooled-employer-plan-bulletin/2025 and /2026.

| Year | Registered PPPs | PEPs filing 5500 | PEP participants | PEP assets ($B) |
|---|---|---|---|---|
| 2020 | 31 | n/a | n/a | n/a |
| 2021 | 88 | 81 | 179,000 | 1.53 |
| 2022 | 119 | 190 | 618,000 | 4.97 |
| 2023 | 143 | 269 | 1,155,000 | 11.76 |
| 2024 | 167 | n/a | n/a | n/a |

### G. IRS W-2: share of wage earners with an elective deferral (%, Computed)
Source: https://www.irs.gov/statistics/soi-tax-stats-individual-information-return-form-w2-statistics (Table 3.C). Full table: `output/irs_w2_deferral_participation.csv`.

| Tax year | Any elective deferral | Box 13 plan indicator | Indicator or deferral | Deferral, under 26 | Deferral, 26–34 |
|---|---|---|---|---|---|
| 2008 | 34.7 | 46.3 | 49.4 | 12.1 | 33.6 |
| 2009 | 33.8 | 46.1 | 49.1 | 11.7 | 31.3 |
| 2010 | 33.5 | 44.9 | 48.1 | 11.8 | 31.5 |
| 2011 | 33.9 | 44.8 | 47.9 | 11.9 | 32.2 |
| 2012 | 34.9 | 45.2 | 48.3 | 12.9 | 33.4 |
| 2013 | 35.4 | 45.0 | 48.3 | 13.3 | 34.0 |
| 2014 | 36.5 | 45.5 | 49.0 | 14.5 | 35.2 |
| 2015 | 37.6 | 46.1 | 49.7 | 15.5 | 36.9 |
| 2016 | 38.8 | 47.1 | 50.6 | 16.5 | 38.7 |
| 2017 | 39.9 | 47.1 | 51.1 | 17.3 | 40.4 |
| 2018 | 41.7 | 48.8 | 52.8 | 18.9 | 43.1 |
| 2019 | 42.2 | 49.0 | 53.1 | 20.1 | 43.8 |
| 2020 | 42.8 | 49.7 | 53.6 | 20.8 | 44.4 |
