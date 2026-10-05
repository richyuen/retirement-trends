# Social Security solvency trends (Trustees Reports, 1982-2026)

Built 2026-10-05 for candidate area 4 in `notes/new_areas_2026-10-05.md`. Everything comes from the annual Social Security (OASDI) and Medicare (HI) Trustees Reports. The copies used are the House Documents on govinfo.gov, because ssa.gov blocks this environment. All figures use the Trustees' intermediate ("best estimate") assumptions unless a line says otherwise. Percentages are used throughout, following Richard's preference.

## Findings

1. **The combined trust fund depletion date has stayed in 2033-2035 for 15 straight reports, so the time left keeps shrinking.** Year of projected combined OASI+DI reserve depletion, by report year: 1983 none (positive for 75 years); 1985 2049; 1990 2043; 1994 2029; 1995 2030; 2000 2037; 2002 2041; 2005 2041; 2009 2037; 2010 2037; 2012 2033; 2015 2034; 2020 2035; 2025 2034; **2026 2034**. Every report from 2012 to 2026 put the date at 2033, 2034 or 2035. Measured from the report year, the runway fell from 64 years (1985 report) to 37 (2000) and to **8 (2026)**. [2026 Trustees Report Table VI.B1, pp. 182-183. The year printed in each report's own tables agrees in all 28 reports checked, 1995-2026: `output/depletion_by_report.csv`]

2. **The retirement fund (OASI) runs out first: late 2032, two years before the combined fund.** In the 2026 report, OASI reserves are depleted in Q4 2032. After that, OASI income covers **78% of scheduled OASI benefits**, falling to 62% by 2100. The combined OASDI fund is depleted in Q3 2034, with **83% payable**, falling to 65% by 2100. DI no longer runs out within the 75 years. It was projected to run out in 2016 (2013-15 reports) and was rescued by the 2015 tax reallocation. Separate OASI and DI funds are the current law; the "combined" date assumes money is moved between them. [2026 report pp. 2, 5, 15; Table II.A1]

3. **The share of benefits payable at depletion has been roughly 73-83% in every report since the 1990s, so the cut is about 17-27%.** OASDI payable share in the depletion year: 1996 77%; 1997-98 about three-quarters; 2000 72%; 2001-04 73%; 2005-06 74%; 2010 78%; 2011-14 77%; 2015-16 79%; 2017 77%; 2018 79%; 2019 80%; 2020 79%; 2021 78%; 2022-23 80%; 2024 83%; 2025 81%; 2026 83%. The OASI-only payable share was 75-79% in the 2016-2026 reports. Lowest was 72% (2000 report). **The long-run figure got worse in 2026.** The payable share at the end of the 75-year window was 72-75% in the 2010-2025 reports but is **65% (OASDI) / 62% (OASI) for 2100** in the 2026 report. That is the same report that cut the ultimate fertility assumption to 1.75 children per woman from 1.90 (p. 3) and names fertility as the largest contributor to its higher deficit (p. 6). [each report's Highlights / section II.D; `raw/curated_report_values.csv`]

4. **The 75-year actuarial deficit has more than doubled since the late 1990s.** As % of taxable payroll: +0.02 (1983, after the 1983 Amendments), -0.91 (1990), -2.17 (1995), -2.23 (1997, 1990s peak), -1.86 (2001, the low point after the 1990s boom), -1.92 (2010), -2.67 (2012), -3.21 (2020), -3.82 (2025), **-4.42 (2026)**, which equals about 1.5% of GDP. The 2026 jump (-0.60) is the largest since 1994. The 2026 report says fertility is the largest cause. The 2025 drop came from the Social Security Fairness Act (repeal of WEP/GPO) and the slower path to ultimate fertility. A deficit of X% means payroll taxes would need to rise by about X points from now on, or costs fall by the same amount. [Table VI.B1; 2026 pp. 6, 185]

5. **Closing the gap now would take a 25% across-the-board benefit cut or a payroll tax of 16.65%. Waiting until 2034 makes it 28.5% or 17.30%.** These are the 2026 report's illustrations for 75-year solvency. Options starting in January 2026: raise the payroll tax from 12.40% to 16.65%; cut all current and future benefits by 25.2%; or cut by 30.3% for people newly eligible from 2026 only. Options starting in 2034: a tax of 17.30%, or a cut of 28.5% for everyone. [2026 report p. 7]

6. **Workers per beneficiary: 5.1 in 1960, 3.3-3.4 from 1975 to 2005, 2.6 now, 2.3 by 2035.** OASDI covered workers per beneficiary: 1960 5.1; 1970 3.7; 1980 3.2; 1990 3.4; 2000 3.4; 2010 2.9; 2020 2.7; 2025 2.6; then 2.4 (2030), 2.3 (2035-40), 2.2 (2050), 1.9 (2075-2100). Put the other way, beneficiaries per 100 workers go from 20 (1960) to 29-31 (1975-2005), 38 (2025), 43 (2035) and 54 (2085). The range across Trustees scenarios widens later: 2.4 (low-cost) to 2.2 (high-cost) in 2035, and 2.6 to 1.3 by 2100. [2026 Table IV.B4, pp. 69-71; `output/workers_per_beneficiary_1945_2100.csv`]

7. **Cost has passed income for good. Cost rises from 5.3% to about 6.9% of GDP, while income stays near 4.4-4.8%.** As % of taxable payroll: OASDI cost was 10.4% in 2000, 13.5% in 2010 and 15.24% in 2025. Non-interest income was 12.5-13.5% throughout. Cost has exceeded non-interest income every year since 2010. Projected cost: 15.37% (2026), 15.8% (2035), peak 20.45% (2085), 20.0% (2100). Income: 12.91% (2026) to 13.45% (2100). As % of GDP: cost 4.05% (2000) to 4.73% (2010), 5.23% (2025), 5.70% (2035), about 6.9% at the 2084-85 peak and 6.69% in 2100. Income is 4.42% (2026), peaks at 4.76% (2035) and is 4.49% in 2100. The 2025 cost jump (14.38% to 15.24% of payroll) coincides with the Social Security Fairness Act. 2025 OASI net benefit payments rose 9.3%, "due primarily to" its implementation (p. 33). [2026 Tables IV.B1 pp. 59-61 and IV.B3 pp. 67-68; p. 4; pp. 17-18]

8. **What a cut would mean for retirees' income.** This is a static calculation. It assumes no behavioral response and ignores taxes, SSI and other programs. Social Security is 32.3% of aggregate income for people 65+ (CPS ASEC 2026, income year 2025, from `../spending/cps_income/`). The cut at depletion is 22% under the OASI-only law path from 2032, or 17% if the funds are combined from 2034.

   | Group (CPS ASEC 2026) | SS share of income | Income loss, 22% cut (OASI, 2032) | Income loss, 17% cut (OASDI, 2034) |
   |---|---|---|---|
   | All 65+, aggregate | 32.3% | 7.1% | 5.5% |
   | Aged units with SS >= 50% of income (58.3% of beneficiary units) | >= 50% | >= 11.0% | >= 8.5% |
   | Aged units with SS >= 90% (31.9%) | >= 90% | >= 19.8% | >= 15.3% |
   | Aged units with SS = 100% (19.7%) | 100% | 22.0% | 17.0% |

   By 2100 the scheduled-benefit gap is 35-38%. The immediate fix illustration (25.2% cut) would cost the aggregate 65+ population 8.1% of income. Survey data overstate reliance. With admin records, about 42-50% of aged units rely on SS for at least half their income, and 12-18% for at least 90% (see `../spending/README.md`). The "most-reliant" rows are therefore smaller groups than the CPS shares suggest. The per-group losses still hold for anyone at those reliance levels. Lower-income retirees, who rely most on Social Security, lose the largest share of their income. [`output/cut_implications.csv`]

9. **Medicare Hospital Insurance (Part A) trust fund: depleted in Q2 2033, 89% payable then.** HI depletion year by report: 1996 2001; 1997 2001; 1998 2008 (after the Balanced Budget Act of 1997); 2000 2025; 2001 2029; 2002 2030; 2003 2026; 2004 2019; 2005 2020; 2006 2018; 2009 2017; 2010 2029 (after the ACA); 2011-12 2024; 2013 2026; 2014-15 2030; 2016 2028; 2017 2029; 2018-21 2026; 2022 2028; 2023 2031; 2024 2036; 2025 2033; **2026 2033**. The HI date swings much more than Social Security's, because it depends on health-cost growth and on legislation. The HI actuarial deficit is 0.56% of payroll in 2026, up from 0.42% in 2025. Income covers 89% of HI costs at depletion and 93% by 2100. Total Medicare spending is projected to rise from 3.9% to 7.5% of GDP by 2100. [2026 Medicare Trustees Report (H. Doc. 119-164) Table II.A1 p. 8 and pp. 8-9, 61; earlier HI reports; `output/hi_depletion_by_report.csv`]

### Main table: what each OASDI report projected
Intermediate assumptions. AB = 75-year actuarial balance, % of taxable payroll. "Payable" = % of scheduled OASDI benefits payable in the combined-fund depletion year; OASI-only in brackets where the report states it. "none" = not depleted within 75 years. Blank = not in a report reachable here.

| Report | OASI | DI | OASDI | Payable at depletion | Payable, end of 75 yrs | AB |
|---|---|---|---|---|---|---|
| 1985 | | | 2049 | | | -0.41 |
| 1990 | | | 2043 | | | -0.91 |
| 1994 | | | 2029 | | | -2.13 |
| 1995 | 2031 | 2016 | 2030 | | | -2.17 |
| 1996 | 2031 | 2015 | 2029 | 77 | 71 | -2.19 |
| 1997 | 2031 | 2015 | 2029 | ~75 ("about 3/4") | ~67 ("about 2/3") | -2.23 |
| 1998 | 2034 | 2019 | 2032 | ~75 ("about 3/4") | | -2.19 |
| 1999 | 2036 | 2020 | 2034 | | | -2.07 |
| 2000 | 2039 | 2023 | 2037 | 72 | ~67 ("about 2/3") | -1.89 |
| 2001 | 2040 | 2026 | 2038 | 73 | 67 | -1.86 |
| 2002 | 2043 | 2028 | 2041 | 73 | 66 | -1.87 |
| 2003 | | | 2042 | | | -1.92 |
| 2004 | 2044 | 2029 | 2042 | 73 | 68 | -1.89 |
| 2005 | 2043 | 2027 | 2041 | 74 | 68 | -1.92 |
| 2006 | 2042 | 2025 | 2040 | 74 | 70 | -2.02 |
| 2007 | | | 2041 | | | -1.95 |
| 2008 | | | 2041 | | | -1.70 |
| 2009 | | | 2037 | | | -2.00 |
| 2010 | 2040 | 2018 | 2037 | 78 | 75 | -1.92 |
| 2011 | 2038 | 2018 | 2036 | 77 | 74 | -2.22 |
| 2012 | 2035 | 2016 | 2033 | | | -2.67 |
| 2013 | 2035 | 2016 | 2033 | 77 | 72 | -2.72 |
| 2014 | 2034 | 2016 | 2033 | 77 | 72 | -2.88 |
| 2015 | 2035 | 2016 | 2034 | 79 | 73 | -2.68 |
| 2016 | 2035 | 2023 | 2034 | 79 (77) | 74 | -2.66 |
| 2017 | 2035 | 2028 | 2034 | 77 (75) | 73 | -2.83 |
| 2018 | 2034 | 2032 | 2034 | 79 (77) | 74 | -2.84 |
| 2019 | 2034 | 2052 | 2035 | 80 (77) | 75 | -2.78 |
| 2020 | 2034 | 2065 | 2035 | 79 (76) | 73 | -3.21 |
| 2021 | 2033 | 2057 | 2034 | 78 (76) | 74 | -3.54 |
| 2022 | 2034 | none | 2035 | 80 (77) | 74 | -3.42 |
| 2023 | 2033 | none | 2034 | 80 (77) | 74 | -3.61 |
| 2024 | 2033 | none | 2035 | 83 (79) | 73 | -3.50 |
| 2025 | 2033 | none | 2034 | 81 (77) | 72 | -3.82 |
| 2026 | 2032 | none | 2034 | 83 (78) | 65 (62) | -4.42 |

The full 1982-2026 OASDI and AB series (every year) is in `output/oasdi_history_tableVIB1_1982_2026.csv`.

## Method
1. `scripts/find_trustees_docs.py` walks govinfo's public CDOC browse service (`https://www.govinfo.gov/wssearch/rb/cdoc/...`; the api.govinfo.gov search needs a key and DEMO_KEY was rate-limited). It lists every House/Senate document titled as an OASDI, HI or SMI Trustees Report, writing `raw/govinfo_trustees_index.csv`. The OASDI reports for 1992, 1999, 2003, 2007, 2008, 2009 and 2012 are not on govinfo as House Documents. The 2017 OASDI report (115hdoc54) is on govinfo but missing from the browse tree.
2. `scripts/fetch_reports.sh` downloads 26 OASDI reports (1995-2026) and 26 HI reports (1996-2026, missing 1999, 2003, 2007-09) to a scratch folder. It converts them with `pdftotext -layout` and keeps gzipped text in `raw/text/` (`oasdi_YYYY.txt.gz`, `hi_YYYY.txt.gz`). The PDFs are not kept; the 2024 and 2026 OASDI PDFs are 87 and 73 MB.
3. `scripts/ocr_scanned.sh` handles the 1995-2000 reports, which are image-only scans. It OCRs their front sections (pages 1-60 for OASDI 1995-98, 1-40 otherwise) with tesseract and writes `raw/text/*_ocr.txt.gz` with page markers. It does the same for the 2018 OASDI report, whose text layer has a broken font encoding. Two OCR'd fractions ("about 3/4", "about 2/3", 1997) were checked against the page image.
4. `scripts/parse_tables.py` parses four multi-year tables from the 2026 OASDI text into `output/`: VI.B1, IV.B4, IV.B1 and IV.B3. Printed page = PDF page - 8 in that report.
5. `raw/curated_report_values.csv` holds 200+ values read by hand from individual reports: depletion years, payable %, AB, the 2026 solvency-gap figures and HI dates. Each value has a verbatim quote. `scripts/build_series.py` re-finds every quote in the report text and checks that the value appears in it. Current result: all verified. It also cross-checks each report's own combined depletion year and AB against 2026 Table VI.B1 (all agree: 28 depletion years, 27 AB values). It then writes `depletion_by_report.csv`, `hi_depletion_by_report.csv` and `cut_implications.csv`, using the CPS shares from `../spending/cps_income/output/` (read only).

Rebuild: `bash scripts/fetch_reports.sh && bash scripts/ocr_scanned.sh && python3 scripts/parse_tables.py && python3 scripts/build_series.py` (set `PDFDIR` for the scratch PDF folder; needs poppler-utils, tesseract-ocr, pandas).

## Outputs
- `output/oasdi_history_tableVIB1_1982_2026.csv`: AB, summarized income/cost rates and combined depletion year for every report 1982-2026.
- `output/depletion_by_report.csv`: wide table by report year. It holds the Table VI.B1 values plus what each report itself states for OASI/DI/OASDI depletion, payable % (at depletion and at end of the 75-year window) and AB, and years from report to depletion.
- `output/hi_depletion_by_report.csv`: Medicare HI depletion year by report (plus 2025-26 AB and 2026 payable %).
- `output/workers_per_beneficiary_1945_2100.csv`: covered workers, beneficiaries, workers per beneficiary, beneficiaries per 100 workers, for history and the three scenarios.
- `output/income_cost_pct_payroll.csv`, `output/income_cost_pct_gdp.csv`: OASI/DI/OASDI income, cost and balance for 1990-2025 (history, 5-year steps to 2015) and 2026-2100 for the three scenarios.
- `output/cut_implications.csv`: income loss by reliance group for four cut scenarios.

## Sources
- 2026 OASDI Trustees Report, H. Doc. 119-163: https://www.govinfo.gov/content/pkg/CDOC-119hdoc163/pdf/CDOC-119hdoc163.pdf. Used: Table II.A1 (p. 2); Highlights pp. 3-7; section II.D pp. 15-18; Tables IV.B1 (pp. 59-61), IV.B3 (pp. 67-68), IV.B4 (pp. 69-71) and VI.B1 (pp. 182-183); appendix text p. 185; Fairness Act p. 33; stochastic range p. 24.
- Earlier OASDI reports, all at `https://www.govinfo.gov/content/pkg/CDOC-<id>/pdf/CDOC-<id>.pdf`: 1995 104hdoc57, 1996 104hdoc228, 1997 105hdoc72, 1998 105hdoc243, 2000 106hdoc221, 2001 107hdoc55, 2002 107hdoc196, 2004 108hdoc176, 2005 109hdoc18, 2006 109hdoc103, 2010 111hdoc137, 2011 112hdoc23, 2013 113hdoc33, 2014 113hdoc139, 2015 114hdoc51, 2016 114hdoc145, 2017 115hdoc54, 2018 115hdoc133, 2019 116hdoc28, 2020 116hdoc123, 2021 117hdoc63, 2022 117hdoc127, 2023 118hdoc21, 2024 118hdoc137, 2025 119hdoc62. Values come from each report's Highlights and its section II.D table "Projected maximum trust fund ratios ... and trust fund exhaustion/depletion dates" (II.D1 or II.D2), plus table II.D3 (2001-02).
- Medicare (HI and SMI) Trustees Reports: 2026 H. Doc. 119-164 (Table II.A1 p. 8; pp. 8-9; p. 61). Also 1996 104hdoc227, 1997 105hdoc73, 1998 105hdoc245, 2000 106hdoc262 (corrected 2000 report), 2001 107hdoc54, 2002 107hdoc197, 2004 108hdoc177, 2005 109hdoc17, 2006 109hdoc102, 2010 111hdoc138, 2011 112hdoc22, 2012 112hdoc101, 2013 113hdoc34, 2014 113hdoc140, 2015 114hdoc50, 2016 114hdoc146, 2017 115hdoc53, 2018 115hdoc132, 2019 116hdoc29, 2020 116hdoc122, 2021 117hdoc62, 2022 117hdoc126, 2023 118hdoc22, 2024 118hdoc136, 2025 119hdoc63.
- CPS ASEC 65+ income shares and SS reliance: `../spending/cps_income/output/income_share_65plus_wide.csv` and `ss_reliance_wide.csv` (ASEC 2026, series C, production file).

## Caveats
- **Combined vs separate funds.** Under current law OASI and DI are separate, so retirees face the OASI date (2032) and OASI payable share (78%). The combined date (2034, 83%) is a hypothetical that assumes reallocation. The 2014-15 reports call the combined fund "theoretical"; later reports call it "hypothetical" or present it as a combined basis. Both appear above; don't mix them.
- **Method changes in AB:** the actuarial balance used the average-cost method in 1973-87. Starting reserves were added in 1988 and an ending target fund in 1991 (Table VI.B1 footnote b). So pre-1991 values are not strictly comparable. The valuation-period shift alone worsens the AB a little every year.
- **Payable % definitions vary slightly.** The 1996-2002 reports quote tax revenue as a % of expenditures. From 2004 they quote % of scheduled benefits, and 2013-2025 phrase it as % of program cost. The 1997-98 reports give fractions ("about 3/4", "almost 3/4"), recorded as about 75. The 1995 report gives no payable share.
- **Gap years** (1999, 2003, 2007-09, 2012): the combined date and AB come from Table VI.B1. OASI/DI dates for 1999 come from the 2000 report ("3 years later than estimated in last year's report"), and for 2012 from the 2013 report ("unchanged from last year's report"). OASI/DI for 2003 and 2007-09 are not available. The 2003 HI date comes from the 2004 report, 2000 from the 2001 report and 2009 from the 2010 report. HI 2007-08 is not available.
- The cut calculation is mechanical. It uses aggregate shares (persons) and reliance thresholds (aged units) from the CPS, which overstates reliance relative to admin data. It ignores benefit taxation, SSI, behavioral responses and the fact that payable % keeps falling after the depletion year.
- The 2025 historical cost rate includes Social Security Fairness Act retroactive payments, so it is not a clean trend point.
- These are projections that change each year. In the 2026 report's stochastic simulations, 95% of outcomes put combined depletion between 2032 and 2039 (p. 24).

## Dropped or not reachable
- SSA's own pages (ssa.gov/oact/TR, Actuarial Note 2026.8 on year-by-year AB changes) are blocked (403). Their content is covered by the govinfo copies and Table VI.B1.
- CBO long-term Social Security projections (cbo.gov) and CRS reports (congress.gov, crsreports.congress.gov) are blocked (403). The CRS table of depletion dates by report was replaced by Table VI.B1.
- 1990-1994 OASDI reports exist on govinfo only as Serial Set scans of 70-106 MB. They were not downloaded; Table VI.B1 covers their combined dates and AB. The 1995 HI report is not on govinfo under the expected number.
- The commonly cited "about 20% cut" is consistent with the 17-23% range above. The sources say 17-22% for 2026 and 23% for "a reduction in all scheduled benefits" in the 2013-14 reports; "about 20%" itself is not a Trustees figure.
