# Contributions to employer DC (and DB) plans: administrative and aggregate series

Built 2026-10-06. All scripts in `scripts/`, run from `contributions/admin/` with `python3 -I`. Order:
`fetch_bls.py` (network) → `parse_bls.py`, `build_bea.py`, `build_dol.py`, `build_recordkeeper.py`.

## Headline findings

**DOL Form 5500 (private plans; excludes one-participant plans)**
- DC plans' share of all private pension contributions rose from **34.6% in 1975** to 55.9% (1985), 76.7% (1990), 85.6% (2000) and **90.7% in 2023**. (Table E13)
- Total DC contributions (employer + employee + rollovers + noncash) rose from **2.0% of private wages and salaries in 1975** to 3.4% (1990), 4.9% (2000) and **7.7% (2023)**. DB contributions fell from 3.8% (1975) to 1.0% (1990), rose to 2.8% in 2003 (post-2001 funding catch-up), and were down to **0.8% in 2023**.
- If you drop rollovers and count only employer + participant cash contributions, DC contributions rose from **4.6% of private wages in 1999 to 6.9% in 2023** (Abstract Table A4). Almost all of that rise came from employees:
  - Participant (employee) contributions went from **2.76% to 4.34%** of private wages.
  - Employer contributions went from **1.83% to 2.58%**.
- **Employees pay about 60% of DC contributions (excluding rollovers), and the share is creeping up.** It sat at 59–61% from 1999 to 2017, then rose to 61.8% in 2019, 63.1% in 2021 and **62.7% in 2023**. Measured against all DC contributions, the employer share fell from 36.6% (1999) to 33.6% (2023).
  - In 401(k)-type plans the employee share is higher, at **70.3% in 1999, 63.7% in 2008 and 65.0% in 2023** (Abstract Table D8/D7).
- **Rollovers ("contributions from others") have grown.** They were 4.9–7.6% of DC contributions from 1999 to 2012, then 8.9% (2014), 10.6% (2019) and a peak of 12.2% (2021), and **9.7% in 2023**.
- **DC contributions (employer + participant) per active DC participant:** $3,387 (1999) and **$7,173 (2023)** in nominal terms. In 2024 dollars that is $6,378 → $7,385. The real series is flat-to-down across 1999–2012 (about $5,700–6,800), partly because of the definition breaks below, and rises after 2013.
  - Per active 401(k) participant: **$7,682 in 2024 dollars in 2023**, against $6,794 in 1999.
  - The E13 total (including rollovers) per active participant runs $6,661 (1975) → $5,147 (1990) → $7,109 (2000) → **$8,200 (2023)** in 2024 dollars.

**BEA NIPA (employer contributions only; all private employers, not only Form 5500 filers)**
- **Private employers' pension contributions (DB + DC)** were **1.4% of private wages in 1950**, 2.5% (1970), 3.3% (1980) and a peak of 4.3% (1993). They have stayed at about **3.5% since 2020 (3.47% in 2025)**. Total employer pension effort has not risen; its mix has flipped from DB to DC.
- **Private DC employer contributions** were **1.30% of private wages in 1984**, 1.95% (1990), 1.94% (2000), 2.44% (2015) and **2.70% (2025)**.
- **Private DB employer contributions (actual cash)** were 2.86% (1984), 0.94% (1990), 0.80% (2000), 1.93% (2008), 1.61% (2015) and **0.71% (2025)**.
- **DC's share of private employers' actual pension contributions** was **31% in 1984**, 67% (1990), 71% (2000), 55% (2008, a DB funding spike) and **79% (2025)**.
- **DC employee ("household") contributions, all sectors** (private plus TSP plus state and local DC) rose from 1.55% of total wages (1984) to **5.04% (2025)**. Employer DC contributions, all sectors, rose from 1.11% to 2.58% over the same period. The employee share of DC contributions in NIPA was 58% (1984) and **66% (2025)**.
- **State and local government:** DB actual employer contributions rose from **6.8% of S&L wages (2000) to a peak near 16% (2019), and were 14.8% in 2025**. S&L DC employer contributions were **1.5%** (2025).

