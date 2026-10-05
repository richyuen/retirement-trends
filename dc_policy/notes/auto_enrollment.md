# Automatic enrollment (AE) and automatic escalation (AutoEsc): do they raise participation and saving, and do the effects persist?

Task: autoenroll. Compiled 2026-10-04. Policies covered: PPA 2006 (AE safe harbor, preemption of state wage-withholding laws, QDIA regulation 2007); SECURE 2.0 Act sec. 101 (new 401(k)/403(b) plans established after Dec 29, 2022 must auto-enroll at 3% to 10% with 1-point annual escalation to at least 10% (max 15%), for plan years beginning on or after Jan 1, 2025; exempt: employers with 10 or fewer employees, businesses under 3 years old, church and governmental plans); federal Thrift Savings Plan (TSP) AE for FERS new hires (Aug 2010, default 3%) and the 5% default (Oct 1, 2020).

Labels: **[gov]** government administrative or statistical; **[academic]** peer-reviewed or NBER/RRC working paper; **[recordkeeper/industry]** Vanguard, Fidelity, PSCA, etc.; **Computed** = my own calculation from public microdata, with the inputs stated.

Raw files kept in `dc_policy/raw/autoenroll/`: the FRTIB participant-behavior reports (2012, 2014, 2017-21, 2019-23, 2021-25), CRS IF12756, my Form 5500 script (`autoenroll_form5500.py`) and its output (`form5500_autoenroll_share.csv`).

---

## Bottom line (read this first)

1. **Participation: strong evidence, large and lasting.** In every setting, AE raises plan participation by about 25 to 50 percentage points (pp) for new hires, and participation stays up. Few people opt out later: 1.6% to 4% in the TSP, and fewer than 1% of UK savers stop per quarter. The gaps by income, age and race narrow sharply.
2. **Saving: positive, but much smaller than the early studies implied.**
   - Low defaults (3%) anchor contributions.
   - People who are not auto-enrolled catch up over time.
   - Turnover, unvested matches and cash-outs when people leave a job erode the gain.
   - The best long-run estimate (Choi, Laibson, Cammarota, Lombardo, Beshears, NBER 2024) is a steady-state gain of only **+0.6% of income from AE and +0.3% from default auto-escalation**. That is 76% below the naive estimate.
   - Choukhmane (AER 2025) finds the effects fade by 36 months, except at the bottom of the distribution.
   - On the other hand, AE does **not** cause offsetting debt (Beshears et al., JF 2022: US Army civilians, +4.1% of salary in TSP contributions after 4 years, no rise in non-mortgage, non-auto debt).
3. **Default design matters, and the TSP is the cleanest government case.**
   - FERS participation rose from 84.7% (2009) to 96.2% (2025).
   - Among employees with under 2 years of tenure it rose from 70.0% (2009) to 97.9% (2012).
   - The 3% default dragged down average deferrals.
   - Moving to a 5% default in Oct 2020 cut the share contributing below the full-match rate from 30% (2019) to 11.2% (2025).
4. **Adoption.**
   - About 31% of 401(k) plans and about 54% of 401(k) participants with balances were in plans reporting AE on Form 5500 in plan year 2024. In 2010 the figures were about 4% and 26% (Computed).
   - The BLS NCS shows AE covering 19% (2009) → 39% (2017) → 40% (2019) → 42% (2022) of private-industry savings-and-thrift participants.
   - Vanguard plans: 10% (2006) → 61% (2025) [recordkeeper/industry].
5. **Early SECURE 2.0 sec. 101 signal (new, Computed, preliminary).** In the Form 5500 data, the share of new 401(k) plans reporting AE has jumped:
   - By first plan year: plans that started in 2019 = 30% (PY2019), 2023 = 60% (PY2023), 2024 = 75% (PY2024), 2025 = 88% (PY2025, partial-year file).
   - Within the 2023 cohort, the share rose from 60% (PY2023) to 74% (PY2025, partial) when the mandate took effect.
   - This is consistent with the mandate binding, but it is not yet a causal estimate. State auto-IRA mandates and start-up tax credits push in the same direction, and the 2025 filings are incomplete.

---

## 1. Firm-level causal studies (US 401(k) and TSP)

### Takeaway
The quasi-experimental literature is unanimous that AE sharply raises participation at the firm where it applies. Participation reaches 85% to 95% under AE, versus roughly 30% to 70% under opt-in for new hires. But participants anchor on the default contribution rate and default fund. Newer work that follows workers over time and across jobs finds the net effect on lifetime saving is modest, concentrated among low earners, and sharply eroded by cash-outs and turnover.

