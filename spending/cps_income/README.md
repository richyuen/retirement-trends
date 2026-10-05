# Income sources of Americans 65+, CPS ASEC 1998-2026 (direct from Census)

All microdata come straight from Census (www2.census.gov). Nothing comes from IPUMS. ASEC year t covers income received in year t-1 (income year), so ASEC 2026 = income in 2025. Shares are nominal-dollar ratios within a year, so inflation does not matter for them.

## Files
- `scripts/extract.py RAW_DIR` downloads the public-use files (any that are missing) into RAW_DIR (we used `/tmp/cps_raw/dl`, about 2.4 GB). It writes `data/asec_aged_income_persons.parquet` (16 MB, 766k rows): every person aged 65+ and every spouse of a person aged 65+, for 32 year/file combinations, with harmonized income components.
  - Fixed-width positions come from Census's own dictionaries (`techdocs/cpsmar98.pdf` … `cpsmar18.pdf`, the "D NAME width position" lines, and `asec2014R_pubuse.dd.txt`).
  - There are only two layouts: ASEC 1998-2010 and ASEC 2011-2018. Every variable used here is identical within each span.
  - URLs and file choices extend `../../cps/scripts/extract.py`.
- `scripts/tabulate.py` produces the point estimates (MARSUPWT):
  - `output/income_sources_long.csv` holds everything: each year × file × unit × age band × measure.
  - `output/income_share_65plus_wide.csv` and `output/income_recipiency_65plus_wide.csv` are the headline tables for persons 65+: the share of aggregate income and the % receiving each source.
  - `output/income_share_exclRINT_65plus_wide.csv` gives the same shares with interest credited inside retirement accounts removed (see caveat 2).
  - `output/aged_unit_share_wide.csv`, `aged_unit_recipiency_wide.csv` and `aged_unit_share_exclRINT_wide.csv` are the same tables for SSA-style aged units.
  - `output/income_by_age_band_persons.csv` breaks the person tables down by age band: 65-69, 70-74, 75-79 and 80+.
  - `output/ss_reliance_wide.csv` gives the % of Social Security beneficiaries with SS ≥ 50%, ≥ 90% and = 100% of income. It covers persons, all aged units, married couples and nonmarried units, plus an "exclRINT" variant.
- `scripts/se.py REP_DIR` (`/tmp/cps_raw/rep`, about 1.8 GB) uses Census replicate weights for ASEC 2005, 2010, 2013, both 2014 files, 2015, 2017 (production and research), 2018 (production and bridge) and 2019-2026. It writes two files:
  - `output/se_income_sources.csv`: the estimate, SE and 90% CI for every measure, unit and age band.
  - `output/se_changes.csv`: breaks and changes, each with its SE, z and a 90% significance flag.
  - The formula is Census SDR, Var = 4/160 Σ(θ_r − θ_0)², the same as `../../cps/scripts/se.py`.
  - All persons matched the replicate files, and PWWGT0 equals MARSUPWT.

## Units
- **Aged unit (main unit for the SS-reliance statistic and the SSA comparison).** This is SSA's *Income of the Aged* unit: a married couple living together with at least one spouse aged 65+ (both spouses' incomes pooled), or a nonmarried person aged 65+. Spouses are linked through A_SPOUSE → A_LINENO. ASEC gives both spouses the same weight (checked on all 385k pairs).
  - Why this is the main unit: couples share income, so the SSA ≥50%/≥90% statistic is defined on it. It also lets us validate against SSA's published numbers (below).
  - Difference from SSA: SSA classifies a couple by the husband's age, except when he is under 55 and the wife is 55 or older. We use "either spouse 65+", so our 2015 aged-unit count is 35.5M vs SSA's 34.6M.
- **Persons 65+ (own income).** This unit is used for the % receiving each source and for the age bands, because a person's age and receipt are unambiguous. It is also the unit of Census's PINC tables.

