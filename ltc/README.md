# Long-term care: risk, cost and who pays

How likely someone turning 65 is to need long-term care (LTC, also called long-term services and supports, LTSS), how long and how much it costs, who pays (Medicaid, out of pocket, Medicare, insurance), how prices have moved against inflation and retirees' incomes, and what happened to private LTC insurance. Built 2026-10-05 from public sources. Two sources are private or industry sources and are marked as such: CareScout/Genworth prices and the Milliman insurance figures.

## Findings

1. **"7 in 10 will need long-term care" is right only under a broad definition. Under the standard insurance trigger it is about 56%.**
   - ASPE 2022 (Johnson & Dey, Urban Institute DYNASIM4 model) covers people turning 65 in 2021-2025 and uses the HIPAA / tax-qualified LTC insurance trigger: help with 2+ activities of daily living for 90+ days, or severe cognitive impairment. Under that trigger, **56.4%** will need care at some point: 48.6% of men and 63.7% of women.
     - Need lasts about **3.1 years on average** (5.4 years among those who need any care).
     - 22.1% will need care for more than 5 years; 11.9% for less than a year.
   - The "about 70%" figures use broader definitions or count everyone who survives to 65:
     - Kemper, Komisar & Alecxih (2005/06) gave **69%**, counting 2+ ADLs, 4+ IADLs, or any paid care. ASPE 2019 cites it.
     - Johnson (ASPE 2019) used historical HRS data from 1995-2014 and found that **70%** of people who survive to 65 develop severe needs and 48% receive some paid care.
   - CareScout (Genworth) still quotes "7 out of 10".
   - [`output/aspe_lifetime_ltc_risk.csv`]

2. **Most care is unpaid and short. Paid care is concentrated in a minority of people.**
   - In ASPE 2022, people average **0.8 years of paid care**. **54.7% will never use paid LTSS**, 24.1% use less than a year, and only **4.4% use 5+ years**.
   - Johnson 2019 (HRS, historical):
     - 28% of 65-year-olds eventually spend 90+ days in a nursing home.
     - 15% spend more than 2 years in a nursing home.
     - 13% receive Medicaid-financed long-term nursing home care.
     - Women are much more exposed than men: 34% vs 20% for long nursing-home stays, and 75% vs 64% for severe need.
   - Unpaid family care for people with significant disability who receive it is worth **$204,000** on average (2020 $), more than all paid care.

3. **Expected lifetime cost is about $121k per person, but the risk is concentrated.**
   - ASPE 2022 puts the average paid LTSS cost from 65 to death at **$120,900** (2020 $), or **$245,400** among people who use paid care. Women average $154,300 and men $85,400.
   - Who pays over a lifetime:

     | Payer | Share of lifetime cost |
     |---|---|
     | Medicaid | 43% |
     | Families out of pocket | 37% |
     | Other public (VA, Older Americans Act, Medicare hospice) | 15% |
     | Private insurance | 5% |

   - Out-of-pocket tail:
     - **14%** of people will pay at least $100,000 out of pocket, and **6.4%** more than $250,000.
     - In the top income quintile, **10.3%** pay more than $250,000 out of pocket.
     - Medicaid mostly protects the bottom: 35.4% of the bottom income quintile will use Medicaid LTSS, against 5.7% of the top.
   - Changes from the earlier ASPE 2016 brief (Favreault & Dey, turning 65 in 2015-2019):
     - That brief gave 52%, $138,100 (2015 $), a ~52% out-of-pocket share and 17% paying $100k or more. The 2022 brief says the drop comes mainly from methodology: it drops incidental Medicare post-acute care and uses new model equations.
     - **Don't read the 2016-to-2022 change as a trend.**

