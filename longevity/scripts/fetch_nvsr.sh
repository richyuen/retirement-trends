#!/bin/sh
# Download NCHS "United States Life Tables" spreadsheets (NVSR), Tables 1-18, data years 2018-2024.
# 69-12=2018, 70-19=2019, 71-01=2020, 72-12=2021, 74-02=2022, 74-06=2023, 75-05=2024
cd "$(dirname "$0")/../raw/nvsr"
for d in 69-12 70-19 71-01 72-12 74-02 74-06 75-05; do
  mkdir -p $d
  for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18; do
    [ -s $d/T$i.xlsx ] && continue
    for c in Table table; do
      curl -s -f -m 60 -o $d/T$i.xlsx https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/NVSR/$d/$c$i.xlsx && break
    done
  done
done
