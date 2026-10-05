# Employer retirement-plan offer and participation, CPS ASEC 2001-2026 (direct from Census)

All microdata come from www2.census.gov public-use ASEC files. None come from IPUMS. Script: `dc_policy/scripts/cps_participation.py` (`extract`, then `tabulate`). Outputs: `dc_policy/output/cps_plan_participation_by_year.csv` (long format), `cps_participation_breaks_ppa.csv` (the break and PPA-window tests) and `cps_state_autoira_check.csv`. ASEC year t asks about the longest job in income year t−1. Every number below marked "Computed" comes from these files.

## 1. Bottom line

### Takeaway
- **PPA 2006:** the CPS shows no rise in participation after the Pension Protection Act of 2006. Among private wage-and-salary workers aged 21-64, the share offered a plan fell steadily from 2000 through 2012. The share participating fell with it (46.9% in income year 2000 to 40.0% in 2012).
- The only PPA-consistent signal is small. Take-up among workers whose employer had a plan rose about 1.4 points, from 78.7% (income years 2002-06) to 80.1% (2009-12). That rise is significant and appears in every subgroup.
- **Measurement breaks:** after 2013 the CPS series is dominated by them. The 2014 questionnaire redesign alone cuts measured participation by 4.5 points within the same year. Then the CPS keeps drifting down, to 28.4% in income year 2025. Other sources contradict that drift (NCS, W-2, EBRI).
- **State auto-IRAs:** small-employer workers in Oregon, Illinois and California show no detectable rise in reported offer or participation relative to other states. This is suggestive only.

### Evidence verdict
- **Auto-enrollment (PPA):** weak positive evidence. Take-up among the offered rose about 1-2 points (statistically clear), but participation fell overall because offer rates fell.
- **State auto-IRAs:** the CPS gives no evidence of an effect. This is a weak null, not evidence against an effect: the CPS question likely misses auto-IRAs, and the samples are small.

## 2. Data, universe and variables

### Takeaway
- **Universe:** private wage-and-salary workers aged 21-64 who worked last year. That means A_AGE 21-64, WKSWORK>0 and LJCW=1 (longest job "Private"). LJCW=1 excludes the incorporated self-employed (code 5).
- **Measures:** the share offered (PENPLAN=1), the share participating (PENINCL=1) and take-up (PENINCL=1 among PENPLAN=1). All are weighted by MARSUPWT.
- **Sample:** n is about 75k persons per year in 2001, 66k in 2013 and 44-48k in 2024-2026. The 2014 redesign subsample has about 20k.

### Cited findings
- **Variable name correction.** The brief named PENATVTY. In the ASEC, PENATVTY is the person's country of birth (3 digits, range 057:555), not pensions. The pension items are PENPLAN and PENINCL — [Census, CPS ASEC technical documentation cpsmar01-cpsmar26](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar26.pdf).
- **PENPLAN wording:** "Other than social security did the employer or union that ... worked for in 20.. have a pension or other type of retirement plan for any of the employees?" Its universe is WRK_CK=1. **PENINCL wording:** "Was ... included in that plan?", with universe PENPLAN=1 — [cpsmar01, p. 8-48](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar01.pdf); the wording is identical in [cpsmar15](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar15.pdf). No PENPLAN or PENINCL value was "not in universe" for anyone in the analysis universe in any year (Computed).
- **NOEMP (employer size, counting all locations).** Codes 1, 4, 5 and 6 (<10, 100-499, 500-999, 1000+) are stable. Codes 2 and 3 were 10-24 and 25-99 through ASEC 2010. They became 10-49 and 50-99 from ASEC 2011. cpsmar11 says: "Item NOEMP ... has a revised description for the values of 2 and 3. Value 2 is now described as 10-49" ([cpsmar11](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar11.pdf)).
  - The 2019-2026 dictionaries still print "10 - 24 / 25 - 99". But the 2019 questionnaire (Q4788) lists "10-49 / 50-99" ([cpsmar19](https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar19.pdf)).
  - The weighted shares confirm it (Computed). Code 2 holds 11.8% of the universe in ASEC 2010, 18.0% in 2013 and 17.0% in 2019. Code 3 holds 14.9%, 8.7% and 8.3%.
  - So the 2019+ labels in the dictionary are a documentation error. The under-100 vs 100+ split, and <10, are consistent across all years.
- **Full-time vs part-time:** based on HRSWK ("In the weeks that ... worked how many hours did ... usually work per week?"), with full-time at 35+ hours and part-time at 1-34. Full-year full-time adds WKSWORK≥50.
- **State:** GESTFIPS from the household record, merged on PH_SEQ = H_SEQ. Every person matched.

**Fixed-width positions (start/width, 1-based), from each year's dictionary:**

| Variable | ASEC 2001-2010 (cpsmar01-10) | ASEC 2011-2018 incl. both 2014 files (cpsmar11-18, asec2014R/early dd) | 2017 research, 2018 bridge, 2019-2026 |
|---|---|---|---|
| PH_SEQ / PPPOS | 2/5, 7/2 | 2/5, 7/2 | CSV pppubYY |
| A_AGE | 15/2 | 19/2 | CSV |
| MARSUPWT (2 implied dec.) | 66/8 | 155/8 | CSV |
| WKSWORK | 171/2 | 258/2 | CSV |
| HRSWK | 181/2 | 268/2 | CSV |
| LJCW | 189/1 | 291/1 | CSV |
| NOEMP | 226/1 | 300/1 | CSV |
| WSAL_VAL (kept, not tabulated) | 243/6 | 364/7 | CSV |
| PENPLAN / PENINCL | 482/1, 483/1 | 731/1, 732/1 | CSV |
| Household H_SEQ / GESTFIPS | 2/5, 42/2 | 2/5, 42/2 | CSV hhpubYY |

**Source files:**
- ASEC 2001: `chip2001pub.cps.gz`, the SCHIP-expanded sample (218k persons), used for consistency with 2002+. The smaller `mar01supp` was not used.
- ASEC 2002: `mar02supp.dat.gz`.
- ASEC 2003-2004: `asec200X.pub.gz`.
- ASEC 2005-2006: `asec200X_pubuse.pub.gz`.
- ASEC 2007: `asec2007_pubuse_tax2.dat.gz`.
- ASEC 2008-2018, the 2014 3/8 and 5/8 files, the 2017 research file, the 2018 bridge file and the 2019-2026 CSV zips: the same URLs as `cps/scripts/extract.py`.

## 3. Standard errors

### Takeaway
- **ASEC 2005-2026: replicate weights.** SEs use Census replicate weights (160 replicates; Var = 4/160·Σ(θr−θ0)²). The files are the same `CPS_ASEC_ASCII_REPWGT_YYYY` files as `cps/scripts/se.py`; the 2005-2009 files have the same 1456-byte layout. Every person matched, and PWWGT0 equals MARSUPWT to within 0.011.
- **ASEC 2001-2004: no public replicate file.** These SEs use a generalized design-effect approach: the binomial SRS SE × √deff. Here deff is the median ratio of replicate to SRS variance for the same group and measure across ASEC 2005-2010, typically 1.4-2.2. These rows are flagged `se_method=gvf_deff_2005_2010`.
- **Size:** the headline SEs are 0.22-0.34 pp for offer and participation and 0.25-0.41 for take-up. The 2014 3/8 file has SEs of about 0.4-0.5.
- **Pooled state comparisons:** SEs use the same replicate index across years. For differences and DiD across periods this treats the years as independent.

## 4. Headline series (Computed)

### Takeaway
- **2000-2012 (traditional questionnaire):** offer fell from 59.6% to 49.7% and participation from 46.9% to 40.0%. Take-up rose from 78.7% to 80.4%.
- **Employer size:** at employers under 100, participation fell from 28.7% to 23.0%; at 100+, from 59.2% to 51.9%.
- **2014 onward:** the series sits at a lower level and drifts down, to 28.4% participation and 35.9% offer in income year 2025.
- **Part-time and young workers:** part-time workers participate at about a third of the full-time rate (10.9% vs 31.3% in 2025). Ages 21-34 have lower take-up (67-71%) than ages 35-64 (83-85%).
- Group codes: emp_lt100 = NOEMP 1-3; emp_100plus = 4-6; fulltime_35h = HRSWK≥35; parttime_lt35h = HRSWK 1-34. Further groups in the CSV: emp_lt10, the detailed sizes, emp_100_499, emp_500_999, emp_1000plus, fullyear_fulltime, and young workers at small and large employers.

