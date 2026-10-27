# SCF microdata: retirement accounts and withdrawals, households 60+

Built 2026-10-04 from the Fed's public SCF files (federalreserve.gov/econres/scfindex.htm).
Re-run: `python3 scf/scripts/scf_analysis.py && python3 scf/scripts/scf_tables.py && python3 scf/scripts/scf_rates.py` (needs pandas, numpy, pyreadstat; about 2 minutes). Updated 2026-10-27 with SCF 2025.

## What is here
- `raw/` downloaded files: summary extracts `rscfpYYYY.dta` 1989-2025, full public files `pYYi6.dta` and replicate weights `pYY_rw1.dta` 2004-2025, codebooks (2004, 2010, 2016, 2022, 2025), Fed `bulletin.macro.txt` (2025 vintage; the 2022-vintage copy is `bulletin.macro_2022vintage.txt`). About 2.6 GB unzipped; the zips were deleted (re-download from the Fed).
- `scripts/scf_analysis.py` all estimates with standard errors -> `output/scf_estimates_long.csv`
- `scripts/scf_tables.py` wide tables `output/t1..t13*.csv` (each cell has an `_se` column)

## Definitions
- Unit: household (SCF "family"), age band of the reference person **at interview**. Withdrawal questions cover the **previous calendar year** (SCF 2022 -> 2021), so `ref_year` = survey year - 1 and people in a band were about a year younger then.
- Retirement accounts = Fed `RETQLIQ` = IRA/Keogh (`IRAKH`) + current-job DC (`THRIFT`) + DC from past jobs (`FUTPEN`) + account plans now paying out (`CURRPEN`).
- Withdrawal = Fed `PENACCTWD` > 0: IRA/Keogh withdrawals (X6557/X6565/X6573, amounts X6558/X6566/X6574) plus annualized withdrawals from account-type pensions (X6464.. current-pension grid, X6965.. past-job grid). The full-file flags reproduce `PENACCTWD > 0` for every household record except 5 of 22,085 in 2007.
- Incidence = withdrawing households per 100 households holding the account at interview (matches the report's "per 100 year-end holders"). Households that emptied an account are not in the denominator.
- Dollar rate = withdrawals in t-1 / balance at interview, among holders.
- Dollars: everything is in **2022 dollars**. The 1989-2022 summary extracts are the Fed's 2022-vintage files (checked: 2019 IRAKH = 1.16 x nominal X variables). The 2025 extract is in 2025 dollars; `scf_analysis.py` multiplies its dollar variables by 4376/4789 (the Fed's CPI bases for 2022 and 2025 in `bulletin.macro.txt`). To restate in 2025 dollars, multiply any 2022-dollar figure by 4789/4376 = 1.094.
- Point estimates pool the 5 implicates; SEs = 999 bootstrap replicate weights (wt1b x mm) on implicate 1 plus 1.2 x between-implicate variance.

## Check against published figures
All-family ownership of retirement accounts 50.5% (2019) and 54.3% (2022), and conditional medians $75.3k and $87.0k, match the Fed's 2023 Bulletin table (50.5, 54.3, 75.3, 86.9; the 0.1k median gap is the median convention).

## SCF 2025 added (2026-10-27)
Released by the Fed 9 Oct 2026; withdrawals refer to 2024. Earlier waves reproduce the previous outputs exactly (max difference 0). Checks: full-file withdrawal flags reproduce `PENACCTWD > 0` for all 21,800 records; all-family ownership of retirement accounts 54.9% and conditional median $106.0k (2025$) match the Fed's 2025 historic table 6 (54.88%, $106k). The Fed's definitions of IRAKH, RETQLIQ and PENACCTWD did not change in 2025.

What 2025 shows (60+, 2024 withdrawals; SEs in the tables):
- **RMD age 73 shows up.** 70-74 incidence per 100 holders fell again, 61.0 (2021) -> 58.5 (2024, SE 3.7); IRA-only 62.5 -> 59.6. SECURE 2.0 moved the RMD age to 73 from 2023, so most of this band (69-73 in 2024) had no RMD yet. The fall is within about one SE of 2021, but the 2015 -> 2018 -> 2021 -> 2024 run is 74.2, 66.4, 61.0, 58.5.
- **75+ incidence at series highs:** 75-79 89.5 (IRA-only 97.4, SE 1.1), 80+ 93.3.
- **Dollar rates fell.** All holders 2.62% (2.92% in 2021), level with 2012 (2.61%) and above only 2009 (2.19%); withdrawers only 4.66% dollar-weighted (5.57% in 2021), the lowest of any wave; median IRA withdrawer 4.9%. Lower at every age band 65+. Part of this is mechanical: the denominator is the balance at the 2025 interview, after strong 2024-25 market gains, while withdrawals are 2024 dollars.
- **Balances jumped:** 60+ retirement accounts $19.0T in 2022$ ($13.8T in 2022 survey); withdrawals $498B in 2024 ($403B in 2021). 60-64 ownership rose to 64.6% (55.7%).
- SCF vs IRS (t13) for 2024 waits for IRS TY2024, not released as of 2026-10-27.
- Noisy cells: 80+ median balance $343k (SE $108k); DC-pension incidence at 75+ (SEs 7-9 points).

