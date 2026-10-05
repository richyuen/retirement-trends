#!/bin/sh
# Re-download the raw sources into working_longer/raw/. The BLS AllData file (~390 MB) is not kept;
# build_bls.py --refresh downloads it to /tmp and keeps only the 89 series used (raw/ln_subset.tsv).
set -e
cd "$(dirname "$0")/../raw"
UA="Mozilla/5.0 (research; ${BLS_CONTACT_EMAIL:-})"  # BLS asks for a contact email; set it locally
for f in ln.series ln.ages ln.sexs ln.lfst ln.periodicity ln.footnote ln.wkst ln.txt ln.pcts; do
  curl -sS -A "$UA" -o "$f" "https://download.bls.gov/pub/time.series/ln/$f"
done
mkdir -p bls_projections crr
curl -sS -A "$UA" -o bls_projections/table_3-3_lfpr_2005_2015_2025_2035.htm \
  https://www.bls.gov/emp/tables/civilian-labor-force-participation-rate.htm
curl -sS -A "$UA" -o crr/avg_ret_age_2025-11.pdf https://crr.bc.edu/wp-content/uploads/2025/11/Average-retirement-age.pdf
curl -sS -A "$UA" -o crr/avg_ret_age_2025-03.pdf https://crr.bc.edu/wp-content/uploads/2025/03/Average-retirement-age.pdf
curl -sS -A "$UA" -o crr/IB_25-8.pdf  https://crr.bc.edu/wp-content/uploads/2025/04/IB_25-8.pdf
curl -sS -A "$UA" -o crr/IB_25-10.pdf https://crr.bc.edu/wp-content/uploads/2025/05/IB_25-10.pdf
curl -sS -A "$UA" -o crr/IB_21-9.pdf  https://crr.bc.edu/wp-content/uploads/2021/05/IB_21-9.pdf
curl -sS -A "$UA" -o crr/IB_15-8.pdf  https://crr.bc.edu/wp-content/uploads/2015/05/IB_15-8.pdf
curl -sS -A "$UA" -o crr/crr_blog_working_longer_claiming_2025-07.pdf \
  "https://crr.bc.edu/wp-content/uploads/2025/07/People-Are-Working-Longer-But-Are-They-Claiming-Social-Security-Later_-%E2%80%93-Center-for-Retirement-Research.pdf"
for f in crr/*.pdf; do pdftotext -layout "$f" "${f%.pdf}.txt"; done
# 2026 Trustees Report (77 MB, not kept): excerpts in trustees/tr2026_excerpts.txt
# https://www.govinfo.gov/content/pkg/CDOC-119hdoc163/pdf/CDOC-119hdoc163.pdf