**Offer: employer/union had a plan (PENPLAN=1)** — % (SE)

| ASEC | Income yr | File | all_21_64 | emp_lt100 | emp_100plus | fulltime_35h | parttime_lt35h | age_21_34 | age_35_64 |
|---|---|---|---|---|---|---|---|---|---|
| 2001 | 2000 | prod | 59.6 (0.26) | 37.9 (0.35) | 74.3 (0.29) | 62.6 (0.28) | 40.3 (0.57) | 53.1 (0.39) | 63.7 (0.31) |
| 2002 | 2001 | prod | 58.3 (0.27) | 36.3 (0.35) | 73.6 (0.30) | 61.6 (0.28) | 37.4 (0.57) | 51.1 (0.40) | 62.7 (0.31) |
| 2003 | 2002 | prod | 56.0 (0.27) | 35.1 (0.34) | 71.1 (0.31) | 59.3 (0.29) | 36.7 (0.56) | 48.9 (0.41) | 60.3 (0.32) |
| 2004 | 2003 | prod | 56.0 (0.27) | 34.6 (0.34) | 71.9 (0.31) | 59.4 (0.29) | 36.9 (0.55) | 48.1 (0.41) | 60.8 (0.32) |
| 2005 | 2004 | prod | 55.8 (0.27) | 35.1 (0.34) | 71.0 (0.30) | 59.0 (0.28) | 37.6 (0.53) | 48.0 (0.38) | 60.4 (0.33) |
| 2006 | 2005 | prod | 53.8 (0.29) | 33.1 (0.34) | 69.1 (0.37) | 57.0 (0.31) | 35.2 (0.55) | 45.5 (0.44) | 58.7 (0.33) |
| 2007 | 2006 | prod | 52.0 (0.28) | 31.5 (0.34) | 66.8 (0.33) | 55.1 (0.29) | 33.2 (0.62) | 44.5 (0.46) | 56.4 (0.33) |
| 2008 | 2007 | prod | 54.0 (0.29) | 33.0 (0.39) | 68.9 (0.33) | 57.1 (0.31) | 34.4 (0.52) | 45.9 (0.43) | 58.6 (0.34) |
| 2009 | 2008 | prod | 52.1 (0.25) | 31.6 (0.30) | 66.9 (0.31) | 55.8 (0.27) | 32.1 (0.55) | 44.7 (0.39) | 56.5 (0.30) |
| 2010 | 2009 | prod | 50.5 (0.28) | 30.1 (0.39) | 65.1 (0.34) | 54.7 (0.31) | 29.9 (0.53) | 42.0 (0.41) | 55.3 (0.32) |
| 2011 | 2010 | prod | 50.3 (0.27) | 29.7 (0.39) | 65.0 (0.32) | 54.7 (0.29) | 29.7 (0.52) | 42.4 (0.48) | 54.8 (0.31) |
| 2012 | 2011 | prod | 50.0 (0.27) | 29.1 (0.38) | 64.7 (0.33) | 54.1 (0.30) | 30.0 (0.48) | 42.0 (0.43) | 54.6 (0.33) |
| 2013 | 2012 | prod | 49.7 (0.27) | 29.3 (0.33) | 64.1 (0.32) | 54.2 (0.28) | 28.2 (0.53) | 41.3 (0.45) | 54.6 (0.29) |
| 2014 | 2013 | 2014 redesign 3/8 | 48.0 (0.45) | 29.3 (0.67) | 61.5 (0.57) | 51.6 (0.49) | 30.4 (1.01) | 42.5 (0.74) | 51.1 (0.52) |
| 2014 | 2013 | 2014 trad 5/8 | 52.7 (0.32) | 31.0 (0.47) | 67.5 (0.40) | 56.8 (0.33) | 32.5 (0.69) | 44.8 (0.51) | 57.4 (0.41) |
| 2015 | 2014 | prod | 46.0 (0.26) | 27.5 (0.32) | 58.7 (0.35) | 49.1 (0.28) | 29.6 (0.54) | 40.6 (0.41) | 49.1 (0.31) |
| 2016 | 2015 | prod | 42.4 (0.30) | 24.5 (0.37) | 54.3 (0.36) | 45.2 (0.35) | 27.3 (0.58) | 36.9 (0.46) | 45.7 (0.36) |
| 2017 | 2016 | prod | 40.4 (0.25) | 23.1 (0.34) | 51.8 (0.32) | 43.1 (0.29) | 25.4 (0.51) | 35.7 (0.41) | 43.2 (0.33) |
| 2017 | 2016 | 2017 research (updated proc.) | 40.5 (0.27) | 23.5 (0.37) | 51.7 (0.34) | 43.2 (0.32) | 25.8 (0.49) | 35.9 (0.43) | 43.3 (0.34) |
| 2018 | 2017 | 2018 bridge (updated proc.) | 41.2 (0.27) | 24.7 (0.34) | 51.7 (0.37) | 43.7 (0.31) | 26.3 (0.56) | 37.0 (0.42) | 43.7 (0.33) |
| 2018 | 2017 | prod | 41.1 (0.28) | 24.5 (0.37) | 51.7 (0.38) | 43.5 (0.31) | 26.8 (0.56) | 36.8 (0.45) | 43.7 (0.33) |
| 2019 | 2018 | prod | 40.1 (0.32) | 23.9 (0.36) | 50.2 (0.40) | 42.3 (0.35) | 27.3 (0.60) | 36.6 (0.46) | 42.3 (0.38) |
| 2020 | 2019 | prod | 39.5 (0.26) | 22.7 (0.34) | 50.0 (0.37) | 41.9 (0.29) | 25.7 (0.60) | 34.6 (0.50) | 42.5 (0.32) |
| 2021 | 2020 | prod | 38.8 (0.33) | 22.4 (0.40) | 48.8 (0.43) | 41.3 (0.36) | 24.1 (0.57) | 34.2 (0.48) | 41.6 (0.38) |
| 2022 | 2021 | prod | 37.8 (0.32) | 22.0 (0.38) | 47.1 (0.39) | 39.8 (0.36) | 25.0 (0.67) | 34.6 (0.48) | 39.8 (0.37) |
| 2023 | 2022 | prod | 37.8 (0.32) | 21.8 (0.38) | 47.1 (0.39) | 39.8 (0.34) | 24.2 (0.72) | 34.1 (0.48) | 39.9 (0.37) |
| 2024 | 2023 | prod | 37.9 (0.34) | 22.3 (0.43) | 47.0 (0.40) | 40.0 (0.36) | 25.3 (0.69) | 34.6 (0.55) | 39.9 (0.39) |
| 2025 | 2024 | prod | 36.1 (0.31) | 21.2 (0.38) | 44.8 (0.40) | 38.1 (0.33) | 23.8 (0.65) | 33.4 (0.49) | 37.7 (0.36) |
| 2026 | 2025 | prod | 35.9 (0.32) | 22.4 (0.43) | 43.7 (0.40) | 38.0 (0.35) | 23.3 (0.66) | 32.3 (0.54) | 38.1 (0.38) |

**Participation: included in plan (PENINCL=1), all workers** — % (SE)