4. **Who pays for nursing homes has shifted from families to Medicare. Medicaid's share has stayed at about a third.**
   - CMS National Health Expenditure Accounts, nursing care facilities and continuing care retirement communities (CCRCs), all ages:

     | Year | Out of pocket | Medicaid | Medicare | Private insurance |
     |---|---|---|---|---|
     | 1980 | 40.5% | 46.2% | 2.0% | 1.2% |
     | 2000 | 31.6% | 37.5% | 12.8% | 8.5% |
     | 2010 | 26.4% | 33.0% | 23.0% | 7.6% |
     | 2019 | 24.5% | 32.8% | 22.1% | 8.9% |
     | 2024 | **22.1%** | **35.9%** | **21.5%** | 8.8% |

   - The Medicare share is mostly short post-acute skilled-nursing stays, not custodial long-term care.
   - Spending reached $219.9B in 2024, but nursing homes' share of personal health care fell from 7.4% (2000) to **4.9% (2024)**.
   - Home health is now 3.8% of personal health care (0.4% in 1970). Its payers in 2024: Medicare 32.9%, Medicaid 22.6%, private insurance 22.0%, out of pocket 17.9%.
   - The category that contains Medicaid home- and community-based (HCBS) waivers is now 63.2% Medicaid-funded (44.4% in 1990). Spending is moving from nursing homes to home and community care, and Medicaid follows it.
   - In 2020, "other third party" jumps to 16.6% of nursing-home spending. That is COVID Provider Relief Fund money, not a change in who pays.
   - [`output/nhe_ltc_payer_shares_1970_2024.csv`, `nhe_nursing_plus_homehealth_payer_shares.csv`]

5. **Far fewer older people live in nursing homes.**
   - Share of people 65+ living in nursing homes on census day:

     | Year | 65+ | 85+ |
     |---|---|---|
     | 1990 | **5.1%** | 24.5% |
     | 2000 | **4.5%** | 18.2% |
     | 2010 | **3.1%** | 11.2% |
     | 2020 | **2.5%** | **10.2%** |

     Ages 75-84 went from 6.1% to 2.7%; ages 65-74 from 1.4% to 0.9%.
   - Assisted living and home care absorbed much of the shift. Licensed residential-care (mostly assisted-living) beds went from 851,400 (2012) to 1,000,000 (2014). Certified nursing-home beds were flat over the same period (1,669,100 to 1,663,300).
   - By 2020 there were 30.0 nursing-home beds and 22.0 residential-care beds per 1,000 people 65+ (NCHS).
   - The 2020 census count fell on April 1, 2020, early in COVID. [`output/census_pct_65plus_in_nursing_homes.csv`]

6. **Nursing-home prices have outpaced general inflation by about 1-1.4 points a year. Home-care prices are less clear.**
   - BLS annual averages:
     - The CPI-U for nursing homes and adult day services rose **3.91%/yr in 1997-2025**, against 2.52% for all items, about 1.4 points a year faster. Over the same period the medical-care CPI rose 3.29%/yr.
     - Since 2006 the gap is 1.18 points; since 2015 it is 0.69.
     - The producer price index (PPI) for nursing care facilities, which includes Medicare/Medicaid rates, rose 3.33%/yr in 1997-2025 (0.81 points above CPI).
     - Home-care prices are ambiguous:
       - The PPI for home health agencies rose **less** than CPI: 1.81%/yr in 1997-2025. Medicare sets much of that pricing.
       - The small, volatile CPI for home health care rose 4.31%/yr in 2015-2025, including a jump in late 2025.
   - Latest 12 months (Aug 2026): nursing-home CPI +4.6% vs all-items +3.4%. [`output/bls_ltc_price_growth.csv`]
   - **Against retirees' incomes, nursing-home prices have not run away.** Census median household income for householders 65+ grew 3.84%/yr in 1997-2025 (nominal), about the same as the nursing-home CPI (3.91%). Since 2006 income grew faster (4.10% vs 3.67%). Part of the income growth probably reflects older people working more and drawing more from retirement accounts (inferred; see S13). CPS also has breaks in 2013/14 and 2019. [`output/nursing_home_prices_vs_65plus_income.csv`]

7. **Prices today (private survey): a year in a nursing-home private room is about 2.2 times the median 65+ household's income.**
   - CareScout (Genworth) Cost of Care Survey 2025 national medians:

     | Service | 2025 annual cost | Change from 2024 |
     |---|---|---|
     | Nursing home, private room | **$129,575** | +1% |
     | Nursing home, semi-private room | $114,975 | +3% |
     | Assisted living | $74,400 | +5% |
     | Non-medical home care, 44 hrs/wk | $80,080 | +3% |

   - Against the 2025 Census median household income for 65+ householders ($59,680), these are:
     - **217%** for a private room
     - 193% for a semi-private room
     - **125%** for assisted living
     - 134% for home care
   - For 75+ households (median $50,880) a private room is 255% of income.
   - This is private industry data from a subsidiary of an LTC insurer. Its 2004-2024 history could not be retrieved. [`output/carescout_2025_costs_vs_income.csv`]

