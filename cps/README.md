# CPS ASEC retirement income by age, 2010-2026 (direct from Census)

All files come straight from Census (www2.census.gov). Nothing comes from IPUMS. ASEC year t covers income received in year t-1.

## Files
- `scripts/extract.py RAW_DIR` downloads any missing public-use files into RAW_DIR, reads persons aged 50+, harmonizes the variables, and writes `data/asec_persons_50plus.parquet` (1.07M person rows across 20 year/file combinations). Since 2026-10-04 it also keeps the match keys `ph_seq` and `pppos` (all other columns unchanged). The raw downloads total about 2 GB and are kept out of the shared folder.
- `scripts/tabulate.py` produces `output/asec_retirement_income_by_age.csv` in long form: for each year, file and age band it gives n, population, % with any retirement income, % with account withdrawals, % with a DB pension, % with an annuity, % receiving Social Security, withdrawer counts, the median withdrawal among recipients, and total withdrawal dollars (nominal).
- `output/acct_withdrawal_pct_by_age_wide.csv` is the headline table (% of people with retirement-account withdrawals, by age).
- `scripts/se.py RAW_DIR` downloads the replicate-weight files, the pandemic entropy-balanced weights and the alternative-control weights, merges them to the persons, and writes four files:
  - `output/asec_acct_wd_se_by_age.csv`: for every year, file and age band, the % with account withdrawals, its SE and 90% CI, and the withdrawer count and population with their SEs (`*_m` = millions).
  - `output/acct_withdrawal_se_by_age_wide.csv`: SEs (percentage points) laid out like the headline table.
  - `output/asec_acct_wd_changes_se.csv`: year-to-year changes in % and in counts, with SEs and a 90% significance flag.
  - `output/asec_alt_weights_by_age.csv`: the same measures under the pandemic weights (ASEC 2019-2021), the 2020-Census-based weights (ASEC 2020-2021), and the Vintage 2025 reweight of ASEC 2025, each set beside the MARSUPWT value.
- Weight: MARSUPWT. Ages are topcoded at 80 (80-84) and 85 (85+).

## Source files
| ASEC year | File | Processing |
|---|---|---|
| 2010-2013, 2015-2018 | `asecYYYY_pubuse.dat.gz` (fixed width) | legacy |
| 2014 | `asec2014_pubuse_tax_fix_5x8_2017` (5/8 sample, traditional income questions) and `asec2014_pubuse_3x8_rerun_v2` (3/8 sample, redesigned questions). Each file is weighted to the full population. | legacy |
| 2017 | `data-extracts/2017/cps-asec-research-file/pppub17.csv` | updated (same sample as 2017 production) |
| 2018 | `data-extracts/2018/cps-asec-bridge-file/pppub18.csv` | updated (same sample as 2018 production) |
| 2019-2026 | `asecpubYYcsv.zip` | updated |

Fixed-width positions in 2011-2018 are identical in every dictionary: A_AGE 19, A_SEX 24, MARSUPWT 155 (8 digits, 2 implied decimals), SS_YN 423, RET_YN 506, RET_SC1 507, RET_SC2 508, RET_VAL1 509, RET_VAL2 514. The 2010 file has its own layout, taken from `techdocs/cpsmar10.pdf`: age 15, weight 66, RET_YN 366 to RET_VAL2 374.

## Harmonized measures
| Measure | Legacy (2010-2018) | Updated (2017R, 2018B, 2019+) |
|---|---|---|
| `acct_wd`: withdrawals from retirement accounts | RET_SC1 or RET_SC2 = 7 ("regular payments from IRA, Keogh, or 401(k)") | DST_YN = 1 (age 58+) or DST_YN_YNG = 1 (under 58). Covers 401(k), 403(b), Roth and traditional IRA, Keogh, SEP, other |
| `db_pension` | RET_SC 1-5 (company/union, federal, military, state/local, railroad) | PEN_YN = 1 |
| `annuity` | RET_SC = 6 | ANN_YN = 1 |
| `any_ret` | RET_YN = 1 | acct_wd, db_pension or annuity |
| `acct_wd_val` | RET_VAL in the slot coded 7 | DST_VAL1+2 (+_YNG) |

The legacy files store only two source codes per person, so someone with three or more sources can be missing their account withdrawals.

**Validation against Census's own published tables (PINC-09, people 65+):** account-withdrawal recipients come to 3,947k vs Census's 3,945k in ASEC 2016 (legacy) and 7,818k vs 7,814k in ASEC 2021 (updated). DB pension recipients come to 14,580k vs 14,576k in 2021. Annuity counts run about 3% below PINC-09's in both years, because Census's annuity line is broader. `any_ret` is narrower than Census's "Retirement income" total.

