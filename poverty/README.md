# Poverty among people 65+: official vs Supplemental Poverty Measure

Official poverty for people 65+ from 1959 to 2025, the Supplemental Poverty Measure (SPM) from 2009 to 2025, what Social Security and out-of-pocket medical spending (MOOP) do to the SPM rate, near-poverty, and breakdowns by age band, sex, living alone, and race/Hispanic origin. Built 2026-10-05 (candidate area 7 in `notes/new_areas_2026-10-05.md`). Everything comes from Census: the historical poverty tables, the tables of each annual SPM/poverty report (P60-241 to P60-290), and the public-use CPS ASEC CSV files 2019-2026. **Years are income (calendar) years.** ASEC year t covers income year t-1. The newest data are for 2025, from P60-290 (*Poverty in the United States: 2025*, Sept 2026).

## Findings

1. **Official poverty among people 65+ fell from 35.2% (1959) to about 10% by the mid-1990s and has stayed there for 30 years. Since 2024 it has again been above the rate for adults 18-64.** Census Historical Poverty Table 3, people 65+:

   | | 1959 | 1966 | 1970 | 1980 | 1990 | 2000 | 2010 | 2019 | 2022 | 2024 | 2025 |
   |---|---|---|---|---|---|---|---|---|---|---|---|
   | 65+ | 35.2 | 28.5 | 24.6 | 15.7 | 12.2 | 9.9 | 8.9 | 8.9 | 10.2 | 9.9 | 9.8 |
   | 18-64 | 17.0 | 10.5 | 9.0 | 10.1 | 10.7 | 9.6 | 13.8 | 9.4 | 10.6 | 9.6 | 9.2 |
   | Under 18 | 27.3 | 17.6 | 15.1 | 18.3 | 20.6 | 16.2 | 22.0 | 14.4 | 15.0 | 14.4 | 13.4 |

   - 1959 is a single year. There is no 65+ series for 1960-1965, so the continuous series starts in 1966.
   - The fall was fastest from 1966 to 1974 (28.5% to 14.6%), the years when Social Security benefits rose sharply and were then indexed. That timing is the standard account, not something tested here.
   - The 65+ rate was above the 18-64 rate in every year from 1966 to 1992. It was at or below it from 1993 to 2023, apart from 2000 (+0.3). The gap was widest after the Great Recession: 8.7% vs 13.7% in 2011.
   - The 65+ rate went above the 18-64 rate again in 2024 (9.9 vs 9.6) and 2025 (9.8 vs 9.2). This happened because working-age poverty fell, not because 65+ poverty rose: the 65+ rate has been 8.7-10.3% in every year since 2009.
   - 2025: 6.37 million people 65+ were officially poor, out of 65.2 million.

   [`output/opm_by_age_1959_2025.csv`]

2. **On the SPM, people 65+ are the poorest age group: 15.4% in 2025, 5.6 points above their official rate.** The gap is the widest of any age group. P60-290 Table 8 (SPM) and Table 3 (official), people 65+:

   | | 2009 | 2012 | 2015 | 2018 | 2019* | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
   |---|---|---|---|---|---|---|---|---|---|---|---|
   | SPM 65+ | 14.9 | 14.8 | 13.7 | 13.6 | 12.7 | 9.4 | 10.6 | 13.8 | 14.0 | 15.1 | 15.4 |
   | Official 65+ | 8.9 | 9.1 | 8.8 | 9.7 | 8.9 | 8.9 | 10.3 | 10.2 | 9.7 | 9.9 | 9.8 |
   | SPM minus official | 6.0 | 5.7 | 4.9 | 3.9 | 3.8 | 0.5 | 0.3 | 3.6 | 4.3 | 5.2 | 5.6 |
   | SPM, all ages | 15.1 | 16.0 | 14.5 | 12.8 | 11.7 | 9.1 | 7.7 | 12.1 | 12.7 | 13.0 | 13.1 |

   \*2019 is the revised SPM methodology, which is the base for 2019-2025. The 90% margin of error on SPM 65+ is ±0.4-0.6 points.

   - In the consistent 2019-2025 series, SPM poverty at 65+ rose 2.7 points (12.7 to 15.4) while the official rate went from 8.9% to 9.8%.
   - In 2025 the 65+ SPM rate (15.4%) was above the rates for children (13.4%) and 18-64 (12.3%). The 65+ rate has been the highest of the three age groups in every year since 2019 except 2020 (9.4 vs 9.6 for children). Children's SPM rate was higher in 2009-2018.
   - 2025 is above every year from 2014 on. Only 2010 (15.8%) and the redesigned 2013 sample (15.6%) were higher, and both belong to older methods.
   - Census explains the 65+ gap this way: it is "primarily due to differences in the treatment of medical expenses between the two measures" (P60-290 text). For the overall SPM-official gap, it says that thresholds rising faster than CPI-U "explain part of this gap" in recent years.
   - In 2020-2021 the gap nearly closed, because pandemic stimulus payments and refundable credits count in the SPM but not in the official measure. For 65+ in 2021, stimulus alone lowered the SPM rate by 3.0 points and MOOP added only +2.8 (P60-277 Table B-7).

   [`output/spm_vs_opm_by_age_2009_2025.csv`]