## Harmonized sources (see `extract.py` docstring for codes)
| Source | Legacy files (1998-2018) | Updated files (2017R, 2018B, 2019-2026) |
|---|---|---|
| Earnings | PEARNVAL (wages + nonfarm + farm self-employment) | same |
| Social Security | SS_VAL | same |
| DB pensions | RET_SC 1-5 + 8 (company/union, federal, military, state/local, railroad, other), survivor pensions SUR_SC 1-5, employer/government disability pensions DIS_SC 2-6 | PEN_VAL1+2 + the same SUR/DIS codes |
| Annuities | RET_SC 6 + SUR_SC 9 | ANN_VAL + SUR_SC 9 |
| Retirement-account withdrawals | RET_SC 7 ("regular payments from IRA, Keogh, 401(k)") | DST_VAL1+2 (all account types, age 58+) |
| Asset income | INT + DIV + RNT | same, but INT = TRDINT (non-retirement) + RINT (interest/dividends credited inside retirement accounts) |
| SSI / public assistance | SSI_VAL + PAW_VAL | same |
| Other | veterans' benefits + PTOTVAL minus all of the above (UC, workers' comp, child support, alimony, educational and financial assistance, estates and trusts, other) | same |

The components add up to PTOTVAL (Census total money income) exactly in every file. "Other" is never negative for anyone aged 65+, apart from one 2001 record.

## Validation against SSA's published (CPS-based) numbers
| Statistic | SSA published | This extract |
|---|---|---|
| Shares of aggregate income, aged units 65+, 2014 (ASEC 2015) | earnings 32.2, SS 33.2 (+RR 0.2), govt pensions 7.9 + private pensions/annuities 12.8, assets 9.7, public assistance 0.6, other 3.4 (SSA, *Income of the Population 55 or Older, 2014*, Table 10.1) | earnings 33.5, SS 32.4, DB + annuity + account withdrawals 21.3, assets 9.3, SSI/PA 0.6, other 2.8 |
| SS ≥ 50% / ≥ 90% of income, aged beneficiary units, 2012 (ASEC 2013) | 65 / 36 (SSA *Income of the Aged Chartbook 2012*, as quoted by Bee & Mitchell 2017, p.22) | 64.1 / 35.7 |
| Same, couples / nonmarried, 2012 | ≥50%: 52 / 74; ≥90%: 22 / 47 (SSA *Fast Facts & Figures*, data year 2012) | 51.6 / 73.8; 21.4 / 46.9 |
| Same, 2009 (ASEC 2010) | ≥50%: 54 / 73; ≥90%: 22 / 43 (SSA *Fast Facts & Figures*, data year 2009) | 53.8 / 73.5; 22.2 / 43.2 |
| Same, 2013 (ASEC 2014, traditional 5/8 file) | ≥50%: 51 / 74; ≥90%: 21 / 46 (SSA *Fast Facts & Figures 2015*) | 49.9 / 74.0; 20.5 / 46.2 |
| Same, 2014 (ASEC 2015) | ≥50%: 48 / 71; ≥90%: 21 / 43 (SSA *Fast Facts & Figures 2016*) | 46.8 / 70.7; 20.4 / 42.7 |

ssa.gov is blocked from this environment, so the SSA values were taken from:
- search-engine extracts of the Fast Facts pages (the edition years for the 2009 and 2012 data are not confirmed);
- a senate.gov mirror of SSA's *Income of the Population 55 or Older, 2014*, Section 10 PDF (sanders.senate.gov/wp-content/uploads/sect10.pdf);
- Bee & Mitchell (2017).

They should be re-checked on ssa.gov before publication.

## Headline results, persons 65+: share of aggregate income (%)
Series: **A** = legacy processing, traditional questions; **B** = legacy processing, redesigned questions (2014 3/8 sample, 2015-2018); **C** = updated processing (2017 research file, 2018 bridge file, 2019+). SE ≈ 0.4-0.6 for the SS and earnings shares in a single year (`se_income_sources.csv`).

