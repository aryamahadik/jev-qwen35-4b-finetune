#!/bin/bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock
nice -n 10 grep -rIio -F -f ../meta_src/gproxy/_terms2.txt texts raw --exclude-dir='*ohs*' --exclude='*ohs*' --exclude='*.bz2' | awk -F: '{split($1,a,"/"); print a[1]"/"a[2]" "tolower($NF)}' | sort | uniq -c > ../meta_src/gproxy/gblock_name_where.txt 2>&1
echo done >> ../meta_src/gproxy/gblock_name_where.txt
