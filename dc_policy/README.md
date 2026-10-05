# DC plan laws: are they getting more people in, and keeping money in longer?

Question (Richard, 2026-10-04): what legislative changes expand DC plan participation (e.g. auto-enrollment) and encourage staying in DC plans longer, and is there evidence they are working?

Scope chosen: US federal law (Revenue Act 1978 through SECURE 2.0 and OBBBA 2025), federal TSP changes, and state auto-IRA mandates. Public and academic sources lead; recordkeeper and industry data are labeled **[recordkeeper/industry]**. Full citations (URL, table, page, verbatim quotes) are in the four notes files; this README gives the findings and points to them. Built 2026-10-04; gaps filled 2026-10-05.

## Short answer

| Provision | Is it working? | Strength of evidence |
|---|---|---|
| Auto-enrollment, where a plan adopts it | Yes for participation (roughly 85-95% vs 35-65% without), and the effect lasts | Strong (firm studies, TSP admin data, UK) |
| Auto-enrollment, effect on lifetime saving | Positive but small: about +0.6% of income a year, +0.3% more from default escalation, after cash-outs and turnover | Moderate (two recent large studies) |
| Auto-enrollment, effect on national participation | Mixed. It spread (31% of 401(k) plans in 2024, up from 4% in 2010). IRS W-2 data show the share of wage earners deferring rising from 34.7% (2008) to 42.8% (2020), but the BLS employer survey shows participation flat at 52-53% | Moderate (IRS W-2, BLS NCS, CPS, Form 5500) |
| Higher default contribution (TSP 3% to 5%, 2020) | Yes: share of FERS contributors below the full match fell from 30% to 11% | Strong (government admin data) |
| SECURE 2.0 auto-enrollment mandate for new plans (2025) | Being complied with: 88% of new 2025 401(k)s have AE vs 30% of 2019 starts | Early, weak-to-moderate (Computed from Form 5500); no saving data yet |
| State auto-IRA mandates | Yes for coverage: real but small accounts, plus firms starting their own 401(k)s | Strong for crowd-in (IRS data), moderate for saving |
| Federal startup credits (SECURE 2019 / 2.0) | Barely used: 1% of eligible firms before, 5.5% in 2023 | Strong that take-up is low |
| Long-term part-time eligibility (2024/2025) | No measurable effect yet | None/weak |
| Automatic rollover of small balances (2005, $1,000-$5,000) | Keeps money tax-deferred, but in passive, often cash-like, frequently abandoned IRAs | Strong (IRS data, regression discontinuity) |
| Force-out limit to $7,000 (2024) | Unknown | None yet |
| Auto-portability (SECURE 2.0 sec. 120) | Not yet: about 42,000 transfers by July 2026, roughly 10% of the yearly volume DOL projected; final rule at White House review since Sep 14 2026 | Weak/none |
| RMD age 70½ to 72 to 73 | Yes, it delays withdrawals | Strong (IRS, SIPP, EBRI) |
| TSP withdrawal flexibility (2019) | Yes, one-year retention rose about 7-10 points | Moderate (one natural experiment; prior project work) |
| New penalty-free withdrawal routes (about 9 since 2018) | Push the other way; CARES 2020 showed loosening penalties raises leakage | Strong for CARES; weak for the rest so far |

The overall picture: laws that change **defaults** work, laws that offer **incentives** (credits) or **permissions** (auto-portability, part-time eligibility) have shown little so far, and Congress has widened withdrawal access at the same time as it encouraged staying in.

## 1. What changed in the law
`notes/provisions.md`, `output/provisions_timeline.csv` (67 provisions, 1978-2026; each tagged participation / contribution / staying-in-plan / leakage-increasing, with effective date and primary-source link).