8. **Private LTC insurance shrank and never became a major payer.**
   - Annual sales of individual policies:
     - Rose from 380,000 (1990) to **755,000 (2002)**.
     - Then fell about **9% a year in 2003-2009**, so fewer were sold in 2009 than in 1990.
   - Insurers selling policies fell from 102 (2002) to fewer than 15 by 2012. The main reasons were mispriced interest rates and lapse rates (ASPE/LifePlans 2013).
   - About 6.58 million people held a policy in 2018, less than 6% of adults 50+ (NAIC data cited by ASPE 2022). Milliman's tabulation of NAIC experience reports gives about **5.8 million in 2024**, falling 1-3% a year. Terminations exceed new issues by about 127,000 a year.
   - Claims are still growing as policyholders age: about $17B in 2024, up more than 80% since 2015. Average claim size went from about $110,000 to $180,000.
   - Insurance is 5% of expected lifetime LTSS cost (ASPE 2022) and 8.8% of nursing-home spending (NHE 2024). The NHE figure includes ordinary health insurance.
   - [`output/private_ltc_insurance_market.csv`]

**Why it matters for the withdrawal report.** About 4% of retirees face very long paid care (5+ years: 4.4% in ASPE 2022). About 6% face out-of-pocket bills above $250k, rising to 10% in the top income quintile, which holds most IRA/DC balances. This is the main tail risk behind the drawdown rates in S4-S10. Most people will need some help, but for the median household the bill is modest because family care and Medicaid absorb much of it (inferred from findings 2-3).

## Method
- **NHE:** built from the CMS `NHE2024.csv`, which covers type of service by source of funds, 1960-2024.
  - Payer groups: out of pocket; Medicaid (CHIP added, under 0.01%); Medicare; private health insurance; VA+DoD; other third party.
  - The 2024 nursing-facility total is checked against CMS's published Table 15 ($219.9B).
  - The "nursing + home health" combined file is a rough proxy for paid LTC (see caveats).
- **BLS:** annual averages (period M13) from the download.bls.gov flat files.
  - CPI-U series: `CUUR0000SA0`, `SAM`, `SEMD02` (Dec 1996=100), `SEMD03` (Dec 2005=100).
  - PPI series: `PCU623110623110` and the payer splits `...1`/`...3`, and `PCU621610621610`.
  - Growth is compound annual over 1997-2025, 2006-2025 and 2015-2025 (the first full year of each index).
  - October 2025 CPI was not collected; BLS's 2025 annual average is used as published.
- **Census:** nursing-home shares come from the decennial briefs. Median household income by age of householder comes from historical table H-10 (current dollars).
- **Transcribed figures:** ASPE, Census, NCHS, CareScout, ASPE/LifePlans and Milliman figures are typed into `scripts/build.py`. The script checks each one against the source's text extract and stops if any is missing.