| ASEC (income yr) | Series | Earnings | Social Security | DB pension | Annuity | Acct withdrawals | Asset income | SSI/PA | Other |
|---|---|---|---|---|---|---|---|---|---|
| 1998 (1997) | A | 16.8 | 40.5 | 19.2 | 0.3 | 0.2 | 19.9 | 0.8 | 2.2 |
| 2000 (1999) | A | 18.7 | 39.2 | 19.0 | 0.3 | 0.5 | 19.3 | 0.7 | 2.3 |
| 2005 (2004) | A | 23.1 | 40.8 | 20.1 | 0.3 | 0.6 | 12.3 | 0.6 | 2.2 |
| 2010 (2009) | A | 25.9 | 40.7 | 18.7 | 0.4 | 0.4 | 11.0 | 0.6 | 2.4 |
| 2013 (2012) | A | 30.2 | 37.6 | 17.5 | 0.3 | 0.8 | 10.5 | 0.5 | 2.5 |
| 2014 (2013) | A (5/8) | 29.6 | 36.6 | 17.8 | 0.3 | 1.0 | 11.4 | 0.6 | 2.7 |
| 2014 (2013) | B (3/8) | 29.4 | 35.0 | 17.3 | 1.3 | 3.1 | 10.8 | 0.6 | 2.5 |
| 2018 (2017) | B | 30.7 | 33.4 | 17.7 | 1.7 | 3.0 | 10.1 | 0.5 | 2.9 |
| 2018 (2017) | C (bridge) | 29.9 | 31.6 | 16.6 | 1.6 | 5.6 | 11.8 | 0.5 | 2.5 |
| 2019 (2018) | C | 29.0 | 32.0 | 15.9 | 2.0 | 7.0 | 11.2 | 0.5 | 2.3 |
| 2020 (2019) | C | 28.9 | 31.2 | 15.7 | 2.0 | 6.6 | 12.5 | 0.4 | 2.6 |
| 2021 (2020) | C | 29.3 | 32.3 | 15.1 | 2.0 | 5.3 | 12.7 | 0.4 | 2.8 |
| 2022 (2021) | C | 28.6 | 31.3 | 13.9 | 1.7 | 7.4 | 14.0 | 0.5 | 2.6 |
| 2024 (2023) | C | 28.5 | 32.6 | 13.8 | 1.6 | 6.4 | 14.3 | 0.4 | 2.5 |
| 2026 (2025) | C | 27.2 | 32.3 | 12.7 | 2.0 | 7.6 | 15.1 | 0.5 | 2.5 |

Without the interest credited inside retirement accounts (series C only; `income_share_exclRINT_65plus_wide.csv`):

| | Earnings | SS | DB | Annuity | Acct withdrawals | Asset income |
|---|---|---|---|---|---|---|
| 2019 | 30.2 | 33.4 | 16.6 | 2.0 | 7.3 | 7.5 |
| 2026 | 29.2 | 34.7 | 13.7 | 2.2 | 8.1 | 9.0 |

## % of persons 65+ receiving each source
| ASEC | Series | Earnings | SS | DB pension | Annuity | Acct withdrawals | Asset income | SSI/PA |
|---|---|---|---|---|---|---|---|---|
| 1998 | A | 15.3 | 89.9 | 34.8 | 0.7 | 0.5 | 62.9 | 4.4 |
| 2005 | A | 18.1 | 88.1 | 33.8 | 1.0 | 1.0 | 55.5 | 3.5 |
| 2013 | A | 21.8 | 84.0 | 31.6 | 0.8 | 1.5 | 50.0 | 2.8 |
| 2014 | A / B | 22.1 / 21.8 | 82.3 / 83.5 | 31.8 / 29.4 | 1.0 / 5.2 | 1.6 / 9.9 | 50.0 / 64.0 | 2.9 / 3.3 |
| 2018 | B / C | 23.0 / 23.0 | 81.1 / 81.2 | 28.5 / 27.8 | 5.9 / 6.1 | 8.9 / 15.7 | 63.3 / 63.3 | 3.0 / 3.0 |
| 2019 | C | 23.5 | 80.8 | 29.4 | 6.8 | 17.5 | 62.6 | 2.9 |
| 2026 | C | 22.3 (SE 0.3) | 81.2 (0.3) | 26.9 (0.35) | 6.4 (0.2) | 17.9 (0.3) | 67.4 (0.4) | 3.0 (0.1) |