| ASEC | Income yr | File | all_21_64 | emp_lt100 | emp_100plus | fulltime_35h | parttime_lt35h | age_21_34 | age_35_64 |
|---|---|---|---|---|---|---|---|---|---|
| 2001 | 2000 | prod | 46.9 (0.25) | 28.7 (0.32) | 59.2 (0.31) | 51.1 (0.28) | 19.5 (0.47) | 35.6 (0.34) | 54.0 (0.32) |
| 2002 | 2001 | prod | 45.6 (0.25) | 27.6 (0.32) | 58.2 (0.32) | 50.0 (0.28) | 18.2 (0.46) | 34.1 (0.35) | 52.6 (0.32) |
| 2003 | 2002 | prod | 43.8 (0.25) | 26.7 (0.31) | 56.1 (0.32) | 48.3 (0.28) | 17.5 (0.44) | 31.8 (0.35) | 51.0 (0.32) |
| 2004 | 2003 | prod | 43.9 (0.25) | 26.9 (0.31) | 56.5 (0.33) | 48.5 (0.29) | 17.8 (0.44) | 31.9 (0.35) | 51.2 (0.33) |
| 2005 | 2004 | prod | 43.9 (0.26) | 27.1 (0.31) | 56.1 (0.32) | 48.4 (0.29) | 17.9 (0.41) | 31.8 (0.34) | 51.0 (0.34) |
| 2006 | 2005 | prod | 42.5 (0.26) | 25.6 (0.32) | 55.0 (0.34) | 46.7 (0.29) | 17.8 (0.45) | 30.1 (0.35) | 49.8 (0.32) |
| 2007 | 2006 | prod | 41.3 (0.25) | 24.5 (0.31) | 53.4 (0.34) | 45.4 (0.26) | 16.3 (0.49) | 30.2 (0.36) | 47.8 (0.33) |
| 2008 | 2007 | prod | 42.9 (0.27) | 25.9 (0.34) | 55.0 (0.33) | 47.2 (0.29) | 16.7 (0.47) | 30.7 (0.38) | 50.0 (0.33) |
| 2009 | 2008 | prod | 41.4 (0.22) | 25.2 (0.29) | 53.1 (0.30) | 46.1 (0.26) | 15.8 (0.38) | 30.3 (0.35) | 47.8 (0.28) |
| 2010 | 2009 | prod | 40.2 (0.26) | 23.5 (0.35) | 52.2 (0.33) | 45.4 (0.30) | 15.1 (0.41) | 28.6 (0.35) | 46.8 (0.33) |
| 2011 | 2010 | prod | 40.4 (0.25) | 23.3 (0.33) | 52.6 (0.34) | 45.8 (0.28) | 15.0 (0.36) | 29.1 (0.40) | 46.9 (0.29) |
| 2012 | 2011 | prod | 40.1 (0.23) | 23.0 (0.34) | 52.0 (0.33) | 45.2 (0.27) | 15.4 (0.36) | 28.4 (0.34) | 46.8 (0.31) |
| 2013 | 2012 | prod | 40.0 (0.25) | 23.0 (0.31) | 51.9 (0.31) | 45.5 (0.28) | 13.5 (0.39) | 28.2 (0.41) | 46.9 (0.29) |
| 2014 | 2013 | 2014 redesign 3/8 | 37.3 (0.41) | 22.2 (0.57) | 48.3 (0.57) | 42.4 (0.46) | 12.4 (0.61) | 27.5 (0.65) | 43.0 (0.49) |
| 2014 | 2013 | 2014 trad 5/8 | 41.8 (0.32) | 23.9 (0.42) | 53.9 (0.41) | 47.2 (0.35) | 15.2 (0.48) | 29.9 (0.51) | 48.7 (0.38) |
| 2015 | 2014 | prod | 35.5 (0.24) | 20.7 (0.30) | 45.6 (0.33) | 39.7 (0.26) | 13.5 (0.40) | 26.5 (0.35) | 40.8 (0.30) |
| 2016 | 2015 | prod | 32.4 (0.29) | 18.1 (0.32) | 41.8 (0.37) | 36.2 (0.32) | 11.2 (0.38) | 23.2 (0.39) | 37.8 (0.35) |
| 2017 | 2016 | prod | 31.1 (0.24) | 17.0 (0.30) | 40.4 (0.33) | 34.8 (0.27) | 10.4 (0.37) | 23.3 (0.38) | 35.8 (0.31) |
| 2017 | 2016 | 2017 research (updated proc.) | 31.3 (0.25) | 17.3 (0.32) | 40.5 (0.32) | 35.0 (0.29) | 11.1 (0.37) | 23.6 (0.40) | 36.0 (0.30) |
| 2018 | 2017 | 2018 bridge (updated proc.) | 31.7 (0.25) | 18.6 (0.30) | 40.1 (0.34) | 35.1 (0.28) | 11.8 (0.38) | 23.7 (0.36) | 36.5 (0.32) |
| 2018 | 2017 | prod | 31.8 (0.25) | 18.5 (0.33) | 40.3 (0.35) | 35.2 (0.28) | 12.1 (0.39) | 23.8 (0.39) | 36.6 (0.31) |
| 2019 | 2018 | prod | 31.2 (0.29) | 18.0 (0.33) | 39.3 (0.36) | 34.2 (0.32) | 12.8 (0.49) | 24.7 (0.38) | 35.1 (0.36) |
| 2020 | 2019 | prod | 31.4 (0.24) | 17.3 (0.30) | 40.2 (0.36) | 34.8 (0.27) | 11.4 (0.44) | 24.1 (0.45) | 35.8 (0.31) |
| 2021 | 2020 | prod | 30.6 (0.30) | 16.9 (0.35) | 39.0 (0.40) | 33.9 (0.33) | 10.9 (0.45) | 23.8 (0.45) | 34.7 (0.35) |
| 2022 | 2021 | prod | 30.0 (0.29) | 16.7 (0.33) | 37.7 (0.37) | 32.8 (0.34) | 11.4 (0.47) | 24.0 (0.42) | 33.5 (0.34) |
| 2023 | 2022 | prod | 29.5 (0.29) | 15.8 (0.33) | 37.5 (0.36) | 32.1 (0.32) | 11.9 (0.47) | 23.5 (0.46) | 33.1 (0.34) |
| 2024 | 2023 | prod | 29.6 (0.31) | 16.9 (0.38) | 37.0 (0.37) | 32.5 (0.34) | 11.5 (0.49) | 23.4 (0.47) | 33.2 (0.36) |
| 2025 | 2024 | prod | 28.1 (0.27) | 15.5 (0.33) | 35.4 (0.35) | 31.0 (0.31) | 10.7 (0.41) | 22.6 (0.42) | 31.3 (0.33) |
| 2026 | 2025 | prod | 28.4 (0.28) | 16.9 (0.38) | 34.9 (0.38) | 31.3 (0.32) | 10.9 (0.47) | 22.9 (0.50) | 31.6 (0.34) |

**Take-up: participation among those offered** — % (SE)

