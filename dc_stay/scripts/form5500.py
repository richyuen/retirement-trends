"""DOL Form 5500 (Private Pension Plan Bulletin Abstracts, participant-status table) ->
private-sector DC plan participants by status, 1999-2023.

Inputs: raw/abstracts/absYYYY.pdf (dol.gov .../private-pension-plan-bulletins-abstract-YYYY.pdf), converted with
`pdftotext -layout`. In each abstract's "Number of Participants in Pension Plans by type of plan and type of
participant" table, the third number in a row is "Total plans, defined contribution".
Output: output/form5500_dc_participant_status.csv (thousands of participants; double counts people in >1 plan)
"""
import re, subprocess, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABS, OUT = ROOT / "raw" / "abstracts", ROOT / "output"
OUT.mkdir(exist_ok=True)
NUM = re.compile(r"\d{1,3}(?:,\d{3})+|\d+")


def nums(line):
    return [int(x.replace(",", "")) for x in NUM.findall(line)]


def row_after(lines, i, k=4):
    """First line at or after i whose numbers look like a table row (>=3 big numbers)."""
    for j in range(i, i + k):
        n = [x for x in nums(lines[j]) if x >= 100]
        if len(n) >= 3:
            return n
    return None


rows = []
for y in range(1999, 2024):
    pdf, txt = ABS / f"abs{y}.pdf", ABS / f"abs{y}.txt"
    if not txt.exists():
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)
    L = txt.read_text(errors="ignore").splitlines()
    rec = {"year": y}
    for i, l in enumerate(L):
        s = l.strip().lower()
        if s.startswith("retired or separated") and "receiving" in " ".join(L[i:i + 3]).lower() and "receiving" not in rec:
            r = row_after(L, i)
            if r: rec["receiving"] = r[2]
        if (s.startswith("separated participants with") or s.startswith("other retired or separated")) and "sep_vested" not in rec:
            r = row_after(L, i)
            if r: rec["sep_vested"] = r[2]
        if s.startswith("total participants") and "sep_vested" in rec and "total" not in rec:
            r = row_after(L, i, 1)
            if r: rec["total"] = r[2]
        if s.startswith("active participants") and "active" not in rec:
            r = row_after(L, i, 2)
            if r and r[0] > 10000: rec["active"] = r[2]
    rows.append(rec)


# derived shares; breaks: active-participant definition revised in 2005 (2004r), Form 5500-SF filers counted
# all participants as active in 2009-2013 (separated understated), SF separated split imputed from 2014.
import pandas as pd
d = pd.DataFrame(rows)
d["separated_per100_active"] = 100 * d.sep_vested / d.active
d["separated_pct_of_total"] = 100 * d.sep_vested / d.total
d["inactive_incl_receiving_pct_of_total"] = 100 * (d.sep_vested + d.receiving) / d.total
d["era"] = pd.cut(d.year, [1998, 2004, 2008, 2013, 2023], labels=["1999-2004 old active def", "2005-2008", "2009-2013 SF break", "2014-2023"])
d.to_csv(OUT / "form5500_dc_participant_status.csv", index=False, float_format="%.1f")
print(d.round(1).to_string())
