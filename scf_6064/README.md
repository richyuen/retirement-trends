# SCF: why did withdrawals at ages 60-64 fall?

Built 2026-10-04 from the SCF public files already in `scf/raw/` (2004-2022 waves = withdrawals in 2003-2021).
Re-run: `sh scf_6064/scripts/run_all.sh` (pandas, numpy, pyreadstat, pyarrow; about 10 minutes). The built file and replicate weights are cached outside the shared folder in `$SCF6064_CACHE` (default `~/.cache/scf_6064`).

## Question
In `scf/` the one clear trend is falling withdrawals at 60-64. The all-holder dollar rate went from 1.59% (2003) and 1.56% (2006) to 0.58% (2021) (`scf/output/t5`). Did incidence fall too, and what explains the decline? Candidate explanations tested: more people working, balances shifting from IRAs to current-job DC plans (`THRIFT`), larger balances, composition (education, income, marital status, DB coverage, Social Security claiming) and Roth share. Comparison bands are 55-59 and 65-69.

## Definitions (same as `scf/README.md`)
- Unit: household, with the reference person's age **at interview** (`AGE`). Withdrawals are for the previous calendar year, so labels here use the withdrawal year (2003 ... 2021). The sample is holders: `RETQLIQ` > 0 = `IRAKH` + `THRIFT` + `FUTPEN` + `CURRPEN`.
- Withdrawal: `PENACCTWD` > 0 (flags `wd_ira`/`wd_pen` from `scf_analysis.full_flags`). IRA part = X6558+X6566+X6574, converted to 2022$ with CPILAG x CPIADJ as in `scf_rates.py`. Pension part = `PENACCTWD` minus the IRA part. That is annualized payouts from account-type plans: the current-pension grid X6464.. (accounts now paying out, `CURRPEN`) and the past-job grid X6965.. (`FUTPEN`). **Current-job DC (`THRIFT`) has no withdrawal item**, so THRIFT balances add to the denominator and never to the numerator.
- Incidence = withdrawing households per 100 holders. Dollar rate = sum `PENACCTWD` / sum `RETQLIQ` among holders, in %. Both are in 2022 dollars.
- Robustness measures:
  - `wd5` / `wd10`: holders whose withdrawals were at least 5% / 10% of their balance.
  - Rate excluding each wave's 3 largest withdrawing households (by weighted dollars, all implicates).
  - Rate with `THRIFT` removed from the denominator.
