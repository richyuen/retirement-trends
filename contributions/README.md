# Contributions to retirement accounts: trends over time

Built 2026-10-06 for Richard's question on trends in contribution rates to IRAs and DC plans, split and combined. Percentages throughout (Richard's preference). Three sub-folders, each with `scripts/`, `output/` and a `notes.md` holding definitions, variable lists, breaks and source URLs:

- `scf/` Survey of Consumer Finances microdata, 1989-2022 (household survey; SEs from replicate weights)
- `irs/` IRS SOI tax data: IRA contributions 2000-2023, Form 1040 IRA deduction 1975-2023, W-2 elective deferrals 2008-2020
- `admin/` DOL Form 5500 (1975-2023), BEA NIPA employer contributions (1948-2025), BLS ECEC employer cost (2004-2026), recordkeeper context (Vanguard, TSP, Fidelity)

## Three meanings of "contribution rate" (kept separate)

1. **Share contributing**: % of people/families/taxpayers putting money in.
2. **Percent of pay**: contribution / pay among contributors (employee, employer, total).
3. **Aggregate effort**: total contributions / total wages of a population.

## Main findings

**1. The rise in DC saving came from more people contributing, not higher rates.**
- Share contributing to a current-job DC plan (SCF): working families with head 25-64 rose from 28.9% (1989) to 44.0% (1998), held at 42-45% through 2019, then 48.1% (2022). All families: 18.0% to 31.3%. [`scf/output/scf_contrib_headline.csv`]
- Take-up among workers with a DC plan (SCF): 74.8% (1989) to 90.2% (2022). Early account plans were often employer-only profit sharing, which partly explains the low early take-up.
- Wage earners making elective deferrals (IRS W-2, all employers): 34.7% (2008) to 42.8% (2020). [`irs/output/w2_deferrals_totals.csv`]
- Employee percent of pay among contributors is flat: SCF median 6% in every wave except 5% in 2010-2013; mean 6.8-7.9% (1992 outlier 8.7%, 7.6% with rates capped at 25%). W-2 deferrers: 6.3-6.7% of pay, 2008-2020. Vanguard (recordkeeper): average 6.9% (2015) to 7.6% (2024-25).

**2. Employers' share is flat to falling; employees carry the growth.**
- Employer % of pay per covered contributor (SCF mean): 5.0% (1989), 4.5% (2004), 3.8-3.9% (2007-2013), 4.1% (2022).
- Form 5500 private DC plans, excluding rollovers: employee contributions 2.76% (1999) to 4.34% (2023) of private wages; employer 1.83% to 2.58%. Employees' share of DC contributions: 59-61% through 2017, 62.7-63.1% in 2021-2023. [`admin/output/dol_dc_contrib_by_source.csv`]
- Total employer pension effort (DB+DC, BEA NIPA) hasn't risen: 4.3% of private wages at its 1993 peak, 3.47% in 2025. The mix flipped: DC 1.30% (1984) to 2.70% (2025), DB cash 2.86% to 0.71%. [`admin/output/bea_nipa_pension_contrib.csv`]
- BLS ECEC: private DC cost 1.8% of total compensation (2004) to 2.5% (2024-2026); DB 1.6% to 0.9%. [`admin/output/bls_ecec_retirement_annual.csv`]

**3. Aggregate DC contributions have risen as a share of wages.**
- Form 5500 DC contributions (employer + employee, excluding rollovers): 4.6% (1999) to 6.9% (2023) of private wages. Including rollovers, DC was 2.0% (1975), 4.9% (2000), 7.7% (2023). DC's share of all private pension contributions: 34.6% (1975), 76.7% (1990), 90.7% (2023).
- SCF employee + employer DC contributions as % of all employees' pay: 5.4% (1989), 7.0% (2004), 6.9% (2022). Per covered worker it is flat at 10.8-12.8% after 1995.
- Three sources agree on the employee piece at about 4.3-4.6% of wages: SCF 4.3% (2022), W-2 4.58% (2020), Form 5500 4.34% (2023, private only).

