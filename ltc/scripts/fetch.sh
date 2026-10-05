#!/usr/bin/env bash
# Re-download every raw file used by build.py into ltc/raw/. Run from anywhere.
# Tested 2026-10-05. Hosts: download.bls.gov, cms.gov, aspe.hhs.gov, census.gov/www2.census.gov,
# cdc.gov, carescout.com (private, Genworth subsidiary), milliman.com (industry actuary).
set -euo pipefail
R="$(cd "$(dirname "$0")/.." && pwd)/raw"
UA="Mozilla/5.0 (research)"
get() { mkdir -p "$(dirname "$R/$2")"; curl -sSL -A "$UA" "$1" -o "$R/$2"; echo "ok $2"; }

# BLS CPI (cu) and PPI (pc) flat files
for f in cu/cu.series cu/cu.data.1.AllItems cu/cu.data.15.USMedical \
         pc/pc.series pc/pc.data.51.NursingResidentialCareFacil pc/pc.data.47.AmbulatoryHealthCareServices; do
  get "https://download.bls.gov/pub/time.series/$f" "bls/$(basename $f)"
done

# CMS National Health Expenditure Accounts (released Dec 2025 / Jan 2026, data through 2024)
get https://www.cms.gov/files/zip/national-health-expenditures-type-service-source-funds-cy-1960-2024.zip nhe/national-health-expenditures-type-service-source-funds-cy-1960-2024.zip
get https://www.cms.gov/files/zip/nhe-tables.zip nhe/nhe-tables.zip
get https://www.cms.gov/files/document/definitions-sources-methods.pdf nhe/definitions-sources-methods.pdf
(cd "$R/nhe" && unzip -o -q national-health-expenditures-type-service-source-funds-cy-1960-2024.zip NHE2024.csv \
  && unzip -o -q nhe-tables.zip "Table 1[345]*")

# ASPE lifetime-risk briefs
get https://www.aspe.hhs.gov/sites/default/files/documents/08b8b7825f7bc12d2c79261fd7641c88/ltss-risks-financing-2022.pdf aspe/johnson_dey_2022_ltss-risks-financing.pdf
get https://aspe.hhs.gov/sites/default/files/private/pdf/106211/ElderLTCrb-rev.pdf aspe/aspe2016_ElderLTCrb-rev.pdf
get https://aspe.hhs.gov/sites/default/files/migrated_legacy_files//188046/LifetimeRisk.pdf aspe/LifetimeRisk_188046.pdf
get https://aspe.hhs.gov/sites/default/files/private/pdf/265136/LTSSRisk.pdf aspe/favreault_johnson_2021_LTSSRisk.pdf

# Census: nursing-home share of 65+ (decennial briefs) and H-10 household income by age
get https://www2.census.gov/library/publications/decennial/2000/briefs/c2kbr01-10.pdf census/c2kbr01-10.pdf
get https://www.census.gov/content/dam/Census/library/publications/2014/demo/p23-212.pdf census/p23-212.pdf
get https://www2.census.gov/library/publications/decennial/2020/census-briefs/c2020br-07.pdf census/c2020br-07.pdf
get https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h10ar.xlsx census/h10ar.xlsx

# NCHS long-term care provider reports
get https://www.cdc.gov/nchs/data/nhsr/nhsr208.pdf nchs/nhsr208.pdf
get https://www.cdc.gov/nchs/data/series/sr_03/sr03_037.pdf nchs/sr03_037.pdf
get https://www.cdc.gov/nchs/data/series/sr_03/sr03_038.pdf nchs/sr03_038.pdf

# Private LTC insurance market (ASPE/LifePlans 2013)
get https://aspe.hhs.gov/sites/default/files/migrated_legacy_files//138401/MrktExit.pdf ltci/aspe_2013_MrktExit.pdf

# CareScout (Genworth) Cost of Care Survey 2025 -- PRIVATE source
get https://assets.carescout.com/x/8fcb50422f/282102.pdf carescout/282102.pdf
get https://assets.carescout.com/x/e3933bfcf1/131168.pdf carescout/131168.pdf
get https://assets.carescout.com/x/5c90319b6a/298701.pdf carescout/298701.pdf
curl -sS -A "$UA" -X POST -H "Content-Type: application/json" -d '{"path":"/national/"}' \
  https://www.carescout.com/cost-of-care/api/cost-of-care -o "$R/carescout/api_national_2025.json"
# The CareScout page text (2024 vs 2025 medians) and the Milliman page text were saved as
# carescout/cost-of-care_page_text_2026-10-05.txt and ltci/milliman_2025_ltci_through_2024_page_text.txt
# (HTML stripped of tags) from https://www.carescout.com/cost-of-care and
# https://www.milliman.com/en/insight/ltci-2024-statistics-experience-reporting-forms

# text versions for the number checks in build.py
for f in $(find "$R" -name '*.pdf'); do pdftotext -layout "$f" "${f%.pdf}.txt" 2>/dev/null; done