| ASEC | Income yr | File | all_21_64 | emp_lt100 | emp_100plus | fulltime_35h | parttime_lt35h | age_21_34 | age_35_64 |
|---|---|---|---|---|---|---|---|---|---|
| 2001 | 2000 | prod | 78.7 (0.25) | 75.9 (0.50) | 79.7 (0.29) | 81.7 (0.24) | 48.3 (0.97) | 67.1 (0.50) | 84.8 (0.26) |
| 2002 | 2001 | prod | 78.2 (0.26) | 76.0 (0.51) | 79.0 (0.29) | 81.1 (0.25) | 48.8 (1.01) | 66.7 (0.52) | 84.0 (0.27) |
| 2003 | 2002 | prod | 78.2 (0.27) | 76.2 (0.52) | 79.0 (0.30) | 81.4 (0.25) | 47.8 (1.02) | 65.1 (0.54) | 84.6 (0.27) |
| 2004 | 2003 | prod | 78.4 (0.27) | 77.7 (0.51) | 78.6 (0.31) | 81.7 (0.25) | 48.3 (0.99) | 66.2 (0.55) | 84.2 (0.28) |
| 2005 | 2004 | prod | 78.6 (0.27) | 77.2 (0.46) | 79.0 (0.32) | 82.0 (0.25) | 47.5 (0.96) | 66.2 (0.54) | 84.4 (0.28) |
| 2006 | 2005 | prod | 79.0 (0.27) | 77.4 (0.55) | 79.6 (0.30) | 82.0 (0.26) | 50.7 (1.03) | 66.2 (0.55) | 84.9 (0.28) |
| 2007 | 2006 | prod | 79.4 (0.30) | 77.7 (0.56) | 80.0 (0.35) | 82.3 (0.28) | 49.2 (1.17) | 67.9 (0.51) | 84.7 (0.31) |
| 2008 | 2007 | prod | 79.6 (0.27) | 78.5 (0.51) | 79.9 (0.30) | 82.6 (0.25) | 48.6 (1.12) | 67.0 (0.60) | 85.3 (0.25) |
| 2009 | 2008 | prod | 79.4 (0.27) | 79.6 (0.55) | 79.3 (0.31) | 82.6 (0.25) | 49.1 (0.99) | 67.8 (0.58) | 84.7 (0.25) |
| 2010 | 2009 | prod | 79.6 (0.29) | 78.1 (0.54) | 80.1 (0.34) | 82.9 (0.28) | 50.5 (1.07) | 68.1 (0.60) | 84.6 (0.29) |
| 2011 | 2010 | prod | 80.3 (0.28) | 78.4 (0.53) | 80.9 (0.32) | 83.7 (0.28) | 50.6 (0.96) | 68.5 (0.61) | 85.6 (0.27) |
| 2012 | 2011 | prod | 80.2 (0.28) | 79.2 (0.51) | 80.5 (0.33) | 83.5 (0.29) | 51.4 (0.88) | 67.6 (0.59) | 85.7 (0.26) |
| 2013 | 2012 | prod | 80.4 (0.26) | 78.6 (0.53) | 81.0 (0.28) | 84.0 (0.25) | 48.0 (1.03) | 68.2 (0.58) | 85.8 (0.27) |
| 2014 | 2013 | 2014 redesign 3/8 | 77.8 (0.52) | 75.7 (0.98) | 78.6 (0.62) | 82.3 (0.47) | 40.9 (1.77) | 64.6 (1.09) | 84.1 (0.49) |
| 2014 | 2013 | 2014 trad 5/8 | 79.2 (0.39) | 77.1 (0.68) | 79.9 (0.43) | 83.0 (0.38) | 46.7 (1.18) | 66.7 (0.81) | 84.9 (0.34) |
| 2015 | 2014 | prod | 77.2 (0.31) | 75.3 (0.59) | 77.8 (0.35) | 80.8 (0.31) | 45.8 (1.11) | 65.2 (0.56) | 83.0 (0.33) |
| 2016 | 2015 | prod | 76.3 (0.35) | 74.1 (0.73) | 76.9 (0.41) | 80.2 (0.34) | 41.1 (1.11) | 62.9 (0.68) | 82.6 (0.36) |
| 2017 | 2016 | prod | 77.0 (0.35) | 73.4 (0.68) | 78.1 (0.38) | 80.8 (0.33) | 41.1 (1.34) | 65.3 (0.70) | 82.8 (0.34) |
| 2017 | 2016 | 2017 research (updated proc.) | 77.3 (0.31) | 73.6 (0.64) | 78.4 (0.34) | 81.0 (0.31) | 43.1 (1.23) | 65.8 (0.66) | 83.0 (0.33) |
| 2018 | 2017 | 2018 bridge (updated proc.) | 77.0 (0.30) | 75.3 (0.56) | 77.6 (0.34) | 80.3 (0.31) | 44.9 (1.13) | 64.0 (0.65) | 83.6 (0.36) |
| 2018 | 2017 | prod | 77.4 (0.31) | 75.5 (0.60) | 77.9 (0.35) | 80.7 (0.31) | 45.1 (1.19) | 64.6 (0.68) | 83.8 (0.34) |
| 2019 | 2018 | prod | 77.6 (0.35) | 75.4 (0.71) | 78.3 (0.41) | 80.9 (0.33) | 47.0 (1.48) | 67.5 (0.70) | 82.9 (0.36) |
| 2020 | 2019 | prod | 79.4 (0.37) | 75.9 (0.82) | 80.4 (0.41) | 83.1 (0.35) | 44.2 (1.44) | 69.6 (0.74) | 84.2 (0.41) |
| 2021 | 2020 | prod | 78.9 (0.37) | 75.6 (0.85) | 79.8 (0.42) | 82.2 (0.36) | 45.3 (1.51) | 69.5 (0.74) | 83.5 (0.40) |
| 2022 | 2021 | prod | 79.2 (0.36) | 76.1 (0.71) | 80.0 (0.42) | 82.4 (0.37) | 45.7 (1.48) | 69.3 (0.75) | 84.2 (0.39) |
| 2023 | 2022 | prod | 78.1 (0.39) | 72.5 (0.93) | 79.6 (0.44) | 80.7 (0.40) | 49.1 (1.60) | 68.8 (0.80) | 82.8 (0.42) |
| 2024 | 2023 | prod | 78.0 (0.41) | 75.7 (0.83) | 78.7 (0.46) | 81.3 (0.40) | 45.7 (1.49) | 67.7 (0.77) | 83.2 (0.40) |
| 2025 | 2024 | prod | 77.8 (0.37) | 73.4 (0.90) | 79.0 (0.42) | 81.2 (0.40) | 45.0 (1.37) | 67.6 (0.76) | 83.1 (0.42) |
| 2026 | 2025 | prod | 79.0 (0.40) | 75.7 (0.88) | 79.9 (0.47) | 82.2 (0.39) | 46.6 (1.69) | 71.0 (0.92) | 83.0 (0.41) |

**Participation by detailed employer size (codes 2/3 = 10-24/25-99 through ASEC 2010, 10-49/50-99 from ASEC 2011)** — % (SE)