3. **Social Security is what keeps most older Americans out of poverty. Without it, SPM poverty at 65+ would be about 47% instead of 15%.** Census "effect of individual elements" tables, people 65+. Each effect is the percentage-point change in the SPM rate when that element is counted.

   | | 2010 | 2012 | 2013 (old Q) | 2013 (new Q) | 2014 | 2016 | 2017 (legacy) | 2017 (updated) | 2019 | 2020 | 2022 | 2024 | 2025 |
   |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   | SPM rate 65+ | 15.8 | 14.8 | 14.6 | 15.5 | 14.4 | 14.55 | 14.11 | 13.63 | 12.76 | 9.48 | 14.14 | 15.13 | 15.37 |
   | Social Security | −38.7 | −39.9 | −38.0 | −35.5 | −35.6 | −34.77 | −34.56 | −34.32 | −32.10 | −33.07 | −34.72 | −32.79 | −32.13 |
   | SSI | −1.1 | −1.2 | −1.5 | −1.2 | −1.4 | −1.23 | −1.30 | −1.22 | −0.93 | −0.90 | −0.88 | −0.85 | −0.99 |
   | Medical expenses (MOOP) | +7.2 | +6.4 | +6.3 | +7.0 | +5.6 | +5.76 | +5.42 | +4.40 | +4.02 | +2.65 | +3.62 | +3.74 | +3.83 |

   - In 2025, counting Social Security lowers the 65+ SPM rate by 32.1 points, from 47.5% to 15.4% (MOE ±0.7).
   - For all ages Social Security lowers the SPM rate by 8.5 points. It moved 28.8 million people out of SPM poverty in 2025, 20.9 million of them aged 65+ (P60-290 text and Table 5).
   - No other element moves 65+ poverty by more than about 1 point. SSI and housing subsidies are about −1.0 each, SNAP −0.9, and taxes, work expenses and FICA together +0.9.
   - The Social Security effect has shrunk within each consistent era: from −35.5 to −34.6 (2013-2017 on the redesigned questions) and from −34.3 to −32.1 (2017-2025 on updated processing).

   [`output/spm_element_effects_65plus.csv`]

4. **Out-of-pocket medical spending is the main reason SPM poverty at 65+ is higher than official poverty. Subtracting it adds 3.8 points (2025), about twice its effect at other ages.**
   - In 2025, MOOP raises the 65+ SPM rate by +3.83 points (MOE ±0.26). The effect is +1.88 for 18-64 and +1.99 for children (P60-290 Table 5).
   - Within the 65+ group (2025, own computation, SE about 0.2-0.3), the MOOP effect is +4.3 at 75+ vs +3.4 at 65-74, +4.1 for women vs +3.5 for men, and +5.0 for people living alone.
   - **The published MOOP effect fell from +7 points (2009-2011) to about +3.7-3.8 (2022-2025), but much of that fall is method.**
     - The 2019 processing change cut it by 1.0 point within the same year (2017: +5.42 legacy vs +4.40 updated).
     - The 2014 questionnaire redesign moved it by 0.7 points (2013: +6.3 vs +7.0).
     - On the legacy redesigned questions it fell from +7.0 (2013) to +5.4 (2017). On updated processing it went +4.4 (2017), +4.0 (2019), +2.65 (2020, COVID year), +3.6 (2022) and +3.8 (2025).
   - So the real 2017-2025 change is small. This matches `health_costs/`, where median MEPS OOP (premiums excluded) fell in real terms after 2010.
   - Note that SPM MOOP *includes* premiums, including Medicare Part B, unlike MEPS `TOTSLF`.

