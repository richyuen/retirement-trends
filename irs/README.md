# IRS SOI IRA tables: rollover check, Form 1040 comparison, TY2024 status, revisions

Checked 4 October 2026, with irs.gov reachable. Everything here is in `irs/`. Nothing in `report/`, `output/`, `data/`, `scripts/` or `CLAUDE.md` was changed.

Re-run: `bash irs/scripts/fetch.sh` (downloads the files), then `python irs/scripts/analyze.py` (writes `irs/output/`).

## Sources

| What | URL | File(s) | Where kept |
|---|---|---|---|
| SOI IRA landing page (last reviewed 12 Jun 2026) | https://www.irs.gov/statistics/soi-tax-stats-accumulation-and-distribution-of-individual-retirement-arrangements | snapshot | `raw/irs_pages/soi-ira-landing_2026-10-04.html` |
| SOI "What's new" page (last reviewed 29 Sep 2026) | https://www.irs.gov/statistics/soi-tax-stats-whats-new | snapshot | `raw/irs_pages/soi-whats-new_2026-10-04.html` |
| SOI IRA Table 1 (by type of plan), TY2001, 2004–2023 | https://www.irs.gov/pub/irs-soi/YYin01ira.xls[x] | e.g. `22in01ira.xlsx` | `raw/irs_soi/` |
| SOI IRA Table 4 (by age), TY2001, 2004–2023 | https://www.irs.gov/pub/irs-soi/YYin04ira.xls[x] | e.g. `22in04ira.xlsx` | `raw/irs_soi/` |
| SOI 95% confidence intervals, TY2022–2023, Tables 1 and 4 | https://www.irs.gov/pub/irs-soi/22in01iraci.xlsx (and so on) | `22in01iraci.xlsx`, `22in04iraci.xlsx`, `23in01iraci.xlsx`, `23in04iraci.xlsx` | `raw/irs_soi/` |
| SOI Tables 5 and 6 (contributions), TY2022; Table 5, TY2021 | https://www.irs.gov/pub/irs-soi/22in05ira.xlsx, `22in06ira.xlsx`, `21in05ira.xlsx` | same | `raw/irs_soi/` |
| Publication 4801, Form 1040 line-item estimates, TY2019–2023 | https://www.irs.gov/pub/irs-prior/p4801--2021.pdf (TY2019), `p4801--2022.pdf` (TY2020), `p4801--2024.pdf` (TY2021), `p4801--122024.pdf` (TY2022, Rev. 12-2024), https://www.irs.gov/pub/irs-pdf/p4801.pdf (TY2023, Rev. 6-2026) | 2.5–5.1 MB each | scratch only (too large). SHA-256 prefixes: 51d17d5c8c755242, 790b2a3cbc652489, 8032f3bbffb0017a, 32f1cef6de0e9469, 49686f6c909452bc |
| ICI, *The US Retirement Market, Second Quarter 2026*, data file (posted 17 Sep 2026) | https://www.ici.org/statistical-report/ret_26_q2_data.xls | Tables 10–12 | `raw/ici/ret_26_q2_data.xls` |
| ICI Research Perspective 32(7), *The Role of IRAs in US Households' Saving for Retirement, 2025* (June 2026) | https://www.ici.org/system/files/2026-06/per32-07.pdf | p.4 and note 21 | `raw/ici/per32-07.pdf` |
| ICI IRA Investor Database data file, Figure A.26 (older vintage, from an earlier session) | https://www.ici.org/files/2026/tax-year-2023-rpt-ira-traditional-data.xlxs | `data/recovered_irs/js_386.txt` | read-only |

`raw/irs_soi_manifest.csv` lists every IRS file with its URL, size, SHA-256 prefix and HTTP `Last-Modified` date. The ICI site returns 403 (Akamai) to curl from this machine, so the two ICI files were fetched with WebFetch. The Wayback Machine could not be reached (the connection was reset), so the February 2025 TY2022 IRS file could not be retrieved.

## 1. Rollover flag (ICI $669.8bn vs IRS $635.9bn / $664.3bn): resolved

