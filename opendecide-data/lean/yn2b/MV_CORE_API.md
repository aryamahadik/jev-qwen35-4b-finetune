# mv_core API (yn2b shared engine)

`golden_src/gen3/mv_core.py` is the shared engine every yn2b family builder uses (SPEC §4). It never computes a
label. Your `decide()` sets the gold; mv_core moves it, checks it and balances around it. It uses the standard
library only, plus `tab_core` and `build_v13_breadth` (both import-safe). It runs on CPU and is deterministic. It
writes only to `data/v14_parts/yn2b_raw/`, `data/v14_parts/yn2b_defs/` and `golden_src/gen3/MANIFEST_yn2b.jsonl`.

Tests: `yn2b/tests/test_mv_core_*.py`. `yn2b/tests/toy_family.py` is a complete worked example of a family: every
view, a decide2, and balancing.

```
cd opendecide-data/lean
PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider --basetemp=<scratch> yn2b/tests/test_mv_core_*.py
```

---

## 1. Quick start: a family builder

```python
import sys; sys.path.insert(0, "<lean>/golden_src/gen3")
import mv_core as mv

fb = mv.FamilyBuilder("gen3_tool_guard", generator_file=__file__)   # asserts the tz pin (SPEC 4.11)
packs = mv.Variants("packs", PACKS, holdout=["smart_home", "clinic"])  # held-out packs for dev_holdout
for split, n in (("train", 4000), ("dev_iid", 250), ("dev_holdout", 250)):
    rng, names = fb.rng(split), fb.names(split)          # SPEC seed stream; the split's own name pool
    while made < n:
        tier = fb.next_tier(split, rng)                  # 15/30/20/35 by deficit (or your tier_shares)
        pack = packs.pick(split, rng)
        fmt  = fb.surface("fmt", FMTS, rng, split=split, extra=(tier, pack))       # strata FIRST ...
        tpl  = fb.surface("tpl", TPLS, rng, split=split, extra=(tier, pack, fmt))
        key  = (split, tier, pack, fmt, tpl)
        want = fb.want_gold(key, rng)                    # ... then the gold for exactly that stratum
        facts = sample(rng, names, want, tier)           # your sampler; retry until decide() == want
        gold, trace = decide(facts)                      # UNDEFINED -> reject, never label
        lat = fb.new_latent(split, pack, facts, query, tier, edge=("hc:decoy_id",))
        u = fb.unit(lat)
        try:
            base = u.add(mv.RowSpec("base", "yn", render(facts, fmt), TPLS[tpl], gold, fmt, renderer, tpl,
                                    defs={"yes": ..., "no": ...}, polarity=0,
                                    shortcut_answers={name: s(facts) for name, s in SHORTCUTS.items()},
                                    decisive=tuple(trace["decisive_surface_strings"])))
            twin = u.add(mv.RowSpec("contrast", ...), twin_of=base)          # one decisive atom flipped
            neg = u.add(mv.RowSpec("ladder", "yn", ..., polarity=1, role="neg")); u.relate("complement", base, neg)
            ...
            fb.commit(u); fb.commit_gold(key, "yes" if gold else "no")
        except mv.Reject as e:
            fb.reject(e)                                  # the whole unit is dropped; counted by reason
print(mv.run_checks(fb.rows, fb.rels)); print(mv.verify_labels(fb.rows, v3_module.decide2_row))
fb.write()                                                # rows, relations, defs, MANIFEST_yn2b.jsonl records
```

---

## 2. Registry, paths, seeds (SPEC §3, §4.10, §4.11)