## Sources
- ASPE, Johnson R & Dey J, *Long-Term Services and Supports for Older Americans: Risks and Financing, 2022* (Research Brief, revised Aug 2022): https://www.aspe.hhs.gov/sites/default/files/documents/08b8b7825f7bc12d2c79261fd7641c88/ltss-risks-financing-2022.pdf (Tables 1-10)
- ASPE, Favreault M & Dey J, *Long-Term Services and Supports for Older Americans: Risks and Financing* (Issue Brief, revised Feb 2016): https://aspe.hhs.gov/sites/default/files/private/pdf/106211/ElderLTCrb-rev.pdf
- ASPE, Johnson R, *What Is the Lifetime Risk of Needing and Receiving Long-Term Services and Supports?* (Research Brief, Apr 2019): https://aspe.hhs.gov/sites/default/files/migrated_legacy_files//188046/LifetimeRisk.pdf
- ASPE, Favreault M & Johnson R, *Projections of Risk of Needing LTSS at Ages 65 and Older* (Jan 2021, technical report behind the 2022 brief; saved, not used for figures): https://aspe.hhs.gov/sites/default/files/private/pdf/265136/LTSSRisk.pdf
- CMS Office of the Actuary, National Health Expenditure Accounts 2024: https://www.cms.gov/files/zip/national-health-expenditures-type-service-source-funds-cy-1960-2024.zip, tables https://www.cms.gov/files/zip/nhe-tables.zip, definitions https://www.cms.gov/files/document/definitions-sources-methods.pdf
- BLS CPI and PPI flat files: https://download.bls.gov/pub/time.series/cu/ (`cu.data.1.AllItems`, `cu.data.15.USMedical`) and https://download.bls.gov/pub/time.series/pc/ (`pc.data.51.NursingResidentialCareFacil`, `pc.data.47.AmbulatoryHealthCareServices`)
- Census Bureau: *The 65 Years and Over Population: 2000* (C2KBR/01-10, Table 8): https://www2.census.gov/library/publications/decennial/2000/briefs/c2kbr01-10.pdf; *65+ in the United States: 2010* (P23-212, p. 49): https://www.census.gov/content/dam/Census/library/publications/2014/demo/p23-212.pdf; *The Older Population: 2020* (C2020BR-07, p. 9): https://www2.census.gov/library/publications/decennial/2020/census-briefs/c2020br-07.pdf; Historical Income Table H-10: https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h10ar.xlsx
- NCHS: *Overview of Post-acute and Long-term Care Providers and Services Users in the United States, 2020* (NHSR 208, Table 2): https://www.cdc.gov/nchs/data/nhsr/nhsr208.pdf; *Long-Term Care Services in the United States: 2013 Overview* (Series 3 No. 37): https://www.cdc.gov/nchs/data/series/sr_03/sr03_037.pdf; *Long-Term Care Providers and Services Users in the United States* 2013-2014 (Series 3 No. 38): https://www.cdc.gov/nchs/data/series/sr_03/sr03_038.pdf
- ASPE, Cohen M (LifePlans), *Exiting the Market: Understanding the Factors Behind Carriers' Decision to Leave the Long-Term Care Insurance Market* (Jul 2013): https://aspe.hhs.gov/sites/default/files/migrated_legacy_files//138401/MrktExit.pdf
- **Private:** CareScout (Genworth subsidiary), Cost of Care Survey 2025: https://www.carescout.com/cost-of-care, data tables https://assets.carescout.com/x/8fcb50422f/282102.pdf, methodology https://assets.carescout.com/x/e3933bfcf1/131168.pdf
- **Industry:** Milliman (Smetek, Gunnlaugsson, Giese, Clemens), *The long-term care insurance industry through 2024* (31 Dec 2025), from NAIC Experience Reporting Forms: https://www.milliman.com/en/insight/ltci-2024-statistics-experience-reporting-forms

## Caveats
- **Definitions drive the risk figures.** The figures range from 52% to 70% depending on the need threshold (HIPAA trigger vs any ADL/IADL limit) and on whether the estimate is a projection (DYNASIM) or historical HRS data. ASPE 2016 and 2022 differ mainly in method; don't present the change as a trend. ASPE 2022 projections predate COVID effects.
- **NHE covers all ages and mixes post-acute and long-term care.**
  - "Nursing care facilities & CCRCs" includes Medicare skilled-nursing post-acute stays and residents under 65.
  - It excludes hospital-based nursing units and **standalone assisted living (NAICS 623312 is out of scope)**.
  - Home health covers freestanding agencies only (incl. skilled and hospice services).
  - Privately hired home aides are largely missing.
  - So NHE understates out-of-pocket LTC spending and overstates Medicare's role in long-term care proper.
  - Medicaid HCBS waivers sit inside "other health, residential & personal care" together with ambulance, school and worksite care and ICF/IID facilities, so that category is only an indicator.
  - CRS publishes an LTSS-specific payer split from NHE detail, but congress.gov/crsreports are blocked here, so it was not used.
