# Retirement contributions in IRS tax data: IRAs, W-2 elective deferrals, Form 1040 deductions

Built 6 October 2026, with irs.gov reachable. Everything is in `contributions/irs/`. Nothing outside this folder was changed. The `dc_policy` participation CSV was only read.

To rebuild: run `bash scripts/fetch.sh` (downloads into `raw/`), then `bash scripts/run_all.sh`. The second script runs `limits.py`, `f1040_long.py`, `ira_contributions.py`, `w2_deferrals.py` and `combined.py`, in that order. All of them run under `python3 -I`, and each prints a summary. `raw/manifest.csv` lists every downloaded file with its URL, size and SHA-256 prefix. It also lists the archive PDFs, which were not kept.

## Findings (numbers first)

### IRA contributions (SOI IRA Table 1 and the by-age table; TY2000-2002 and 2004-2023; TY2003 was never published)

- **All IRA types:** 15.1m taxpayers contributed in 2000, which is **8.4% of all taxpayers**. That fell to 11.3m (**5.7%**) in 2011, then recovered to 17.7m (**8.2%**) in 2021-2023.
  - Dollars rose from $36.5bn (2000) to $91.0bn (2021) and $89.1bn (2023).
  - The average contribution rose from $2,412 to $5,034.
  - Measured against IRA balances, contributions fell from **1.39% of year-end FMV (2000) to 0.61% (2023)**, because balances grew much faster than contributions.
  - As a share of Form 1040 wages, contributions held at 0.8-1.0% throughout (0.82% in 2000, 1.01% in 2021, 0.87% in 2023).
  - The share of IRA owners contributing fell from 32.7% (2000) to 20.7% (2011) and was 24.9% in 2023.
- **By IRA type, % of all taxpayers:**
  - **Roth:** 3.8% (2000), 2.9% (2011), **4.7% (2021)**, 4.4% (2023).
  - **Traditional:** 3.2%, 1.7%, 2.4% and **2.7%** in the same years.
  - **SEP:** fell from 1.0% to 0.5%.
  - **SIMPLE:** about 1.0% throughout.
  - Roth contributors (9.5m in 2023) have outnumbered traditional contributors (5.9m) every year since 2000.
  - The 2020-2021 jump is mostly Roth: 7.9m contributors in 2019, 10.2m in 2021.
  - Average Roth contribution in 2023 was $3,458; average traditional was $4,581.
  - Share of owners contributing in 2023: SIMPLE 62%, Roth 32%, SEP 31%, traditional 11%. Traditional is low because most traditional balances come from rollovers.
- **By age, % of all taxpayers contributing to any IRA (harmonised groups):**
  - Contribution rates peak at **55-59** and drop sharply after 65.
  - 55-59: 14.0% (2000), 9.1% (2011), 10.6% (2023).
  - 25-34: 8.0%, 5.3% and **9.5%** in the same years. Under 25: 3.7%, 1.7% and 6.0%.
  - Since about 2019 the young groups have caught up, so the age profile is now flat from 25 to 64 at roughly 9.5-10.6%.
  - 70+ rose from about 0.9% to 2.2% after the SECURE Act removed the age-70½ bar on traditional contributions (from TY2020).
  - By type and age (Table 8, 2023), the share of Roth owners contributing falls with age: 74% at 20-24, 30% at 50-54, 5% at 70+.
- **Contributing exactly the limit** (Tables 5/6; exactly the regular limit or the limit plus catch-up):
  - About **45-55% of traditional contributors** and **30-40% of Roth contributors** contribute exactly the limit.
  - The share dips in the year a limit rises: 2005, 2008, 2013, 2019 and 2023. For example, traditional was 52.4% in 2022 and 45.2% in 2023, when the limit went from $6,000 to $6,500.

### Form 1040 deductions, long series (1975-2023; gaps in 1976-79 and 1981-82; returns, not persons)

- **IRA deduction, share of returns claiming it:**
  - 1.5% in 1975 and 2.7% in 1980.
  - The 1982 universal IRA (ERTA) took it to **15.9% in 1985** (16.2m returns, $38.2bn, **1.66% of AGI**).
  - The Tax Reform Act of 1986 income limits cut it to 6.8% in 1987.
  - 4.1% (1991), 2.9% (1999), 1.8% (2010), **1.56% in 2023** (2.5m returns, $13.8bn, 0.09% of AGI).
  - The amount has been flat at $11-14bn since 2005, even though limits have risen.
