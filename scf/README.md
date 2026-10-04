# SCF microdata: retirement accounts and withdrawals, households 60+

Built 2026-10-04 from the Fed's public SCF files (federalreserve.gov/econres/scfindex.htm).
Re-run: `python3 scf/scripts/scf_analysis.py && python3 scf/scripts/scf_tables.py` (needs pandas, numpy, pyreadstat; about 1 minute).

## What is here
- `raw/` downloaded files: summary extracts `rscfpYYYY.dta` 1989-2022, full public files `pYYi6.dta` and replicate weights `pYY_rw1.dta` 2004-2022, codebooks (2004, 2010, 2016, 2022), Fed `bulletin.macro.txt`. About 2.6 GB unzipped; the zips were deleted (re-download from the Fed).
- `scripts/scf_analysis.py` all estimates with standard errors -> `output/scf_estimates_long.csv`
- `scripts/scf_tables.py` wide tables `output/t1..t13*.csv` (each cell has an `_se` column)

## Definitions
- Unit: household (SCF "family"), age band of the reference person **at interview**. Withdrawal questions cover the **previous calendar year** (SCF 2022 -> 2021), so `ref_year` = survey year - 1 and people in a band were about a year younger then.
- Retirement accounts = Fed `RETQLIQ` = IRA/Keogh (`IRAKH`) + current-job DC (`THRIFT`) + DC from past jobs (`FUTPEN`) + account plans now paying out (`CURRPEN`).
- Withdrawal = Fed `PENACCTWD` > 0: IRA/Keogh withdrawals (X6557/X6565/X6573, amounts X6558/X6566/X6574) plus annualized withdrawals from account-type pensions (X6464.. current-pension grid, X6965.. past-job grid). The full-file flags reproduce `PENACCTWD > 0` for every household record except 5 of 22,085 in 2007.
- Incidence = withdrawing households per 100 households holding the account at interview (matches the report's "per 100 year-end holders"). Households that emptied an account are not in the denominator.
- Dollar rate = withdrawals in t-1 / balance at interview, among holders.
- Dollars: the Fed's summary extracts are in **2022 dollars** (checked: 2019 IRAKH = 1.16 x nominal X variables).
- Point estimates pool the 5 implicates; SEs = 999 bootstrap replicate weights (wt1b x mm) on implicate 1 plus 1.2 x between-implicate variance.

## Check against published figures
All-family ownership of retirement accounts 50.5% (2019) and 54.3% (2022), and conditional medians $75.3k and $87.0k, match the Fed's 2023 Bulletin table (50.5, 54.3, 75.3, 86.9; the 0.1k median gap is the median convention).

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