**4. IRAs: a small and fairly stable share; Roth now dominates.**
- Taxpayers contributing to any IRA (IRS SOI): 8.4% (2000), low of 5.7% (2011), 8.2% (2021-2023). Roth 3.8% to 4.4% (2023); traditional 3.2% to 2.7%; Roth contributors outnumber traditional every year (9.5M vs 5.9M in 2023). [`irs/output/ira_contributions_by_type.csv`]
- IRA owners contributing: 32.7% (2000), 20.7% (2011), 24.9% (2023). SCF agrees: IRA holders contributing 29.9-33.0% (2016-2022).
- IRA contributions are 0.8-1.0% of wages; as % of IRA assets they fell from 1.39% to 0.61% (2000-2023) because balances grew much faster than new contributions (inferred: mainly rollovers and investment returns).
- About 45-55% of traditional and 30-40% of Roth contributors put in exactly the limit; the share dips whenever the limit rises. [`irs/output/ira_contributions_at_limit.csv`]
- By age: young adults caught up (25-34: 8.0% in 2000, 5.3% in 2011, 9.5% in 2023); 70+ rose 0.9% to 2.2% after SECURE removed the age-70½ bar (TY2020).
- Long view (Form 1040 IRA deduction, returns, not persons): 1.5% of returns (1975), 15.9% (1985) when IRAs were universal, 6.8% (1987) after the 1986 tax reform, 1.56% (2023). Deductible IRA use never recovered; Roth (not deductible) took its place. [`irs/output/f1040_ira_keogh_deduction_long.csv`]

**5. Combined IRA + DC.**
- Tax data (2008-2020): traditional + Roth IRA contributions plus W-2 elective deferrals were 4.24% (2008) and 5.25% (2020) of gross wages; IRAs are ~12% of that. Employer DC money is not on the W-2, so this is employee saving only. [`irs/output/combined_ira_w2_contributions.csv`]
- Families contributing to a DC plan or an IRA (SCF, the only person-level combined measure): 33.7% (2016), 33.5% (2019), 36.3% (2022). SCF has no IRA contribution question before 2016.

## Method breaks and caveats (do not lose)

- **SCF:** 2004 pension-module redesign (account test by balance; variables X42xx-X50xx moved to X110xx-X115xx); 2010 detailed plans per person cut from 3 to 2 (1.2-1.7% of plan holders have more plans); 1989-2001 combination plans lack employer questions; post-2004 public file rounds percents (lumpy medians, some median SEs 0); IRA items are prior-year, DC items current. Share with a DC plan matches the Fed's DCPLANCJ exactly 1989-1998 and runs 0.7-1.8 pts lower after because DCPLANCJ also counts plans already paying out.
- **SCF raw 1989-2001 full files** are not in the shared folder (about 1 GB); `scf/scripts/scf_contrib.py` expects them in `/tmp/scfraw/x`. Re-download from https://www.federalreserve.gov/econres/files/ (scf89s/92s/95s/98s/01s.zip + rw1s zips) before re-running.
- **IRS IRA tables:** TY2022 method break (June 2026 revision raised 2022 traditional contributors 18%, cut Roth 9% vs the original release); treat 2000-2021 and 2022-2023 as separate eras (`method_era` column). No TY2003 tables. TY2022 by-age shows zero owners at 20-24 (blanked).
- **IRS W-2 stats:** stop at TY2020 (TY2021 file 404). Medicare-wage totals for 2008 and 2012 look inflated; use the box-1-plus-pretax denominator.
- **Form 1040 long series:** 1975-1992 values hand-copied from scanned reports, cross-checked across 2-4 reports; 1976-79 and 1981-82 missing; 1992-96 returns counts blank; counts returns, not persons.
- **Form 5500:** active definition widened in 2005 (per-active contributions drop ~9% that year for definitional reasons); 2009-2013 5500-SF counted everyone as active; rollovers sit inside E13 totals, so use the Table A4 employer + participant series for saving effort; private plans only.
- **BEA:** 1948-83 total is accrual-based and has no DB/DC split; NIPA employee DC includes the TSP and state/local plans, so it doesn't compare with Form 5500 participant contributions.
- **Recordkeeper data** (Vanguard 2015+, Fidelity one point, TSP) are plan-population samples skewed to large, auto-enrolling plans; label as such.

## Not done / gaps

- BLS NCS employer-match provisions (series list not downloadable; bls.gov 403 and API limit).
- ICI/EBRI 401(k) database and Vanguard before 2015 (blocked or not retrievable).
- No public source gives combined IRA + employer-DC contribution rates for the same people over a long period; the SCF 2016-2022 measure is the closest.