"Asset income" in series C includes the 34.8% (2026) who report interest inside retirement accounts. Excluding that, the 2026 figure is 63.1%. The account-withdrawal figures match `../../cps/` exactly. The SS receipt decline is concentrated at 65-69: 83.8% in 1998 and 64.4% in 2026, consistent with later claiming and the rise of the full retirement age to 66-67. At 80+ it is about 91-93% throughout.

## Social Security reliance (% of SS-beneficiary units with SS ≥ 50% / ≥ 90% of their income)
| ASEC (income yr) | All aged units | Couples | Nonmarried | Persons 65+ (own income) |
|---|---|---|---|---|
| 1998 (1997) | 64.2 / 30.0 | 52.6 / 19.5 | 72.5 / 37.4 | 68.0 / 35.0 |
| 2005 (2004) | 65.2 / 33.9 | 53.0 / 21.3 | 74.0 / 43.0 | 69.4 / 40.1 |
| 2013 (2012) | 64.1 / 35.7 | 51.6 / 21.4 | 73.8 / 46.9 | 69.6 / 43.4 |
| 2014 A / B | 63.2 / 34.8 vs 60.5 / 34.5 | 49.9 / 20.5 vs 46.8 / 21.2 | 74.0 / 46.2 vs 71.6 / 45.2 | |
| 2018 B / C | 59.2 / 34.4 vs 58.2 / 33.0 | | | |
| 2019 (2018) | 58.0 / 31.6 | 45.0 / 18.4 | 68.2 / 41.9 | 63.9 / 39.2 |
| 2021 (2020) | 59.0 / 33.5 | 45.1 / 19.5 | 69.9 / 44.5 | 65.0 / 40.6 |
| 2026 (2025) | 58.3 / 31.9 (SE 0.4 / 0.4) | 45.2 / 18.5 | 68.3 / 42.2 | 64.1 / 38.6 |

Excluding interest credited inside retirement accounts, the 2026 aged-unit figures are 60.6 / 33.2. Within series C the statistic is flat: 2019 → 2026 is +0.3 (SE 0.6) at ≥50% and +0.4 (SE 0.6) at ≥90%. The visible fall from about 64-65% (1998-2013) to about 58% comes mostly at the two breaks: −2.8 points at the 2014 redesign (SE 1.1) and −1.0 at the 2019 processing change (SE 0.6, conservative), plus a −1.2 drift within 2015-2018.

**Survey vs administrative data:**
- Bee & Mitchell (2017, Table 10) linked ASEC 2013 to SSA and IRS records. For aged-unit beneficiaries, SS ≥ 50% of income falls from 64.4% (survey) to 50.4% (admin), and ≥ 90% falls from 35.5% to 18.1%. For persons in families, the figures are 55.5 → 42.2 and 26.2 → 12.2.
- The SSA *Basic Facts* fact sheet figures (admin-linked, 2015) were dropped on 2026-10-04: the sheet is only on ssa.gov, which blocks this environment. Verified admin-linked equivalents: Bee & Mitchell (2017) Table 10 (above) and Dushi, Trenkamp, Bee & Mitchell (J. Pension Econ. & Finance 2025, abstract): majority-of-income reliance 53% CPS / 49% HRS vs 42% admin (2015 income).
- The often-quoted CPS-based figures therefore overstate reliance by roughly 14 points at ≥ 50% and roughly halve at ≥ 90%.

## Breaks (measured within one ASEC year)
**2014 income-question redesign** (random 5/8 vs 3/8 split, independent SEs):
- Account-withdrawal receipt goes from 1.6% to 9.9% (+8.3, SE 0.5), and its share of income from 1.0 to 3.1 (+2.2, SE 0.3).
- Annuity share goes from 0.3 to 1.3 (+1.1, SE 0.2).
- DB receipt goes from 31.8 to 29.4 (−2.4, SE 0.8).
- The SS share goes from 36.6 to 35.0 (−1.7, SE 0.9). The earnings share is unchanged (29.7 → 29.4).

