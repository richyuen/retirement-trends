# Working longer and later retirement

Labor force participation of older Americans by age and sex (BLS CPS, 1948-2025), full- vs part-time work, BLS projections to 2035, the CRR average retirement age (1962-2025), Social Security claiming trends (CRR from SSA data, plus a CPS ASEC receipt check), and the usual explanations. Built 2026-10-05. All rates are annual averages of unadjusted monthly CPS data. **2025 annual averages cover 11 months**: October 2025 was not collected because of the government shutdown (BLS footnote 11).

## Findings

1. **Participation at 65+ fell for 40 years, then nearly doubled, and has been flat since 2019.** 65+ LFPR (both sexes) was 27.0% in 1948, bottomed at 10.8% in 1985, was 12.1-12.4% in 1994-1997, peaked at 20.2% in 2019 and was 19.1% in 2025 (19.5% in 2024). Every band 65+ peaked in 2019 and is 0.6-1.0 points lower in 2025: 65-69 34.3 -> 33.3, 70-74 19.8 -> 18.8, 75+ 9.1 -> 8.5. The dip since 2019 is not age mix: holding the 2019 mix of 65-69/70-74/75+ fixed gives 19.3% for 2025. [BLS LN series; `output/lfpr_wide_both_sexes.csv`]

   | LFPR, both sexes (%) | 1976 | 1985 | 1994 | 2000 | 2010 | 2019 | 2025 |
   |---|---|---|---|---|---|---|---|
   | 55-61 | 62.5 | 61.2 | 64.2 | 66.0 | 70.4 | 70.5 | 72.5 |
   | 62-64 | 41.0 | 36.7 | 38.7 | 40.2 | 49.8 | 52.5 | 53.6 |
   | 65+ | 13.1 | 10.8 | 12.4 | 12.9 | 17.4 | 20.2 | 19.1 |
   | 65-69 | 21.3 | 18.4 | 21.9 | 24.5 | 31.5 | 34.3 | 33.3 |
   | 70-74 | 12.8 | 10.7 | 11.8 | 13.5 | 18.0 | 19.8 | 18.8 |
   | 75+ | 5.2 | 3.9 | 5.4 | 5.3 | 7.4 | 9.1 | 8.5 |

2. **Before 65, work kept rising after COVID.** 62-64 LFPR rose from a low of 36.2% (1987) to 53.6% (2024 and 2025), and 55-61 from 61.0% (1984) to 72.5% (2025, a record). So the post-2019 stall is a 65+ story; people near the usual claiming and withdrawal ages are working more than ever.

3. **Men recovered to about 1970s levels; women's gains are new.**
   - Men 65+: 46.8% (1948) -> 15.6% low (1993) -> 24.7% (2019) -> 23.1% (2025). Men 65-69: 43.4% in 1967, 24.4% low in 1985, 39.4% in 2019, 38.1% in 2025. Men 62-64: 56.1% (1976), 45.0% low (1995), 58.2% (2019 and 2025). Men 55-61 (78.1% in 2025) are still below 1976 (81.1%).
   - Women 65+: 9.1% (1948), 7.3% low (1985), 16.4% (2019), 15.7% (2025). Women 62-64: 28.3% (1976) -> 49.4% (2025, a record); women 55-61: 45.9% -> 67.0%. Women's rise reflects both later retirement and each cohort having worked more over its life (CRR IB 25-8).

   | LFPR 2025 vs 2019 (%) | Men 2019 | Men 2025 | Women 2019 | Women 2025 |
   |---|---|---|---|---|
   | 55-61 | 76.8 | 78.1 | 64.6 | 67.0 |
   | 62-64 | 58.2 | 58.2 | 47.3 | 49.4 |
   | 65-69 | 39.4 | 38.1 | 29.8 | 28.9 |
   | 70-74 | 24.1 | 22.3 | 16.1 | 15.7 |
   | 75+ | 12.1 | 11.1 | 6.8 | 6.6 |

4. **BLS projects further gains at 55-64 and 65-74 to 2035, and a falling overall 55+ rate (aging).** BLS Employment Projections 2025-35 (Table 3.3, last modified Sept 1, 2026): 55-64 rises from 66.6% (2025) to 69.5% (2035), 65-74 from 26.7% to 29.1%, 75+ from 8.5% to 10.1%. 55+ overall falls from 38.1% to 36.7% because more of the group is 75+. By sex for 65-74: men 31.1 -> 33.0, women 22.8 -> 25.6. That projection runs against CRR's view (finding 8) that the drivers have played out. [`output/lfpr_bls_projections_2035.csv`]

