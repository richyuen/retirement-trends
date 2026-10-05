# US federal provisions affecting DC plan participation and keeping money in DC plans (map, 1978 to Oct 2026)

Worker: `laws` | Compiled 2026-10-04 | Machine-readable copy: `dc_policy/output/provisions_timeline.csv` (67 rows, same columns as the master table below)

**Sourcing.** Statute text comes from govinfo.gov Public Law HTML. Effective-date clauses were extracted verbatim from each section by script. Regulations come from the Federal Register API (federalregister.gov) and govinfo FR text. IRS guidance comes from irs.gov PDFs, and state programs from the Georgetown CRI tracker. The Senate Finance SECURE 2.0 section-by-section (Dec 19 2022) was used to cross-check and is saved at `dc_policy/raw/laws/senate_finance_secure2_section_by_section_2022-12-19.pdf`. congress.gov and crsreports.congress.gov returned 403 from this environment, so CRS material was read from everycrsreport.com instead.

**Category key.** *participation* means the provision gets people into plans: auto-enrollment, coverage, eligibility, small-employer credits. *contribution* means it raises how much people save. *staying-in-plan* means it keeps assets in plans or tax-deferred longer: rollovers/portability, RMD age, anti-leakage. *leakage-increasing* means it makes pre-retirement withdrawals easier or cheaper, or shortens deferral, which cuts against staying in plans.

**Direction column.** + means it pushes toward more participation, more saving or more retention. - means it pushes toward more leakage or less deferral. +/- means mixed. 0 means neutral.

## 1. Participation: from permission to mandate

### Takeaway
Auto-enrollment went through four stages:
1. **Permitted by IRS ruling:** Rev. Rul. 98-30 (1998) for new hires; Rev. Rul. 2000-8 for current employees.
2. **De-risked by PPA 2006:** QACA/EACA safe harbors, ERISA 514(e) preemption of state wage-withholding laws, and the QDIA reg effective Dec 24 2007.
3. **Sweetened:** SECURE 2019 Sec. 105 auto-enrollment credit, and the 15% QACA cap in Sec. 102.
4. **Mandated for new 401(k)/403(b) plans:** SECURE 2.0 Sec. 101, plan years beginning after Dec 31 2024.

The federal workforce got the mandate first. FERS new hires have been auto-enrolled since Aug 1 2010 (3% default), and the default rose to 5% on Oct 1 2020. Uniformed services have been auto-enrolled at 3% since Jan 1 2018. Eligibility was also widened to part-timers: 3 years of 500+ hours (SECURE Sec. 112, first entrants 2024), cut to 2 years (SECURE 2.0 Sec. 125, from 2025).