**Verdict: the two numbers come from different releases of the same IRS SOI TY2022 Table 1, traditional-IRA row. Neither is an error. $669.8bn is the traditional-IRA rollover figure from SOI's first TY2022 release (February 2025, former methodology). $635.9bn is the same cell after SOI re-released TY2022 under a revised methodology on 4 June 2026. The near-match with the all-types total ($664.3bn) is a coincidence. Use $635.9bn for traditional IRAs and $664.3bn for all IRA types. ICI's own current data now uses $635.9bn.**

Evidence (all in `output/rollover_2022_flag_reconciliation.csv` and `output/traditional_ira_2022_vintage_comparison.csv`):

1. **SOI re-released TY2022.** The What's-new entry for June 2026 reads: "Data on Individual Retirement Arrangements (IRAs) for tax years 2022 and 2023 using a revised methodology are now available ... Although estimates for tax year 2022 were also previously released under the former methodology, tax year 2023 and later years will be released using only the new methodology." The matched sample now also uses Forms W-2. The February 2025 entry announces the first TY2022 release. The landing page adds: "Beginning with data for 2022, SOI introduced enhancements to improve the data's overall quality as a new series of information." The source line in `22in01ira.xlsx` (A17) is dated "June 2026", and every `22in*` file has HTTP Last-Modified 4 Jun 2026.
2. **ICI's figure predates the re-release.** The ICI paper and its news release are dated 3 June 2026, one day before the IRS re-release. The text says "$670 billion ... to traditional IRAs in 2022", and note 21 says "See Internal Revenue Service, Statistics of Income Division 2025", meaning the 2025 web release. ICI's Figure A.26 (js_386), which shows 669.8, has no 2023 flow data, which is consistent with a file built before June 2026.
3. **ICI matches IRS exactly in years without a re-release.** ICI 2020 = 594.8 and 2021 = 706.0. These equal the traditional-row rollover cells G7 in `20in01ira.xlsx` (594,816,630K) and `21in01ira.xlsx` (706,016,725K). The 2021 traditional withdrawals (437,994,952K) and year-end FMV (12,144,857,233K) also match ICI exactly.
4. **ICI now shows the new figure.** ICI's Q2 2026 data file (17 Sep 2026), Table 11 row 2022, reads: contributions 25.8 | rollovers **635.9** | conversions 36.5 | withdrawals 480.3 | assets 10,783.9. These are identical to `22in01ira.xlsx` C7, G7, I8, K7 and M7. The row for 2023 (652.8) equals `23in01ira.xlsx` G7.
5. **The whole TY2022 traditional row changed between releases**, not just rollovers:

   | Traditional IRA, 2022, $bn | ICI Fig. A.26 (Feb-2025 SOI vintage) | IRS June 2026 (`22in01ira.xlsx`) | Change |
   |---|---|---|---|
   | Contributions | 22.5 | 25.8 (C7) | +14.7% |
   | Rollovers | 669.8 | 635.9 (G7) | −5.1% |
   | Roth conversions | 36.5 | 36.5 (I8, Roth row) | 0 |
   | Withdrawals | 467.0 | 480.3 (K7) | +2.8% |
   | Year-end FMV | 10,781.2 | 10,783.9 (M7) | 0.0% |

   A third source confirms the contributions change. CRS R48051 (Dec 2025) quotes the earlier TY2022 Table 5: 4,989,322 traditional contributors averaging $4,510, which is $22.5bn and matches ICI's 22.5. The current `22in05ira.xlsx` B7:C7 shows 5,900,726 contributors and $25,807,585K. For Roth, CRS has 10,036,960 contributors; current `22in06ira.xlsx` B7 has 9,170,792.
6. **Sampling error does not explain the gap.** In the June 2026 file the 95% CI for traditional rollovers (`22in01iraci.xlsx` G7) is $608.2–663.1bn, and 669.8 lies outside it. The all-types interval (G6) is $635.9–691.9bn.
7. **Other explanations ruled out.** Recharacterizations and SEP/SIMPLE/Roth rollovers do not explain it. ICI's series has always been the traditional row, not the Total row: SEP + SIMPLE + Roth rollovers in 2022 were 6.0 + 0.5 + 22.0 = $28.4bn, and 664.3 − 635.9 = 28.4.