5. **Most older workers work full time, and the full-time share has grown.** Of employed people 65+, 38.3% usually worked part time in 2025, down from 43.1% in 2009 (the first year BLS publishes this split for 65+; 37.9% in 2019). At 55-64 (by subtraction) the part-time share fell from 17.2% (2009) to 14.2% (2025). As a share of everyone 65+, 11.4% worked full time and 7.1% part time in 2025 (9.2% and 6.9% in 2009), so the rise in work at 65+ since 2009 is mainly full time. For 55+ as a whole the part-time share was 23.5% in 1986 and 21.5% in 2025 (men 16.3 -> 16.5, women 33.7 -> 27.1). The 55+ figure is pulled up over time by the growing weight of the 65+ group, and it jumps at the 1994 redesign (26.0% in 1993, 28.2% in 1994). [`output/ft_pt_older_workers.csv`]

6. **The average retirement age is up about three years since the mid-1990s and flat for a decade.** CRR defines it as the age at which the CPS LFPR consistently falls below 50%. Men: 66 (1962) -> 62 (1986-1995) -> 64 (2010) -> 65 (2016-2025, except 64 in 2018); 64.6 in 2024 and 64.8 in 2025. Women: 53 (1962) -> 57 (1986) -> 60 (1995) -> 62 (2007-2010) -> 62-63 since 2013; 62.6 in 2024 and 63.3 in 2025. [CRR, Average Retirement Age for Men and Women, 1962-2025; IB 25-8; `output/crr_average_retirement_age.csv`]

7. **Fewer people claim Social Security at 62, and more wait past the FRA.**
   - *Claim-year data (SSA, via CRR):* the share of retired-worker awards taken at 62 was about 55% (men) and 60% (women) until about 2005, and was 31%/34% in 2019. Between 2019 and 2023: men at 62 31% -> 26%, at 67+ 19% -> 26%; women at 62 34% -> 27%, at 67+ 20% -> 25%. [CRR IB 21-9; IB 25-10 Fig 1; `output/crr_claiming_age_distribution.csv`]
   - *Cohort data (better for trends, since the number of 62-year-olds doubled from 2.0M in 1997 to 4.3M in 2023):* the share of men turning 62 who claimed at 62 was 51.9% (1985), 56.0% (1996) and 35.6% (2013); women 63.6%, 62.8%, 39.5%. CRR puts it at about one-quarter of 62-year-olds by 2019. [IB 15-8 Table 1; IB 21-9]
   - *Average claiming age* rose about two years (63 to 65), a little less than the three-year rise in the retirement age, because some people claim before they stop working. [IB 25-10]
   - *CPS ASEC check (our tabulation, survey data):* the share of people aged 63-64 at the March interview who received any Social Security in the prior year fell from 41.8% (ASEC 2010) to 33.3% (2019) and 29.5% (2026). At 65-66 it fell from 69.4% to 59.1% and 52.0%. At 60-61, before retirement eligibility (disability and survivor benefits only), it stays at 9-13%. Men 63-64: 38.3 -> 27.6; women 44.9 -> 31.2 (2010 -> 2026). The SS question is unaffected by the 2014 and 2019 ASEC changes: same-year file pairs differ by at most 1.9 points. [`output/cps_ss_receipt_by_age.csv`]

8. **Why: the reasons usually cited, and whether they still apply** (CRR IB 25-8, Munnell 2025, which reviews the literature):
   - *Social Security rules:* the FRA rose from 65 to 67 (cohorts turning 62 in 2000-2022), the earnings test was relaxed and then removed at the FRA, and the delayed retirement credit rose from 3% to 8% a year. The benefit at 62 fell from 80% of PIA to 70%, and the benefit at 70 is 132% of PIA for those born 1943-54 and 124% for those born 1960 or later [2026 Trustees Report Table V.C3]. One estimate (Coile 2025, cited in IB 25-8) attributes about one-fifth of the rise in work at 65-69 to these changes. These changes are now fully phased in.
   - *DB to 401(k):* DB plans built in incentives to retire; 401(k) participants retire a year or two later on average than similar DB-covered workers (studies cited in IB 25-8). The shift is essentially complete.
   - *Education:* more older workers have degrees, and they work longer, but the share of men 50-54 with a degree has been flat since about 2000. BLS's own 2025 LFPR at 65+ by education (series LNU0131CB67-6E) is in `raw/ln.series` but was not tabulated.
   - *Health and longevity:* men's life expectancy at 65 rose about 3.2 years since 1990 (IB 25-8), but gains in disability-free life expectancy stalled after about 2005.
   - *Other:* declining retiree health insurance (work until Medicare at 65), less physically demanding jobs, and couples coordinating retirement. The 2026 Trustees Report gives a similar list (pp. 120-121).
   - *Outlook:* CRR concludes these drivers have "run their course", so further large increases in the average retirement age are unlikely. BLS (finding 4) still projects modest gains.