5. **Many more older people are near poor than are poor, and more so on the SPM.**
   - Official measure (Historical Table 5, people 65+):

     | | 1975 | 1985 | 1995 | 2005 | 2015 | 2019 | 2025 |
     |---|---|---|---|---|---|---|---|
     | Below 100% of threshold | 15.3 | 12.6 | 10.5 | 10.1 | 8.8 | 8.9 | 9.8 |
     | 100-149% | 19.7 | 16.0 | 14.8 | 13.5 | 10.8 | 8.8 | 8.4 |
     | Below 150% | 35.0 | 28.6 | 25.3 | 23.6 | 19.6 | 17.7 | 18.2 |
     | Below 200% | 50.3 | 42.0 | 39.6 | 36.8 | 31.1 | 26.8 | 27.2 |

     - The near-poor band shrank faster than poverty itself: 100-199% fell from 35.0% (1975) to 17.4% (2025).
     - Deep poverty (below 50%) went the other way, from 2.0% (1975, 1985) to 3.9% (2025). Its peak was 4.4% in 2022. Part of the rise is the 2019 processing change: on the same 2017 sample it is 3.2% under legacy processing and 3.8% under updated processing.
   - On the SPM (P60-290 Table 16, 2025, people 65+):
     - 5.1% are below 50% of the threshold, 10.2% at 50-99%, 14.5% at 100-149% and 11.8% at 150-199%.
     - So 29.8% are below 150% and 41.6% below 200%.
     - The official figures are 18.2% and 27.2%. The SPM 100-149% band (14.5%) is 1.7 times the official band (8.4%), because MOOP pushes people who sit just above the official line below 150%.
   - The microdata reproduce these numbers: 29.82% and 41.58%.

   [`output/near_poverty_65plus.csv`; SPM bands in `output/asec_65plus_poverty_by_group.csv`]