## Findings (households 60+)
1. **Withdrawals track RMDs, as in IRS data.** Per 100 holders, withdrawal incidence is 14-16 at 60-64 and 21-33 at 65-69, then 61-80 at 70-74 and 80-92 at 75+ in normal years (t1).
2. **The 2009 RMD waiver shows clearly.** SCF 2010 (2009 withdrawals): 70-74 incidence 46.2 (SE 3.4) vs 66.9 in 2006 and 70.8 in 2012; 80+ 56.7 vs 82.5 and 82.2. The 2020 waiver falls between waves and is not observable.
3. **SCF 2022 shows the RMD age moving to 72.** 70-74 incidence fell from 74.2 (2015) and 66.4 (2018) to 61.0 (2021), while 75-79 and 80+ stayed at 86.6 and 91.6.
4. **Incidence among 75+ holders has risen.** 75-79: 68.1 (2003) -> 79-87 (2012-2021); 80+: 70.6 -> 82-92. Ownership by the oldest rose too: 80+ households with any account 20.3% (2004) -> 39.3% (2022).
5. **Rates are small and stable.** Withdrawals were 2.2-3.1% of 60+ balances every wave (2.2% in 2009); by age about 1% at 60-64 rising to 5-7% at 80+ (t5; 12% in 2006 rests on a small sample), consistent with RMD-sized draws.
6. **Pension-account (DC) withdrawals are much rarer than IRA withdrawals** at every age: 60+ DC-holders 13-25 per 100 vs IRA-holders 36-55 (t2, t3). Consistent with retirees rolling DC money to IRAs before drawing.
7. **Scale.** 60+ households held $13.8T in retirement accounts in 2022 (2022$; $0.9T in 1989) and withdrew $403B in 2021 (t7, t11).

## SCF vs IRS SOI IRA incidence (t13)
Same reference year, IRA holders only. The age pattern and the 2009/2021 dips line up; SCF levels run below IRS at 65+ (e.g. 2018: 70-74 SCF 70.5 vs IRS 85.6; 80+ 95.3 vs 101.1). Reasons, not yet quantified: SCF ages are about a year older than at withdrawal (moves some pre-RMD people into 70-74); SCF counts households and the reference person's age, IRS counts individuals; IRS incidence uses year-end holders and can exceed 100; Roth IRAs (no RMD) are in both denominators.

## Caveats
- Withdrawal items start in SCF 2004 (questions changed that year); earlier waves give balances only.
- The 60+ cells for 75-79/80+ DC-pension incidence rest on few cases (SEs 7-24 points).
- The IRA withdrawal question does not ask whether a withdrawal was an RMD, a rollover or a Roth conversion, and does not separate partial withdrawals from full cash-outs.

## Withdrawal rates: all holders vs withdrawers only (added 2026-10-04)
`scripts/scf_rates.py` -> `output/scf_rates_long.csv` (with SEs) and `output/t14_withdrawal_rates_holders_vs_withdrawers.csv`.
Rate = prior-year withdrawals / balance at interview, 2022 dollars. Dollar-weighted (sum/sum) for all holders and for withdrawers only, plus the weighted median of each withdrawing household's own rate. All accounts (PENACCTWD/RETQLIQ) and IRA only (X6558+X6566+X6574 put in 2022$ with the Fed's CPILAG x CPIADJ, / IRAKH).
Headlines, 60+: all holders 2.2-3.1%; withdrawers 5.2-6.9% dollar-weighted, median 5.7-7.5%. In 2009 the all-holder rate fell (3.0 -> 2.2) but the withdrawers-only rate did not (6.9 -> 6.8). Withdrawers-only rate drifted down from 6.6-6.9 (2003-2009) to 5.2-6.1 (2012-2021).