**BLS ECEC (employer cost; March reference; NAICS series start 2004)**
- **Private industry, DC:** **1.8% of total compensation in 2004**, rising to **2.5% in 2024–2026**. In dollars per hour worked: **$0.43 (2004) → $1.10 (2024) → $1.16 (March 2026)**. That equals **2.6% → 3.6% of wages and salaries**.
- **Private industry, DB:** 1.6% of total compensation (2004) → **0.9% (2025–26)**, or $0.37 → $0.40 per hour.
- **DC's share of private retirement-and-savings cost:** **54% (2004) → 74% (2026)**.
- **State and local government:** DC is 0.7–0.9% of compensation ($0.25 → $0.60 per hour). DB rose from 5.3% to **12.4%** ($1.83 → $8.22 per hour), and DC is only about 7% of S&L retirement cost.

**Recordkeeper/industry context (not administrative data)**
- **Vanguard How America Saves**, participants only:
  - Average employee deferral rate: **6.9% (2015)**, 6.8–7.1% (2016–19), 7.3–7.4% (2020–22), 7.7% (2023), **7.6% (2024 and 2025 estimated)**.
  - Median deferral rate: 6.0% (2015–19) → **6.6–6.8% (2023–25)**.
  - Total (employee + employer) contribution rate, average: **10.8% (2015) → 12.1% (2024, 2025 estimated)**. Median: 10.0% → 11.6%.
  - Including eligible non-participants at 0%, the average total rate was 10.1% (2024).
  - Participant-weighted participation: 71% (2016) → 83% (2025 estimated).
- **Federal TSP (FERS participants):**
  - Average deferral rate: 8.5% (2012), 8.1% (2014), 7.9% (2017–19), then up after the default rose from 3% to 5% in October 2020: 8.4% (2021) → **9.3% (2025)**. FRTIB says it was about 9.5% in the mid-2000s, before auto-enrollment.
  - Participation: 88.6% (2012) → **96.2% (2025)**.
- **Fidelity, Q2 2026:** employee rate 9.6%, employer 4.8%, total 14.4% (single data point from a press release).

## Definitions
- **Form 5500 "contributions"** (E13, E19, A4) are employer + participant + "contributions from others (including rollovers)" + noncash. "Employer + participant" excludes rollovers and noncash; noncash is about 0.2–0.5% and is mostly employer stock.
- **Participant share** = participant / (employer + participant), from the A4 DC column.
- **Per active participant** = contributions / active participants, taken from Historical Table E7 (all DC) or E19 (401(k)-type).
- **Real values** use the CPI-U (CUUR0000SA0) annual average, expressed in 2024 dollars. The 2025 CPI average would be built from 11 months, because October 2025 was not collected, so 2025 is not used as the base.
- **% of private wages** uses BEA NIPA Table 2.1 line 4, wages and salaries of private industries (A132RC).
  - This is an economy-wide denominator, not the wages of covered workers. The ratio therefore measures aggregate contribution effort, not individual contribution rates.
- **NIPA "actual employer contributions"** (W350RC DB, Y934RC = W351RC DC) are cash contributions. W350RC equals Form 5500 DB employer contributions exactly (for example, $73,748m in 2023).
  - NIPA "imputed" DB contributions (Y240RC) make DB contributions accrual-based (normal cost) since the 2013 comprehensive revision.
  - B4921C (1948–) = DC + DB actual + DB imputed, so the pre-1984 total is on an accrual-consistent basis, not cash.
- **ECEC** = employer cost per hour worked, and percent of total compensation, for civilian (1), private (2) and state-and-local (3) workers. Component codes: 180 retirement and savings, 190 DB, 200 DC.
  - The annual file gives both March (Q1) values and 4-quarter means.