6. **Who is poor at 65+: people living alone, the oldest, women, and Black and Hispanic elders.**
   - Own computation from ASEC 2026 microdata (income year 2025). SEs are from Census replicate weights. Population 65+ is 65.2M, n = 26,202.

   | 2025, % | Official | SE | SPM | SE | SPM <150% | Social Security effect | MOOP effect |
   |---|---|---|---|---|---|---|---|
   | All 65+ | 9.8 | 0.3 | 15.4 | 0.3 | 29.8 | −32.1 | +3.8 |
   | 65-74 | 9.5 | 0.4 | 14.5 | 0.4 | 27.7 | −28.0 | +3.4 |
   | 75+ | 10.2 | 0.4 | 16.6 | 0.5 | 32.6 | −37.4 | +4.3 |
   | Men | 8.6 | 0.3 | 13.7 | 0.3 | 26.6 | −30.3 | +3.5 |
   | Women | 10.7 | 0.4 | 16.8 | 0.4 | 32.6 | −33.6 | +4.1 |
   | Living alone | 18.4 | 0.6 | 23.7 | 0.7 | 46.0 | −40.0 | +5.0 |
   | Living with others | 6.4 | 0.3 | 12.1 | 0.3 | 23.5 | −29.0 | +3.3 |
   | White alone, non-Hispanic | 7.3 | 0.3 | 11.9 | 0.3 | 24.5 | −33.2 | +3.5 |
   | Black alone | 19.2 | 0.9 | 25.8 | 1.0 | 45.9 | −31.6 | +5.1 |
   | Asian alone | 10.8 | 1.1 | 19.4 | 1.6 | 33.7 | −23.1 | +3.3 |
   | Hispanic (any race) | 17.1 | 1.1 | 27.8 | 1.2 | 49.2 | −27.5 | +5.0 |

   - **Living alone** is the strongest marker. Officially, 18.4% of people 65+ who live alone are poor, vs 6.4% of those living with others. People living alone depend most on Social Security: without it their SPM rate would be 63.7% (23.7 + 40.0).
   - **Age and sex:** 75+ and women are about 2-3 points higher on both measures.
   - **Race and Hispanic origin:**
     - The microdata race rates match Census's published 65+ rates within 0.1-0.4 points. Published, 2025: official 7.3 / 19.1 / 10.8 / 17.1 and SPM 11.9 / 25.9 / 19.2 / 27.6 for White non-Hispanic / Black alone / Asian alone / Hispanic. Sources: Historical Table 3 and P60-290 Table 8.
     - The SPM gap is largest for Hispanic (+10.7) and Asian (+8.6) elders. Both groups get a smaller Social Security effect than average (−27.5 and −23.1, vs −32.1), consistent with fewer or smaller benefits.
     - Long-run official series for Black people 65+: 36.3% (1975), 33.8% (1990), 21.8% (2000), 19.1% (2025). White non-Hispanic: 13.0%, 9.6%, 7.9%, 7.3%. Hispanic: 32.6%, 22.5%, 20.9%, 17.1%.
   - Trend 2019-2025 (consistent ASEC processing):
     - The official rate rose at 65-74 (7.9 to 9.5) but not at 75+ (10.3 to 10.2).
     - The official rate for people living alone rose from 16.1 to 18.4.
     - SPM rates rose in every group. Those rises mix the real change with the revised thresholds (see caveats).

   [`output/asec_65plus_poverty_by_group.csv` for 2018-2025 by group with SEs; `output/opm_65plus_by_race.csv`, `output/spm_65plus_by_race.csv`]

## Method

- **Published tables** (`scripts/published_tables.py`, which reads `raw/` and writes six CSVs):
  - Historical Poverty Tables 3 (by age and race, 1959-2025) and 5 (income-to-poverty ratios, all people and 65+, 1973/1975-2025).
  - P60-290 Table 8 (SPM by age and race, 2009-2025) and Table 16 (SPM ratio bands).
  - Effect-of-elements tables for people 65+ from every SPM report:
    - xlsx: P60-258 Table 5a, P60-261/265/268 Table A-6, P60-272/275 Appendix Table 6, P60-277/280 Table B-7, P60-283/287 Table B-6, P60-290 Table 5.
    - PDF tables read via `pdftotext`: P60-241 Tables 3a/3b, P60-244 and P60-247 Tables 5a/5b, P60-251 Table 5a, P60-254 Tables 4a/4b.
  - Reports up to P60-254 publish "the SPM rate if the element were excluded". The script turns these into effects (SPM rate minus the rate excluding the element), which is Census's later convention.
  - Each year's element effect is taken from the report where that year first appears, except where a newer report shows a same-year methodology comparison (2013 old/new questions, 2017 legacy/updated, 2024 original/revised). The CSV keeps every report's value, so revisions are visible. They are small (≤0.25 points) except at the method breaks.