### Cited findings
- Rev. Rul. 98-30 is listed in IRB 1998-25 (June 22 1998), p. 8, as "Qualified cash or deferred arrangement; participation" — [IRB 1998-25](https://www.irs.gov/pub/irs-irbs/irb98-25.pdf). CRS: automatic enrollment "is permissible for newly hired employees" (98-30) and "for current employees who have not already enrolled" (2000-8). It is also permitted in 403(b) (Rev. Rul. 2000-35), 457(b) (Rev. Rul. 2000-33) and prototype plans (Ann. 2000-60) — [CRS RS21954, Jan 16 2007](https://www.everycrsreport.com/reports/RS21954.html).
- PPA Sec. 902 QACA defaults are "3 percent", "4 percent during the first plan year following", "5 percent during the second", and "6 percent during any subsequent plan year". The match is "100 percent of the elective contributions ... [up to] 1 percent of compensation plus 50 percent of so much ... as exceeds 1 percent but does not exceed 6 percent". Vesting is full after "2 years of service". Effective "plan years beginning after December 31, 2007, except that the amendments made by subsection (f) [ERISA preemption] shall take effect on the date of the enactment" (Aug 17 2006) — [P.L. 109-280](https://www.govinfo.gov/content/pkg/PLAW-109publ280/html/PLAW-109publ280.htm).
- QDIA final rule: 72 FR 60452, effective 2007-12-24 — [Federal Register](https://www.federalregister.gov/documents/2007/10/24/07-5147/default-investment-alternatives-under-participant-directed-individual-account-plans).
- TSP Enhancement Act 2009 Sec. 102: "the default percentage shall be equal to 3 percent or such other percentage, not less than 2 percent nor more than 5 percent, as the Board may prescribe" — [P.L. 111-31](https://www.govinfo.gov/content/pkg/PLAW-111publ31/html/PLAW-111publ31.htm). FRTIB implementing rule effective 2010-08-01 — [75 FR 43799](https://www.federalregister.gov/documents/2010/07/27/2010-18346/employee-contribution-elections-and-contribution-allocations). FRTIB raised the rate "from 3 percent to 5 percent of basic pay for all participants who are automatically enrolled ... on or after October 1, 2020" — [85 FR 57665](https://www.federalregister.gov/documents/2020/09/16/2020-17811/automatic-enrollment-program).
- SECURE 2.0 Sec. 101 (new IRC 414A) sets the initial default at "not less than 3 percent and not more than 10 percent". It rises by "1 percentage point (to at least 10 percent, but not more than 15 percent)". The default must be invested per 29 CFR 2550.404c-5 (QDIA). Exempt: arrangements "established before the date of the enactment", "governmental plan ... or any church plan", SIMPLE plans, employers "in existence for less than 3 years", and until 1 year after the employer "normally employed more than 10 employees". Effective "plan years beginning after December 31, 2024" — [P.L. 117-328 Div. T](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm).
- **414A regulation status (verified 2026-10-04):**
  - Proposed regs were published Jan 14 2025 ([90 FR 3092](https://www.federalregister.gov/documents/2025/01/14/2025-00501/automatic-enrollment-requirements-under-section-414a)). They "would apply to plan years that begin more than 6 months after the date that final regulations under section 414A are issued. For earlier plan years, a plan would be treated as having complied ... if the plan complies with a reasonable, good faith interpretation" ([govinfo text](https://www.govinfo.gov/content/pkg/FR-2025-01-14/html/2025-00501.htm)).
  - Draft final regs (RIN 1545-BR08, "Automatic Enrollment Requirements Under Section 414A", stage "Final Rule") were received by OIRA on **2026-06-23** and were still listed as under EO 12866 review in OIRA's pending-review file run 2026-10-04 — [reginfo.gov, EO rules under review (XML)](https://www.reginfo.gov/public/do/XMLViewFileAction?f=EO_RULES_UNDER_REVIEW.xml) (verified by gapB 2026-10-05; it confirms the trade-press date). Treasury's Unified Agenda had targeted "Final Action 07/00/2026" — [reginfo.gov agenda entry](https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=1545-BR08).
  - A Federal Register API search for "414A" shows **no final rule published** as of 2026-10-04. The answer to "final regs issued Jan 2025?" is no: Jan 2025 was the *proposed* rule.
- LTPT:
  - SECURE Sec. 112 (3 years of 500+ hours) applies to plan years after 12/31/2020, but "12-month periods beginning before January 1, 2021, shall not be taken into account" — [P.L. 116-94](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm). That makes 2024 the first entry year (Computed: 2021-2023).
  - SECURE 2.0 Sec. 125 shortens this to "2 consecutive 12-month periods during each of which the employee has at least 500 hours of service", for plan years after 12/31/2024, and extends it to ERISA 403(b) plans.
  - Proposed regs were published Nov 27 2023 ([88 FR 82796](https://www.federalregister.gov/documents/2023/11/27/2023-25987/long-term-part-time-employee-rules-for-cash-or-deferred-arrangements-under-section-401k)). No final rule was found.
- Small-employer coverage tools:
  - SECURE Sec. 101 creates PEPs (plan years after 12/31/2020) and Sec. 104 raises the startup credit; Sec. 105 adds the $500 auto-enrollment credit.
  - SECURE 2.0 Sec. 102 raises the credit to 100% for employers with 50 or fewer employees, plus an employer-contribution credit capped at "$1,000" per employee. Sec. 121 adds Starter 401(k)s with a "3 or more than 15 percent" auto-enrollment band and a "$6,000" cap. Sec. 113 allows de minimis incentives.
  - DOL issued PEP interpretive guidance and an RFI toward a safe harbor (July 29 2025, [90 FR 35646](https://www.federalregister.gov/documents/2025/07/29/2025-14281/pooled-employer-plans-big-plans-for-small-businesses)).

### Evidence verdict
Out of scope for this worker; other workers cover the evidence. Short pointer: evidence that auto-enrollment raises participation at adopting plans is strong and positive (Madrian-Shea 2001 onward). Evidence on the SECURE 2.0 mandate is **none yet**. It binds only new plans, from 2025, and final regs are not out.

### Gaps
- The 414A final-rule OIRA receipt date (2026-06-23) is now verified on reginfo.gov (gapB, 2026-10-05).
- The Revenue Act 1978 effective-date clause is now text-verified (gapB): Sec. 135(c)(1), "The amendments made by this section shall apply to plan years beginning after December 31, 1979" — [92 Stat. 2787](https://www.govinfo.gov/content/pkg/STATUTE-92/pdf/STATUTE-92-Pg2763.pdf), pdf p.25. Sec. 135(c)(2) adds a transitional rule for arrangements in existence on June 27, 1974, for plan years beginning before January 1, 1980.
- No federal mandate covers existing plans or employers without plans. Coverage gaps are left to the states (Section 4).

## 2. Contribution levels

### Takeaway
Contribution levels have been pushed up mainly through defaults:
- the QACA escalator (PPA), with its cap raised from 10% to 15% (SECURE Sec. 102)
- the 414A default of at least 3%, escalating to at least 10% (SECURE 2.0 Sec. 101)
- the TSP default raised from 3% to 5% (2020)

Targeted incentives add to this: the Saver's Credit (2002), student-loan matching (2024), age 60-63 super catch-up (2025), and the refundable **Saver's Match from tax year 2027**, deposited into accounts from 2028.

### Cited findings
- SECURE 2.0 Sec. 103 (IRC 6433): match of "50 percent" of contributions up to "$2,000". Phase-out starts at an "applicable dollar amount [of] $41,000" with a "phaseout range [of] $30,000" for joint filers. Applies to "taxable years beginning after December 31, 2026" — [P.L. 117-328](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm).
- Implementation status:
  - Treasury/IRS Notice 2026-48 (IR-2026-89, Aug 7 2026) announces intent to propose regs, with comments due Oct 5 2026. Payments begin in 2028 for 2027 contributions — [IRS release](https://www.irs.gov/newsroom/treasury-irs-begin-implementing-executive-order-14403-by-announcing-intent-to-issue-proposed-regulations-on-savers-match-which-will-benefit-millions-of-low-and-moderate-income-taxpayers); [Notice 2026-48](https://www.irs.gov/pub/irs-drop/n-26-48.pdf).
  - EO 14403 (signed Apr 30 2026) creates TrumpIRA.gov, launching Jan 1 2027 — [91 FR 24329](https://www.federalregister.gov/documents/2026/05/05/2026-08908/promoting-retirement-savings-access-for-american-workers-by-establishing-trumpiragov).
  - **No proposed regulation had been published** as of 2026-10-04 (FR API search).
- Catch-ups:
  - Sec. 109 sets the age 60-63 limit at the greater of "$10,000" or "150 percent", for tax years after 12/31/2024.
  - Sec. 603 makes catch-ups Roth for high earners.
  - The final catch-up regs, published Sept 16 2025, are effective Nov 17 2025 and "generally apply with respect to contributions in taxable years beginning after December 31, 2026" — [90 FR 44527](https://www.federalregister.gov/documents/2025/09/16/2025-17865/catch-up-contributions).
- Student-loan match: SECURE 2.0 Sec. 110, plan years after 12/31/2023; [Notice 2024-63](https://www.irs.gov/pub/irs-drop/n-24-63.pdf).

### Evidence verdict
Out of scope here. TSP's own data on the 3% to 5% change is the cleanest natural experiment. There is no evidence yet on the Saver's Match.

### Gaps
- No Saver's Match proposed rule yet.
- How IRAs and plans will be designated to receive deposits is unresolved (Notice 2026-48 asks for comment).

## 3. Keeping money in plans / tax-deferred longer, and the provisions that cut the other way

### Takeaway
**Measures that keep money in plans or tax-deferred:**
- portability: EGTRRA rollovers (2002), and auto-rollover of $1,000-$5,000 force-outs to IRAs (from Mar 28 2005)
- auto-portability: statutory exemption effective Dec 29 2023, but the DOL implementing rule is **still only proposed (Jan 2024)**; the final rule (RIN 1210-AC21) has been at OIRA since 2026-09-14 (verified on reginfo.gov by gapB)
- the Lost & Found database (Dec 2024)
- loan-offset rollover extension (2018)
- the credit-card loan ban (2019)
- later RMD ages: 70½ to 72 (2020), to 73 (2023), to 75 (2033)
- the 2020 RMD waiver

**Measures that increase leakage (13 rows in the table; listed below):** at the same time, Congress has steadily added penalty-free withdrawal channels: hardship liberalization (2019), birth/adoption ($5,000, 2020), CARES CRDs (up to $100,000, 2020) and loans, emergency ($1,000/yr, 2024), domestic abuse (up to $10,000, 2024), terminal illness (Dec 2022), permanent disaster distributions ($22,000), and 403(b) hardship conformity (2024). SECURE's 10-year inherited-account rule shortens deferral for heirs.

**Mixed:** the force-out ceiling rose to $7,000 (2024). More small balances can be pushed out of employer plans, though $1,000+ balances still default into IRAs.

### Cited findings
- EGTRRA Sec. 657 applies "to distributions made after final regulations implementing subsection (c)(2)(A) are prescribed" — [P.L. 107-16](https://www.govinfo.gov/content/pkg/PLAW-107publ16/html/PLAW-107publ16.htm). DOL safe harbor: 69 FR 58018 (Sept 28 2004), **effective 2005-03-28** — [FR](https://www.federalregister.gov/documents/2004/09/28/04-21591/fiduciary-responsibility-under-the-employee-retirement-income-security-act-of-1974-automatic). See also [IRS Notice 2005-5](https://www.irs.gov/pub/irs-drop/n-05-05.pdf).
- SECURE 2.0 Sec. 304 strikes "$5,000" and inserts "$7,000" for "distributions made after December 31, 2023".
- Auto-portability (Sec. 120): applies to "transactions occurring on or after the date which is 12 months after the date of the enactment", which is 2023-12-29.
  - The DOL proposed rule was published Jan 29 2024 ([89 FR 5624](https://www.federalregister.gov/documents/2024/01/29/2024-01208/automatic-portability-transaction-regulations)). The FR API (searched 2026-10-04) shows **no final rule**.
  - Before the statute: DOL individual exemption for Retirement Clearinghouse, July 31 2019 ([84 FR 37337](https://www.federalregister.gov/documents/2019/07/31/2019-16237/notice-of-exemption-involving-retirement-clearinghouse-llc-rch-or-the-applicant-located-in-charlotte)).
- Lost & Found (Sec. 303): DOL was to establish the database "Not later than 2 years after the date of the enactment". OMB approved data collection on Nov 20 2024 ([89 FR 91787](https://www.federalregister.gov/documents/2024/11/20/2024-27098/retirement-savings-lost-and-found)). Live at [lostandfound.dol.gov](https://lostandfound.dol.gov/).
- RMD ages:
  - SECURE Sec. 114 applies to individuals "who attain age 70 1/2 after" Dec 31 2019.
  - SECURE 2.0 Sec. 107: "age 72 after December 31, 2022, and age 73 before January 1, 2033, the applicable age is 73 ... attains age 74 after December 31, 2032, the applicable age is 75".
  - Final RMD regs: [89 FR 58886](https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions), effective 2024-09-17.
- CARES Act Sec. 2202:
  - CRDs are capped at "$100,000", made "on or after January 1, 2020, and before December 31, 2020", to people with COVID diagnosis or "adverse financial consequences". Income is "ratably over the 3-taxable-year period" and repayable within 3 years. The plan administrator "may rely on an employee's certification".
  - Loans: "$100,000" substituted for "$50,000" for 180 days after enactment.
  - Sec. 2203 waived 2020 RMDs — [P.L. 116-136](https://www.govinfo.gov/content/pkg/PLAW-116publ136/html/PLAW-116publ136.htm); [Notice 2020-50](https://www.irs.gov/pub/irs-drop/n-20-50.pdf), [Notice 2020-51](https://www.irs.gov/pub/irs-drop/n-20-51.pdf).
- SECURE 2.0 withdrawal channels:
  - Sec. 115 emergency: "the lesser of $1,000" per calendar year, after 12/31/2023.
  - Sec. 314 domestic abuse: "lesser of-- (I) $10,000, or (II) 50 percent".
  - Sec. 326 terminal illness: after enactment.
  - Sec. 331 disaster: "shall not exceed $22,000".
  - Sec. 602: 403(b) hardship rules conformed.
  - Guidance: [Notice 2024-55](https://www.irs.gov/pub/irs-drop/n-24-55.pdf).
- PLESAs (Sec. 127):
  - Auto-enrollment at "not more than 3 percent".
  - Balance cap "$2,500".
  - Withdrawals "at least once per calendar month", with "the first 4 withdrawals ... in a plan year" free of fees.
  - Plan years after 12/31/2023; [Notice 2024-22](https://www.irs.gov/pub/irs-drop/n-24-22.pdf).
  - PLESAs are designed as a buffer so workers don't tap the 401(k), but they are themselves a liquid channel. I classed them as leakage-increasing with direction +/-.
- BBA 2018 Secs. 41113-41114 delete "the 6-month prohibition on contributions" after hardship withdrawals and expand withdrawable sources. Final regs [84 FR 49651](https://www.federalregister.gov/documents/2019/09/23/2019-20511/hardship-distributions-of-elective-contributions-qualified-matching-contributions-qualified) (Sept 23 2019).
- TSP Modernization Act 2017 took effect "on the date on which the regulations ... take effect", which was **2019-09-15** ([84 FR 46419](https://www.federalregister.gov/documents/2019/09/04/2019-19029/additional-withdrawal-options)). FRTIB later removed the 30-day wait between withdrawals ([89 FR 18533](https://www.federalregister.gov/documents/2024/03/14/2024-05346/removal-of-30-calendar-day-waiting-period-between-withdrawals), effective 2024-05-15).

### Evidence verdict
Out of scope here. Note for synthesis: the statutory trend is **two-directional**. Default/retention tools were added alongside at least 9 new or broadened penalty-free withdrawal exceptions since 2018. Count (Computed from table): BBA hardship, QBAD, CRD, CARES loans, emergency, domestic abuse, terminal illness, disaster, and 403(b) hardship.

### Gaps
- Auto-portability final rule and Lost & Found usage statistics: none in the Federal Register as of 2026-10-04. The final rule (RIN 1210-AC21, "Exemption for Certain Automatic Portability Transactions", economically significant) was received by OIRA on 2026-09-14 and is under review — [reginfo.gov pending EO 12866 reviews](https://www.reginfo.gov/public/do/XMLViewFileAction?f=EO_RULES_UNDER_REVIEW.xml) (gapB). Check DOL/Portability Services Network releases for usage.
- No federal data source tracks use of the new 72(t) exceptions (Form 5329 codes might).

## 4. State auto-IRA mandates (dates only)

### Takeaway
As of 2026, 22 states and 3 cities have enacted programs for private-sector workers; 17 states plus Philadelphia use the auto-IRA (mandatory employer facilitation) model. Programs launched between 2017 (Oregon) and 2026 (Minnesota). Hawaii, Washington and Philadelphia are pending for 2026-2027. Several states lowered employer-size thresholds in 2026: NJ from 25 to 10, and VA from 25 to 5.

A federal DOL safe harbor for these programs existed only from Oct 31 2016 ([81 FR 59464](https://www.federalregister.gov/documents/2016/08/30/2016-20639/savings-arrangements-established-by-states-for-non-governmental-employees)) until Congress disapproved it on May 17 2017 ([P.L. 115-35](https://www.govinfo.gov/content/pkg/PLAW-115publ35/html/PLAW-115publ35.htm)).

**Sources.** Enactment years: [Georgetown CRI State Brief 23-03, June 30 2023](https://cri.georgetown.edu/wp-content/uploads/2023/03/cri-state-brief-snapshot.pdf), p. 5, plus the 2024-2026 enactments on the CRI tracker. Launch dates and waves: [Georgetown CRI State Programs page, accessed 2026-10-04](https://cri.georgetown.edu/states/).

| State (program) | Enacted | Pilot / open to all employers | Employer-size registration waves (deadlines) |
|---|---|---|---|
| Oregon (OregonSaves) | 2015 | pilot 2017-07-01; all 2017-10-01 | 100+ (11/15/2017); 50-99 (5/15/2018); 20-49 (12/15/2018); 10-19 (5/15/2019); 5-9 (11/2019); 3-4 (3/1/2023); 1-2 (7/31/2023) |
| Illinois (Secure Choice, now "My Illinois Savings") | 2015 | pilot May 2018; all Oct 2018 | >500 (Nov 2018); 100-499 (Jul 2019); 25-99 (Nov 2019); 16-24 (11/1/2022); 5-15 (11/1/2023) |
| California (CalSavers) | 2016 | pilot Nov 2018; all 2019-07-01 | 100+ (9/30/2020); 50+ (6/30/2021); 5+ (6/30/2022); 1-4 (12/31/2025) |
| Connecticut (MyCTSavings) | 2016 | pilot 2021-10-25; all 2022-04-01 | 100+ (6/30/2022); 26-99 (10/31/2022); 5-25 (3/30/2023) |
| Maryland (MarylandSaves) | 2016 | pilot Mar 2022; all 2022-09-15 | all covered (12/1/2022) |
| New Jersey (RetireReady NJ) | 2019 (as amended) | pilot May 2024; all 2024-06-30 | 40+ (9/15/2024); 25-39 (11/15/2024); threshold lowered to 10 by law of 2026-01-20 |
| Colorado (Secure Savings) | 2020 | pilot 2022-10-17; all 2023-01-18 | 50+ (3/15/2023); 15-49 (5/15/2023); 5-14 (6/30/2023) |
| Virginia (RetirePathVA) | 2021 | pilot 2023-02-23; all 2023-06-20 | all (2/15/2024); threshold 25 to 5 effective 2026-07-01 |
| Maine (MERIT) | 2021 | pilot 2023-10-23; all 2024-01-27 | 15+ (4/30/2024); <15 (6/30/2024); remaining (12/31/2024) |
| New York (Secure Choice) | 2021 (auto-IRA amendment; original 2018) | pilot 2025-07-14; all 2025-10-08 | 30+ (3/18/2026); 15-29 (5/15/2026); 10-14 (7/15/2026) |
| Delaware (DE EARNS) | 2022 | pilot 2024-05-01; all 2024-07-01 | all (10/15/2024) |
| Hawaii (Retirement Savings) | 2022 | expected late 2026 / early 2027 | TBD |
| Vermont (Vermont Saves) | 2023 (auto-IRA) | pilot Oct 2024; all 2024-12-01 | all (3/1/2025); covers 2+ employees from Feb 2026 |
| Nevada (NEST) | 2023 | all 2025-06-09 | all (9/1/2025) |
| Minnesota (Secure Choice) | 2023 | soft launch 2026-01-01; full 2026-04-01 | 100+ (6/30/2026); 50-99 (12/1/2026); 25-49 (6/30/2027); 10-24 (12/31/2027); 5-9 (6/30/2028) |
| Rhode Island (RISavers) | 2024 (H 7127 / S 2045, enacted 06/26/2024; P.L. 2024 ch. 350 and 351; R.I. Gen. Laws ch. 35-23) [verified gapB] | all 2025-10-21 (launch event; CT Comptroller release) | Statute: within 12, 24 and 36 months of opening for >100, 50+ and all other eligible employers (5+). RI Treasury compliance dates per secondary sources: 100+ (10/15/2026); 50-99 (10/15/2027); 5-49 (10/15/2028). CRI tracker shows 10/21 dates; see `notes/gapfill_B.md` |
| Washington (Washington Saves) | March 2024 | pilot ~Apr 2027; full by 2027-07-01 | TBD |
| Philadelphia (city auto-IRA) | 2026-05-19 (ballot measure) | contributions by 2027-07-01 | TBD |
| *Voluntary models:* MA CORE MEP (open Oct 2017); WA Marketplace (Mar 2018); MO MEP (statutory target 9/1/2025, not launched); NM Work and $ave and Marketplace (on hold); UT Retirement Plan Exchange (enacted 2026-03-24); MS Work and Save (enacted 2026-04-08; contributions by 2028-08-01) | | | |

### Evidence verdict
Not assessed here; another worker covers the evidence.

### Gaps
- Rhode Island enactment verified (gapB): 2024 -- H 7127, "Enacted 06/26/2024" — [RI Public Law 2024 ch. 350](https://webserver.rilegislature.gov/PublicLaws/law24/law24350.htm); companion S 2045 (ch. 351). The exact compliance dates (Oct 15 vs Oct 21) differ between RI Treasury-derived sources and the CRI tracker; RI Treasury pages return 403 from here.
- NYC and Seattle city programs were superseded by state programs.

## 5. 2025-2026 developments checklist (status as of 2026-10-04)
- **414A mandatory auto-enrollment regs:** proposed Jan 14 2025. Final regs at OIRA since June 23 2026 (verified on reginfo.gov; still under review on 2026-10-04); not published in the Federal Register. Good-faith compliance applies until plan years starting 6 months or more after the final rule.
- **Saver's Match:** Notice 2026-48 (Aug 7 2026), with no proposed regs yet. Starts tax year 2027, first deposits 2028. EO 14403 / TrumpIRA.gov launches Jan 1 2027.
- **Auto-portability:** statutory exemption live since Dec 29 2023. DOL rule is proposed only (Jan 29 2024); the final rule went to OIRA on 2026-09-14 (reginfo.gov; agenda target "Final Rule 09/00/2026") and is not yet published.
- **LTPT regs:** proposed only (Nov 27 2023). Treasury's agenda targets "Final Action 09/00/2026" (RIN 1545-BQ70), but no final rule is at OIRA or in the Federal Register as of 2026-10-04 (gapB).
- **Roth catch-up/super catch-up:** final regs Sept 16 2025, generally applying from 2027.
- **OBBBA (P.L. 119-21, July 4 2025):** a full-text search found no changes to 401(k)/403(b) participation or distribution rules.
  - Adjacent: Sec. 70204 Trump accounts. These are child IRAs with a $5,000/yr limit and employer contributions up to $2,500 excludable under new IRC 128. There is a $1,000 federal pilot deposit, and no contributions are accepted "before the date that is 12 months after the date of the enactment" (Computed: 2026-07-04).
  - Sec. 70116 extends the Saver's Credit for ABLE contributions.
  - Source: [P.L. 119-21](https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm).
- **DOL:** PEP guidance/RFI (July 29 2025). EO 14330 on alternative assets (Aug 7 2025), followed by a DOL proposed rule on selecting designated investment alternatives (Mar 31 2026). These concern the investment menu, not participation or withdrawals.
- **TSP:** in-plan Roth conversions effective Jan 28 2026 ([91 FR 1669](https://www.federalregister.gov/documents/2026/01/15/2026-00765/roth-in-plan-conversions)).
- **Pending bills (status from GovTrack and govinfo bill text, as of 2026-10-04; gapB):** S. 3333 Emergency Savings Enhancement Act (PLESA cap $2,500 → $5,000, eligibility widened; reported by Senate HELP, Calendar No. 544) is the only participation/withdrawal bill to clear committee. Introduced only: H.R. 6722 Automatic IRA Act; H.R. 6729 / S. 1831 Auto Reenroll Act; H.R. 2696 / S. 1526 Retirement Savings for Americans Act; H.R. 6324 / S. 5156 Retirement Simplification and Clarity Act (in-service rollovers to buy annuities); H.R. 6450 / S. 3352 Retirement Rollover Flexibility Act (Roth IRA → designated Roth rollovers); S. 5507 Saver's Match Enhancement Act of 2026; S. 2217 Independent Retirement Fairness Act. Adjacent: S. 2403 Retire through Ownership Act (ESOP valuation) passed both chambers 2026-09-16, awaiting signature. No 2026 statute changing DC participation or withdrawal rules was found. Full list with links: `notes/gapfill_B.md`.

## 6. Master table

| Law | Section | Provision | Category | Direction | Effective date | Primary source URL | Status / notes |
|---|---|---|---|---|---|---|---|
| Revenue Act of 1978 (P.L. 95-600, Nov 6 1978) | Sec. 135 (IRC 401(k)) | Creates qualified cash-or-deferred arrangements: employee can defer pay pre-tax into a profit-sharing/stock bonus plan | contribution | + | Plan years beginning after 12/31/1979 (Sec. 135(c)(1), 92 Stat. 2787; text-verified gapB) | [link](https://www.govinfo.gov/content/pkg/STATUTE-92/pdf/STATUTE-92-Pg2763.pdf) | Sec. 135 starts at 92 Stat. 2785 |
| IRS Rev. Rul. 98-30 | IRB 1998-25, p. 8 (June 22 1998) | Automatic enrollment ("negative election") of NEW hires into a 401(k) is permissible if the employee is notified and can opt out | participation | + | 1998-06-22 | [link](https://www.irs.gov/pub/irs-irbs/irb98-25.pdf) | Treasury first approved auto-enrollment in 1998 (Senate Finance SECURE 2.0 summary, Sec. 101) |
| IRS Rev. Rul. 2000-8 | IRB 2000-7 (Feb 14 2000) | Auto-enrollment also permissible for CURRENT employees not yet enrolled; default rate may differ from the 3% example | participation | + | 2000-02-14 | [link](https://www.irs.gov/pub/irs-irbs/irb00-07.pdf) |  |
| IRS Rev. Rul. 2000-33 / 2000-35; Ann. 2000-60 | 457(b), 403(b), prototype 401(k) | Auto-enrollment permitted in governmental 457(b), 403(b) and IRS-approved prototype 401(k) plans | participation | + | 2000 | [link](https://www.everycrsreport.com/reports/RS21954.html) | CRS RS21954 (Jan 16 2007) summarizes |
| EGTRRA 2001 (P.L. 107-16, June 7 2001) | Sec. 618 | Saver's Credit (nonrefundable credit for elective deferrals/IRA contributions by low/moderate earners) | contribution | + | Tax years beginning after 12/31/2001 | [link](https://www.govinfo.gov/content/pkg/PLAW-107publ16/html/PLAW-107publ16.htm) | Replaced by refundable Saver's Match from 2027 (SECURE 2.0 Sec. 103) |
| EGTRRA 2001 | Secs. 641-643 | Rollovers allowed among 401(k), 403(b), governmental 457(b) and IRAs (incl. IRA-to-plan and after-tax amounts) | staying-in-plan | + | Distributions after 12/31/2001 | [link](https://www.govinfo.gov/content/pkg/PLAW-107publ16/html/PLAW-107publ16.htm) | Portability keeps money tax-deferred on job change |
| EGTRRA 2001 | Sec. 657 (IRC 401(a)(31)(B)) | Mandatory (force-out) distributions of $1,000-$5,000 must be directly rolled to an IRA unless participant elects otherwise | staying-in-plan | + (tax deferral) / - (leaves plan) | Distributions after final DOL safe-harbor regs -> 2005-03-28 | [link](https://www.govinfo.gov/content/pkg/PLAW-107publ16/html/PLAW-107publ16.htm) | Keeps small balances tax-deferred but moves them out of the employer plan |
| DOL safe harbor reg 29 CFR 2550.404a-2 | 69 FR 58018 (Sept 28 2004) | Fiduciary safe harbor for automatic rollovers of mandatory distributions into default IRAs | staying-in-plan | + | 2005-03-28 | [link](https://www.federalregister.gov/documents/2004/09/28/04-21591/fiduciary-responsibility-under-the-employee-retirement-income-security-act-of-1974-automatic) | IRS Notice 2005-5 companion guidance: https://www.irs.gov/pub/irs-drop/n-05-05.pdf |
| Pension Protection Act 2006 (P.L. 109-280, Aug 17 2006) | Sec. 902 (IRC 401(k)(13), QACA) | Qualified automatic contribution arrangement safe harbor: default deferral >=3% yr1, 4% yr2, 5% yr3, 6% thereafter (max 10%); employer match 100% of first 1% + 50% of next 5% (or 3% nonelective); 2-yr vesting; exempt from ADP/ACP/top-heavy | participation | + | Plan years beginning after 12/31/2007 | [link](https://www.govinfo.gov/content/pkg/PLAW-109publ280/html/PLAW-109publ280.htm) | Built-in auto-escalation; SECURE 2019 Sec. 102 raised the post-yr-1 cap to 15% |
| Pension Protection Act 2006 | Sec. 902 (IRC 414(w), EACA) | Eligible automatic contribution arrangement: uniform default + notice; 90-day permissible withdrawal of default deferrals; 6-month corrective-distribution window | participation | + (90-day unwind is small leakage) | Plan years beginning after 12/31/2007 | [link](https://www.govinfo.gov/content/pkg/PLAW-109publ280/html/PLAW-109publ280.htm) | Final regs 74 FR 8200 (Feb 24 2009) |
| Pension Protection Act 2006 | Sec. 902(f) (ERISA 514(e)) | ERISA preempts state wage-payment/withholding laws that would prohibit or restrict automatic contribution arrangements | participation | + | 2006-08-17 (date of enactment) | [link](https://www.govinfo.gov/content/pkg/PLAW-109publ280/html/PLAW-109publ280.htm) | Removed legal barrier to auto-enrollment |
| Pension Protection Act 2006 | Sec. 624 (ERISA 404(c)(5)) | Fiduciary relief for investing non-electing participants' money in a default investment | participation | + (enabler) | Plan years beginning after 12/31/2006 | [link](https://www.govinfo.gov/content/pkg/PLAW-109publ280/html/PLAW-109publ280.htm) |  |
| DOL QDIA regulation 29 CFR 2550.404c-5 | 72 FR 60452 (Oct 24 2007) | Qualified default investment alternatives (target-date, balanced, managed account; capital-preservation only first 120 days) | participation | + (enabler) | 2007-12-24 | [link](https://www.federalregister.gov/documents/2007/10/24/07-5147/default-investment-alternatives-under-participant-directed-individual-account-plans) | SECURE 2.0 Sec. 101 requires 414A plans to use a QDIA |
| Pension Protection Act 2006 | Sec. 827 (IRC 72(t)(2)(G)) | Penalty-free qualified reservist distributions | leakage-increasing | - | Distributions after 9/11/2001 (retroactive) | [link](https://www.govinfo.gov/content/pkg/PLAW-109publ280/html/PLAW-109publ280.htm) | Narrow population |
| Treasury/IRS final regs on automatic contribution arrangements | 74 FR 8200 (Feb 24 2009) | Final regs for QACA (401(k)(13)) and EACA (414(w)) | participation | + | 2009-02-24 | [link](https://www.federalregister.gov/documents/2009/02/24/E9-3716/automatic-contribution-arrangements) | Notice 2009-65 sample amendments: https://www.irs.gov/pub/irs-drop/n-09-65.pdf |
| Thrift Savings Plan Enhancement Act 2009 (P.L. 111-31 Div. B, June 22 2009) | Sec. 102 (5 U.S.C. 8432(b)) | Automatic enrollment of newly hired/rehired FERS employees at default 3% (Board may set 2%-5%); opt-out allowed | participation | + | 2010-08-01 (FRTIB rule 75 FR 43799) | [link](https://www.federalregister.gov/documents/2010/07/27/2010-18346/employee-contribution-elections-and-contribution-allocations) | Statute: https://www.govinfo.gov/content/pkg/PLAW-111publ31/html/PLAW-111publ31.htm |
| Thrift Savings Plan Enhancement Act 2009 | Sec. 103 | Roth TSP contributions | contribution | + | 2012-05-07 (FRTIB rule 77 FR 26417) | [link](https://www.federalregister.gov/documents/2012/05/04/2012-10630/roth-feature-to-the-thrift-savings-plan-and-miscellaneous-uniformed-services-account-amendments) |  |
| DOL state savings program safe harbor | 81 FR 59464 (Aug 30 2016) | Safe harbor: state auto-IRA payroll programs are not ERISA plans | participation | + | 2016-10-31; nullified by CRA resolution P.L. 115-35 (May 17 2017) | [link](https://www.federalregister.gov/documents/2016/08/30/2016-20639/savings-arrangements-established-by-states-for-non-governmental-employees) | Repeal: https://www.govinfo.gov/content/pkg/PLAW-115publ35/html/PLAW-115publ35.htm ; state programs proceeded anyway |
| NDAA FY2016 (P.L. 114-92) | Sec. 632 (Blended Retirement System) | Uniformed services: automatic enrollment in TSP at 3% plus government automatic 1% and matching for new entrants | participation | + | 2018-01-01 (FRTIB rule 82 FR 60099) | [link](https://www.federalregister.gov/documents/2017/12/19/2017-27304/blended-retirement-system) | Statute: https://www.govinfo.gov/content/pkg/PLAW-114publ92/html/PLAW-114publ92.htm |
| Tax Cuts and Jobs Act 2017 (P.L. 115-97) | Sec. 13613 (IRC 402(c)(3)(C)) | Extended rollover deadline (to tax-return due date) for qualified plan-loan offsets after job separation/plan termination | staying-in-plan | + | Tax years beginning after 12/31/2017 | [link](https://www.govinfo.gov/content/pkg/PLAW-115publ97/html/PLAW-115publ97.htm) | Reduces loan-default leakage |
| TSP Modernization Act 2017 (P.L. 115-84, Nov 17 2017) | Sec. 2 | Multiple post-separation partial withdrawals, age-based in-service withdrawals, flexible installments; separated participants no longer forced into a one-time full election | staying-in-plan | + (keep $ in TSP) / - (easier access) | 2019-09-15 (FRTIB rule 84 FR 46419) | [link](https://www.federalregister.gov/documents/2019/09/04/2019-19029/additional-withdrawal-options) | Statute: https://www.govinfo.gov/content/pkg/PLAW-115publ84/html/PLAW-115publ84.htm |
| Bipartisan Budget Act 2018 (P.L. 115-123) | Secs. 41113-41114 | Hardship withdrawals: delete 6-month contribution suspension; no loan-first requirement; earnings, QNECs, QMACs withdrawable | leakage-increasing | - (easier hardship) / + (no suspension of saving) | Plan years beginning after 12/31/2018; final regs 84 FR 49651 (Sept 23 2019) | [link](https://www.federalregister.gov/documents/2019/09/23/2019-20511/hardship-distributions-of-elective-contributions-qualified-matching-contributions-qualified) | Statute: https://www.govinfo.gov/content/pkg/PLAW-115publ123/html/PLAW-115publ123.htm |
| SECURE Act 2019 (P.L. 116-94 Div. O, Dec 20 2019) | Sec. 101 | Open multiple employer plans; pooled employer plans (PEPs) with pooled plan providers | participation | + | Plan years beginning after 12/31/2020 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) | DOL PEP interpretive guidance + RFI 90 FR 35646 (July 29 2025) |
| SECURE Act 2019 | Sec. 102 | QACA auto-escalation cap raised from 10% to 15% after first plan year | contribution | + | Plan years beginning after 12/31/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) |  |
| SECURE Act 2019 | Sec. 103 | Nonelective safe-harbor 401(k): annual notice eliminated; mid-year/late adoption allowed (4% if adopted late) | participation | + | Plan years beginning after 12/31/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) |  |
| SECURE Act 2019 | Sec. 104 | Small-employer startup credit raised to greater of $500 or lesser of $250 x non-HCEs or $5,000, for 3 years | participation | + | Tax years beginning after 12/31/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) |  |
| SECURE Act 2019 | Sec. 105 | New $500/yr credit for 3 years for small employers adding auto-enrollment | participation | + | Tax years beginning after 12/31/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) |  |
| SECURE Act 2019 | Sec. 107 | Repeal of age-70 1/2 cap on traditional IRA contributions | contribution | + | Contributions for tax years beginning after 12/31/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) |  |
| SECURE Act 2019 | Sec. 108 | Plan loans via credit cards prohibited | staying-in-plan | + (anti-leakage) | Loans after 12/20/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) |  |
| SECURE Act 2019 | Sec. 109 | Portability of lifetime income: in-plan annuity can be distributed/rolled when option is discontinued | staying-in-plan | + | Plan years beginning after 12/31/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) |  |
| SECURE Act 2019 | Sec. 112 | Long-term part-time (LTPT) workers: 401(k) deferral eligibility after 3 consecutive 12-month periods of >=500 hours | participation | + | Plan years beginning after 12/31/2020; pre-2021 periods ignored, so first entrants 2024 (Computed: 2021+2022+2023 -> 1/1/2024) | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) | Proposed regs 88 FR 82796 (Nov 27 2023); not final as of 2026-10-04 per FR search; not at OIRA (agenda target 09/2026) |
| SECURE Act 2019 | Sec. 113 | Qualified birth or adoption distributions up to $5,000 per child, 10% penalty waived, repayable | leakage-increasing | - | Distributions after 12/31/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) | SECURE 2.0 Sec. 311 limits repayment window to 3 years |
| SECURE Act 2019 | Sec. 114 | RMD required beginning age raised from 70 1/2 to 72 | staying-in-plan | + | For individuals attaining 70 1/2 after 12/31/2019 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) |  |
| SECURE Act 2019 | Sec. 401 | Stretch IRA ended: most non-spouse beneficiaries must empty inherited accounts within 10 years | leakage-increasing | - (shortens deferral for heirs) | Deaths after 12/31/2019; final RMD regs 89 FR 58886 (eff 2024-09-17; apply from 2025) | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm) | Final regs: https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions |
| CARES Act 2020 (P.L. 116-136, Mar 27 2020) | Sec. 2202(a) | Coronavirus-related distributions (CRDs) up to $100,000; 10% penalty waived; income spread over 3 years; repayable within 3 years; self-certification | leakage-increasing | - | Distributions 2020-01-01 to 2020-12-30 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ136/html/PLAW-116publ136.htm) | IRS Notice 2020-50: https://www.irs.gov/pub/irs-drop/n-20-50.pdf |
| CARES Act 2020 | Sec. 2202(b) | Plan-loan limit raised to $100,000 / 100% of vested balance for 180 days; repayments due through 2020 delayed one year | leakage-increasing | - | Loans 2020-03-27 to 2020-09-22 (Computed: 180 days from enactment) | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ136/html/PLAW-116publ136.htm) |  |
| CARES Act 2020 | Sec. 2203 | Waiver of 2020 required minimum distributions from DC plans and IRAs | staying-in-plan | + | Calendar year 2020 | [link](https://www.govinfo.gov/content/pkg/PLAW-116publ136/html/PLAW-116publ136.htm) | IRS Notice 2020-51: https://www.irs.gov/pub/irs-drop/n-20-51.pdf |
| FRTIB rule (TSP) | 85 FR 57665 (Sept 16 2020) | TSP automatic-enrollment default raised from 3% to 5% of basic pay (FERS new hires; BRS re-enrollment from 1/1/2021) | contribution | + | 2020-10-01 | [link](https://www.federalregister.gov/documents/2020/09/16/2020-17811/automatic-enrollment-program) | 5% earns full agency match |
| SECURE 2.0 Act 2022 (P.L. 117-328 Div. T, Dec 29 2022) | Sec. 101 (new IRC 414A) | Mandatory auto-enrollment for NEW 401(k)/403(b) plans: EACA at 3%-10% initial, +1 pt/yr to at least 10% (max 15%), QDIA default, 90-day permissible withdrawal. Exempt: plans established before 12/29/2022, SIMPLE, governmental and church plans, employers <3 years old, employers with <=10 employees | participation | + | Plan years beginning after 12/31/2024 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | Proposed regs 90 FR 3092 (Jan 14 2025): final regs apply to plan years beginning >6 months after issuance; good-faith compliance until then. Draft final regs received by OIRA 2026-06-23 (reginfo.gov, verified); NOT published in FR as of 2026-10-04 |
| SECURE 2.0 Act 2022 | Sec. 102 | Startup credit = 100% of admin costs for employers with <=50 employees; new credit for employer contributions up to $1,000/employee (phased down over 5 years) | participation | + | Tax years beginning after 12/31/2022 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 103 (new IRC 6433) | Saver's Match: federal deposit of 50% of up to $2,000 of contributions (max $1,000) into plan/IRA; phases out from $41,000 AGI (joint; $30,000 range); replaces Saver's Credit | contribution | + | Tax years beginning after 12/31/2026 (first deposits 2028) | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | IRS Notice 2026-48 (IR-2026-89, Aug 7 2026), comments due Oct 5 2026: https://www.irs.gov/pub/irs-drop/n-26-48.pdf ; EO 14403 TrumpIRA.gov (signed 2026-04-30, 91 FR 24329) launches 2027-01-01 |
| SECURE 2.0 Act 2022 | Secs. 105-106 | PEP modifications; 403(b) plans may join MEPs/PEPs | participation | + | Plan years beginning after 12/31/2022 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 107 | RMD age 73 (attain 72 after 2022 and 73 before 2033); age 75 (attain 74 after 2032) | staying-in-plan | + | Distributions required after 12/31/2022; age 75 from 2033 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 109 | Higher catch-up at ages 60-63: greater of $10,000 or 150% of regular catch-up | contribution | + | Tax years beginning after 12/31/2024 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | Final catch-up regs 90 FR 44527 (eff 2025-11-17; generally apply 2027) |
| SECURE 2.0 Act 2022 | Sec. 603 | Catch-ups must be Roth for employees with prior-year FICA wages > $145,000 (indexed) | contribution | 0 (tax timing) | Statutory 2024; IRS admin transition to 2026 (Notice 2023-62); final regs generally apply to tax years after 12/31/2026 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | Final regs: https://www.federalregister.gov/documents/2025/09/16/2025-17865/catch-up-contributions |
| SECURE 2.0 Act 2022 | Sec. 110 | Employer may treat qualified student-loan payments as elective deferrals for matching | contribution | + | Plan years beginning after 12/31/2023 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | IRS Notice 2024-63: https://www.irs.gov/pub/irs-drop/n-24-63.pdf |
| SECURE 2.0 Act 2022 | Sec. 111 | Startup credit available to employers joining an existing MEP | participation | + | Retroactive to SECURE Act Sec. 104 (2020) | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 112 | Small-employer credit for making military spouses eligible within 2 months | participation | + | Tax years beginning after 12/29/2022 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 113 | De minimis financial incentives (e.g., gift cards) for enrolling allowed | participation | + | Plan years beginning after 12/29/2022 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 115 (IRC 72(t)(2)(I)) | Emergency personal expense distribution: 1 per year, up to $1,000, penalty-free, repayable within 3 years; no further such withdrawals for 3 years unless repaid | leakage-increasing | - | Distributions after 12/31/2023 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | IRS Notice 2024-55: https://www.irs.gov/pub/irs-drop/n-24-55.pdf |
| SECURE 2.0 Act 2022 | Sec. 120 (IRC 4975(d)(25), (f)(12)) | Statutory prohibited-transaction exemption for automatic portability providers: default-IRA balances (force-outs <= $7,000) auto-moved into new employer's plan unless participant opts out | staying-in-plan | + | Transactions on/after 2023-12-29 (12 months after enactment) | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | DOL proposed reg 89 FR 5624 (Jan 29 2024); final rule (RIN 1210-AC21) received by OIRA 2026-09-14; NO final rule in FR as of 2026-10-04. Pre-statute: individual exemption for Retirement Clearinghouse 84 FR 37337 (July 31 2019) |
| SECURE 2.0 Act 2022 | Sec. 121 | Starter 401(k)/safe-harbor 403(b): deferral-only, auto-enroll 3%-15%, deferral limit $6,000 (indexed), no ADP testing | participation | + | Plan years beginning after 12/31/2023 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 125 | LTPT rule cut to 2 consecutive years of >=500 hours; extended to ERISA 403(b) plans | participation | + | Plan years beginning after 12/31/2024 (pre-2023 periods ignored -> first 2-yr entrants 2025) | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | Proposed regs 88 FR 82796 (Nov 27 2023) |
| SECURE 2.0 Act 2022 | Sec. 127 | Pension-linked emergency savings accounts (PLESAs) for non-HCEs: Roth, cap $2,500 (indexed), auto-enroll up to 3%, at least monthly withdrawals with first 4 per year fee-free | leakage-increasing | +/- (liquidity buffer intended to reduce 401(k) leakage, but adds in-plan withdrawal channel) | Plan years beginning after 12/31/2023 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | IRS Notice 2024-22: https://www.irs.gov/pub/irs-drop/n-24-22.pdf |
| SECURE 2.0 Act 2022 | Sec. 202 | QLAC limit raised to $200,000 (indexed); 25%-of-balance limit repealed | staying-in-plan | + (defers RMDs on annuity portion) | Contracts purchased/exchanged on or after 2022-12-29 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 303 (ERISA 523) | DOL Retirement Savings Lost and Found online database | staying-in-plan | + | Database launched Dec 2024 (data collection approved, 89 FR 91787, Nov 20 2024) | [link](https://lostandfound.dol.gov/) | FR notice: https://www.federalregister.gov/documents/2024/11/20/2024-27098/retirement-savings-lost-and-found |
| SECURE 2.0 Act 2022 | Sec. 304 | Involuntary cash-out (force-out) threshold raised from $5,000 to $7,000 (automatic IRA rollover still required for $1,000+) | staying-in-plan | - (more balances pushed out of plans) / + (still IRA tax-deferred) | Distributions after 12/31/2023 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | Senate Finance summary mis-labels as Sec. 307 |
| SECURE 2.0 Act 2022 | Sec. 311 | Repayment of birth/adoption distributions limited to 3 years | staying-in-plan | 0 | Distributions after 12/29/2022 (earlier ones: repay by 12/31/2025) | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 314 | Domestic-abuse victim distributions: lesser of $10,000 (indexed) or 50% of vested balance, penalty-free, repayable within 3 years | leakage-increasing | - | Distributions after 12/31/2023 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) | IRS Notice 2024-55 |
| SECURE 2.0 Act 2022 | Sec. 326 | Terminal illness exception to 10% early-withdrawal penalty | leakage-increasing | - | Distributions after 2022-12-29 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 331 | Permanent qualified disaster recovery distributions up to $22,000 per disaster, penalty-free, 3-year income spread; higher loan limits | leakage-increasing | - | Disasters with incident period beginning on/after 2021-01-26 (Computed: 30 days after Dec 27 2020 enactment of Taxpayer Certainty and Disaster Tax Relief Act 2020) | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| SECURE 2.0 Act 2022 | Sec. 602 | 403(b) hardship-withdrawal rules conformed to 401(k) (earnings, QNEC/QMAC; no suspension) | leakage-increasing | - | Plan years beginning after 12/31/2023 | [link](https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm) |  |
| FRTIB rule (TSP) | 89 FR 18533 (Mar 14 2024) | Removal of 30-calendar-day waiting period between TSP withdrawals | leakage-increasing | - (minor) | 2024-05-15 | [link](https://www.federalregister.gov/documents/2024/03/14/2024-05346/removal-of-30-calendar-day-waiting-period-between-withdrawals) |  |
| Executive Order 14330 + DOL proposed rule | 90 FR 38921 (EO, Aug 7 2025); 91 FR 16088 (NPRM, Mar 31 2026) | Alternative assets in 401(k) menus/asset-allocation funds; proposed fiduciary safe harbor for selecting designated investment alternatives | other (investment menu) | 0 (not participation/withdrawal) | Proposed; comments closed 2026-06-01 | [link](https://www.federalregister.gov/documents/2026/03/31/2026-06178/fiduciary-duties-in-selecting-designated-investment-alternatives) | Context only |
| One Big Beautiful Bill Act 2025 (P.L. 119-21, July 4 2025) | Sec. 70204 (new IRC 530A, 128, 6434) | Trump accounts: IRA-type accounts for children; $5,000/yr limit; employer contributions up to $2,500 excludable (new IRC 128); $1,000 federal pilot deposit for eligible children born 2025-2028; no contributions before 12 months after enactment | other (adjacent; not a DC plan) | 0 | Tax years beginning after 12/31/2025; first contributions 2026-07-04 (Computed: 12 months after enactment) | [link](https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm) | Full-text search of P.L. 119-21 found no amendment to 401(k)/403(b) participation or distribution rules; Sec. 70116 extends Saver's Credit for ABLE contributions |
| Executive Order 14403 | 91 FR 24329 (signed Apr 30 2026) | TrumpIRA.gov: federal website promoting Saver's Match and IRAs for workers without employer plans | contribution | + | Website launch 2027-01-01 | [link](https://www.federalregister.gov/documents/2026/05/05/2026-08908/promoting-retirement-savings-access-for-american-workers-by-establishing-trumpiragov) | Implementation started via Notice 2026-48 |
| FRTIB rule (TSP) | 91 FR 1669 (Jan 15 2026) | In-plan Roth conversions within TSP | other (tax treatment) | 0 | 2026-01-28 | [link](https://www.federalregister.gov/documents/2026/01/15/2026-00765/roth-in-plan-conversions) |  |
## Chart-ready series

Timeline of key default/threshold parameters (statutory values, not outcomes):

| Year effective | Parameter | Value | Source |
|---|---|---|---|
| 2005 | Auto-rollover band for force-outs | $1,000-$5,000 | https://www.federalregister.gov/documents/2004/09/28/04-21591/fiduciary-responsibility-under-the-employee-retirement-income-security-act-of-1974-automatic |
| 2024 | Force-out ceiling | $7,000 | https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm |
| 2008 | QACA min default yr1 / cap | 3% / 10% | https://www.govinfo.gov/content/pkg/PLAW-109publ280/html/PLAW-109publ280.htm |
| 2020 | QACA cap after yr1 | 15% | https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm |
| 2025 | 414A initial default band / escalation target / cap | 3-10% / >=10% / 15% | https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm |
| 2010 | TSP FERS default | 3% | https://www.federalregister.gov/documents/2010/07/27/2010-18346/employee-contribution-elections-and-contribution-allocations |
| 2020 | TSP FERS default | 5% | https://www.federalregister.gov/documents/2020/09/16/2020-17811/automatic-enrollment-program |
| pre-2020 | RMD age | 70.5 | https://www.govinfo.gov/content/pkg/PLAW-116publ94/html/PLAW-116publ94.htm |
| 2020 | RMD age | 72 | same |
| 2023 | RMD age | 73 | https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm |
| 2033 | RMD age | 75 | same |
| 2021/2024 | LTPT hours rule (first entrants) | 3 yrs x 500 hrs (2024) | P.L. 116-94 Sec. 112 |
| 2025 | LTPT hours rule | 2 yrs x 500 hrs | P.L. 117-328 Sec. 125 |
| 2027 | Saver's Match max (50% of $2,000) | $1,000 | P.L. 117-328 Sec. 103; https://www.irs.gov/pub/irs-drop/n-26-48.pdf |

Count of state auto-IRA programs open to all employers, by year opened (Computed from table in Section 4: OR, IL 2017-18; CA 2019; CT, MD 2022; CO, VA 2023; ME, NJ, DE, VT 2024; NV, NY, RI 2025; MN 2026):

| Year | Cumulative state auto-IRAs open | Source |
|---|---|---|
| 2017 | 1 | https://cri.georgetown.edu/states/ |
| 2018 | 2 | same |
| 2019 | 3 | same |
| 2022 | 5 | same |
| 2023 | 7 | same |
| 2024 | 11 | same |
| 2025 | 14 | same |
| 2026 | 15 | same |