- **Self-employed SEP/SIMPLE/qualified-plan ("Keogh") deduction:**
  - $1.6bn (1975), $6.2bn (1986), $11.9bn (1999), **$30.1bn (2023)**.
  - Steady at about **0.20-0.29% of AGI** since 1985. It has exceeded the IRA deduction every year since 1995.
- **Saver's credit (Form 8880):** 5.3m returns in 2002 (4.1% of returns), 9.8m in 2023 (**6.1%**). Total $2.04bn in 2023; the average was $207, which has barely moved since 2002 ($199).

### Employer DC elective deferrals (SOI Form W-2 statistics; TY2008-2020; nothing later is posted)

- **Share of wage earners deferring** (the existing `dc_policy` series, reproduced exactly): 34.7% (2008), 33.5% (2010), **42.8% (2020)**.
- **Total deferrals:** $219bn (2008) to **$379bn (2020)**. The average per deferrer rose from $4,484 to $6,058.
- **Deferral rate among deferrers (% of Medicare wages):** flat at **6.3-6.7%** throughout (6.49% in 2008, 6.74% in 2020). Growth in dollars came from more people deferring and from wage growth, not from higher rates.
- **Deferrals as a share of all W-2 gross pay** (box-1 wages plus pre-tax deferrals): **3.70% (2008) to 4.58% (2020)**.
- **Roth deferrals** (codes AA/BB/EE) were **1.0% of deferral dollars in 2008 and 9.6% in 2020**.
- **Deferrers at the 402(g) maximum:** about **8% overall** (7.8-9.3%). The share is 14-16% at ages 60-64.
- **By age in 2020:**
  - Share deferring: under 26, 20.8%; 26-34, 44.4%; 45-59, 51-52%; 65-74, 34.9%.
  - Deferral rate: from 5.5% (under 26) up to 8.0-8.3% (60-74).
- **By wage size in 2020:**
  - Share deferring rises from 16% ($10-15k) to 78% ($100-200k) and 84-87% above $200k.
  - Deferral rate peaks at 8.6% for $100-200k, then falls at higher wages because of the dollar cap (0.1% at $10m+).
- **By plan code in 2020:** 401(k) (code D) accounts for 73% of dollars, 403(b) 10%, 457(b) 5%, Roth 401(k) 8.5%.

### Combined tax-data view (TY2008-2020)

- Traditional and Roth IRA contributions plus all W-2 elective deferrals came to **4.24% of gross wages in 2008 and 5.25% in 2020**. The broader measure, which adds SEP and SIMPLE IRA contributions net of W-2 codes F and S, went from 4.55% to 5.50%.
- IRAs are about **12% of the core total** (11.4-13.4%).
- Participation runs at roughly 7% of taxpayers contributing to any IRA versus 34-43% of wage earners deferring. People cannot be de-duplicated across the two sources, so no union rate is given.
- Employer contributions (match and nonelective) are not on the W-2, so this view leaves them out.

## Definitions

- **Taxpayer (IRA tables):** primary or secondary taxpayer on a filed Form 1040. Spouses count separately, and non-filers are excluded.
  - **Contributor:** a taxpayer with any contribution to that IRA type, from Form 5498.
  - **Owner:** a taxpayer with year-end FMV above zero.
  - **% of all taxpayers:** contributors divided by all taxpayers (column 1 of the by-age table: 215m in 2023).
  - **SEP and SIMPLE contributions** include employer contributions. The "All IRA types" row counts each person once.
- **Form 1040 series:** counts returns, not persons, so a joint return counts once. The IRA deduction is the deductible traditional-IRA adjustment, which excludes Roth and nondeductible contributions.
  - Percentages are of all returns, of AGI less deficit, and of Form 1040 salaries and wages. Form 1040 wages exclude pre-tax 401(k) deferrals.
  - Amounts are in $ thousands, current dollars, throughout.
- **W-2 series:**
  - **Taxpayers:** taxpayers on filed returns who have W-2 wages.
  - **Deferrals:** W-2 box 12 codes D, E, F, G, H, S, AA, BB and EE. These are employee elective contributions, pre-tax and Roth; employer contributions are excluded. Code G (457(b)) can include employer contributions.
  - **Deferral rate:** deferrals divided by the deferrers' Medicare wages (box 5).