- **Microdata** (`scripts/asec_spm.py RAW_DIR`): Census public-use CPS ASEC CSV files 2019-2026, income years 2018-2025. These files carry Census's own SPM variables.
  - SPM poor = `SPM_RESOURCES < SPM_POVTHRESHOLD`. It matches `SPM_POOR` exactly in every year.
  - Official poor = `PERLIS == 1`. Official <125% and <150% use `PERLIS` 2 and 3.
  - Element effects use Census's Table 5 method: the threshold is held fixed and the element is removed from resources.
    - Social Security: subtract the SPM unit's summed `SS_VAL`. SSI: summed `SSI_VAL`. MOOP: add back `SPM_MEDXPNS`.
  - Living alone = a one-person household.
  - Race: `PRDTRACE` 1/2/4 (alone). Hispanic: `PEHSPNON` = 1.
  - Weight is `MARSUPWT`, over the poverty universe (`PERLIS` > 0).
  - SEs use the 160 replicate weights in each zip (`asec_csv_repwgt_YYYY.csv`, merged on `PH_SEQ`/`PPPOS`): Var = 4/160 × Σ(θr − θ0)².
  - **Validation against P60-290 Table 5, people 65+, 2025:**

    | | Own computation | Published |
    |---|---|---|
    | SPM | 15.38 | 15.37 |
    | Social Security effect | −32.10 | −32.13 |
    | SSI effect | −0.98 | −0.99 |
    | MOOP effect | +3.80 | +3.83 |
    | Official rate | 9.77 | 9.8 |
    | Official <150% | 18.17 | 18.2 |

    Earlier years match their *original* reports to within about 0.1. For example, 2023 Social Security −33.04 vs −32.99 and MOOP +3.65 vs +3.75. 2021: −32.16 vs −32.19.
- Rebuild (from `poverty/`):

  ```
  python3 scripts/published_tables.py                 # needs pandas, openpyxl, xlrd, pdftotext (poppler)
  python3 scripts/asec_spm.py /tmp/asec               # downloads 8 ASEC zips (~1.26 GB) if missing; ~5 min
  ```

## Sources (all opened; copies in `raw/` unless noted)

- Census Historical Poverty Tables (people), CPS ASEC 1960-2026: Table 3 "Poverty Status of People by Age, Race, and Hispanic Origin: 1959 to 2025" and Table 5 "Percent of People by Ratio of Income to Poverty Level for All People and People Age 65 and Over: 1970 to 2025". https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-poverty-people/hstpov3.xlsx and `.../hstpov5.xlsx` (`raw/hstpov3.xlsx`, `hstpov5.xlsx`; `hstpov2.xlsx` and `hstpov6.xlsx` are kept but not used). Footnotes: https://www.census.gov/topics/income-poverty/poverty/guidance/poverty-footnotes/cps-historic-footnotes.html (`raw/cps_historic_footnotes.html`).
- *Poverty in the United States: 2025*, P60-290, Sept 2026. Report PDF: https://www2.census.gov/library/publications/2026/demo/p60-290.pdf. Tables: https://www2.census.gov/programs-surveys/demo/tables/p60/290/ (`table_8_spm_hist`, `table_5_spm_program_effect_rates`, `table_4_spm_person`, `table_16_spm_opm_plus_income_pov_ratios` and others, in `raw/p60_290/`).
- Earlier poverty and SPM reports and tables, at https://www2.census.gov/programs-surveys/demo/tables/p60/NNN/ (NNN = 258, 261, 265, 268, 272, 275, 277, 280, 283, 287; `raw/p60_NNN/`) and as report PDFs (`raw/spm_reports_pdf/`):
  - P60-241 (SPM 2010): https://www2.census.gov/library/publications/2011/demo/p60-241.pdf
  - P60-244 (2011): https://www2.census.gov/library/publications/2012/demo/p60-244.pdf
  - P60-247 (2012): https://www2.census.gov/library/publications/2013/demo/p60-247.pdf
  - P60-251 (2013): https://www2.census.gov/library/publications/2014/demographics/p60-251.pdf
  - P60-254 to P60-280: `https://www.census.gov/content/dam/Census/library/publications/YYYY/demo/p60-NNN.pdf`
  - P60-283: https://www2.census.gov/library/publications/2024/demo/p60-283.pdf
  - P60-287: tables only, plus the PDF from the p60/287 table folder.
- CPS ASEC public-use CSV files 2019-2026: https://www2.census.gov/programs-surveys/cps/datasets/20YY/march/asecpubYYcsv.zip. These are 139-184 MB each, so they are **not stored**. The data dictionary is https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar26.pdf.
- Not used: the Census SPM research files 2009-2023 (`https://www2.census.gov/programs-surveys/supplemental-poverty-measure/datasets/spm/spm_YYYY_pu.dta`, about 1.1 GB each). The published tables already cover 2009-2017, and no file exists for 2020, 2024 or 2025.