### Cited findings
- **Madrian & Shea (QJE 2001).** Participation of the cohort hired under AE was 86%, versus 37% for the comparable pre-AE cohort at 3-15 months of tenure: "The 401(k) participation rate of the WINDOW cohort at 3-15 months of tenure was 37%. This is less than half the 86% participation rate of the NEW cohort." The company's overall participation before AE was 61%, which implies a steady-state gain of about 25 pp. Many AE participants stuck to both the 3% default rate and the money-market default ("default behavior"). — [Madrian & Shea, "The Power of Suggestion," NBER w7682 / QJE 116(4) 2001](https://www.nber.org/papers/w7682) (PDF p.10-12: https://www.nber.org/papers/w7682.pdf) [academic]
- **Choi, Laibson, Madrian & Metrick, "For Better or for Worse" (NBER w8651, 2001; in *Perspectives on the Economics of Aging*, 2004).** Three large firms. "401(k) participation rates at all three firms exceed 85%, but participants tend to anchor at a low default savings rate and in a conservative default investment vehicle... initially, about 80% of participants accept both the default savings rate (2% or 3%...) and the default investment fund... Even after three years, half of the plan participants subject to automatic enrollment continue to contribute at the default rate." The effects on asset accumulation "are roughly offsetting on average," but AE "does increase saving in the lower tail." — [NBER w8651](https://www.nber.org/papers/w8651) [academic]
- **Choi, Laibson, Madrian & Metrick, "Defined contribution pensions: plan rules, participant decisions, and the path of least resistance" (NBER w8655; Tax Policy and the Economy 2002).** "Employees often follow 'the path of least resistance.'" — [NBER w8655](https://www.nber.org/papers/w8655) [academic]
- **Beshears, Choi, Laibson & Madrian, "The Importance of Default Options for Retirement Saving Outcomes: Evidence from the United States" (NBER w12009, 2006; in *Social Security Policy in a Changing Environment*, 2009).** A review showing defaults affect participation, saving rates, asset allocation and post-retirement distributions. — [NBER w12009](https://www.nber.org/papers/w12009) [academic]
- **Thaler & Benartzi, SMarT (JPE 112(S1), 2004).** This is the prototype for automatic escalation. Published abstract (first implementation, four annual raises): "(1) a high proportion (78 percent) of those offered the plan joined, (2) the vast majority of those enrolled in the SMarT plan (80 percent) remained in it through the fourth pay raise, and (3) the average saving rates for SMarT program participants increased from 3.5 percent to 13.6 percent over the course of 40 months." Thaler's JEC testimony rounds take-up to "Over 80 percent" and adds the interim step: "from 3.5 percent to 9.4 percent" within 14 months. It was voluntary opt-in to escalation at a single firm. — [JPE abstract (NBER/Field Experiments copy via EconPapers)](https://econpapers.repec.org/paper/febnatura/00337.htm); [Thaler, JEC testimony, 10 Mar 2004](https://www.jec.senate.gov/archive/Documents/Hearings/thalertestimony10march2004.pdf), p.2; [JPE citation via IDEAS](https://ideas.repec.org/a/ucp/jpolec/v112y2004is1ps164-s187.html) [academic] *(gapB 2026-10-05: take-up corrected from "more than 80%" to 78% per the published abstract; full JPE PDF not retrievable, journals.uchicago.edu 403.)*
- **Beshears, Choi, Laibson, Madrian & Skimmyhorn, "Borrowing to Save? The Impact of Automatic Enrollment on Debt" (JF 77(1), Feb 2022, 403-447).** This is a US Army civilian TSP natural experiment (Army civilians auto-enrolled from Aug 2010). "Four years after hire, automatic enrollment increases cumulative contributions to the plan by 4.1% of annual salary," with "no significant change in credit scores (point estimate = +0.001 standard deviations), debt balances excluding auto debt and first mortgages (point estimate = -0.6% of annual salary), or adverse credit outcomes ... with the possible exception of increased first mortgage balances in foreclosure." The NBER version adds that auto-loan and first-mortgage increases "are economically and statistically significant in alternative specifications." **Net effect:** little offset through unsecured debt. Auto and mortgage debt (which also buy assets) may absorb part of the gain. — [Harvard DASH author copy](https://dash.harvard.edu/server/api/core/bitstreams/b4a74c35-1cef-4d0b-8d56-44e6ca07bc04/content); [NBER w25876](https://www.nber.org/papers/w25876) [academic]
- **Choukhmane, "Default Options and Retirement Saving Dynamics" (AER 115(11), Nov 2025, 3749-87).** Abstract: AE gains "in the short run (at 12 months)... are attenuated over the medium run (at 36 months). At this longer horizon, the average savings increases are modest, though AE significantly lowers inequality in savings." The model's switching cost is about $250. The 2019 working paper finds that UK workers auto-enrolled in their current job had participation and contribution rates "in their next employer's opt-in retirement savings plan [that] fall by 13 percentage points and 0.35% of income." In 86 US firms, "for each percentage point increase in the auto-enrollment default contribution rate, participation drops by nearly 1 percentage point." The median cumulative contributions of non-auto-enrolled workers "catch up" within 3 years. — [IDEAS/AER abstract](https://ideas.repec.org/a/aea/aecrev/v115y2025i11p3749-87.html); [2019 WP (NBER conf. paper)](https://conference.nber.org/conf_papers/f120839/f120839.pdf), pp.2-3, 7-8 [academic]. *Note: the specific numbers come from the 2019 version and may differ in the published AER version (not verified).*
- **Choi, Laibson, Cammarota, Lombardo & Beshears, "Smaller than We Thought? The Effect of Automatic Savings Policies" (NBER w32828, Aug 2024, rev. Nov 2024).** The study covers nine 401(k) plans.
  - Steady-state effects: "Steady-state saving rates increase by 0.6% of income due to automatic enrollment and 0.3% of income due to default autoescalation." Introducing both together gives 0.8%.
  - The most comprehensive effect is "smaller by 76%: 0.6 percentage points of income instead of 2.5."
  - Acceptance of the auto-escalation default is "43% on the first escalation date, 36% on the second date, and 29% on the third date" (21 firms).
  - "42% of 401(k) balances are cashed out upon departure from the firm."
  - Leakage among treated cohorts is 8 pp higher, because they separate with small balances.
  - With Vanguard-level take-up assumed, the effects rise only to 0.9% (escalation) and 1.1% (both).
  - The authors conclude that "the job transition moment is a key weakness in the U.S. retirement savings system." — [NBER w32828](https://www.nber.org/papers/w32828), pp.3-6 [academic]
- **Goda, Levy, Manchester, Sojourner & Tasoff, "Who is a passive saver under opt-in and auto-enrollment?" (JEBO 2020).** Under opt-in, financial literacy predicts contributions; under AE, present bias does. "A causal interpretation of the estimates suggests that auto-enrollment increases saving primarily among those with low financial literacy." — [IDEAS (HCEO WP 2019-050)](https://ideas.repec.org/p/hka/wpaper/2019-050.html) [academic]
- **Burke, Hung & Luoto (RAND WR-1162, Sept 2016, for DOL).** Vanguard data on about 95,000 new hires in 206 AE plans. "59 percent elect a different contribution rate, investment portfolio, or both within the first few years"; 57% change the contribution rate (about 2/3 up, 1/3 down) and 17% change investments. Participants are more likely to cut below the default in plans with default auto-escalation or a default above 3%. — [DOL-hosted RAND WP](http://www.dol.gov/sites/dolgov/files/EBSA/researchers/analysis/retirement/opting-out-of-retirement-plan-defaults.pdf) [academic]
- **Butrica & Karamcheva (CRR WP 2015, HRS 2006-2012).** Among older workers, automatically enrolled workers' accounts "receive, on average, $900 less in combined annual contributions" than voluntary enrollees' accounts, with contribution rates 1.6 pp lower. Employers of AE workers contribute more. — [CRR](https://crr.bc.edu/the-relationship-between-automatic-enrollment-and-dc-plan-contributions-evidence-from-a-national-survey-of-older-workers/) [academic]
- **Butrica & Karamcheva (BLS Monthly Labor Review, May 2015, NCS microdata 2009-10).**
  - Participation is "77.1 percent" in AE plans versus "67.3 percent" without AE.
  - AE plans offer a "maximum match rate that is 0.38 percentage point (11 percent) lower" (3.2% vs 3.5%).
  - There is "no evidence that total compensation costs statistically differ." — [MLR article](https://www.bls.gov/opub/mlr/2015/article/automatic-enrollment-employer-match-rates-and-employee-compensation-in-401k-plans.htm) [gov/academic]
- **Clark & Young, "Automatic enrollment: The power of the default" (Vanguard, Feb 2021) [recordkeeper/industry].** 813,918 new hires in 520 plans, hired 2017-2019. New-hire participation was 91% under AE versus 28% under voluntary enrollment; after three years 92% vs 29%; employees earning under $15,000: 82% vs 4%; 70% of the 520 plans paired AE with auto-escalation. — [401k Specialist, Mar 2021](https://401kspecialistmag.com/new-data-further-showcases-power-of-auto-enrollment/); [PLANSPONSOR, 8 Apr 2021](https://www.plansponsor.com/vanguard-report-underscores-power-automatic-enrollment/) (two independent trade-press summaries agree; the primary Vanguard PDF is still not retrievable, as vanguard.com research URLs redirect to a landing page). Auto-escalation acceptance in the Vanguard universe was 63%, 63% and 60% after one, two and three years, and 29%, 42% and 52% of new hires had left the firm by one, two and three years — as cited in [Choi et al. 2024, NBER w32828](https://www.nber.org/system/files/working_papers/w32828/w32828.pdf), pdf pp.5 and 7 (verified gapB 2026-10-05).

### Evidence verdict
- **Participation: strong, positive and persistent at the firm level.**
- **Contribution rates and wealth: moderate evidence of a positive but small long-run effect.** About +0.6% of income per year for AE and +0.3% for default auto-escalation, net of offsets. Gains are concentrated at the bottom of the distribution. The large early estimates do not hold up once turnover, catch-up by non-defaulted workers, vesting and cash-outs are accounted for.
- **Debt offset: little, apart from possible auto and mortgage debt** (one study, federal civilians).

### Gaps
- Few studies follow AE workers for 10 years or more, or across all their jobs, using administrative data. Choukhmane's UK cross-job estimate is the main one.
- No public US study yet uses W-2/IRS data to estimate AE's national effect on deferral rates. The Census-IRS linked-W-2 project (Choukhmane, Colmenares, O'Dea, Rothbaum & Schmidt, [NBER w32843](https://nber.org/system/files/working_papers/w32843/w32843.pdf)) studies distributional gaps (Black and Hispanic contribution rates "roughly 40% lower") but not AE adoption per se.
- I could not retrieve the full SMarT JPE paper or the Clark & Young 2021 PDF. SMarT numbers are now checked against the published abstract; Clark & Young numbers against two trade-press summaries and Choi et al. 2024 (gapB, 2026-10-05).

---

## 2. TSP evidence (federal, administrative) [gov]

### Takeaway
The TSP is the cleanest large-scale government example.
- **Participation.** AE for FERS new hires (Aug 2010, 3% default) lifted FERS participation from 84.7% (2009) to 89.9% (2014) and 96.2% (2025). Participation among workers with under 2 years of tenure jumped from 70.0% (2009) to 97.9% (2012). The old pattern where younger, lower-paid and Black employees participated least reversed or narrowed.
- **The 3% default had a cost.** FRTIB itself says the 3% default dragged average deferrals down: about 22-30% of contributors stayed below the 5% needed for the full match.
- **The 5% default worked.** After the default rose to 5% (Oct 2020), the share contributing below 5% fell from 30% (2019) to 11.15% (2025). The full-match rate passed 88% for the first time (Sept 2024), and average deferrals rose from 7.9% to 9.3%.
- **Opt-outs stay low:** about 1.6-2.2% of auto-enrollees, and "has not exceeded 4%" since 2010.

### Cited findings
- **Participation before and after AE.** "FERS participation was at a five-year high of 88.6% by the end of 2012... In 2009, the participation rate experienced a decline of nearly 3% to 84.7%." Among employees with under 2 years of tenure, participation was 81.5% (2008), 70.0% (2009), 82.1% (2010), 92.6% (2011) and 97.9% (2012). Among the lowest-paid quintile: 77.0% → 71.1% → 76.2% → 80.6% → 81.0%. — [FRTIB, TSP Participant Behavior and Demographics 2008-2012](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-Demographics-2012.pdf), pp.2-4, table "Annual FERS Participation Rates by Age, Tenure, and Salary Quintile"
- "FERS participation was at a five-year high of 89.9% by the end of 2014." Among employees with under 2 years of tenure, participation was "98.4% - the highest rate of participation among all tenure bands." Lowest quintile: "growing from 76.2% in 2010 to 85.8% in 2014." Black employees: 79.6% (2010) → 83.7% (2014). Opt-outs: "since the implementation of automatic enrollment, the opt-out rate has not exceeded 4% of participants." — [FRTIB PBD 2014](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-Demographics-2014.pdf), pp.4-6, 15
- **Aggregate FERS participation 2008-2014 read from chart images (gapB, 2026-10-05; approximate).** PBD 2014 Figure 1 (p.4) prints data labels on the bars, read from the rendered image: 86.6% (2010), 88.2% (2011), 89.0% (2012), 89.6% (2013), 89.9% (2014). PBD 2012 Figure 1 (report p.3, pdf p.4) has no labels; measured by pixel against the axis ticks: about 87.4% (2008), 84.7% (2009), 86.6% (2010), 88.2% (2011), 88.6% (2012). The pixel method reproduces the two values stated in the text (84.7%, 88.6%) within 0.02 pp, and the text notes "an almost 2% gain in overall participation in 2010". The 2012 value differs between reports (88.6% in PBD 2012, 89.0% in PBD 2014); PBD 2014 Table 1 (p.6) also revises under-2-years-tenure participation for 2012 from 97.9% to 98.2%.
- **The 3% default lowered average deferrals.** The FERS deferral rate "dropping slightly to 8.1% in 2014," below "the 9.5% FERS deferral rates of the mid-2000s." AE "appears to have had an overall dampening effect on deferral rates." 25.6% were contributing below 5% (2014). — same, pp.7-8
- **2015-2019.** Participation was 91.1% (2015), 91.9% (2016), 92.6% (2017), 93.3% (2018) and 93.8% (2019). "Approximately 2.2% of auto-enrolled participants opting out." "30% of participants are not receiving the full matching contribution as they are contributing less than 5%. In October 2020, FRTIB will be increasing the default level to 5%." — [FRTIB PBD 2015-2019](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2015-2019.pdf), pp.4-6
- **2017-2021.** Participation was 94.6% (2020) and 95.5% (2021). "Approximately 1.6% of auto-enrolled participants opting out." 79% of auto-enrollees made some active change, and the 21% who made none are "mostly in the lowest salary quintiles." With the 5% default, "21.5% of participants are not receiving the full matching contribution... a decrease of 5 percentage points from 2020." Average deferral: 7.9% (2017-19) → 8.1% (2020) → 8.4% (2021). The authors attribute the rise to "the increase in the default deferral rate in 2020 from 3% to 5%." — [FRTIB PBD 2017-2021](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2017-2021.pdf), pp.4-6, 13
- **2018-2022.** Participation was 95.1% (2022). "13.8% of participants are not receiving the full matching contribution... a decrease of 7.7 percentage points from 2021." — [FRTIB PBD 2018-2022](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2018-2022.pdf), pp.4-6
- **2019-2023.** Participation was 95.9% (2023), "leveling off at around 95%." Each salary quintile had "2% or fewer participants opting out" (2023 enrollees, first 90 days). 12.4% were below 5%. Deferral rate 9.1%. *Methodology break: 2022 recordkeeper change; "year over year comparison is advised against" for AE-status data.* — [FRTIB PBD 2019-2023](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2019-2023.pdf), pp.1, 4-7
- **2020-2024 and 2021-2025** (published as appendices to the TSP Annual Report to Congress).
  - Participation was 95.9% (2024) and 96.2% (2025), with "rates began leveling off at around 96%."
  - Opt-outs were "2.2% or fewer" (2024) and "1.7% or fewer" (2025) per salary quintile.
  - The share below 5% was 11.31% (2024) and 11.15% (2025). Deferral rate 9.2% (2024) and 9.3% (2025).
  - The FERS lowest-highest quintile gap is 4.5 pp (2025).
  - Loans: 9.5% of FERS participants used a loan in 2025, versus 7.0% in 2021, and hardship withdrawals rose from 4.0% to 4.9%. This is leakage that offsets part of the AE gain.
  - Sources: [TSP Annual Report (June 30, 2025)](https://www.frtib.gov/pdf/reading-room/congress/annual/TSP-Annual-Report_2024.pdf), pp.3-9; [TSP Annual Report (June 30, 2026)](https://www.frtib.gov/pdf/reading-room/congress/annual/TSP-Annual-Report_2025.pdf), pp.3-9
- **Full-match rate after the 5% default.** "FERS full match rate reached 88.1 percent in September [2024], marking its first-ever rise above 88 percent... since the policy of enrolling participants at five percent of their salary started in October 2020, the overall matching rate has shown a steady increase." — [FRTIB Board minutes, Oct 2024](https://www.frtib.gov/meeting_minutes/2024/2024Oct.pdf), p.1-2
- **Army civilians** (TSP natural experiment): +4.1% of salary in cumulative contributions after 4 years; see section 1.

### Evidence verdict
- **Participation: strong and positive.** The before/after jump for new hires is large, has persisted for 15 years, and is concentrated among young, low-paid and less-educated workers.
- **Raising the default from 3% to 5%: strong and positive.** The share of contributors below the full match fell by almost two-thirds (30% → 11%) without any visible rise in opt-outs (about 2%).
- **Caveats:**
  - The aggregate series is descriptive, not causal: 2009 was a recession trough, and definitions shift between reports.
  - Loan and hardship use rose to record highs in 2024-25.

### Gaps
- The FERS aggregate participation rates for 2008, 2010, 2011 and 2013 appear only in chart images; gapB read them from the rendered charts (above and Table A). Treat them as approximate; the 2012 value was revised between reports (88.6% → 89.0%).
- The reports switched from OPM-matched data (through about 2015) to TSP records, and the recordkeeper changed in 2022. Treat the series as having breaks.
- The TSP reports do not publish a causal estimate of the 5% default; the Army/TSP 5% default has no published study yet (not found).

---

## 3. National and aggregate evidence

### Takeaway
- AE has spread steadily since PPA 2006, but it still covers a minority of plans and a bit over half of participants.
  - BLS NCS: the share of private-industry savings-and-thrift participants whose plan has AE went from 19% (Mar 2009) to 39% (2017), 40% (2019) and 42% (2022).
  - Form 5500 (Computed): 401(k) plans reporting AE rose from about 4% (PY2010) to 31% (PY2024). Their share of 401(k) participants with balances rose from 26% to 54%.
- National participation has moved much less than firm studies would imply. The NCS DC **access** rate rose from 59% (2010) to 70% (2024-2026), and overall retirement take-up was 72-73% in 2025-26.
  - AE mostly applies to new hires.
  - Plans adopting AE are concentrated among large employers who already had high participation.
- In the UK, by contrast, the 2012 employer mandate moved national private-sector participation of eligible employees from 42% (2012) to 89% (2024).

### Cited findings
- **BLS NCS [gov].**
  - "Among all private industry workers who participated in savings and thrift plans, 19 percent had automatic enrollment" (March 2009). The figure was 25% in establishments with 100+ workers versus 9% in those with 1-99. — [BLS TED, 15 Sep 2010](https://www.bls.gov/opub/ted/2010/ted_20100915.htm)
  - 39% in 2017 and 42% in 2022 (52% "did not have automatic enrollment"). 2022 breakdowns: 1-49 workers 34%, 500+ 46%, service occupations 24%, union 51%. Median default 3% (10th pct 2%, 90th pct 6%). 26% had automatic escalation. — [BLS fact sheet, "Automatic enrollment in savings and thrift defined contribution plans," Apr 13 2023](https://www.bls.gov/ebs/factsheets/automatic-enrollment-in-savings-and-thrift-defined-contribution-plans.htm)
  - "Forty percent of private industry workers participating in savings and thrift plans had an automatic enrollment feature, compared with 28 percent of state and local government workers" (2019). Median default 3%. — [BLS Beyond the Numbers vol.12, Jan 10 2023](https://www.bls.gov/opub/btn/volume-12/how-do-retirement-plans-for-private-industry-and-state-and-local-government-workers-compare.htm)
  - DC access, private industry (series NBU22000000000000028312, BLS API): 59% (2010), 58% (2011), 59% (2012), 59% (2013), 60% (2014), 61% (2015), 62% (2016), 62% (2017), 64% (2018), 64% (2019), 64% (2020), 65% (2021), 66% (2022), 67% (2023), 70% (2024), 70% (2025), 70% (2026). — [BLS data series NBU22000000000000028312](https://data.bls.gov/timeseries/NBU22000000000000028312)
  - All retirement plans, private industry, March 2026: access 72%, participation 52%, take-up 72%. — [BLS Employee Benefits, Table 1](https://www.bls.gov/news.release/ebs2.t01.htm). March 2025: participation 53%, take-up 73%. — [BLS ebs2 Sept 25 2025](https://www.bls.gov/news.release/archives/ebs2_09252025.htm)
- **CRS (Form 5500, plan year 2021) [gov].** "Among the 718,735 DC plans (with 114.9 million participants)... 16.5% had automatic enrollment and 37.1% of participants were in plans that had automatic enrollment." 15.7% of plans with under 500 participants had AE versus 39.7% of plans with 500+. Among plans with effective years 2009-2013, fewer than 10% had AE, versus 36.2% (2020) and 37.3% (2021). — [CRS IF12756, Sept 5 2024](https://www.everycrsreport.com/files/2024-09-05_IF12756_4b87c2c47bf47264f81aa0f1bfc93e12dc2e65aa.pdf) (copy in raw/)
- **Computed (Form 5500 + 5500-SF, DOL EBSA "Latest" research files).**
  - Method:
    - Plans are de-duplicated by EIN and plan number.
    - A DC plan is any plan with a pension feature code starting "2"; a 401(k) plan has code 2J; AE means code 2S (automatic enrollment).
    - Participants = participants with account balances at end of year.
    - Script: `raw/autoenroll/autoenroll_form5500.py`.
    - Sources: `https://www.askebsa.dol.gov/FOIA%20Files/<YEAR>/Latest/F_5500_<YEAR>_Latest.zip` and `F_5500_SF_<YEAR>_Latest.zip` (downloaded 2026-10-04).
  - The PY2025 file is partial (filings run through Oct 2026) and under-represents large plans.
  - Results are in the chart-ready tables below. My PY2019 and PY2023 figures bracket CRS's PY2021 figures (16.5% of plans, 37.1% of participants), which is a consistency check.
- **GAO-10-31 (Oct 2009) [gov].**
  - "The percentage of plans with automatic enrollment policies increased from about 1 percent in 2004 to more than 16 percent in 2009" (Fidelity data). Vanguard: 8% (June 2006) → 19% (Dec 2008).
  - About 40% of large plans versus 14% of small plans had AE by March 2009.
  - "Low default contribution rates and an apparent lag in the adoption of automatic escalation policies raise questions about the adequacy of long-term savings rates."
  - AE "may not be suitable for all plan sponsors, such as those with a high-turnover workforce."
  - [GAO-10-31 (Senate Aging copy)](https://www.aging.senate.gov/download/gao-retirement-saving-report?download=1), pp. summary, 19-21; [gao.gov product page](https://www.gao.gov/products/gao-10-31)
- **JCT score of SECURE 2.0 sec. 101 [gov].** "Expanding automatic enrollment in retirement plans": revenue effect −$403M (FY2025), −$643M (FY2026), −$1,708M for FY2023-27 and **−$5,089M for FY2023-32**. The revenue loss reflects the additional tax-deferred contributions JCT expects. — [JCT, JCX-21-22, Dec 22 2022 (copy hosted by Sikich)](https://www.sikich.com/wp-content/uploads/2022/12/Pension-and-Other-Items-in-Year-end-Omnibus-Spending-Legislation-JCT-Revenue-Effects-of-HR-2617.pdf), Division T, Title I, item 1
- **UK auto-enrolment (international comparison).**
  - DWP official statistics (ASHE), participation of eligible employees:
    - Private sector: 46% (2009), 42% (2012), 63% (2014), 81% (2017), 86% (2019-2023), 89% (2024).
    - Public sector: 88% (2012) → 92% (2024).
    - Overall: 55% (2012) → 89% (2024).
  - "The number of active savers who stop saving each quarter as a proportion of total active savers has been stable over multiple years at under 1%."
  - [DWP, "Workplace pension participation and saving trends of eligible employees: 2009 to 2024," 31 July 2025](https://www.gov.uk/government/statistics/workplace-pension-participation-and-savings-trends-2009-to-2024), Table 1.1 (xlsx) [gov, UK]
  - Cribb & Emmerson, National Tax Journal 74(2), June 2021: AE at small employers "increased pension participation by 44 percentage points, reaching 70 percent — still substantially lower than the 90 percent rate among those working for the largest employers." Their JPubE 2020 paper finds "a 37 percentage point increase for medium and large employers." — [NTJ paper (Georgetown CRI copy)](https://cri.georgetown.edu/wp-content/uploads/2025/10/16.-What-can-we-learn-about-automatic-enrollment-into-pensions-from-small-employers.pdf), pp.377-378 [academic]
  - Per Choi et al. (2024, fn.4), UK opt-out rates did not rise significantly as minimum contributions went from 2% to 5% to 8% of earnings.

### Evidence verdict
- **Diffusion of AE: strong evidence that it has spread** (NCS, Form 5500, CRS, GAO all agree). It is still a minority of plans, it is concentrated in large plans, and it typically covers only new hires.
- **Effect on national participation and access: moderate.** DC access and participant coverage within AE plans rose, but the aggregate US take-up of about 72-73% is far from the 90%+ seen inside AE plans.
- **The UK shows that a universal employer mandate moves national participation** (private sector 42% → 89%). The US approach (voluntary AE plus a new-plan-only mandate) is much slower.

### Gaps
- I could not retrieve the BLS NCS DC-only participation and take-up time series. The BLS API daily limit was hit; the take-up series ID is not confirmed. The DC access series ID is confirmed.
- I found no Treasury OTA, CBO or SSA W-2 study tracking deferral participation over time that attributes trends to AE. The SSA Research Note 2008-03 covers deferrals only for 1990-2001 (not used).
- No GAO report since 2009 specifically evaluates AE outcomes (not found).

---

## 4. Plan adoption and plan-level outcomes over time [recordkeeper/industry], plus early SECURE 2.0 evidence

### Takeaway
- **Vanguard.** AE adoption rose from 10% of plans (2006) to 61% (2024-2025), including 79% of plans with 1,000+ participants.
- **Participation gap.** AE plans had 93-94% participant-weighted participation in 2021-2025, versus 64-66% in voluntary plans. The gap is largest for low earners (80% vs 16% under $15k) and young workers (90% vs 24% under age 25).
- **Default rates are rising.** 62% of AE plans default at 4% or more (versus 27% in 2005), and 71% have default auto-increase. Even so, 32% still default at 3%.
- **Early SECURE 2.0 evidence.** New 401(k) plans are now overwhelmingly AE plans (Computed, Form 5500).

### Cited findings
- Vanguard, *How America Saves 2026* (2025 data):
  - "By year-end 2025, 61% of Vanguard defined contribution (DC) plans had adopted automatic enrollment, including 79% of plans with at least 1,000 participants."
  - "More than 70% of automatic enrollment plans used automatic annual deferral rate increases."
  - "62% of plans now defaulting employees at a deferral rate of 4% or higher, compared with 43% of plans in 2015."
  - "Plans with automatic enrollment had a 94% participation rate, compared with 64% among voluntary enrollment plans."
  - 93% of AE plans versus 50% of voluntary plans had participation of 80% or more.
  - Average deferral 7.7% (AE) versus 7.5% (voluntary).
  - When offered, 25% of participants in voluntary-enrollment plans used the annual-increase feature.
  - In 2025, 2% of participants stopped contributing and 8% cut their rate.
  - [HAS 2026](https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf), pp.19, 26-41 (Figures 15, 18, 19, 24, 27, 28, 36) [recordkeeper/industry]
- **PSCA annual surveys of 401(k) plans [recordkeeper/industry] (re-checked by gapB, 2026-10-05; psca.org, napa-net.org and asppa-net.org all return 403/Cloudflare blocks, so trade press and a PSCA press release mirrored on BenefitsLink were used).**
  - *Correction:* the earlier bullet attributed "60% default at 4%+" and "nearly 7 in 10 AE plans include auto-escalation" to PSCA's 68th survey. The March 2024 PSCA news item ("Good News: Automatic Enrollment Defaults Trending Higher") was reposting **Vanguard's How America Saves 2024 preview** (2023 data), not a PSCA survey. Vanguard's own figures: plans with AE 54%, 56%, 58%, 59%, 61% (2020-2024); AE plans with automatic annual increases 69% in every year 2020-2024; "Sixty-one percent of plans now default employees at a deferral rate of 4% or higher, up from 39% of plans in 2014" (about 60% in 2023, read from Figure 21). — [Vanguard, How America Saves 2025](https://corporate.vanguard.com/content/dam/corp/research/pdf/how_america_saves_report_2025.pdf), pdf pp.5, 9, 29 (Figures 17, 18, 21).
  - *Older PSCA figure, not current:* "3% remains the most common default (36.4% of plans)" with "more than half" defaulting above 3% traces to an older PSCA survey (a search extract places it in the 60th survey, 2016 plan year); **not verified**. PSCA's 62nd survey (2018 plan year): "more than 60 percent of plans with automatic enrollment used a default deferral rate above 3 percent"; plans defaulting at 6% rose "from 23.8% in 2017 to 29.7% in 2018"; "Fully 80% of automatic enrollment plans include features that facilitate an increase in the savings rate." — [401k Specialist](https://401kspecialistmag.com/higher-auto-defaults-dominate-in-many-dc-plans/) (verified against trade press).
  - PSCA 2021 plan year: "58.8% of the 557 plans in its survey had automatic enrollment" — [CRS IF12756 (Sept 2024)](https://www.everycrsreport.com/files/2024-09-05_IF12756_4b87c2c47bf47264f81aa0f1bfc93e12dc2e65aa.html) (verified).
  - PSCA 67th survey (2023 plan year, 709 plans): 64% of plans use AE; "Thirteen percent of plans automatically reenroll nonparticipants annually – up from 4 percent of plans 10 years ago"; 86.9% of eligible employees made deferrals. — [PSCA press release, 18 Dec 2024 (BenefitsLink copy)](https://benefitslink.com/articles/psca-survey-results-20241218.pdf) (verified; saved at `raw/gapB/`); the 64% AE share from [401k Specialist, 19 Dec 2024](https://401kspecialistmag.com/top-10-highlights-from-pscas-newest-survey-of-401k-plans/) (verified against trade press).
  - PSCA 68th survey (2024 plan year, 755 plans): 64.3% of plans use AE, but only 36.2% of plans with 1-49 participants (28.8% in 2021); 87.4% of eligible employees deferred. **Not verified**: these come from search-engine extracts of psca.org/napa-net.org pages that could not be opened. The extracts also disagree on auto-escalation (41.7% vs "75%" of AE plans), so that figure should not be used.
- T. Rowe Price reported AE adoption in its 401(k) plans of 22% (2005) → 37% (2018) → 73% (Nov 2020), via search summary, **not verified**. — [T. Rowe Price, "Auto-enrollment's long-term effect on retirement saving," 2020](https://www.troweprice.com/content/dam/retirement-plan-services/pdfs/insights/Auto-Enroll-2020-White-Paper.pdf) [recordkeeper/industry]
- **Early SECURE 2.0 sec. 101 evidence (Computed, Form 5500).** Share of 401(k) plans reporting AE (code 2S) by plan effective year, at their first and later plan-year filings:
  - Plans effective 2019: 30.1% in PY2019.
  - Plans effective 2022 (pre-mandate cutoff): 47.9% (PY2023), 47.9% (PY2024), 52.2% (PY2025 partial).
  - Plans effective 2023 (mandate applies from PY2025 if not exempt): 60.0% (PY2023), 62.4% (PY2024), **74.1% (PY2025 partial)**.
  - Plans effective 2024: 75.0% (PY2024), 83.5% (PY2025 partial).
  - Plans effective 2025: 87.9% (PY2025 partial).
  - **Interpretation.** The jump within the 2023 cohort between PY2024 and PY2025 (+11.7 pp), with only +4.3 pp for the exempt 2022 cohort, is the first quantitative sign that the mandate is binding.
  - **Limitations.** Remaining non-AE new plans are likely exempt: 10 or fewer employees, businesses under 3 years old, or plans effective before Dec 29, 2022. The PY2025 file is partial (early filers), and the 2S code is self-reported.
  - The data cannot yet show participation effects for these plans. Participant counts in new plans are small, about 0.6-1.0 million participants with balances per cohort.

### Evidence verdict
- **Plan-level gap: strong.** Recordkeeper data consistently show AE plans with 25-30 pp higher participation. These are cross-sectional comparisons and partly reflect which employers adopt AE.
- **SECURE 2.0 mandate: early, weak-to-moderate evidence that it is being complied with** (rising share of new plans with AE). There is no evidence yet on its effect on saving.

### Gaps
- No government or academic evaluation of SECURE 2.0 sec. 101 exists yet. The PY2025 Form 5500 file will be more complete in 2027.
- No public data on default rates or auto-escalation in new plans (Form 5500 does not record them).
- PSCA and Fidelity primary reports were not retrievable (403). PSCA 67th-survey figures were verified from the PSCA press release on BenefitsLink; 68th-survey figures remain unverified (gapB, 2026-10-05).

---

## Chart-ready series

### A. TSP FERS participation rate (contributing FERS participants as % of eligible) [gov]
| Year | FERS participation % | Source |
|---|---|---|
| 2008 | ~87.4 (approx., read from chart) | [FRTIB PBD 2012](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-Demographics-2012.pdf), Figure 1, pdf p.4 (pixel-measured; text: 2009 fell "nearly 3%") |
| 2009 | 84.7 | [FRTIB PBD 2012, p.2](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-Demographics-2012.pdf) |
| 2010 | 86.6 (approx., read from chart label) | [FRTIB PBD 2014](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-Demographics-2014.pdf), Figure 1, p.4 (bar label); PBD 2012 Figure 1 pixel estimate 86.6 |
| 2011 | 88.2 (approx., read from chart label) | same; PBD 2012 pixel estimate 88.2 |
| 2012 | 88.6 | [FRTIB PBD 2012, p.2](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-Demographics-2012.pdf) (PBD 2014 Figure 1 label shows a revised 89.0) |
| 2013 | 89.6 (approx., read from chart label) | [FRTIB PBD 2014](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-Demographics-2014.pdf), Figure 1, p.4 |
| 2014 | 89.9 | [FRTIB PBD 2014, p.4](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-Demographics-2014.pdf) |
| 2015 | 91.1 | [FRTIB PBD 2015-2019, p.4](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2015-2019.pdf) |
| 2016 | 91.9 | same |
| 2017 | 92.6 | same |
| 2018 | 93.3 | same |
| 2019 | 93.8 | same |
| 2020 | 94.6 | [FRTIB PBD 2017-2021, p.4](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2017-2021.pdf) |
| 2021 | 95.5 | same |
| 2022 | 95.1 | [FRTIB PBD 2019-2023, p.1](https://www.frtib.gov/pdf/reading-room/SurveysPart/behavior/Participant-Behavior-and-Demographics-2019-2023.pdf) |
| 2023 | 95.9 | same |
| 2024 | 95.9 | [TSP Annual Report 2026 (2021-25 analysis), p.3](https://www.frtib.gov/pdf/reading-room/congress/annual/TSP-Annual-Report_2025.pdf) |
| 2025 | 96.2 | same |
Event markers: AE at 3% for new hires in Aug 2010; default fund changed from G to L Fund in Sept 2015; default raised to 5% on Oct 1, 2020. Series breaks: OPM-matched data through 2014-15, then TSP-record salary proxy; recordkeeper change in 2022.

### B. TSP FERS participation, tenure under 2 years and lowest-paid quintile [gov]
| Year | Tenure <2 yrs % | Lowest-paid quintile % | Source |
|---|---|---|---|
| 2008 | 81.5 | 77.0 | FRTIB PBD 2012 table |
| 2009 | 70.0 | 71.1 | same |
| 2010 | 82.1 | 76.2 | same |
| 2011 | 92.6 | 80.6 | same |
| 2012 | 97.9 | 81.0 | same |
| 2013 | 98.3 | 84.3 | FRTIB PBD 2014 Table 1 |
| 2014 | 98.4 | 85.8 | same |
| 2019 | n/a | 92.9 | FRTIB PBD 2019-2023 Table 1 |
| 2023 | n/a | 93.6 | same |
| 2025 | n/a | 93.8 | TSP Annual Report 2026 Table 1 |
Note: the 2014 report's quintile values for 2012 (82.7) differ slightly from the 2012 report (81.0) because of re-matching; both are as published.

### C. TSP: % of FERS contributors deferring less than 5% (below full match) and average deferral rate [gov]
| Year | % below 5% | Avg FERS deferral % | Source |
|---|---|---|---|
| 2012 | 22 | 8.5 | FRTIB PBD 2012 pp.5-6 |
| 2014 | 25.6 | 8.1 | FRTIB PBD 2014 p.7-8 |
| 2019 | 30 | 7.9 | FRTIB PBD 2015-2019 p.6; PBD 2019-2023 p.1 |
| 2020 | 26.5 (Computed: 21.5 + 5.0, per "decrease of 5 percentage points from 2020") | 8.1 | FRTIB PBD 2017-2021 p.6 |
| 2021 | 21.5 | 8.4 | same |
| 2022 | 13.8 | 8.9 | FRTIB PBD 2018-2022 p.6 |
| 2023 | 12.4 | 9.1 | FRTIB PBD 2019-2023 p.7 |
| 2024 | 11.31 | 9.2 | TSP Annual Report 2025 (PBD 2020-24) |
| 2025 | 11.15 | 9.3 | TSP Annual Report 2026 (PBD 2021-25) |

### D. BLS NCS: % of private-industry savings-and-thrift participants whose plan has AE [gov]
| Year (March) | % with AE | Source |
|---|---|---|
| 2009 | 19 | [BLS TED 2010-09-15](https://www.bls.gov/opub/ted/2010/ted_20100915.htm) |
| 2017 | 39 | [BLS AE fact sheet (2023)](https://www.bls.gov/ebs/factsheets/automatic-enrollment-in-savings-and-thrift-defined-contribution-plans.htm) |
| 2019 | 40 | [BLS BTN vol.12](https://www.bls.gov/opub/btn/volume-12/how-do-retirement-plans-for-private-industry-and-state-and-local-government-workers-compare.htm) |
| 2022 | 42 | [BLS AE fact sheet (2023)](https://www.bls.gov/ebs/factsheets/automatic-enrollment-in-savings-and-thrift-defined-contribution-plans.htm) |
(Butrica & Karamcheva's NCS microdata sample for 2009-10: 14.5%.)

### E. BLS NCS: % of private-industry workers with access to a DC plan [gov]
| Year | % | Source |
|---|---|---|
| 2010 | 59 | [BLS series NBU22000000000000028312](https://data.bls.gov/timeseries/NBU22000000000000028312) |
| 2012 | 59 | same |
| 2014 | 60 | same |
| 2016 | 62 | same |
| 2018 | 64 | same |
| 2020 | 64 | same |
| 2022 | 66 | same |
| 2023 | 67 | same |
| 2024 | 70 | same |
| 2025 | 70 | same |
| 2026 | 70 | same |

### F. Form 5500 (Computed): 401(k) plans reporting AE (code 2S), private sector [gov data, Computed]
| Plan year | % of 401(k) plans with AE | % of 401(k) participants (with balances) in AE plans | % of 401(k) plans with 100+ participants with AE | % of all DC plans with AE | Source |
|---|---|---|---|---|---|
| 2010 | 3.9 | 26.3 | 19.8 | 3.2 | DOL EBSA Form 5500 + SF Latest files; `raw/autoenroll/form5500_autoenroll_share.csv` |
| 2015 | 6.9 | 39.4 | 30.4 | 6.0 | same |
| 2019 | 13.6 | 46.7 | 37.4 | 12.3 | same |
| 2021 (CRS) | n/a | n/a | n/a | 16.5 (37.1% of participants) | [CRS IF12756](https://www.everycrsreport.com/files/2024-09-05_IF12756_4b87c2c47bf47264f81aa0f1bfc93e12dc2e65aa.pdf) |
| 2023 | 26.2 | 51.9 | 43.0 | 24.2 | Form 5500 Computed |
| 2024 | 31.4 | 53.5 | 44.6 | 29.3 | same |
| 2025 (partial file, early filers) | 41.8 | 51.5 | 48.5 | 39.9 | same; not comparable, incomplete |

### G. Form 5500 (Computed): % of new 401(k) plans with AE in their first plan year (SECURE 2.0 sec. 101 signal)
| Plan effective year | % with AE in first plan year | Same cohort in PY2025 (partial) | Source |
|---|---|---|---|
| 2010 | 5.2 | n/a | Form 5500 Computed |
| 2015 | 12.2 | n/a | same |
| 2019 | 30.1 | n/a | same |
| 2022 | 47.9 (PY2023 filing; first-year file not pulled) | 52.2 | same |
| 2023 | 60.0 | 74.1 | same |
| 2024 | 75.0 | 83.5 | same |
| 2025 | 87.9 (partial) | 87.9 | same |

### H. Vanguard: % of plans with AE [recordkeeper/industry]
| Year | % plans | Source |
|---|---|---|
| 2006 | 10 | [Vanguard HAS 2026, Fig. 15](https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf) (values read from chart labels) |
| 2007 | 15 | same |
| 2008 | 20 | same |
| 2009 | 24 | same |
| 2010 | 27 | same |
| 2011 | 29 | same |
| 2012 | 32 | same |
| 2013 | 34 | same |
| 2014 | 36 | same |
| 2015 | 41 | same |
| 2016 | 45 | same |
| 2017 | 46 | same |
| 2018 | 48 | same |
| 2019 | 50 | same |
| 2020 | 54 | same |
| 2021 | 56 | same (table p.19) |
| 2022 | 58 | same |
| 2023 | 59 | same |
| 2024 | 61 | same |
| 2025 | 61 | same |
Caution: the chart has 20 labels for 2006-2025, and I assigned them in order. The 2021-2025 values match the report's table. GAO-10-31 reports Vanguard at 19% in Dec 2008 (versus 20% here).

### I. Vanguard: participant-weighted participation rate, AE vs voluntary plans [recordkeeper/industry]
| Year | AE plans % | Voluntary plans % | All % | Source |
|---|---|---|---|---|
| 2021 | 93 | 64 | 82 | HAS 2026 p.19 |
| 2022 | 94 | 64 | 82 | same |
| 2023 | 94 | 66 | 82 | same |
| 2024 | 94 | 64 | 82 | same |
| 2025 | 94 | 64 | 83 | same |
Comparison points: BLS NCS microdata for 2009-10 shows 77.1% (AE) vs 67.3% (no AE) ([MLR 2015](https://www.bls.gov/opub/mlr/2015/article/automatic-enrollment-employer-match-rates-and-employee-compensation-in-401k-plans.htm)). Madrian-Shea firm: 86% vs 37% (new hires).

### J. Vanguard 2025: participation by income, AE vs voluntary [recordkeeper/industry]
| Income | Voluntary % | AE % |
|---|---|---|
| <$15k | 16 | 80 |
| $15-30k | 26 | 89 |
| $30-50k | 53 | 91 |
| $50-75k | 72 | 94 |
| $75-100k | 76 | 95 |
| $100-150k | 80 | 96 |
| $150k+ | 89 | 98 |
Source: [HAS 2026, Fig. 27](https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf).

### K. Vanguard: AE plans' default deferral rate [recordkeeper/industry]
| Year | % AE plans defaulting at ≤3% | % at 4%+ | % at 6%+ | Source |
|---|---|---|---|---|
| 2005 | 73 | 27 | n/a | HAS 2026 Fig.19 |
| 2015 | 57 | 43 | n/a | same |
| 2016 | 52 | 48 | 20 | HAS 2026 Fig.18 (≤3% = 1%+2%+3% rows) |
| 2020 | 43 | 57 | 26 | same |
| 2025 | 38 | 62 | 31 | same |

### L. UK: workplace pension participation of eligible employees (AE mandate staged in from Oct 2012) [gov, UK]
| Year | Private sector % | Public sector % | Overall % | Source |
|---|---|---|---|---|
| 2009 | 46 | 89 | 58 | [DWP 2009-2024, Table 1.1](https://www.gov.uk/government/statistics/workplace-pension-participation-and-savings-trends-2009-to-2024) |
| 2012 | 42 | 88 | 55 | same |
| 2013 | 47 | 90 | 59 | same |
| 2014 | 63 | 92 | 71 | same |
| 2015 | 70 | 91 | 75 | same |
| 2016 | 72 | 91 | 77 | same |
| 2017 | 81 | 92 | 84 | same |
| 2018 | 85 | 93 | 87 | same |
| 2019 | 86 | 92 | 88 | same |
| 2020 | 86 | 93 | 88 | same |
| 2021 | 86 | 93 | 88 | same |
| 2022 | 86 | 92 | 88 | same |
| 2023 | 86 | 93 | 88 | same |
| 2024 | 89 | 92 | 89 | same |

### M. Long-run net saving effects of automatic policies (academic estimates)
| Study | Policy | Short-run / naive effect | Long-run / net effect |
|---|---|---|---|
| Choi, Laibson, Cammarota, Lombardo, Beshears 2024 (NBER w32828) | AE | 2.5% of income (naive, average across policies) | +0.6% of income steady state |
| same | Default auto-escalation on top of AE | n/a | +0.3% of income |
| same | AE + AutoEsc together | n/a | +0.8% of income (1.1% at Vanguard take-up) |
| Beshears et al. 2022 (JF), Army civilians | TSP AE 3% | n/a | +4.1% of salary cumulative after 4 yrs; non-auto, non-mortgage debt −0.6% of salary (n.s.) |
| Choukhmane 2025 (AER) | AE (US 401(k), UK) | Large at 12 months | "Attenuated" at 36 months; next-job participation −13 pp (UK, 2019 WP) |
| Thaler & Benartzi 2004 | SMarT (opt-in escalation) | 3.5% → 9.4% (14 months) | 13.6% after ~40 months |
| Auto-escalation acceptance rates | Choi et al. 2024 (21 firms): 43/36/29% at escalations 1/2/3; Vanguard (Clark & Young 2021): 63/63/60%; OregonSaves (Zhong 2021, cited in Choi et al.): 47% | | |
