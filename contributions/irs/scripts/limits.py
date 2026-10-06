"""Contribution limits by year (IRA and 401(k)/403(b)/457 elective deferrals), from IRS sources.

Writes output/contribution_limits.csv.
Sources:
  * IRS "COLA increases for dollar limitations on benefits and contributions" page (2023-2026 columns),
    https://www.irs.gov/retirement-plans/cola-increases-for-dollar-limitations-on-benefits-and-contributions
    (snapshot raw/page_cola.html)
  * IRS "Cost-of-Living Adjustments for Retirement Items" prior-years table (PDF linked from that page),
    https://www.irs.gov/pub/foia/ig/tege/cola-table-dci005ma4578824.pdf  (raw/cola_prior_years.pdf), covers 1989, 1991-2025.
Values are transcribed from those tables (code sections 402(g)(1), 414(v)(2)(B)(i), 219(b)(5)(A), 219(b)(5)(B), 408(p)(2)(E)).
Pre-2002 IRA limit ($2,000) is statutory and shown as '----' in the COLA table (not indexed); it is left blank here.
Run: python3 -I limits.py
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'output')

# year: (402g elective deferral, 401k catch-up 50+, IRA limit, IRA catch-up 50+, SIMPLE limit)
L = {
 1989: (7627, None, None, None, None), 1991: (8475, None, None, None, None), 1992: (8728, None, None, None, None), 1993: (8994, None, None, None, None),
 1994: (9240, None, None, None, None), 1995: (9240, None, None, None, None), 1996: (9500, None, None, None, None), 1997: (9500, None, None, None, None),
 1998: (10000, None, None, None, None), 1999: (10000, None, None, None, None), 2000: (10500, None, None, None, None), 2001: (10500, None, None, None, None),
 2002: (11000, 1000, 3000, 500, None), 2003: (12000, 2000, 3000, 500, None), 2004: (13000, 3000, 3000, 500, None), 2005: (14000, 4000, 4000, 500, None),
 2006: (15000, 5000, 4000, 1000, None), 2007: (15500, 5000, 4000, 1000, None), 2008: (15500, 5000, 5000, 1000, None), 2009: (16500, 5500, 5000, 1000, None),
 2010: (16500, 5500, 5000, 1000, None), 2011: (16500, 5500, 5000, 1000, None), 2012: (17000, 5500, 5000, 1000, None), 2013: (17500, 5500, 5500, 1000, None),
 2014: (17500, 5500, 5500, 1000, None), 2015: (18000, 6000, 5500, 1000, 12500), 2016: (18000, 6000, 5500, 1000, 12500), 2017: (18000, 6000, 5500, 1000, 12500),
 2018: (18500, 6000, 5500, 1000, 12500), 2019: (19000, 6000, 6000, 1000, 13000), 2020: (19500, 6500, 6000, 1000, 13500), 2021: (19500, 6500, 6000, 1000, 13500),
 2022: (20500, 6500, 6000, 1000, 14000), 2023: (22500, 7500, 6500, 1000, 15500), 2024: (23000, 7500, 7000, 1000, 16000), 2025: (23500, 7500, 7000, 1000, 16500),
 2026: (24500, 8000, 7500, 1100, 17000),
}

def main():
    rows = []
    for y, (g, cu, ira, icu, simple) in sorted(L.items()):
        src = ('IRS COLA increases page (2023-2026 columns), raw/page_cola.html' if y == 2026 else
               'IRS Cost-of-Living Adjustments for Retirement Items (prior years), https://www.irs.gov/pub/foia/ig/tege/cola-table-dci005ma4578824.pdf')
        note = []
        if y >= 2025: note.append('SECURE 2.0: higher 401(k) catch-up for ages 60-63 from 2025 ($11,250 in 2025-26 per IRS page); not shown.')
        if y == 2026: note.append('IRA catch-up indexed from 2024 law; 2026 = $1,100.')
        if y <= 2001: note.append('IRA limit $2,000 (statutory, not COLA-indexed; shown as ---- in the IRS table), left blank.')
        rows.append(dict(year=y, elective_deferral_402g=g, deferral_catchup_50plus=cu, deferral_max_50plus=(g + cu) if cu else None,
                         ira_limit=ira, ira_catchup_50plus=icu, ira_max_50plus=(ira + icu) if ira else None, simple_limit=simple,
                         source=src + '; IRS page https://www.irs.gov/retirement-plans/cola-increases-for-dollar-limitations-on-benefits-and-contributions',
                         note=' '.join(note)))
    d = pd.DataFrame(rows)
    d.to_csv(os.path.join(OUT, 'contribution_limits.csv'), index=False)
    print(d[['year', 'elective_deferral_402g', 'deferral_catchup_50plus', 'ira_limit', 'ira_catchup_50plus']].to_string(index=False))

if __name__ == '__main__':
    main()