| ASEC | Income yr | File | emp_lt10 | emp_10_24 | emp_10_49 | emp_25_99 | emp_50_99 | emp_100_499 | emp_500_999 | emp_1000plus |
|---|---|---|---|---|---|---|---|---|---|---|
| 2001 | 2000 | prod | 18.2 (0.45) | 26.7 (0.61) | nan | 39.8 (0.57) | nan | 52.5 (0.59) | 55.9 (0.91) | 62.4 (0.38) |
| 2002 | 2001 | prod | 16.5 (0.43) | 25.7 (0.60) | nan | 39.2 (0.57) | nan | 50.4 (0.60) | 56.1 (0.91) | 61.7 (0.38) |
| 2003 | 2002 | prod | 15.8 (0.42) | 25.1 (0.60) | nan | 38.3 (0.57) | nan | 48.6 (0.60) | 55.4 (0.94) | 59.5 (0.39) |
| 2004 | 2003 | prod | 15.4 (0.41) | 25.4 (0.59) | nan | 39.4 (0.58) | nan | 49.3 (0.61) | 51.7 (0.96) | 60.3 (0.40) |
| 2005 | 2004 | prod | 15.3 (0.42) | 26.7 (0.58) | nan | 39.5 (0.61) | nan | 49.3 (0.64) | 54.4 (1.00) | 59.2 (0.40) |
| 2006 | 2005 | prod | 15.1 (0.46) | 24.5 (0.61) | nan | 36.4 (0.57) | nan | 48.3 (0.61) | 53.9 (1.02) | 58.0 (0.42) |
| 2007 | 2006 | prod | 14.0 (0.46) | 23.4 (0.56) | nan | 34.9 (0.58) | nan | 45.6 (0.63) | 51.4 (0.95) | 57.1 (0.40) |
| 2008 | 2007 | prod | 15.2 (0.40) | 25.1 (0.65) | nan | 36.8 (0.52) | nan | 48.3 (0.58) | 53.8 (0.93) | 58.0 (0.41) |
| 2009 | 2008 | prod | 14.7 (0.37) | 23.8 (0.59) | nan | 36.4 (0.58) | nan | 46.8 (0.57) | 51.2 (0.95) | 55.9 (0.39) |
| 2010 | 2009 | prod | 13.4 (0.40) | 23.3 (0.59) | nan | 33.9 (0.60) | nan | 43.7 (0.65) | 53.2 (0.96) | 55.2 (0.39) |
| 2011 | 2010 | prod | 14.3 (0.45) | nan | 25.3 (0.50) | nan | 35.0 (0.81) | 45.4 (0.66) | 49.3 (0.90) | 55.7 (0.40) |
| 2012 | 2011 | prod | 14.2 (0.39) | nan | 24.5 (0.56) | nan | 35.3 (0.77) | 44.4 (0.64) | 49.9 (1.11) | 55.1 (0.41) |
| 2013 | 2012 | prod | 13.2 (0.41) | nan | 24.4 (0.53) | nan | 36.6 (0.66) | 44.8 (0.64) | 49.3 (1.14) | 54.9 (0.39) |
| 2014 | 2013 | 2014 redesign 3/8 | 12.3 (0.76) | nan | 24.0 (0.91) | nan | 35.5 (1.44) | 43.0 (1.14) | 46.5 (1.76) | 50.7 (0.67) |
| 2014 | 2013 | 2014 trad 5/8 | 13.2 (0.51) | nan | 25.6 (0.58) | nan | 38.3 (0.93) | 47.1 (0.75) | 49.8 (1.30) | 57.0 (0.49) |
| 2015 | 2014 | prod | 11.8 (0.43) | nan | 22.3 (0.44) | nan | 32.1 (0.69) | 39.1 (0.62) | 44.2 (1.04) | 48.3 (0.39) |
| 2016 | 2015 | prod | 11.2 (0.43) | nan | 18.4 (0.46) | nan | 28.9 (0.81) | 34.6 (0.69) | 39.8 (0.99) | 44.6 (0.44) |
| 2017 | 2016 | prod | 10.1 (0.43) | nan | 17.9 (0.48) | nan | 26.3 (0.71) | 35.2 (0.68) | 38.8 (0.98) | 42.5 (0.38) |
| 2017 | 2016 | 2017 research (updated proc.) | 10.5 (0.44) | nan | 17.9 (0.50) | nan | 27.1 (0.65) | 35.2 (0.65) | 39.5 (1.00) | 42.5 (0.38) |
| 2018 | 2017 | 2018 bridge (updated proc.) | 10.7 (0.39) | nan | 19.6 (0.51) | nan | 29.1 (0.77) | 34.1 (0.70) | 39.4 (1.04) | 42.3 (0.40) |
| 2018 | 2017 | prod | 10.5 (0.39) | nan | 19.7 (0.49) | nan | 28.8 (0.81) | 34.1 (0.68) | 39.4 (1.13) | 42.6 (0.41) |
| 2019 | 2018 | prod | 10.2 (0.44) | nan | 19.4 (0.48) | nan | 27.5 (0.78) | 33.1 (0.67) | 39.4 (1.02) | 41.4 (0.44) |
| 2020 | 2019 | prod | 9.5 (0.38) | nan | 18.4 (0.53) | nan | 26.5 (0.74) | 33.9 (0.76) | 40.0 (1.10) | 42.3 (0.41) |
| 2021 | 2020 | prod | 9.1 (0.38) | nan | 18.7 (0.57) | nan | 25.9 (0.77) | 34.4 (0.70) | 36.1 (1.12) | 40.7 (0.45) |
| 2022 | 2021 | prod | 9.9 (0.47) | nan | 17.2 (0.48) | nan | 26.7 (0.83) | 32.8 (0.74) | 36.4 (0.98) | 39.4 (0.45) |
| 2023 | 2022 | prod | 8.8 (0.43) | nan | 17.1 (0.48) | nan | 24.1 (0.87) | 32.2 (0.68) | 33.3 (1.17) | 39.7 (0.46) |
| 2024 | 2023 | prod | 9.3 (0.45) | nan | 17.9 (0.52) | nan | 26.6 (0.87) | 31.8 (0.72) | 35.3 (0.99) | 38.9 (0.45) |
| 2025 | 2024 | prod | 9.2 (0.47) | nan | 16.8 (0.50) | nan | 22.5 (0.87) | 30.5 (0.81) | 32.0 (0.98) | 37.3 (0.42) |
| 2026 | 2025 | prod | 10.4 (0.50) | nan | 17.6 (0.50) | nan | 25.9 (0.92) | 29.9 (0.77) | 35.2 (1.10) | 36.5 (0.44) |

## 5. Measurement breaks

### Takeaway
- **2014 questionnaire redesign (large).** Comparing the redesigned 3/8 subsample with the traditional 5/8 subsample in the same ASEC 2014 (random split):
  - Offer is lower by 4.8 pp (SE 0.55) and participation by 4.5 pp (SE 0.52). Take-up is lower by only 1.4 pp (SE 0.65).
  - The drop is concentrated among workers at employers of 100+ (participation −5.5 pp), full-time workers (−4.7) and ages 35-64 (−5.7). At employers under 100 it is −1.7, and at ages 21-34 −2.5.
  - This matches EBRI's finding that the groups most likely to participate were hit hardest.
- **2019 processing change (negligible).** On identical samples, with paired replicate SEs, the 2018 bridge file minus production is +0.08 pp for offer (SE 0.13) and −0.08 for participation (SE 0.12). The 2017 research file minus production is +0.13 (0.12) and +0.21 (0.12). No difference exceeds 0.4 pp except part-time take-up in 2017 (+2.0, SE 0.8).
  - The processing change matters a lot for account withdrawals (see `cps/README.md`) but not for these pension items.
- **After 2014 the CPS keeps falling.**
  - Participation went from 37.3% (2014 redesign subsample) to 35.5% (income year 2014), 32.4% (2015) and 31.1% (2016).
  - It then drifts down about 0.3-0.4 pp a year, to 28.4% in income year 2025.
  - Offer goes from 48.0% to 35.9%.
  - Take-up stays at 77-80%. The decline is therefore in *reported offer*, which is the item that is implausible against employer-side data (next bullet).

