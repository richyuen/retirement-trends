# Longevity trends, before and after COVID

US life expectancy at birth and at 65, by sex, period and cohort, 1980-2025, with the 2020-2021 COVID drop and the recovery measured against the pre-COVID trend and against what Social Security's Trustees projected just before COVID. Built 2026-10-04.

## Findings

1. **Long run: gains at 65 slowed sharply in the 2010s.** Period life expectancy at 65 (both sexes) rose from 16.4 years in 1980 to 19.1 in 2010 and 19.6 in 2019. The pace fell from about 1.5 years per decade in 2000-2010 to 0.4 per decade in 2010-2019 (men 1.8 to 0.5, women 1.4 to 0.5). At birth, gains stopped entirely in 2010-2019 (about 0 per decade, men slightly negative). [NCHS; `output/covid_gap.csv`]

2. **COVID took about 1.1-1.2 years off life expectancy at 65, and it is now back.** At 65 (both sexes): 19.59 (2019), 18.46 (2020), 18.42 (2021), 18.91 (2022), 19.52 (2023), 19.66 (2024). 2024 is a record, but only 0.07 above 2019 and about 0.1 below where the 2010-2019 trend would have put it. At birth: 78.85 (2019), 76.37 (2021 low), 78.97 (2024, also a record). [NCHS US Life Tables 2019-2024]

   | At 65, period | 2019 | 2021 | 2024 | 2024 vs 2010-19 trend |
   |---|---|---|---|---|
   | Men | 18.20 | 16.99 | 18.36 | -0.05 |
   | Women | 20.82 | 19.74 | 20.83 | -0.18 |

3. **Against the pre-COVID Trustees projection, the remaining shortfall is small.** The 2020 Trustees Report (assumptions set before COVID) projected period life expectancy at 65 of 18.5 (men) and 21.0 (women) for 2025. The 2026 Trustees Report estimates 2025 at 18.2 and 20.7, about 0.3 years lower. NCHS actuals for 2024 sit 0.06 (men) and 0.11 (women) below the 2020 report's interpolated path. SSA's 2025 figure is from partial-year provisional data and is slightly below its 2024 estimate (18.3/20.8). [SSA Trustees Reports 2020 and 2026, Table V.A4] See finding 7 for NCHS's later 2025 provisional data, which point the other way.

4. **Cohort life expectancy, the measure that matters for retirement planning, barely moved.** Cohort life expectancy assumes death rates keep improving over the person's remaining life. For someone turning 65 in 2025, the 2026 Trustees Report gives 19.1 years for men and 21.7 for women (to about age 84 and 87), about 0.9-1.0 years more than the period figure. The pre-COVID 2020 report gave 19.3 and 21.8 for the same group, so COVID and the weaker 2010s trimmed cohort expectations by 0.1-0.2 years. The 2026 report projects cohort life expectancy at 65 of 19.5/22.0 in 2030 and 20.7/23.1 in 2050. [Table V.A5; `output/trustees_period_cohort.csv`]

5. **Chance of reaching 90, from 65 (period life tables):** 30.2% in 2019, 25.4% in 2021, 30.7% in 2024. Men 24.2% to 19.6% to 25.1%; women 35.4% to 30.8% to 35.7%. Reaching 95: 11.8%, 9.1%, 12.0%. These are period figures; cohort survival is higher because mortality is assumed to keep improving. [`output/life_table_summary_2018_2024.csv`]

6. **The COVID hit at 65 was much larger for Hispanic, Black and American Indian adults, and all groups have recovered.** Fall in life expectancy at 65, 2019 to the 2020-2021 low: Hispanic 2.8 years, American Indian/Alaska Native 2.2, non-Hispanic Black 2.0, non-Hispanic Asian 1.5, non-Hispanic White 1.1. By 2024 every group was at or above 2019 except non-Hispanic White, which is flat (19.48 in 2019, 19.47 in 2024); the 2024 national record comes from the other groups and from population mix, not from White non-Hispanic gains (inferred from the group figures). Caution on the AIAN gain to 19.21 in 2024 (18.21 in 2019): it is not a change in NCHS's misclassification adjustment (the AIAN classification ratios at 65+ are identical in the 2019 and 2024 reports, Technical Notes Table II). But 2019 uses 2010-based population estimates and 2020-2024 use the 2020-census blended base, and NCHS warns that denominator changes hit small groups like AIAN hardest. On the consistent 2020-based denominators AIAN life expectancy at 65 still rose 1.4 years from 2022 to 2024 (17.83 to 19.21), so some of the gain is real; how much of the 2019-2024 comparison is the population base is not known.

