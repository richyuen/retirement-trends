# How household spending changes with age and over time: older consumer units (BLS CE + research)

Status: complete 2026-10-04. Owner: spending/CE sub-task. Everything in this folder is reproducible from `scripts/`.

## Data and method

- **Source**: BLS Consumer Expenditure Survey (CE) published annual means, LABSTAT time-series database `cx`
  (https://download.bls.gov/pub/time.series/cx/ : `cx.series`, `cx.data.1.AllData`, downloaded 2026-10-04).
  Series id pattern `CXU{item}LB04{age}M`, where LB04 = age of reference person and the age codes are 01 = all CUs,
  06 = 55-64, 07 = 65+, 08 = 65-74 and 09 = 75+. For example, `CXUTOTALEXPLB0407M` is average annual expenditures for 65+.
  Bands 55-64, 65-74 and 75+ run 1984-2024. The 65+ band (07) starts in 1988. Most detailed items (e.g. Medicare
  payments, item 580901) start in 2010. **The latest year in LABSTAT on 2026-10-04 is 2024.**
- **Deflator**: CPI-U, U.S. city average, all items, annual average, series `CUUR0000SA0` period M13
  (https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems). Real values are in **2024 dollars**.
  R-CPI-U-RS, which grows more slowly before 1999, would show somewhat larger real growth over 1984-2024. It is not used here.
- **Per person** = published mean expenditure per CU divided by published mean CU size (item 980010). This is a ratio of means.
  CU size is published to one decimal, so per-person values carry roughly ±3% rounding noise.
- Scripts: `scripts/01_extract.py` reads raw files from `/tmp/ce_raw` (not kept in the shared folder) and writes
  `output/ce_age_long.csv` (all LB04 age bands, selected items) plus `output/ce_series_list.csv` and `output/cpi_u_annual.csv`.
  `scripts/02_analyze.py` builds the tables below.

| File | Content |
|---|---|
| `output/t1_total_spending_by_age.csv` | Nominal and real (2024$) mean expenditures per CU and per person; 65-74, 75+, 65+ relative to 55-64; spending as % of income before and after taxes; 1984-2024 |
| `output/t2_budget_shares_long.csv` / `t2_budget_shares_wide.csv` | Category shares of total expenditures by age band, incl. health split (insurance, medical services, drugs, supplies, Medicare payments 2010+) |
| `output/t3_pandemic_2017_2024.csv` | Real 2024$ by category, index 2019 = 100, for 55-64, 65+, 65-74, 75+ |
| `output/t4_income_sources_long.csv` | Income sources as % of income before taxes, by age band, with method flag (complete reporters to 2003, imputed 2004+) |
| `output/t5_pseudo_cohorts.csv` | Synthetic cohorts: 55-64 in year t, 65-74 in t+10, 75+ in t+20 (per CU and per person, real) |
| `output/t6_cu_characteristics.csv` | CU size, mean age, homeownership/mortgage, earners, number of CUs |
| `output/t7_age_profile_selected_years.csv` | Full age profile (under 25 ... 75+) for 1984, 1990, 2000, 2007, 2019, 2024 |

## Findings from the CE

### 1. Older households spend less than 55-64s, but the gap has narrowed a lot since 1984 (t1, series `CXUTOTALEXPLB04{06,08,09}M`)

| Real mean expenditures per CU, 2024$ | 1984 | 1990 | 2000 | 2010 | 2019 | 2020 | 2024 |
|---|---|---|---|---|---|---|---|
| All CUs | 66,346 | 68,116 | 69,305 | 69,208 | 77,345 | 74,337 | 78,535 |
| 55-64 | 70,651 | 70,233 | 71,664 | 73,223 | 85,269 | 78,683 | 84,946 |
| 65-74 | 47,829 | 50,164 | 56,074 | 59,606 | 67,591 | 63,467 | 65,354 |
| 75+ | 33,579 | 37,081 | 39,909 | 45,357 | 53,525 | 49,468 | 55,834 |
| 65+ | n/a | 44,524 | 48,334 | 52,942 | 61,620 | 57,660 | 61,432 |
| **65-74 as % of 55-64** | **67.7%** | 71.4% | 78.2% | 81.4% | 79.3% | 80.7% | **76.9%** |
| **75+ as % of 55-64** | **47.5%** | 52.8% | 55.7% | 61.9% | 62.8% | 62.9% | **65.7%** |

- Real spending per CU grew much faster for older households than for 55-64s. From 1984 to 2024 it rose
  **+37% for 65-74** and **+66% for 75+**, against +20% for 55-64 and +18% for all CUs.
- **Per person** the age gradient is much flatter, because CU size falls with age (2024: 2.2 persons at 55-64,
  1.9 at 65-74, 1.6 at 75+). In 2024 real spending per person was $38,612 at 55-64, $34,397 at 65-74 and $34,896 at 75+,
  so 65-74 was at **89%** and 75+ at **90%** of the 55-64 level. In 1984 those ratios were 89% and 74%.
- **Synthetic cohorts (t5)** follow the 55-64 band in year t to 65-74 at t+10 and 75+ at t+20 (cohorts 1984-2004).
  Per CU, spending falls to an average **82%** of the 55-64 level ten years later and **68%** twenty years later.
  Per person it is roughly flat: the averages are 97.5% and 97.3%. Across individual cohorts the range is 0.89-1.11.
  Much of the cross-sectional decline per household reflects shrinking households (widowhood) and rising real spending
  across calendar time, not individuals cutting back. CE cannot follow individuals, though; the panel studies in section 5 do.
- **Spending as % of income before taxes** (t1). The 65+ figure was 98.5% in 1990 and 105.2% in 2000.
  Both are pre-2004 figures that use complete income reporters only. After imputation began it was 88.9% in 2004,
  90.2% in 2019 and **91.1% in 2024**. For 75+ it was **99.7%** in 2024, against **69.9%** for 55-64.
  As a share of income after taxes, 65+ spending has been around 100% since 2014: 104.2% in 2014 and 101.9% in 2023.
  After-tax income is not published for 2024, and TAXSIM tax imputation from 2013 is a break.
  Older CUs spend about all of their measured income. That is consistent with drawing on assets (including retirement
  accounts) and with income that CE does not capture well; see the caveats.

### 2. Budget shares of older CUs (t2_budget_shares_wide.csv; % of total average annual expenditures)

| 65+ CUs (`CXU{item}LB0407M`) | 1988 | 2000 | 2010 | 2019 | 2024 |
|---|---|---|---|---|---|
| Housing | 32.1 | 33.0 | 35.4 | 34.8 | 36.1 |
| Transportation | 17.6 | 16.6 | 14.2 | 14.9 | 15.5 |
| Food | 14.9 | 13.8 | 12.4 | 13.1 | 12.9 |
| **Healthcare** | **12.1** | 12.2 | 13.2 | **13.6** | **12.7** |
| - of which health insurance | 5.1 | 6.1 | 8.4 | 9.4 | 8.3 |
| - insurance as % of healthcare | 42.0 | 49.9 | 63.7 | 69.5 | 65.5 |
| Personal insurance and pensions | 4.2 | 3.5 | 5.1 | 5.7 | 5.7 |
| Cash contributions | 4.4 | 6.9 | 6.2 | 5.1 | 5.1 |
| Entertainment | 3.8 | 4.0 | 5.1 | 4.7 | 4.9 |
| Apparel and services | 4.4 | 3.5 | 2.6 | 2.6 | 2.0 |

- **Healthcare** takes about 1.5x the all-CU share (12.7% vs 7.9% in 2024). It is highest for 75+:
  13.5% in 1984, 15.8% in 2019 and 14.2% in 2024. For 65+ the share rose slowly from about 12% (1988-2000) to a peak of 14.0% in 2020.
  It has fallen back since. The 2024 dip comes from health insurance, which fell 12% in real terms from 2019 to 2024.
- **The mix shifted from out-of-pocket care to premiums.** For 65+, health insurance went from 42% of healthcare
  spending (1988) to 70-73% (2019-2020) and 65.5% in 2024. Drugs fell from 2.6% of the budget in 1990 to 2.2% in 2010
  and 1.5% in 2019-2024, after Medicare Part D (2006). Medical services fell from 3.6% (1990) to 2.1-2.4%.
  Medicare payments (item 580901, Part B etc.) alone were 3.6% of 65+ spending in 2010, 4.3% in 2019 and 4.5% in 2024 (75+: 5.1%).
  Some of the 2013-2014 jump in the insurance share for all CUs (61% to 67%) coincides with ACA coverage expansion
  and with CE questionnaire changes. Treat 2013/14 as a soft break.
- **Housing** has risen by about 4 points for 65+ (32% to 36%) and for 75+ (36.0% in 1984 to 39.4% in 2024).
  More older homeowners now carry a mortgage: 15% of 65+ CUs in 1990, 24% in 2019 and 2024 (item 980230).
- **Food** and **apparel** shares have fallen for every age. Cash contributions are about twice the all-CU share
  (65+ 5.1% vs 2.9% in 2024; 75+ 6.3%) and are volatile (75+: 12.6% in 2022, a high-RSE item).
  Personal insurance and pensions are mostly Social Security and pension contributions, so they track work.
  They are 7.0% for 65-74 and 3.4% for 75+, against 14.3% for 55-64.

### 3. Pandemic: 2019 vs 2020 vs 2021-2024, 65+ (t3; real 2024$, index 2019 = 100)

| 65+ | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| Total ($, 2024$) | 61,620 | 57,660 | 60,361 | 61,990 | 61,859 | 61,432 |
| Total (index) | 100 | **93.6** | 98.0 | 100.6 | 100.4 | 99.7 |
| Food away from home | 100 | 58.2 | 74.2 | 86.4 | 90.7 | 86.4 |
| Apparel and services | 100 | 62.1 | 71.3 | 75.6 | 82.8 | 74.8 |
| Transportation | 100 | 82.0 | 90.2 | 95.3 | 101.2 | 103.8 |
| Healthcare | 100 | 96.4 | 97.1 | 96.6 | 98.6 | 93.0 |
| Shelter | 100 | 100.4 | 100.4 | 104.7 | 107.8 | 108.5 |
| Cash contributions | 100 | 120.2 | 122.9 | 151.4 | 102.5 | 100.4 |

- In 2020 real spending fell **6.4% for 65+**, 7.6% for 75+ and 7.7% for 55-64. Restaurants, apparel, travel and
  vehicles drove the drop; shelter and health insurance did not fall.
- Total real spending for 65+ was back to its 2019 level by 2022 and flat through 2024 (99.7). The mix did not fully
  return: food away from home and apparel were still 14-25% below 2019 in 2024, while shelter was 8.5% above
  (75+: 23.7% above). Spending was 72.3% of the 55-64 level in both 2019 and 2024, so the pandemic did not change
  the age gradient in the published data.

### 4. Income sources of older CUs (t4; % of income before taxes; series e.g. `CXURETIRINCLB0407M`, `CXU900000LB0407M`)

| 65+ | 1988 | 2000 | 2003 | 2004 | 2012 | 2013 | 2019 | 2024 |
|---|---|---|---|---|---|---|---|---|
| Wages and salaries | 20.9 | 23.3 | 24.6 | 29.3 | 31.7 | 35.0 | 33.1 | **35.3** |
| Social Security + private/govt retirement (RETIRINC) | 59.5 | 64.2 | 62.0 | 55.9 | 56.3 | 53.3 | 47.4 | **49.5** |
| - Social Security and railroad retirement (900030, 2010+) | | | | | 36.9 | 37.4 | 36.5 | 38.3 |
| - Pensions/annuities (900040, to 2013) or retirement, survivors, disability (900170, 2013+) | | | | | 19.4 | 14.6 | 10.8 | 11.2 |
| Interest, dividends, rental, other property (INDIVRNT) | 13.5 | 7.5 | 6.3 | 7.5 | 6.4 | 6.1 | 8.2 | 7.6 |
| Self-employment | 4.1 | 3.2 | 5.3 | 5.9 | 3.6 | 3.6 | 9.7 | 5.9 |

- Earnings now make up about 35% of 65+ CU income before taxes, up from about 20% around 1990. Some of the step-up
  comes at the 2004 imputation break (24.6% to 29.3%), but the trend continues before and after it. The 65-74 band
  is at 43.6% in 2024.
- Social Security is a steady 37-38% of 65+ income (about 50% for 75+). Non-Social-Security retirement income
  (pensions, annuities, and probably some regular retirement-account distributions) fell from 14.6% (2013) to 11.2% (2024).
  Property income fell from 13.5% (1988) to 6-8% as interest rates dropped.
- Method breaks: before 2004, income is for complete income reporters only (footnote 1 in `cx.footnote`).
  Imputation starts in 2004. Income questions were redesigned in 2013, when item 900040 was replaced by 900170/900180.
  Compare levels only within 1988-2003, 2004-2012 and 2013-2024.

## Caveats (keep with any use of these numbers)

1. **Cross-section, not panel.** Each year's age profile mixes age, cohort and period effects. The 65-74 vs 55-64 ratio
   is not how a household's spending changes when it ages. The synthetic cohorts in t5 help, but survivorship
   (wealthier people live longer) and changes in who heads the CU (widowhood, moving in with children) bias them.
2. **Consumer unit ≠ household ≠ person.** A CU is a financially independent group, so a household can contain several CUs.
   Age is the reference person's age. CU size falls with age, and per-person figures use a rounded mean size.
3. **Open-ended 75+ band.** Its mean reference-person age is about 81. The CE institutional sample excludes nursing-home
   residents, so late-life long-term-care spending is largely missing.
4. **Spending, not consumption.** Owners' housing is counted as mortgage interest, property tax, insurance and repairs.
   There is no imputed rent, and mortgage principal is excluded. Vehicles are counted at net purchase outlay. Paying off a
   mortgage lowers measured "spending" without lowering consumption.
5. **Survey changes.** Income imputation starts in 2004. Income questions and TAXSIM after-tax income change in 2013.
   Health insurance detail is restructured in 2013 and 2017 (new item codes). Vehicle insurance changes in 2019 (`cx.footnote` 4).
   BLS documents further processing and questionnaire changes in its CE 'changes' notes (not itemized here).
   Several food and alcohol items are re-coded 2021-2023. Treat 2013-2015 as a soft break for income, taxes and health insurance.
6. **Income under-reporting.** CE income, like CPS before its 2014-2019 redesigns, likely under-captures irregular
   retirement-account withdrawals and asset income. Spending/income near or above 100% is therefore an upper bound on
   "dissaving". Use IRS/SCF numbers elsewhere in this project for withdrawals.
7. **Sampling error.** Small items carry BLS footnote 6 (RSE ≥ 25%); see `footnote_codes` in `ce_age_long.csv`.
   Year-to-year moves in 75+ categories (e.g. cash contributions in 2022) are noisy.

## 5. Published research on spending trajectories in retirement

| Study (date) | Data / design | Key quantitative finding |
|---|---|---|
| Hurd & Rohwedder, "Some Answers to the Retirement-Consumption Puzzle", NBER WP 12057 (Feb 2006). https://www.nber.org/papers/w12057 | HRS + CAMS 2001-2003; **panel** (anticipated vs recollected) | Workers anticipated a **13.3%** drop in spending at retirement and later recollected **12.9%** (n=146 matched; full wave-1 recollected 13.8%). Fewer than half of retirees recall any decline. Drops are larger with poor health (20.9% if fair/poor health before and after). They conclude there is no real "puzzle". The paper also cites Fisher et al. (CE synthetic panel): total spending falls only **2.5%** at retirement, food 5.9%. |
| Hurd & Rohwedder, "Heterogeneity in spending change at retirement", J. Economics of Ageing 1-2 (2013) 60-71. https://ideas.repec.org/a/eee/joecag/v1-2y2013ip60-71.html | HRS/CAMS **panel** | Spending declines only a little at retirement. Spending **increased** at retirement in the upper half of the wealth distribution. |
| Rohwedder, Hurd & Hudomiet, "Explanations for the Decline in Spending at Older Ages", NBER WP 30460 (Sep 2022). https://www.nber.org/papers/w30460 | CAMS 2005-2019, **panel** (two-year changes) | Median real spending fell **1.88%/yr for singles and 2.78%/yr for couples** (2005-2019), and almost every age-by-year cell was negative. A single high-school graduate at 85 is predicted to spend **72%** of what they spent at 65 (57% without a HS degree). The out-of-pocket health budget share reaches **15% at 85+**. Satisfaction with finances rises with age, and close to 20% of those over 80 are not satisfied. Most of the decline reflects less enjoyment of activities as health declines and people are widowed, not running out of money. |
| Hurd & Rohwedder, "Insights on Economic Well-being at Older Ages from Analyses of Household Spending", Wharton PRC Symposium slides (3 May 2024). https://pensionresearchcouncil.wharton.upenn.edu/wp-content/uploads/2024/05/PRC-2024-Rohwedder_v4.pdf | CAMS **panel**, paths from 65 to 90 by initial wealth quartile | Average annual real change is **-2.7% for married** and **-2.0% for single** households. Spending declines in all wealth quartiles; the steepest decline is in the lowest quartile. Also published as "Spending Trajectories After Age 65: Variation by Initial Wealth" (RAND EP70132). (A secondary-summary figure of -1.7%/-2.4% a year was dropped on 2026-10-04: the paper's hosts, RAND and the Michigan center, block this environment.) |
| Banerjee (EBRI), "Expenditure Patterns of Older Americans, 2001-2009", EBRI Issue Brief 368 (Feb 2012). https://www.ebri.org/content/expenditure-patterns-of-older-americans-2001-2009-4992 (PDF mirror: https://www.ncpssm.org/wp-content/uploads/2015/12/EBRI_IB_02-2012_No368_ExpPttns.pdf) | HRS/CAMS 2001-2009, age profile from pooled waves (mostly **cross-section by age**) | Relative to age 65, household spending is **19% lower by 75, 34% lower by 85 and 52% lower by 95**. Home-related spending stays at 40-45% of the budget. Health rises from about **10% of the budget at 50-64 to about 20% at 85+**. |
| Banerjee (EBRI), "Change in Household Spending After Retirement: Results from a Longitudinal Sample", EBRI Issue Brief (19 Nov 2015; issue number not shown on the EBRI page, so not given). https://www.ebri.org/crawler/view/change-in-household-spending-after-retirement-results-from-a-longitudinal-sample-3291 | HRS/CAMS **panel**, same households up to 6 years after retirement | Median spending was **5.5%** below pre-retirement in the first two years and **12.5%** below by the third or fourth year, then the decline slowed. Transportation fell most (median -25.1% in the first two years; checked on the EBRI page 2026-10-04). **45.9%** of households spent more than before retirement in the first two years; **33.4%** did by year six. |
| Blanchett, "Exploring the Retirement Consumption Puzzle", J. Financial Planning (May 2014). https://www.financialplanningassociation.org/article/journal/MAY14-exploring-retirement-consumption-puzzle | RAND HRS + CAMS 2001-2009, **panel** (591 retired households in all 5 waves); CE for budget shares | Average real change is **-0.96%/yr** from age 60 to 90 (t = -4.31). Declines are smaller at the younger and older ends, which he calls the "retirement spending smile" (still negative). Households spending a lot relative to their net worth cut spending considerably. Those with low spending and high net worth increased spending from 65 to 75. In CE, health is about 20% of spending by 85. He cites earlier work finding about -2.5% at retirement and then about -1%/yr. |
| Chen & Munnell (CRR), "Do Retirees Want to Consume More, Less, or the Same as They Age?", Issue Brief 21-21 (Dec 2021). https://crr.bc.edu/wp-content/uploads/2021/12/IB_21-21.pdf | CAMS 2001-2019 linked to HRS, and PSID 2005-2019; **panel** | Consumption falls about **1.5-1.6% every two years (~0.8%/yr)**, so it is about 12-13% lower after 20 years. The top wealth tercile declines only about 0.7% per two years (~0.35%/yr), and wealthy, healthy households are nearly flat. Households in fair/poor health decline faster. The authors read the decline as partly constraint-driven, which contrasts with Rohwedder et al. |
| Aguiar & Hurst, "Deconstructing Lifecycle Expenditure", NBER WP 13893 (2008), JPE 121(3) 2013. https://www.nber.org/papers/w13893 | CE, **cross-section/synthetic cohort** | The post-middle-age decline in nondurables comes from work-related categories (food, clothing, transportation) and categories open to home production. Entertainment rises throughout the lifecycle. Aguiar & Hurst (JPE 2005) find food *expenditure* falls about 17% at retirement while food *intake* does not (as summarized by Blanchett 2014). |
| J.P. Morgan Asset Management, "Three new spending surprises" (2025 update; Chase transactions Jan 2017-Nov 2024). https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/insights/retirement-insights/RI-3-SPEND.pdf | More than 280,000 Chase households (cross-section by age) plus a longitudinal subset of more than 55,000 | Spending peaks in mid-life and falls at older ages. 65+ households spend more on health care and charity and less on everything else. **53%** of households do not retire all at once. Partially retired households with less than $150k pre-retirement income show a post-retirement spending **surge**. JPM's 2026 Guide to Retirement press release says six in ten new retirees see significant spending volatility in their first three years. The 2026 Guide's finding that average real spending falls by more than 30% between ages 60 and 85 is reported by PLANADVISER (V. Baez, 17 Dec 2025, https://www.planadviser.com/research-finds-slowdown-in-spending-during-retirement/) and Financial Planning (E. Nicholson-Messmer, 29 Dec 2025); the Guide PDF itself was not retrievable, so cite it as reported. |
| Paulin, "Expenditure patterns of older Americans, 1984-97", Monthly Labor Review (May 2000). https://www.bls.gov/opub/mlr/2000/05/art1full.pdf ; Paulin & Duly, "Planning ahead: consumer expenditure patterns in retirement", MLR (Jul 2002). https://www.bls.gov/opub/mlr/2002/07/art3full.pdf | CE, **cross-section** | Spending trends for older consumers resemble those of younger ones, and 65-74 differ from 75+. Older consumers' share of all real spending rose from 12.6% to 14.6% (1984-97, quoted in Paulin & Duly). |

Summary of the literature:
- **Panel evidence (HRS/CAMS)** consistently shows real spending declining after 65. The estimates range from about 1%/yr
  (Blanchett, CRR) to about 2-2.8%/yr (Rohwedder, Hurd et al.). Couples decline faster than singles, partly because of widowhood.
- At retirement itself, households recall a drop of about 13%. EBRI's panel shows a median decline of 5.5% within two years,
  but more than 40% of households increase spending. Wealthier households are flat or rising.
- Whether the decline reflects choice or constraint is disputed. Hurd and Rohwedder point to health and satisfaction;
  CRR finds it is concentrated among less wealthy and less healthy households.
- The CE cross-section above shows a larger per-CU age gradient than the per-person synthetic cohorts. Panel declines
  of 1-2.5%/yr per household fit with CE's per-CU synthetic-cohort ratio of about 0.82 after 10 years (about -2%/yr),
  given widowhood and shrinking CU size.