| Name | What |
|---|---|
| `FAMILIES` | Raw key to family index: `gen3_rule_chain` 1 … `gen3_table_layouts` 8. The source is `gd_<key>`. |
| `family_label(key)` | `"F1"`…`"F8"`. This is `meta.family`. |
| `SPLITS` | `train`, `dev_iid`, `dev_holdout`, `devx`. `DEV_KIND` maps them to `None` / `iid` / `holdout` / `devx`. |
| `split_seed(key, split)` | `20261001 + index`, plus 1e9 (dev_iid), 2e9 (dev_holdout) or 3e9 (devx). |
| `rng_for(key, split, *parts)` | `Random(split_seed)`. With parts, a sha256-derived sub-stream. |
| `derive_seed(*parts)` | A 64-bit sha256 seed that is identical in every process. |
| `assert_tz()` | Checks the tz pin: `TZ_PIN` = system zoneinfo `2026c` plus the sha256 of every UTC-offset change of `TZ_ZONES` over 2025-2027. `FamilyBuilder` calls it; pass `check_tz=False` only in tests. `assert_tz_year(d)` keeps dates inside the pinned years. |
| `raw_paths(key, part)` | Returns `(rows, relations)` for one part. **train:** `yn2b_raw/<key>.jsonl` and `yn2b_raw/relations/<key>.jsonl`. **dev** (dev_iid + dev_holdout): `yn2b_raw/dev/<key>.jsonl` and `yn2b_raw/dev/relations/<key>.jsonl`. **devx:** `yn2b_raw/dev/<key>__devx.jsonl`. |
| `defs_path(key, qid)` | `yn2b_defs/<key>__<qid>.json`. The qid is content-addressed (`defs_qid(defs)`), so identical definitions share one file. |
| `register_test_family(key, index>=100)` | Tests only. |

## 3. Names and hard-case helpers (SPEC §4.7, §4.11)

- **`NamePool(split)`** gives invented names built from syllables:
  - methods: `.person`, `.first_name`, `.surname`, `.org`, `.stem`, `.domain(reserved=True)` (`.example` / `.test`),
    `.email`, `.ident(rng, "W", 7)`;
  - the pools are disjoint across the 4 splits (sha256 bucket 70/10/10/10); `name_split(name)` tells which split
    owns a name.
- **Numbers:** `boundary_triple(limit, step)`, `pct_off(limit, pct)`, `compare(v, op, limit)` (exact Fraction),
  `round_half_up`, `convert(amount, rate, places)`, `fmt_amount`.
- **Look-alikes:**
  - `decoy_id(id, rng)` swaps adjacent digits (W3319027 → W3319072);
  - `lookalike_domain(d, rng, kind)` with kind tld / hyphen / double / rn / suffix;
  - `ENV_ALIASES`.
- **Time:**
  - `local_time_ok(naive, tz)` is False inside DST gaps and folds (reject those items);
  - `to_utc`;
  - `business_days_between(start, end, holidays)` counts days in (start, end];
  - `add_business_days`.
- **`HARD_CASES`** holds the SPEC §4.7 catalogue as `hc:*` tags per area. Put them in `RowSpec.edge` or
  `Latent.edge`. `EDGE_TAGS` is the allowed vocabulary: the GOLDEN tags, the `hc:*` tags, `exc:deny_allow` /
  `exc:allow_deny` / `exc:near_miss`, `missing_info:decisive` / `missing_info:irrelevant`, and `mixed_provenance`.
- **`Variants(name, items, holdout=None, frac=0.2)`** splits packs, renderers, phrasings, archetypes or machines into
  kept and held-out parts:
  - `.for_split(split)`: train and dev_iid use the kept part; dev_holdout and devx use the held-out part;
  - `.pick(split, rng)`.

## 4. Items (SPEC §4.1)

- **`Latent`**
  - Create it only with `fb.new_latent(split, pack, facts, query, tier, edge=())`.
  - `latent_id` looks like `f2-tr-000123`.
  - `.rng(*parts)` depends only on this latent, so re-rendering it (attack twin, format twin) is reproducible.
  - `.dev_kind`.
- **`UNDEFINED` / `is_undefined(x)`**: what `decide()` returns when the predicate does not apply. The item is
  rejected, never labelled.