## Method breaks and caveats

1. **IRS IRA tables, TY2022 revision.** In June 2026 SOI re-released TY2022 and TY2023 under a new methodology (the matched sample adds Forms W-2). The TY2022 numbers originally published in February 2025 under the old method are no longer posted.
   - The revision moved TY2022 contributor counts substantially. The old figures, as quoted by CRS R48051 (see `irs/README.md`), were 4,989,322 traditional contributors and 10,036,960 Roth contributors. The current files show 5,900,726 traditional (+18%) and 9,170,792 Roth (−9%).
   - So the 2021-to-2022 rise in traditional contributors and fall in Roth contributors are at least partly a method effect. Treat **2000-2021 and 2022-2023 as separate eras** (the `method_era` column).
2. **TY2022 by-age table quirk.** At ages 20-24 the year-end owners and FMV are published as 0 and appear to be folded into 25-29. Owner-based rates for 20-24, 25-29, Under 25 and 25-34 are blanked for 2022.
3. **Missing tables.**
   - TY2003 IRA tables were never published.
   - The TY2022 Table 8 link on the SOI page returns a 404, so Table 8 covers 2017-2021 and 2023.
   - TY2021 and later W-2 tables are not posted. The SOI W-2 page lists only TY2019-2020 plus the 2008-2018 compendium, and `21in03w2all.xlsx` returns a 404.
4. **Contribution limits change the at-limit shares** (`contribution_limits.csv`, from IRS COLA tables).
   - IRA limit: $3,000 (2002) → $4,000 (2005) → $5,000 (2008) → $5,500 (2013) → $6,000 (2019) → $6,500 (2023) → $7,000 (2024) → $7,500 (2026).
   - IRA catch-up: $500 (2002-05), then $1,000, then $1,100 (2026).
   - 402(g) deferral limit: $7,627 (1989) → $10,500 (2000) → $15,500 (2007) → $19,500 (2020) → $22,500 (2023) → $24,500 (2026).
   - 401(k) catch-up: $1,000 (2002) rising to $5,000 (2006), $6,500 (2020), $7,500 (2023) and $8,000 (2026). SECURE 2.0 adds a higher age 60-63 catch-up from 2025.
5. **Policy breaks.**
   - ERTA 1981 made IRAs universal from TY1982; TRA 1986 restricted the IRA deduction from 1987.
   - Roth IRAs started in 1998, Roth 401(k)/403(b) in 2006 (codes AA/BB), and Roth 457(b) in 2011 (code EE).
   - SECURE Act: no age cap on traditional contributions from TY2020.
   - SECURE 2.0: Roth employer contributions and the higher catch-up are not yet in the tax data.
6. **Form 1040 archive values (1975-1992) are hand-transcribed** from the OCR text of scanned SOI reports (Table A). Every value except 1983 appears in two or more reports and was cross-checked. The notes column records each OCR conflict and how it was resolved (for example, 1984 all returns 99,438,708 vs 99,458,708).
   - In 1976-79 and 1981-82 the value was not extractable from the OCR, so those years are blank.
   - For 1992-1996 the IRA deduction is published only as separate primary and secondary lines. The amount is their sum; the count of returns is blank. AGI for 1992 was not transcribed.
7. **Form 1040 deduction vs IRA Table 1 "deducted".** These are different concepts: returns vs persons, and Form 1040 vs the matched 5498 sample. For example, in 2023 Form 1040 shows $13.8bn on 2.5m returns, while Table 1 shows traditional deducted of $10.0bn and a total deducted (including SEP/SIMPLE) of $21.2bn. Do not mix them.
8. **W-2 Medicare-wage totals.** The published box-5 totals for TY2008 and TY2012 exceed box 1 by unusually large amounts (2012: +$921bn, against +$245-336bn in other years). Deferrals as a share of all Medicare wages therefore dips in those years (3.35% in 2012).
   - Use `deferrals_pct_box1_plus_pretax`, which is steady.
   - The 2020 figures for ages 45-54 (deferral rate 7.1% vs 6.4% in 2019) look like a jump in the published table; flag before quoting.
   - In the lowest wage-size bins the deferral rate is inflated: the bins are on box-1 wages, which are net of pre-tax deferrals.