**Implication for the project (new caveat): TY2022–2023 are a new SOI series.** The "consistent era 2012–2023" therefore has a methodology break between 2021 and 2022. Age-level traditional and total figures move little: 70–74 incidence is 69.0 in 2021 and 69.1 in 2022. The break is large in the small plan types:

| Withdrawals by plan type | 2021 | 2022 |
|---|---|---|
| Roth | $5.7bn, 0.96m people | $23.8bn, 2.19m people |
| SEP | $26.4bn | $6.7bn |
| SIMPLE | $0.1bn | $1.9bn |

The new SEP/SIMPLE footnote says these "allocate any distributions from Form 1040, schedule 1, line 16, which may include other account types". The February 2025 TY2022 numbers for all-IRA totals and by age could not be retrieved, so the size of the break in Table 4 cannot be measured.

## 2. Form 1040 gross IRA distributions vs SOI IRA-study withdrawals, 2019–2023

**TY2022 Form 1040 line 4a (gross IRA distributions): 17,355,700 returns, $497,467,733K.** Source: Publication 4801 Rev. 12-2024 (`p4801--122024.pdf`), PDF page 15 (returns) and page 16 (amounts), "Total of all returns filed = 161,336,659". SOI Table 1.4 (`22in14ar.xls`) has only the taxable amount (column 45, "Taxable IRA distributions"), so it cannot supply the gross figure. Line 4b taxable is $437,775,580K, which matches Pub 1304 Table A.

| Tax year | Form 1040 line 4a, $K (Pub 4801, p.16) | SOI IRA withdrawals, all types, $K (Table 1, total row, col. 10) | Gap | SOI withdrawals + Roth conversions vs 4a |
|---|---|---|---|---|
| 2019 | 379,260,994 (p4801--2021.pdf) | 375,946,058 (`19in01ira.xlsx` K5) | −0.87% | +3.6% |
| 2020 | 353,034,392 (p4801--2022.pdf) | 345,315,493 (`20in01ira.xlsx` K6) | −2.19% | +7.6% |
| 2021 | 473,451,893 (p4801--2024.pdf) | 470,171,905 (`21in01ira.xlsx` K6) | −0.69% | +8.0% |
| **2022** | **497,467,733** (p4801--122024.pdf) | 512,641,060 (`22in01ira.xlsx` K6, new methodology) | **+3.05%** | +10.4% |
| 2023 | 505,480,278 (p4801.pdf) | 515,221,523 (`23in01ira.xlsx` K6, new methodology) | +1.93% | +9.2% |

The returns counts are on page 15 of each PDF; `analyze.py` re-located every value in the PDFs. The full table, with conversions and cell references, is `output/form1040_vs_soi_ira_withdrawals_2019_2023.csv`.

- The 2019–2021 and 2023 gaps reproduce the existing −0.9 / −2.2 / −0.7 / +1.9%. **2022 is +3.1%**, so "within about 2%" holds only for 2019–2021 and 2023. In both new-methodology years SOI's withdrawals are above line 4a; in all three old-methodology years they are below it.
- A rough check, not a measurement: the traditional-row withdrawals in the February 2025 vintage were about $13.3bn lower (467.0 vs 480.3). If the all-types total moved by the same amount, the old-vintage 2022 gap would have been about +0.4%.
- On verification item 4 (are conversions inside SOI "withdrawals"?): line 4a includes Roth conversions, and also indirect rollovers and QCDs. Adding SOI's separately reported conversions to its withdrawals overshoots line 4a by 3.6–10.4%; without them the two totals agree within 1–3%. Taken alone this cannot settle the question, because the two concepts differ on several items: indirect rollovers, QCDs, Roth distributions, and coverage of the matched sample. It is consistent with the IRS footnote ("Roth IRA conversions are shown separately"). It does not support the claim that conversions are counted in SOI withdrawals.
- Do not compare SOI's count of withdrawers (persons) with line-4a returns (joint returns count once).
- The TY2023 Pub 4801 confidence-interval table (PDF page 10) shows "Taxable IRA distributions 437,775,580". This is the TY2022 value, carried over unchanged from the TY2022 publication (same table, page 10). It confirms the stale-page caveat in `notes/rmd_policy_tax_data.md`. Use page 16 (line 4b = 438,147,938K).