| At 65, both sexes | 2019 | Low (2020-21) | 2024 |
|---|---|---|---|
| Hispanic | 21.58 | 18.82 | 21.77 |
| NH Asian | 23.44 | 21.90 | 23.66 |
| NH White | 19.48 | 18.41 | 19.47 |
| NH Black | 18.18 | 16.18 | 18.32 |
| NH AIAN | 18.21 | 16.03 | 19.21 |

7. **2025 looks like another improvement, though by how much is uncertain.** NCHS's provisional 2025 data (VSRR No. 44, July 2026, 99.9% of records) put the age-adjusted death rate at 689.2 per 100,000, 4.6% below 2024 (722.1) and a record low. Death rates fell 1.7% at 65-74, 4.1% at 75-84 and 7.6% at 85+. NCHS has not published a provisional 2025 life expectancy. Two cautions: the 2025 rates use Vintage 2025 population estimates, built on a different method (2020 census plus the MARC file) from the 2024 blended base, so part of the drop may come from bigger denominators rather than fewer deaths (the same population reset seen in the CPS ASEC 2026 file); and SSA's partial-year estimate shows 2025 flat at 65. Final 2025 life tables should settle it. [`raw/nchs_reports/vsrr044_provisional_mortality_2025.pdf`]

8. **Longevity by income: the gap is large and was widening before COVID.**
   - *By household income (Chetty et al. 2016, IRS-linked deaths, 2001-2014):* for 40-year-olds, expected age at death is 72.7 for the poorest 1% of men vs 87.3 for the richest 1%, a 14.6-year gap; for women 78.8 vs 88.9, a 10.1-year gap. By quartile, men in the bottom quarter gained 0.08 years per year in 2001-2014 and men in the top quarter 0.20; for women 0.10 vs 0.23. Bottom-quartile men went from 76.1 to 77.4, top-quartile men from 84.8 to 87.2. [`output/income_le40_chetty.csv`, computed from the Health Inequality Project tables]
   - *By lifetime earnings, across cohorts (National Academies 2015, SSA earnings linked to HRS):* life expectancy at 50 for men in the bottom earnings quintile is 26.6 years for those born in 1930 and a projected 26.1 for those born in 1960, no gain. For the top quintile it rises from 31.7 to 38.8 years. The top-bottom gap for men widens from 5.1 to 12.7 years; for women from 4 to 13.6 years, with the bottom quintile falling from 32.3 to 28.3.
   - *By education, through COVID (Case and Deaton, Brookings Papers 2023):* the gap in life expectancy at 25 between adults with and without a BA grew from 2.6 years in 1992 to 6.3 in 2019 and 8.5 in 2021. Adults without a BA peaked in 2010 and have not regained it. During the pandemic, adults with a BA lost 1.1 years and those without lost 3.3. Their data stop at 2021; no source here shows whether the gap closed in the 2022-2024 recovery.
   - *Why it matters for retirement:* average life expectancy at 65 overstates how long lower earners will draw on savings or annuitize, and understates it for higher earners, who hold most retirement-account balances (inferred; ties to the SCF/IRS findings on who holds IRA and DC assets).

## Period vs cohort (why the numbers differ)
- **Period** life expectancy uses one year's death rates at every age. It shows the COVID shock clearly but is not anyone's actual expected lifetime.
- **Cohort** life expectancy uses the death rates a person will actually face in each future year (actual, then projected). It is the right input for how long retirement savings must last, and it is about one year higher at 65.
- SSA (Social Security area population) and NCHS (US resident population) differ slightly; e.g. men's period life expectancy at birth in 2000 is 74.0 (SSA) vs 74.1 (NCHS). Don't mix the two in one series.

