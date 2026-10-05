# Keeping money in DC plans / tax-deferred accounts longer: is it working? Leakage trends and the "stay" provisions

Task `stayinplan`, compiled 2026-10-04. US only. Scope: pre-retirement leakage (cash-outs, hardship, CARES/SECURE 2.0 emergency access), force-out thresholds, auto-portability, RMD-age changes, in-plan income / withdrawal flexibility. Recordkeeper and industry figures are labelled **[recordkeeper/industry]**; simulations are labelled **[simulation]**; my own arithmetic is labelled **Computed** with its inputs.

New files from this task:
- `dc_policy/output/irs_early_distribution_penalty.csv`: IRS SOI, returns paying the "penalty tax on qualified retirement plans" (Schedule 2 line 8), TY1996-2023 (TY1996-2001 added by gapC, 2026-10-05), with % of all returns, the amount, and the amount per $100 of taxable IRA + pension distributions.
- `dc_policy/output/irs_form5329_part1.csv`: Form 5329 Part I (additional tax on early distributions) line-item estimates, TY2003-2023 (lines 3-4 only before TY2009; TY2003-2016 added by gapC).
- `dc_policy/raw/stayinplan/`: the 28 SOI Table 3.3 spreadsheets (TY1996-2023) and `build_penalty_series.py`, which rebuilds both CSVs.

---

## 0. Already covered by earlier project work (not redone)

- **TSP retention after the Sep 2019 withdrawal-flexibility change.** FERS one-year post-separation retention was 57-61% (FY15-16) and 64-65% (FY18-FY20Q3), peaked at 68-73% in FY21-22 and was 67-71% in FY24-26 (latest 69.1%). See `dc_stay/README.md` §1 and `notes/dc_plan_distributions.md` §5.
- **Form 5500 separated participants.** Separated vested participants with money still in private DC plans rose from 15.2% of participants (1999) to 22.2% (2023), with series breaks. See `dc_stay/README.md` §2.
- **SCF past-job accounts.** Among households 60-74 not working that hold an IRA or past-job plan, the share with past-job plan money was 16-19% (2004-07) and 26-29% (2019-22). See `dc_stay/README.md` §3.
- **RMD age 70½ → 72 → 73.** SIPP: at age 72, 64-67 per 100 IRA holders withdrew in 2020-22, then 37 (2023) and 30 (2024). EBRI: 85.3% of 71-year-olds withdrew in 2019, 31.7% in 2021. Mortenson-Schramm-Whitten (2009 waiver), Brown-Poterba-Richardson (TIAA) and Derby et al. (2020 waiver) are also already summarised. See `notes/followups_2026-10-04.md` §1 and `notes/rmd_policy_tax_data.md` §2.
- **Auto-portability adoption.** PSN had 549 completed transactions by 1 Dec 2024 and about 21,000 adopting plans by Sep 2025; Vanguard reports 7% of plans by YE2025. See `notes/rollovers.md` §9.
- **Force-out settings and SECURE 2.0 provisions.** T. Rowe Price: 38% of plans use automatic rollover at $7,000 and 45% at $5,000 (mid-2024). Vanguard: 57% at $7,000. GAO-15-73 on forced-transfer IRAs. See `notes/dc_plan_distributions.md` §4 and §8.
- **Leakage context already in notes:** Goodman et al. 2021 (22% of contributions), Argento-Bryant-Sabelhaus (under-55 gross/taxable/penalised 2004-2010), GAO-19-179 ($69B of early withdrawals in 2013 at ages 25-55), and the ICI recordkeeper hardship series. See `notes/rmd_policy_tax_data.md` §2 and `notes/dc_plan_distributions.md` §2 and §8. They are cited again below only where they anchor a new comparison.

---

## 1. Leakage trend: IRS SOI early-distribution additional tax, 2002-2023 (new series), plus CARES and SECURE 2.0 emergency access

### Takeaway
The share of all individual returns paying the additional tax on early distributions fell from about 4% around the Great Recession (peak 4.18% in 2009) to 3.30% in 2018-19. It then dropped to 2.36% in 2020, when coronavirus-related distributions (CRDs) were exempt, and climbed back to 3.17% by 2023, still below the 2019 level. Relative to the taxable IRA and pension distributions that dominate the system, the penalty tax has fallen almost every year: from $0.78 per $100 in 2002 to $0.55 in 2019 and $0.47 in 2023. Penalised early distributions are therefore a shrinking share of total outflows. In nominal dollars, implied penalised distributions are back at their 2019 peak (about $64B in 2023 vs $60B in 2019). Recordkeeper data show hardship withdrawals rising sharply since 2022, which the penalty series does not yet capture beyond TY2023.