## 3. TY2024 IRA tables: not released

- The landing page (reviewed 12 Jun 2026) lists only tax years up to 2023.
- `24in01ira.xlsx`, `24in04ira.xlsx` and `24in01ira.xls` return HTTP 404.
- What's new (reviewed 29 Sep 2026) announces nothing for TY2024. Its "Upcoming data releases" list, which runs to 27 Oct 2026, has no IRA item.

No TY2024 incidence or rate can be computed yet. Recorded in `output/ty2024_status.json`. Given the release history (TY2021 in Feb 2025, TY2022–23 in Jun 2026), TY2024 is unlikely before 2027.

Instead, `output/irs_soi_ira_2004_2023_current.json` re-parses Tables 1 and 4 for 2004–2023 from the current files. It uses the same keys as `data/irs_derived.json`: `age`, `inc`, `rate_prior`, `rate_same`, `t1`. Each age group also gets `rn`/`ra` (rollover taxpayers and $K) and `cn`/`ca` (Roth conversions), so the build script can take TY2024 in the same format once it appears. The file also records which table file each year came from and the vintage line of each Table 1.

## 4. Revisions to the recovered data

**None found.** Every cell was compared, not a sample:

- **`js_559` (Table 4 by age, 2004–2023):** all 720 cells (20 years × 9 groups × withdrawers / withdrawals / holders / FMV) equal the current IRS files. Maximum difference 0. Details: `output/revisions_js559_table4_vs_current.csv`, with cell addresses.
- **`js_563` (Table 1 by type):** all 240 cells are identical. Details: `output/revisions_js563_table1_vs_current.csv`.

So `data/irs_derived.json` reflects the current IRS files, and the 2022–2023 values in it are already the June 2026 (new-methodology) vintage.

Other revision notices on What's new, none of which touch Tables 1 or 4:
- Apr 2026: Tables 5 and 8 for 2020–2022, traditional contributions (SECURE Act age change).
- Jun 2026: Table 8 for 2017–2021 (disclosure protection).

Table 1/4 Last-Modified dates for TY2021 and earlier are unchanged (TY2021: 20 Feb 2025).

Minor: the landing page's TY2022 Table 8 link (`/system/files/irs-soi/22in08ira.xlsx`) is broken, and `/pub/irs-soi/22in08ira.xlsx` also returns 404. Only `22in08iraci.xlsx` downloads.

## Files

- `README.md`: this file
- `scripts/fetch.sh`: downloads the sources
- `scripts/analyze.py`: all parsing and calculations
- `output/rollover_2022_flag_reconciliation.csv`: every rollover figure with its file and cell
- `output/traditional_ira_2022_vintage_comparison.csv`: ICI old vintage vs IRS June 2026, five flow items
- `output/form1040_vs_soi_ira_withdrawals_2019_2023.csv`: the Form 1040 comparison
- `output/irs_soi_ira_2004_2023_current.json`: current Tables 1 and 4 in the `irs_derived.json` structure, plus rollovers and conversions
- `output/revisions_js559_table4_vs_current.csv`, `output/revisions_js563_table1_vs_current.csv`: cell-by-cell revision checks
- `output/ty2024_status.json`, `output/summary.json`
- `raw/irs_soi/` (49 IRS spreadsheets, each under 60 KB), `raw/irs_soi_manifest.csv`, `raw/ici/` (ICI Q2-2026 data .xls, 1.1 MB; ICI per32-07.pdf, 0.98 MB), `raw/irs_pages/` (page snapshots)