**2019 processing system** (the same 2018 sample, production vs bridge file). The SEs treat the two files as independent, which is conservative: the bridge file uses different household sequence numbers, so the replicates cannot be paired.
- Account withdrawals: receipt goes from 8.9% to 15.7%, and the share from 3.0 to 5.6 (+2.6, SE 0.3).
- Interest credited inside retirement accounts newly enters income: 4.2% of aggregate income in the 2018 bridge file, 6.8% by 2026.
- As a result, the SS share falls 33.4 → 31.6 (−1.9, SE 0.6) while earnings and DB barely move. Excluding that interest, the SS share changes by only −0.5 (SE 0.6).
- The 2017 research file gives the same picture.

## Trends
**1. Earnings rose, then plateaued, tracking 65+ labor-force participation.**
- Earnings' share of aggregate income for persons 65+ rose from 16.8% (1997 income) to 30.2% (2012), within series A (2005 → 2013: +7.1, SE 1.1).
- It was about 29-31% in 2014-2018. In series C it slips from 29.0% to 27.2% (2018-2025 income), or 30.2 → 29.2 excluding retirement-account interest (−1.0, SE 0.8, not significant).
- Earnings receipt rose from 15.3% to 23.5% and then flattened, and "worked last year" (WKSWORK > 0) follows the same path.
- This matches BLS's 65+ labor-force participation rate: 11.9% in 1998, 12.9% in 2000, 17.4% in 2010, 18.7% in 2013, a peak of 20.2% in 2019, 18.9% in 2021 and 19.1% in 2025. Sources: BLS *Monthly Labor Review* 2022, Colato, Dubina, Kim and Rieley, Chart 4 data for 1991-2021; BLS *TED*, "Nearly one in five older Americans in the labor force in 2025" (2026), for 2000, 2019 and 2025.
- For aged units the earnings share is higher (33-35% in 2013-2020; 33.1% excluding retirement-account interest in 2026), because it includes the earnings of under-65 spouses.

**2. Social Security share.** Within series A it fell from about 38-42% (1998-2010) to 36.6% (2013). Since 2019 it has been flat to slightly up: excluding retirement-account interest, 33.4 → 34.7 (+1.3, SE 0.5). Published levels depend heavily on the processing era (caveat 2).

**3. DB pensions are declining; account withdrawals are rising.**
- The DB share fell from about 19-20% (1998-2005) to 17.5% (2013).
- Within series C it fell from 16.6% to 13.7% excluding retirement-account interest (2019 → 2026, −2.9, SE 0.4). DB receipt fell 29.4 → 26.9 (−2.5, SE 0.5), concentrated at 65-69 (24.6 → 20.0).
- Account withdrawals rose from 7.3% to 8.1% of income (+0.8, SE 0.4, borderline significant) and are now about 60% of DB's size. Annuities stay at about 2%.
- Retirement income other than SS (DB + annuities + withdrawals) is about 22-25% of income in series C. In series A it was about 19-21%, but that series misses most withdrawals.

**4. Asset income** fell from about 20% (1997-99 income) to about 10-11% (2009-2013), as interest rates fell. In series C, excluding retirement-account interest, it rose from 7.5% to 9.0% (2019 → 2026, +1.5, SE 0.4) as rates rose.

**5. COVID / RMD waiver (2020 income, ASEC 2021).** Account withdrawals' share fell 6.6 → 5.3 and receipt 18.8 → 14.0 (−4.8, SE 0.5), recovering in 2021 income. That year SS reliance rose (aged units ≥50%: 56.7 → 59.0, +2.4, SE 0.7) and then fell back. ASEC 2020-2021 also have pandemic nonresponse; see `../../cps/README.md`, "Pandemic weights".

**6. By age (2025 income, persons).** SS is 21.8% of income at 65-69 and 42.0% at 80+; earnings are 44.8% at 65-69 and 9.4% at 80+. Account withdrawals peak at 75-79 and 80+, at 9.2-9.6% of income and 20-25% receiving.

