# Staying in the DC plan after leaving the employer: non-recordkeeper evidence

Question (Richard, 2026-10-04): are there trends, as percentages, from non-corporate sources (not Vanguard or other recordkeepers) on how many people keep money in an employer DC plan after leaving? Can we infer it from the incidence data we already have?

Short answer: yes, three independent government or survey sources all point the same way as the recordkeeper data. More people keep money in former employers' plans now than 10-20 years ago. None of them gives a clean "share of 60+ leavers who stay" series like Vanguard's, so each is a proxy.

## 1. TSP one-year retention (FRTIB administrative data). Best direct series
Share of FERS (civilian federal) participants who still have a TSP balance one year after separating. All ages, no age split published. Quarterly; numbers and URLs in `notes_external_sources.md`.

| Fiscal year | Retention |
|---|---|
| FY15-FY16 | 57-61% (corrected values; the originally reported ones had a calculation error) |
| FY18-FY20 Q3 | 64-65% |
| FY21-FY22 Q2 | 68-73% (peak 72.7%), after more flexible withdrawal options started Sep 2019 |
| FY24-FY26 Q2 | 67-71% (latest 69.1%) |

Separated accounts as a share of all TSP accounts: 21.2% (2011), 24.3% (2013), 29.1% (2018), 30.9% (2021), 35.1% (2025).

## 2. DOL Form 5500: separated participants in private DC plans (administrative, all plans)
`output/form5500_dc_participant_status.csv`, script `scripts/form5500.py`, source PDFs in `raw/abstracts/`. "Separated" = "other retired or separated participants with vested right to benefits" (left the employer, money still in the plan, not drawing).

| Year | Separated per 100 active participants | Separated, % of all participants |
|---|---|---|
| 1999 | 18.2 | 15.2 |
| 2004 | 22.7 | 18.4 |
| 2005 | 20.0 | 16.5 |
| 2008 | 21.4 | 17.5 |
| 2014 | 23.9 | 19.1 |
| 2019 | 26.1 | 20.4 |
| 2023 | 29.1 | 22.2 |

Breaks: active definition widened in 2005 (eligible non-contributors added); 2009-2013 small-plan (5500-SF) filers counted everyone as active, so separated is understated then; SF split imputed from 2014. Compare within 1999-2004, 2005-2008, 2014-2023. Counts double-count people with several plans. This is a stock, not a leaver flow, and is pushed up by auto-enrollment (many small abandoned accounts) as well as by retirees staying. No age split.

## 3. SCF 1989-2022: households with money in a former employer's plan (the "infer from incidence" route)
`output/scf_pastjob_long.csv`, script `scripts/scf_pastjob.py` (reuses `scf/scripts/scf_analysis.py`; replicate-weight SEs 2004+). Past-job plan = Fed FUTPEN (account plans from a past job, not yet paying) + CURRPEN (account plans now paying out). CURRPEN exists only from 2001, so use 2001+ for trends; FUTPEN alone runs from 1989.

Main measure: of households holding either an IRA or a past-job plan account, % that have money in a past-job plan (IRAs being where rolled-over money goes). SE in brackets.

| Group (reference person) | 2004 | 2007 | 2010 | 2013 | 2016 | 2019 | 2022 |
|---|---|---|---|---|---|---|---|
| Age 60-74, not working | 16.1 (2.7) | 19.1 (2.2) | 23.0 (1.9) | 18.8 (1.8) | 23.3 (1.9) | 29.3 (2.6) | 26.0 (2.6) |
| Age 65-74 | 17.6 (2.4) | 12.5 (1.9) | 18.7 (1.7) | 15.9 (1.4) | 20.1 (1.6) | 27.2 (2.0) | 21.9 (2.2) |
| Age 55-64 | 13.7 (1.7) | 19.0 (1.8) | 17.0 (1.4) | 19.1 (1.6) | 20.0 (1.3) | 25.1 (1.8) | 24.7 (2.1) |
| All households | 15.2 (0.9) | 17.3 (0.9) | 17.7 (0.7) | 19.9 (0.9) | 17.7 (0.7) | 25.8 (0.9) | 21.8 (1.0) |

Dollar share (past-job plan $ / (past-job plan + IRA $)), age 60-74 not working: 14-21% in 2004-2013, 19-27% in 2016-2022, but noisy (2022 SE 9.5 points). All households: 14-17% 2004-2016, 17-18% 2019-2022.

Caveats: IRAs also hold contributory (non-rollover) money, so this understates the stay share among leavers; respondents may misreport an old 401(k) as an IRA or vice versa; it's a stock across all past job changes, not a leaver cohort. 2019 looks high across most groups and 2022 eases back, so read the trend as 2004-07 vs 2019-22.

## 4. Other non-corporate sources (snapshots, not trends)
See `notes_external_sources.md`. TSP 2012 leavers by end 2013: 49% took no action (pre-2019 rules). HRS 2008/2010 (EBRI analysis of survey data, 50+): of retirees from their last job, 17.2% left money in the plan, 42.8% were receiving benefits, 21.5% rolled to an IRA, 15.1% cashed out. SIPP (Copeland 2013) covers only lump-sum takers. GAO, PSCA and state 457 plans gave no retention rates.

## What goes where
Nothing here has been put in the report or CLAUDE.md. The TSP retention series and the SCF table are the natural candidates for the report (the "Microdata cross-check section" thread owns it).