**Ties to the rest of the project.** The 65+ LFPR path (11.9% in 1998, 20.2% in 2019, 19.1% in 2025) matches the rise and plateau in the earnings share of 65+ income in `spending/` (16.8% to about 27-31%). The rise at 62-64 (49.8% in 2010, 53.6% in 2025) and the drop in early claiming fit `scf_6064/`'s finding that more 60-64 account holders are working (70.2% to 77.0%), with lower withdrawals. Inference: more work and later claiming before 65 mean less need to draw on accounts early. After 65, flat participation since 2019 means work is no longer adding to that effect.

## Method
- **LFPR**: BLS CPS (LN database) annual averages (period M13) of unadjusted series. Where BLS publishes a rate it is used directly: 55-59, 55-64, 65+, 65-69, 70-74, 75+ for both sexes and by sex; 60-61 and 62-64 for men and women only. Bands BLS doesn't publish are computed from labor force and population levels (thousands): 55-61 = (55-59 + 60-61); 62-64 and 60-61 for both sexes = men + women. Check against published rates: 1,430 year/band/sex pairs where both exist, max difference 0.13 points (`output/lfpr_check_published_vs_computed.csv`). Coverage: 65+ and 55-64 from 1948; 55-59, 65-69, 70-74 and 75+ from 1967 (some published rates start later, e.g. 65-69 both sexes 1982, 75+ men 1987, so earlier years are computed from levels); 60-61, 62-64 and 55-61 from 1976. The `source` column says which method each value used.
- **Full/part time**: "usually work full time" (35+ hours) vs "usually work part time", which sum to total employment (checked). 55+ by sex from 1986 (LNU02524230-32, LNU02624230-32); 65+ annual-only series from 2009 (LNU02500097, LNU02600097); 55-64 = 55+ minus 65+.
- **CRR retirement age**: CRR's published table (whole years) plus the one-decimal labels on its chart for the latest years. We did not recompute it, because it needs single-year-of-age LFPR, which the BLS series don't provide and the project's CPS ASEC extract lacks (it has no labor-force variables).
- **Claiming**: CRR figures are read from published text, tables and bar labels (checked against the rendered page). CPS ASEC: weighted (MARSUPWT) share with SS_YN = 1, by age at interview, using the cps/ thread's extract (production files; 2014 = traditional 5/8 file).