- **Vanguard deferral rate** = employee-elective deferral as % of pay among participants. "Total contribution rate" adds employer contributions.
- **TSP deferral rate** = annualized employee contributions / estimated salary (FRTIB's approximation). It excludes the agency 1% automatic contribution and the match.

## Method breaks and caveats
1. **Active participant definition widened in 2005.** Eligible non-contributors are counted from 2005; E7's 2004r row raises 2004 DC actives from 52.2m to 61.3m. As a result, contributions per active participant drop about 9% in 2005 for definitional reasons, not behavioral ones. Do not compare across 2004/2005 without adjusting.
2. **2009–2013: all 5500-SF participants were counted as active.** This inflates actives and lowers per-active figures. From 2014, 5500-SF reports actives separately.
3. **Rollovers sit inside "contributions from others"** and inflate E13/E19 DC totals by 5–12%. Use the A4 employer + participant series for saving effort. Rollovers in are partly offset by rollovers out, which appear in benefits.
4. **Vintages:** Abstract A4 DC totals match the historical E13 to within 0.1% in every year 1999–2023, and D8/D7 match E19, so the abstract splits are consistent with the historical totals. The 1999 abstract covers plan years *beginning* in 1999; later abstracts cover plan years *ending* in the year. No 401(k) income statement exists for 2000–2001.
5. **E13 and E19 exclude one-participant plans.** Multiple-employer plans are split out from 2017, but the "Total" columns are unaffected. DB/DC classification was revised in the 2015 release (Appendix).
6. **NIPA DC/DB detail exists only from 1984** (Tables 7.22/7.25); Table 6.11D starts in 1998. The 1948–1983 split (Tables 6.11A–C) is not in the NipaDataA flat file, and the BEA XLSX archive returned an error page. NIPA DC household contributions (Y344RC) include TSP and S&L DC employee contributions, so they are **not** comparable with Form 5500 participant contributions ($581bn vs $434bn in 2023).
7. **ECEC private DB cost** reflects employer cash contributions per hour, which are volatile with funding rules. ECEC percentages are published to one decimal.
8. **Recordkeeper data** describe each firm's own client base, which changes over time; Vanguard notes a 2016 client-mix shift. TSP report methods changed across editions, and 2012/2014 values come from separate reports.

## Files
- `output/dol_e13_contributions_by_type.csv`: 1975–2023 total/DB/DC contributions (E13), actives (E7), 401(k) (E19), % of private wages, per active (nominal and real).
- `output/dol_dc_contrib_by_source.csv`: 1999–2023 DC employer/participant/others/noncash (A4), shares, % of wages, per active, cross-check against E13.
- `output/dol_a4_contrib_by_source_all_types.csv`: the A4 split for total, DB and DC.
- `output/dol_401k_contrib_by_source.csv`: 401(k)-type plans by source (D8/D7), 1999 and 2002–2023.
- `output/bea_nipa_pension_contrib.csv` (wide) and `bea_nipa_pension_contrib_long.csv`: NIPA series, 1948–2025.
- `output/bls_ecec_retirement_quarterly.csv` and `bls_ecec_retirement_annual.csv`: ECEC DC/DB/retirement cost, 2004Q1–2026Q2.
- `output/recordkeeper_contribution_rates.csv`: Vanguard, TSP and Fidelity (labelled as industry context).
- `raw/`: BEA flat files, BLS series pages and Vanguard PDFs (untrusted downloads). The DOL and TSP inputs are read in place from `dc_stay/raw/` and `dc_policy/raw/autoenroll/`.

## Sources and access
- **DOL EBSA:** Private Pension Plan Bulletin Historical Tables 1975–2023 and Abstracts 1999–2023 (files on disk; dol.gov is 403 from here). https://www.dol.gov/agencies/ebsa/researchers/statistics/retirement-bulletins
- **BEA:** https://apps.bea.gov/national/Release/TXT/NipaDataA.txt and SeriesRegister.txt (reachable). The XLSX section files return an error page, and FRED timed out.
- **BLS:** download.bls.gov/pub/time.series/cm/ and nb/ returned 403 (BLS_CONTACT_EMAIL was not set), and api.bls.gov reported its daily threshold reached. The series pages at https://data.bls.gov/timeseries/<id> were reachable and were used.
- **CPI-U:** https://data.bls.gov/timeseries/CUUR0000SA0
- **Vanguard:**
  - HAS 2025: https://corporate.vanguard.com/content/dam/corp/research/pdf/how_america_saves_report_2025.pdf
  - HAS 2026: https://workplace.vanguard.com/content/dam/inst/iig-transformation/has/2026/pdf/HowAmericaSaves2026.pdf
  - Earlier editions (pressroom.vanguard.com) were not retrievable.
- **FRTIB:** participant behavior reports (on disk).
- **Fidelity:** https://about.fidelity.com/data-and-insights/q2-2026-retirement-analysis
- **Blocked:** ICI (403), tsp.gov (403), www.bls.gov (403), FRED (timeout).

## Unresolved
- **BLS NCS employer-match provisions** (share of DC/savings-and-thrift plans with a match, match formulas): the nb series list could not be retrieved (download.bls.gov 403; Data Finder and PDQ blocked by bot challenge), so no match series were built.
- **Vanguard HAS before 2015** and the ICI/EBRI 401(k) database were not retrieved.
- **NIPA 1948–1983 DC/DB split** was not retrieved.