- **`Reject(reason, detail)`**: the exception that drops an item or a whole unit. `fb.reject(e)` counts it by reason.
- **`RowSpec(view, qkind, state, instructions, gold, fmt, renderer, tpl, …)`**: one rendered row.

  | qkind | gold | options | defs / card |
  |---|---|---|---|
  | `yn` | True / False / 1 / 0 / "yes" / "no" | set by mv_core: `["yes","no"]` | `{"yes":…, "no":…}` required. Extra keys (for example F6's operative definition) print first. `card_style` is None (the balanced quota picks it), lower, upper or none. **none** is allowed only with `self_contained=True`. |
  | `choice` | an option | placed by you (`fb.place` / `fb.mirror`) | `{option: definition}`. Every key must be an option, so it shows on the option line. Options that carry a definition cannot contain `": "`. |
  | `score` | a level text | the level texts in ascending order (`fb.score_options`), K = 3-6 | none |
  | `jb` | an option | `fb.jb(...)`, which gives `[yes-desc, no-desc]` | none |

  Other fields:
  - `polarity` (yes/no: 0, 1 or 2 negation flips);
  - `role` (aff, neg, dneg, para, choice or attacked; the default is aff for yes/no and choice otherwise);
  - `edge`;
  - `shortcut_answers` ({solver: answer in this row's answer space, None = abstains});
  - `decisive` (surface strings that must appear verbatim, raw or JSON-escaped, in the state or definitions);
  - `judge` (applies the banned-word rule);
  - `none_option`, `n_events`, `levels`;
  - `plant` (attack rows only);
  - `provenance` (F4(a) only: dataset, licence, revision, derived_from, derived_by, group_id).

## 5. Formats (SPEC §4.3). Each renderer has a parse-back.

| Render | Parse | Notes |
|---|---|---|
| `render_json(obj)` | `json.loads` / `is_canonical_json` | Exactly `json.dumps(obj, indent=1, ensure_ascii=False)`. A `fmt="json"` state must be canonical JSON (checked). |
| `render_kv(obj)` | `parse_kv(text)` | Nested keys join with `.`; list items are `key.1`, `key.2`; keys contain no `:` or `.`. |
| `render_markdown([(title, body)])` | `parse_markdown` | The body is a str, a list of bullets, a list of `(id, text)` numbered rules, or a dict (`- k: v`). |
| `render_log(entries, order, rng, ts_style, title)` | `parse_log` | `order`: chrono, newest, shuffled or grouped. `Entry(ts, source, text, ref)`. Timestamps must be unique and timezone-aware. |
| `render_email_thread(msgs, newest_first)` | `parse_email_thread` | `Msg(sender, text, ts, to, subject)`. Blocks are separated by a line of 10 dashes. |
| `render_chat(msgs, ts_style)` | `parse_chat` | One line per message. |
| `render_grid(headers, rows, layout)` | `parse_grid(text, layout)` | Uses `tab_core.render_table` (imported, never edited). `TABLE_LAYOUTS` = md, pipe, csv, fixed, records, tsv, transposed. |
| `fmt_ts(t, "iso" or "space")` | `parse_ts` | iso looks like `2026-03-14T09:05:00Z`; space looks like `2026-03-14 09:05 UTC+01:00`. |

Other helpers:
- `join_paragraphs` joins prose paragraphs.
- `state_keys(state, fmt)` returns the JSON keys or markdown titles a probe could read.
- `len_bin(n)` uses `LEN_BINS` = 0 / 1.5K / 3K / 6K / 12K.

`meta.fmt` is a base format from `FORMATS`, optionally with a variant, for example `log:newest`.

## 6. Cards and options, as decoder_io reads them (SPEC §4.4)

- `card_defs(card)` is byte-identical to `decoder_io.card_defs` (tested).
- `yn_card(defs, style)`:
  - lower gives `- yes: …\n- no: …`;
  - upper gives `- Yes: …\n- No: …`, which is also attached to the Yes/No option lines;
  - none gives no card.
- `choice_card(defs, options)` raises if any line keys a non-option, because decoder_io would silently drop that line.
- `check_card(qtype, card, options)` is the assembler's card rule.
- `check_options(options, qkind)`: options are unique single lines of at most 200 characters; 2-26 of them; jb has
  exactly 2; score has 3-6.
- `check_text(s, what, allow_markers=False)`: no empty text, no `<|`, `|>`, `<think>` or `</think>`, and no
  untrusted-text markers except inside marker-spoof plants.
- `judge_violations(*texts)`: the banned judge-view words and phrases (SPEC §4.7).

## 7. Balancing and views (SPEC §4.2, §4.6, §4.8)

- **`Quota(shares).pick(stratum, rng, allowed=None, commit=True, also=(), pending=None)`** is a deterministic deficit
  allocator. Ties go to the `also` strata first (for example, overall under per-template), then to the rng.
- **`FamilyBuilder` quota helpers:**
  - `fb.next_tier(split, rng)`: `commit` counts the tier once per latent.
  - `fb.want_gold(stratum, rng)` and `fb.commit_gold(stratum, gold)`.
  - `fb.surface(name, choices, rng, gold=None, split, extra)`.
  - `fb.quota(name, shares)`: your own quota, for example the three exception groups, view mixes or pack rotation.
- **The recommended balance pattern:**
  1. Choose every stratum dimension first (tier, pack, fmt, tpl, renderer), before the gold is known.
  2. Ask `want_gold` for exactly that stratum.
  3. Sample facts until `decide()` gives that gold.
  4. For free choices made after the gold is known (a format twin's format, for example), use
     `fb.pick_balanced(latent, [RowSpec…], rng)`. It picks the candidate whose joint stratum (`fb.stratum_key`)
     stays most balanced.
- **Check that every (tier, gold) target is reachable with your shortcut set.** For example, "hard" needs at least 2
  shortcut solvers wrong. If one combination is impossible, `want_gold` keeps asking for it and your loop never ends.
  Cap your attempts.
- **`fb.place(gold, others, rng, stratum, none_option=None, none_is_gold=False)`**: the gold goes to a position that
  is uniform per stratum and K. A none option always goes last.
- **`fb.mirror(gold, shortcut_answers, fillers, rng, stratum, none_text="None of these")`**: a choice mirror.
  - It returns `(options, gold, info)`.
  - "None of these" appears in 20% of mirrors and is the gold in 25% of those; the true answer is then left out.
  - **K never depends on whether none is the gold.**
- **`fb.jb(yes_desc, no_desc, truth, rng, stratum)`**:
  - options are `[yes, no]` with the "true" criterion first;
  - 80% use the family wording and 20% use `JB_FALLBACK`, balanced per gold;
  - it returns `(options, gold, wording)`.
- **`FamilyBuilder.score_options(levels)`**: ascending level texts; any `i:` prefix is refused.
- **`fb.plant(latent, channel, answer_phrase, gold, wrong, rule=, date_s=, number=, json_key=)`** returns a
  `Plant(text, channel, direction, target, spoof, tpl, json_key)`.
  - Templates rotate evenly.
  - The direction is 50/50 per template and overall: `for_gold` argues for the gold, `against_gold` for one of
    `wrong`. The gold never changes.
  - A quarter of F1/F2 plants spoof the markers (`SPOOF_TEMPLATES`). Other families never spoof.
  - Channels are `PLANT_CHANNELS`: tool_result, email, rep_note, doc_footer, log_note, pasted_doc.
  - You insert `plant.text` into that untrusted sub-field only. For JSON states, set `json_key` to the top-level key
    that holds the plant.
  - `PLANT_TEMPLATES` / `SPOOF_TEMPLATES` share no 6-word run with the injected spans of eval_jagged, eval_opi or
    eval_redef (tested). `template_runs(t)` and `runs6(text)` support the 6-gram bans.

## 8. Units and the builder (SPEC §4.2, §4.9, §4.10)

**`u = fb.unit(latent)`** makes one latent into one call_id unit.

**`u.add(spec, twin_of=None)`** returns the rid, for example `f2-tr-000123-0`. It raises `Reject` when:
- the unit already has 5 rows;
- the unit's states total more than 24K characters;
- a unit with any state over 6K characters would get a 4th row;
- a `json` state is not canonical;
- the gold is not an option;
- a card or option rule fails;
- a yes/no row is missing its yes or no definition, or asks for no card without being self-contained;
- polarity is missing;
- a decisive fact is not in the text (grounding);
- a judge row uses a banned word;
- a hard base row has fewer than 2 wrong shortcuts;
- an edge tag is unknown;
- a state + question repeats one already in the unit or the family (normalised with `words()`);
- markers appear outside a spoof plant, or a spoof appears outside F1/F2;
- the attack view, plant and `attacked` role do not all go together.

**`u.relate(type, a, b)`** records a relation:
- **complement:** two yes/no rows with opposite golds; each row is in at most one complement;
- **equiv:** the same golden qtype and the same gold; choice-type rows need an identical option list;
- **inv:** a = the clean row, b = its attack twin.

**`fb.commit(u)`** runs `finalize` and then keeps the unit:
- A contrast twin keeps the question and the options, flips the gold, and changes at most 3 lines of
  state + definitions.
- Every attack twin has exactly one `inv` relation, and `check_attack_pair` passes: same question, options, gold
  and definitions; exactly one contiguous insertion that holds the plant; for JSON, only `json_key` changed.
- Then the card-style, tier and joint-balance counts are updated.

**`fb.write(parts=("train","dev","devx"), overwrite=False)`**:
- writes the rows and relations of each part, plus the content-addressed defs files;
- appends one `MANIFEST_yn2b.jsonl` record per file (written, tool, key, part, path, rows, sha256, revision, seed,
  tz, summary);
- refuses to overwrite unless `overwrite=True`, and refuses any path outside yn2b_raw/ and yn2b_defs/;
- `manifest_append(record)` is append-only, one locked O_APPEND write, and uses the same record shape as
  `yn2b_common`.

**Readers:** `read_raw(key, part)` and `load_defs(key, qid)`.

**Raw row.** GOLDEN-compatible. A yes/no row has options `["yes","no"]` and gold `"yes"` / `"no"`. `soft` is null.
`meta` always has exactly `RAW_META_KEYS`:
- dataset, licence, revision, split (always `"train"`, the source-split field of GOLDEN), family, pack, edge, tier;
- n_shortcut_wrong, shortcut_hits;
- view, qkind, role, fmt, renderer, tpl, polarity, judge;
- latent_id, twin_of, defs (qid), card_style, none_option, dev_kind, n_events, levels;
- plant_dir, plant_channel, plant_spoof, plant_tpl, len_bin.

F4(a) rows also carry derived_from, derived_by and derived_group.

## 9. Assembly into golden rows (SPEC §4.5)

**`assemble(raw_rows, raw_rels, defs_lookup, split=None)`** returns `(golden rows, golden relations)`.
`defs_lookup(raw_row)` returns that row's definitions. Relations whose ends were dropped are dropped too. Each row
goes through `to_golden(raw, defs, split, id_map)`, which then runs `check_golden_row`:

| Field | Value |
|---|---|
| id | `r_yn2b_<key>_<k>`, with k = the rid minus its family prefix (`tr_000123_0`), so ids stay stable when decontamination drops other units |
| group_id | `g:yn2b:<key>:<latent_id>` (F4(a): the base row's) |
| call_id | `cid(group_id)` |
| split | `train` / `yn2b_dev` / `yn2b_devx`, or the `split` argument |
| track | `GD` |
| source | `gd_<key>` |
| role | from meta |
| yes/no rows | qtype `noul`, `options: null`, integer gold 1/0, card from `meta.card_style` |
| choice / score / jb rows | qtype `choice`, gold = the option string; choice card = option lines; score and jb have no card |
| meta | the raw meta without split/defs, plus `domain`; **never `teacher`** |

`check_golden_relations` checks that related rows share a call_id, that complement golds sum to 1, that equiv rows
share qtype and gold, and that inv rows share the gold with b attacked.

## 10. Checks (SPEC §4.6-4.8, §8)

**`run_checks(rows, rels, tier_shares=None)`** returns one report per check plus `ok`. It runs on the raw rows of
one family part.

| Check | Rule |
|---|---|
| `balance_report` | Yes share of yes/no + JB rows in the joint stratum family × qkind × tier × polarity × fmt × len_bin × pack, and in every single dimension plus tpl, renderer, view and card_style. The rule is `share_ok`: \|yes − n/2\| ≤ max(0.05·n, 1), which is exactly 45-55% for n ≥ 20. |
| `position_report` / `level_report` | Choice gold positions per (family, view, tpl, K), and score levels per (family, K), are uniform within max(0.2·n/K, 2). |
| `none_report` | Mirrors that offer "none": gold in 25% ± 5 pp. Other none options: gold at mean(1/K) ± 5 pp. |
| `tier_report` | The latent tier mix is within ±3 pp of the shares; hard base rows have ≥ 2 wrong shortcuts; every hard latent carries shortcut answers. |
| `shortcut_report` | No shortcut solver is above 60% on the family's rows. |
| `edge_report` | The three exception groups are equal (±5 pp); `missing_info*` rows are balanced yes/no; `mixed_provenance` is ≤ 5% in F1/F2. |
| `plant_report` | Plant direction is 50/50 overall and per template; spoofs are 25% in F1/F2 and 0 elsewhere. |
| `card_report` | The card style is independent of gold (max gap ≤ 3 pp). |
| `artefact_corr` | \|corr(gold, x)\| < 0.05 for length, fmt, tier, polarity, len_bin, card presence and card style, per qkind (yn, jb). |
| `keyset_report` | One JSON top-level key set per (family, pack). |
| `structure_report` | The file-level SPEC §8.3 re-check: relations, twins, split side, unit sizes. |
| `hard_case_report` | A report (not a gate) of `hc:*` coverage and absent tags. |
| `verify_labels(rows, decide2_row)` | SPEC §8.1: the independent decide2 on the **rendered** row must agree 100% (UNDEFINED counts as a failure). |

**Not in mv_core; this is check_yn2b's job:** TF-IDF probes, decontamination (12-gram), and the 6-gram bans against
the ship splits, OHS-1/2, dialogue_rebuttal and v11 templates.

---

## 11. SPEC points this module had to settle (and how)

1. **Raw yes/no rows** keep the GOLDEN raw form: options `["yes","no"]` and string gold. Only the assembler converts
   to `noul` with options null and gold 1/0 (the §4.5 F1 fix).
2. **Card style is per row in `meta.card_style`**, because the raw format has no card field. Defs are stored for
   no-card rows too, for audit. They are content-addressed per SPEC `gen3_<name>__<qid>.json`.
3. **Extra yes/no card lines** (for example F6's operative definition) are allowed before the yes/no lines. The
   whole card is printed as Definitions on yes/no rows.
4. **Relation files** are not placed by the SPEC. They go in `yn2b_raw/relations/` and `yn2b_raw/dev/relations/`, so
   a glob over row files never picks them up. The dev part holds dev_iid + dev_holdout; devx is `<key>__devx.jsonl`.
5. **`meta.split` stays `"train"`**, the GOLDEN source split. The yn2b split is in `meta.dev_kind`. Golden dev rows
   get split `yn2b_dev` / `yn2b_devx`, following the `pg_dev` naming.
6. **The golden id `k`** is the latent-based rid, not a running index, so it is stable when other units are dropped.
7. **Balance in tiny strata:** "45-55% in every stratum" is read as |yes − n/2| ≤ max(0.05·n, 1).
8. **Judge banned words** apply to judge rows' instructions, options and card, not the state. Every row would be too
   strict: F4(a)'s own proposition says "the right label".
9. **The hard-tier rule** (≥ 2 shortcut solvers wrong) applies to base rows that carry shortcut answers. A secondary
   base row, for example the score view of the same latent, may carry none. The tier mix counts latents, not rows.
10. **Choice mirror:** "None of these" goes last, and its presence never changes K. Otherwise a model could read
    "3 options with none = none" from the option count; the SPEC did not mention this. The 25% none-gold share
    follows the SPEC, which makes positions exactly uniform at K = 4.
11. **JB-letter "true option listed first"** means options are always `[yes-desc, no-desc]`, and gold is the first
    option iff the answer is yes. JB rows count as yes/no rows in the balance checks.
12. **"Planted only in an untrusted sub-field"** is checked as one contiguous insertion (JSON: only the declared key
    changes). The channel's meaning is the family's declaration (`meta.plant_channel`).
13. **Plant direction** is balanced per template **and** overall, so neither the template nor the family predicts
    "do the opposite".
14. **Tz pin:** the venv has no `tzdata` package, so zoneinfo reads the system database (`/usr/share/zoneinfo`,
    2026c). The pin is that version string plus a transition fingerprint.
15. **Contrast twin "at most 3 lines differ"** is measured over state + definitions, because F6's exclusion twin
    changes the card, not the state.
16. **Equiv** needs the same golden qtype. choice, score and jb are all golden `choice`, and need an identical
    option list.
17. **Dedupe:** mv_core dedupes on normalised state + question inside a family, across its splits. Deduping against
    golden_train and across families is check_yn2b's job (§7.5).