## Caveats
- **1994 CPS redesign** (January 1994; the LN flat files don't footnote it, but the break is visible in the data). Measured 65+ LFPR jumps from 11.2% (1993) to 12.4% (1994) and 75+ from 4.3% to 5.4%; part-time shares also jump. Treat 1993-94 changes as a break; the long-run turnaround (low in 1985, rising since the mid-1990s) is visible on both sides.
- **Population controls**: BLS updates CPS population controls periodically (usually in January) without revising earlier years. This mainly moves levels (counts), not rates, which is one reason to use percentages here. The only control change the LN flat files flag in the series used is January 2026 (footnote 12); 2025 rates are not affected. We did not verify the dates of earlier control changes from a source opened here, so they are not listed.
- **2025** = 11-month average (no October data). 2020-2021 COVID dip.
- **BLS projections** use BLS's own historical values, which may differ slightly from CPS series because of rounding. They give 65-74, not 65-69/70-74, and no 65+ total.
- **Claiming data are SSA's**, reached only through CRR, because ssa.gov (Annual Statistical Supplement Table 6.B5) returns 403 here. We could not get an annual series of claim-year shares by age (CRR shows it only as a chart, 1985-2023) or the share claiming at exactly 70; CRR groups 67+. The cohort series is published only for selected years (1985, 1996, 2013) plus the about-25% statement for 2019.
- **CPS ASEC SS receipt** is survey-reported, includes disability, survivor and spouse benefits, refers to the prior calendar year, and uses age at interview. It is a direction check, not a claiming rate. No standard errors were computed (n is about 3,300 per two-year band in 2026; see the `n` column).
- The CRR average retirement age is rounded to whole years in its table, so year-to-year moves of ±1 (e.g., men 65 -> 64 -> 65 in 2017-2019) are rounding noise.

## Sources
- BLS, Labor Force Statistics from the CPS, LN flat files: `https://download.bls.gov/pub/time.series/ln/` (ln.series, ln.data.1.AllData, ln.footnote, mapping files). The AllData file (392 MB) is not kept; `raw/ln_subset.tsv` holds the 89 series used. Requests need a browser-like User-Agent.
- BLS Employment Projections, Table 3.3 "Civilian labor force participation rates by age, sex, race, and ethnicity, 2005, 2015, 2025, and projected 2035": `https://www.bls.gov/emp/tables/civilian-labor-force-participation-rate.htm` (this bls.gov page was reachable on 2026-10-05; saved in `raw/bls_projections/`).
- CRR, "Average Retirement Age for Men and Women, 1962-2025" (Nov 2025): `https://crr.bc.edu/wp-content/uploads/2025/11/Average-retirement-age.pdf`; 1962-2024 edition: `https://crr.bc.edu/wp-content/uploads/2025/03/Average-retirement-age.pdf`.
- Munnell, A. "Will the Average Retirement Age Keep Rising?" CRR Issue in Brief 25-8, April 2025: `https://crr.bc.edu/wp-content/uploads/2025/04/IB_25-8.pdf`.
- Chen, Munnell and Gok, "How Much Have Social Security Claiming Ages Increased?" IB 25-10, May 2025: `https://crr.bc.edu/wp-content/uploads/2025/05/IB_25-10.pdf`; Munnell, MarketWatch blog of July 7, 2025, summarizing it (`raw/crr/`).
- Chen and Munnell, "Pre-COVID Trends in Social Security Claiming," IB 21-9, May 2021: `https://crr.bc.edu/wp-content/uploads/2021/05/IB_21-9.pdf`.
- Munnell and Chen, "Trends in Social Security Claiming," IB 15-8, May 2015: `https://crr.bc.edu/wp-content/uploads/2015/05/IB_15-8.pdf`.
- 2026 OASDI Trustees Report (House Doc 119-163), pp. 120-121 (labor force history) and Table V.C3 (NRA and delayed retirement credits): `https://www.govinfo.gov/content/pkg/CDOC-119hdoc163/pdf/CDOC-119hdoc163.pdf` (77 MB, not kept; excerpts in `raw/trustees/tr2026_excerpts.txt`). The report has no claiming-age distribution.
- CPS ASEC public-use files via the project extract `../cps/data/asec_persons_50plus.parquet` (see `../cps/README.md`).

## Files
- `scripts/fetch_raw.sh` re-downloads the raw sources. `scripts/build_bls.py [--refresh]` writes the LFPR, full/part-time and projections outputs (`--refresh` re-pulls AllData to /tmp). `scripts/build_crr.py` parses the CRR PDFs. `scripts/build_cps_ss.py` tabulates SS receipt from the CPS ASEC extract. Each prints summaries only.
- `output/lfpr_by_age_sex_annual.csv` (long, with source and population), `lfpr_wide_both_sexes.csv`, `lfpr_wide_men.csv`, `lfpr_wide_women.csv`, `lfpr_check_published_vs_computed.csv`.
- `output/ft_pt_older_workers.csv`: part-time share of employed, and full/part-time workers as % of the age group.
- `output/lfpr_bls_projections_2035.csv`.
- `output/crr_average_retirement_age.csv`, `crr_claiming_age_distribution.csv`, `crr_claiming_at_62_cohort.csv`.
- `output/cps_ss_receipt_by_age.csv`.

## Not covered, and why
- SSA claiming tables (Annual Statistical Supplement 6.B5, share claiming at 70) are on ssa.gov, which is blocked; HRS-based retirement-age measures (HRS blocked) and Pew/GAO summaries (blocked) were not used.
- BLS projections to 2033/2034 were superseded: the current BLS table runs to 2035, so it is used instead.
- A CRR-style retirement age from our own data would need monthly CPS basic microdata by single year of age (not downloaded; large).