## Headline: % of people with retirement-account withdrawals
| ASEC (income yr) | File | 60-64 | 65-69 | 70-74 | 75-79 | 80+ | 65+ |
|---|---|---|---|---|---|---|---|
| 2010 (2009) | prod | 0.4 | 0.8 | 1.0 | 1.0 | 0.5 | 0.8 |
| 2013 (2012) | prod | 0.5 | 1.3 | 1.9 | 2.2 | 1.0 | 1.5 |
| 2014 (2013) | traditional 5/8 | 0.6 | 1.1 | 2.6 | 1.5 | 1.3 | 1.6 |
| 2014 (2013) | redesigned 3/8 | 3.3 | 5.4 | 13.2 | 12.8 | 10.6 | 9.9 |
| 2016 (2015) | prod | 3.7 | 5.4 | 10.8 | 10.8 | 8.1 | 8.3 |
| 2018 (2017) | prod (legacy) | 3.4 | 6.2 | 11.2 | 11.2 | 8.4 | 8.9 |
| 2018 (2017) | bridge (updated) | 5.6 | 10.6 | 19.8 | 19.5 | 15.6 | 15.7 |
| 2019 (2018) | prod | 5.3 | 11.3 | 21.9 | 22.6 | 17.5 | 17.5 |
| 2020 (2019) | prod | 5.7 | 12.0 | 23.1 | 23.4 | 19.7 | 18.8 |
| 2021 (2020) | prod | 5.8 | 10.2 | 16.1 | 17.4 | 14.3 | 14.0 |
| 2022 (2021) | prod | 5.1 | 10.8 | 18.6 | 22.7 | 18.8 | 16.8 |
| 2024 (2023) | prod | 6.0 | 10.0 | 17.2 | 23.3 | 20.1 | 16.7 |
| 2026 (2025) | prod | 6.6 | 11.9 | 17.2 | 25.0 | 20.4 | 17.9 |
The full series, including 55-59 and 60+, is in `output/acct_withdrawal_pct_by_age_wide.csv`.

## Findings
1. **The two breaks are large, and both can be measured within a single year.** The 2014 redesign raises 65+ withdrawal receipt from 1.6% to 9.9% within the same ASEC year (a random split of the sample). The 2019 processing change raises it again, from 8.9% to 15.7%, on the identical 2018 sample (production vs bridge). The 2017 research file shows the same thing (8.6% vs 15.5%). Neither level is comparable across a break, so the consistent series are 2019-2026 (updated processing, extended back to 2017-2018 by the research and bridge files) and, separately, 2015-2018 (legacy processing, redesigned questions). The pre-2014 numbers (around 1%) are known to badly undercount account withdrawals.
2. **The 2020 RMD waiver shows up clearly** (ASEC 2021). At 70-74, receipt falls from 23.1% to 16.1% (SE of the change 0.85, z = −8), and at 65+ from 18.8% to 14.0% (z = −11). With the pandemic EBW weights the drop is 22.3 → 15.8. It then recovers only partly, matching the IRS SOI dip (IRS 70-74 incidence: 86.0 in 2019, 58.8 in 2020).
3. **The RMD-age increases move withdrawals to older ages.** The SECURE Act (age 72, from 2020) and SECURE 2.0 (age 73, from 2023) pushed the first required year back. Since then, 70-74 receipt has stayed near 17-18% (it was 22-23% before 2020), while 75-79 receipt rose from 22.6% to 25.0%.
4. **Recipients 65+ grew from 9.3M to 11.7M (2019 to 2026 ASEC; SE about 0.2M each)**. Part of this is the population-control changes, including +0.33M at the 2025/2026 switch. On Vintage 2025 controls, ASEC 2025 has 11.3M. Nominal withdrawal dollars grew from $151B to $277B. The median among recipients rose from $7,000 to $10,000. These dollar totals are inferred, not checked, to sit well below the IRS 1099-R/1040 totals, as is typical for survey undercounts.
5. **DB pension receipt is slowly declining, and the decline is concentrated in the newest retirees.** Among people 65+ it was 28.4% before the redesign (2014, traditional questions), 25.6% under the redesigned questions, and 24.7% in 2026. At 65-69 it fell from 22.9% (2019) to 18.3% (2026), while 80+ held at about 28%. The 2014 redesign lowered DB receipt by about 3 points. The 2019 processing change barely moved it (25.8% vs 25.2% in 2018). Account withdrawals are the growing source.