### Cited findings
- EBRI (Craig Copeland), "Current Population Survey: Issues Continue for Retirement Plan Participation and Retiree Income Estimates", EBRI Issue Brief, June 12, 2018 — [ebri.org](https://www.ebri.org/content/current-population-survey-issues-continue-for-retirement-plan-participation-and-retiree-income-estimates). Key quotes:
  - "After the CPS redesign, despite no changes to the retirement plan questions, the estimates of the percentage of workers who participated in an employment-based retirement plan decreased dramatically."
  - Full-time full-year wage and salary workers 21-64: "from 54.5 percent before the questionnaire redesign to 41.0 percent in 2016."
  - From the NCS, "the percentage of private-sector wage and salary workers at establishments with 500 or more employees participating ... remained relatively flat between 2013 and 2016, at around 76 percent," while CPS "decreased from 64 percent before the redesign in 2013 to 47 percent in 2016."
- EBRI (Copeland), "Current Population Survey: Checking in on the Retirement Plan Participation and Retiree Income Estimates", May 30, 2019 — [ebri.org](https://www.ebri.org/content/current-population-survey-checking-in-on-the-retirement-plan-participation-and-retiree-income-estimates). The 2017 figure "held steady ... at 41.4 percent compared with 41.0 percent in 2016"; for 500+ establishments, CPS "decreased from 64 percent in 2013 ... to 47 percent in 2017."
- EBRI (Copeland), "Retirement Plan Participation and the Current Population Survey: The Impact of New Income Questions on These Estimates", Jan 30, 2020 — [ebri.org](https://www.ebri.org/content/retirement-plan-participation-and-the-current-population-survey-the-impact-of-new-income-questions-on-these-estimates).
  - Participation "stood at 31.6 percent for all workers [2018] compared with 39.7 percent in 2011."
  - "when adjustments were made for the new questions [counting workers with retirement-account income from the 2019 items], the percentage participating increased to 47.5 percent."
  - Form 5500 active participants rose "from 89.9 million in 2014 to 94.6 million in 2017."
- EBRI (Copeland), "The Effect of the Current Population Survey Redesign on Retirement-Plan Participation Estimates", EBRI Notes, Dec 2015 — [ebri.org summary](https://www.ebri.org/retirement/content/ebri-research-questions-the-decline-in-retirement-plan-participation-shown-in-the-current-population-survey). The redesign cut participation "from 64 percent under the old questionnaire to 58 percent under the redesigned questionnaire for the same year" [recordkeeper/industry: EBRI is industry-funded; the analysis uses public CPS data].
- Alicia Munnell (CRR), "Lack of Coverage Is the Biggest Problem with Our Retirement System", May 13, 2022 — [crr.bc.edu](https://crr.bc.edu/lack-of-coverage-is-the-biggest-problem-with-our-retirement-system/).
  - It relays John Sabelhaus's explanation: "new questions were inserted *before* the coverage questions" about retirement accounts and withdrawals, so "some respondents might have perceived that they were asking about *additional* retirement plans."
  - It cites Sabelhaus's W-2-based estimate that "52 percent" of private-sector workers aged 18-65 were covered in 2019-2021.
- BLS National Compensation Survey (employer-reported), March 2026, private industry. Establishments with 1-99 workers: 59% access, 39% participation, 66% take-up. Establishments with 100+: 87% access, 68% participation, 77% take-up. Overall participation is 52% — [BLS Employee Benefits news release, Sept 25, 2026](https://www.bls.gov/news.release/ebs2.htm). By contrast, the CPS employers-100+ offer rate in income year 2025 is 43.7% (Computed). (The NCS is establishment-size based and counts workers at establishments, so it is not like-for-like, but the gap is about 40 points.)
- Census also documents broad underreporting of retirement income in the redesigned ASEC: "Measuring Income of the Aged in Household Surveys: Evidence from Linked Administrative Records", CES-WP-24-32, 2024 — [census.gov](https://www.census.gov/library/working-papers/2024/adrm/CES-WP-24-32.html). This concerns income, not coverage. No Census working paper specific to the coverage undercount was found (unverified gap).

**Break table (Computed; `cps_participation_breaks_ppa.csv`), all private workers 21-64:**

| Comparison | Offer diff (SE) | Participation diff (SE) | Take-up diff (SE) |
|---|---|---|---|
| 2014 redesign 3/8 − traditional 5/8 | −4.78 (0.55) | −4.46 (0.52) | −1.40 (0.65) |
| 2017 research − production (same sample) | +0.13 (0.12) | +0.21 (0.12) | +0.28 (0.18) |
| 2018 bridge − production (same sample) | +0.08 (0.13) | −0.08 (0.12) | −0.33 (0.19) |

### Evidence verdict
- The 2014 break is strong and clearly measured.
- The 2019 processing change has no material effect on these items.
- The post-2014 downward drift is very likely an artifact, judging by the contradicting NCS, Form 5500 and W-2 evidence. That makes CPS levels after 2013 unusable for "did participation rise" questions. Within-CPS *relative* comparisons (subgroups, states) remain usable if the artifact is common across groups. EBRI 2019 found that ratios between demographic groups were "nearly identical before and after the survey redesign."

### Gaps
- No admin-linked validation of PENPLAN/PENINCL (for example, CPS linked to W-2 box 12/box 13) was found in a Census publication.
- Allocation (imputation) rates for PENPLAN/PENINCL were not tabulated here. The I_PENPL-type flags exist in the files.

## 6. Did participation rise after the PPA of 2006?

### Takeaway
- The PPA was signed August 2006, with auto-enrollment safe harbors from plan years 2008. The comparison is the mean of ASEC 2003-2007 (income years 2002-2006) against ASEC 2010-2013 (income years 2009-2012). Both windows are before the 2014 redesign, on the same questionnaire.
- **Results (Computed):**
  - Take-up among the offered rose +1.41 pp (78.71 → 80.12; SE 0.19).
  - Offer fell −4.62 pp (54.73 → 50.11) and participation fell −2.93 pp (43.07 → 40.15).
- The take-up gain is broad: +1.8 at ages 21-34, +1.4 at employers of 100+, +1.3 under 100, +1.6 full-time and +1.4 part-time.
- Year by year, take-up was flat at 78.2-78.6% in ASEC 2002-2005, then climbed to 79.0-79.6% (2006-2010) and 80.2-80.4% (2011-2013).
- The rise starts in ASEC 2006 (income year 2005), before the PPA. That is consistent with early adoption of auto-enrollment by large sponsors, or with other trends; the CPS cannot separate them.
- The 2007-2009 recession is a confounder: offer fell, and the composition of employment shifted toward workers in jobs with plans and with tenure. Read the take-up rise as consistent with modest PPA-era auto-enrollment, not as causal.

### Cited findings
- Computed from `cps_plan_participation_by_year.csv` and `cps_participation_breaks_ppa.csv`. SEs treat years as independent, which is conservative.
- Caveat on the measure: PENPLAN asks whether the employer had a plan "for any of the employees". So "take-up" mixes the ineligible with those who opted out. Auto-enrollment moves only the opt-out part, and recordkeeper data show much larger effects in auto-enroll plans (see the other dc_policy notes).

### Evidence verdict
- Weak positive evidence for take-up (about +1.4 pp, highly significant).
- No evidence of rising participation overall, because the share offered declined over 2000-2012.

### Gaps
- The CPS cannot identify whether a plan auto-enrolls, plan eligibility, or tenure.
- A cleaner test would need the SIPP or the NCS (employer-side take-up), or W-2 data.

## 7. State auto-IRA mandates (descriptive; suggestive only)

### Takeaway
- **Design:** private workers 21-64 at employers with fewer than 100 workers, pooled by period.
  - Waves: early = OR, IL, CA; mid = CT, MD, CO, VA; late = ME, DE, NJ, VT, NV, MN, RI, NY, HI. "None" is all other states and DC.
  - Periods: pre = income years 2012-2016; rollout = 2017-2020; post = 2021-2025.
  - One file per year: production, with the 2014 3/8 file for income year 2013.
  - Yearly estimates are averaged with equal year weights.
- **Results (Computed):**
  - Early-wave states vs other states, post vs pre: DiD offer +1.1 pp (SE 0.75), participation +0.1 (0.68), take-up −3.3 (1.38).
  - OR+IL alone: offer +1.3 (1.29), participation +0.1 (1.12).
  - CA alone: offer +1.0 (0.86), participation +0.1 (0.77).
  - Year-by-year early-wave gaps in offer and participation show no break after 2018-2020.
- Participation shows no detectable rise. The early states' small relative gain in reported *offer* comes with a relative fall in *take-up*. That pattern fits auto-IRA-covered workers saying the employer "has a plan" but not that they are "included", or workers who opted out. It cannot be distinguished from noise.
- **Respondent framing.** An auto-IRA is not an employer plan. Respondents may or may not report it as "a pension or other type of retirement plan" at work, so the CPS is a poor instrument for this question.

### Cited findings — program timing (verify before reuse)
- **OregonSaves** registration deadlines: 100+ employees by Nov 15, 2017; 50-99 by May 15, 2018; 20-49 by Dec 15, 2018. Smaller employers followed in 2019-2020 — [Paylocity compliance alert / Oregon Business](https://oregonbusiness.com/18097-oregonsaves-what-employers-need-to-know/). (oregonsaves.gov did not resolve from this environment.) In this analysis, Oregon's <100 employers are treated from income year 2019.
- **Illinois Secure Choice** waves: pilot May 2018; ≥500 employees Nov 2018; 100-499 Jul 2019; 25-99 Nov 2019; 16-24 Nov 2022; 5-15 Nov 2023 — [Georgetown CRI webinar slides, Mar 27, 2025](https://cri.georgetown.edu/wp-content/uploads/2025/03/3-27-25-States-and-Access_Webinar-Slide-Deck_Final-32725.pdf). Treated from 2020.
- **CalSavers** deadlines: 100+ employees Sept 30, 2020; 50+ June 30, 2021; 5+ June 30, 2022 — [Greenberg Glusker](https://www.greenbergglusker.com/publications/coming-up-calsavers-compliance-deadlines-what-california-employers-should-know); [Fenwick](https://fenwick.com/insights/publications/eligible-california-employers-with-5-or-more-employees-must-comply-with-calsavers-retirement-savings-trust-act-by-june-30-2022). Treated from 2021.
- **Launch years** — [AARP, "States with automatic IRA savings programs", updated June 3, 2026](https://www.aarp.org/money/retirement/states-with-automatic-ira-savings-programs/) [advocacy group]:
  - "MyCTSavings ... launched 2022"
  - "Maryland$aves ... launched 2022"
  - "Colorado SecureSavings ... launched 2023"
  - "RetirePath Virginia ... launched 2023"
  - "Maine ... MERIT ... launched 2023"
  - "Delaware EARNS ... launched 2024"
  - "Nevada ... NEST ... launched 2025"
  - "New York State Secure Choice ... launched 2025"
  - "RISavers ... launched 2025"
  - "Minnesota Secure Choice ... launched January 2026"
- **NJ RetireReady (2024) and VT Saves (Dec 2024 / July 2025)** — [CRI slides](https://cri.georgetown.edu/wp-content/uploads/2025/03/3-27-25-States-and-Access_Webinar-Slide-Deck_Final-32725.pdf); [InvestmentNews on VT Saves](https://www.investmentnews.com/?p=252169).
- Treatment years for CT, MD, CO and VA follow their launches: CT 2023, MD 2023, CO 2023, VA 2024. Exact registration deadlines for those four were not checked against the program sites. In the analysis they only form a separate "mid" group.

### Cited findings — other evidence
- **Bloomfield, Lee, Philbrick and Slavov**, "How Do Firms Respond to State Retirement Plan Mandates?", NBER WP 31398, 2023 — [nber.org](https://www.nber.org/papers/w31398). As summarized by [Georgetown CRI](https://cri.georgetown.edu/do-state-facilitated-retirement-savings-programs-have-a-positive-impact-on-employers-offering-plans-and-worker-participation/):
  - With CPS data, workers in auto-IRA states are "3.2 percent more likely to work for an" employer offering a plan, with "a 7 percent increase in the probability of a worker participating in such a plan" (relative, not percentage-point, changes; not verified in the full paper here).
  - With Form 5500 data, the firm offer probability rises "1.5 – 1.7 percent."
- **Firm plan formation induced by mandates** (Bloomfield, Goodman, Rao, Slavov; CRI slides, Mar 2025), as the share of non-offering firms induced to offer: OR 20-99 employees (2018) 13.1%; IL 25-99 (2019) 12.8%; CA 50-99 (2021) 22.6%; CA 5-49 (2022) 16.0% — [CRI slides, p. 31](https://cri.georgetown.edu/wp-content/uploads/2025/03/3-27-25-States-and-Access_Webinar-Slide-Deck_Final-32725.pdf).
- **Rao, Dao and Lee**, CRI WP 2026-02 (SIPP 2014-2024, staggered DiD): mandates have "significant first order effects on account ownership" and reduce early retirement by 1.2 pp — [CRI](https://cri.georgetown.edu/wp-content/uploads/2026/06/CRI_WP_Rao_Dao_Lee_AutoIRA_final.pdf).

**Levels, private workers 21-64 at employers under 100 (% , replicate SE):**

| States | Measure | Pre (inc. 2012-16) | Rollout (2017-20) | Post (2021-25) |
|---|---|---|---|---|
| CA_only | offer | 22.8 (0.56) | 20.7 (0.51) | 18.9 (0.50) |
| CA_only | participation | 17.3 (0.51) | 15.6 (0.44) | 13.5 (0.42) |
| CA_only | takeup | 75.9 (1.00) | 75.4 (1.07) | 71.7 (1.10) |
| early | offer | 24.8 (0.46) | 22.2 (0.46) | 21.0 (0.44) |
| early | participation | 19.0 (0.42) | 16.8 (0.39) | 15.3 (0.37) |
| early | takeup | 76.8 (0.78) | 75.7 (0.87) | 72.8 (0.81) |
| early_OR_IL_only | offer | 29.8 (0.81) | 26.1 (0.90) | 26.2 (0.87) |
| early_OR_IL_only | participation | 23.4 (0.71) | 19.9 (0.81) | 19.6 (0.76) |
| early_OR_IL_only | takeup | 78.5 (1.33) | 76.2 (1.71) | 74.7 (1.36) |
| late | offer | 27.9 (0.54) | 25.2 (0.49) | 23.6 (0.56) |
| late | participation | 21.7 (0.46) | 19.7 (0.47) | 18.7 (0.54) |
| late | takeup | 77.8 (0.84) | 78.0 (0.99) | 79.1 (1.00) |
| mid | offer | 30.3 (0.60) | 26.6 (0.75) | 23.3 (0.83) |
| mid | participation | 22.6 (0.54) | 20.0 (0.66) | 17.9 (0.76) |
| mid | takeup | 74.4 (1.25) | 75.2 (1.44) | 76.9 (1.41) |
| none | offer | 26.6 (0.27) | 23.0 (0.24) | 21.7 (0.23) |
| none | participation | 19.9 (0.22) | 17.2 (0.23) | 16.0 (0.20) |
| none | takeup | 74.6 (0.45) | 75.1 (0.51) | 73.8 (0.52) |

Pooled n (persons) by wave and period: early 16,982 / 13,662 / 13,533; none 70,008 / 57,213 / 57,802; mid 7,615 / 4,625 / 4,761 (pre / rollout / post).

**Difference-in-differences vs "none" states (pp; SE from pooled replicate weights; Computed):**

| Treated group | Window vs pre | Measure | Change treated | Change other states | DiD (pp) | SE | z |
|---|---|---|---|---|---|---|---|
| early | rollout_2017_2020 | offer | -2.6 | -3.7 | +1.1 | 0.76 | +1.5 |
| early | rollout_2017_2020 | participation | -2.2 | -2.7 | +0.4 | 0.66 | +0.7 |
| early | rollout_2017_2020 | takeup | -1.1 | +0.5 | -1.6 | 1.39 | -1.1 |
| early | post_2021_2025 | offer | -3.8 | -4.9 | +1.1 | 0.75 | +1.5 |
| early | post_2021_2025 | participation | -3.8 | -3.9 | +0.1 | 0.68 | +0.2 |
| early | post_2021_2025 | takeup | -4.0 | -0.7 | -3.3 | 1.38 | -2.4 |
| early_OR_IL_only | rollout_2017_2020 | offer | -3.8 | -3.7 | -0.1 | 1.21 | -0.1 |
| early_OR_IL_only | rollout_2017_2020 | participation | -3.5 | -2.7 | -0.8 | 1.09 | -0.8 |
| early_OR_IL_only | rollout_2017_2020 | takeup | -2.2 | +0.5 | -2.7 | 2.33 | -1.1 |
| early_OR_IL_only | post_2021_2025 | offer | -3.7 | -4.9 | +1.3 | 1.29 | +1.0 |
| early_OR_IL_only | post_2021_2025 | participation | -3.7 | -3.9 | +0.1 | 1.12 | +0.1 |
| early_OR_IL_only | post_2021_2025 | takeup | -3.7 | -0.7 | -3.0 | 1.94 | -1.5 |
| CA_only | rollout_2017_2020 | offer | -2.1 | -3.7 | +1.6 | 0.90 | +1.8 |
| CA_only | rollout_2017_2020 | participation | -1.7 | -2.7 | +1.0 | 0.81 | +1.2 |
| CA_only | rollout_2017_2020 | takeup | -0.5 | +0.5 | -0.9 | 1.61 | -0.6 |
| CA_only | post_2021_2025 | offer | -3.9 | -4.9 | +1.0 | 0.86 | +1.2 |
| CA_only | post_2021_2025 | participation | -3.8 | -3.9 | +0.1 | 0.77 | +0.1 |
| CA_only | post_2021_2025 | takeup | -4.2 | -0.7 | -3.5 | 1.71 | -2.0 |
| mid | rollout_2017_2020 | offer | -3.8 | -3.7 | -0.1 | 0.91 | -0.1 |
| mid | rollout_2017_2020 | participation | -2.7 | -2.7 | +0.0 | 0.84 | +0.0 |
| mid | rollout_2017_2020 | takeup | +0.8 | +0.5 | +0.3 | 2.03 | +0.2 |
| mid | post_2021_2025 | offer | -7.1 | -4.9 | -2.1 | 1.12 | -1.9 |
| mid | post_2021_2025 | participation | -4.7 | -3.9 | -0.9 | 1.00 | -0.9 |
| mid | post_2021_2025 | takeup | +2.5 | -0.7 | +3.3 | 2.17 | +1.5 |

**Year-by-year gap, early wave (OR+IL+CA) minus "none" states, employers <100 (pp, SE):**

| Income yr | Offer gap (SE) | Participation gap (SE) | Take-up gap (SE) |
|---|---|---|---|
| 2012 | -1.9 (0.9) | -1.2 (0.8) | +1.0 (1.6) |
| 2013 | -3.0 (1.6) | -2.4 (1.5) | -0.4 (2.9) |
| 2014 | -1.7 (0.9) | -0.6 (0.8) | +2.4 (1.6) |
| 2015 | -1.2 (1.0) | -0.2 (1.0) | +2.7 (1.9) |
| 2016 | -1.6 (0.9) | +0.0 (0.8) | +5.4 (2.0) |
| 2017 | -1.8 (1.0) | -1.2 (0.9) | +0.4 (2.0) |
| 2018 | +1.3 (1.0) | +0.9 (0.9) | -0.4 (1.8) |
| 2019 | -2.7 (0.9) | -1.9 (0.9) | +1.0 (2.4) |
| 2020 | +0.2 (0.9) | +0.5 (0.8) | +1.5 (2.1) |
| 2021 | -0.4 (1.0) | +0.2 (0.9) | +2.0 (2.1) |
| 2022 | -0.5 (1.0) | -1.9 (0.9) | -7.2 (2.6) |
| 2023 | +0.2 (1.0) | -0.0 (0.9) | -0.7 (2.1) |
| 2024 | -1.0 (1.0) | -0.3 (0.8) | +1.9 (2.3) |
| 2025 | -1.9 (1.2) | -1.7 (1.0) | -1.4 (2.2) |


### Evidence verdict
- From the CPS: no evidence (a weak null) that state auto-IRA mandates raised reported offer or participation among small-employer workers.
- The CPS is a weak instrument here, for three reasons: the question framing; the post-2014 measurement drift (common to all states, so it differences out only if it is uniform); and small samples: about 2,700-3,400 small-employer workers a year across the three early states, about 1,000 a year in OR and IL combined.
- Administrative evidence (program accounts, and firm plan formation in Form 5500 and tax data) is the better guide. It shows real but modest coverage gains.

### Gaps
- Firm size in the CPS is employer-wide (all locations). Mandates key on in-state employee counts, and exempt employers that already offer a plan.
- Auto-IRA participation itself is not identified in the CPS. Starting with ASEC 2019, the retirement-account *income* items (RETCB_YN, DST_*) could be explored, but they measure distributions, not contributions.
- The pre period straddles the 2014 redesign (income year 2013 uses the 3/8 file). That is harmless only if the redesign affected all states equally. A pre period limited to 2014-2016 was not tested.

## 8. Caveats
- CPS PENPLAN/PENINCL refer to the longest job last year and include any employer plan (DB or DC), reported by the respondent or by a proxy.
- The levels after 2013 are biased down relative to administrative sources (Section 5). For trends, use 2000-2012 (traditional) and treat 2014-2025 as a separate, likely drifting series.
- The 2001-2004 SEs are approximate (design-effect method). All other SEs come from Census replicate weights.
- ASEC 2020-2021 had pandemic nonresponse. Census's entropy-balanced weights were not applied here; the cps/ thread found they change shares by ≤0.8 pp.
- Raw downloads and the person-level cache (about 0.7 GB with replicates) are in `/tmp/cpspart/` and not in the shared folder. The script re-creates them (`extract`), deleting each raw file after extraction.

## Chart-ready series
Private wage-and-salary workers aged 21-64, all employer sizes. Offer, participation and take-up are %; the participation SE is in pp. Computed from Census ASEC public-use files (source folder URL per row).

| Income year | ASEC file | Offer % | Participation % | Take-up % | SE (particip.) | Source |
|---|---|---|---|---|---|---|
| 2000 | 2001 prod | 59.6 | 46.9 | 78.7 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2001/march/ |
| 2001 | 2002 prod | 58.3 | 45.6 | 78.2 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2002/march/ |
| 2002 | 2003 prod | 56.0 | 43.8 | 78.2 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2003/march/ |
| 2003 | 2004 prod | 56.0 | 43.9 | 78.4 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2004/march/ |
| 2004 | 2005 prod | 55.8 | 43.9 | 78.6 | 0.26 | https://www2.census.gov/programs-surveys/cps/datasets/2005/march/ |
| 2005 | 2006 prod | 53.8 | 42.5 | 79.0 | 0.26 | https://www2.census.gov/programs-surveys/cps/datasets/2006/march/ |
| 2006 | 2007 prod | 52.0 | 41.3 | 79.4 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2007/march/ |
| 2007 | 2008 prod | 54.0 | 42.9 | 79.6 | 0.27 | https://www2.census.gov/programs-surveys/cps/datasets/2008/march/ |
| 2008 | 2009 prod | 52.1 | 41.4 | 79.4 | 0.22 | https://www2.census.gov/programs-surveys/cps/datasets/2009/march/ |
| 2009 | 2010 prod | 50.5 | 40.2 | 79.6 | 0.26 | https://www2.census.gov/programs-surveys/cps/datasets/2010/march/ |
| 2010 | 2011 prod | 50.3 | 40.4 | 80.3 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2011/march/ |
| 2011 | 2012 prod | 50.0 | 40.1 | 80.2 | 0.23 | https://www2.census.gov/programs-surveys/cps/datasets/2012/march/ |
| 2012 | 2013 prod | 49.7 | 40.0 | 80.4 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2013/march/ |
| 2013 | 2014 redesign 3/8 | 48.0 | 37.3 | 77.8 | 0.41 | https://www2.census.gov/programs-surveys/cps/datasets/2014/march/ |
| 2013 | 2014 trad 5/8 | 52.7 | 41.8 | 79.2 | 0.32 | https://www2.census.gov/programs-surveys/cps/datasets/2014/march/ |
| 2014 | 2015 prod | 46.0 | 35.5 | 77.2 | 0.24 | https://www2.census.gov/programs-surveys/cps/datasets/2015/march/ |
| 2015 | 2016 prod | 42.4 | 32.4 | 76.3 | 0.29 | https://www2.census.gov/programs-surveys/cps/datasets/2016/march/ |
| 2016 | 2017 prod | 40.4 | 31.1 | 77.0 | 0.24 | https://www2.census.gov/programs-surveys/cps/datasets/2017/march/ |
| 2016 | 2017 research (updated) | 40.5 | 31.3 | 77.3 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2017/march/ |
| 2017 | 2018 bridge (updated) | 41.2 | 31.7 | 77.0 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2018/march/ |
| 2017 | 2018 prod | 41.1 | 31.8 | 77.4 | 0.25 | https://www2.census.gov/programs-surveys/cps/datasets/2018/march/ |
| 2018 | 2019 prod | 40.1 | 31.2 | 77.6 | 0.29 | https://www2.census.gov/programs-surveys/cps/datasets/2019/march/ |
| 2019 | 2020 prod | 39.5 | 31.4 | 79.4 | 0.24 | https://www2.census.gov/programs-surveys/cps/datasets/2020/march/ |
| 2020 | 2021 prod | 38.8 | 30.6 | 78.9 | 0.30 | https://www2.census.gov/programs-surveys/cps/datasets/2021/march/ |
| 2021 | 2022 prod | 37.8 | 30.0 | 79.2 | 0.29 | https://www2.census.gov/programs-surveys/cps/datasets/2022/march/ |
| 2022 | 2023 prod | 37.8 | 29.5 | 78.1 | 0.29 | https://www2.census.gov/programs-surveys/cps/datasets/2023/march/ |
| 2023 | 2024 prod | 37.9 | 29.6 | 78.0 | 0.31 | https://www2.census.gov/programs-surveys/cps/datasets/2024/march/ |
| 2024 | 2025 prod | 36.1 | 28.1 | 77.8 | 0.27 | https://www2.census.gov/programs-surveys/cps/datasets/2025/march/ |
| 2025 | 2026 prod | 35.9 | 28.4 | 79.0 | 0.28 | https://www2.census.gov/programs-surveys/cps/datasets/2026/march/ |
