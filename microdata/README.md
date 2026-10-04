# Microdata setup
**SCF** (free): https://www.federalreserve.gov/econres/scfindex.htm — download the "Summary Extract Public Data" (Stata/CSV) for each wave (1989-2022; 2025 expected late 2026) and, for withdrawal questions, the full public dataset + codebook. Put files in `microdata/raw/scf/`.
**CPS ASEC**: use IPUMS-CPS (free account): https://cps.ipums.org — select ASEC samples 2010+, variables AGE, SEX, ASECWT, YEAR, and retirement-income variables (e.g. INCRETIR; check the codebook for current names/comparability across 2014 and 2019). Save the extract to `microdata/raw/cps/`.
Verify all URLs/variable names against current documentation; they change.
Weights: SCF summary extract has 5 implicates per household (Y1 = household id, YY1 = original id); WGT is already divided by 5. Pool the 5 implicates for point estimates; use SCF replicate weights / the Fed's sample code for standard errors. CPS: use ASECWT.