## Caveats
1. **CPS underreports retirement income heavily.** Bee & Mitchell (2017, Census SEHSD WP 2017-39) linked ASEC 2013 to IRS and SSA records:
   - Median household income of householders 65+ in 2012 was $44,400, not the survey's $33,800 (+30%), and the 65+ poverty rate was 6.9%, not 9.1% (the abstract's figure; the text says 9.0%).
   - Retirement income receipt was 37% in the survey vs 61% in the records, with a 46% false-negative rate. "Distributions from IRAs are rarely reported", and DB income is also underreported. Survey receipt was flat (40% in 1990, 36% in 2012) while the admin records rose from 45% to 61%.
   - SS amounts and earnings match the records well.
   - These figures predate the 2014/2019 redesigns, which recovered part of the gap, mainly account withdrawals.
   - The source shares here therefore **overstate SS and earnings and understate pensions and withdrawals**. Read trends within a series, not levels.
2. **Interest credited inside retirement accounts (RINT) counts as income in updated processing.**
   - From the 2017 research file onward, INT_VAL = TRDINT_VAL + RINT_VAL1+2. RINT answers "how much did you earn in interest or dividends" within each 401(k)/IRA account, "include small amounts reinvested or credited" (cpsmar26, questionnaire section 5.15).
   - It is in PTOTVAL; we checked that the identity holds exactly. Yet it is generally not withdrawn, and when it is withdrawn it reappears as a distribution.
   - It is 6.8% of 65+ aggregate income in 2026, and 34.8% of people 65+ report some. The `exclRINT` files remove it.
   - It is low in ASEC 2023 (2.9% vs 5.3% in 2022 and 5.0% in 2024). The share of people 65+ reporting any RINT is unchanged (34.0% -> 34.1% -> 34.7%), but the mean among reporters halves ($7,094 -> $3,854 -> $7,315). Income year 2022 was a bad market year (S&P 500 year-end level -19.4%, FRED SP500: 4,766 -> 3,840), and income year 2018 (-6.2%) is also low (4.0% vs 5.5% the next year). Inferred, not confirmed by Census: respondents report account returns, which were near zero or negative in 2022, and negative values are not recorded (no negative RINT in any file). Use the exclRINT tables for trends.
   - SSA's definition of asset income also counts interest "credited to … IRAs", so this is not an error, but it is a series break.
3. **Series breaks.** There are three series: A for ASEC 1998-2014 (traditional questions), B for 2014 (3/8) through 2018, and C for 2017R/2018B and 2019-2026. Compare levels only within a series. The bridge points (2014 split, 2017 research file, 2018 bridge file) measure the jumps; see Breaks above.
4. **Legacy files keep two retirement source codes per person.** People with three or more sources can lose a component, which most likely understates account withdrawals and annuities in series A and B. Survivor and disability pensions also keep two sources each.
5. **Topcoding and swapping.** Before ASEC 2011, amounts above the topcodes were replaced by cell means. From ASEC 2011, Census uses rank-proximity swapping, and the topcodes vary by source and year. Aggregate shares of earnings and asset income are the measures most exposed. We used the public values as published, with no adjustment.
6. **Income year vs survey year.** ASEC year t = income in t−1, and age is measured in March of year t. The 65+ population and the aged-unit population depend on population controls. The 2025 → 2026 jump is mostly Vintage 2025 controls (`../../cps/README.md`); shares are unaffected.
7. **Other.** "Other" includes veterans' benefits, which are about 1.6% of income in 2026 and are reported separately as `memo_veterans`. Railroad Retirement is in DB pensions here, while SSA reports it beside Social Security (0.2% in 2014). The aged-unit definition differs slightly from SSA's (see Units). The 1998-2001 files predate the SCHIP sample expansion; the samples are smaller but the weights are consistent.
8. **SEs.** Changes over time treat years as independent. That is conservative, because about half of each March sample carries over from the previous year. Same-sample break SEs (2017/2018) are also treated as independent, so they are overstated. EBW pandemic weights are not applied here.

## Reproduce
```
python3 scripts/extract.py /tmp/cps_raw/dl     # about 2 min after the downloads
python3 scripts/tabulate.py
python3 scripts/se.py /tmp/cps_raw/rep         # about 1 min after the downloads
```
Raw files are not kept in the shared folder. The scripts download them again when needed.
