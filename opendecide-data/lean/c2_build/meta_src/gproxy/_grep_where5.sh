#!/bin/bash
cd /Users/aryamahadik/Documents/jev/opendecide-data/lean
T=c2_build/meta_src/gproxy/_terms5.txt
OUT=c2_build/meta_src/gproxy/trainside_name_counts5.txt
: > $OUT
for blk in c2_build/gblock/texts c2_build/gblock/raw data/c2_md_parts data/c2_parts; do
  nice -n 10 grep -rIio -F -f $T $blk --exclude-dir='*ohs*' --exclude='*ohs*' --exclude='*.bz2' 2>/dev/null | awk -F: -v b=$blk '{print b" "tolower($NF)}' | sort | uniq -c >> $OUT
done
echo done >> $OUT