## Sources
- NCHS, United States Life Tables, data years 2018-2024 (National Vital Statistics Reports vol 69 no 12, 70-19, 71-1, 72-12, 74-2, 74-6, 75-5). Spreadsheets from `https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/NVSR/<vol-no>/TableNN.xlsx`; Tables 1-3 total/male/female, 4-6 Hispanic, 7-9 NH AIAN, 10-12 NH Asian, 13-15 NH Black, 16-18 NH White (2018 report uses a different grouping, so groups start in 2019).
- NCHS, Health, United States 2020-2021, Table LExpMort (life expectancy at birth, 65, 75 by sex, 1900-2019, one decimal): `https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/Health_US/hus20-21tables/LExpMort.xlsx`. Used for 1980-2017; matches NVSR for 2018-2019 within rounding (checked in the script).
- 2026 OASDI Trustees Report, House Document 119-163, Tables V.A4 and V.A5: `https://www.govinfo.gov/content/pkg/CDOC-119hdoc163/pdf/CDOC-119hdoc163.pdf` (pp. 109-110).
- 2020 OASDI Trustees Report, House Document 116-123, Tables V.A4 and V.A5: `https://www.govinfo.gov/content/pkg/CDOC-116hdoc123/pdf/CDOC-116hdoc123.pdf` (pp. 98-99).
- NCHS, Mortality in the United States: Provisional Data, 2025 (Vital Statistics Rapid Release No. 44, July 2026): `https://www.cdc.gov/nchs/data/vsrr/vsrr044.pdf`. NCHS US Life Tables 2019 and 2024 reports (NVSR 70-19, 75-5) Technical Notes Table II for the classification-ratio check: `https://www.cdc.gov/nchs/data/nvsr/nvsr75/nvsr75-05.pdf`.
- Chetty R, Stepner M, Abraham S, et al. The Association Between Income and Life Expectancy in the United States, 2001-2014. JAMA 2016. Online Data Tables 1-2: `https://healthinequality.org/data/` (saved in `raw/income/`). Life expectancy is race-adjusted expected age at death for 40-year-olds; quartiles are simple means of percentiles.
- National Academies of Sciences, Engineering, and Medicine. The Growing Gap in Life Expectancy by Income: Implications for Federal Programs and Policy Responses. 2015. Summary: `https://nap.nationalacademies.org/read/19015/chapter/2` (saved in `raw/income/`).
- Case A, Deaton A. Accounting for the Widening Mortality Gap between American Adults with and without a BA. Brookings Papers on Economic Activity, Fall 2023 (conference draft): `https://www.brookings.edu/wp-content/uploads/2023/09/1_Case-Deaton_unembargoed.pdf` (saved in `raw/income/`). The 2.6/6.3/8.5 figures are life expectancy at 25; the paper's other measure (years lived between 25 and 85) gives 2.6/5.0/6.9.
- ssa.gov blocks this environment (403), so the Trustees tables come from the govinfo copies; table text is saved in `raw/trustees/`.

## Files
- `scripts/fetch_nvsr.sh` downloads the NVSR spreadsheets to `raw/nvsr/`. `scripts/build.py` writes all outputs.
- `output/le_nchs_1980_2024.csv` annual period life expectancy at birth, 65, 75 by sex (one decimal to 2017, two from 2018).
- `output/life_table_summary_2018_2024.csv` e0, e65, e75 and % surviving 65 to 85/90/95, by group, sex, year.
- `output/trustees_period_cohort.csv` SSA period and cohort life expectancy at birth and 65, intermediate, 2020 and 2026 reports.
- `output/covid_gap.csv` 2019-2024 actual vs 2010-2019 linear trend and vs the 2020 Trustees path (interpolated between 2020 and 2025), plus decade slopes.
- `output/income_le40_chetty.csv` life expectancy at 40 by household income quartile (pooled, 2001, 2014, annual gain) and top/bottom 1%, by sex.

## Not covered, and why
- Income gaps after 2014 and through COVID: the Chetty tables end in 2014 and no public update exists. SSA's differential-mortality work (Actuarial Notes, Trustees technical panel papers) and GAO's lower-earner longevity reports are on ssa.gov and gao.gov, which both return 403 from this environment, so they could not be used.
- HRS-based longevity by wealth: the HRS site is blocked here.
- NCHS provisional 2025 life expectancy: not yet published; finding 7 uses the provisional 2025 death rates instead.