- Characteristics:
  - Work and Social Security: R working = Fed `LF`=1 (from X4100). Spouse/partner working uses the same rule on X4700. R retired = X4100 in (13, 50). R receives Social Security = X5303=1 (retirement benefit: also X5304=1). Household receives SS = X5301=1.
  - Account structure: IRA only / DC only / both, from `IRAKH` and `THRIFT`+`FUTPEN`+`CURRPEN`. Current-job DC = `THRIFT`>0. Past-job or paying DC = `FUTPEN`+`CURRPEN`>0.
  - IRA types: Roth = X6551+X6559+X6567. Rollover IRA = X6552+X6560+X6568. Both are used as shares of IRA balances.
  - Demographics: BA+ = `EDCL`=4. DB = `DBPLANT`. Married = `MARRIED`=1. Income = `INCOME` minus `PENACCTWD` (the Fed's income includes the withdrawals).
- Pooled periods: early = 2003/06 (SCF 2004+2007), late = 2018/21 (SCF 2019+2022). The waves are simply stacked with their own weights.
- SEs follow `scf_analysis.py`: 999 bootstrap replicate weights (wt1b x mm) on implicate 1, plus 1.2 x the between-implicate variance. Pooled-wave and decomposition statistics apply replicate k of every wave together, and the DFL logit is refit for every replicate and implicate.

## Method
- (a) `a_descriptives.py` -> `output/a_descriptives_long.csv` (all bands) and `a_descriptives_6064_wide.csv`. About 40 outcome and characteristic series by band and wave, with SEs and `n` (unweighted holder households).
- (b) `b_subgroups.py` -> `output/b_subgroups_long.csv`: incidence and rate within subgroups, with `n_holders`/`n_withdrawers`. The subgroups are working status, account type, THRIFT, SS receipt and DB. `output/b_shiftshare.csv` splits the change from early to late (and to 2021) into between-group (composition) and within-group parts.
- (c) `c_decomposition.py`:
  - `c_differences.csv`: late minus early with SEs. It also splits the rate change accounting-wise into withdrawals per holder vs balance per holder (log points) and into the IRA vs pension parts.
  - `c_dfl.csv`: DiNardo-Fortin-Lemieux reweighting of late holders to the early composition. Specs:
    - `work_ss`: R working, spouse working, married, R gets SS
    - `accounts`: has IRA, has past-job/paying DC, THRIFT share of balance 0 / up to 0.5 / over 0.5
    - `balance_income`: 6 real balance bins, 5 income bins
    - `demographics`: education (4 categories), DB, female, single-year age
    - `all`
    `composition` = actual late minus counterfactual. `unexplained` = counterfactual minus early. Each row also reports the largest weight share and the effective n.
  - `c_lpm.csv`: pooled 7-wave weighted LPM of 100 x 1{withdrew} (also `wd5`, `wd10`) on wave dummies, with and without the same controls. It reports the late-minus-early contrast.

## Findings (60-64 unless stated; estimate (SE))
1. **Incidence did not fall.** Withdrawers per 100 holders: 15.5 (3.0), 15.7 (2.4), 14.0, 15.6, 16.1, 16.3, 13.9 (2.0) for 2003-2021.
   - Early to late: 15.6 (1.7) -> 15.0 (1.4), change -0.6 (2.1). Early to 2021: -1.7 (2.5).
   - Per 100 IRA holders it rose: 15.7 (1.7) -> 19.6 (1.8).
   - What fell is **large** draws. Holders withdrawing at least 10% of their balance: 7.7 (1.6) -> 3.3 (0.9), change -4.3 (1.6). At least 5%: 11.9 -> 8.5, change -3.4 (1.9).
2. **The dollar rate fell: 1.58% (0.37) -> 0.69% (0.10), change -0.88 (0.38); 2021 alone 0.58 (0.11).** In log points, early to 2021 is -1.00 (0.32):
   - -0.61 (0.33) from lower withdrawals per holder: $6.3k (1.5k) -> $3.4k (0.7k), 2022$
   - -0.39 (0.13) from higher balances per holder: $398k (33k) -> $587k (62k)
   Balances per holder grew just as much at 55-59 (+$128k) and 65-69 (+$201k), where rates did not fall (55-59: 0.33 -> 0.42; 65-69: 1.91 -> 2.00). So "bigger balances" is only a mechanical explanation where withdrawal dollars did not keep up, and that happened only at 60-64.
3. **Almost all of the decline is in the pension-account part, which rests on a handful of households.**
   - Pension part: 0.95 (0.36) -> 0.17 (0.05), change -0.78 (0.36). IRA part: 0.62 (0.11) -> 0.52 (0.09), change -0.10 (0.13). IRA withdrawals / `IRAKH` were steady at 1.0-1.9% through 2018 (early 1.19, late 1.08), then 0.79 (0.19) in 2021.
   - Only 31-65 withdrawing households a wave stand behind the 60-64 rate. The largest one in the 2006 data (a $1.5M payout from a pension account) is 41% of 60-64 withdrawal dollars; the top 3 are 41% in 2003 and 58% in 2006.
   - Excluding each wave's top 3 withdrawing households, the decline is real but smaller: 0.83 (0.13) -> 0.49 (0.07), change -0.34 (0.14).
   - Payouts from account-type pensions moved to older ages. The pension part at 65-69 rose from 0.26 (0.07) to 0.75 (0.25). This fits later retirement but is thin.
4. **Characteristics of 60-64 holders, early -> late:**
   - Working: R working 70.2 -> 77.0%. R or spouse working 81.0 -> 86.7%. R retired 33.7 -> 26.1%.
   - Social Security: R receives SS 26.4 -> 15.2% (retirement benefit 18.4 -> 7.9%).
   - Accounts: holders with THRIFT 47.7 -> 62.1%. DC-only 26.4 -> 43.5%. IRA-only 42.9 -> 25.7%. THRIFT share of balances 34.2 (4.5) -> 40.2 (3.0)%. CURRPEN share 5.1 -> 2.5%.
   - Roth: share of IRA dollars 7.2 (2.1) -> 11.0 (1.3)%; holders with a Roth 16.5 -> 22.6%.
   - DB coverage 50.5 -> 42.7%. BA+ (49%) and married (69-71%) are unchanged. Median balance $143k -> $177k.
5. **Within subgroups (b), early -> late:**
   - Incidence of working households: 12.0 (1.8) -> 10.3 (1.1), and 8.1 in 2021. Of households where neither works: 31.1 (4.9) -> 46.0 (5.8).
   - Incidence in THRIFT households is low and flat: 5.3 -> 5.0. IRA-only households: 22.8 -> 31.1.
   - The rate fell inside almost every group: working 0.97 -> 0.42; neither working 4.5 -> 2.1; IRA and DC 1.68 -> 0.27. IRA-only did not fall: 1.49 -> 1.78.
   - Shift-share: composition changes in holder shares would have lowered incidence by
     - 1.1 (0.5) points for working status
     - 2.3 (0.7) for SS receipt
     - 2.8 (0.8) for account type
     Rising within-group incidence offset them. Balance-share composition explains at most -0.18 (0.17) of the -0.88 rate change.
6. **Reweighting (DFL) and regression (c), early -> late:**
   - Incidence: the `all` composition predicts a fall of 6.1 (2.6) points (accounts 4.2, work/SS 2.1). Within-cell incidence rose +5.5 (3.3), so composition explains a decline that did not happen in the raw series.
   - `wd5`: composition explains all of the -3.4 or more (-5.3, SE 2.5).
   - `wd10`: composition explains little: -0.6 (0.7) of -4.3 (1.6). LPM: -4.4 (1.6) without controls, -2.7 (1.5) with all controls.
   - Dollar rate: composition explains -0.23 (0.11) of -0.88 (about a quarter). Mostly accounts -0.19 (0.08) and work/SS -0.11 (0.06). Balance/income -0.04 and demographics +0.05 contribute nothing.
   - Trimmed (top-3-excluded) rate: composition explains -0.28 (0.11) of -0.34 (0.14), most of it.
   - Same picture for 2021 alone: rate -1.00, of which composition is -0.36 (0.18).
7. **The comparison bands show no decline.**
   - 55-59: incidence 4.7 -> 5.4; rate 0.33 -> 0.42; composition effects about 0.
   - 65-69: incidence 26.1 -> 28.3; rate 1.91 -> 2.00. `wd10` fell there too: 13.2 -> 8.1, change -5.1 (2.3).
   So the fall in large draws is not specific to 60-64. The fall in the dollar rate is.

**Bottom line.**
- The 60-64 decline is a decline in withdrawal **dollars** relative to balances, not in how many holders withdraw.
- About 77-88% of the measured fall comes from account-pension payouts (-0.78 of -0.88 early to late; -0.77 of -1.00 to 2021). Their 2003/06 level depends on a few very large cases, and in part they seem to have moved to 65-69.
- Of the robust remainder (the trimmed rate, -0.34 points), most is composition:
  - more 60-64 holders still working and not yet claiming Social Security
  - more holders whose money sits in current-job DC plans with no withdrawal item, and fewer IRA-only holders
- Larger balances add mechanically: dollars per holder did not grow while balances per holder rose about 40%.
- Roth growth (7% -> 11% of IRA dollars), education, marital status and DB coverage explain essentially nothing.

## Caveats
- **Thin cells.** About 300-475 holder households per wave at 60-64, with only 31-65 withdrawers. Dollar rates are dominated by a few households (see finding 3). Any 2003/06-vs-2021 contrast on the untrimmed rate is only about 2.3 SE. Subgroup cells with fewer than about 15 withdrawers (e.g. THRIFT households, SS recipients in 2021: `n_withdrawers` in `b_subgroups_long.csv`) are not reliable.
- The DFL results depend on specification order and spec. The `all` spec has an effective n of about 390 for 2021 alone (largest weight share 1.2%). Composition effects on incidence and on the rate point in the same direction but are not precisely measured.
- Balances are at interview (year t) and withdrawals in t-1. The 2021 rate divides 2021 withdrawals by early-2022 balances, after the 2021 market rise. A 2020 CARES Act pull-forward would also depress 2021 IRA withdrawals. Neither can be separated here.
- The SCF does not ask which IRA type a withdrawal came from, so the Roth share is measured only on balances. Withdrawals are not split into RMD, rollover, conversion, partial or full.
- THRIFT has no withdrawal item, so in-service withdrawals or hardship distributions from current-job plans are not measured at all. More current-job DC lowers the measured rate by construction.
- Ages are the reference person's at interview, about a year older than at withdrawal. Spouses' ages and accounts are pooled at the household level.