### Cited findings
- **IRS SOI Table 3.3, "Penalty tax on qualified retirement plans", all returns.** Selected years: 4,924,584 returns and $3,640,374K (2004); 5,874,254 and $5,312,413K (2009); 5,203,674 and $6,043,348K (2019); 3,873,810 and $3,642,009K (2020); 4,484,060 and $5,199,727K (2021); 4,788,972 and $5,646,079K (2022); 5,092,999 and $6,380,591K (2023). All returns: 157,796,807 (2019) and 160,602,107 (2023). Full series 2002-2023 in `output/irs_early_distribution_penalty.csv`. — [IRS SOI Table 3.3, TY2023 (Pub 1304, March 2026)](https://www.irs.gov/pub/irs-soi/23in33ar.xls); prior years at `https://www.irs.gov/pub/irs-soi/YYin33ar.xls`. **Correction (gapC, 2026-10-05):** the TY1996-2001 tables do have the column, in a lower "All other taxes" panel of the sheet that the first parser missed. All returns: 3,434,814 returns and $2,189,148K (1996, 2.85% of returns); 3,415,245 and $2,335,845K (1997, [97in33.xls](https://www.irs.gov/pub/irs-soi/97in33.xls)); 3,786,186 and $2,699,419K (1998); 4,076,050 and $3,074,825K (1999); 4,334,527 and $3,414,692K (2000); 4,571,187 and $3,259,975K (2001, 3.51%). — [96in33ar.xls](https://www.irs.gov/pub/irs-soi/96in33ar.xls) to [01in33ar.xls](https://www.irs.gov/pub/irs-soi/01in33ar.xls). TY1996 is the earliest Table 3.3 SOI posts online; Pub 1304 PDFs before TY2019 are not on irs.gov. In the 1990s the line (Form 1040 "Tax on IRAs, other retirement plans, and MSAs") also carried excess-contribution and excess-accumulation taxes, as it does now.
- **What the column is.** It equals Form 1040 Schedule 2 line 8, "Additional tax on IRAs or other tax-favored accounts. Attach Form 5329 if required". The TY2021 count of 4,484,060 returns matches Table 3.3 exactly. — [Pub 4801, TY2021 line-item estimates, PDF p.27](https://www.irs.gov/pub/irs-prior/p4801--2024.pdf). Form 5329 states: "If you only owe the additional 10% tax on the full amount of the early distributions, you may be able to report this tax directly on Schedule 2 (Form 1040), line 8, without filing Form 5329." — [Pub 4801 TY2022, PDF p.131](https://www.irs.gov/pub/irs-prior/p4801--122024.pdf). Other Form 5329 taxes on the line are small. In TY2022, education/ABLE distributions were $64.8M, traditional-IRA excess contributions $21.7M and excess accumulation (missed RMD) $4.2M, against $1,848M of early-distribution tax on Form 5329 itself. — same PDF, pp.131-132. The line also includes the 25% SIMPLE-IRA rate within two years.
- **Form 5329 Part I (early distributions), filers who itemise their exceptions.** Early distributions reported: $26.1B (2019), $27.5B (2020), $25.7B (2021), $28.3B (2022). Excepted from the tax: 37.3%, 66.5%, 35.5%, 35.2% of dollars. Amount subject to tax: $16.4B, $9.2B, $16.5B, $18.3B. Additional tax: $1.66B, $0.93B, $1.66B, $1.85B, which is 25-33% of all Schedule 2 line 8 tax. The rest is reported directly without Form 5329. — [Pub 4801 TY2019, pp.123-124](https://www.irs.gov/pub/irs-prior/p4801--2021.pdf); [TY2020, pp.121-122](https://www.irs.gov/pub/irs-prior/p4801--2022.pdf); [TY2021, pp.143-144](https://www.irs.gov/pub/irs-prior/p4801--2024.pdf); [TY2022, pp.131-132](https://www.irs.gov/pub/irs-prior/p4801--122024.pdf). TY2023 shows $133.0B on line 1 and $110.8B on line 2, about five times every prior year, while line 3 ($22.2B) and line 4 ($2.24B) look normal. — [Pub 4801 TY2023 (Rev. 6-2026), pp.131-132](https://www.irs.gov/pub/irs-pdf/p4801.pdf). **Diagnosis (gapC, 2026-10-05): not a parsing problem, not a units problem, not a definition change; treat as an SOI estimation anomaly and do not use TY2023 lines 1-2.** (a) Re-extracted from the PDF: the printed amounts are exactly $132,957,756K and $110,788,817K, on the page headed "Amounts of selected lines filed (in thousands of dollars)"; line 3 = line 1 minus line 2 to the dollar, and line 4 ($2,238,517K) is 10.1% of line 3, as it should be. (b) The extra ~$105B on line 1 is matched by ~$101B on line 2 (excepted), so it affects only the excepted portion. The average excepted amount per excepting return jumps to **Computed** $146.9K (110,788,817/754,282) from $15.2K in 2022 (9,985,273/658,908), while the number of excepting returns rises only 14%. (c) No aggregate moves with it: Form 1040 gross IRA distributions $497.5B → $505.5B (+1.6%) and gross pensions $1,528.4B → $1,594.9B (+4.4%), 2022 → 2023 (Pub 4801 Form 1040 pages), and Table 3.3 penalty tax +13%. (d) The 2023 Form 5329 instructions add no new exception code relative to 2022 (codes 20 terminal illness and 21 corrective distributions were already in the 2022 instructions; the 2023 reminders list corrective IRA distributions and qualified disaster distributions, both effective Dec 29, 2022) — [i5329 2023](https://www.irs.gov/pub/irs-prior/i5329--2023.pdf), [i5329 2022](https://www.irs.gov/pub/irs-prior/i5329--2022.pdf). (e) Pub 4801 warns that "some less popular items should be used with a high degree of caution" (p.3). The most likely cause is one or a few heavily weighted sample returns with very large excepted amounts (or a capture error on them); SOI has published no errata. Lines 3-4 are unaffected and remain usable. TY2024 (Pub 4801 next edition, `24in33ar.xls`) is not out as of 5 Oct 2026, so the anomaly can't yet be checked against the next year.
- **Form 5329 Part I back to TY2003 (gapC).** Amount subject to the tax (line 3): $11.4B (2004), $10.6B (2005), $11.9B (2006), $13.3B (2007), $13.9B (2008), $14.8B (2009), $16.0B (2010), $15.1-15.9B (2011-2016). Excepted share of line-1 dollars (Computed): 24.1% (2009), 32-36% (2010-2016), 35-40% (2017-2022 excluding 2020). The excepted share has drifted up since 2009, consistent with more exceptions being claimed, not with less leakage. — `output/irs_form5329_part1.csv`, from [p4801--2006 to p4801--2017](https://www.irs.gov/prior-year-forms-and-instructions?find=4801) and [16inlinecount.pdf](https://www.irs.gov/pub/irs-soi/16inlinecount.pdf); TY2003-2008 publish lines 3-4 only.
- **TIGTA, TY2021: the penalty series undercounts early withdrawals.** "Approximately 6.2 million taxpayers who had one or more associated Forms 1099-R indicating that the taxpayers took an early distribution that could be subject to the 10 percent additional tax" (codes 1, J, L, M, 5); "Approximately 1 million of these taxpayers had attached Forms 5329" and "Approximately 3.1 million of the 5.2 million taxpayers did not self-report the 10 percent additional tax"; 2.8 million (after removing likely rollovers) had "a total taxable amount of approximately $12.9 billion", potentially $1.29B of unpaid additional tax. **Computed:** 3.1M/6.2M = 50% of taxpayers with a code-1-type early distribution neither paid the tax nor claimed an exception; the $1.29B is about 25% of the $5.20B the SOI series shows paid for TY2021. — [TIGTA 2024-100-065, 30 Sep 2024, pp.2-4](https://www.oversight.gov/sites/default/files/documents/reports/2024-10/2024100065fr.pdf) (tigta.gov copy 404s; copy saved in `raw/gapC/`).
- **Argento, Bryant & Sabelhaus (SOI 1099-R/5498 cross-sections), under age 55: penalised distributions** were $29.7B (2004) and $47.3B (2010); "for every dollar contributed, roughly 40 cents flowed back out" (2010). — [Argento et al., Contemporary Economic Policy 2015](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/argento%20et%20al%20coep%202015.pdf) (already in notes; used here as a cross-check).
- **Goodman, Mortenson, Mackie & Schramm (IRS panel, more than 140M person-years, 2003-2015):** distributions to people 50 or younger "were equal to 22 percent of the contributions made by this age group"; job separation raises the probability of leakage "by more than 200 percent". — [NTJ 74(3), 2021](https://www.journals.uchicago.edu/doi/10.1086/715819). In the JCT version, net contributions of under-50s "dipped in 2009-2010 relative to the pre-Great Recession trend and did not regain their 2007 inflation-adjusted level until 2014. Total net distributions, on the other hand, remained relatively on-trend", so the leakage ratio "increased following the Great Recession". JCT also concludes that "rules related to forced distributions and portability of plans likely affect leakage". — [JCX-20-21, pp.7-9 and 15](https://www.jct.gov/getattachment/ed1c9da4-f180-41cd-b3f9-b8afb9531d18/x-20-21.pdf). The year-by-year leakage ratio is printed only as a chart (Fig. 3) and is not extractable.
- **Munnell & Webb (CRR):** "About 1.5 percent of assets leak out of the 401(k)/IRA system each year"; "Aggregate 401(k) and IRA retirement wealth is at least 20 percent lower than it would have been without current leakage rules"; "In-service withdrawals and cashouts appear to represent the most significant source of leakages, while loans created a measurable but relatively small leakage." — [CRR WP 2015-2, 3 Feb 2015](https://crr.bc.edu/the-impact-of-leakages-from-401ks-and-iras/)
- **GAO-09-715 (Aug 2009):** leakage incidence and amounts "have remained relatively steady"; "Approximately 15 percent of participants initiated some form of leakage" (Census SIPP, 1998, 2003, 2006). The 2006 graphic shows cash-outs at job change of $74B, hardship withdrawals of $9B and loan defaults of $561M, against $2.7T in 401(k) assets. — [GAO-09-715 Highlights](https://gao.gov/assets/gao-09-715-highlights.pdf). **Computed:** (74 + 9 + 0.561) / 2,700 = 3.1% of 401(k) assets in 2006. That is not comparable with Munnell-Webb's 1.5%, which nets out rolled-over money and includes IRAs.
- **CARES Act CRDs (2020), uptake [recordkeeper/industry, compiled by CRS]:** Fidelity "6.3% of eligible participants took CRDs in 2020" (25.8M participants); Empower 4.4%; Vanguard 5.7% (median CRD $6,500, average $15,700); Ascensus 4.9%; ICI (30M+ participants) "5.8% of DC plan participants took CRDs". TSP (government): 119,720 participants took CRDs, 2.8% of active participants; CARES loans 0.4%. — [CRS R46837, Myers, 13 Jul 2021](https://www.everycrsreport.com/reports/R46837.html)
- **CARES in IRS data:** Derby, Goodman, Mackie & Mortenson (JCT, 5% IRS sample) find total under-59½ withdrawals rose about $60B (25%) in 2020 while penalised distributions fell nearly 50% (already in `notes/rmd_policy_tax_data.md`). — [arXiv 2204.12359](https://arxiv.org/pdf/2204.12359v1). The new SOI series is consistent with that: **Computed** 2019→2020, returns paying the tax -25.6% (5,203,674 → 3,873,810); tax dollars -39.7% ($6.04B → $3.64B); Form 5329 amount subject to tax -43.8% ($16.38B → $9.21B). The excepted share of Form 5329 early distributions jumped from 37% to 67%.
- **SECURE 2.0 emergency-expense withdrawal ($1,000/yr, from 2024) [recordkeeper/industry]:** "Only 4% of plans offered emergency expense withdrawals" in 2025 and "just 0.4% of participants initiated one"; self-certification of hardship: "Only 3% of plans offering the provision"; qualified disaster recovery distributions: 16% of plans and 0.2% of participants; domestic abuse withdrawals: 6% of plans and 0.1% of participants. — [Vanguard, "Which optional provisions of SECURE 2.0 are taking hold?", 10 Feb 2026](https://workplace.vanguard.com/insights-and-research/perspective/which-optional-provisions-of-secure-2-0-are-taking-hold.html). PSCA's 68th survey (plan year 2024) reportedly shows 36% of plans adopting the emergency withdrawal (29.3% in plan year 2023, per the earlier notes). The 36% comes from a search-engine summary because psca.org returned 403; **unverified**.
- **Hardship withdrawals and loans, TSP (government administrative data, FERS participants; added by gapC).** Hardship withdrawal usage: 3.3% (2015), 3.2% (2016), 3.5% (2017), 3.3% (2018), 3.7% (2019), 2.9% (2020), 4.0% (2021), 2.1% (2022), 3.1% (2023), 3.8% (2024), 4.9% (2025). Loan usage ("Includes CARES Loans"): 8.5%, 8.7%, 8.8%, 8.5%, 8.6%, 7.1%, 7.0%, 6.6%, 8.3%, 8.5%, 9.5%. FRTIB: "Hardship withdrawals increased from 2024 to 2025, with 4.9% of participants taking withdrawals in 2025"; the 2019 rise is "partly due to the lapse in appropriations" (Dec 2018-Jan 2019); 2021 hardship use "returned to slightly higher levels than those seen before the pandemic". FRTIB gives no reason for the 2022 dip (2.1%); one possibility (not stated by FRTIB) is that the Sept 2019 TSP Modernization Act's multiple age-based in-service withdrawals after 59½ substitute for hardship withdrawals. — [FRTIB Participant Behavior and Demographics 2015-2019, Fig. 9](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2015-2019.pdf); [2017-2021, Fig. 9](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2017-2021.pdf); [2019-2023, Fig. 9](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2019-2023.pdf); [TSP Annual Report 2025, participant behavior 2021-2025, Fig. 9](https://www.frtib.gov/pdf/reading-room/congress/annual/TSP-Annual-Report_2025.pdf). Later reports revise earlier years slightly (2019 hardship 3.8% in the 2015-19 report vs 3.7% later; 2024 shown as 3.8% in the summary table and 3.9% in the chart; loans 2024 8.5%/8.6%); the latest report's value is used. Earlier reports (2010-2016) show hardship and loans only by age and pay, not in total. TSP hardship withdrawals are limited to employee contributions and carry the 10% tax under 59½. This is the only non-recordkeeper annual hardship series found; it rises to a record 4.9% in 2025, matching the direction of Vanguard's series.
- **Hardship withdrawals since the 2018 BBA easing [recordkeeper/industry]:** "Of participants permitted to take hardship withdrawals, 6% initiated at least one in 2025, up from 5% in 2024". Figure 2 reads 2% (2020), 2% (2021), 3% (2022), 4% (2023), 5% (2024), 6% (2025). 95% of plans offer hardship withdrawals. Initiation rates by administrative process in 2025: 2.5% where documentation is required (10% of plans), 6.4% with a summary offer (87%), 8.5% with self-certification (3%). Participants in auto-enrollment plans "were about 30% more likely to initiate" one. "By the second half of 2021, hardship withdrawal activity reverted to prepandemic levels and has continued to increase." — [Vanguard, "How America withstands financial hardships", 2026, pp.2-6](https://workplace.vanguard.com/content/dam/inst/iig-transformation/insights/pdf/2026/how-america-withstands-financial-hardships.pdf)
- **Small-balance cash-out rates at separation (DOL's RIA, 2024), [recordkeeper/industry] inputs:** for balances of $1,000-$4,999, Vanguard 2023: 34% cash out, 51% remain, 15% roll over; Alight 2023: 39% / 28% / 33%. DOL's weighted baseline is 36% cash-out. DOL also cites Wang, Zhai & Lynch (2023): "over 40 percent of separating employees report cashing out at least some of their retirement account balance". — [DOL NPRM, 89 FR 5624, 29 Jan 2024, Table 2](https://www.govinfo.gov/content/pkg/FR-2024-01-29/html/2024-01208.htm)

### Evidence verdict
- **Penalised early withdrawals are not rising relative to the system.** The evidence is moderate (administrative and comprehensive, but descriptive). As a share of returns the series is flat to falling (3.7-4.2% in 2002-2011, 3.3% in 2017-19, 3.2% in 2023). Per $100 of taxable IRA and pension distributions it fell by about 40% from 2002 to 2023. CARES produced a one-year shift into penalty-free CRDs and not a lasting change.
- **The 10% tax and its exceptions matter at the margin.** The evidence is strong. The 2020 suspension of the tax for CRDs cut penalised amounts by about 40-50% (SOI and IRS-panel evidence agree), while total under-59½ withdrawals rose about 25%. Loosening penalties raises leakage.
- **SECURE 2.0 emergency withdrawals have almost no uptake so far** (0.4% of participants in the 4% of Vanguard plans that offer them; weak evidence, one recordkeeper). The **2018 BBA hardship easing coincides with a tripling of hardship use at Vanguard (2% → 6%)**. Moderate evidence on direction, causal weight unclear, since inflation, the end of pandemic support and the spread of auto-enrollment all overlap.

### Gaps
- No IRS series of early distributions by account type (DC vs IRA) or by age after 2010. SOI Table 3.3 mixes IRAs and plans and counts returns, not people.
- **Form 8915-E (CRDs) has no IRS/SOI tabulation (re-checked by gapC, 2026-10-05).** Pub 4801 TY2020 and TY2021 have no Form 8915-E pages (only Form 8606's qualified-disaster lines, which cover nondeductible-IRA filers only: line 15b $872.8M and line 25b $544.2M in TY2020, [p4801--2022 pp.155-158](https://www.irs.gov/pub/irs-prior/p4801--2022.pdf)); Pub 1304 TY2020/2021 tables do not break out CRDs; the SOI CARES Act page covers only Economic Impact Payments ([SOI CARES Act statistics](https://www.irs.gov/statistics/soi-tax-stats-coronavirus-aid-relief-and-economic-security-act-cares-act-statistics)). TIGTA 2021-16-044 (now read via [oversight.gov](https://www.oversight.gov/sites/default/files/oig-reports/TIGTA/202116044fr.pdf)) has no IRS count either; it relies on Fidelity (6.3%, ~1.6M participants), Vanguard (5.7%) and TSP (119,720 participants, $2.9B) and says "millions of taxpayers took coronavirus-related distributions in Tax Year 2020". The best tax-data estimate remains Derby et al. (JCT): under-59½ withdrawals +$60B (+25%) in 2020 with penalised amounts down ~50%. Its share of IRA/pension distributions cannot be computed from published IRS tables. GAO-24-103577 reportedly says "6 percent took a Coronavirus-Related Distribution" with an average of $18,344, but that comes from a single WebFetch extraction; the PDF returned 503, so it is **unverified**.
- TY2024 Table 3.3 (the first year of SECURE 2.0 emergency, domestic-abuse and terminal-illness exceptions) is not released (`24in33ar.xls` returns 404).
- The JCT leakage ratio by year (2003-2015) exists only as a chart.
- Pre-1996 SOI penalty-tax counts are not online. A Tax Policy Center fact sheet (Orszag) reportedly says the share of returns with the penalty tax "rose from 2.3 percent in 1993 to 3.8 percent in 2002" (search-engine snippet only; TPC PDF returned 403) — **unverified**.

---

## 2. Force-out / automatic-rollover thresholds (EGTRRA 2005 $1,000-$5,000; SECURE 2.0 $7,000 in 2024)

### Takeaway
The best causal evidence comes from IRS data on the 2005 automatic-rollover rule (Goodman, Mukherjee & Ramnath). The thresholds clearly bind. About 48% of IRA rollovers just above $1,000, and 29% just below $5,000, happen only because of the default. Those forced-transfer IRAs are passive (47% are touched within ten years, against about 70% of voluntary rollovers), sit in principal-preserving investments (40-47% vs 12-13%), and are far more often abandoned. The default therefore keeps small balances tax-deferred instead of cashed out, but often in a form that loses value and gets forgotten. There is no published before/after evidence yet on cash-out rates after the 2024 increase to $7,000. DOL's own RIA assumes the higher limit adds about 866,000 more accounts a year that can be forced out.

### Cited findings
- **Regression discontinuity at the $1,000 and $5,000 thresholds, using IRS records of IRA rollovers 2005-2010.** Share of compliers (rollovers induced by the default): 0.483 [0.471, 0.493] at $1,000 and 0.294 [0.280, 0.307] at $5,000. Any interaction with the account over the following years: always-takers 0.673 / 0.699, compliers 0.470 / 0.457. Apparently in a principal-preserving investment: always-takers 0.127 / 0.124, compliers 0.474 / 0.402. — [Goodman, Mukherjee & Ramnath, "Set It and Forget It? Financing Retirement in an Age of Defaults", Chicago Fed WP 2022-50, Table 7](https://www.chicagofed.org/-/media/publications/working-papers/2022/wp2022-50-pdf.pdf?sc_lang=en); published in Journal of Financial Economics 148 (2023), pp.47-68.
- **Same paper, abandonment:** failure to claim through age 72.5 is 0.010 / 0.008 for always-takers and 0.061 / 0.075 for compliers (Table 8). Abstract: "certain accounts created by default enrollment are at higher risk of abandonment by passive savers"; "0.4% of retirement-age individuals abandoned an aggregate of $66 million". Those induced into an automatic IRA rollover "are five percentage points more likely to have missed three years of RMDs". Context: "Nearly all employers take up this policy option". — same source, pp.3-4 and Table 8.
- **GAO-15-73:** "Because fees outpaced returns in most of the IRAs analyzed, these account balances tended to decrease over time"; a plan "can force out a participant with a balance of $20,000 if less than $5,000 is attributable to contributions other than rollover contributions". — [GAO-15-73](https://www.gao.gov/products/gao-15-73) (already in notes).
- **DOL RIA for the $7,000 limit (2024):** "There are 865,736 accounts that are not subject to mandatory distribution in the baseline because their balances are between $5,001 and $7,000." Year-one dispositions of accounts under $7,000: 1,773,374 cash out, 2,399,821 remain, 1,540,664 roll over, out of 5,713,860. DOL also states: "Increased mandatory distribution threshold leads to cost savings for plans but reduced benefits for separating participants." — [89 FR 5624, Table 3 and the A-4 accounting statement](https://www.govinfo.gov/content/pkg/FR-2024-01-29/html/2024-01208.htm). Also cited there: "roughly 40 percent of these accounts [small-balance default IRAs] remain in principal-preserving investments for at least 10 years".
- **Plan adoption of the $7,000 limit [recordkeeper/industry]:** 57% of Vanguard plans (2024) and 38% of T. Rowe Price plans (mid-2024) use automatic rollover at $7,000 (already in `notes/dc_plan_distributions.md` §8).
- **Vanguard 2025 update [recordkeeper/industry] (gapC):** share of plans with "Automatic cash-out if balance is <$1,000, roll over if between $1,000 and $7,000": 57% (2024) → 54% (2025); $1,000-$5,000 rollover: 29% → 25%; "Automatic portability" 7% (2025, new category); remain in plan above $1,000: 12% both years. Participants with termination dates who preserved assets, by balance: <$1,000 64% (2024) / 69% (2025); $1,000-4,999 61% / 62%; $5,000-9,999 59% / 59%; $10,000-24,999 65% / 64%. All terminated participants: 70% (2024) / 71% (2025) preserved; 28-29% took cash. — [Vanguard, How America Saves 2026, Figs. 113, 117, 118](https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf); [How America Saves 2025, Figs. 113, 118](https://corporate.vanguard.com/content/dam/corp/research/pdf/how_america_saves_report_2025.pdf). Pre-change comparator: DOL's RIA cites Vanguard 2023 for $1,000-4,999 as 34% cash-out, i.e. 66% preserved (89 FR 5624, Table 2). EBRI/NAGDCA's PRRL Fast Fact sizes the accounts newly in range in public plans but is a cross-section, not an outcome ([EBRI](https://www.ebri.org/content/secure-2.0-act-low-balance-distribution-limit-changes-a-look-by-age-and-tenure)). PSCA published "Automatic Rollover Rates" (June 2026) but psca.org returned 403; not read.

### Evidence verdict
- **The automatic-rollover default kept small balances in tax-deferred accounts.** Strong evidence (IRS data, RD design). About half of rollovers just above $1,000 are default-induced, meaning money that would otherwise have stayed in the plan or, below $1,000, been cashed out.
- **Whether that money is "working" is doubtful.** Moderate-to-strong evidence: compliers are passive, stay in principal-preserving funds and abandon accounts about 6-9 times more often than always-takers (computed from Table 8: 0.061/0.010 and 0.075/0.008). GAO found fees outpacing returns.
- **The 2024 $7,000 limit:** still no government or academic evidence (searched to 5 Oct 2026). Mechanically it enlarges the forced-out pool, which pushes against "staying in plan" but toward staying tax-deferred if the money lands in an IRA rather than cash. The only post-change data are Vanguard's [recordkeeper/industry] (see the cited finding below): adoption has plateaued at a bit over half of plans, and small-balance preservation in 2024-25 (61-62% for $1,000-4,999) is slightly below the 66% DOL took from Vanguard 2023. That is no sign the higher limit raised preservation, though it is not a before/after test.

### Gaps
- No study of cash-out rates by balance before and after 2005 or after 2024 (re-searched 5 Oct 2026: none from DOL, GAO, CRR, EBRI or NBER). Recordkeeper balance-band cash-out rates (Alight, Vanguard; `notes/dc_plan_distributions.md` §4) are cross-sections.
- GAO-15-73's numeric tables (fee and return simulations, number of forced-transfer IRAs) could not be downloaded (gao.gov 403; not on govinfo).

---

## 3. Auto-portability (SECURE 2.0 §120): regulation status, actual transfers vs DOL projection, and simulations

### Takeaway
The DOL rule implementing §120 is still only proposed (Jan 2024), but the final rule reached the White House on 14 Sep 2026: OIRA lists RIN 1210-AC21 "Exemption for Certain Automatic Portability Transactions", stage Final Rule, "Status: Pending Review", "RECEIVED DATE: 09/14/2026" ([reginfo.gov EO 12866 review search](https://www.reginfo.gov/public/do/eoReviewSearch?rin=1210-AC21), read 5 Oct 2026). The Federal Register shows no final rule as of 5 Oct 2026. Adoption is growing, but completed transfers are a small fraction of DOL's projection: about 16,700 cumulative completed transactions by Oct 2025, against a projected 337,000-398,000 a year. The only "effect" estimates are an industry pilot and EBRI simulations.

### Cited findings
- **Proposed rule:** "Automatic Portability Transaction Regulations", 89 FR 5624, proposed rule published 29 Jan 2024; comments closed 29 Mar 2024. — [Federal Register](https://www.federalregister.gov/documents/2024/01/29/2024-01208/automatic-portability-transaction-regulations); [DOL news release, 18 Jan 2024](https://www.dol.gov/newsroom/releases/ebsa/ebsa20240118)
- **Status:** Unified Agenda RIN 1210-AC21: "The Department received thirteen comments in response and is taking the public's input into account as it works to draft a final regulation." Final Rule date "01/00/2026" (Spring 2025 agenda) and "09/00/2026" (Fall 2025 agenda). — [reginfo.gov, Spring 2025](https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202504&RIN=1210-AC21); [Fall 2025](https://www.reginfo.gov/public/do/eAgendaViewRule?pubId=202510&RIN=1210-AC21). A Federal Register API search for "automatic portability" on 4 Oct 2026 returned only the 2024 proposed rule.
- **DOL's projection (NPRM RIA):** with PSN growth and the $7,000 limit, automatic-portability transfers of 397,749 in year 1, rising to 839,779 in year 9, for 7,029,170 over ten years. The baseline ($5,000 limit, RCH/PSN operating) has 337,484 a year. Annualised benefits are $191.12M/yr (7%) or $234.19M/yr (3%), and costs $1.21M/yr. DOL assumes auto-portability "reduce[s] the propensity to cash out for separating participants with small accounts by 25 percent", based on "a pilot study of automatic portability conducted by RCH which reduced cashout rates for small balance account holders by approximately 50 percent", while noting that the pilot "suggests that this finding is larger than we would observe under the statutory exemption". — [89 FR 5624, Tables 2-4 and the accounting statement](https://www.govinfo.gov/content/pkg/FR-2024-01-29/html/2024-01208.htm)
- **Actual activity [recordkeeper/industry]:** "over 21,000 plan sponsors that have enrolled"; "we've completed now 16,700 transactions"; "there's now 24,000. Transactions in motion" (Neal Ringquist, Retirement Clearinghouse, 22 Oct 2025). — [CAPTRUST podcast ep. 81](https://www.captrust.com/resources/portability-services-network-update/). There were 549 completed by 1 Dec 2024 (earlier notes). Retirement Clearinghouse reports more than 525,000 accounts and $20B consolidated across all its services since 2009, not only auto-portability (16-17 Dec 2025). — [RCH recent developments](https://rch1.com/auto-portability/recent-developments). PSCA (May 2026) headlines "Auto-Portability is Taking Off with Larger Plans", citing 60,000-100,000-participant plans; the page returned 403, so it was **not read**.
- **Update to July 2026 [recordkeeper/industry] (gapC):** PSN says it has been "automatically consolidating over 42,000 plan-to-plan balance transfers"; its six recordkeepers cover "63% of all defined contribution participants" and "82 million workers across more than 185,000 employer-sponsored retirement plans" (Steve Holman, PSN SVP, 24 Jul 2026). — [401k Specialist, "Busting 5 Key Myths About Auto Portability"](https://401kspecialistmag.com/busting-5-key-myths-about-auto-portability/). Vanguard: 7% of its plans had adopted auto-portability by year-end 2025 (HAS 2026, Fig. 113). PSN reported 20,997 adopting plan sponsors as of 30 Sep 2025 ([PLANSPONSOR](https://www.plansponsor.com/nearly-21000-plan-sponsors-have-adopted-psn-auto-portability)); no later sponsor count found. **Computed:** 42,000 cumulative = 12.4% of DOL's one-year baseline (337,484) and 10.6% of its post-rule year-1 projection (397,749); the run-rate between 22 Oct 2025 (16,700) and 24 Jul 2026 (42,000) is about 33,600 a year (25,300 over 275 days), roughly 10% of the projected annual flow.
- **Comparison, Computed:** 16,700 cumulative completed transactions (late 2023 to Oct 2025) are 4.9% of DOL's baseline one-year projection of 337,484, and 4.2% of the post-rule year-1 projection of 397,749.
- **[simulation] EBRI (VanDerhei, 15 Aug 2019):** the present value of additional accumulations over 40 years from "partial" auto-portability is $1,509B, or $1,987B under "full" auto-portability; retirement deficits fall 13-29% across household types. — [EBRI release](https://www.ebri.org/retirement/content/ebri-finds-auto-portability-preserves-retirement-savings). The $1.6T figure quoted by PSN is an update of the same model [simulation; industry-sponsored].
- **International comparison (government):** GAO reports that Australia's automatic transfer programme reunited "close to 4.7 million accounts valued at $7.11 billion AUD" between late 2019 and the end of 2022, and recommends that Congress authorise an automatic plan-to-plan rollover system and a pension dashboard. — [GAO-24-103577, Jan 2024](https://www.gao.gov/products/gao-24-103577)

### Evidence verdict
**Weak or none so far.** There is no independent evaluation of cash-out reduction under PSN. The 25% effect DOL uses is an assumption anchored on a 2013 industry pilot that DOL itself says overstates it. Realised volume is growing (about 42,000 cumulative by July 2026, a run-rate near 10% of DOL's projected annual flow), and the final rule has been at OIRA since 14 Sep 2026.

### Gaps
- No public data on dollars moved via PSN, match rates or opt-out rates (DOL assumed a 1.4% opt-out).
- No independent study (Treasury, IRS, GAO, academic) of whether auto-portability reduces cash-outs.

---

## 4. RMD age changes: new IRS SOI evidence and literature beyond the notes

### Takeaway
IRS SOI Table 4 has only five-year age bands, so age 72 cannot be isolated. The 70-74 band still shows a dose-response that matches the law. Withdrawal incidence among IRA holders aged 70-74 was 84.8-86.0 per 100 in 2016-2019, 58.8 in 2020 (waiver), 69.0-69.1 in 2021-22 (RMD age 72) and 61.7 in 2023 (RMD age 73). The 65-69 band moved by only about 1-3 points. A simple two-group decomposition reproduces the 2023 drop within about 4 points. No peer-reviewed or agency tax-data study of the 2020/2023 age changes was found; the literature remains the 2009/2020 waiver papers already in notes.

### Cited findings
- **IRS SOI Table 4 (all IRA types), age 70-74, withdrawers per 100 holders:** 84.8 (2016), 85.7 (2017), 85.6 (2018), 86.0 (2019), 58.8 (2020), 69.0 (2021), 69.1 (2022), 61.7 (2023). Age 65-69: 33.0, 33.9, 34.2, 35.0, 31.6, 34.5, 35.4, 37.8. Withdrawals as % of same-year FMV, 70-74: 5.11, 4.73, 5.46, 4.70, 3.23, 3.96, 4.63, 3.81. 2023 counts at 70-74: 3,917,487 withdrawers of 6,352,437 holders. — [IRS SOI IRA Table 4, e.g. 23in04ira.xlsx](https://www.irs.gov/pub/irs-soi/23in04ira.xlsx), as parsed in `irs/output/irs_soi_ira_2004_2023_current.json` (keys `inc`, `rate_same`, `age`). 2022-23 are a new SOI series (see `irs/README.md`).
- **Computed, illustrative decomposition.** Assume ages within 70-74 are equally populated and each person is either under RMD (incidence p1) or not (p0). The share of the band under RMD is about 0.9 in 2019 (70½ rule), 0.6 in 2021-22 (ages 72-74) and 0.4 in 2023 (ages 73-74). Solving with 2019 (86.0) and 2021 (69.0) gives p1 ≈ 91.7 and p0 ≈ 35.0. The p0 value matches the observed 65-69 incidence (34.5-35.0). The predicted 2023 incidence is 0.6×35.0 + 0.4×91.7 = 57.7, against 61.7 observed. Inputs: the `inc` values above. This is a consistency check, not an estimate.
- **Brown, Poterba & Richardson (TIAA):** 35.5% of 2008 RMD recipients suspended in 2009. **Mortenson, Schramm & Whitten (IRS):** about 50% would prefer to withdraw less than the RMD; up to 38% of constrained people did not respond to the 2009 suspension. Both are already in `notes/rmd_policy_tax_data.md` §2.
- **[simulation] Horneff, Maurer & Mitchell**, life-cycle model of raising the RMD age (NBER WP 28490, 2021). — [NBER w28490](https://www.nber.org/system/files/working_papers/w28490/w28490.pdf). Model-based, not evidence of behaviour.

### Evidence verdict
**The move from 70½ to 72 to 73 is "working" in the narrow sense of delaying withdrawals. Strong evidence**: IRS SOI band data, SIPP single-age data (in notes) and EBRI all agree, and the effect is large (the decomposition implies about 57 points lower incidence for people taken out of RMD coverage: about 35 vs 92 per 100). Whether the deferred money is eventually spent differently or left to heirs is not yet observable.

### Gaps
- No Treasury OTA, JCT or academic study using IRS microdata on the SECURE (2020) or SECURE 2.0 (2023) age changes was found. JCT's scores for SECURE 2.0 §107 were not retrieved.
- TY2024 SOI IRA tables are not released, and SOI publishes no single-year age tabulation.

---

## 5. In-plan retirement income and withdrawal flexibility: adoption and retention evidence

### Takeaway
The SECURE Act (2019) annuity-provider safe harbor has not produced widespread in-plan annuities: GAO cites an industry survey showing "nearly 7 percent" of 401(k)/profit-sharing plans with an in-plan annuity in 2023. Flexible installment and partial withdrawals are now common in large plans (already in notes). Evidence that flexibility keeps people in plans comes from the TSP natural experiment and Vanguard's non-randomised comparison (both in notes). No new academic causal study was found.

### Cited findings
- **GAO-26-107536 (released 6 Apr 2026):** "In 2023, nearly 7 percent of profit-sharing or 401(k) plans offered an 'in-plan' annuity option"; "About 17 percent of these types of plans are considering offering some form of annuity option in the future" (industry survey). It also reports that "about 11 percent" of married households with DC accounts took out funds in 2021 (SCF 2022), median $8,500. — [GAO-26-107536](https://files.gao.gov/reports/GAO-26-107536/index.html)
- **DOL direct final rule (1 Jul 2025)** removes the 2008 regulatory annuity-selection safe harbor (29 CFR 2550.404a-4) as "unnecessary" given the 2019 statutory safe harbor (ERISA §404(e)). — [90 FR, 2025-11615](https://www.federalregister.gov/documents/2025/07/01/2025-11615/selection-of-annuity-providers-safe-harbor-for-individual-account-plans)
- **Flexibility and retention (in notes):** TSP retention up about 4-8 points after Sep 2019 (64-65% before vs 68-73% after) (`dc_stay/README.md`). Vanguard 2021 retirees: 27% vs 20% still in plan three years later with vs without flexible distributions ("35% more likely"), and 15-25% less likely to cash out [recordkeeper/industry] (`notes/dc_plan_distributions.md` §1). Alight: 38% vs 28% retention among $250K+ leavers aged 60+ when installments are offered [recordkeeper/industry] (§4).

### Evidence verdict
- **Withdrawal flexibility raises retention:** moderate evidence and positive direction (one government natural experiment plus consistent recordkeeper cross-sections, none randomised).
- **In-plan annuities / lifetime income safe harbor:** weak evidence of take-up. About 7% of plans offer one, and the notes show participant election rates near zero historically.

### Gaps
- No DOL or GAO count of plans offering installments or partial withdrawals after 2017 (the last BLS NCS read). PSCA tables are paywalled.
- No data on take-up of in-plan annuities or lifetime-income target-date products by participants after 2022.

---

## Overall verdict (one line each)
- **Leakage before retirement:** flat-to-down relative to the system on IRS data; CARES showed that removing the penalty moves behaviour; recordkeeper hardship use rising since 2022. Mixed.
- **Force-out defaults:** keep money tax-deferred (strong), but often idle or abandoned (moderate-strong). $7,000 effect unknown.
- **Auto-portability:** not yet demonstrably working; small volumes; final rule pending.
- **RMD age:** clearly delays withdrawals (strong).
- **Flexible withdrawals:** help retention (moderate); annuity safe harbor take-up low (weak).

---

## Chart-ready series

### A. Returns paying the additional tax on early distributions (Schedule 2 line 8 / "penalty tax on qualified retirement plans"), % of all returns and per $100 of taxable IRA + pension distributions
Source for each year: `https://www.irs.gov/pub/irs-soi/YYin33ar.xls` (SOI Table 3.3), e.g. [23in33ar.xls](https://www.irs.gov/pub/irs-soi/23in33ar.xls). Denominator for the last column: taxable IRA + taxable pension amounts from `notes/rmd_policy_tax_data.md` series A/B (Pub 1304 / FRED / Pub 4801); for 2018 the combined line. All derived columns are **Computed**. The 2020-21 return counts include many non-filers who filed only for Economic Impact Payments, which inflates the denominator.

| Tax year | Returns with tax, % of all returns | Tax per $100 taxable IRA+pension distributions | Tax amount, $B | Implied penalised distributions (tax ÷ 0.10), $B |
|---|---|---|---|---|
| 1996 | 2.85 | 0.77 | 2.19 | 21.9 |
| 1997 | 2.79 | 0.74 | 2.34 | 23.4 |
| 1998 | 3.03 | 0.76 | 2.70 | 27.0 |
| 1999 | 3.21 | 0.79 | 3.07 | 30.7 |
| 2000 | 3.35 | 0.80 | 3.41 | 34.1 |
| 2001 | 3.51 | 0.75 | 3.26 | 32.6 |
| 2002 | 3.76 | 0.78 | 3.50 | 35.0 |
| 2003 | 3.74 | 0.74 | 3.41 | 34.1 |
| 2004 | 3.72 | 0.73 | 3.64 | 36.4 |
| 2005 | 3.59 | 0.72 | 3.82 | 38.2 |
| 2006 | 3.72 | 0.76 | 4.35 | 43.5 |
| 2007 | 3.88 | 0.78 | 5.00 | 50.0 |
| 2008 | 4.03 | 0.79 | 5.27 | 52.7 |
| 2009 | 4.18 | 0.81 | 5.31 | 53.1 |
| 2010 | 4.14 | 0.77 | 5.82 | 58.2 |
| 2011 | 3.93 | 0.71 | 5.70 | 57.0 |
| 2012 | 3.87 | 0.66 | 5.58 | 55.8 |
| 2013 | 3.89 | 0.69 | 5.87 | 58.7 |
| 2014 | 3.85 | 0.65 | 5.84 | 58.4 |
| 2015 | 3.62 | 0.63 | 5.98 | 59.8 |
| 2016 | 3.44 | 0.58 | 5.49 | 54.9 |
| 2017 | 3.34 | 0.56 | 5.66 | 56.6 |
| 2018 | 3.30 | 0.54 | 5.92 | 59.2 |
| 2019 | 3.30 | 0.55 | 6.04 | 60.4 |
| 2020 (CARES) | 2.36 | 0.33 | 3.64 | 36.4 |
| 2021 | 2.79 | 0.41 | 5.20 | 52.0 |
| 2022 | 2.97 | 0.42 | 5.65 | 56.5 |
| 2023 | 3.17 | 0.47 | 6.38 | 63.8 |

1996-2001 added by gapC (denominators for 1996-98 from SOI Table 1.4: [96in14si.xls](https://www.irs.gov/pub/irs-soi/96in14si.xls), [97in14.xls](https://www.irs.gov/pub/irs-soi/97in14.xls), [98in14ar.xls](https://www.irs.gov/pub/irs-soi/98in14ar.xls)). Bracketing EGTRRA's automatic-rollover rule (DOL safe harbor effective 28 Mar 2005): the share of returns is 3.72% (2004), 3.59% (2005), 3.72% (2006) and the tax per $100 is 0.73, 0.72, 0.76, with no visible break. The rule moved $1,000-$5,000 balances into IRAs instead of cash, but those accounts are small relative to the aggregate, so an aggregate series would not be expected to show it. The 1996-2002 rise in the share of returns (2.85% to 3.76%) parallels the growth of IRA/401(k) balances, while tax per $100 of distributions stays flat at 0.74-0.80.

Implied penalised distributions are an upper-bound proxy: the line includes small non-early-distribution taxes and the 25% SIMPLE rate. Cross-check (**Computed**): Argento et al.'s under-55 penalised distributions are 0.82 (2004: 29.7/36.4) and 0.81 (2010: 47.3/58.2) of this proxy, which is consistent because the proxy also covers ages 55-59½.

### B. Form 5329 Part I: share of early distributions excepted from the 10% tax (filers of Form 5329 only)
| Tax year | Early distributions reported, $B | Excepted, % of dollars (Computed) | Subject to tax, $B | Source |
|---|---|---|---|---|
| 2004 | n/p | n/p | 11.39 | https://www.irs.gov/pub/irs-prior/p4801--2006.pdf |
| 2005 | n/p | n/p | 10.55 | https://www.irs.gov/pub/irs-prior/p4801--2007.pdf |
| 2006 | n/p | n/p | 11.88 | https://www.irs.gov/pub/irs-prior/p4801--2008.pdf |
| 2007 | n/p | n/p | 13.27 | https://www.irs.gov/pub/irs-prior/p4801--2009.pdf |
| 2008 | n/p | n/p | 13.89 | https://www.irs.gov/pub/irs-prior/p4801--2010.pdf |
| 2009 | 19.54 | 24.1 | 14.83 | https://www.irs.gov/pub/irs-prior/p4801--2011.pdf |
| 2010 | 24.36 | 34.3 | 16.02 | https://www.irs.gov/pub/irs-prior/p4801--2012.pdf |
| 2011 | 22.29 | 32.2 | 15.11 | https://www.irs.gov/pub/irs-prior/p4801--2013.pdf |
| 2012 | 22.82 | 33.6 | 15.16 | https://www.irs.gov/pub/irs-prior/p4801--2014.pdf |
| 2013 | 23.52 | 35.1 | 15.25 | https://www.irs.gov/pub/irs-prior/p4801--2015.pdf |
| 2014 | 24.88 | 36.2 | 15.86 | https://www.irs.gov/pub/irs-prior/p4801--2016.pdf |
| 2015 | 24.44 | 35.7 | 15.72 | https://www.irs.gov/pub/irs-prior/p4801--2017.pdf |
| 2016 | 24.14 | 35.8 | 15.51 | https://www.irs.gov/pub/irs-soi/16inlinecount.pdf |
| 2017 | 26.98 | 40.0 | 16.19 | https://www.irs.gov/pub/irs-prior/p4801--2019.pdf |
| 2018 | 26.89 | 35.1 | 17.45 | https://www.irs.gov/pub/irs-prior/p4801--2020.pdf |
| 2019 | 26.12 | 37.3 | 16.38 | https://www.irs.gov/pub/irs-prior/p4801--2021.pdf |
| 2020 | 27.47 | 66.5 | 9.21 | https://www.irs.gov/pub/irs-prior/p4801--2022.pdf |
| 2021 | 25.68 | 35.5 | 16.54 | https://www.irs.gov/pub/irs-prior/p4801--2024.pdf |
| 2022 | 28.33 | 35.2 | 18.34 | https://www.irs.gov/pub/irs-prior/p4801--122024.pdf |
| 2023 | (133.0, SOI estimation anomaly; see §1) | (do not use) | 22.17 | https://www.irs.gov/pub/irs-pdf/p4801.pdf |

n/p = not published (TY2004-2008 editions print only lines 3-4).

### C. IRA withdrawal incidence, age 70-74 vs 65-69 (IRS SOI Table 4; withdrawers per 100 holders)
| Year | RMD rule for the 70-74 band | 70-74 | 65-69 | Source |
|---|---|---|---|---|
| 2016 | 70½ | 84.8 | 33.0 | https://www.irs.gov/pub/irs-soi/16in04ira.xls |
| 2017 | 70½ | 85.7 | 33.9 | https://www.irs.gov/pub/irs-soi/17in04ira.xlsx |
| 2018 | 70½ | 85.6 | 34.2 | https://www.irs.gov/pub/irs-soi/18in04ira.xlsx |
| 2019 | 70½ | 86.0 | 35.0 | https://www.irs.gov/pub/irs-soi/19in04ira.xlsx |
| 2020 | waived | 58.8 | 31.6 | https://www.irs.gov/pub/irs-soi/20in04ira.xlsx |
| 2021 | 72 | 69.0 | 34.5 | https://www.irs.gov/pub/irs-soi/21in04ira.xlsx |
| 2022 | 72 | 69.1 | 35.4 | https://www.irs.gov/pub/irs-soi/22in04ira.xlsx |
| 2023 | 73 | 61.7 | 37.8 | https://www.irs.gov/pub/irs-soi/23in04ira.xlsx |

### D. IRA withdrawals under age 60 (IRS SOI Table 4; includes penalty-free ages 59½-59 and Roth contribution withdrawals). 2012-2023 only; earlier years have breaks
| Year | Withdrawers per 100 holders <60 | Withdrawals, % of same-year FMV (Computed: wa/fa) | Source |
|---|---|---|---|
| 2012 | 12.3 | 2.77 | https://www.irs.gov/pub/irs-soi/12in04ira.xls |
| 2013 | 12.7 | 2.38 | https://www.irs.gov/pub/irs-soi/13in04ira.xls |
| 2014 | 12.6 | 2.33 | https://www.irs.gov/pub/irs-soi/14in04ira.xls |
| 2015 | 12.7 | 2.46 | https://www.irs.gov/pub/irs-soi/15in04ira.xls |
| 2016 | 12.2 | 2.07 | https://www.irs.gov/pub/irs-soi/16in04ira.xls |
| 2017 | 12.6 | 1.93 | https://www.irs.gov/pub/irs-soi/17in04ira.xlsx |
| 2018 | 12.7 | 2.21 | https://www.irs.gov/pub/irs-soi/18in04ira.xlsx |
| 2019 | 12.9 | 1.84 | https://www.irs.gov/pub/irs-soi/19in04ira.xlsx |
| 2020 | 11.7 | 1.72 | https://www.irs.gov/pub/irs-soi/20in04ira.xlsx |
| 2021 | 12.1 | 1.65 | https://www.irs.gov/pub/irs-soi/21in04ira.xlsx |
| 2022 (new series) | 12.3 | 2.01 | https://www.irs.gov/pub/irs-soi/22in04ira.xlsx |
| 2023 (new series) | 13.0 | 1.96 | https://www.irs.gov/pub/irs-soi/23in04ira.xlsx |

### E. Hardship withdrawal use, Vanguard plans [recordkeeper/industry] (% of participants permitted)
| Year | % initiating | Source |
|---|---|---|
| 2020 | 2 | https://workplace.vanguard.com/content/dam/inst/iig-transformation/insights/pdf/2026/how-america-withstands-financial-hardships.pdf (Fig. 2) |
| 2021 | 2 | same |
| 2022 | 3 | same |
| 2023 | 4 | same |
| 2024 | 5 | same |
| 2025 | 6 | same |

### E2. TSP (FRTIB administrative data): % of FERS participants taking a hardship withdrawal / with a loan (government)
| Year | Hardship withdrawal % | Loan % (incl. CARES loans) | Source |
|---|---|---|---|
| 2015 | 3.3 | 8.5 | https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2015-2019.pdf |
| 2016 | 3.2 | 8.7 | same |
| 2017 | 3.5 | 8.8 | https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2017-2021.pdf |
| 2018 | 3.3 | 8.5 | same |
| 2019 | 3.7 | 8.6 | https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2019-2023.pdf |
| 2020 | 2.9 | 7.1 | same |
| 2021 | 4.0 | 7.0 | https://www.frtib.gov/pdf/reading-room/congress/annual/TSP-Annual-Report_2025.pdf |
| 2022 | 2.1 | 6.6 | same |
| 2023 | 3.1 | 8.3 | same |
| 2024 | 3.8 (chart: 3.9) | 8.5 (chart: 8.6) | same |
| 2025 | 4.9 | 9.5 | same |

### F. CRD uptake, 2020 (% of eligible participants)
| Source | % | Type | URL |
|---|---|---|---|
| TSP (of active participants) | 2.8 | government | https://www.everycrsreport.com/reports/R46837.html |
| Empower | 4.4 | recordkeeper/industry | same |
| Ascensus | 4.9 | recordkeeper/industry | same |
| Vanguard | 5.7 | recordkeeper/industry | same |
| ICI (30M+ participants) | 5.8 | recordkeeper/industry | same |
| Fidelity | 6.3 | recordkeeper/industry | same |

### G. Auto-portability: actual vs projected
| Measure | Value | Source |
|---|---|---|
| Completed PSN transactions, cumulative to 1 Dec 2024 | 549 | https://www.psca.org/news/psca-news/2024/12/portability-services-network-now-covers-5m-participants-15000-plans/ |
| Completed PSN transactions, cumulative to ~Oct 2025 | 16,700 | https://www.captrust.com/resources/portability-services-network-update/ |
| DOL projected AP transfers per year (baseline) | 337,484 | https://www.govinfo.gov/content/pkg/FR-2024-01-29/html/2024-01208.htm |
| DOL projected AP transfers, year 1 post-rule | 397,749 | same |
| Cumulative actual as % of one projected baseline year (Computed) | 4.9% | inputs above |
| Completed PSN transfers, cumulative to 24 Jul 2026 [industry] | 42,000+ | https://401kspecialistmag.com/busting-5-key-myths-about-auto-portability/ |
| Cumulative to Jul 2026 as % of one projected baseline year (Computed) | 12.4% | inputs above |
| Annualised run-rate Oct 2025-Jul 2026 as % of baseline year (Computed: 25,300 × 365/275 ÷ 337,484) | ~10% | inputs above |
| Vanguard plans with auto-portability, YE2025 [recordkeeper] | 7% | https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf |
| DOL final rule status | At OIRA, received 14 Sep 2026, pending | https://www.reginfo.gov/public/do/eoReviewSearch?rin=1210-AC21 |
