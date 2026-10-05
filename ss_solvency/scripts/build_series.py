"""Build the report-by-report solvency series and verify every hand-extracted value.

Inputs
  raw/curated_report_values.csv  one row per value read from a Trustees Report:
      report_year, program (OASI/DI/OASDI/HI), measure, value, text_file, quote, note
      `quote` is a verbatim snippet from raw/text/<text_file>; parts separated by
      " ... " must appear in order within 400 characters. The value must appear in
      the quote (for OCR'd fractions, see `note`).
  output/oasdi_history_tableVIB1_1982_2026.csv  (scripts/parse_tables.py)
  ../spending/cps_income/output/*.csv           (read only; CPS ASEC income shares)

Outputs (output/)
  depletion_by_report.csv     wide table, one row per report year 1982-2026
  hi_depletion_by_report.csv  Medicare HI depletion year by report
  cut_implications.csv        what the payable-benefit shortfall means as % of income
Prints a verification summary and headline numbers.
"""
import gzip, os, re, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
TEXT = os.path.join(ROOT, "raw", "text")
OUT = os.path.join(ROOT, "output")
CPS = os.path.join(ROOT, "..", "spending", "cps_income", "output")

_cache = {}


def norm(s):
    s = s.replace("’", "'").replace("—", "-").replace("–", "-").replace("−", "-")
    s = re.sub(r"-\s*\n\s*", "", s)                # re-join hyphenated line breaks
    s = re.sub(r"(\s*\.){2,}", " ", s)             # dot leaders in tables
    s = re.sub(r"\s+", " ", s)
    return s.lower()


def text(fname):
    if fname not in _cache:
        with gzip.open(os.path.join(TEXT, fname), "rt", encoding="utf-8", errors="replace") as f:
            _cache[fname] = norm(f.read())
    return _cache[fname]


def found(fname, quote):
    t = text(fname)
    parts = [norm(p).strip() for p in quote.split(" ... ")]
    for m in re.finditer(re.escape(parts[0]), t):
        pos, ok = m.end(), True
        for p in parts[1:]:
            j = t.find(p, pos)
            if j < 0 or j - pos > 400:
                ok = False
                break
            pos = j + len(p)
        if ok:
            return True
    return False


def verify(cur):
    bad = []
    for r in cur.itertuples():
        ok = found(r.text_file, r.quote)
        v = str(r.value)
        v = v[:-2] if v.endswith(".0") else v
        in_quote = v.lstrip("-") in norm(r.quote) or "ocr" in str(r.note).lower() or v == "none"
        if not (ok and in_quote):
            bad.append((r.report_year, r.program, r.measure, r.value, ok, in_quote))
    print(f"verified {len(cur) - len(bad)}/{len(cur)} curated values against report text")
    for b in bad:
        print("  FAILED", b)
    return not bad


