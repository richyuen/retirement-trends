# RMD policy, administrative tax-data evidence, and aggregate retirement account distributions (United States)

Research notes compiled 2026-10-03. Scope: US only; retirement-age withdrawals (about 59½ and older); pre-retirement leakage only as brief context.

Method note (applies to every number below): pages and PDFs were read through an automated fetch-and-extract tool. Direct file downloads were blocked by the session's network policy, so IRS/ICI spreadsheets (.xlsx/.xls) could not be opened; where a series exists only in a spreadsheet it is listed under Gaps. Numbers that I calculated are marked "computed" with inputs. Numbers read only once from a dense table are marked "single read". Where two readings of the same document disagreed, that is stated.

---

## 1. Policy timeline governing withdrawals in retirement (effective dates, statutory citations, Uniform Lifetime Table)

### Takeaway
The two age gates are the 10% additional tax before 59½ and the RMD start age, which was 70½ until 2019, 72 for 2020 to 2022, 73 from 2023, and is scheduled to be 75 from 2033. RMDs were waived outright twice (calendar 2009 and calendar 2020), and the divisor table was loosened twice (2002/2003 and 2022); the 2022 table cut the RMD percentage by roughly 6% to 7.5% at ages 72 to 90 (computed).

### Cited Findings

Early-withdrawal rule (59½)
- Traditional IRAs were created by ERISA 1974 (P.L. 93-406); withdrawals before 59½ carry an additional 10% tax. — [Stuart & Bryant, "The Impact of Withdrawal Penalties on Retirement Savings", pp. 1-4](https://www.aeaweb.org/conference/2022/preliminary/paper/7e3b6nQN); [CRS 96-20 EPW (June 8, 1998)](https://www.everycrsreport.com/files/19980608_96-20_7c1bac842cf6e2af124eb901c77bcdb29bd7f108.html)
- Exceptions listed by CRS (Dec 22, 2008): age 59½, death, disability, QDRO, separation from service at 55+, ESOP dividends, IRS levy, medical expenses above 7.5% of AGI, substantially equal periodic payments; IRA-only: health insurance while unemployed, higher education, first home (up to $10,000). — [CRS RL31770, "Individual Retirement Accounts and 401(k) Plans: Early Withdrawals and Required Distributions"](https://www.everycrsreport.com/reports/RL31770.html)
- P.L. 104-191 (HIPAA, 1996) added penalty-free early withdrawals for certain health expenses; the Taxpayer Relief Act of 1997 created the Roth IRA and added penalty-free withdrawals for higher education and first-home purchase. — [CRS 96-20 EPW](https://www.everycrsreport.com/files/19980608_96-20_7c1bac842cf6e2af124eb901c77bcdb29bd7f108.html)

RMD age 70½ and the 50% excise tax
- "In 1962, Congress established formal distribution requirements for Keogh plans ... requiring plan owners to begin taking distributions by the later of the year in which they retired or the year in which they reached age 70½." Stated purpose: "RMD rules limit the revenue cost of tax deferral and help to focus the tax subsidy for saving on accumulations for retirement." Penalty: "an excise tax of 50% of the required, but undistributed, amount." — [Brown, Poterba & Richardson, NBER WP 20464](https://www.nber.org/system/files/working_papers/w20464/w20464.pdf)
- "Required withdrawals ... were imposed for IRAs as part of the Tax Reform Act of 1986"; first RMD due by April 1 of the calendar year after the holder turns 70½; penalty 50% of the amount not withdrawn. — [Stuart & Bryant, p. 5](https://www.aeaweb.org/conference/2022/preliminary/paper/7e3b6nQN). Tax Reform Act of 1986 is P.L. 99-514. — [congress.gov H.R. 3838](https://www.congress.gov/bill/99th-congress/house-bill/3838)
- Distributions must begin no later than April 1 of the year after reaching 70½; excise tax at 26 U.S.C. §4974. — [CRS RL31770](https://www.everycrsreport.com/reports/RL31770.html)
- Still-working exception: DC plan participants (other than 5% owners) may delay RMDs until retirement if the plan allows; IRAs have no such exception. — [CRS IF12750 (Aug 29, 2024)](https://www.everycrsreport.com/reports/IF12750.html)

2001 proposed and 2002 final regulations (lower RMD amounts)
- 1987 proposed regulations (52 FR 28070); January 2001 proposed regulations (66 FR 3928) "substantially simplified" the rules and introduced a uniform lifetime table based on the joint life expectancy of the owner and a hypothetical beneficiary 10 years younger. EGTRRA 2001 (P.L. 107-16) section 634 directed Treasury to update the life tables. Final regulations: T.D. 8987, 67 FR 18988, published April 17, 2002, effective January 1, 2003; for calendar year 2002 taxpayers could rely on the final, the 2001 proposed, or the 1987 proposed regulations. New tables were "derived by starting with the basic 2000 individual annuity mortality table and projecting mortality improvement for the period 2000 through 2003," blended 50% male / 50% female. — [Federal Register, T.D. 8987](https://www.federalregister.gov/documents/2002/04/17/02-8963/required-distributions-from-retirement-plans)
- "In 2002, the entire RMD schedule was relaxed due to a change in the life expectancy tables used by the IRS." — [Mortenson, Schramm & Whitten working paper, Sec. 3.1, Fig. 5](https://conference.nber.org/conf_papers/f85635/f85635.pdf)

2009 RMD suspension
- Worker, Retiree, and Employer Recovery Act of 2008 (H.R. 7327), P.L. 110-458, enacted December 23, 2008; section 201 "Provides a waiver of minimum distribution requirements for certain retirement plans and accounts for 2009." — [congress.gov H.R. 7327](https://www.congress.gov/bill/110th-congress/house-bill/7327)
- H.R. 7327 passed the House Dec 10, 2008 and the Senate Dec 12, 2008; suspended RMDs for 2009 only. — [CRS RL31770](https://www.everycrsreport.com/reports/RL31770.html)

SECURE Act of 2019
- SECURE Act = P.L. 116-94 (Dec 20, 2019). Section 114 raised the RMD age from 70½ to 72 for individuals who reach 70½ after Dec 31, 2019; section 401 limited life-expectancy payouts to eligible designated beneficiaries (10-year rule for others). — [Federal Register, T.D. 10001](https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions); [CRS IF12750](https://www.everycrsreport.com/reports/IF12750.html)
- 10-year rule: beneficiaries not taking life-expectancy payments must withdraw the entire balance "by December 31 of the year containing the 10th anniversary of the owner's death." — [IRS Publication 590-B (2025)](https://www.irs.gov/publications/p590b)

CARES Act 2020
- CARES Act = P.L. 116-136, enacted March 27, 2020. Section 2202: coronavirus-related distributions up to $100,000 in 2020, exempt from the 10% early-withdrawal tax; section 2203 "suspends RMDs for 2020," including first-time RMDs otherwise due by April 1, 2020; applies to DC plans (401(k), 403(b), 457(b)), traditional IRAs and designated Roth accounts. Notice 2020-50 (June 19, 2020) expanded eligibility; Notice 2020-51 (June 23, 2020) extended the rollover window to August 31, 2020 for amounts that would have been 2020 RMDs. — [CRS IN11441 (June 30, 2020)](https://www.everycrsreport.com/files/2020-06-30_IN11441_d3b56786563e2c15f0f7ecfe3aab0b374bc73bd6.html); enactment date from [ICI Research Perspective Vol. 28 No. 1](https://www.ici.org/files/2022/per28-01.pdf)
- IRS wording: "You are not required to make RMDs in tax year 2020, whether that distribution is one required after the initial RMD ... or the distribution that would be required by April 1." — [IRS Publication 590-B (2020)](https://www.irs.gov/pub/irs-prior/p590b--2020.pdf)

New life expectancy tables effective 2022
- T.D. 9930, 85 FR 72472, published Nov 12, 2020; applies to distribution calendar years beginning on or after Jan 1, 2022. "A 72-year-old IRA owner who applied the Uniform Lifetime Table under formerly applicable §1.401(a)(9)-9 ... used a life expectancy of 25.6 years. Applying the Uniform Lifetime Table set forth in these regulations, a 72-year-old IRA owner will use a life expectancy of 27.4 years." "The effect of these changes is to reduce required minimum distributions generally." — [Federal Register, T.D. 9930](https://www.federalregister.gov/documents/2020/11/12/2020-24723/updated-life-expectancy-and-distribution-period-tables-used-for-purposes-of-determining-minimum)
- Current Uniform Lifetime Table divisors: 72: 27.4; 73: 26.5; 74: 25.5; 75: 24.6; 76: 23.7; 77: 22.9; 78: 22.0; 79: 21.1; 80: 20.2; 81: 19.4; 82: 18.5; 83: 17.7; 84: 16.8; 85: 16.0; 90: 12.2; 95: 8.9; 100: 6.4; 105: 4.6; 110: 3.5; 115: 2.9; 120+: 2.0. — [26 CFR 1.401(a)(9)-9(c)](https://www.law.cornell.edu/cfr/text/26/1.401(a)(9)-9)
- Old table (2003 to 2021) divisors, ages 72 to 85: 25.6, 24.7, 23.8, 22.9, 22.0, 21.2, 20.3, 19.5, 18.7, 17.9, 17.1, 16.3, 15.5, 14.8. — [STWS comparison table](https://www.stwserve.com/life-expectant-factors-for-rmds/). Old table at 70: 27.4; 71: 26.5; 90: 11.4; 95: 8.6; 100: 6.3. — [IRS Publication 590-B (2019), Appendix B Table III](https://www.irs.gov/pub/irs-prior/p590b--2019.pdf) (the automated read of ages 77 to 84 in this PDF was garbled; ages 72 to 85 are taken from the STWS table, which matches the T.D. 9930 quote for age 72)
- Check on old table: Mortenson et al. report an RMD of "4.37% which applied to over 96% of 75-year olds in 2008" (1/22.9 = 4.37%, computed). — [Mortenson et al. WP](https://conference.nber.org/conf_papers/f85635/f85635.pdf)

SECURE 2.0 Act of 2022 (Division T of P.L. 117-328, Dec 29, 2022)
- Section 107: RMD age 73 for those who turn 72 after Dec 31, 2022 and 73 before Jan 1, 2033; age 75 for those who turn 73 after Dec 31, 2032. Birth-year mapping: before July 1, 1949: 70½; July 1, 1949 to Dec 31, 1950: 72; 1951 to 1958: 73; 1960 or later: 75; born in 1959: statute ambiguous, proposed regulations (89 FR 58644) say 73. — [CRS IF12750](https://www.everycrsreport.com/reports/IF12750.html)
- Section 302: excise tax cut from 50% to 25%, and to 10% if corrected in the correction window (generally within two years); effective 2023. Section 325: no lifetime RMDs from designated Roth accounts in employer plans, taxable years beginning after Dec 31, 2023. Sections 201, 202, 204, 327, 337 also implemented in the 2024 final rule. — [CRS IF12750](https://www.everycrsreport.com/reports/IF12750.html); [Federal Register, T.D. 10001](https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions)
- Section 202 (QLAC): repeals the 25%-of-balance limit and allows up to $200,000 (indexed) for contracts purchased on or after Dec 29, 2022. Section 307: indexes the $100,000 QCD limit. Section 115: penalty-free emergency personal expense distribution up to $1,000 a year, repayable within three years, distributions after Dec 31, 2023. Section 314: domestic abuse distribution, lesser of $10,000 (indexed) or 50% of vested balance, after Dec 31, 2023. Section 127: pension-linked emergency savings accounts, $2,500 cap. Section 126: 529-to-Roth IRA rollovers, $35,000 lifetime. — [T. Rowe Price SECURE 2.0 cheat sheet (2026 Q1)](https://www.troweprice.com/financial-intermediary/us/en/insights/articles/2026/q1/secure-2-0-act-cheat-sheet.html)
- Terminal illness withdrawals penalty-free; disaster withdrawals up to $22,000 (retroactive to Jan 26, 2021). — [AARP, May 1, 2026](https://www.aarp.org/money/retirement/savers-guide-to-secure-two-point-zero/)
- Original QLAC limit (2014 regulations): premium "must not exceed the lesser of $125,000 or 25% of the source balance." — [Panis & Brien for DOL/EBSA, Oct 24, 2016](https://www.dol.gov/sites/dolgov/files/ebsa/pdf_files/innovations-and-trends-in-annuities.pdf)

Qualified charitable distributions
- Created by the Pension Protection Act of 2006 (P.L. 109-280) for tax years 2006 and 2007; extended by P.L. 110-343, 111-312, 112-240, 113-295; made permanent by the PATH Act of 2015 (Division Q of P.L. 114-113) for distributions after Dec 31, 2014. Age 70½ or older. QCDs count toward the RMD. SECURE 2.0 section 307 indexed the limit and allowed a one-time split-interest QCD. Limits: $108,000 (2025), $111,000 (2026); split-interest $54,000 (2025), $55,000 (2026). — [CRS IF11377, updated Jan 15, 2026](https://www.everycrsreport.com/files/2026-01-15_IF11377_059b9cc6503b7b2bd5d08658b8e2a80ac2eb5d58.pdf)
- 2024 limits were $105,000 (QCD) and $53,000 (split-interest); QLAC premium limit rose from $200,000 to $210,000 for 2025; domestic abuse limit rose from $10,000 to $10,300 for 2025. — [IRS Notice 2024-80](https://www.irs.gov/pub/irs-drop/n-24-80.pdf)

2024 final regulations and 2025 to 2026 changes
- T.D. 10001, 89 FR 58886, published July 19, 2024, effective Sept 17, 2024, applies to distribution calendar years beginning Jan 1, 2025. If the employee dies after the required beginning date, the beneficiary must take annual distributions during the 10-year period. Notices 2022-53, 2023-54 and 2024-35 gave relief for missed annual payments for 2021 to 2024. — [Federal Register, T.D. 10001](https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions)
- IRS Announcement 2025-2 (Dec 18, 2024) moved the anticipated applicability date of parts of the July 2024 proposed RMD regulations (spousal election, partial annuity, Roth accounts, corrective distributions, QLAC) from Jan 1, 2025 to Jan 1, 2026, with a reasonable good-faith standard before then. — [Groom Law Group](https://www.groom.com/resources/irs-extends-anticipated-effective-date-for-certain-2024-proposed-rmd-rules-until-2026/)
- 2026 limits (Notice 2025-67): QLAC premium limit "remains $210,000"; QCD limit $108,000 to $111,000; split-interest $54,000 to $55,000; qualified long-term care distribution limit "remains $2,600"; domestic abuse distribution $10,300 to $10,500; elective deferral $23,500 to $24,500; IRA contribution $7,000 to $7,500; age-50 catch-up $7,500 to $8,000; ages 60 to 63 catch-up remains $11,250. — [IRS Notice 2025-67](https://www.irs.gov/pub/irs-drop/n-25-67.pdf)
- Qualified long-term care distributions (SECURE 2.0 section 334; IRC 401(a)(39), 72(t)(2)(N), 6050Z): available for distributions made after Dec 29, 2025 from defined contribution plans that adopt the feature; capped at the least of premiums paid, 10% of vested balance, or $2,500 indexed ($2,600 for 2026); taxable but exempt from the 10% tax. IRS guidance: Notice 2026-33 (May 20, 2026). — [Current Federal Tax Developments, May 20, 2026](https://www.currentfederaltaxdevelopments.com/blog/2026/5/20/demystifying-notice-2026-33-comprehensive-guidance-on-qualified-long-term-care-distributions-under-the-secure-20-act)
- One Big Beautiful Bill Act (signed July 2025): created "Trump accounts" (IRA-type accounts, $5,000 annual contribution cap, no distributions before age 18, $1,000 federal seed for children born 2025 to 2028) and a temporary deduction of up to $6,000 for people 65 and older, phased out above $75,000 single / $150,000 joint. The article reports no change to RMD or early-withdrawal rules. — [PLANADVISER, July 2025](https://www.planadviser.com/massive-tax-policy-bill-signed-law/)
- As of May 2026 the RMD age "remains at 73," next step age 75 in 2033. — [AARP, May 1, 2026](https://www.aarp.org/money/retirement/savers-guide-to-secure-two-point-zero/)
- IRS Publication 590-B (2025): QCD limit $108,000; one-time election $54,000; excess-accumulation excise tax 25% (10% if corrected timely); emergency personal expense distributions capped at $1,000; original Roth IRA owners "don't have to take distributions regardless of your age." — [IRS Publication 590-B (2025)](https://www.irs.gov/publications/p590b)

### Inferences
- RMD as a percent of the prior year-end balance equals 100 divided by the divisor (computed). Old table: 70: 3.65%; 72: 3.91%; 73: 4.05%; 75: 4.37%; 80: 5.35%; 85: 6.76%; 90: 8.77%; 95: 11.63%; 100: 15.87%. Current table: 72: 3.65%; 73: 3.77%; 75: 4.07%; 80: 4.95%; 85: 6.25%; 90: 8.20%; 95: 11.24%; 100: 15.63%.
- The 2022 table lowered the required percentage by 6.6% at 72, 6.8% at 73, 6.9% at 75, 7.4% at 80, 7.5% at 85, 6.6% at 90, 3.4% at 95 and 1.6% at 100 (computed as 1 minus old divisor / new divisor).
- A first-year RMD at 73 under the current table (3.77%) is about the same as the first-year RMD under the old 70½ rule (3.65% for owners who were 70 at year-end, 3.77% for those who were 71), so the age increases removed two to three years of forced withdrawals without raising the starting percentage.
- Policy has moved in one direction since 2002: later start, smaller percentages, lower penalty, Roth plan balances exempt. Each change mechanically lowers forced withdrawals for the cohorts affected.

### Gaps
- The specific Tax Reform Act of 1986 provisions (uniform 10% additional tax under IRC 72(t) for all qualified plans; uniform required beginning date of April 1 after the year of 70½ for all owners; 50% excise tax under IRC 4974 for all plans) and their effective dates could not be confirmed from a fetched primary source; the congress.gov summary of H.R. 3838 does not contain that text. The only fetched statements are Stuart & Bryant's (RMDs "imposed for IRAs as part of the Tax Reform Act of 1986") and Brown, Poterba & Richardson's (Keogh rule dating to 1962). The two sources date the origin differently; neither gives the 1974 IRA rule or the 1996 Small Business Job Protection Act still-working change (the congress.gov page for H.R. 3448 could not be fetched).
- No fetched source quantified how much the 2001/2002 regulations lowered the RMD at a given age relative to the 1987 proposed rules. The old-table divisor at 70 (27.4) is confirmed; the pre-2001 default divisor is not.
- SECURE Act section 113 (birth/adoption withdrawals) and section 107 (repeal of age cap on traditional IRA contributions), and the SECURE 2.0 Roth catch-up requirement and its regulatory timing, were not verified from fetched sources.
- CARES Act: the three-year income spread and repayment rule for coronavirus-related distributions, and the loan-limit section number, were not in the CRS insight fetched; the congress.gov page was blocked.
- The One Big Beautiful Bill Act public law number and exact signing date are not stated in the fetched article.
- The treatment of people born in 1959 is settled only in proposed regulations per CRS (age 73); one automated summary of the final rule listed "1959 or later: 75", which conflicts with CRS and should not be relied on.

---

## 2. Administrative tax-data and recordkeeper studies: withdrawal incidence and rates around RMD age and during suspensions

### Takeaway
Tax data show a step change at the RMD age: about one in four traditional IRA owners in their 60s withdraws in a year, versus roughly 85% to 90% right after 70½, and about half of those subject to RMDs would withdraw less if allowed. When RMDs were waived in 2009, about 35% to 40% of affected people stopped withdrawing, but a large minority kept taking the "phantom" RMD.

### Cited Findings

Mortenson, Schramm & Whitten (National Tax Journal 72(3), Sept 2019, pp. 507-542; DOI 10.17310/ntj.2019.3.02)
- Published abstract: "Using a nationally representative panel of 1.8 million IRA holders from 2000 to 2013, we estimate that around 50 percent of individuals would prefer to withdraw less than their required minimum. However, we also estimate that up to 38 percent of these RMD-constrained individuals did not respond to a temporary suspension of RMD rules in 2009." — [IDEAS/RePEc record](https://ideas.repec.org/a/ntj/journl/v72y2019i3p507-542.html)
- Working-paper version (March 2016; 5% random sample of individuals 60+ from IRS data, 1999 to 2014; about 2.6 million individuals a year; 37.58 million person-years for 2000 to 2013): "Approximately 25% of individuals younger than 70.5 took a distribution, with an average distribution of 6.2%, measured as a percent of the account balance"; in 2008 and 2010 "the proportion taking a distribution increases to over 90% for 70.5-year olds. The average size of a distribution jumps by 76% to 10.9% of the IRA account balance"; "In 2009, only 60% of 70.5-year old IRA-holders took a distribution, with an average distribution of 8.2% of account balances." Average among all individuals subject to RMDs: 13.1% of balances in normal years, 10.4% in 2009. — [Mortenson et al. WP, Sec. 4.1, Figs. 2-3](https://conference.nber.org/conf_papers/f85635/f85635.pdf)
- Same WP: "Under this definition, 35% of individuals are suspenders in 2009 – very similar to the findings of BPR" (authors' own estimate, Sec. 4.4); "65% of individuals in 2008 choose distributions amounts within 1 percentage point of their RMD"; in 2009 "approximately 20% of individuals made a withdrawal within half a percentage point of the distribution they would have been required to take"; WP estimate "at least 41%" would take less than the RMD if unconstrained (39% among 73-year-olds, Table 6). — [Mortenson et al. WP](https://conference.nber.org/conf_papers/f85635/f85635.pdf)
- Same WP descriptive statistics: "Among individuals in their 70.5 year, over 84% take their first RMD in their 70.5 year"; "Ninety-one percent of individuals take a normal distribution that satisfies their RMD"; "The average RMD in 2014 dollars is $5,893, approximately 5% of the IRA balance"; average normal distribution $12,991, 15% of prior-year balance in the full sample and 12% in the RMD sample; "In 2013, individuals age 60 or older held $3.8 trillion in wealth in IRAs"; share of people 60+ with a traditional IRA rose from 29% (2000) to 35% (2013). — [Mortenson et al. WP, Sec. 3.3, Table 2, Figs. 8-9](https://conference.nber.org/conf_papers/f85635/f85635.pdf)
- JCT staff version as reported in trade press (Feb 2019): "approximately 20% of 60-year-old IRA holders took distributions, and the percentage increased linearly until age 70, by which approximately 35% took a distribution"; "around 52% of individuals required to make a distribution would rather take a smaller distribution than an RMD"; those first subject to the rules at 70½ "are 28% more likely" to close accounts than those 60 to 70½. — [ASPPA summary of JCT study](https://www.asppa-net.org/news/2019/2/rmds-driven-income-level-jct-study-finds)

Brown, Poterba & Richardson (Journal of Public Economics; NBER WP 20464; TIAA-CREF data)
- Abstract: "roughly one third of those who were affected by minimum distribution rules discontinued their distributions in 2009"; "The probability of suspension declines substantially with age" and "rises modestly with economic resources"; monthly-payment takers were less likely to suspend than annual takers. — [NBER WP 20464](https://www.nber.org/papers/w20464)
- Detail: 327,286 TIAA-CREF participants received a distribution in 2008; balanced panel of 63,859; average age 76.7 in 2009. "Just over one third -- 35.5% -- of the participants who received a minimum distribution in 2008 suspended these payouts in 2009"; 36.5% among those taking only the RMD versus 35.1% among those taking the RMD plus other distributions; about 40% at ages 70 to 74 versus 23% over 90; top four asset deciles "about twice as likely" to suspend as bottom two (about 20% lowest decile, about 48% highest); primary participants 37.2% versus secondary beneficiaries 19.5%; "In 2010 ... the mean RMD was 102.6% of the mean 2008 level." — [NBER WP 20464 PDF](https://www.nber.org/system/files/working_papers/w20464/w20464.pdf)
- Same paper, national context from SOI: taxable IRA distributions "totaled $148 billion in 2007, $162 billion in 2008, $135 billion in 2009, and $194 billion in 2010"; taxpayers with withdrawals 10.7 million, 11.3 million, 9.7 million, 12.5 million. — [NBER WP 20464 PDF](https://www.nber.org/system/files/working_papers/w20464/w20464.pdf)

IRS SOI on the 2009 suspension
- "Of the 8.1 million taxpayers age 70½ and over holding a traditional IRA in 2009, some 3.2 million taxpayers took advantage of the suspension by not withdrawing money from their accounts"; among those under 75 (3.0 million taxpayers), "46 percent chose not to take a withdrawal." All-IRA withdrawals rose 48% from 2009 to $257.6 billion in 2010, and taxpayers with withdrawals rose 13.9% to 13.5 million. — [Bryant & Gober, SOI Bulletin Fall 2013, "Accumulation and Distribution of Individual Retirement Arrangements, 2010"](https://www.irs.gov/pub/irs-soi/13inirafallbul.pdf)

Stuart & Bryant (IRS 5% sample, 1999 to 2015; 3,913,401 IRA holders; cross-section for 2005, N = 1,449,868)
- Share of traditional IRA holders taking a withdrawal, 2005: 10.4% at 58½, 20.4% at 59½ (+10.0 points); 32.4% at 69½, 87.3% at 70½ (+54.9 points). 1.4% of holders (about 648,400) retime withdrawals because of the early-withdrawal penalty, with about $12.6 billion a year not withdrawn; 16.2% (about 7.7 million) retime because of the excess-accumulation penalty, with $45.3 billion a year withdrawn earlier than otherwise. Abstract: penalties "cause over 17% of traditional IRA holders to change their withdrawal timing each year, shifting almost $60 billion of distributions annually." — [Stuart & Bryant, Fig. 3 and Table 2](https://www.aeaweb.org/conference/2022/preliminary/paper/7e3b6nQN)

Goda, Jones & Ramnath (IRS data)
- Average annual IRA withdrawals rise from $1,965 to $3,540 ("an 80 percent increase") after people cross 59½. — [CRR summary, "People Tap IRAs After the Penalty Ends"](https://crr.bc.edu/people-tap-iras-after-the-penalty-ends)

Brady, Bass, Holland & Pierce (ICI Research Report, April 7, 2017; SOI 1999 Edited Panel through tax year 2010; workers 55 to 61 in 1999; 7.2 million of 12.5 million claimed Social Security 2000 to 2007 and survived three years)
- "81 percent of individuals had income, either directly or through a spouse, from employer retirement plans, annuities, or IRAs; and another 8 percent had a Form 1099-R ... a Form 5498 ... or both." Share receiving retirement income rose "from 67 percent one year after claiming to 72 percent three years after claiming." Median replacement rate three years after claiming: 103% overall; 123% lowest quintile; 103% middle quintile; 88% for the 95th to 99th percentile. — [Brady et al. 2017](https://www.idc.org/system/files/attachments/ppr_17_brady_tax_panel_data.pdf)
- Follow-up with tax year 2016 data: "70 percent or more of the population receiving retirement income directly or through a spouse from age 71 through age 91"; own-income incidence 43% at 65 and "64 percent or more" at 72; the last large jump in incidence is "from age 69 to age 71"; at 72 median per capita retirement income is $3,350 (ventile 5), $12,000 (ventile 10), $26,000 (ventile 15). — [Brady & Bass, "A Day in the Life Cycle", SOI working paper, Dec 10, 2024](https://www.irs.gov/pub/irs-soi/24rpchangesincomebyage.pdf)

2020 RMD waiver
- Derby, Goodman, Mackie & Mortenson (5% sample of IRS records, 2003 to 2020): "driven by the suspension of required minimum distribution rules, IRA withdrawals substantially declined in 2020 for those older than age 72"; in both 2009 and 2020 "there is a substantial shifting of mass from exactly the RMD to zero" (Fig. 4); "we do not see any obvious increase in retirement withdrawals for those aged 60-70." Context for under-59½: total withdrawals rose about $60 billion (25%) in 2020 while penalized distributions fell nearly 50%; about 165,000 people aged 20 to 58 withdrew within $500 of $100,000. — [Derby et al., arXiv 2204.12359](https://arxiv.org/pdf/2204.12359v1); [PRC record with abstract](https://repository.upenn.edu/entities/publication/bbc03c8e-93ce-4a64-abc1-a6d0428db9aa)
- ICI IRA Investor Database: 20.3% of traditional IRA investors took withdrawals in 2020 versus 25.1% in 2019; by age in 2020: 18 to 59: 6.0%; 60 to 69: 18.7%; 70 or older: 59.6%; 70 to 74: 49.7%; 75 or older: 67.2%. Among investors 70+ with withdrawals in 2020: 43.6% took exactly the Uniform Lifetime RMD, 2.4% the joint-table RMD, 0.4% an inherited-IRA RMD, 35.7% more than the RMD, 17.9% less. Earlier pattern: 13.9% withdrew in 2009 versus about 18% in 2007 and 2008 (one automated read attributes these to all investors, another attributes the 18% to ages 60 to 69; unresolved). — [ICI, "The IRA Investor Profile: Traditional IRA Investors' Activity, 2010–2020", March 2024](https://www.ici.org/files/2024/24-rpt-ira-traditional.pdf)
- ICI household survey: 23% of traditional IRA-owning households took withdrawals in tax year 2020 versus 27% in tax year 2019; 60% of those headed by someone 70+ withdrew in tax year 2020; 61% of withdrawers based the amount on the RMD in tax year 2020 versus 76% in tax year 2019. — [ICI Research Perspective Vol. 28 No. 1, Jan 2022](https://www.ici.org/files/2022/per28-01.pdf). For tax year 2019, 22% of households aged 59 to 69 and 81% aged 70+ withdrew. — [Vanguard, citing ICI, Feb 2023](https://workplace.vanguard.com/content/dam/inst/iig-transformation/insights/pdf/2023/Retirement-distribution-decisions-among-dc-participants.pdf)
- 2009 in the same survey: "Fifteen percent of traditional IRA–owning households took a withdrawal in tax year 2009" versus 19% in 2008 and 20% in 2007; 48% of withdrawers based the amount on the RMD in tax year 2009 versus 64% in tax year 2008; median withdrawal $7,500. — [ICI, "The Role of IRAs in U.S. Households' Saving for Retirement, 2010", Figs. 17 and 19](https://www.ici.org/pdf/fm-v19n8.pdf)
- EBRI/HRS (biennial 2002 to 2016): "The 2009 RMD waiver had a modest impact in lowering the share of households who made RMD-only withdrawals." — [EBRI Issue Brief 510, Ebrahimi, 2020](https://www.ebri.org/content/ira-withdrawal-patterns-in-times-of-crisis)

Move to age 72 (SECURE Act)
- EBRI IRA Database, owners with balances of $10,000 or more: "85.3% of IRA owners aged 71 took a distribution in 2019, when the RMD age was 70.5"; "In 2021, 82.4% of those aged 72 took a distribution"; "In 2021, only 31.7% of those at age 71 took a distribution; and in 2019, only 30% took a distribution at age 69." — [ASPPA report of Craig Copeland's EBRI 2025 Retirement Symposium presentation, March 2025](https://www.asppa-net.org/news/2025/3/rmds-a-default-withdrawal-strategy-regardless-of-secure-2.0-study-says)

How many take only the RMD
- J.P. Morgan Asset Management / EBRI (31,000 people approaching and entering retirement, 2013 to 2018): "Around 80% who are younger than RMD age are not taking withdrawals"; "around 84% of those subject to RMDs only took the required amount." — [EBRI release, June 24, 2021](https://www.ebri.org/content/new-combined-dataset-reveals-unique-insights-into-income-and-spending-in-retirement); [PLANSPONSOR](https://www.plansponsor.com/not-retirement-drawdown-strategy-can-affect-retirement-security/)
- EBRI IRA Database, 2015 (27.9 million accounts, 22.1 million individuals, $2.76 trillion): 24% of IRA owners and 27.5% of traditional IRA owners took a withdrawal; fewer than 12% of any age group under 60; among traditional owners 71+, "only slightly more than one-quarter" withdrew more than the RMD. — [EBRI Issue Brief by Copeland, Sept 12, 2017](https://www.ebri.org/retirement/content/overall-withdrawal-levels-from-iras-are-driven-by-the-minimum-distribution-rules)
- HRS, households 71+: share withdrawing no more than the RMD was 68% (2002), 67% (2004), 61% (2006), 67% (2008), 63% (2010), 64% (2012), 68% (2014), 65% (2016). — [EBRI Issue Brief 510 infographic](https://www.ebri.org/retirement/content/ira-withdrawal-patterns-in-times-of-crisis-ig)
- HRS 1998 to 2014: "as much as 82% of respondents who withdrew funds from their IRA took only the minimum required" (Table 4). — [Panis & Brien for DOL, 2016](https://www.dol.gov/sites/dolgov/files/ebsa/pdf_files/innovations-and-trends-in-annuities.pdf)

Noncompliance
- TIGTA, tax year 2012: "nearly 639,000 taxpayers with IRAs worth $40.4 billion who may not have taken required distributions"; sample error rate 28%; projected 121,419 noncompliant traditional IRA owners and $103.6 million potential revenue; SEP/SIMPLE: 23,777 potentially noncompliant, 40% sample error rate, 11,827 projected, $25.7 million. "Nearly 6,500 taxpayers ... submitted Form 5329 to self-report ... paid excise taxes totaling $6.2 million"; IRS sent 1,498 soft notices in a pilot. — [TIGTA 2015-10-042, May 29, 2015](https://www.oversight.gov/sites/default/files/oig-reports/201510042fr.pdf)
- Vanguard, 2024 (about 400,000 RMD-age Vanguard IRA clients): 6.7% took no withdrawal; 24% withdrew less than the RMD; 69% withdrew at or above the RMD; average RMD $11,600; 56.8% of balances under $5,000 missed versus 2.5% above $1 million; 55% of missers miss again the next year; national extrapolation 585,000 IRA holders and $678 million to $1.7 billion in potential penalties a year. — [Vanguard, Reed & Goodman, "How costly are missed RMDs?", Dec 17, 2025](https://corporate.vanguard.com/content/corporatesite/us/en/corp/articles/how-costly-are-missed-rmds.html)

Pre-retirement leakage (context only)
- Goodman, Mortenson, Mackie & Schramm (National Tax Journal 74(3), 2021, pp. 689-719; more than 140 million person-years, 2003 to 2015): distributions from DC plans and IRAs to people 50 or younger "were equal to 22 percent of the contributions made by this age group"; job separation raises the probability of leakage by more than 200%. — [NTJ abstract](https://www.journals.uchicago.edu/doi/10.1086/715819). JCT version: leakage ratio in the year of a job separation is "roughly 26 percentage points, relative to a baseline leakage ratio of seven." — [JCX-20-21, April 26, 2021](https://www.jct.gov/getattachment/ed1c9da4-f180-41cd-b3f9-b8afb9531d18/x-20-21.pdf)
- Argento, Bryant & Sabelhaus (Contemporary Economic Policy, 2015; SOI cross-sections 2004 to 2010 with Forms 1099-R and 5498), under age 55: gross distributions $170.0B (2004), $183.0B (2005), $206.4B (2006), $218.6B (2007), $209.6B (2008), $181.4B (2009), $229.8B (2010); net taxable $64.8B, $66.9B, $72.9B, $77.9B, $81.0B, $81.0B, $94.8B; penalized $29.7B, $30.9B, $35.2B, $39.9B, $42.4B, $42.3B, $47.3B. In 2010, 41% of gross was net taxable, 21% penalized, 66% of dollars rolled over; "for every dollar contributed, roughly 40 cents flowed back out." — [Argento et al. 2015](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/argento%20et%20al%20coep%202015.pdf)

CBO and JCT
- CBO expects "the retirement of members of the baby-boom generation to cause a gradual increase in distributions from tax-deferred retirement accounts, including individual retirement accounts, 401(k) plans, and traditional defined benefit pension plans," which "would boost revenues relative to GDP by 0.2 percentage points over the next decade" (p. 94). — [CBO, The Budget and Economic Outlook: 2016 to 2026, Chapter 4](https://thompsoncoburn.com/wp-content/uploads/2024/10/51129-chapter4.pdf); [NAPA summary](https://www.napa-net.org/news/2019/2/cbo-puts-figure-tax-revenue-impact-retirement-distributions/)

### Inferences
- In SOI data 3.2 million of 8.1 million traditional IRA owners aged 70½+ did not withdraw in 2009, which is 39.5% (computed: 3.2 / 8.1). That brackets the 35% (Mortenson et al., tax data) and 35.5% (TIAA) suspension estimates, which condition on having withdrawn in 2008.
- Returns reporting taxable IRA distributions fell 14.2% in 2009 and 16.2% in 2020; taxable amounts fell 16.6% and 12.6% (computed from the SOI series in Section 3). The two waivers produced declines of similar size in the national totals.
- Incidence just before the RMD age is about 30% to 35% in every dataset (JCT about 35% at 70; Stuart & Bryant 32.4% at 69½ in 2005; EBRI 30% at 69 in 2019 and 31.7% at 71 in 2021), and 82% to 90% just after. When the age moved from 70½ to 72, the low-incidence pattern moved with it, which indicates the rule, not age itself, drives the jump.
- Roughly a fifth of affected owners still withdrew the exact "phantom" RMD in 2009 and 43.6% of withdrawers aged 70+ took exactly the table amount in 2020, so the RMD also works as a default or anchor, not only as a constraint.
- Person-level average withdrawal rates in Mortenson et al. (12% to 15% of balance) are far above aggregate dollar-weighted rates (about 5% to 8%; see Section 4) because small accounts are often emptied; the two measures should not be mixed on one chart.

### Gaps
- No peer-reviewed or agency study using tax data was found for the move to age 73 in 2023; the only evidence is descriptive (ICI survey, SOI totals). Web search budget ran out before a targeted search for 2025 to 2026 working papers could be completed.
- Derby et al. give no numeric estimate (in the text that could be extracted) of the 2020 change in incidence or dollars for people 72 and older; their evidence is graphical.
- Fidelity and JPMorgan Chase Institute statistics on the 2020 waiver were not found.
- The JCT staff paper itself ("Estimating the Effects of the Required Minimum Distribution Rules on Withdrawals from Individual Retirement Arrangements") was read only through a trade-press summary; the 52% figure differs from the working paper (at least 41%) and the published abstract (around 50%).
- TIGTA's 639,000 and 121,419 figures do not reconcile with the stated 28% error rate (28% of 639,000 would be about 179,000, computed); the report was read once and the population to which the 28% applies is unclear.
- Mortenson et al.: it is not clear from the extract whether the 6.2% and 10.9% average distribution rates are conditional on taking a distribution.

---

## 3. Aggregate national time series from IRS SOI and related tabulations

### Takeaway
Taxable IRA distributions reported on Form 1040 rose from $87.1 billion on 8.1 million returns in 1999 to $438.1 billion on 16.7 million returns in 2023, with visible dips in the two waiver years (2009: $135.2 billion; 2020: $284.0 billion). Taxable pensions and annuities rose from $304.3 billion to $932.1 billion over the same span, so IRAs went from 22% to 32% of the combined taxable total (computed).

### Cited Findings

Form 1040 taxable IRA distributions and taxable pensions and annuities
- 1988 to 1996 taxable IRA withdrawals, $ billions (SOI via Sabelhaus Table 1): 1988: 11.1; 1989: 13.9; 1990: 17.6; 1991: 20.6; 1992: 26.3; 1993: 27.1; 1994: 33.1; 1995: 37.3; 1996: 45.5. — [Sabelhaus, "Modeling IRA Accumulation and Withdrawals", National Tax Journal 2000](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/sabelhaus%20ntj%202000.pdf) (single read)
- 1997: 6,287,644 returns, $55,558,686 thousand; 1998 (preliminary): 7,847,579 returns, $74,332,903 thousand (+33.8%), "partly due to the income resulting from conversions of traditional IRA's to Roth IRA's." Taxable pensions and annuities 1997: 19,729,019 returns, $264,326,557 thousand; 1998 (preliminary): 20,719,686 returns, $284,873,835 thousand. — [SOI, Individual Income Tax Returns, 1998 preliminary data](https://www.irs.gov/pub/irs-soi/98inprel.pdf)
- 1999 to 2016 taxable IRA distributions, amount in thousands of dollars: 1999: 87,140,912; 2000: 98,966,627; 2001: 94,327,585; 2002: 88,219,481; 2003: 88,335,605; 2004: 101,672,181; 2005: 112,277,199; 2006: 124,705,552; 2007: 147,959,327; 2008: 162,150,226; 2009: 135,202,708; 2010: 194,332,950; 2011: 217,319,190; 2012: 230,783,461; 2013: 213,602,353; 2014: 235,005,032; 2015: 253,213,041; 2016: 257,507,903. — [FRED series TIRADTSA, source IRS SOI Historical Data Tables](https://fred.stlouisfed.org/data/TIRADTSA)
- 1999 to 2016 number of returns with taxable IRA distributions: 1999: 8,129,376; 2000: 8,732,291; 2001: 8,834,138; 2002: 8,291,357; 2003: 8,611,702; 2004: 8,913,846; 2005: 9,387,189; 2006: 9,965,065; 2007: 10,683,225; 2008: 11,259,424; 2009: 9,659,133; 2010: 12,517,280; 2011: 13,008,887; 2012: 13,195,644; 2013: 13,331,179; 2014: 13,653,703; 2015: 14,159,018; 2016: 14,386,567. — [FRED series TIRADTS](https://fred.stlouisfed.org/data/TIRADTS)
- 1999 to 2016 taxable pensions and annuities, thousands of dollars: 1999: 304,310,714; 2000: 325,827,702; 2001: 338,745,409; 2002: 357,840,960; 2003: 372,931,442; 2004: 394,285,849; 2005: 420,144,855; 2006: 450,454,465; 2007: 490,581,465; 2008: 506,269,008; 2009: 523,295,800; 2010: 558,540,932; 2011: 581,180,358; 2012: 612,544,219; 2013: 638,659,076; 2014: 663,223,262; 2015: 689,991,999; 2016: 693,626,543. — [FRED series PATSIAGIA](https://fred.stlouisfed.org/data/PATSIAGIA)
- 1999 to 2016 returns with taxable pensions and annuities: 1999: 21,343,646; 2000: 21,765,211; 2001: 22,262,774; 2002: 22,794,417; 2003: 22,822,842; 2004: 23,123,390; 2005: 23,247,374; 2006: 24,098,220; 2007: 25,180,637; 2008: 25,540,246; 2009: 26,020,252; 2010: 26,596,737; 2011: 26,757,165; 2012: 27,289,708; 2013: 27,755,892; 2014: 28,143,561; 2015: 28,199,160; 2016: 27,860,995. — [FRED series PATSIAGI](https://fred.stlouisfed.org/data/PATSIAGI)
- 2015 to 2019 (Table A): taxable IRA distributions 2015: 14,159,018 returns, $253,213,041K; 2016: 14,386,567, $257,507,903K; 2017: 15,117,193, $286,496,949K; 2018: 253,031 returns, $5,523,744K, footnoted "Data from prior-year returns" (not comparable); 2019: 15,641,734, $324,971,510K. Taxable pensions and annuities 2017: 28,264,910 returns, $729,187,412K; 2018: 618,423, $16,511,632K (same footnote); 2019: 28,284,849, $784,497,673K. — [IRS Publication 1304 (Rev. 12-2021), Tax Year 2019, Table A](https://www.irs.gov/pub/irs-prior/p1304--2021.pdf)
- 2019 to 2022 (Table A): taxable IRA distributions 2019: 15,641,734 returns, $324,971,510K; 2020: 13,101,306, $284,005,168K; 2021: 15,584,165, $408,382,461K; 2022: 16,282,441, $437,775,580K (+4.5% returns, +7.2% amount vs 2021). Taxable pensions and annuities 2019: 28,284,849, $784,497,673K; 2020: 30,412,365, $827,597,726K; 2021: 29,357,159, $858,038,339K; 2022: 30,020,638, $911,698,884K. Taxable Social Security benefits 2018: 21,792,987 returns, $337,046,241K; 2019: 22,416,436, $360,038,769K; 2020: 23,057,234, $374,166,924K; 2021: 23,798,351, $412,830,233K; 2022: 24,667,460, $458,513,595K. — [IRS Publication 1304 (Rev. 1-2025), Tax Year 2022, Table A](https://www.irs.gov/pub/irs-pdf/p1304.pdf)
- 2023 (line-item estimates, returns processed in 2024; 160,602,107 returns): line 4a IRA distributions 17,839,121 returns, $505,480,278K; line 4b taxable amount 16,694,154 returns, $438,147,938K; line 5a pensions and annuities 32,538,787 returns, $1,594,900,577K; line 5b taxable amount 29,541,284 returns, $932,130,236K; line 6a Social Security 32,104,077 returns, $973,642,779K; line 6b taxable 25,716,763 returns, $527,072,873K. — [IRS Publication 4801 (Rev. 6-2026), Tax Year 2023](https://www.irs.gov/pub/irs-pdf/p4801.pdf)
- Gross (line 4a/5a) amounts for other years: 2019: IRA distributions 16,495,748 returns, $379,260,994K; pensions and annuities 30,830,618 returns, $1,290,875,434K. — [Publication 4801 (Rev. 12-2021), TY2019](https://www.irs.gov/pub/irs-prior/p4801--2021.pdf). 2020: IRA 14,205,309 returns, $353,034,392K; pensions 33,021,101 returns, $1,407,948,180K. — [Publication 4801 (Rev. 11-2022), TY2020](https://www.irs.gov/pub/irs-prior/p4801--2022.pdf). 2021: IRA $473,451,893K; pensions $1,506,948,061K (return counts 16,635,357 and 32,171,355 in one read, garbled in a second). — [Publication 4801 (Rev. 2-2024), TY2021](https://www.irs.gov/pub/irs-prior/p4801--2024.pdf)
- 2018 (Form 1040 combined IRAs, pensions and annuities on one line): line 4a 37,166,371 returns, $1,625,642,430K; line 4b taxable 34,701,850 returns, $1,087,228,437K. — [Publication 4801, TY2018](https://www.irs.gov/pub/irs-prior/p4801--2020.pdf)

SOI IRA study (Forms 5498 and 1099-R): withdrawals, rollovers, conversions
- Traditional IRA flows, $ billions, source "Investment Company Institute and Internal Revenue Service Statistics of Income Division" (Figure 1.2). Withdrawals: 2000: 96.8; 2001: 105.8; 2002: 116.7; 2003: 103.4e; 2004: 133.0; 2005: 119.3; 2006: 136.8; 2007: 159.0; 2008: 212.3; 2009: 165.2; 2010: 243.3; 2011: 189.6; 2012: 237.2; 2013: 243.7; 2014: 257.7; 2015: 276.9; 2016: 272.6; 2017: 303.4; 2018: 341.1. Rollovers: 1996: 114.0; 1997: 121.5; 1998: 160.0; 1999: 199.9; 2000: 225.6; 2001: 187.8; 2002: 204.4; 2003: 205.0e; 2004: 214.9; 2005: 228.5; 2006: 282.0; 2007: 316.6; 2008: 272.1; 2009: 257.3; 2010: 288.4; 2011: 297.5; 2012: 334.6; 2013: 393.4; 2014: 423.9; 2015: 459.9; 2016: 430.8; 2017: 463.0; 2018: 516.7. Contributions: 1996: 14.1; 1997: 15.0; 1998: 11.9; 1999: 10.3; 2000: 10.0; 2001: 9.2; 2002: 12.4; 2003: 12.3e; 2004: 12.6; 2005: 13.4; 2006: 14.3; 2007: 14.4; 2008: 13.4; 2009: 12.8; 2010: 12.8; 2011: 12.3; 2012: 15.5; 2013: 16.8; 2014: 17.5; 2015: 17.7; 2016: 18.3; 2017: 18.8; 2018: 18.6. Roth conversions: 1998: 39.3; 1999: 3.7; 2000: 3.2; 2001: 3.1; 2002: 3.3; 2003: 3.0; 2004: 2.8; 2005: 2.6; 2006: 2.8; 2007: 2.2; 2008: 3.7; 2009: 6.8; 2010: 64.8; 2011: 11.3; 2012: 18.1; 2013: 7.5; 2014: 8.3; 2015: 9.0; 2016: 9.1; 2017: 10.0; 2018: 13.7. Year-end assets: 1997: 1,642e; 1998: 1,974; 1999: 2,423; 2000: 2,407; 2001: 2,395; 2002: 2,322; 2003: 2,719e; 2004: 2,957; 2005: 3,034; 2006: 3,722; 2007: 4,187; 2008: 3,257; 2009: 3,941; 2010: 4,340; 2011: 4,459; 2012: 4,969; 2013: 5,828; 2014: 6,225; 2015: 6,387; 2016: 6,824; 2017: 8,018; 2018: 7,745; 2019: 9,165e; 2020: 10,290e. — [ICI, "The IRA Investor Profile: Traditional IRA Investors' Activity, 2007–2018" (2021), Figure 1.2](https://www.ici.org/files/2021/21_rpt_ira_traditional.pdf)
- 2020 inflows: traditional IRAs $616.9 billion, of which rollovers $594.8 billion and contributions $22.1 billion; Roth IRAs $85 billion, of which rollovers $17.5 billion, contributions $33.0 billion, conversions $34.5 billion. IRA assets: traditional $6,225B (2014), $10,722B (2020), $11,441B (2023 est.); Roth $600B, $1,233B, $1,405B; total $7,292B, $12,661B, $13,556B. — [CRS R48456, March 18, 2025, citing ICI](https://www.everycrsreport.com/files/2025-03-18_R48456_2da886a77ca615d09c68c1f445f261674c65ce7c.html)
- All IRA types: 2007: 11.8 million taxpayers withdrew $167.1 billion; 2008: 15.2 million withdrew $227.5 billion; rollovers 2007: 4.4 million taxpayers, $322.3 billion; 2008: 5.6 million, $272.1 billion. Definition: "Withdrawals are reported on Form 1099-R; does not include withdrawals made for the purpose of rollovers to other IRA accounts if the transfer was made by the trustee; Roth IRA conversions are shown separately." — [Bryant, SOI Bulletin Spring 2012, "Accumulation and Distribution of Individual Retirement Arrangements, 2008"](https://www.irs.gov/pub/irs-soi/12insprbulretirement.pdf) (single read)
- Tax year 2010, all IRA types, Table 4 (amounts in thousands): all taxpayers 54,428,897 with IRAs; 13,459,025 with withdrawals; withdrawals $257,611,337K; year-end fair market value $5,029,473,427K. Age 60 under 65: 6,664,113; 1,429,492; $43,292,551K; FMV $949,927,965K. Age 65 under 70: 5,022,545; 1,347,126; $41,021,477K; $877,341,166K. Age 70 under 75: 3,563,566; 2,705,865; $43,716,677K; $627,955,155K. Age 75 under 80: 2,530,225; 2,209,310; $29,937,344K; $408,213,641K. Age 80 and over: 2,765,906; 2,539,610; $30,082,310K; $307,803,175K. Traditional IRAs: 13.3 million taxpayers withdrew $243.3 billion. The 2010 jump was driven by "taxpayers at higher income levels, primarily those with an AGI of $100,000 or more, whose withdrawal amounts more than doubled from 2009 to 2010." — [Bryant & Gober, SOI Bulletin Fall 2013](https://www.irs.gov/pub/irs-soi/13inirafallbul.pdf) (age rows read twice, consistent)
- IRS SOI IRA tables exist through tax year 2023 (Table 1 by type of plan; tables by age), published as spreadsheets. — [SOI Tax Stats, Accumulation and Distribution of IRAs](https://www.irs.gov/statistics/soi-tax-stats-accumulation-and-distribution-of-individual-retirement-arrangements)
- Tax year 2023, Roth IRA row of SOI Table 1 as quoted by a secondary site: contributions 9,488,414 taxpayers, $32,809,393,000; conversions 1,597,798 taxpayers, $36,652,896,000. — [RothIRAHub data page citing IRS 23in01ira.xlsx](https://rothirahub.com/tools/statistics/)
- Tax year 2022 contributors: traditional IRAs 4,989,322 taxpayers, average $4,510; Roth IRAs 10,036,960 taxpayers, average $3,482. — [CRS R48051, updated Dec 3, 2025, citing IRS SOI](https://www.everycrsreport.com/files/2025-12-03_R48051_33c649736244ce72e13114e7b4f95fef86ca6107.html)

Three categories kept distinct (older participants leaving DC plans)
- Vanguard recordkeeping: 504,400 participants aged 60+ who terminated 2011 to 2020, followed through Dec 31, 2021. For the 2011 cohort at year-end 2021, participants: remained in plan without installments 3%, remained with installments 4%, rolled over to an IRA 57%, combination 8%, cash-out 28%. Assets: 8%, 8%, 66%, 13%, 5%. Average balances: stay without installments $418,900; stay with installments $347,200; rollover $239,300; combination $289,700; cash-out $39,700. Share remaining in plan by cohort: 2011: 7% of participants, 16% of assets; 2015: 14%, 27%; 2020: 32%, 46%. — [Vanguard, Clark & Walsh, "Retirement distribution decisions among DC participants", Feb 2023](https://workplace.vanguard.com/content/dam/inst/iig-transformation/insights/pdf/2023/Retirement-distribution-decisions-among-dc-participants.pdf) (single read)
- HRS, people who left employment with a DC plan and retired 2000 to 2006: 38.8% left funds in the account, 30.3% rolled over to an IRA, 15.8% took a withdrawal, 6.1% converted some or all to an annuity. DB retirees: 67.8% began the annuity, 8.6% took cash, 10.3% rolled over. — [GAO-11-400, Figs. 6-7](https://www.gao.gov/assets/a319390.html)
- 2025, all terminated participants in Vanguard plans: 83% preserved assets (stayed or rolled over); 97% of assets available for distribution were preserved. — [Vanguard, How America Saves 2026, Fig. 120](https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf)

### Inferences
- Combined taxable IRA plus pension and annuity income on Form 1040 (computed sums, $ billions): 1997: 319.9; 1999: 391.5; 2005: 532.4; 2010: 752.9; 2015: 943.2; 2017: 1,015.7; 2018 (single combined line): 1,087.2; 2019: 1,109.5; 2020: 1,111.6; 2021: 1,266.4; 2022: 1,349.5; 2023: 1,370.3.
- Taxable IRA distributions grew 5.03 times from 1999 to 2023 versus 3.06 times for taxable pensions and annuities (computed), and the IRA share of the combined total rose from 22.3% to 32.0% (computed).
- Year-over-year changes (computed): 2008 to 2009 amount −16.6%, returns −14.2%; 2009 to 2010 +43.7%, +29.6%; 2019 to 2020 −12.6%, −16.2%; 2020 to 2021 +43.8%, +19.0%; 2022 to 2023 +0.1%, +2.5%. The flat 2023 amount is consistent with the RMD age moving to 73 (no new cohort started RMDs in 2023) and lower end-2022 balances, but no study isolating those causes was found.
- Average taxable IRA distribution per return (computed): $10,719 (1999), $14,401 (2008), $17,899 (2016), $20,776 (2019), $26,246 (2023), nominal dollars.
- Gross minus taxable on Form 1040 (computed, $ billions): IRA line 54.3 (2019), 69.0 (2020), 65.1 (2021), 67.3 (2023); pension line 506.4 (2019), 580.4 (2020), 648.9 (2021), 662.8 (2023). The pension-line gap is the right order of magnitude for direct rollovers from employer plans plus non-taxable basis and Roth amounts; SOI does not label it that way in the documents read, so treat as indicative only.
- 2010 withdrawal incidence by age from SOI Table 4 (computed, taxpayers with withdrawals / taxpayers with IRAs): 60 to 64: 21.5%; 65 to 69: 26.8%; 70 to 74: 75.9%; 75 to 79: 87.3%; 80+: 91.8%; all ages 24.7%; 60 to 69 combined 23.8%; 70+ combined 84.1%. People 70+ took 40.3% of all IRA withdrawal dollars and people 60 to 69 took 32.7% (computed).
- SOI "withdrawals" for 2010 appear to include that year's large Roth conversions: traditional withdrawals are $243.3 billion in 2010 against $165.2 billion in 2009 and $189.6 billion in 2011, conversions were $64.8 billion, and SOI attributes the jump to taxpayers with AGI of $100,000 or more (2010 was the year the conversion income limit ended). If so, the traditional IRA withdrawal series overstates spending-type withdrawals in conversion-heavy years. This is my reading, not a statement in the source.
- 2009 all-IRA withdrawals back-calculated from SOI's stated growth rates: $257.6B / 1.48 = about $174.1 billion and 13.5 million / 1.139 = about 11.9 million taxpayers (computed, approximate because the growth rates are rounded).

### Gaps
- IRS SOI IRA Tables 1 to 8 for tax years 2019 to 2023 (withdrawals, rollovers, conversions, fair market value, by type and age) are spreadsheets and could not be read. Missing as a result: traditional IRA withdrawals after 2018, rollovers for 2019 and 2021 to 2023, conversions for 2019 and 2021 to 2022, and age breakdowns after 2010.
- 2018 cannot be split between IRA and pension lines (form change); Publication 1304 shows only a residual from prior-year returns.
- 1998 values are preliminary; final 1998 figures were not retrieved. 1988 to 1996 have dollar amounts only (no return counts).
- Gross (line 4a/5a) amounts for tax year 2022 and years before 2019 were not retrieved; the Publication 4801 for tax year 2022 returned a 404.
- Publication 4801 for tax year 2023: one of three automated reads returned different amounts for lines 4b, 5b and 6b ($437,775,580K; $858,038,339K; $458,513,595K), which a follow-up read located on page 9 (a confidence-interval table) rather than the Form 1040 line page. Those three numbers equal Table A values for tax years 2022, 2021 and 2022 respectively, so page 9 may carry stale figures. The values reported above are from the Form 1040 line-item page (page 15) and were returned by two reads. They could not be cross-checked against a tax year 2023 Publication 1304.
- No published table of Form 1099-R gross distributions by distribution code (normal, early, direct rollover, death, Roth) was found. JCX-20-21 Table A-1 ("Flows Between Individuals and the Retirement Saving System, 2015") exists but its numbers were not extractable. Argento et al. cover only people under 55.
- No official count of taxpayers subject to RMDs each year was found beyond SOI's 8.1 million traditional IRA owners aged 70½+ in 2009 and the 2010 age table.
- The 2008 SOI figures (15.2 million taxpayers with withdrawals) look inconsistent with 2009 (about 11.9 million, computed) and 2010 (13.5 million); the 2008 article was read once and may use a different definition.

---

## 4. Drawdown-rate evidence: what share of balances retirees withdraw

### Takeaway
Across tax, survey and recordkeeper data, most account owners take nothing before the RMD age and then take about the RMD: dollar-weighted withdrawals run near 4% to 5% of balances in the 60s and 7% to 10% in the 70s and 80s, and typical households still hold most of their starting assets after nearly two decades of retirement.

### Cited Findings
- SOI, 1993 to 1996: "The fraction of balances withdrawn from IRAs declines slightly with age ... from 2 to 3 percent when taxpayers are in their 30s to 1 to 2 percent when taxpayers are in their 50s"; "the kernel-smoothed point estimate for the age 65 withdrawal rate is less than 4 percent"; "The significant jump in withdrawal rates occur when taxpayers cross the age 70½ threshold." — [Sabelhaus 2000, Fig. 1](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/sabelhaus%20ntj%202000.pdf)
- SIPP 1997 to 2010 (personal retirement accounts = IRA, 401(k), Keogh): "Only 18 percent of PRA households in this age group [60 to 69] make any withdrawals"; "only seven percent ... take annual distributions of more than ten percent"; households 60 to 69 "withdraw only about two percent of their account balances each year"; after 70½ the share withdrawing "jumps to over 60 percent by age 71" and 70% a few years later; "the percentage of balances withdrawn remains at about five percent"; average balances keep rising after 70½. — [Poterba, Venti & Wise, NBER WP 16675](https://www.nber.org/system/files/working_papers/w16675/revisions/w16675.rev1.pdf)
- IRS panel 2000 to 2013: about 25% of IRA holders under 70½ take a distribution (average 6.2% of balance); over 90% at 70½ (average 10.9%); average among all subject to RMDs 13.1% of balance; average RMD about 5% of balance. — [Mortenson et al. WP](https://conference.nber.org/conf_papers/f85635/f85635.pdf)
- ICI household survey: traditional IRA-owning households that withdrew took "a median of 5% of the account balance" in tax year 2024; median 6% and median amount $14,000 in tax year 2022. — [ICI Research Perspective Vol. 32 No. 7, June 2026](https://www.ici.org/system/files/2026-06/per32-07.pdf); [ICI Research Perspective Vol. 30 No. 1, Feb 2024, Fig. 11](https://www.ici.org/files/2024/per30-01.pdf)
- ICI IRA Investor Database, 2020 median withdrawal amounts: ages 65 to 69 $12,260 (peak); 70 to 74 $7,200; 75+ $5,930. — [ICI 2024 traditional IRA report, Fig. A.21](https://www.ici.org/files/2024/24-rpt-ira-traditional.pdf) (single read)
- HRS, households 50 to 70: share making any IRA withdrawal 10% (2002), 11% (2004), 11% (2006), 13% (2008), 15% (2010), 14% (2012), 15% (2014), 15% (2016); withdrawals among them were 7.6% to 10.2% of balance; they "did not adjust their withdrawals relative to their account balance during the 2008–2010 market downturn." — [EBRI Issue Brief 510 infographic](https://www.ebri.org/retirement/content/ira-withdrawal-patterns-in-times-of-crisis-ig)
- J.P. Morgan / EBRI: about 80% below RMD age take no withdrawals and about 84% above take only the RMD; "The problem with using the RMD [as drawdown guidance] is that it is mismatched with how we observed households actually spending. It constrains spending in the beginning and leaves assets in the end." Median known retirement wealth about $110,000; 75% reduced equity exposure after rolling a 401(k) into an IRA (median 17% reduction). — [PLANSPONSOR](https://www.plansponsor.com/not-retirement-drawdown-strategy-can-affect-retirement-security/); [AAII Journal](https://www.aaii.com/journal/article/14761-how-retirees-handle-portfolio-allocation-income-and-spending); [401(k) Specialist](https://401kspecialistmag.com/most-retirees-wait-until-rmds-to-tap-retirement-accounts/)
- Vanguard, retirees still in plan: "Roughly 70% of retirees remaining in their plan after three years didn't take a withdrawal"; over half remain in plan at the end of the retirement year; 75% preserve assets three years after retiring; retirees who cash out have a median balance near $7,000. — [Vanguard, How America Retires 2025](https://workplace.vanguard.com/insights-and-research/report/how-america-retires-2025.html); [401(k) Specialist, Nov 2025](https://401kspecialistmag.com/how-america-retires-new-vanguard-report-shows-most-retirees-stay-in-plan-after-first-year/)
- BlackRock / EBRI (HRS, about 17 to 18 years into retirement): retirees with $500,000+ at retirement retained 83% of assets; $200,000 to $500,000 retained 77%; under $200,000 retained 80%; "more than one-third of retirees continue to grow their assets." — [PLANADVISER on "Spending Retirement Assets … or Not?"](https://www.planadviser.com/retirees-still-80-savings-nearly-two-decades/)
- EBRI (HRS and CAMS, 2015 dollars, first 18 years of retirement): under $200,000 "spent down (at the median) about one-quarter of their assets"; $200,000 to $500,000 "had spent down 27.2 percent"; $500,000+ "had spent down only 11.8 percent"; "about one-third of all sampled retirees had increased their assets"; pensioners' median non-housing assets "had gone down only 4 percent, compared to 34 percent for non-pensioners." — [EBRI, "Asset Decumulation or Asset Preservation? What Guides Retirement Spending?"](https://www.ebri.org/content/asset-decumulation-or-asset-preservation-what-guides-retirement-spending)
- CRR (HRS 1992 to 2018, cohorts born 1924 to 1953): households with DB coverage drew down 13 log points less wealth by 70 and 36 log points less by 75 and 80 (about $28,000 and $86,000 more remaining on $200,000); "Past generations drew down their financial wealth slowly ... forecasting drawdown for the currently retiring Boomers must account for ... the shift from DB to DC plans." — [Wettstein & Siliciano, CRR Issue in Brief 22-8, May 2022](https://crr.bc.edu/wp-content/uploads/2022/05/IB_22-8.pdf)
- T. Rowe Price (2022): "30% of retirees adjust their balances to maintain their spending, while 70% adjust their spending to maintain their retirement funds." — [NAPA](https://www.napa-net.org/news/2022/2/new-data-provides-different-take-decumulation/)
- Prescriptive benchmarks: experts cited by GAO suggest "annual withdrawals of 3 to 6 percent of the value of the investments in the first year of retirement." — [GAO-11-400](https://www.gao.gov/assets/a319390.html). Morningstar base-case safe starting rate 3.9% for 2025, 3.7% for 2024; guardrails 5.2%. — [401(k) Specialist on Morningstar State of Retirement Income 2025](https://401kspecialistmag.com/flexible-strategies-can-surge-starting-safe-retirement-withdrawals/)
- RMD as a spending rule: the Spend Safely in Retirement Strategy is to (1) delay Social Security and (2) "generate retirement income from savings using the IRS required minimum distribution (RMD) rules"; rule-implied rates 3.1250% at 65 and 3.6496% at 70; compared with 292 strategies on eight metrics; for middle-income retirees optimized Social Security "might comprise two-thirds to over 80% of the total retirement income." Stated drawback: "potential for significant fluctuations in year-to-year amounts." — [Pfau, Tomlinson & Vernon, Society of Actuaries / Stanford Center on Longevity, July 2019](https://www.soa.org/globalassets/assets/files/resources/research-report/2019/viability-spend-safely.pdf)
- Lifecycle model: delaying or eliminating RMDs "should have little effects on consumption profiles but more impact on withdrawals and tax payments for households with bequest motives"; with a bequest motive, at 75 under an age-75 rule "about 20% of retirees withdraw the required minimum fraction of 4.4%"; a progressive age-75 rule exempting accounts under $100,000 lowers tax payments about 7% relative to the age-72 rule. — [Horneff, Maurer & Mitchell, NBER WP 28490](https://www.nber.org/system/files/working_papers/w28490/w28490.pdf)

### Inferences
- Dollar-weighted IRA withdrawals as a share of year-end fair market value, SOI tax year 2010, all IRA types (computed from Table 4): 60 to 64: 4.56%; 65 to 69: 4.68%; 70 to 74: 6.96%; 75 to 79: 7.33%; 80+: 9.77%; all ages 5.12%; 60 to 69 combined 4.61%; 70+ combined 7.72%. 2010 includes large Roth conversions, so the 60s figures are probably overstated relative to a normal year.
- Traditional IRA withdrawals as a share of prior year-end traditional IRA assets (computed from ICI Figure 1.2): 2000: 4.00%; 2001: 4.40%; 2002: 4.87%; 2003: 4.45%; 2004: 4.89%; 2005: 4.03%; 2006: 4.51%; 2007: 4.27%; 2008: 5.07%; 2009: 5.07%; 2010: 6.17%; 2011: 4.37%; 2012: 5.32%; 2013: 4.90%; 2014: 4.42%; 2015: 4.45%; 2016: 4.27%; 2017: 4.45%; 2018: 4.25%. This is across owners of all ages, so it understates the rate among retirees and is stable at about 4% to 5%.
- Average withdrawal per withdrawing taxpayer in 2010 was $30,285 at 60 to 64 and $30,451 at 65 to 69 but $16,156 at 70 to 74, $13,551 at 75 to 79 and $11,845 at 80+ (computed). Voluntary early withdrawers take larger amounts; RMD-driven withdrawers take small ones.
- For RMD-only households, the withdrawal path is the table: about 3.8% at 73, 5% at 80, 6.3% at 85, 8.2% at 90 under the current table. The evidence that 65% to 84% take about the RMD implies the statutory table is the de facto national drawdown schedule for IRA balances.

### Gaps
- No study was retrieved that reports dollar-weighted withdrawal rates by single year of age for a recent year (2019 or later). The SOI age tables for 2011 to 2023 would allow this but are in unreadable spreadsheets.
- The J.P. Morgan "Mystery No More" paper and EBRI Issue Brief "In Data There Is Truth" were read only through press coverage; withdrawal amounts and what share of RMD cash is spent versus saved were not extracted.
- The Vanguard "How America Retires" PDF, earlier Vanguard retiree spending studies, the BlackRock white paper itself (link dead), Morningstar's and T. Rowe Price's primary reports were not read; figures are from summaries.
- JPMorgan Chase Institute and newer J.P. Morgan "Guide to Retirement" statistics were not retrieved (search budget exhausted).
- Evidence on drawdown from 401(k)-type plans specifically (as opposed to IRAs) in tax data is thin; plan-level evidence is Vanguard's.

---

## 5. Annuitization of DC and IRA balances

### Takeaway
Annuitizing DC or IRA money is rare and has been getting rarer where it is measured: about 6% of DC retirees annuitized in 2000 to 2006 HRS data, and at TIAA the share of new income-takers choosing a life annuity fell from 61% in 2000 to 18% in 2018 while RMD-only became the modal choice.

### Cited Findings
- TIAA, 2000 to 2018 (672,316 participants who first drew income): "the fraction of first-time retirement income claimants who selected a life-contingent annuitized payout stream declined from 61% to 18%"; "the fraction of retirees taking no income until their RMD rose from 10% to 52%"; average retirement age rose about 1.3 years for women and 2 years for men; average age at first income draw rose from 65.5 to 69.8; among all income recipients "the proportion who had a life annuity as part of their payout strategy fell from 52% in 2008 to 31% in 2018." Published in Journal of Pension Economics and Finance 24(1), Jan 2025, pp. 47-68. — [NBER WP 29946](https://www.nber.org/papers/w29946); [TIAA Institute Research Dialogue 182, Sept 2021](https://www.tiaa.org/content/dam/tiaa/institute/pdf/research-report/2021-09/tiaa-institute-trends-in-retirement-and-retirement-income-choices-by-tiaa-participants-2000-to-2018-rd-182-brown-september-2021.pdf)
- Same TIAA report, selected detail (single read): RMD-only share of first income draws 10% (2000), 28% (2007), 54% (2017), 52% (2018); life annuity share among first-time takers aged 70+ 41% (2000) to 5% (2018); systematic withdrawals peaked at 27% (2006) and were 17% in 2018; among all income recipients life annuity share 52% (2008) to 30.5% (2018) and RMD share 16% to 29% (Fig. 2.1). — [TIAA Institute RD 182](https://www.tiaa.org/content/dam/tiaa/institute/pdf/research-report/2021-09/tiaa-institute-trends-in-retirement-and-retirement-income-choices-by-tiaa-participants-2000-to-2018-rd-182-brown-september-2021.pdf)
- Earlier version (2000 to 2017): life-annuity share of first-time claimants "dropped from 54% in 2000 to 19% in 2017"; share making no withdrawals until RMD age rose "from 9% to 58%"; average age at first draw rose nearly five years. — [Brown, Poterba & Richardson, NBER RDRC NB19-10 summary, Sept 2019](https://www.nber.org/sites/default/files/2020-04/NB19-10%20Brown%20Richardson%20Poterba%20SUMMARY.pdf)
- HRS 2000 to 2006: "only 6 percent of those with a DC plan chose or purchased an annuity at retirement" (6.1%); 38.8% left funds in the plan; 30.3% rolled over; 15.8% took a withdrawal. — [GAO-11-400](https://www.gao.gov/assets/a319390.html)
- Plan menus, end of 2014 (GAO questionnaire to 11 record keepers with over 40% of 401(k) assets): "About three-quarters did not offer an annuity"; "about two-thirds did not offer a withdrawal option." — [GAO-16-433, Aug 2016](https://www.gao.gov/products/gao-16-433)
- Vanguard plans: installments other than RMDs offered by 68% of plans in 2025 (64% in 2021); ad hoc partial distributions by 43% (37% in 2021; 16% in 2015); the 2026 report contains no annuity distribution-option statistics. — [Vanguard, How America Saves 2026, Fig. 114](https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf); [401(k) Specialist on How America Retires](https://401kspecialistmag.com/how-america-retires-new-vanguard-report-shows-most-retirees-stay-in-plan-after-first-year/)
- QLACs: "Deferred income annuities (longevity annuities) ... accounted for less than $3 billion in 2015"; QLACs "are still in their infancy"; "As of December 2015, 11 insurance companies offered QLACs to individual IRA investors and only one offered QLACs to DC plans"; deferred income annuity sales $1.0B (2012), $2.2B (2013), $2.7B (2014), $2.7B (2015) in 2015 dollars; total individual annuity sales $237.2B (2014), $236.7B (2015); NAIC count for 2014: 2.7 million active immediate annuities versus 50.3 million deferred annuities. — [Panis & Brien for DOL/EBSA, Oct 24, 2016](https://www.dol.gov/sites/dolgov/files/ebsa/pdf_files/innovations-and-trends-in-annuities.pdf)
- LIMRA, 2025: total US individual annuity sales $461.3 billion (+6%); fixed-rate deferred $160.6B; fixed indexed $128.2B; registered index-linked $79.6B; traditional variable $65.2B; single premium immediate $14.0B (+3%); deferred income $4.8B (−3%). — [Insurance Business, Feb 16, 2026, citing LIMRA](https://www.insurancebusinessmag.com/us/news/breaking-news/us-annuity-sales-hit-record-461-billion-as-indexed-products-surge--limra-565533.aspx)

### Inferences
- Income annuities (immediate plus deferred income) were $18.8 billion of $461.3 billion in 2025 sales, or 4.1% (computed). Record annuity sales are almost entirely accumulation products, so they are not evidence of rising annuitization of retirement balances.
- Deferred income annuity sales were $2.7 billion in 2015 and $4.8 billion in 2025; QLACs are a subset, so QLAC volume remains small relative to roughly $18 trillion of IRA assets even after the 2023 limit increase to $200,000.
- TIAA is the most annuity-friendly large DC system, so a fall to 18% there suggests economy-wide annuitization of DC and IRA money is well below that.

### Gaps
- LIMRA data on the share of annuity premium funded with qualified (IRA or plan) money, and QLAC sales by year, were not found; search budget ran out. QLAC take-up after SECURE 2.0 is therefore unquantified here.
- The TIAA documents give 2000 starting values of 61% (abstracts), 54% (2019 version) and, in one automated read of the report text, 52%. These may reflect different denominators; the year-by-year series is only in a chart (Fig. 5.1).
- No TIAA data after 2018 and no economy-wide annuitization rate after the 2000 to 2006 HRS figure were retrieved.
- Share of 401(k) plans offering in-plan annuities in 2024 to 2026 (PSCA, Vanguard, TIAA trend reports) not retrieved.

---

## 6. Roth accounts: withdrawal incidence and the shift of new money to Roth

### Takeaway
Roth IRA owners in their 70s withdraw at about one-tenth the rate of traditional IRA owners (6.1% versus 59.6% in 2020, a waiver year; 6.8% of Roth owners aged 70+ in 2018) because there are no lifetime RMDs, and Roth now takes the majority of new IRA contributions and all conversion flows, so the share of retiree balances exempt from forced withdrawal will rise.

### Cited Findings
- 2020, share of investors with a withdrawal (Figure E.3): ages 18 to 59 Roth 2.5%, traditional 6.0%; 60 to 69 Roth 6.0%, traditional 18.7%; 70 or older Roth 6.1%, traditional 59.6%; all Roth 3.4%, traditional 20.3%. "Unlike traditional IRAs, there are no RMDs (unless the Roth IRAs are inherited)." Roth withdrawal incidence was "nearly 2.5 percent" in each of 2007, 2008 and 2009 and 3.3% in 2010. 35.2% of Roth IRA investors contributed in tax year 2020. — [ICI, "The IRA Investor Profile: Roth IRA Investors' Activity, 2010–2020", June 2024](https://ici.org/system/files/2024-07/24-rpt-ira-roth.pdf)
- 2018: 4.1% of Roth IRA investors took withdrawals versus 24.9% of traditional IRA investors; Roth by age: 18 to 59: 3.1%; 60 to 69: 6.9%; 70+: 6.8%. 33% of Roth investors were under 40 versus 16% of traditional; 76% of new Roth IRAs in 2018 were opened with contributions only. — [ICI, "Ten Important Facts About Roth IRAs", July 2022](https://ici.org/files/2024/ten-facts-roth-iras.pdf)
- Household survey, tax year 2024: 33% of traditional IRA-owning households withdrew versus "only 6%" of Roth IRA-owning households; 32.6% of US households own traditional IRAs, 27.8% own Roth IRAs, 17.1% own both. — [ICI Research Perspective Vol. 32 No. 7, June 2026](https://www.ici.org/system/files/2026-06/per32-07.pdf)
- Contributors, tax year 2022: 10,036,960 taxpayers contributed to Roth IRAs (average $3,482) versus 4,989,322 to traditional IRAs (average $4,510). — [CRS R48051](https://www.everycrsreport.com/files/2025-12-03_R48051_33c649736244ce72e13114e7b4f95fef86ca6107.html)
- 2020 flows: Roth contributions $33.0 billion and conversions $34.5 billion versus traditional contributions $22.1 billion; "39% of Roth IRA owners made contributions in tax year 2022 compared to 22% of traditional IRA owners"; 2022 SCF ownership: Roth 16.1% of households, traditional 13.3%, rollover 11.3%; median balances Roth $30,000, traditional $90,000, rollover $120,000. Roth IRA assets $600B (2014), $1,233B (2020), $1,405B (2023 est.), 10.4% of IRA assets in 2023. — [CRS R48456](https://www.everycrsreport.com/files/2025-03-18_R48456_2da886a77ca615d09c68c1f445f261674c65ce7c.html)
- Tax year 2023 (secondary quotation of SOI Table 1): Roth contributions $32.8 billion by 9,488,414 taxpayers; Roth conversions $36.65 billion by 1,597,798 taxpayers. — [RothIRAHub citing IRS SOI](https://rothirahub.com/tools/statistics/)
- Conversion history, $ billions (SOI via ICI): 1998: 39.3; 1999: 3.7; 2007: 2.2; 2009: 6.8; 2010: 64.8; 2012: 18.1; 2015: 9.0; 2018: 13.7 (full series in Section 3). — [ICI 2021 traditional IRA report, Fig. 1.2](https://www.ici.org/files/2021/21_rpt_ira_traditional.pdf)
- Employer plans (Vanguard): plans offering Roth contributions 77% (2019) to 98% (2025); participants using Roth when offered 12% (2019) to 18% (2025); 36% of plans offer in-plan Roth conversions and 4% of participants in those plans converted. — [Vanguard, How America Saves 2026, Fig. 41](https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf)
- Rule change: designated Roth accounts in employer plans have no lifetime RMDs for taxable years beginning after Dec 31, 2023 (SECURE 2.0 section 325). — [Federal Register, T.D. 10001](https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions)

### Inferences
- Roth share of traditional-plus-Roth IRA contribution dollars: 59.9% in 2020 (computed: 33.0 / (33.0 + 22.1)) and about 60.8% in tax year 2022 (computed: 10,036,960 × $3,482 = $34.95B Roth; 4,989,322 × $4,510 = $22.50B traditional). Roth share of contributors in 2022: 66.8% (computed).
- Annual conversions rose from $2 billion to $14 billion a year in 2007 to 2018 (outside the 2010 spike) to $34.5 billion in 2020 and $36.65 billion in 2023, so conversions now move more money into Roth IRAs than contributions do.
- Roth balances are still small (about 10% of IRA assets in 2023) and held by younger owners, so the effect on aggregate withdrawal incidence among people in their 70s is modest today and grows as these cohorts age. Rollovers, which dominate IRA inflows ($594.8B to traditional versus $17.5B to Roth in 2020), still go overwhelmingly to traditional IRAs.

### Gaps
- Roth IRA withdrawal dollars and incidence by age from SOI (tax data) for any year were not retrieved (spreadsheet only). The Roth-versus-traditional comparison above is from ICI's recordkeeper database and household survey.
- No series of Roth share of 401(k) contribution dollars was found; Vanguard reports participant take-up, not dollars.
- Conversions for 2019, 2021 and 2022 are missing. The tax year 2023 figures come from a secondary site quoting the IRS spreadsheet and were not verified against the IRS file.

---

## 7. Latest evidence (data years 2022 to 2025; publications in 2025 and 2026)

### Takeaway
The newest data show withdrawal incidence back above pre-waiver levels and still organized around the RMD: 33% of traditional IRA households withdrew in tax year 2024 (84% of those headed by someone 73+, 30% of those 59 to 72), 70% of withdrawers sized the withdrawal by the RMD, and national taxable IRA distributions were flat at about $438 billion in 2022 and 2023.

### Cited Findings
- Tax year 2024 (survey May to June 2025): "33% of households owning traditional IRAs reported taking withdrawals ... in tax year 2024, compared with 31% in tax year 2023, 31% in tax year 2022, 29% in tax year 2021, and 23% in tax year 2020"; 8% of households headed by someone under 59, 30% aged 59 to 72, 84% aged 73 or older; "70% of households owning traditional IRAs and making withdrawals in tax year 2024 calculated their withdrawal amount based on the RMD"; median 5% of balance; 37% used withdrawals for living expenses; 44% of retired withdrawing households reinvested or saved at least some; Roth IRA households: 6% withdrew. IRA assets $18.0 trillion in mid-2025, 39% of US retirement assets; 61% of traditional IRA households hold rollover money. — [ICI Research Perspective Vol. 32 No. 7, "The Role of IRAs in US Households' Saving for Retirement, 2025", June 2026](https://www.ici.org/system/files/2026-06/per32-07.pdf)
- Tax year 2022: 5% (under 59), 25% (59 to 69), 75% (70 or older) withdrew; 76% of withdrawers based the amount on the RMD; among households headed by someone 72+ with a withdrawal, 91% said it was based on RMD rules; median withdrawal $14,000, 6% of balance. Survey mode changed in 2016 from telephone to an online probability panel. — [ICI Research Perspective Vol. 30 No. 1, Feb 2024](https://www.ici.org/files/2024/per30-01.pdf)
- SOI: taxable IRA distributions $437,775,580K on 16,282,441 returns in tax year 2022 and $438,147,938K on 16,694,154 returns in tax year 2023; gross IRA distributions $505,480,278K on 17,839,121 returns in 2023; taxable pensions and annuities $911,698,884K (2022) and $932,130,236K (2023). — [Publication 1304 TY2022 Table A](https://www.irs.gov/pub/irs-pdf/p1304.pdf); [Publication 4801 TY2023](https://www.irs.gov/pub/irs-pdf/p4801.pdf)
- Vanguard IRA clients of RMD age, 2024: 6.7% took nothing, 24% took less than the RMD, 69% took at least the RMD; average RMD $11,600. — [Vanguard, Dec 17, 2025](https://corporate.vanguard.com/content/corporatesite/us/en/corp/articles/how-costly-are-missed-rmds.html)
- EBRI IRA Database, 2021: 82.4% of 72-year-olds and 31.7% of 71-year-olds took a distribution after the RMD age moved to 72 (2019: 85.3% at 71, 30% at 69). — [ASPPA, March 2025](https://www.asppa-net.org/news/2025/3/rmds-a-default-withdrawal-strategy-regardless-of-secure-2.0-study-says)
- Vanguard DC plans: over half of retirees remain in plan at the end of the retirement year; 75% preserve assets three years out; about 70% of those still in plan after three years took no withdrawal; retirees in plans with flexible distribution options are 30% to 35% more likely to stay; 68% of plans offered installments at year-end 2024 (58% ten years earlier) and 43% allowed ad hoc partial withdrawals (16% in 2015). In 2025, 83% of terminated participants preserved assets and 97% of assets were preserved. — [Vanguard, How America Retires 2025](https://workplace.vanguard.com/insights-and-research/report/how-america-retires-2025.html); [401(k) Specialist](https://401kspecialistmag.com/how-america-retires-new-vanguard-report-shows-most-retirees-stay-in-plan-after-first-year/); [How America Saves 2026](https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf)
- Published 2025: Brown, Poterba & Richardson on TIAA payout choices 2000 to 2018 (Journal of Pension Economics and Finance 24(1)). — [NBER WP 29946 page](https://www.nber.org/papers/w29946)
- Published Dec 2024: Brady & Bass, tax year 2016 incidence of retirement income by age. — [SOI working paper](https://www.irs.gov/pub/irs-soi/24rpchangesincomebyage.pdf)
- Rules new in 2025 to 2026: annual RMDs inside the 10-year window enforced from 2025; QCD limit $111,000 and QLAC limit $210,000 for 2026; long-term-care distributions from DC plans from Dec 30, 2025 (Notice 2026-33). — see Section 1 sources: [T.D. 10001](https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions); [Notice 2025-67](https://www.irs.gov/pub/irs-drop/n-25-67.pdf); [Notice 2026-33 summary](https://www.currentfederaltaxdevelopments.com/blog/2026/5/20/demystifying-notice-2026-33-comprehensive-guidance-on-qualified-long-term-care-distributions-under-the-secure-20-act)

### Inferences
- In the ICI survey the group just below the RMD age withdraws at 25% to 30% (59 to 69 in 2022; 59 to 72 in 2024) and the group above at 75% to 84%, the same two-level pattern seen in tax data for 2000 to 2013. Raising the age to 73 widened the low-incidence band by about two and a half years of age.
- The RMD-based share of withdrawers (64% in tax year 2008, 48% in 2009, 76% in 2019, 61% in 2020, 76% in 2022, 70% in 2024) drops only in waiver years, so reliance on the RMD as the sizing rule has not weakened.
- Total incidence among all traditional IRA households has trended up (15% to 22% in tax years 2009 to 2014; 25% to 27% in 2015 to 2019; 29% to 33% in 2021 to 2024), which fits an aging owner base, though part of the 2015 step coincides with the 2016 survey-mode change.

### Gaps
- No tax-data study of the 2023 move to age 73 or of behavior under the 2022 tables was found. No SOI age tables after 2010 could be read.
- Tax year 2024 SOI totals are not yet published in the documents reachable here; the latest SOI year is 2023.
- Fidelity, EBRI IRA Database (post-2021), and JPMorgan Chase data for 2023 to 2025 were not retrieved.

---

## Chart-ready series

All values are as reported unless marked computed. "K" = thousands of dollars.

### A. Form 1040 taxable IRA distributions (IRS SOI)

| Tax year | Returns | Amount ($K unless shown in $B) | Source URL |
|---|---|---|---|
| 1988 | n/a | $11.1B | https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/sabelhaus%20ntj%202000.pdf |
| 1989 | n/a | $13.9B | same |
| 1990 | n/a | $17.6B | same |
| 1991 | n/a | $20.6B | same |
| 1992 | n/a | $26.3B | same |
| 1993 | n/a | $27.1B | same |
| 1994 | n/a | $33.1B | same |
| 1995 | n/a | $37.3B | same |
| 1996 | n/a | $45.5B | same |
| 1997 | 6,287,644 | 55,558,686 | https://www.irs.gov/pub/irs-soi/98inprel.pdf |
| 1998 (preliminary) | 7,847,579 | 74,332,903 | same |
| 1999 | 8,129,376 | 87,140,912 | https://fred.stlouisfed.org/data/TIRADTS and https://fred.stlouisfed.org/data/TIRADTSA |
| 2000 | 8,732,291 | 98,966,627 | same |
| 2001 | 8,834,138 | 94,327,585 | same |
| 2002 | 8,291,357 | 88,219,481 | same |
| 2003 | 8,611,702 | 88,335,605 | same |
| 2004 | 8,913,846 | 101,672,181 | same |
| 2005 | 9,387,189 | 112,277,199 | same |
| 2006 | 9,965,065 | 124,705,552 | same |
| 2007 | 10,683,225 | 147,959,327 | same |
| 2008 | 11,259,424 | 162,150,226 | same |
| 2009 (RMD waiver) | 9,659,133 | 135,202,708 | same |
| 2010 | 12,517,280 | 194,332,950 | same |
| 2011 | 13,008,887 | 217,319,190 | same |
| 2012 | 13,195,644 | 230,783,461 | same |
| 2013 | 13,331,179 | 213,602,353 | same |
| 2014 | 13,653,703 | 235,005,032 | same |
| 2015 | 14,159,018 | 253,213,041 | same |
| 2016 | 14,386,567 | 257,507,903 | same |
| 2017 | 15,117,193 | 286,496,949 | https://www.irs.gov/pub/irs-prior/p1304--2021.pdf |
| 2018 | not separately available (form combined IRA and pension lines) | not available | https://www.irs.gov/pub/irs-prior/p1304--2021.pdf |
| 2019 | 15,641,734 | 324,971,510 | https://www.irs.gov/pub/irs-pdf/p1304.pdf |
| 2020 (RMD waiver) | 13,101,306 | 284,005,168 | same |
| 2021 | 15,584,165 | 408,382,461 | same |
| 2022 | 16,282,441 | 437,775,580 | same |
| 2023 | 16,694,154 | 438,147,938 | https://www.irs.gov/pub/irs-pdf/p4801.pdf |

### B. Form 1040 taxable pensions and annuities (IRS SOI)

| Tax year | Returns | Amount ($K) | Source URL |
|---|---|---|---|
| 1997 | 19,729,019 | 264,326,557 | https://www.irs.gov/pub/irs-soi/98inprel.pdf |
| 1998 (preliminary) | 20,719,686 | 284,873,835 | same |
| 1999 | 21,343,646 | 304,310,714 | https://fred.stlouisfed.org/data/PATSIAGI and https://fred.stlouisfed.org/data/PATSIAGIA |
| 2000 | 21,765,211 | 325,827,702 | same |
| 2001 | 22,262,774 | 338,745,409 | same |
| 2002 | 22,794,417 | 357,840,960 | same |
| 2003 | 22,822,842 | 372,931,442 | same |
| 2004 | 23,123,390 | 394,285,849 | same |
| 2005 | 23,247,374 | 420,144,855 | same |
| 2006 | 24,098,220 | 450,454,465 | same |
| 2007 | 25,180,637 | 490,581,465 | same |
| 2008 | 25,540,246 | 506,269,008 | same |
| 2009 | 26,020,252 | 523,295,800 | same |
| 2010 | 26,596,737 | 558,540,932 | same |
| 2011 | 26,757,165 | 581,180,358 | same |
| 2012 | 27,289,708 | 612,544,219 | same |
| 2013 | 27,755,892 | 638,659,076 | same |
| 2014 | 28,143,561 | 663,223,262 | same |
| 2015 | 28,199,160 | 689,991,999 | same |
| 2016 | 27,860,995 | 693,626,543 | same |
| 2017 | 28,264,910 | 729,187,412 | https://www.irs.gov/pub/irs-prior/p1304--2021.pdf |
| 2018 | not separately available | not available | same |
| 2019 | 28,284,849 | 784,497,673 | https://www.irs.gov/pub/irs-pdf/p1304.pdf |
| 2020 | 30,412,365 | 827,597,726 | same |
| 2021 | 29,357,159 | 858,038,339 | same |
| 2022 | 30,020,638 | 911,698,884 | same |
| 2023 | 29,541,284 | 932,130,236 | https://www.irs.gov/pub/irs-pdf/p4801.pdf |

2018 combined line (IRAs, pensions and annuities): total 37,166,371 returns, $1,625,642,430K; taxable 34,701,850 returns, $1,087,228,437K (https://www.irs.gov/pub/irs-prior/p4801--2020.pdf).

### C. Form 1040 gross versus taxable (line-item estimates)

| Tax year | Gross IRA distributions ($K) | Taxable IRA ($K) | Gross pensions and annuities ($K) | Taxable pensions ($K) | Source URL |
|---|---|---|---|---|---|
| 2019 | 379,260,994 | 324,971,510 | 1,290,875,434 | 784,497,673 | https://www.irs.gov/pub/irs-prior/p4801--2021.pdf |
| 2020 | 353,034,392 | 284,005,168 | 1,407,948,180 | 827,597,726 | https://www.irs.gov/pub/irs-prior/p4801--2022.pdf |
| 2021 | 473,451,893 | 408,382,461 | 1,506,948,061 | 858,038,339 | https://www.irs.gov/pub/irs-prior/p4801--2024.pdf |
| 2022 | not retrieved | 437,775,580 | not retrieved | 911,698,884 | https://www.irs.gov/pub/irs-pdf/p1304.pdf |
| 2023 | 505,480,278 | 438,147,938 | 1,594,900,577 | 932,130,236 | https://www.irs.gov/pub/irs-pdf/p4801.pdf |

### D. Traditional IRA flows (IRS SOI via ICI), $ billions

Source for all rows: https://www.ici.org/files/2021/21_rpt_ira_traditional.pdf (Figure 1.2); 2020 row from https://www.everycrsreport.com/files/2025-03-18_R48456_2da886a77ca615d09c68c1f445f261674c65ce7c.html. "e" = estimated by source. Withdrawals/prior-year assets is computed.

| Year | Contributions | Rollovers in | Roth conversions out | Withdrawals | Year-end assets | Withdrawals / prior year-end assets (computed) |
|---|---|---|---|---|---|---|
| 1996 | 14.1 | 114.0 | n/a | n/a | not read | |
| 1997 | 15.0 | 121.5 | n/a | n/a | 1,642e | |
| 1998 | 11.9 | 160.0 | 39.3 | n/a | 1,974 | |
| 1999 | 10.3 | 199.9 | 3.7 | n/a | 2,423 | |
| 2000 | 10.0 | 225.6 | 3.2 | 96.8 | 2,407 | 4.00% |
| 2001 | 9.2 | 187.8 | 3.1 | 105.8 | 2,395 | 4.40% |
| 2002 | 12.4 | 204.4 | 3.3 | 116.7 | 2,322 | 4.87% |
| 2003 | 12.3e | 205.0e | 3.0 | 103.4e | 2,719e | 4.45% |
| 2004 | 12.6 | 214.9 | 2.8 | 133.0 | 2,957 | 4.89% |
| 2005 | 13.4 | 228.5 | 2.6 | 119.3 | 3,034 | 4.03% |
| 2006 | 14.3 | 282.0 | 2.8 | 136.8 | 3,722 | 4.51% |
| 2007 | 14.4 | 316.6 | 2.2 | 159.0 | 4,187 | 4.27% |
| 2008 | 13.4 | 272.1 | 3.7 | 212.3 | 3,257 | 5.07% |
| 2009 | 12.8 | 257.3 | 6.8 | 165.2 | 3,941 | 5.07% |
| 2010 | 12.8 | 288.4 | 64.8 | 243.3 | 4,340 | 6.17% |
| 2011 | 12.3 | 297.5 | 11.3 | 189.6 | 4,459 | 4.37% |
| 2012 | 15.5 | 334.6 | 18.1 | 237.2 | 4,969 | 5.32% |
| 2013 | 16.8 | 393.4 | 7.5 | 243.7 | 5,828 | 4.90% |
| 2014 | 17.5 | 423.9 | 8.3 | 257.7 | 6,225 | 4.42% |
| 2015 | 17.7 | 459.9 | 9.0 | 276.9 | 6,387 | 4.45% |
| 2016 | 18.3 | 430.8 | 9.1 | 272.6 | 6,824 | 4.27% |
| 2017 | 18.8 | 463.0 | 10.0 | 303.4 | 8,018 | 4.45% |
| 2018 | 18.6 | 516.7 | 13.7 | 341.1 | 7,745 | 4.25% |
| 2019 | n/a | n/a | n/a | n/a | 9,165e | |
| 2020 | 22.1 | 594.8 | 34.5 (into Roth IRAs) | not retrieved | 10,290e (ICI 2021 report) / 10,722 (CRS, later ICI vintage) | |

### E. IRA withdrawals by age, tax year 2010, all IRA types (IRS SOI Table 4)

Source: https://www.irs.gov/pub/irs-soi/13inirafallbul.pdf. Last three columns computed.

| Age | Taxpayers with IRAs | Taxpayers with withdrawals | Withdrawals ($K) | Year-end FMV ($K) | Incidence (computed) | Withdrawals / FMV (computed) | Average withdrawal (computed) |
|---|---|---|---|---|---|---|---|
| 60 under 65 | 6,664,113 | 1,429,492 | 43,292,551 | 949,927,965 | 21.5% | 4.56% | $30,285 |
| 65 under 70 | 5,022,545 | 1,347,126 | 41,021,477 | 877,341,166 | 26.8% | 4.68% | $30,451 |
| 70 under 75 | 3,563,566 | 2,705,865 | 43,716,677 | 627,955,155 | 75.9% | 6.96% | $16,156 |
| 75 under 80 | 2,530,225 | 2,209,310 | 29,937,344 | 408,213,641 | 87.3% | 7.33% | $13,551 |
| 80 and over | 2,765,906 | 2,539,610 | 30,082,310 | 307,803,175 | 91.8% | 9.77% | $11,845 |
| All taxpayers | 54,428,897 | 13,459,025 | 257,611,337 | 5,029,473,427 | 24.7% | 5.12% | $19,140 |

### F. Withdrawal incidence around the age thresholds (tax and recordkeeper microdata)

| Label | Unit | Year / category | Value | Source URL |
|---|---|---|---|---|
| Traditional IRA holders with withdrawal, age 58½ | % | 2005 | 10.4 | https://www.aeaweb.org/conference/2022/preliminary/paper/7e3b6nQN |
| same, age 59½ | % | 2005 | 20.4 | same |
| same, age 69½ | % | 2005 | 32.4 | same |
| same, age 70½ | % | 2005 | 87.3 | same |
| IRA holders with distribution, age 60 | % | 2008 to 2010 data (JCT study) | about 20 | https://www.asppa-net.org/news/2019/2/rmds-driven-income-level-jct-study-finds |
| same, age 70 | % | same | about 35 | same |
| IRA holders under 70½ (60 to 70) with distribution | % | 2000 to 2013 | about 25 | https://conference.nber.org/conf_papers/f85635/f85635.pdf |
| IRA holders aged 70½ with distribution | % | 2008 and 2010 | over 90 | same |
| IRA holders aged 70½ with distribution | % | 2009 (waiver) | 60 | same |
| Average distribution, 70½-year-olds | % of balance | 2008 and 2010 | 10.9 | same |
| Average distribution, 70½-year-olds | % of balance | 2009 | 8.2 | same |
| Average distribution, all subject to RMD | % of balance | normal years | 13.1 | same |
| Average distribution, all subject to RMD | % of balance | 2009 | 10.4 | same |
| IRA owners ($10,000+) with distribution, age 69 | % | 2019 | 30 | https://www.asppa-net.org/news/2025/3/rmds-a-default-withdrawal-strategy-regardless-of-secure-2.0-study-says |
| same, age 71 | % | 2019 (RMD age 70½) | 85.3 | same |
| same, age 71 | % | 2021 (RMD age 72) | 31.7 | same |
| same, age 72 | % | 2021 | 82.4 | same |

### G. Response to the two RMD waivers

| Label | Unit | Year | Value | Source URL |
|---|---|---|---|---|
| Traditional IRA owners 70½+ who did not withdraw | million of 8.1 million | 2009 | 3.2 (39.5% computed) | https://www.irs.gov/pub/irs-soi/13inirafallbul.pdf |
| Traditional IRA owners 70½ to under 75 not withdrawing | % | 2009 | 46 | same |
| "Suspenders" among those subject to RMD who withdrew in 2008 (tax data) | % | 2009 | 35 | https://conference.nber.org/conf_papers/f85635/f85635.pdf |
| TIAA participants with 2008 minimum distribution who suspended | % | 2009 | 35.5 | https://www.nber.org/system/files/working_papers/w20464/w20464.pdf |
| TIAA suspension, ages 70 to 74 | % | 2009 | about 40 | same |
| TIAA suspension, over 90 | % | 2009 | 23 | same |
| Withdrew within 0.5 point of the suspended RMD | % | 2009 | about 20 | https://conference.nber.org/conf_papers/f85635/f85635.pdf |
| RMD-constrained who did not respond to suspension | % | 2009 | up to 38 | https://ideas.repec.org/a/ntj/journl/v72y2019i3p507-542.html |
| Would prefer to withdraw less than RMD | % | 2000 to 2013 | around 50 (published); at least 41 (2016 WP); 52 (JCT version) | same; https://conference.nber.org/conf_papers/f85635/f85635.pdf; https://www.asppa-net.org/news/2019/2/rmds-driven-income-level-jct-study-finds |
| Returns with taxable IRA distributions, change | % | 2008 to 2009 | −14.2 (computed) | Table A above |
| Taxable IRA distributions, change | % | 2008 to 2009 | −16.6 (computed) | Table A above |
| Returns with taxable IRA distributions, change | % | 2019 to 2020 | −16.2 (computed) | Table A above |
| Taxable IRA distributions, change | % | 2019 to 2020 | −12.6 (computed) | Table A above |
| Traditional IRA investors with withdrawal (ICI database) | % | 2019 / 2020 | 25.1 / 20.3 | https://www.ici.org/files/2024/24-rpt-ira-traditional.pdf |
| Traditional IRA investors 70+ with withdrawal (ICI database) | % | 2020 | 59.6 | same |
| Households 70+ with traditional IRA withdrawal (ICI survey) | % | TY2019 / TY2020 | 81 / 60 | https://workplace.vanguard.com/content/dam/inst/iig-transformation/insights/pdf/2023/Retirement-distribution-decisions-among-dc-participants.pdf ; https://www.ici.org/files/2022/per28-01.pdf |

### H. ICI household survey: traditional IRA-owning households taking a withdrawal, by tax year

Tax year = survey year minus one (figure labels are survey years). Values for tax years 2006 to 2018 are reconstructed from two automated reads of ICI's bar chart (17 bars for survey years 2007 to 2023); anchors confirmed in ICI text are tax years 2007 (20), 2008 (19), 2009 (15), 2019 (27), 2020 (23), 2021 (29), 2022 (31), 2023 (31), 2024 (33). Survey mode changed in 2016. Sources: https://www.ici.org/files/2022/per28-01.pdf ; https://www.ici.org/files/2024/per30-01.pdf ; https://www.ici.org/pdf/fm-v19n8.pdf ; https://www.ici.org/system/files/2026-06/per32-07.pdf

| Tax year | % with withdrawal |
|---|---|
| 2006 | 18 |
| 2007 | 20 |
| 2008 | 19 |
| 2009 (waiver) | 15 |
| 2010 | 22 |
| 2011 | 21 |
| 2012 | 21 |
| 2013 | 20 |
| 2014 | 22 |
| 2015 | 25 |
| 2016 | 26 |
| 2017 | 26 |
| 2018 | 25 |
| 2019 | 27 |
| 2020 (waiver) | 23 |
| 2021 | 29 |
| 2022 | 31 |
| 2023 | 31 |
| 2024 | 33 |

By age of household head: TY2019: 59 to 69: 22%; 70+: 81%. TY2020: under 59: 7%; 70+: 60%. TY2022: under 59: 5%; 59 to 69: 25%; 70+: 75%. TY2024: under 59: 8%; 59 to 72: 30%; 73+: 84%.

Share of withdrawing households that sized the withdrawal by the RMD: TY2008: 64%; TY2009: 48%; TY2019: 76%; TY2020: 61%; TY2022: 76%; TY2024: 70%.

### I. Share taking only (or no more than) the RMD, by study

| Label | Unit | Data year | Value | Source URL |
|---|---|---|---|---|
| Distributions within 1 point of RMD (tax data) | % of those subject | 2008 | 65 | https://conference.nber.org/conf_papers/f85635/f85635.pdf |
| Took only the RMD (J.P. Morgan / EBRI) | % of those subject | 2013 to 2018 | about 84 | https://www.ebri.org/content/new-combined-dataset-reveals-unique-insights-into-income-and-spending-in-retirement |
| No withdrawals before RMD age (J.P. Morgan / EBRI) | % | 2013 to 2018 | about 80 | same |
| Traditional owners 71+ withdrawing more than RMD (EBRI IRA Database) | % | 2015 | slightly more than 25 | https://www.ebri.org/retirement/content/overall-withdrawal-levels-from-iras-are-driven-by-the-minimum-distribution-rules |
| Households 71+ withdrawing no more than RMD (HRS) | % | 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016 | 68, 67, 61, 67, 63, 64, 68, 65 | https://www.ebri.org/retirement/content/ira-withdrawal-patterns-in-times-of-crisis-ig |
| IRA withdrawers taking only the minimum (HRS) | % | 1998 to 2014 | as much as 82 | https://www.dol.gov/sites/dolgov/files/ebsa/pdf_files/innovations-and-trends-in-annuities.pdf |
| Withdrawers 70+ taking exactly the ULT RMD (ICI database) | % | 2020 (waiver year) | 43.6 (35.7 more; 17.9 less) | https://www.ici.org/files/2024/24-rpt-ira-traditional.pdf |
| Vanguard RMD-age IRA clients: none / below RMD / at or above | % | 2024 | 6.7 / 24 / 69 | https://corporate.vanguard.com/content/corporatesite/us/en/corp/articles/how-costly-are-missed-rmds.html |

### J. Uniform Lifetime Table: divisor and implied RMD percentage

Divisors: old table from https://www.stwserve.com/life-expectant-factors-for-rmds/ (72 to 85) and https://www.irs.gov/pub/irs-prior/p590b--2019.pdf (70, 71, 90, 95, 100); current table from https://www.law.cornell.edu/cfr/text/26/1.401(a)(9)-9. Percentages computed as 100 / divisor.

| Age | Old divisor (2003 to 2021) | Old RMD % (computed) | Current divisor (2022 on) | Current RMD % (computed) | Reduction in required % (computed) |
|---|---|---|---|---|---|
| 70 | 27.4 | 3.65 | n/a | n/a | n/a |
| 71 | 26.5 | 3.77 | n/a | n/a | n/a |
| 72 | 25.6 | 3.91 | 27.4 | 3.65 | 6.6% |
| 73 | 24.7 | 4.05 | 26.5 | 3.77 | 6.8% |
| 75 | 22.9 | 4.37 | 24.6 | 4.07 | 6.9% |
| 80 | 18.7 | 5.35 | 20.2 | 4.95 | 7.4% |
| 85 | 14.8 | 6.76 | 16.0 | 6.25 | 7.5% |
| 90 | 11.4 | 8.77 | 12.2 | 8.20 | 6.6% |
| 95 | 8.6 | 11.63 | 8.9 | 11.24 | 3.4% |
| 100 | 6.3 | 15.87 | 6.4 | 15.63 | 1.6% |

### K. RMD starting age by date of birth

Source: https://www.everycrsreport.com/reports/IF12750.html

| Date of birth | RMD age |
|---|---|
| Before July 1, 1949 | 70½ |
| July 1, 1949 to Dec 31, 1950 | 72 |
| Jan 1, 1951 to Dec 31, 1958 | 73 |
| 1959 | 73 under proposed regulations (statute ambiguous) |
| Jan 1, 1960 or later | 75 |

### L. Indexed limits

| Label | Unit | Year | Value | Source URL |
|---|---|---|---|---|
| QCD annual limit | $ | 2006 to 2023 | 100,000 | https://www.everycrsreport.com/files/2026-01-15_IF11377_059b9cc6503b7b2bd5d08658b8e2a80ac2eb5d58.pdf |
| QCD annual limit | $ | 2024 | 105,000 | https://www.irs.gov/pub/irs-drop/n-24-80.pdf |
| QCD annual limit | $ | 2025 | 108,000 | same |
| QCD annual limit | $ | 2026 | 111,000 | https://www.irs.gov/pub/irs-drop/n-25-67.pdf |
| One-time split-interest QCD | $ | 2024 / 2025 / 2026 | 53,000 / 54,000 / 55,000 | both notices |
| QLAC premium limit | $ | 2014 regulations | lesser of 125,000 or 25% of balance | https://www.dol.gov/sites/dolgov/files/ebsa/pdf_files/innovations-and-trends-in-annuities.pdf |
| QLAC premium limit | $ | 2023 to 2024 | 200,000 | https://www.irs.gov/pub/irs-drop/n-24-80.pdf |
| QLAC premium limit | $ | 2025 and 2026 | 210,000 | https://www.irs.gov/pub/irs-drop/n-25-67.pdf |
| RMD excise tax | % of shortfall | through 2022 / from 2023 | 50 / 25 (10 if corrected) | https://www.everycrsreport.com/reports/IF12750.html |
| Long-term-care distribution limit | $ | 2026 | 2,600 | https://www.irs.gov/pub/irs-drop/n-25-67.pdf |

### M. Roth versus traditional IRA withdrawal incidence (ICI IRA Investor Database)

| Age group | Year | Roth % | Traditional % | Source URL |
|---|---|---|---|---|
| 18 to 59 | 2020 | 2.5 | 6.0 | https://ici.org/system/files/2024-07/24-rpt-ira-roth.pdf |
| 60 to 69 | 2020 | 6.0 | 18.7 | same |
| 70 or older | 2020 | 6.1 | 59.6 | same |
| All 18+ | 2020 | 3.4 | 20.3 | same |
| 18 to 59 | 2018 | 3.1 | not read | https://ici.org/files/2024/ten-facts-roth-iras.pdf |
| 60 to 69 | 2018 | 6.9 | not read | same |
| 70 or older | 2018 | 6.8 | not read | same |
| All | 2018 | 4.1 | 24.9 | same |
| Households (survey) | TY2024 | 6 | 33 | https://www.ici.org/system/files/2026-06/per32-07.pdf |

### N. Roth share of new money

| Label | Unit | Year | Value | Source URL |
|---|---|---|---|---|
| Roth IRA contributions | $B | 2020 | 33.0 | https://www.everycrsreport.com/files/2025-03-18_R48456_2da886a77ca615d09c68c1f445f261674c65ce7c.html |
| Traditional IRA contributions | $B | 2020 | 22.1 | same |
| Roth share of contribution dollars | % | 2020 | 59.9 (computed) | same |
| Roth IRA contributors | taxpayers | TY2022 | 10,036,960 (avg $3,482) | https://www.everycrsreport.com/files/2025-12-03_R48051_33c649736244ce72e13114e7b4f95fef86ca6107.html |
| Traditional IRA contributors | taxpayers | TY2022 | 4,989,322 (avg $4,510) | same |
| Roth share of contribution dollars | % | TY2022 | 60.8 (computed: $34.95B vs $22.50B) | same |
| Roth conversions | $B | 2020 | 34.5 | CRS R48456 |
| Roth conversions | $B; taxpayers | TY2023 | 36.65; 1,597,798 | https://rothirahub.com/tools/statistics/ (secondary) |
| Roth contributions | $B; taxpayers | TY2023 | 32.81; 9,488,414 | same (secondary) |
| Vanguard plans offering Roth | % of plans | 2019 / 2025 | 77 / 98 | https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf |
| Participants using Roth when offered | % | 2019 / 2025 | 12 / 18 | same |

### O. Annuitization

| Label | Unit | Year | Value | Source URL |
|---|---|---|---|---|
| TIAA first-time income-takers choosing a life annuity | % | 2000 / 2018 | 61 / 18 | https://www.nber.org/papers/w29946 |
| TIAA first-time income-takers, RMD-only | % | 2000 / 2007 / 2017 / 2018 | 10 / 28 / 54 / 52 | https://www.tiaa.org/content/dam/tiaa/institute/pdf/research-report/2021-09/tiaa-institute-trends-in-retirement-and-retirement-income-choices-by-tiaa-participants-2000-to-2018-rd-182-brown-september-2021.pdf |
| TIAA all income recipients with any life annuity | % | 2008 / 2018 | 52 / 31 | https://www.nber.org/papers/w29946 |
| TIAA average age at first income draw | years | 2000 / 2018 | 65.5 / 69.8 | TIAA Institute RD 182 (URL above) |
| DC retirees who annuitized (HRS) | % | 2000 to 2006 | 6.1 | https://www.gao.gov/assets/a319390.html |
| DC retirees: left in plan / rolled over / withdrew | % | 2000 to 2006 | 38.8 / 30.3 / 15.8 | same |
| Record keepers' plans not offering an annuity | share | end 2014 | about three-quarters | https://www.gao.gov/products/gao-16-433 |
| US annuity sales, total | $B | 2025 | 461.3 | https://www.insurancebusinessmag.com/us/news/breaking-news/us-annuity-sales-hit-record-461-billion-as-indexed-products-surge--limra-565533.aspx |
| Single premium immediate annuity sales | $B | 2025 | 14.0 | same |
| Deferred income annuity sales | $B | 2025 | 4.8 | same |
| Income annuities share of total sales | % | 2025 | 4.1 (computed: 18.8 / 461.3) | same |
| Deferred income annuity sales (2015 dollars) | $B | 2012 / 2013 / 2014 / 2015 | 1.0 / 2.2 / 2.7 / 2.7 | https://www.dol.gov/sites/dolgov/files/ebsa/pdf_files/innovations-and-trends-in-annuities.pdf |

### P. What retirement-age DC participants do at separation (Vanguard, 2011 termination cohort observed at year-end 2021)

Source: https://workplace.vanguard.com/content/dam/inst/iig-transformation/insights/pdf/2023/Retirement-distribution-decisions-among-dc-participants.pdf

| Outcome | % of participants | % of assets | Average balance |
|---|---|---|---|
| Remain in plan, no installments | 3 | 8 | $418,900 |
| Remain in plan, installments (partial withdrawals) | 4 | 8 | $347,200 |
| Rollover to IRA | 57 | 66 | $239,300 |
| Combination | 8 | 13 | $289,700 |
| Cash-out (full) | 28 | 5 | $39,700 |

Share still in plan by termination cohort (participants / assets): 2011: 7% / 16%; 2015: 14% / 27%; 2020: 32% / 46%.

### Q. Asset retention after about 18 years of retirement (HRS-based)

| Starting non-housing assets | Share retained (BlackRock / EBRI) | Share spent at median (EBRI) | Source URL |
|---|---|---|---|
| Under $200,000 | 80% | about one-quarter | https://www.planadviser.com/retirees-still-80-savings-nearly-two-decades/ ; https://www.ebri.org/content/asset-decumulation-or-asset-preservation-what-guides-retirement-spending |
| $200,000 to $500,000 | 77% | 27.2% | same |
| $500,000 or more | 83% | 11.8% | same |

---

## Gaps and caveats

Access limits
- Direct downloads were blocked by network policy and the web search budget was exhausted partway through, so several named sources were not reached: IRS SOI IRA spreadsheets (all years after the 2010 Bulletin article), ICI data workbooks, the J.P. Morgan "Mystery No More" PDF, the EBRI issue briefs behind the press summaries, the BlackRock white paper, Vanguard's "How America Retires" PDF, LIMRA qualified-money and QLAC statistics, Fidelity and JPMorgan Chase data, Morningstar and T. Rowe Price primary reports, the JCT staff paper on RMDs, and congress.gov pages for ERISA, the Small Business Job Protection Act and the CARES Act.
- Every figure was read by an automated extractor. In this session the extractor demonstrably garbled multi-column tables several times (Uniform Lifetime Table in IRS Publication 590-B; Publication 4801 for tax year 2023; ICI bar-chart labels; the 2008 SOI age table). Figures confirmed by a second read or a second source are: SOI Table A 2015 to 2022; FRED 1999 to 2016 (matches Table A for 2015 and 2016); Publication 4801 taxable amounts for 2019 to 2021 (match Table A); SOI 2010 age table; ICI Figure 1.2 for 2000 to 2018; current Uniform Lifetime Table; old table ages 72 to 85. Treat everything marked "single read" as needing a spot check before publication.

Series breaks and definitions
- Form 1040 "taxable IRA distributions" include taxable Roth conversions and exclude rollovers, non-taxable basis and qualified charitable distributions. Conversion-heavy years (1998, 2010 to 2012, 2020 onward) lift the series for reasons unrelated to retiree spending. Income from 2010 conversions could be spread into 2011 and 2012 under the rules then in force (this deferral rule is from background knowledge, not a fetched source).
- "Taxable pensions and annuities" mixes DB pension payments, DC plan distributions, and commercial annuities; it cannot be split into DC versus DB from the Form 1040 line. Gross line 5a includes direct rollovers.
- Tax year 2018 has no separate IRA and pension lines. 1998 is preliminary. 1988 to 1996 come from a secondary table in Sabelhaus (2000).
- SOI IRA-study "withdrawals" (Form 1099-R based) exclude trustee-to-trustee rollovers; whether they include Roth conversions is not clear from the footnote, and the 2010 spike suggests they do.
- ICI total-asset figures differ by vintage (2020 traditional IRA assets: 10,290e in the 2021 report versus 10,722 in CRS's later citation).
- ICI household survey switched from telephone to online panel in 2016; its figure is labelled by survey year, not tax year.
- Person-level average withdrawal rates (Mortenson et al.: 12% to 15%) and dollar-weighted rates (SOI: 5% to 10%) measure different things.
- EBRI's IRA Database, ICI's IRA Investor Database, TIAA and Vanguard are recordkeeper samples, not national; owners may hold accounts elsewhere, which biases "took no RMD" upward at any single provider.

Conflicts between sources
- Share who would withdraw less than the RMD: at least 41% (2016 working paper), 52% (JCT version in trade press), around 50% (published 2019 abstract).
- TIAA life-annuity share in 2000: 61% (2021 and 2022 abstracts), 54% (2019 version through 2017), 52% (one read of report text).
- Derby et al.: the under-59½ increase is given as $60 billion in one sentence and $65 billion in another.
- TIGTA: 639,000 potentially noncompliant versus 121,419 projected noncompliant with a 28% sample error rate; the arithmetic does not reconcile from the extract.
- Publication 4801 tax year 2023: alternative amounts on page 9 (see Section 3 Gaps).
- Origin of RMD rules: 1962 Keogh plans (Brown, Poterba & Richardson) versus Tax Reform Act of 1986 for IRAs (Stuart & Bryant).

Not found
- Form 1099-R national totals by distribution code for any year.
- Annual count of taxpayers subject to RMDs and total RMD dollars.
- Tax-data evaluation of the age-73 change (2023) or the 2022 table change.
- QLAC sales and take-up after 2015; qualified-money share of annuity sales.
- Dollar-weighted withdrawal rates by single year of age after 2010.
- Roth IRA withdrawals by age in tax data.
- Treasury Office of Tax Analysis working papers on retirement distributions (none surfaced before the search budget ran out).
- CBO projections of retirement distributions later than the January 2016 Outlook; the January 2025 Outlook landing page has no such statement.
