"""Per-wave SCF variable maps for current-job pension plans and IRA contributions.

Verified against the Fed codebooks (contributions/scf/raw/codebk89..2019.txt and
scf/raw/codebk2004/2010/2016/2022.txt). See notes.md "Variables by wave".

Each current-job plan "slot" is described by a dict of X-variable numbers.
person: 'r' = respondent (survey reference person), 's' = spouse/partner.
"""
from pathlib import Path

PROJ = Path(__file__).resolve().parents[3]          # .../retirement-withdrawals
OLDRAW = PROJ / "scf" / "raw"                        # shared raw folder (2004-2022 full files, summaries)
SCRATCH = Path("/tmp/scfraw/x")                      # 1989-2001 full files + replicate weights (downloaded)

WAVES = [1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013, 2016, 2019, 2022]


def full_path(year):
    yy = str(year)[2:]
    if year >= 2004:
        return OLDRAW / f"p{yy}i6.dta"
    return SCRATCH / ("p92i4.dta" if year == 1992 else f"p{yy}i6.dta")


def rw_path(year):
    yy = str(year)[2:]
    if year >= 2004:
        return OLDRAW / f"p{yy}_rw1.dta"
    return SCRATCH / ("scf2001rw1s.dta" if year == 2001 else f"p{yy}_rw1.dta")


def summary_path(year):
    return OLDRAW / f"rscfp{year}.dta"


def slots(year):
    """List of plan slots for the current-job pension grid."""
    out = []
    if year <= 2001:
        # 1989-2001: up to 3 plans per person (R: 4200/4300/4400; S: 4800/4900/5000).
        # X4n03 type: 1 formula (DB), 2 account (DC), 3 both.
        # Account plans (type 2): employee contrib X4n22 (1 yes/5 no), % X4n23, $ X4n24, freq X4n25;
        #   employer contrib X4n18, % X4n19, $ X4n20, freq X4n21; balance X4n26.
        # Combination plans (type 3) and formula plans (type 1): employee contrib X4n05, % X4n06, $ X4n07, freq X4n08;
        #   account part balance X4n04 (type 3 only); no employer-contribution questions.
        for person, bases in (("r", (4200, 4300, 4400)), ("s", (4800, 4900, 5000))):
            for b in bases:
                out.append(dict(person=person, era="A", type=b + 3,
                                ee=b + 22, ee_pct=b + 23, ee_amt=b + 24, ee_frq=b + 25,
                                er=b + 18, er_pct=b + 19, er_amt=b + 20, er_frq=b + 21, bal=b + 26,
                                ee_c=b + 5, ee_c_pct=b + 6, ee_c_amt=b + 7, ee_c_frq=b + 8, bal_c=b + 4))
        return out
    if year <= 2007:
        bases = {"r": (11000, 11100, 11200), "s": (11300, 11400, 11500)}   # 3 plans per person
    else:
        bases = {"r": (11000, 11100), "s": (11300, 11400)}                 # 2 plans per person from 2010
    for person, bs in bases.items():
        for b in bs:
            out.append(dict(person=person, era="B" if year <= 2007 else "C",
                            t1=b, t2=b + 1, bal=b + 32,
                            ee=b + 40, ee_pct=b + 41, ee_amt=b + 42, ee_frq=b + 43,
                            ee_ly_pct=b + 44, ee_ly_amt=b + 45, ee_ly_frq=b + 46,
                            er=b + 47, er_how=b + 48, er_pct=b + 49, er_match=b + 50, er_amt=b + 51, er_frq=b + 52,
                            er_ly_how=b + 53, er_ly_pct=b + 54, er_ly_match=b + 55, er_ly_amt=b + 56, er_ly_frq=b + 57))
    return out


# person-level work/wage variables (same numbers in every wave 1989-2022)
PERSON = {"r": dict(age=14, work=4105, selfemp=4106, wage=4112, wfrq=4113, hrs=4110, wks=4111),
          "s": dict(age=19, work=4705, selfemp=4706, wage=4712, wfrq=4713, hrs=4710, wks=4711)}

# offered-but-not-included plans (1995+): eligible X4137/X4737 (1 yes); plan kinds offered X6708-X6712 (R),
# X6713-X6717 (S): thrift, 401(k)/403(b)/SRA, profit sharing, tax-deferred annuity (1 = checked), other (coded).
OFFER = {"r": dict(elig=4137, kinds=[6708, 6709, 6710, 6711], other=6712),
         "s": dict(elig=4737, kinds=[6713, 6714, 6715, 6716], other=6717)}
OFFER_OTHER_ACCT = [7, 9, 10, 11, 13, 16]   # ESOP, SEP/SIMPLE, DC/TIAA-CREF, money purchase, other salary reduction, other account
OFFER_FROM = 1995

# IRA contributions (2016, 2019, 2022 only): did R / spouse / other family members contribute in prior calendar year,
# and total amount.  Not asked in 1989-2013 (checked codebooks 1989, 1992, 1995, 1998, 2001, 2004, 2007, 2010, 2013).
IRA_CONTRIB = dict(yes=[6791, 6793, 6795], amt=[6792, 6794, 6796])
IRA_WAVES = [2016, 2019, 2022]

# annualisation factors for SCF frequency codes (1 day, 2 week, 3 biweekly, 4 month, 5 quarter, 6 year,
# 8 lump sum, 11 twice a year, 12 every two months, 31 twice a month). Hour (18) handled with hours x weeks.
FREQ = {1: 260, 2: 52, 3: 26, 4: 12, 5: 4, 6: 1, 8: 1, 11: 2, 12: 6, 31: 24}