def main():
    cur = pd.read_csv(os.path.join(ROOT, "raw", "curated_report_values.csv"), dtype={"value": str})
    ok = verify(cur)

    vib1 = pd.read_csv(os.path.join(OUT, "oasdi_history_tableVIB1_1982_2026.csv"))
    CORE = ["depletion_year", "payable_pct_at_depletion", "payable_pct_end", "actuarial_balance"]
    oas = cur[(cur.program != "HI") & cur.measure.isin(CORE)].copy()
    oas["col"] = oas.program.str.lower() + "_" + oas.measure
    wide = oas.pivot_table(index="report_year", columns="col", values="value", aggfunc="first")
    v = vib1[["report_year", "actuarial_balance", "oasdi_depletion_year", "summarized_income_rate",
              "summarized_cost_rate"]].rename(columns={"oasdi_depletion_year": "oasdi_depletion_year_tableVIB1",
                                                       "actuarial_balance": "oasdi_actuarial_balance_tableVIB1"})
    wide = v.merge(wide, left_on="report_year", right_index=True, how="left")

    # cross-check: combined depletion year stated in each report vs 2026 Table VI.B1
    if "oasdi_depletion_year" in wide:
        chk = wide.dropna(subset=["oasdi_depletion_year"])
        diff = chk[chk.oasdi_depletion_year.astype(float) != chk.oasdi_depletion_year_tableVIB1]
        print(f"combined depletion year: own report vs 2026 Table VI.B1 agree in "
              f"{len(chk) - len(diff)}/{len(chk)} reports" + ("" if diff.empty else f"; differ: {diff.report_year.tolist()}"))
    if "oasdi_actuarial_balance" in wide:
        chk = wide.dropna(subset=["oasdi_actuarial_balance"])
        diff = chk[(chk.oasdi_actuarial_balance.astype(float) - chk.oasdi_actuarial_balance_tableVIB1).abs() > 0.005]
        print(f"actuarial balance: own report vs Table VI.B1 agree in {len(chk) - len(diff)}/{len(chk)}"
              + ("" if diff.empty else f"; differ: {diff[['report_year','oasdi_actuarial_balance','oasdi_actuarial_balance_tableVIB1']].values.tolist()}"))
    wide["years_from_report_to_oasdi_depletion"] = wide.oasdi_depletion_year_tableVIB1 - wide.report_year
    wide.to_csv(os.path.join(OUT, "depletion_by_report.csv"), index=False)

    hi = cur[(cur.program == "HI") & cur.measure.isin(CORE)].pivot_table(index="report_year", columns="measure", values="value", aggfunc="first")
    hi.reset_index().to_csv(os.path.join(OUT, "hi_depletion_by_report.csv"), index=False)

    # Headlines
    w = wide.set_index("report_year")
    print("OASDI combined depletion year by report (Table VI.B1): " +
          ", ".join(f"{y}:{int(v) if v == v else 'none'}" for y, v in w.oasdi_depletion_year_tableVIB1.items()
                    if y in (1983, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025, 2026)))
    print(f"years of runway: 1985 {w.years_from_report_to_oasdi_depletion[1985]:.0f}, 2000 "
          f"{w.years_from_report_to_oasdi_depletion[2000]:.0f}, 2026 {w.years_from_report_to_oasdi_depletion[2026]:.0f}")
    rec = w.loc[2012:2026, "oasdi_depletion_year_tableVIB1"]
    print(f"reports 2012-2026: combined depletion year always {rec.min():.0f}-{rec.max():.0f}; "
          f"AB 2012 {w.oasdi_actuarial_balance_tableVIB1[2012]:+.2f} -> 2026 {w.oasdi_actuarial_balance_tableVIB1[2026]:+.2f}")
    if "hi" in str(hi.columns).lower() or not hi.empty:
        print("HI depletion year by report: " + ", ".join(f"{y}:{v}" for y, v in hi["depletion_year"].dropna().items()))

    # What the shortfall means for retirees' income (static, mechanical)
    share = pd.read_csv(os.path.join(CPS, "income_share_65plus_wide.csv"))
    ss_share = float(share[(share.asec_year == 2026) & (share.file_label == "production")].social_security.iloc[0])
    rel = pd.read_csv(os.path.join(CPS, "ss_reliance_wide.csv"))
    r = rel[(rel.asec_year == 2026) & (rel.file_label == "production")].iloc[0]
    pay26 = cur[(cur.report_year == 2026) & (cur.measure.isin(["payable_pct_at_depletion", "payable_pct_end"]))]
    p = {(a, b): float(v) for a, b, v in zip(pay26.program, pay26.measure, pay26.value)}
    scen = [("OASI reserves depleted (2032): OASI payable", 100 - p[("OASI", "payable_pct_at_depletion")]),
            ("Combined OASDI depleted (2034): payable", 100 - p[("OASDI", "payable_pct_at_depletion")]),
            ("Combined OASDI, 2100: payable", 100 - p[("OASDI", "payable_pct_end")]),
            ("Immediate 75-year fix, all beneficiaries from 2026", 25.2)]
    groups = [("All persons 65+, aggregate income (CPS ASEC 2026, SS share of income)", ss_share, None),
              ("Aged units with SS >= 50% of income (at threshold; 58.3% of beneficiary units, CPS)", 50.0,
               r.aged_unit__ss_reliance_ge50_pct_of_beneficiaries),
              ("Aged units with SS >= 90% of income (at threshold; 31.9% of beneficiary units, CPS)", 90.0,
               r.aged_unit__ss_reliance_ge90_pct_of_beneficiaries),
              ("Aged units with SS = 100% of income (19.7% of beneficiary units, CPS)", 100.0,
               r.aged_unit__ss_reliance_100_pct_of_beneficiaries)]
    rows = []
    for sname, cut in scen:
        for gname, sh, pct_units in groups:
            rows.append(dict(scenario=sname, benefit_cut_pct=round(cut, 1), group=gname,
                             ss_share_of_income_pct=round(sh, 1),
                             pct_of_beneficiary_units_in_group=None if pct_units is None else round(float(pct_units), 1),
                             income_loss_pct=round(cut * sh / 100, 1)))
    ci = pd.DataFrame(rows)
    ci.to_csv(os.path.join(OUT, "cut_implications.csv"), index=False)
    print(f"SS share of 65+ income (CPS ASEC 2026, income 2025): {ss_share:.1f}%")
    for sname, cut in scen[:2]:
        sub = ci[ci.scenario == sname]
        print(f"  {sname} -> cut {cut:.0f}%: income loss " +
              ", ".join(f"{g.split('(')[0].strip()} {l:.1f}%" for g, l in zip(sub.group, sub.income_loss_pct)))
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
