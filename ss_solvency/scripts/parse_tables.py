"""Parse multi-year tables from the 2026 OASDI Trustees Report text
(raw/text/oasdi_2026.txt.gz, made by fetch_reports.sh with pdftotext -layout).

Tables (2026 report, House Doc 119-163):
  VI.B1  Long-range OASDI actuarial balances and combined-fund depletion years,
         reports 1982-2026 (printed pp. 182-183)
  IV.B4  Covered workers and beneficiaries, 1945-2100 (pp. 69-71)
  IV.B1  Annual income rates, cost rates, balances, % of taxable payroll (pp. 59-61)
  IV.B3  Same as % of GDP (pp. 67-68)
Printed page = PDF page - 8 in this report.
Writes CSVs to output/ and prints a short summary.
"""
import gzip, os, re
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
TXT = os.path.join(ROOT, "raw", "text", "oasdi_2026.txt.gz")
OUT = os.path.join(ROOT, "output")

NUM = r"[-+−]?\d[\d,]*\.?\d*|[-+−]?\.\d+"
ROW = re.compile(r"^\s*(\d{4})\s*[a-z]?\s*(?:\.\s*)+(.*)$")


def lines():
    with gzip.open(TXT, "rt", encoding="utf-8", errors="replace") as f:
        return f.read().splitlines()


def num(tok):
    tok = tok.replace(",", "").replace("−", "-")
    if tok.startswith("d") or tok == "d":
        return 0.0  # footnote d = between -0.005 and 0.005
    if tok in ("e", "—", "-"):
        return None
    tok = re.sub(r"^[a-z]", "", tok)  # e.g. 'd184,666' (footnote letter glued on)
    return float(tok)


def table_block(L, title, stop=r"^\s*[a-z] [A-Z]"):
    """All lines from each occurrence of `title` until the footnotes start."""
    out, on = [], False
    for ln in L:
        if title in ln:
            on = True
            continue
        if on and re.match(stop, ln):
            on = False
        if on:
            out.append(ln)
    return out


def parse_rows(block, ncols, sections=("Historical data", "Intermediate", "Low-cost", "High-cost")):
    rows, sec = [], None
    for ln in block:
        s = ln.strip()
        for name in sections:
            if s.startswith(name):
                sec = name
        m = ROW.match(ln)
        if not m:
            continue
        toks = m.group(2).split()
        if len(toks) < ncols:
            continue
        rows.append([sec, int(m.group(1))] + [num(t) for t in toks[:ncols]])
    return rows


def main():
    L = lines()

    # VI.B1 history of actuarial balance and depletion year
    blk = table_block(L, "Table VI.B1.—Long-Range OASDI Actuarial Balances")
    recs = []
    for ln in blk:
        m = ROW.match(ln)
        if m:
            t = m.group(2).split()
            recs.append(dict(report_year=int(m.group(1)), summarized_income_rate=num(t[0]),
                             summarized_cost_rate=num(t[1]), actuarial_balance=num(t[2]),
                             change_from_previous=None if t[3] == "d" and int(m.group(1)) in (1982,) else num(t[3]),
                             oasdi_depletion_year=None if t[4] == "e" else int(t[4])))
    vib1 = pd.DataFrame(recs).drop_duplicates("report_year")
    vib1.loc[vib1.report_year == 1982, "change_from_previous"] = None
    vib1["note"] = ""
    
    vib1.loc[vib1.oasdi_depletion_year.isna(), "note"] = "reserves positive through 75-year period (footnote e)"
    vib1.loc[vib1.report_year < 1991, "note"] = (vib1.loc[vib1.report_year < 1991, "note"] + "; AB method differs before 1991 (avg-cost to 1987)").str.lstrip("; ")
    vib1["source"] = "2026 OASDI Trustees Report Table VI.B1 (H. Doc. 119-163, pp. 182-183)"
    vib1.to_csv(os.path.join(OUT, "oasdi_history_tableVIB1_1982_2026.csv"), index=False)
    print(f"VI.B1: {len(vib1)} reports {vib1.report_year.min()}-{vib1.report_year.max()}; "
          f"AB 1983 {vib1.set_index('report_year').actuarial_balance[1983]:+.2f}, "
          f"2026 {vib1.set_index('report_year').actuarial_balance[2026]:+.2f}")

    # IV.B4 covered workers and beneficiaries
    blk = table_block(L, "Table IV.B4.—Covered Workers and Beneficiaries")
    rows = parse_rows(blk, 6)
    w = pd.DataFrame(rows, columns=["section", "year", "covered_workers_k", "oasi_benef_k", "di_benef_k",
                                    "oasdi_benef_k", "workers_per_beneficiary", "beneficiaries_per_100_workers"])
    w = w.drop_duplicates(["section", "year"])
    w["source"] = "2026 OASDI Trustees Report Table IV.B4 (pp. 69-71)"
    w.to_csv(os.path.join(OUT, "workers_per_beneficiary_1945_2100.csv"), index=False)
    h = w[w.section == "Historical data"].set_index("year").workers_per_beneficiary
    i = w[w.section == "Intermediate"].set_index("year").workers_per_beneficiary
    print(f"IV.B4: {len(w)} rows; workers/beneficiary 1960 {h[1960]}, 2025 {h[2025]}, "
          f"2035 {i[2035]}, 2100 {i[2100]} (intermediate)")

    # IV.B1 (% of taxable payroll) and IV.B3 (% of GDP)
    for tab, fname, unit in (("Table IV.B1.—Annual Income Rates, Cost Rates", "income_cost_pct_payroll.csv", "% taxable payroll"),
                             ("Table IV.B3.—Annual Income Rates, Cost Rates", "income_cost_pct_gdp.csv", "% GDP")):
        blk = table_block(L, tab, stop=r"^\s*a [A-Z]")
        rows = parse_rows(blk, 9)
        d = pd.DataFrame(rows, columns=["section", "year", "oasi_income", "oasi_cost", "oasi_balance",
                                        "di_income", "di_cost", "di_balance",
                                        "oasdi_income", "oasdi_cost", "oasdi_balance"])
        d = d.drop_duplicates(["section", "year"])
        d["unit"] = unit
        d["source"] = f"2026 OASDI Trustees Report {tab.split('.—')[0]} (" + ("pp. 59-61" if "IV.B1" in tab else "pp. 67-68") + ")"
        d.to_csv(os.path.join(OUT, fname), index=False)
        x = d[d.section.isin(["Historical data", "Intermediate"])].set_index("year")
        print(f"{tab.split('.—')[0]} ({unit}): {len(d)} rows; OASDI cost 2000 {x.oasdi_cost[2000]}, "
              f"2025 {x.oasdi_cost[2025]}, 2035 {x.oasdi_cost[2035]}, 2085 {x.oasdi_cost[2085]}, "
              f"2100 {x.oasdi_cost[2100]}; income 2026 {x.oasdi_income[2026]}")


if __name__ == "__main__":
    main()
