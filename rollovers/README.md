# DC-to-IRA rollovers over time: is the share rising or falling?

Question (Richard, 2026-10-06): it's often said most DC assets are rolled to IRAs at retirement. Is that share increasing or decreasing, and what is the best data?

Built on existing work: `notes/rollovers.md` (published sources), `irs/` (IRS SOI tables, June 2026 vintage), `dc_stay/` (TSP, Form 5500, SCF past-job plans), report Section 7 (Vanguard 60+ cohorts). Nothing in the report or CLAUDE.md was changed.

Re-run: `python rollovers/scripts/build.py` from `retirement-withdrawals/`.

## Short answer

Most retirement-age DC dollars still end up in IRAs, but the share has been **falling for about 15 years**, and the money that stays is staying in the employer plan, not being cashed out. Two independent measures agree:

1. **Dollars, all ages (administrative):** rollovers into traditional IRAs equalled 93-99% of everything leaving DC plans in 1999-2007, 88-92% in 2008-2015, and 75-82% in 2019-2023.
2. **People and dollars at retirement age (recordkeeper):** among Vanguard participants 60+ who left their job, the share of assets rolled to an IRA fell cohort by cohort from about 65% (2011-2013 leavers) to 45-49% (2019-2020 leavers), while the share left in the plan rose from 16% to 46%. Cash stayed at ~5% of assets.

Government proxies for the flip side all rise: TSP one-year retention 57-61% (FY15-16) to 67-71% (FY24-26); Form 5500 separated participants per 100 actives 23.9 (2014) to 29.1 (2023); SCF retired 60-74 households with past-job plan money 16-19% (2004-07) to 26-29% (2019-22) (all in `dc_stay/README.md`).

One counter-signal: Vanguard's 2024-2025 leavers rolled over more in their first year (all ages 18% to 25% of people; 60s 34% to 36% of people, 46% to 48% of assets). Two years is too short to call a reversal.

At the same time, rollovers have become **more of a retirement event**: people 60+ supplied 43% of IRA rollover dollars in 2004 and 66% in 2023 (IRS). That is boomers reaching retirement, not a higher rollover rate: IRS rollovers per 100 IRA holders aged 60-64 were 8.8 (2004), 10.5 (2010), 10.1 (2016), 10.8 (2023).

## 1. IRA rollovers vs total DC outflows (best dollar measure)

`output/ira_rollovers_vs_dc_outflows.csv`. Numerator: IRS SOI rollovers into traditional IRAs (Form 5498; ICI tabulation for 1996-2002; current IRS files 2004-2023). Denominator: BEA Table 7.25 DC "benefit payments and withdrawals" (series Y353RC), which covers private, federal and state/local DC plans and counts rollovers out of plans as withdrawals. Form 5500 private DC benefits (incl. direct rollovers) shown as a second denominator.

| Period | Trad-IRA rollovers / BEA DC outflows | / Form 5500 private DC benefits |
|---|---|---|
| 1999-2007 | 93-99% (2002: 103%) | 104-114% |
| 2008-2015 | 88-94% | 99-107% |
| 2016-2018 | 85-86% | 94-95% |
| 2019 / 2020 / 2021 | 80.7 / 76.4 / 82.1% | 89 / 85 / 91% |
| 2022 / 2023 (new IRS method) | 80.1 / 74.7% | 89 / 83% |

This is a ratio, not a true rollover share:
- The numerator also includes DB lump sums rolled to IRAs and 60-day IRA-to-IRA redeposits (trustee-to-trustee transfers are excluded). Those inflate it, which is why it tops 100% against private-only Form 5500.
- The denominator includes RMDs, installments, hardship withdrawals, cash-outs and plan-to-plan rollovers (~8% of outflow dollars per Cerulli). More retirees drawing income inside the plan pushes the ratio down; that is part of the same "staying in plan" shift, not a separate effect.
- 2020 is depressed by CARES Act withdrawals; 2022-2023 use the new IRS method (traditional rollovers revised down 5% in 2022), so the last two points are not strictly comparable. The decline is already visible in 2016-2021 under the old method.
- No age split exists on the outflow side, so this is all ages, job changers and retirees mixed. Given 60+ supply two-thirds of rollover dollars, it is dominated by retirement-age money.