## Standard errors
Census publishes a replicate-weight file for every year and file used here: `CPS_ASEC_ASCII_REPWGT_YYYY` in `datasets/YYYY/march/` (2014: `..._2014` for the 5/8 file and `..._2014_3x8_run5` for the 3/8 file), and `cps_asec_ascii_repwgt_2017_111618.dat` and `cps_asec_ascii_repwgt_2018_022619.dat` next to the research and bridge files. None was missing. There are no CSV replicate files, even for the CSV years. Each record holds PWWGT0-PWWGT160 (9 digits with 4 implied decimals; 10 digits in the 2014 3/8 file), then H_SEQ and PPPOS. The files are merged on PH_SEQ and PPPOS. All 1,067,244 persons matched, and PWWGT0 equals MARSUPWT to within 0.005 in every file.

The formula is Census's successive-difference replication: Var = 4/160 × Σ_r (θ_r − θ_0)², with 160 replicates (from Census's "Estimating ASEC Variances with Replicate Weights" usage instructions, 2026 edition, and cpsmar26). θ is the full statistic recomputed with each replicate, and shares are computed as ratios.

**Size.** For the headline % with account withdrawals, in the updated series (2019-2026):
- SE about 0.3 points at 65+
- 0.5-0.65 at 65-69 and 70-74
- 0.7-0.8 at 75-79 and 80+
- 0.3 at 60-64

The legacy-processing years (2015-2018) have SEs of 0.2-0.6, and before 2014 they are under 0.3. The 2014 3/8 redesign file has SEs of 0.4-1.2, about three times the full-sample size. The count of withdrawers 65+ has an SE of 0.16-0.21M (CV about 2%). Population counts by age are controlled, so their SEs are small (0.03-0.2M).

**What is statistically clear** (`asec_acct_wd_changes_se.csv`). Year-to-year SEs treat the two samples as independent. About half of the March sample is shared with the year before, so the correlation is positive and these SEs are conservative.
- The RMD-waiver dip is clear. At 70-74 the share fell 23.1 → 16.1 (−7.0 ± 0.85 SE, z = −8.2). At 65+ it fell 18.8 → 14.0 (z = −10.6). The dip is also significant at 65-69, 75-79 and 80+. The 2021 → 2022 rebound is significant at 70-74 and above.
- The post-2020 shift is clear. At 70-74, every year from 2022 to 2026 sits 4.6-6.0 points below 2020 (z between −5 and −7), and 2026 is 4.6 below 2019 (z = −5.6). At 75-79, 2026 (25.0) is above 2019 (22.6) at z = 2.2. It is not significantly above 2020 (23.3, z = 1.5), and no single-year step after the 2021 → 2022 rebound is significant.
- The 65+ share in 2026 (17.9) is not different from 2019 (17.5). The 2024 → 2025 rise at 65+ (+1.2, z = 2.5, driven by 65-69) is significant, and 2025 → 2026 is flat.
- Within the 2015-2018 legacy series, no year-to-year change in the shares at 65 and over is significant. The only significant change is at 60-64 from 2015 to 2016 (+0.8).

## Pandemic weights
Census's entropy-balanced weights for pandemic nonresponse are in `data-extracts/2020/cpsYYYY_ebw_covidnonresp.csv`, for ASEC 2017-2021 (Rothbaum & Bee). The variables are h_seq, pppos and ebw_pu_person, with the weight given in thousands. They are applied to ASEC 2019, 2020 and 2021 by merging on h_seq/pppos (100% match). Census publishes no replicate weights for them. The SEs in `asec_alt_weights_by_age.csv` scale each MARSUPWT replicate by the person's EBW/MARSUPWT ratio, so they are approximate.

| % with account withdrawals | 65-69 | 70-74 | 75-79 | 80+ | 65+ |
|---|---|---|---|---|---|
| ASEC 2019, MARSUPWT / EBW | 11.3 / 11.0 | 21.9 / 21.5 | 22.6 / 22.0 | 17.5 / 17.1 | 17.5 / 17.1 |
| ASEC 2020, MARSUPWT / EBW | 12.0 / 11.7 | 23.1 / 22.3 | 23.3 / 22.7 | 19.7 / 19.0 | 18.8 / 18.2 |
| ASEC 2021, MARSUPWT / EBW | 10.2 / 10.0 | 16.1 / 15.8 | 17.4 / 17.0 | 14.3 / 13.9 | 14.0 / 13.7 |

The EBW weights lower every share at 65+ by 0.2-0.8 points; 60-64 is essentially unchanged. The cut is largest in ASEC 2020 (−0.6 at 65+, −0.8 at 70-74). This fits Census's finding that pandemic-era respondents were disproportionately higher-income. With EBW, the 2020 RMD-waiver dip at 70-74 is 22.3 → 15.8 (−6.5, vs −7.0 with MARSUPWT), and at 65+ it is 18.2 → 13.7 (−4.5 vs −4.8). The dip is essentially unchanged and still highly significant. With EBW, the ASEC 2019 → 2020 rise at 65+ (+1.1) is about the same size as under MARSUPWT (+1.2). The population counts are unchanged, because EBW preserves the totals by age.