- **Participation:** IRS approval of "negative election" (Rev. Rul. 98-30, 2000 rulings); PPA 2006 (QACA and EACA safe harbors, preemption of state wage-withholding laws, QDIA rule 2007); TSP auto-enrollment of new federal hires Aug 1 2010 at 3%, default 5% from Oct 1 2020; SECURE Act 2019 (pooled employer plans, bigger startup credit, $500 auto-enrollment credit, long-term part-time 3 years x 500 hours); SECURE 2.0 2022 (mandatory AE at a 3-10% starting rate rising 1 point a year to at least 10%, cap 15%, for 401(k)/403(b) plans set up after Dec 29 2022, for plan years from 2025, small and new employers exempt; part-time rule cut to 2 years from 2025; Saver's Match from 2027).
- **Staying in:** EGTRRA automatic IRA rollover of $1,000-$5,000 force-outs (DOL safe harbor, March 28 2005); TSP Modernization Act (withdrawal flexibility, Sept 15 2019); RMD age 72 (2020), 73 (2023), 75 (2033); SECURE 2.0 auto-portability (sec. 120, from Dec 29 2023), Lost & Found database (sec. 303), force-out limit $7,000 (sec. 304, 2024).
- **Pushing the other way (leakage-increasing):** easier hardship withdrawals (BBA 2018), birth/adoption $5,000 (2020), CARES coronavirus distributions up to $100,000 (2020), $1,000 emergency withdrawals (2024), domestic abuse, terminal illness, permanent disaster distributions ($22,000), 403(b) hardship parity.
- **Not final as of 2026-10-05:** the AE-mandate regulation (proposed Jan 14 2025; final rule at OIRA since June 23 2026 per reginfo.gov; good-faith compliance meanwhile), the DOL auto-portability rule (proposed Jan 29 2024; final rule at OIRA since Sep 14 2026), long-term part-time regs (proposed Nov 2023), Saver's Match (Notice 2026-48 only). OBBBA 2025 made no change to 401(k)/403(b) participation or withdrawal rules. Pending bills (GovTrack, since congress.gov is blocked): only S. 3333 (emergency-savings side-account cap to $5,000) has been reported from committee; the Automatic IRA Act and Auto Reenroll Act are introduced only.
- **States:** 17 state auto-IRA programs plus Philadelphia enacted 2015-2026; 15 open to all covered employers by 2026 (Oregon first, 2017; Minnesota latest, 2026). Dates from the Georgetown CRI tracker, checked against program sites for CT, MD, CO, VA and RI (`notes/gapfill_B.md`). Rhode Island: enacted June 26 2024, launched Oct 21 2025.
- Revenue Act 1978: 401(k) applies to "plan years beginning after December 31, 1979" (sec. 135(c)(1), 92 Stat. 2787).

## 2. Getting people in: auto-enrollment
`notes/auto_enrollment.md` (13 chart-ready tables), `output/form5500_autoenroll_share.csv` (script `raw/autoenroll/autoenroll_form5500.py`).

- **Firm studies:** participation of new hires 86% with AE vs 37% without (Madrian & Shea 2001, [NBER w7682](https://www.nber.org/papers/w7682)); over 85% at all three firms in Choi et al.
- **Long-run saving is much smaller than early studies implied:** about +0.6% of income from AE and +0.3% from default escalation, 76% below the naive estimate, because 42% of balances are cashed out at job change, matches go unvested, and only 43%, 36%, then 29% accept each scheduled step-up (Choi, Laibson, Cammarota, Lombardo & Beshears 2024, [NBER w32828](https://www.nber.org/papers/w32828)). Gains fade within 36 months except for low earners (Choukhmane, AER 2025). Army civilians: +4.1% of salary after 4 years with little extra debt beyond car loans and mortgages (Beshears et al., JF 2022).
- **TSP (FRTIB administrative data):** FERS participation 84.7% (2009), about 86.6% (2010), 88.2% (2011), 89.0% (2012), 89.6% (2013) (2010-2013 read from FRTIB charts, approximate), 96.2% (2025); employees with under 2 years' tenure 70.0% (2009) to 97.9% (2012); opt-outs about 1.6-4%. After the default rose to 5%, contributors below the full 5% match fell from 30% (2019) to 11.15% (2025).
- **Spread (DOL Form 5500, Computed):** 401(k) plans reporting automatic enrollment 3.9% (2010), 6.9% (2015), 13.6% (2019), 26.2% (2023), 31.4% (2024); their share of participants with balances 26% to 54%. BLS NCS: share of private participants in plans with AE 19% (2009), 40% (2019), 42% (2022). [recordkeeper/industry] Vanguard: 10% of plans (2006) to 61% (2025); participation 94% in AE plans vs 64% in voluntary ones.
- **Recordkeeper detail [recordkeeper/industry]:** 62% of Vanguard AE plans default at 4% or more and about 7 in 10 auto-escalate (How America Saves 2025; earlier attributed to PSCA in error). Thaler-Benartzi SMarT: 78% joined the escalation plan.
- **SECURE 2.0 mandate, first signal (Computed, Form 5500; 2025 filings incomplete):** new 401(k) plans with AE in their first year: 30% (2019 starts), 60% (2023), 75% (2024), 88% (2025). Mandate-covered 2023 plans went from 62% to 74% when the mandate began; exempt 2022 plans rose about 4 points. Consistent with compliance, not a causal estimate.
- **UK comparison:** a universal employer mandate took private-sector participation among eligible employees from 42% (2012) to 89% (2024).

## 3. Coverage: state auto-IRAs, credits, part-timers, national trend
`notes/coverage_state_autoira.md`, `output/bls_ncs_access_participation.csv` (script `raw/stateira/build_bls_csv.py`).

- **State programs (Georgetown CRI, 31 Aug 2026):** 1,413,435 funded accounts, $3.39B assets, 404,101 registered employers (109k funded accounts in Dec 2019). CalSavers opt-out 34.4%; OregonSaves 26.5% within 30 days, but about half opt out within 12 months and about 70% stop contributing (Chalmers, Mitchell, Reuter & Zhong 2024). Contribution rates about 5-7% of pay; CalSavers median balance $704. Withdrawals equal 32.3% (CalSavers) and 41.1% (OregonSaves) of all contributions ever made (Computed). Only about 8% of CalSavers' estimated eligible employers have started deductions.
- **Crowd-in (the strongest finding here):** with IRS data, about 17% of mandate-covered firms started their own plan, with no sign of firms dropping plans; firm-run plans are 30-45% of the mandates' total coverage effect (Bloomfield, Goodman, Rao & Slavov, J. Public Economics 2025, [NBER w32817](https://www.nber.org/papers/w32817)).
- **Do national surveys count auto-IRAs?** BLS gives no explicit rule, but its definitions say a payroll-deduction IRA with minimal employer involvement "is not treated as an employer-sponsored retirement plan", so NCS most likely excludes auto-IRAs and understates coverage gains in mandate states.
- **Startup credits (sec. 45E):** claimed by 1% of eligible firms before SECURE and 5.5% in 2023 (about 18,000 firms, mostly pass-throughs); "a limited impact on new ESRP formation" ([Georgetown CRI 2025](https://cri.georgetown.edu/wp-content/uploads/2025/07/Bloomfield-Goodman-Ramnath-Slavov-2025-Georgetown-CRI.pdf)).
- **National trend, BLS NCS, private industry, March (all retirement plans):**

| Year | Access | Participation | Take-up | Access, <50 workers | Part-time access | Part-time take-up |
|---|---|---|---|---|---|---|
| 2009 | 67 | 51 | 77 | 48 | 39 | 55 |
| 2012 | 65 | 48 | 75 | 46 | 38 | 50 |
| 2016 | 66 | 50 | 76 | 47 | 37 | 57 |
| 2019 | 67 | 52 | 77 | 50 | 39 | 57 |
| 2022 | 69 | 52 | 75 | 52 | 43 | 48 |
| 2024 | 72 | 53 | 73 | 55 | 47 | 51 |
| 2026 | 72 | 52 | 72 | 55 | 44 | 46 |

DC-only figures (2010-2026, `plan_type` column) show the same pattern: access 64% (2019) to 70% (2026), take-up 74% to 70%. Access is up 5 points since 2019, mostly at small establishments, but participation is flat because take-up fell: new access is reaching workers who join less (small-firm, part-time, low-wage). BLS widened "access" in 2009, so earlier years are not comparable. Whether NCS counts state auto-IRAs as plans is unverified; if not, mandate-state gains are understated. Part-time access rose through 2025 then dipped; no direct evaluation of the long-term part-time rule exists.
- **IRS W-2 data (new admin series, `output/irs_w2_deferral_participation.csv`, Computed from SOI Form W-2 statistics Table 3.C):** share of filers with wages who made an elective deferral (W-2 box 12 D/E/F/G/H/S/AA/BB/EE), private and public employers:

| Tax year | % with elective deferral | Under 26 | % retirement-plan box checked |
|---|---|---|---|
| 2008 | 34.7 | 12.1 | 46.3 |
| 2010 | 33.5 | 11.8 | 44.9 |
| 2014 | 36.5 | 14.5 | 45.5 |
| 2017 | 39.9 | 17.3 | 47.1 |
| 2020 | 42.8 | 20.8 | 49.7 |

The rise is concentrated among young workers, which is where auto-enrollment bites, and it differs from the flat NCS participation rate. Two reasons are likely: W-2 counts anyone who deferred at any point in the year at any job, while NCS is a March snapshot; and part of the rise is nominal wage growth moving people into higher wage bands (within wage bands the gain is only 1-4 points). TY2021+ is not published yet.
- **Plan formation (Form 5500):** DC plan count growth went from 1-2% a year (2016-19) to 5.0% (2022) and 4.7% (2023); plans under 100 participants +15.7% 2019-2023 (DOL's 2023 participant-counting change does not appear to have shifted the size classes: large DC plans rose 4.6% in 2023 rather than falling). Pooled employer plans: 81 filings (2021) to 269 (2023), 1.16M participants, 39,446 employers. Consistent with policy, not attributed by DOL.

### CPS ASEC from Census files (new microdata series)
`notes/cps_participation.md`, `scripts/cps_participation.py`, `output/cps_plan_participation_by_year.csv`, `output/cps_participation_breaks_ppa.csv`, `output/cps_state_autoira_check.csv`. Private wage-and-salary workers 21-64 who worked last year, ASEC 2001-2026, replicate-weight SEs from ASEC 2005 (design-effect SEs before).

- Offer (PENPLAN) fell from 59.6% to 49.7% and participation (PENINCL) from 46.9% to 40.0% over income years 2000-2012 on a consistent questionnaire.
- **PPA test:** take-up among those offered rose 1.41 points (SE 0.19) between ASEC 2003-07 and 2010-13, in every subgroup, but it starts in 2005 (before PPA) and overlaps the recession. Weak evidence of a PPA effect.
- **The 2014 redesign breaks the series:** within ASEC 2014 the redesigned sample shows offer 4.8 points lower (SE 0.55) and participation 4.5 lower (SE 0.52). CPS keeps drifting down after that (participation 28.4% in income year 2025), which W-2 and NCS evidence say is an artifact. Do not use CPS levels after 2013 for trends. The 2019 processing change moves these measures by at most 0.3 points.
- **State auto-IRA check (suggestive):** employers under 100, Oregon, Illinois and California vs non-adopting states, income years 2021-25 vs 2012-16: offer +1.1 (SE 0.75), participation +0.1 (SE 0.68). A weak null; auto-IRA savers may not report a "plan at work".

## 4. Keeping money in: stay-in-plan provisions and leakage
`notes/stay_in_plan_leakage.md`, `output/irs_early_distribution_penalty.csv`, `output/irs_form5329_part1.csv` (script `raw/stayinplan/build_penalty_series.py`). Builds on `../dc_stay/` (TSP retention, Form 5500, SCF), `../notes/followups_2026-10-04.md` (SIPP age-72) and `../notes/rollovers.md` section 9 (auto-portability adoption), which are not repeated.

- **Leakage before 59½ is not rising relative to the system (IRS SOI, Computed):** returns paying the 10% additional tax on early distributions:

| Tax year | % of all returns | Tax per $100 of taxable IRA + pension distributions |
|---|---|---|
| 1996 | 2.85 | 0.77 |
| 2002 | 3.76 | 0.78 |
| 2009 | 4.18 | 0.81 |
| 2015 | 3.62 | 0.63 |
| 2019 | 3.30 | 0.55 |
| 2020 (CARES) | 2.36 | 0.33 |
| 2023 | 3.17 | 0.47 |

There is no break around the 2005 automatic-rollover rule (3.72%, 3.59%, 3.72% in 2004-06). The series understates early withdrawals: TIGTA found that for TY2021 half of the 6.2M taxpayers with early distributions neither paid the tax nor filed Form 5329. The 2020 drop (returns -25.6%, tax dollars -39.7%) is CARES moving withdrawals into penalty-free coronavirus distributions while total under-59½ withdrawals rose, so loosening penalties does raise leakage. No IRS or Treasury tabulation of the 2020 coronavirus distributions (Form 8915-E) exists; GAO (GAO-24-103577) reports 6% of participants took one, averaging $18,344. Hardship withdrawals in a government plan (TSP, FERS participants): 3.3% (2015), 2.1% (2022), 4.9% (2025); loans 9.5% (2025), both series highs. [recordkeeper/industry] Vanguard hardship withdrawals rose from 2% (2020) to 6% (2025) of participants; the $1,000 emergency withdrawal is offered by 4% of Vanguard plans and used by 0.4% of their participants.
- **Automatic rollover default (2005):** about 48% of IRA rollovers just above $1,000 and 29% just below $5,000 happen only because of the default; those accounts are passive, often in cash-like funds, and abandoned 6-9 times more often (Goodman, Mukherjee & Ramnath, [Chicago Fed WP 2022-50](https://www.chicagofed.org/-/media/publications/working-papers/2022/wp2022-50-pdf.pdf?sc_lang=en), IRS data). GAO found fees outpacing returns in such IRAs. The 2024 $7,000 limit: no government or academic evidence yet. [recordkeeper/industry] Vanguard: plans using automatic rollover up to the limit fell from 57% to 54%, and leavers with $1,000-4,999 kept their money tax-deferred 61-62% of the time vs 66% in 2023, so no sign yet that it raised preservation.
- **Auto-portability:** about 16,700 transfers completed by October 2025 and over 42,000 by July 24 2026 [industry], roughly 10% of the 337,000-398,000 a year DOL projected (Computed). The DOL final rule (RIN 1210-AC21) has been at OIRA since Sep 14 2026 and is not yet published. EBRI's $1.5-2.0 trillion figure is a simulation.
- **RMD age (IRS SOI, IRA holders 70-74 withdrawing):** 86.0% (2019), 58.8% (2020 waiver), 69.0-69.1% (2021-22, age 72), 61.7% (2023, age 73). Combined with SIPP (age 72 falls from 64-67 to 30-37 per 100) and EBRI, delay is clear. Whether the deferred money is later spent or left to heirs can't be seen yet.
- **Withdrawal flexibility:** TSP one-year retention 57-61% (FY15-16) to 68-73% (FY21-22) after the 2019 change (`../dc_stay/`), backed by recordkeeper cross-sections. In-plan annuities: about 7% of plans offered one in 2023 (GAO 2026 citing an industry survey), and take-up historically near zero.

## Caveats
- Most national series (NCS, Form 5500, CPS, IRS penalty counts) are descriptive and overlap several policies and the business cycle; only the firm studies, TSP, the state-mandate study and the rollover-default study are causal designs.
- Form 5500 2025 filings are incomplete (AE share for 2025 plans will move). Form 5500 counts plans, not people; the 2023 DOL participant-counting change may affect small-plan counts (unconfirmed).
- BLS NCS 2009 definition break; CPS ASEC 2014 redesign break (levels after 2013 unusable).
- TY2023 Form 5329 lines 1-2 (exception amounts) are printed by SOI as $133.0B and $110.8B, about 5x prior years with nothing else moving; likely a sample outlier or capture error, so excluded. Lines 3-4 are usable (`notes/gapfill_C.md`).
- Gaps closed on 2026-10-05 are logged in `notes/gapfill_A.md`, `gapfill_B.md`, `gapfill_C.md`. Still not verifiable from here: PSCA 68th-survey figures incl. 36% emergency-withdrawal adoption (psca.org and napa-net.org blocked); Pew April 2026 new-plan shares (pewtrusts.org blocked; two search extracts agree); Rhode Island's first-wave deadline (RI Treasury pages 403); several state size-wave deadlines rest on secondary sources. Illinois Secure Choice opt-out 36.94% (Dec 2025) is verified; its dashboard shows 25-26% from June 2026 with no explanation, likely a new definition, so don't compare across it.
- Not available anywhere: IRS counts of startup-credit claims for pass-through firms (C corporations only, 115-729 a year, `output/irs_form8881_credit_claims.csv`); IRS W-2 statistics after TY2020; a CPS ASEC series after 2013 usable for levels.

## Files
- `notes/provisions.md`, `notes/auto_enrollment.md`, `notes/coverage_state_autoira.md`, `notes/stay_in_plan_leakage.md`, `notes/cps_participation.md`: cited findings, verdicts, gaps and chart-ready tables per topic.
- `output/`: `provisions_timeline.csv`, `irs_w2_deferral_participation.csv`, `irs_form8881_credit_claims.csv`, `form5500_autoenroll_share.csv`, `bls_ncs_access_participation.csv`, `irs_early_distribution_penalty.csv`, `irs_form5329_part1.csv`, `cps_plan_participation_by_year.csv`, `cps_participation_breaks_ppa.csv`, `cps_state_autoira_check.csv`.
- `scripts/cps_participation.py` (downloads from www2.census.gov; cache outside the shared folder). Other build scripts sit beside their raw inputs in `raw/autoenroll/`, `raw/stateira/`, `raw/stayinplan/`.
- `raw/`: source PDFs and tables (FRTIB, CRS, IRS SOI, state program dashboards, Senate Finance SECURE 2.0 summary).

Nothing here has been put in the report or CLAUDE.md.