## Caveats

- **Series breaks: compare levels only within a consistent era.**
  - **2013 (2014 ASEC questionnaire redesign).** Census publishes 2013 twice: traditional questions on a 5/8 sample (official 65+ 9.5, SPM 14.6) and redesigned questions on a 3/8 sample (10.2, 15.6). The redesign raises measured 65+ poverty by about 0.7-1 point, and it also changes the element effects (Social Security −38.0 vs −35.5).
  - **2017 (2019 updated processing system).** Census publishes 2017 both ways: official 65+ 9.2 legacy vs 9.6 updated, SPM 14.1 vs 13.6. The MOOP effect falls from +5.42 to +4.40. The same break shows up in `cps/` as the jump in retirement-account withdrawals.
  - **2019 (revised SPM methodology, 2021).** 12.7 vs 12.8 for 65+.
  - **2019-2024 SPM thresholds revised (BLS re-release of July 17, 2026; P60-290).** Every 2019-2024 SPM figure in P60-290 differs from the figure first published. For example, 65+ in 2022 is now 13.8, against 14.1 in P60-280. **`spm_vs_opm_by_age_2009_2025.csv` uses the revised P60-290 values. The element-effect CSV and the microdata breakdowns for 2018-2024 use the original thresholds, because the public files carry the thresholds as first released.** Only 2025 (and 2024 in P60-290 Table 5) are on the revised basis. So the 2018-2024 microdata SPM rates sit about 0.1-0.4 above the revised published values. For example, the 2022 microdata value is 14.17 against a revised 13.8.
  - **Population controls.** 2010 Census-based controls start in 2009, 2020 Census-based controls in 2020, and Vintage 2025 controls in 2024 (P60-290). For 2024, SPM 65+ went from 15.0 (P60-287) to 15.1 (P60-290), with the reweight and the revised thresholds combined.
  - **2025 tax model** includes the new enhanced senior deduction for people 65+, which lowers SPM taxes. Census says the new tip and overtime deductions could not be modelled with CPS ASEC data. Federal income tax raises the 65+ SPM rate by only +0.2 points in both 2024 and 2025 (P60-290 Table 5), so this change is small for 65+.
- **What the measures count.**
  - The official measure is pre-tax money income only. It counts Social Security and retirement-account distributions but not MOOP, taxes or in-kind benefits. Its thresholds date from the 1960s and are indexed by CPI-U.
  - The SPM thresholds come from spending on food, clothing, shelter, utilities, telephone and internet, and vary by housing tenure and area. MOOP (premiums plus cost sharing) is subtracted from resources. **The SPM does not value Medicare itself, and does not count assets** (home equity or savings drawn down beyond reported income), so retirees with wealth but low income can be counted as poor.
- **Element effects are one-at-a-time.** Removing two elements does not equal the sum of their two effects. The "47.5% without Social Security" figure is static and ignores behaviour (work, saving, claiming).
- **Social Security in microdata.** Social Security for the SPM unit is summed from members' `SS_VAL`. The SPM resource total may include Census edits that are not visible in `SS_VAL`. The <0.15-point gap against the published effects suggests any such difference is small.
- **ASEC is the non-institutionalized population.** Nursing-home residents are excluded, which matters for the MOOP effect at 85+ (see `ltc/`).
- **Small groups.** In 2025 the microdata hold about 1,600 Asian and 3,200 Black and Hispanic persons aged 65+. Their SEs are 0.9-1.6 points, so year-to-year changes for these groups are mostly not significant.
- **Dropped or not verified.** The note in `notes/new_areas_2026-10-05.md` says the SPM is "several points higher, mainly because of MOOP". The numbers here support both parts for recent years: a 5.6-point gap and a +3.8 MOOP effect in 2025. The gap is not the MOOP effect alone, though; thresholds, taxes and in-kind benefits net out the rest. I found no Census table for 2009-2017 SPM by 65-74/75+, sex or living arrangement, so those breakdowns cover only 2018-2025. Before 2018 they would need the 1-GB SPM research files.
