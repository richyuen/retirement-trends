#!/usr/bin/env bash
# Rebuild all outputs (after scripts/fetch.sh). Order matters.
set -e
D="$(cd "$(dirname "$0")" && pwd)"
cd /tmp
for s in limits f1040_long ira_contributions w2_deferrals combined; do echo "== $s"; python3 -I "$D/$s.py"; done
