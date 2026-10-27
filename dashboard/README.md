# Retirement Trends Dashboard

Live: https://claude.ai/artifact/VmDdCGVfexjmJhADyspW3W (Dashboard artifact type, separate from the report).

16 headline indicators, grouped by the report's parts, each with latest value, a base-year comparison, a trend chart, source note and a link to its report section. Values are the report's own chart data (`CH` in report/parts/30-script.html, v17), so they match the report.

Rebuild after a report version changes:
1. `python dashboard/build.py` (reads CH, writes data/*.json and marks.json; picks latest/base cells)
2. Re-upload any changed data/*.json as assets to the dashboard and update blobs.json
3. `python dashboard/page.py` (writes index.html and store/ documents), then write store/ docs to the dashboard's store.

Conventions kept: CPS income shares 1997-2013 and 2016-2025 are drawn as separate segments (no change computed across the break); DC participation is BLS DC-only (not the 52-53% all-plans rate); NRRI original and v2.0 never joined; IRS rollover ratio and SPM lines break where the report breaks them.
