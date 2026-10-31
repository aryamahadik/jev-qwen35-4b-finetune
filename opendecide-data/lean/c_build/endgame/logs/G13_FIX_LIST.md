# G13 fix list after the 7 Oct batch (counts only; our own files). Fix at the generator, then rebuild + re-run gates + G13.

## Binding seed-literal hits (file:line, hit count)

- **packs** seeds_clean=False binding_lines=158: `c_src/packs/packs-1/build_packs.py#52` (101), `c_src/packs/packs-1/packs.jsonl#12948` (50), `c_src/packs/packs-1/packs.jsonl#13077` (50), `c_src/packs/packs-1/packs.jsonl#21367` (83), `c_src/packs/packs-2/build_packs.py#116` (491), `c_src/packs/packs-2/build_packs.py#117` (493), `c_src/packs/packs-2/build_packs.py#32` (806), `c_src/packs/packs-2/packs.jsonl#10046` (12), `c_src/packs/packs-2/packs.jsonl#10763` (13), `c_src/packs/packs-2/packs.jsonl#10865` (13), `c_src/packs/packs-2/packs.jsonl#11557` (14), `c_src/packs/packs-2/packs.jsonl#11686` (14) ...
- **formats** seeds_clean=False binding_lines=1000: `c_src/formats/formats-1/build_pool.py#857` (54), `c_src/formats/formats-1/data/registers.jsonl#10` (2), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1263` (43), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1273` (43), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1283` (43), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1302` (44), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1310` (44), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1324` (44), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1336` (45), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1344` (45), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1354` (45), `c_src/formats/formats-2/codebooks/codebooks.jsonl#1371` (46) ...
- **F3** seeds_clean=True binding_lines=3: `c_src/F3/gen/f3common.py#32` (128), `c_src/F3/gen/f3common.py#33` (129), `c_src/F3/gen/registry.py#8` (114)
- **F4** seeds_clean=False binding_lines=2: `c_src/F4/gen/f4lex.py#151` (241), `c_src/F4/gen/packs_f4.py#29` (96)
- **F5** seeds_clean=True binding_lines=0: 
- **F7** seeds_clean=True binding_lines=1: `c_src/F7/gen/f7parse.py#1` (36)
- **F9** seeds_clean=True binding_lines=0: 
- **F11** seeds_clean=False binding_lines=2: `c_src/F11/gen/lex.py#227` (68), `c_src/F11/gen/lex.py#29` (29)

## Template phrases behind the unit drops (5-grams in >50% of dropped rows, <10% of kept rows)

- **F3** dropped 1369 / kept 7692: 'and receiver 'to' is the' (58% vs 0%); 'share one entry number sequence' (58% vs 0%); 'and take effect in entry' (58% vs 0%); 'take effect in entry number' (58% vs 0%); 'sender and receiver 'to' is' (58% vs 0%); 'number sequence 'from' and 'to'' (58% vs 0%); 'entry a void or correction' (58% vs 0%); 'change but in a creation' (58% vs 0%)
- **F4** dropped 1676 / kept 3724: 
- **F5** dropped 2957 / kept 2295: 'but also b means both' (95% vs 0%); 'a and b are true' (95% vs 0%); 'b means both a and' (95% vs 0%); 'both a and b are' (95% vs 0%); 'means both a and b' (95% vs 0%); 'also b means both a' (95% vs 0%); 'include n at most n' (73% vs 4%); 'more reaches n and meets' (73% vs 4%)
- **F9** dropped 5263 / kept 742: '' for decimals negative numbers' (100% vs 0%); 'means that many of that' (100% vs 0%); 'thousands and ' ' for' (100% vs 0%); 'upper lower case and spaces' (100% vs 0%); 's ' means s appears' (100% vs 0%); 'match when they are the' (100% vs 0%); 'case and spaces at either' (100% vs 0%); 'decimals negative numbers have a' (100% vs 0%)
- **F11** dropped 1822 / kept 3593: 'it is not enough on' (53% vs 0%); 'condition that must also hold' (53% vs 0%); 'names a condition that must' (53% vs 0%); 'if' names a condition that' (53% vs 0%); 'also hold it is not' (53% vs 0%); 'enough on its own 'one' (53% vs 0%); ''only if' names a condition' (53% vs 0%); 'must also hold it is' (53% vs 0%)
