#!/bin/sh
# Re-run the whole SCF 60-64 analysis (about 10 minutes). Cache of the built file goes to $SCF6064_CACHE
# (default ~/.cache/scf_6064, outside the shared folder).
set -e
cd "$(dirname "$0")"
python3 a_descriptives.py
python3 b_subgroups.py
python3 c_decomposition.py