## 2. Vanguard, retirement-age leavers (best direct measure at retirement)

**60+ leavers by termination cohort, status at end-2021** (Vanguard 2023, *Retirement distribution decisions among DC participants*, Fig. 3; 504,400 people; in report Section 7):

| Leaver cohort | Rolled to IRA: people | Rolled to IRA: assets | In plan: assets | Cash: assets |
|---|---|---|---|---|
| 2011 | 57% | 66% | 16% | 5% |
| 2014 | 57% | 64% | 22% | 5% |
| 2017 | 48% | 55% | 33% | 6% |
| 2019 | 43% | 49% | 40% | 5% |
| 2020 | 38% | 45% | 46% | 4% |

Caveat: older cohorts had more years to roll over. Timing matters a lot: of Vanguard's 2021 *retirees*, 27% had rolled over by end-2021 but 50% by 2024 (Vanguard *How America Retires* 2025, via trade-press summaries; PDF not retrievable here). So part of the cohort gradient is timing. Vanguard reads the rest as a real shift toward staying in plan, and the in-plan asset share rising from 16% to 46% is far larger than three or four extra years of follow-up would plausibly produce (inferred, not tested).

**Year-of-termination status, How America Saves** (`output/vanguard_has_terminators.csv`, `vanguard_has_by_age_60s_70s.csv`; HAS 2025 and 2026, Figs. 116-117). All ages, status at end of the leaving year:

| | 2015 | 2018 | 2021 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| Rollover, % of people | 20 | 18 | 18 | 18 | 21 | 25 |
| Rollover, % of assets | 37 | 37 | 34 | 33 | 35 | 36 |
| Remain in plan, % of assets | 56 | 56 | 61 | 61 | 59 | 58 |
| Cash, % of assets | 5 | 6 | 4 | 5 | 5 | 5 |

60s leavers: rolled over 34% of people / 46% of assets (2024), 36% / 48% (2025); 70s: 32-35% / 55%. Only two years of the age split were obtainable (earlier HAS editions are no longer downloadable).

## 3. Other sources and why they rank lower

- **IRS SOI by age** (`output/irs_rollovers_by_age.csv`): the most authoritative count of money *arriving* in IRAs, 2004-2023, but no denominator of money *available*, so it can't give a share by itself. Rollover dollars as % of the age group's IRA assets are flat (60-64: 7.8-9.6% most years).
- **ICI IRA Owners Survey**: share of traditional-IRA households holding rollover money flat at 57-62% (2016-2025, online mode); "retirement" cited as a reason rose from 34-36% (2016-2020) to 43-46% (2022-2025). A stock measure of IRA owners, not leavers.
- **Industry volume estimates** (Cerulli, LIMRA): $779bn (2022) etc. Levels only, partly built on IRS.
- **Surveys**: SIPP rollover item ran only 2017-2022 and is unreliable (n≈100); older SIPP lump-sum modules ended 2012. HRS (blocked here) gives snapshots (2008/2010: 21.5% of retirees from last job rolled to an IRA, 17.2% left money in the plan). SCF covers stocks, not flows.
- **TSP**: clean administrative retention series, but federal workers only and no rollover split.

## Best data, ranked

1. For dollars: IRS SOI rollovers (Form 5498) against BEA DC outflows. Administrative, complete, 1996-2023, but a ratio with mismatched coverage.
2. For behaviour at retirement: Vanguard's cohort data. Direct, large, age-specific, by people and assets, but one recordkeeper (larger plans, more auto-features) and sensitive to follow-up length.
3. Supporting: TSP retention, Form 5500 separated participants, SCF past-job plan share.

The ideal source, Form 1099-R distribution code G (direct rollover) linked to W-2 separations, exists only in restricted IRS data (not public).
