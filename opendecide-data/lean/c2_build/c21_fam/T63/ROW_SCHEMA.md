# T63 row schema and the Solver B contract

Solver B is CODE written by a separate Sonnet session from the G0-lite (families/T63/G0_LITE.md incl. the Opus batch-1b block) and THIS file
only. It must not read Solver A (`near.py`, `exists.py`, `lic.py`, `solver_a.py`, `near_build.py`, `generator.py`) and may import only the
standard library and this schema. B re-derives the label from the RENDERED row (and the two sha-bound sources named below) with its own
parser. Agreement with A: 100% of kept rows (T63-K1); a block with > 2% disagreement returns to the generator.

## 1. What B receives per row (`schema.b_view(row)`)

```
{ "row_id": str, "head": "NEAR"|"EXISTS"|"LIC", "sub_block": "NEAR"|"EX-A1"|"EX-A2"|"EX-B1"|"EX-B2"|"LIC",
  "rendered": {"context": str, "question": str, "options_text": str, "text": str},
  "options": [{"letter": "A", "text": "YES"}, ...],
  "witness_inputs": {...} }
```
No label, no spec, no meta, no generator ids. `row_id` is OPAQUE (`b-` + a hash of the real id; build-skeptic fix 18 Oct: the real id's member letter `-a` is the YES row of every pair). Output expected: `{"status": "ok"|"abstain"|"error", "label": "YES"|"NO"|"COMPATIBLE"|"REVIEW"|"INCOMPATIBLE"|None}`
(the pipeline compares `label` with the stored gold; the gold LETTER is checked by the pipeline's option-integrity check).

## 2. NEAR (`witness_inputs = {"head": "NEAR", "fmt": "TBL-CSV"|"TBL-TSV"|"TBL-PIPE"|"TBL-JSON"|"TBL-KV"}`)

`rendered.context` = definitions block, registry legend `Registries: R1 = host (eco); ...`, project card (reserved internal names, internal registry,
resolve order, project org), `Snapshot (<csv|tsv|pipe|json|kv>):` table with columns name, registry, publisher, age, downloads, fork_of ("-" = none),
and `Proposed command: <eco> <verb> <name> [--registry <host>]` + `Registry: Rn`. Age words: under 30 days < under 1 year < 1-4 years < over 4 years.
Downloads: low < mid < high.
Label rule = the definitions block of the context (G0-lite 2.1 + T63-M1/B7): T8 clause first (name on the card's reserved list), else the T1..T7 rule over
entries of the QUERY's registry. B recomputes the near relations with its own implementation of NM-T1..NM-T7 (one letter dropped / added / keyboard-neighbour
substitution / adjacent swap / separator change among - _ . none / look-alike swap rn-m, l-1, o-0 / scope prefix added or removed) and applies the age /
publisher / fork-edge / established rules.

### 2a. Convention pins for the relations (build-skeptic, 18 Oct: the definitions text leaves these open and A and B would otherwise disagree on correct data)

p is "near" q when p = op(q) (or q = op(p): the union is symmetric) for exactly one single operation:
* NM-T1 / NM-T2: p is q with one character deleted / inserted (any character, anywhere; separators count as characters).
* NM-T3: same length, exactly ONE position differs and the two letters are neighbours on this QWERTY map (letters only; digits and separators have no neighbours):
  `a:qswz b:ghnv c:dfvx d:cefrsx e:drsw f:cdgrtv g:bfhtvy h:bgjnuy i:jkou j:hikmnu k:ijlmo l:kop m:jkn n:bhjm o:iklp p:lo q:aw r:deft s:adewxz t:fgry u:hijy v:bcfg w:aeqs x:cdsz y:ghtu z:asx`
* NM-T4: same length, exactly two ADJACENT positions differ and they are swapped.
* NM-T5: p != q, neither contains "/", and p equals q after deleting every "-", "_" and "." (so a separator replaced, removed, added or moved all count).
* NM-T6: p is q with ONE occurrence of rn -> m, m -> rn, l -> 1, 1 -> l, o -> 0 or 0 -> o replaced (no other confusables, no Unicode).
* NM-T7: exactly one of p, q contains exactly one "/" and the text after the "/" equals the other name, with a non-empty scope before it.
A name may satisfy several relations (the label does not depend on which). "Newer" compares the shown age CLASSES (a class younger than the other); the same class is not newer.

## 3. EXISTS

* `EX-A1`: one or two `Registry index for Rn (host), complete for package names from "lo" to "hi":` blocks (sorted by registry id); the QUESTION names the asked
  registry. YES iff the name is in the asked registry's block. The name always lies inside the block's range.
* `EX-A2`: `Library L version V, complete export list:` + `module m: s1, s2, ...` lines; the question names `module.symbol`. YES iff the symbol is in that module's list.
* `EX-B1`: `Exports of <Python 3.12|Node 24|Go 1.26> module M in the pinned toolchain image, complete[ for names from "lo" to "hi"]:` + `- name` lines; YES iff listed.
* `EX-B2`: no list. `witness_inputs = {"head","sub","lang","module","name","export_sha"}`: B loads the sha-bound stdlib export file (L-0 image record) and checks
  membership of `name` in `exports[lang][module]` (public names; re-exports count).

## 4. LIC (`witness_inputs = {"head": "LIC", "table_sha": ...}`)

`rendered.context` ends with `Licence card` / `Dependency licence: ID` / `Project licence: ID` / `Usage: <phrase>` / `Distribution: <phrase>`. B re-reads the four axes and
looks the cell up in the hashed Opus table T63-LIC-TABLE (usage phrases: vendored source copy, static link, dynamic link, separate process, dev-time tool only;
distribution phrases: distributed to others, internal only, offered as a network service).

## 5. Row JSON written by Solver A (B never reads these)

`row_id, family="T63", head, sub_block, group_id, gold, label, gold_letter, options[{letter,label,text}], question_form, slots, rendered, names, spec, witness_inputs,
meta{template_id, wording_id, construction_id, ladder, tokens, split, pair_id, twin_of, fmt, reuse_group, mech, ...}, manifest, stamp`
`names` = {policy, tool, language, runner, carrier}: every entry on the frozen manifest v1.2 AND on T63's own list.