- **2020 NHE** includes COVID Provider Relief Fund money as "other third party" (16.6% of nursing-home spending). Compare 2019 with 2023-24 instead.
- **Census nursing-home shares:**
  - 1990/2000 count "nursing homes"; 2010/2020 count "nursing facilities/skilled-nursing facilities".
  - The 2020 count is from April 1, 2020 and uses differential privacy.
  - The shares are a point-in-time count of residents, not the lifetime risk of a stay.
  - The 2010 P23-212 also notes another 2.4% of older people in senior housing with support services (AoA 2009); that figure was not used in the series.
- **BLS price indexes:**
  - The nursing-home CPI measures out-of-pocket prices paid by consumers, so mostly private-pay rates. The PPI measures receipts from all payers.
  - The home-health CPI (SEMD03) has a small sample, missing months in 2025 and large jumps. Treat it with caution.
  - Prices don't capture changes in care intensity or quality.
- **Income comparison:** H-10 median household income is pre-tax, nominal, from the CPS ASEC, with breaks in 2013/14 and 2019. The 2026 ASEC uses new population controls. The ratio of the CareScout price to H-10 income mixes a private price survey with a public income survey.
- **CareScout/Genworth** is a private survey run by an LTC insurer's subsidiary: medians from about 16,000 provider responses. The method changed in 2025: homemaker and home-health-aide rates were merged into "non-medical caregiver". The 2024 annual figures in the output are computed as monthly x 12 or hourly x 44 x 52 from the page's 2024 column.
- **Insurance-market figures:**
  - Pre-2012 sales come from AHIP/LifePlans industry surveys reported by ASPE.
  - The 2018 and 2024 policyholder counts come from NAIC filings. 2018 is via ASPE; 2024 is via Milliman, an actuarial consultancy to insurers.
  - The NAIC changed its reporting format in 2020, so pre/post-2020 claim counts are not comparable.
  - Milliman's "about 7% of people 60+" covered uses a simplifying denominator. It is not comparable with ASPE's "under 6% of 50+".
  - Hybrid life/LTC policies are excluded, so the stand-alone decline overstates the fall in total LTC coverage.

## Dropped or not reachable
- NAIC itself (content.naic.org, naic.org): 403. Its LTC experience reports were used only through ASPE and Milliman.
- Census API: it now requires a key (redirects to missing_key). The 2020 DHC national file is 2.3 GB. Published briefs were used instead.
- Genworth/CareScout history 2004-2024: the site's API returns only the current year. No reachable file gave the earlier national medians, so the long-run price trend uses BLS instead.
- CRS IF10343 *Who Pays for LTSS?*: congress.gov is blocked. Its numbers (seen only in a search snippet via everycrsreport.com, a non-government mirror) were dropped.
- The ASPE 2013 Advisory Council slides on the LTC insurance industry are image-only and were not used.
- NCHS 2015-16 overview (Series 3 No. 43): the URL tried returned 404.
- HRS, SSA and GAO are blocked here and were not used. KFF's Medicaid LTSS notes were not needed once NHE was in hand.

## Files
- `scripts/fetch.sh` re-downloads raw files. `scripts/build.py` writes all outputs and prints a summary.
- `output/nhe_ltc_payer_shares_1970_2024.csv`: payer shares, $bn and % of personal health care for nursing facilities, home health, and other HRPC, 1970-2024.
- `output/nhe_nursing_plus_homehealth_payer_shares.csv`: the two combined.
- `output/bls_ltc_price_indexes_annual.csv` and `output/bls_ltc_price_growth.csv`: annual index levels, and cumulative/annual growth vs CPI.
- `output/census_pct_65plus_in_nursing_homes.csv`: 1990-2020 by age.
- `output/aspe_lifetime_ltc_risk.csv`: risk, duration, cost and payer figures from the three ASPE briefs.
- `output/carescout_2025_costs_vs_income.csv` and `output/nursing_home_prices_vs_65plus_income.csv`.
- `output/private_ltc_insurance_market.csv`.
- `raw/`: all source files (PDFs plus their `.txt` extracts, BLS flat files, NHE CSV/tables, H-10, CareScout JSON/page text, Milliman page text). The largest are the Census P23-212 and NCHS Series 3 No. 38 PDFs (12 MB and 6 MB); every other file is under 3 MB.
