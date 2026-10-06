"""Print an Excel sheet compactly: row index then non-null cells (col:value). Usage: python3 -I peek.py file [sheet] [maxrows] [width]"""
import sys, pandas as pd
f = sys.argv[1]; sh = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else 0
n = int(sys.argv[3]) if len(sys.argv) > 3 else 80; w = int(sys.argv[4]) if len(sys.argv) > 4 else 40
try: sh = int(sh)
except ValueError: pass
df = pd.read_excel(f, sheet_name=sh, header=None)
for i in range(min(n, len(df))):
    cells = [f"{j}:{str(v).replace(chr(10),' ')[:w]}" for j, v in enumerate(df.iloc[i]) if not pd.isna(v)]
    if cells: print(i, ' | '.join(cells))