Census also publishes **2020-Census-based** replicate weights for ASEC 2020 and 2021 (`CPS_ASEC_ASCII_REPWGT_202x_2020BASE`; PWWGT0 is the alternative full weight), for comparing those years with ASEC 2022+. These leave the shares within 0.1 point of the published ones. They lower the 65+ population (2021: 55.8M → 54.3M) and the 65+ withdrawer count (7.81M → 7.58M). Use them, not MARSUPWT, for 2020/2021 counts set beside 2022+.

## 2026 population controls (the 65+ jump)
The 61.5M (ASEC 2025) → 65.2M (ASEC 2026) jump in the 65+ population is mostly real aging plus a change of population controls. It is not a sampling or processing artifact.
- ASEC 2026 is weighted to Census's **Vintage 2025** population estimates (for March 1, 2026). ASEC 2025 used Vintage 2024. Vintage 2025 is the first vintage built directly on the 2020 Census, through the Modified Age and Race Census (MARC) file. It replaces the "blended base" used in Vintages 2021-2024, which mixed the 2020 Census, the 2020 Demographic Analysis and the Vintage 2020 estimates (cpsmar26, footnote 18; Census working paper SEHSD-WP2026-16, Fox and Jensen, August 2026). The total population barely changes, but the age, sex and race mix does.
- Census re-weighted ASEC 2025 to Vintage 2025. The replicate file in `datasets/2025/march/vintage/` (posted 2026-09-18; its PWWGT0 is the Vintage 2025 weight) gives **63.14M people 65+ vs 61.49M** under the original weights. This matches WP2026-16 Table 3 exactly (61,490k → 63,140k). It also gives 50-64 at 60.1M vs 60.9M. So about 1.65M of the 3.7M jump is the control change. The other 2.1M is one year of growth on consistent controls (63.1 → 65.2), in line with the Vintage 2025 national estimates (65+ resident population +1.8M from July 2024 to July 2025).
- The Census national estimates (`nc-est2024-agesex-res` vs `nc-est2025-agesex-res`) show the same revision. For July 2024, the 65+ population is 61.18M in Vintage 2024 vs 62.81M in Vintage 2025 (+1.63M, +2.7%), and ages 50-64 are 62.15M vs 61.67M (−0.48M). Vintage 2025 already has more people 65+ in 2020 (55.95M vs 54.46M), so the revision comes from the base, not from migration.
- **Shares are unaffected.** Under the Vintage 2025 reweight, the ASEC 2025 shares move by at most 0.05 points (65+: 17.84 → 17.89; 70-74: 17.54 → 17.51).
- **Read counts on consistent controls.** On Vintage 2025 controls, ASEC 2025 has 11.30M withdrawers 65+ (vs 10.97M published). The 2025 → 2026 growth is therefore +0.39M (11.30 → 11.69M), not +0.73M. Counts from ASEC 2026 are not comparable with earlier years without a similar re-base, and Census has published a re-base only for ASEC 2025 (and the 2020-based weights for 2020-2021). Count series that cross 2021/2022 (blended base introduced) or 2025/2026 (Vintage 2025) include control shifts. Shares do not.

## Caveats and open flags
- These are shares of **all people** in each age band. The IRS SOI incidence uses **IRA holders** as the denominator, so the levels are not comparable. Use trends and breaks for the cross-check.
- The CPS question asks about income received. Rollovers and conversions are presumably excluded, but the questionnaire wording should be checked before any comparison of dollars.
- Under-58 distributions (DST_*_YNG) are included in `acct_wd` but are not counted as income by Census. This affects the 50-54 and 55-57 ages only.
- ASEC 2020-2021 had pandemic nonresponse. Applying Census's entropy-balanced weights lowers the 65+ shares by 0.2-0.8 points and leaves the 2020 RMD dip intact (see Pandemic weights). The headline table still uses MARSUPWT.
- RESOLVED (2026-10-04): the 65+ population jump 61.5M → 65.2M (ASEC 2025 → 2026) comes from Vintage 2025 population controls (about +1.65M) plus normal aging (about +2.1M). Shares are unaffected. Compare counts only on consistent controls (see 2026 population controls).
- DONE (2026-10-04): standard errors from Census replicate weights are available for all 20 year/file combinations. The SEs for year-to-year changes ignore sample overlap and are conservative. The 2014 3/8 file is small (n = 7.7k aged 65+; SEs about 3× larger).
- Open: no replicate weights exist for the pandemic EBW weights (the EBW SEs are approximate). Count series also include control shifts at 2021/2022 (blended base) and 2025/2026 (Vintage 2025).
