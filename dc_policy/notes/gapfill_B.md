# Gap-fill B: verification log (worker gapB, 2026-10-05)

Scope: verify or replace unverified items in `notes/provisions.md`, `output/provisions_timeline.csv`, `notes/auto_enrollment.md`, and list the status of items in `notes/stay_in_plan_leakage.md` and dates used by `notes/cps_participation.md` (those two files were not edited). Each item below is marked **verified**, **corrected (old -> new)** or **could not verify (why)**. Saved sources: `raw/gapB/`.

Hosts blocked from here: psca.org, napa-net.org, asppa-net.org (Cloudflare 403), treasury.ri.gov (403), gao.gov via curl (403; WebFetch worked for the highlights PDF), congress.gov (not used), journals.uchicago.edu (403), vanguard.com research PDFs for 2021/2024 (redirect to a landing page). Reachable: govinfo.gov (including the bill-text link service), reginfo.gov (XML reports), federalregister.gov API, govtrack.us API (rate-limited), rilegislature.gov, osc.ct.gov, treasury.colorado.gov, the state program sites (with a browser user-agent), nber.org, benefitslink.com.

## 1. State auto-IRA dates

### Rhode Island (RISavers)
- **Enactment year: verified, 2024.** "2024 -- H 7127 ... Enacted 06/26/2024", creating R.I. Gen. Laws ch. 35-23, "Rhode Island Secure Choice Retirement Savings Program Act" — [RI P.L. 2024 ch. 350](https://webserver.rilegislature.gov/PublicLaws/law24/law24350.htm). Companion S 2045 is ch. 351. Statute history: "P.L. 2024, ch. 350, § 1, effective June 26, 2024; P.L. 2024, ch. 351, § 1, effective June 26, 2024" — [§ 35-23-1](https://webserver.rilegislature.gov/Statutes/TITLE35/35-23/35-23-1.htm).
- **Statutory phase-in: verified.** Employers with "more than one hundred (100) eligible employees" must have a payroll deposit arrangement "Within twelve (12) months after the office of the general treasurer opens the program for enrollment". The 50+ wave follows at 24 months and "all other eligible employers" (5+ employees) at 36 months (ch. 350, § 35-23-9 "Employer participation", subsections (b)-(d)).
- **Launch: verified, Oct 21 2025.** In a release dated October 21, 2025, the CT Comptroller "joined Rhode Island Governor Dan McKee, Treasurer James Diossa ... to celebrate the launch of the RISavers retirement saving program, a partner of MyCTSavings" — [CT OSC release, 2025-10-21](https://osc.ct.gov/wp-content/uploads/2025/10/2025.10.21-Comptroller-RISavers.pdf).
- **Compliance deadlines: partly corrected, not fully verified.** provisions.md had 10/21/2026, 10/21/2027 and 10/21/2028 (from the CRI tracker). Sources quoting the RI Treasury give **Oct 15, 2026 (100+), Oct 15, 2027 (50-99) and Oct 15, 2028 (5-49)** ([OnPay, updated May 12 2026](https://onpay.com/insights/rhode-island-risavers-retirement-mandate/); search extract of the [RI Treasury notice](https://treasury.ri.gov/press-releases/important-information-regarding-risavers-program)). The Treasury notice also says an earlier Dec 12, 2025 information/registration date "does not trigger enforcement". The RI Treasury pages return 403 from here. provisions.md now shows the statutory rule plus the Oct 15 dates, with the discrepancy flagged.
- **Status:** open to all covered employers since Oct 21 2025; first compliance wave due Oct 2026.

### Connecticut (MyCTSavings)
| Item | Date | Status / source |
|---|---|---|
| Pilot | Sept/Oct 2021 | **Could not verify the exact date.** CRI says 2021-10-25; NAPA/ASPPA (Mar 2022) say a pilot "launched in September 2021" (psca/napa blocked; search extract only) |
| Statewide launch | March 24 2022 announcement; letters to about 30,000 employers in early April 2022 | Secondary (NAPA/ASPPA via search). CRI "all 2022-04-01" is consistent |
| 100+ employees deadline | June 30, 2022 | Secondary ([CBIA](https://www.cbia.com/news/featured/ct-retirement-plan-deadline/), Pullcom) |
| 26-99 employees | Oct 31, 2022 | Secondary (same) |
| 5-25 employees | March 30, 2023 | **Verified:** "Following the initial deadline of March 30" — [CT Comptroller release, 5 Apr 2023](https://osc.ct.gov/articles/comptroller-sean-scanlon-releases-myctsavings-enrollment-statistics-formally-extends-registration-deadline/) |
| Extension for all employers | **Aug 31, 2023** | **Verified:** "we are extending the enrollment deadline to August 31, 2023" (same release). *New detail; provisions.md lists 3/30/2023 only.* |
| Current | "Newly eligible businesses: August 31, 2026 Next deadline" | **Verified:** [myctsavings.com program details](https://myctsavings.com/employers/program-details) (accessed 2026-10-05) |

The same release reports that 3,400+ businesses enrolled, 10,000+ employees saving and $3.5M in assets after the March 30, 2023 deadline.

### Maryland (MarylandSaves; "$aves")
| Item | Date | Status / source |
|---|---|---|
| Pilot | Mar 2022 | Could not verify (no official page found) |
| Statewide launch | **Sept 15, 2022** | **Verified:** "Launched statewide on Sep 15, 2022" — [marylandsaves.org](https://www.marylandsaves.org/) |
| Registration "deadline" | Dec 1, 2022 | **Secondary only.** NAPA (Sept 2022, via search) ties it to the incentive: employers enrolling "by December 1st" avoid the $300 SDAT annual-report fee for 2023. Maryland has no penalty-based wave schedule. The official site describes only the fee waiver and mentions no size waves. Treat 12/1/2022 as an incentive date, not a mandate wave. |

### Colorado (Colorado SecureSavings)
| Item | Date | Status / source |
|---|---|---|
| Pilot | **October 2022** | **Verified:** "October 2022: Pilot Program began" and "Launched in October 2022, the pilot program included over 20 employers" — [CSSP Annual Report, Apr 2023](https://treasury.colorado.gov/sites/treasury/files/FINAL%20Colorado%20SecureSavings%20Annual%20Report%20%281%29.pdf), pp.5, 7 |
| Statewide open | **January 2023** (portal opened Jan 18, 2023) | **Verified:** "January 2023: Program implementation officially began" (same report). The Jan 18 date comes from the [Treasury press release title](https://treasury.colorado.gov/press-release/1182023-colorado-securesavings-program-provides-access-to-retirement-savings-plan) and BizWest (2023-01-18) |
| Waves: 50+ | March 15, 2023 | Official report: "waves of notices will be sent according to business size beginning March 15, 2023". The per-size deadlines are secondary ([NFP](https://www.nfp.com/insights/certain-colorado-employers-required-to-register-with-colorado-secure-savings-program/), Ogletree) |
| 15-49 | May 15, 2023 | Secondary |
| 5-14 | June 30, 2023 | Secondary |
| Enforcement | Fines not assessed before Feb 2024 | **Verified:** "enforcement fines will not be assessed until February 2024" (annual report p.13) |
| Current | New businesses: "Registration May 15, 2026 deadline" | **Verified:** [coloradosecuresavings.com program details](https://coloradosecuresavings.com/employers/program-details) |

### Virginia (RetirePath Virginia)
| Item | Date | Status / source |
|---|---|---|
| Pilot | early 2023 (CRI: 2023-02-23) | Official plan: "The pilot program is scheduled to begin in early 2023" — [Virginia529 release, 2 Jun 2022](https://virginia529.com/newsroom/virginias-state-facilitated-private-retirement-program-scheduled-to-launch-in-2023). The exact pilot date is not verified |
| Statewide | Notices from June 20, 2023; "will open by July 1, 2023" | Official target verified (same release). The June 20 notice date is secondary (GRF CPA / trade press) |
| Registration deadline (25+ employees) | **Feb 15, 2024** | Secondary, consistent across sources ([PBMares](https://www.pbmares.com/retirepath-virginia-registration-deadline-is-february-15-2024/), Spotts Fain, Henrico Citizen). retirepathva.com is JavaScript-only and could not be read |
| Threshold cut 25 -> 5 (effective 2026-07-01) | not re-verified | — |

## 2. Revenue Act of 1978, 401(k) effective date: verified
P.L. 95-600, sec. 135(c): "(1) IN GENERAL.—The amendments made by this section shall apply to plan years beginning after December 31, 1979. (2) TRANSITIONAL RULE.—In the case of cash or deferred arrangements in existence on June 27, 1974 ... shall be determined for plan years beginning before January 1, 1980 in a manner consistent with Revenue Ruling 56-497 ..., 63-180 ..., and 68-89" — [92 Stat. 2787 (govinfo STATUTE-92-Pg2763.pdf, pdf p.25)](https://www.govinfo.gov/content/pkg/STATUTE-92/pdf/STATUTE-92-Pg2763.pdf). Sec. 135 begins on 92 Stat. 2785. provisions.md and the CSV are updated.

## 3. Pending federal bills (119th Congress) affecting DC participation or withdrawals: status as of 2026-10-04
Sources: GovTrack API (status) and govinfo bill text via `https://www.govinfo.gov/link/bills/119/<type>/<number>`. The GovTrack keyword search is title-based and was rate-limited, so the list may miss bills with generic titles.

| Bill | Title / what it does (long title, govinfo) | Sponsor | Status (GovTrack) |
|---|---|---|---|
| S. 3333 | Emergency Savings Enhancement Act of 2025. PLESA: drops the restriction to non-HCE "eligible participants", raises the cap from $2,500 to $5,000, for tax years after 12/31/2026. Also adds employee-ownership grant funding | Young (R-IN), with Booker, Cassidy, Kaine | **Reported** by Senate HELP with an amendment (GovTrack 2026-07-30; bill text "August 5, 2026 Reported by Mr. Cassidy", Calendar No. 544). [govtrack](https://www.govtrack.us/congress/bills/119/s3333) |
| H.R. 6722 | Automatic IRA Act of 2025: "rules for automatic contribution retirement plans and arrangements" (federal auto-IRA/auto-plan mandate) | (Neal, W&M ranking member, per trade press) | Introduced 2025-12-15. [govtrack](https://www.govtrack.us/congress/bills/119/hr6722) |
| H.R. 6729 / S. 1831 | Auto Reenroll Act of 2025: "periodic automatic reenrollment under qualified automatic contribution arrangements" | Vindman (D-VA) / — |
| H.R. 10254 | MORE Savings Act (GovTrack title; the govinfo link returned unrelated text, so content not verified) | Dean (D-PA) | Introduced 2026-09-03 |
| S. 5550 | 529 Retirement Enhancement Act of 2026 (content not checked) | Cruz (R-TX) | Introduced 2026-09-24 | Introduced 2025-12-15 / 2025-05-21 |
| H.R. 2696 / S. 1526 | Retirement Savings for Americans Act of 2025: "establish the American Worker Retirement Plan" (federal plan with government contributions for workers without a plan) | Smucker (R-PA) / Hickenlooper (D-CO) | Introduced 2025-04-07 / 2025-04-30 |
| H.R. 6324 / S. 5156 | Retirement Simplification and Clarity Act: "in-service rollovers for individual retirement annuity purchases" | Panetta (D-CA) / Marshall (R-KS) | Introduced 2025-11-28 / 2026-07-29 |
| H.R. 6450 / S. 3352 | Retirement Rollover Flexibility Act: "permit rollover contributions from Roth IRAs to designated Roth accounts" (money into plans) | LaHood (R-IL) / Barrasso (R-WY) | Introduced 2025-12-04 (both) |
| S. 5507 | Saver's Match Enhancement Act of 2026: "expand retirement savings opportunities for more American families" | Wyden (D-OR) | Introduced 2026-09-24 |
| S. 2217 | Independent Retirement Fairness Act: pension plans for independent workers | Cassidy (R-LA) | Introduced 2025-07-09 |
| H.R. 10039 / S. 5204 | SMART Savings Act of 2026: exempts individual account plans from certain prohibited-transaction rules (investment menu; adjacent) | Tenney (R-NY) / — | Introduced 2026-08-03 / 2026-07-30 |
| S. 2403 (adjacent) | Retire through Ownership Act: ESOP "adequate consideration" valuation safe harbor | Marshall (R-KS) | **Passed both chambers 2026-09-16**, sent to the President; not shown as enacted on 2026-10-04. Enrolled text on govinfo. Not a participation or withdrawal provision |

No 2026 statute changing DC participation or withdrawal rules was found. The previous provisions.md description of H.R. 6324 as a general "simplification" bill is corrected: it concerns in-service rollovers to buy annuities. **Could not verify:** committee press releases (W&M, Senate Finance) were not checked one by one; congress.gov not used.

## 4. Pending final rules: verified on reginfo.gov and the Federal Register
OIRA file "EO_RULES_UNDER_REVIEW.xml" (RUNDATE 2026-10-04) — [reginfo.gov](https://www.reginfo.gov/public/do/XMLViewFileAction?f=EO_RULES_UNDER_REVIEW.xml):

| RIN | Title | Stage | Received by OIRA | Status 2026-10-04 |
|---|---|---|---|---|
| 1545-BR08 | Automatic Enrollment Requirements Under Section 414A | Final Rule | **2026-06-23** | Under review. **Verified**; trade-press date confirmed |
| 1210-AC21 | Exemption for Certain Automatic Portability Transactions (econ. significant) | Final Rule | **2026-09-14** | Under review. **New** |
| 1545-BQ70 | LTPT 401(k) regs | — | not at OIRA | Agenda target "Final Action 09/00/2026" |

- Unified Agenda (pubId 202510) targets: 414A "Final Action 07/00/2026"; auto-portability "Final Rule 09/00/2026"; LTPT "Final Action 09/00/2026" — [1545-BR08](https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=1545-BR08), [1210-AC21](https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=1210-AC21), [1545-BQ70](https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=1545-BQ70).
- Federal Register API, searched by RIN: each RIN has only its proposed rule (1545-BR08: 2025-01-14; 1210-AC21: 2024-01-29; 1545-BQ70: 2023-11-27). **No final rule was published through 2026-10-04.** provisions.md and the CSV are updated.

## 5. PSCA figures
### In auto_enrollment.md (edited)
| Figure | Result |
|---|---|
| "60% default at 4%+", "nearly 7 in 10" AE plans with auto-escalation (attributed to the PSCA 68th survey) | **Corrected (misattributed).** The Mar 2024 PSCA news item reposted Vanguard's How America Saves 2024 preview. Now cited to Vanguard HAS 2025: 61% at 4%+ in 2024 (39% in 2014), about 60% in 2023 (chart), and 69% of AE plans with annual increases 2020-24 [recordkeeper] |
| "More than half >3%", "36.4% at 3%" | **Could not verify.** These trace to an older PSCA survey (a search extract says the 60th). Replaced with the PSCA 62nd survey via 401k Specialist: >60% of AE plans default above 3%; 6% default 23.8% -> 29.7% (2017-18); 80% of AE plans facilitate increases |
| PSCA 2021: 58.8% of 557 plans with AE | **Verified** (CRS IF12756) |
| PSCA 67th (2023 plan year, 709 plans): 64% AE, 13% re-enroll, 86.9% deferring | **Verified** (PSCA press release, Dec 18 2024, BenefitsLink copy saved as `raw/gapB/PSCA_67th_survey_press_release_2024-12-18.pdf`; 64% via 401k Specialist) |
| PSCA 68th (2024 plan year, 755 plans): 64.3% AE, 36.2% of 1-49-participant plans, 87.4% deferring | **Could not verify** (psca/napa blocked; search extracts only; auto-escalation share conflicts between extracts) |

### In stay_in_plan_leakage.md (not edited)
| Figure (line) | Status |
|---|---|
| 29.3% of plans adopting the $1,000 emergency withdrawal (line 41, "plan year 2023") | **Verified:** "29.3% are adopting the provision allowing a $1,000 emergency withdrawal" — PSCA 67th survey press release (2023 plan year), [BenefitsLink copy](https://benefitslink.com/articles/psca-survey-results-20241218.pdf). Same release: 72% natural-disaster distributions, 52.3% QBAD, 48.9% terminal illness, <1% PLESA, 2% student-loan match; hardship withdrawals 2.1% of participants (1.5% in 2022); loans outstanding 17.5% |
| 36% of plans adopting the emergency withdrawal (68th survey, 2024 plan year) | **Could not verify** (psca.org/napa-net.org 403). Search extracts consistently give 36% and PLESA 1.3% |
| 68th survey hardship 2.7% of participants (2024) vs 2.1% (2023) | 2.1% verified (67th release); 2.7% could not verify |
| PSN: 549 completed auto-portability transactions by 1 Dec 2024 (line 289) | **Verified:** "549 auto portability transactions have been completed as of December 1, 2024" and "7,841 ... are in motion" — PSN press release (Dec 2024) as reposted by [BPRW](https://150.starofzion.org/2024/12/09/bprw-portability-services-network-jump-starts-nationwide-adoption-of-auto-portability/). Also 15,000+ plans and about 5M participants ([RCH, 3 Dec 2024](https://rch1.com/blog/psn-auto-portability-signs-up-15000-plans-in-year-one)) |
| PSCA "Automatic Rollover Rates" (June 2026), "Auto-Portability is Taking Off with Larger Plans" (May 2026) | **Could not verify** (psca.org 403; no trade-press mirror found) |

## 6. Clark & Young (Vanguard 2021) and SMarT (JPE 2004): auto_enrollment.md edited
- **Clark & Young: verified via secondary sources; primary PDF not retrievable.** 813,918 new hires in 520 plans; 91% vs 28% participation (new hires); 92% vs 29% after 3 years; <$15k earners 82% vs 4%; 70% of plans pair AE with escalation. These come from two independent trade-press summaries ([401k Specialist](https://401kspecialistmag.com/new-data-further-showcases-power-of-auto-enrollment/), [PLANSPONSOR 2021-04-08](https://www.plansponsor.com/vanguard-report-underscores-power-automatic-enrollment/)). The 63/63/60% escalation acceptance is **verified** in [Choi et al. 2024, NBER w32828](https://www.nber.org/system/files/working_papers/w32828/w32828.pdf), pdf pp.7 and 28 (the earlier note said p.5; the body text is on pdf p.7). The same source adds 29/42/52% of new hires gone by years 1/2/3.
- **SMarT: corrected.** "More than 80% of those offered signed up" -> **78%** per the JPE abstract ("a high proportion (78 percent) of those offered the plan joined"; 80% stayed through the 4th raise; 3.5% -> 13.6% over 40 months) — [EconPapers abstract](https://econpapers.repec.org/paper/febnatura/00337.htm). "Over 80 percent" is Thaler's rounded JEC testimony wording, and the 9.4% at 14 months is also from that testimony (p.2). The JPE full text is 403.

## 7. GAO-24-103577: verified
Highlights PDF obtained via WebFetch (gao.gov blocks curl); saved as `raw/gapB/GAO-24-103577_highlights.pdf`. Title: "401(k) PLANS: Additional Federal Actions Would Help Participants Track and Consolidate Their Retirement Savings", January 2024 (publicly released Feb 20 2024).
- "Of these participants with access, 6 percent took a Coronavirus-Related Distribution and less than 1 percent took a CARES Act loan." **Verified.**
- 2020 CRDs: average **$18,344**, median $9,000. 2019 hardship withdrawals: average $6,913, median $3,144. 2020 CARES loans: average $33,793, median $11,998. 2019 loans: average $9,564, median $5,097 (source: GAO survey of 14 record keepers). **Verified.**
- Context: the 14 companies covered "about 64 percent of all active 401(k) participants"; "about 80 percent of them had access to the CARES Act options"; "less than one-third of the plans" offered them.
- Australia: "close to 4.7 million accounts valued at $7.11 billion AUD (about $4.61 billion USD) have been reunited ... between late 2019 and the end of 2022." **Verified.** Also: 25% said rollovers had too many steps and 22% were unclear on forms; two-thirds would find a pension dashboard useful.
- Implication (Computed): about 80% x 6% = **about 4.8%** of the represented active participants took a CRD.

## 8. TSP FERS participation 2008, 2010, 2011, 2013: added to auto_enrollment.md Table A (approximate)
- PBD 2014 Figure 1 (p.4) prints bar labels, read from the rendered image (pdftoppm): **86.6% (2010), 88.2% (2011), 89.0% (2012), 89.6% (2013), 89.9% (2014)**.
- PBD 2012 Figure 1 (pdf p.4) has no labels. Pixel measurement against axis ticks gives 87.4 (2008), 84.68 (2009), 86.61 (2010), 88.21 (2011), 88.60 (2012). It matches the text values 84.7 and 88.6 within 0.02 pp, which supports the method.
- Inconsistency: 2012 is 88.6% in PBD 2012 but 89.0% in PBD 2014 (revised data). PBD 2014 Table 1 also revises <2-year-tenure 2012 participation from 97.9% to 98.2%. Labeled approximate. No FRTIB text source stating these values was found.

## Files changed
- `notes/provisions.md`: 414A OIRA (verified), auto-portability final rule at OIRA, LTPT status, Revenue Act clause, RI row and gap, pending-bills bullet.
- `output/provisions_timeline.csv`: 5 rows (Revenue Act sec. 135; SECURE 2.0 secs. 101, 120, 125; SECURE sec. 112).
- `notes/auto_enrollment.md`: SMarT, Clark & Young, TSP chart values and Table A rows, PSCA bullet rewritten, gaps.
- New raw files: `raw/gapB/GAO-24-103577_highlights.pdf`, `raw/gapB/PSCA_67th_survey_press_release_2024-12-18.pdf`.