9. **W-2 coverage.** Filed returns only. Covers both private and public employers. The participation shares match `dc_policy/output/irs_w2_deferral_participation.csv` exactly in every year.

## Files

| Output | Content |
|---|---|
| `output/ira_contributions_by_type.csv` | TY2000-2023 by IRA type: contributors, amount, deducted, owners, FMV, all taxpayers, % of taxpayers, % of owners, average, % of FMV, % of Form 1040 wages |
| `output/ira_contributions_by_age.csv` | Native 5-year bands and harmonised groups (Under 25 … 70+): % of taxpayers, % of owners, average, % of FMV |
| `output/ira_contributions_by_type_age.csv` | Table 8 by type and age, 2017-2021 and 2023 (% of owners contributing, average) |
| `output/ira_contributions_at_limit.csv` | Traditional and Roth contributors at the limit, 2004-2023 |
| `output/f1040_ira_keogh_deduction_long.csv` | IRA deduction and Keogh/SEP/SIMPLE deduction, 1975-2023: returns, $, % of returns, % of AGI, % of wages |
| `output/f1040_savers_credit.csv` | Saver's credit 2002-2023 |
| `output/w2_deferrals_totals.csv` | National W-2 deferral totals 2008-2020: counts, $, rates, Roth share, at-max share, box-1/box-5 totals |
| `output/w2_deferrals_by_age.csv`, `w2_deferrals_by_wage_size.csv`, `w2_deferrals_by_plan_type.csv` | Breakdowns |
| `output/combined_ira_w2_contributions.csv` | IRA + deferrals as % of gross wages, 2008-2020 |
| `output/contribution_limits.csv` | 402(g), catch-ups, IRA and SIMPLE limits, 1989-2026 |
| `scripts/` | `fetch.sh`, `run_all.sh`, five build scripts, `peek.py` (sheet viewer) |
| `raw/` | `ira/` (100 SOI IRA tables), `w2/`, `f1040/` (Table 1.4, Table 3.3, histab1), COLA PDF and page snapshots, `manifest.csv` |

## Sources

- **SOI IRA tables:** https://www.irs.gov/statistics/soi-tax-stats-accumulation-and-distribution-of-individual-retirement-arrangements
  - Files at https://www.irs.gov/pub/irs-soi/YYin0Tira.xls[x]. Table 1 is by type, Table 4 by age, Tables 5/6 by size of contribution, Table 8 by type and age.
  - TY2000 uses `00in0Tir.xls`, where Table 5 is by age. TY2002 uses `02in06ira.xls` (by type) and `02in10ira.xls` (by age).
- **SOI Form W-2 statistics:** https://www.irs.gov/statistics/soi-tax-stats-individual-information-return-form-w2-statistics
  - `18inallw2.xls` (TY2008-2018), `19in0Tw2all.xlsx`, `20in0Tw2all.xlsx`.
- **SOI Table 1.4:** https://www.irs.gov/statistics/soi-tax-stats-individual-statistical-tables-by-size-of-adjusted-gross-income
  - `93in14si.xls` … `23in14ar.xls`; Table 3.3 `YYin33ar.xls`.
- **SOI historical Table 1:** https://www.irs.gov/pub/irs-soi/histab1.xls (TY1999-2016).
- **SOI archive reports:** https://www.irs.gov/statistics/soi-tax-stats-archive-1954-to-1999-individual-income-tax-return-reports (`84inar.pdf` … `93inar.pdf`, Table A).
- **IRS COLA tables:** https://www.irs.gov/retirement-plans/cola-increases-for-dollar-limitations-on-benefits-and-contributions and https://www.irs.gov/pub/foia/ig/tege/cola-table-dci005ma4578824.pdf

## Unresolved

- 1976-79 and 1981-82 IRA and Keogh deductions are missing. They could be read by eye from the archive PDFs (`76inar.pdf` … `82inar.pdf`, Table 1.4 "Payments to an IRA").
- TY2021+ W-2 tables and TY2024 IRA tables are not yet released.
- The old-method TY2022 IRA files cannot be retrieved, so the size of the method break cannot be measured beyond the CRS-quoted counts.
