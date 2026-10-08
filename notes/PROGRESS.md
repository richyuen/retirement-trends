# Retirement withdrawal trends report — working state

## What happened
- 3:33 PM EDT Oct 3 2026: user asked for multi-page HTML research report (withdrawal incidence & rates; partial withdrawals vs full cashouts vs rollovers; IRA + DC; in retirement; sources ICI, EBRI, SCF, IRS, CPS; charts + animations).
- First run spawned 5 researchers; 4 finished, the IRA researcher was cut off when the user's session limit hit at 4:20 PM. No report written.
- 8:59 PM: user re-sent request; asked "are we resuming work from before?" -> answered yes, building from saved notes.
- CONSTRAINT: user has a session usage limit. Be token-economical. No new research fan-out. Publish a draft early.

## Inputs on disk
- Notes: /home/claude/research_notes/Retirement account withdrawal trends/{ira_withdrawals,dc_plan_distributions,rollovers,household_surveys,rmd_policy_tax_data}.md
- Recovered IRS SOI extractions (from interrupted researcher's transcript): /home/claude/work/recovered/js_*.txt
  - js_559 = IRS SOI Table 4 by age 2004-2023 (withdrawers, amounts, EOY holders, FMV)
  - js_563 = IRS SOI Table 1 by IRA type 2004-2023
  - js_331 = TY2023 Table 4 full (incl. rollovers by age) and Table 8
  - js_355/359/367 = Form 1040 taxable IRA distributions (Table 1.4)
- Earlier researcher transcripts: /root/.claude/projects/-home-claude/30764398-ac58-5b73-b29e-785f33e5213c/subagents/

## Plan
1. Build chart data file: /home/claude/work/data.json (with source URLs)
2. Load artifact-design + dataviz skills, then write /home/claude/work/report/index.html (self-contained, inline SVG charts, animations, print CSS)
3. Render check with Playwright (desktop/phone, light/dark)
4. Publish as Artifact early; then fact-check pass against notes/sources; republish
5. Final message: summary + sources

## Status log
- [done] located notes, recovered IRS data
- [done] read chart-ready sections of all 5 notes files + takeaways; IRS derived series computed (build_data.py -> irs_derived.json, irs_2023_table4.json)
- Decision: NOT spawning report-writer/research subagents (session-limit risk); writing report directly from notes.
- Key computed facts: IRS 2012-2023 consistent era (withdrawer counts jump in 2012, also odd 2004/2008): 70-74 incidence 86.9 (2012) -> 86.0 (2019) -> 58.8 (2020) -> 69.0 (2021) -> 69.1 (2022) -> 61.7 (2023); 65-69 32.6 -> 37.8; 60-64 23.9 -> 27.5.
  Rates W/prior-yr FMV 70+: 7.98 (2012), 6.83 (2019), 4.56 (2020), 6.07, 5.86, 5.93 (2023). 60-69: 4.29 (2012) -> 3.10 (2019) -> 3.21 (2023).
  Rollovers TY2023 all IRAs $682.4B, 5.86M taxpayers; 60+ share of $ 66.1% (2001: 40.6, 2010: 53.5); 55+ 80.3%.
  ICI says trad rollovers 2022 = $669.8B; IRS June-2026 file says trad $635.9B, all types $664.3B -> flag.
- Planned figures: (1) three-source overall incidence lines; (2) ICI db by age group lines 2007-2023 w/ waivers; (3) IRS animated bars by age 2012-2023; (4) ICI median % of balance by balance band & age; (5) IRS dollar-weighted rates; (6) RMD-only vs more stacked; (7) Vanguard 4-row stacked w/ people<->dollars toggle; (8) HAR 2021 retirees followed; (9) plan design lines; (10) Form 5500 benefits vs contributions; (11) IRA flows (IRS all-IRA 2004-2023); (12) rollover $ by age 2001/2010/2023; (13) survey capture bars; (14) policy timeline + RMD table.
- NEXT: Artifact quickstart (intent other) + dataviz skill -> write /home/claude/work/report/index.html
- [done] dataviz + artifact design guidance loaded; palettes validated (categorical 4 slots + 5-step blue ordinal, light #fdfdfe / dark #171a1f)
- Build layout: parts in /home/claude/work/report/parts/{10-head.html,20-body.html,30-script.html}; build.py concatenates -> report/index.html (artifact body, no doctype) and /home/claude/reports/Retirement account withdrawal trends.html (standalone)
- Design: cool paper bg, navy/black ink, "copy-A red" accent, Public Sans + Source Serif 4 + Roboto Mono, key figures as numbered tax-form boxes; refs auto-numbered by JS from REFS map.
- [done] report built (parts -> report/index.html + /home/claude/reports/Retirement account withdrawal trends.html); render-checked desktop/phone/dark; artifact published v1 at https://claude.ai/artifact/JTfbBBXQfUrpabgjxiGdqT
- [done] independent fact-check (verification.md: 38 findings, all 506 chart values OK) + ~25 web spot checks against sources; 55 text corrections applied; refs fixed (69 refs)
- NEXT: republish artifact (same path), SendUserFile standalone html, final summary with sources

- [done] 2026-10-04: microdata cross-check (Section 10, Figs 15-16, Tables 7-8, summary finding 9, data note) added; republished as version 3 of https://claude.ai/artifact/JTfbBBXQfUrpabgjxiGdqT

## 2026-10-04 v6
Folded in SIPP (sipp/), IRS refresh (irs/), SCF 60-64 (scf_6064/), CPS finish. Fig 16 = SIPP by age (RMD 72->73). Rollover flag resolved; IRS 2022 method break documented. 20 figures, 9 tables, 76 refs. Published v6.

## 2026-10-04 v7
SIPP long series 1996-2024 (sipp_hist/): Figs 17-18 inserted after Fig 16; later figs renumbered 19-22. Chart renderer gained zones and breaks options. 77 refs (nber-sipp96 added).

## 2026-10-04 v8
New Section 11 "Staying in the plan: evidence beyond recordkeepers" from dc_stay/: Figs 23 (TSP one-year retention), 24 (Form 5500 + TSP separated share), 25 (SCF former-employer plan share). Watch/notes/sources renumbered 12-14. 80 refs (tsp-minutes, tsp-stats, dol-5500-abs, ebri-hrs). Published v8.

## 2026-10-05 v9
New Sections 12 "Do the laws work?" (Table 10 scorecard, Fig 26 AE spread vs NCS participation, Fig 27 IRS early-withdrawal penalty 1996-2023), 13 "Where retirees' income comes from, and how they spend it" (Fig 28 CPS income shares, exclRINT; Fig 29 CE spending vs 55-64), 14 "How long the money has to last" (Fig 30 e65 by sex, Table 11 period vs cohort, income/education gaps). Summary findings 10-12, two watch items, three data notes. Watch/notes/sources renumbered 15-17. 107 refs. Line renderer: per-series connect. Published v9.

## 2026-10-05 v10
New Sections 15 Working longer (Fig 31 LFPR by age), 16 Health care costs (Fig 32 Medicare premiums vs SS benefit, Fig 33 MEPS OOP burden, Table 12 lifetime cost estimates), 17 Long-term care (Fig 34 nursing-home payer shares), 18 Social Security's finances (Fig 35 years to depletion by report, Table 13 cut vs income). Summary findings 13-15, one watch item, three data notes. Watch/notes/sources renumbered 19-21. 127 refs. Published v10.

## 2026-10-05 v11
New Sections 19 Are workers ready for retirement? (Fig 36, 37, Table 14), 20 Debt and housing wealth (Fig 38), 21 Poverty among older Americans (Fig 39, 40, Table 15), 22 Decline of DB pensions (Fig 41), 23 Annuities and lifetime income (Fig 42), from readiness/, debt_housing/, poverty/, db_pensions/, annuities/. Summary findings 16-20, a lifetime-income watch item and three data-notes bullets added; 27 refs (154 total). Section 13 DB share reworded to two clean segments at the research thread's request. Published as artifact version 11.

## 2026-10-06 v12
Section 12 participation trend switched from BLS all-plans (48-53%, includes DB) to BLS DC-only (41% 2010, 47% 2019, 49% 2026; Fig 26 now DC access/participation 2010-2026), plus a sentence reconciling with recordkeeper rates (Vanguard HAS 2026 86% of eligible; survey take-up 72%). Summary finding 12-area text and Table 10 row updated, data-notes sentence added, ref psca-2026. Requested by Richard via the DC policy thread; reasoning in dc_policy/README.md.

## 2026-10-06 v13
New Section 13 How much goes in: contribution trends (Fig 28 share contributing: SCF families 25-64, W-2 deferrers, IRA taxpayers; Fig 29 percent of pay: SCF employee/employer, W-2, Vanguard; Fig 30 Form 5500 DC contributions % private wages + IRA % wages), from contributions/. Later sections renumbered +1, figures +3. Summary finding and data note added; refs bea-nipa, bls-ecec, dol-a4, irs-1040-hist (159 total). Published as artifact version 13.

## 2026-10-06 v14
Richard asked whether Figs 29 and 30 are comparable. They are not in level: Fig 29 is rates among contributors (own pay), Fig 30 aggregate contributions over all wages. Captions now say so, and Section 13 adds a bridge (W-2: 6.5%->6.7% of deferrers pay x deferrers 55%->67% of wages = 3.6%->4.5% of all wages). Fig 29 caption also corrected: SCF rates are among contributors, not all workers with a plan.

## 2026-10-06 v15
Section 8 gets 'Is the share of plan money rolled over falling?' with Fig 14 rollshare (IRS trad-IRA rollovers / BEA DC outflows 93-99% 1999-2007 -> 75-82% 2019-2023; / Form 5500 private DC benefits), Vanguard 60+ cohort shift (Fig 8: rolled 66%->45% of assets, in plan 16%->46%), and 60-64 rollovers per 100 IRA holders flat ~10. Summary finding on staying in plan extended. Later figures +1.

## 2026-10-07 v16
Richard asked for an organization pass and chose Publish. Report regrouped into 7 labeled parts, 26 sections (old Section 11 merged into 7, duplicate TSP 2012 story told once; Section 7 annuity paragraph moved to annuities). Contributions and readiness now precede the laws scorecard; Social Security, DB and annuities join income; longevity, work, health, LTC grouped. Summary findings and data notes reordered; all cross-references remapped. See notes/reorg_proposal_v16.md.

## 2026-10-08 v17
Richard chose 'Add to report' for work after retirement. Section 19 gains 'Work after claiming Social Security' (Fig 41 workret, Table 14): 11.7% of SS retired-worker beneficiaries 62+ employed in March 2026 (7.1% PT, 4.6% FT), flat since 2010 apart from COVID; withdrawers 10.4% vs 12.0%; 62-64 fall is claiming selection. Summary finding on working longer and the data note extended.
