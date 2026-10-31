# DRAFT A53: G13 and the C2-side dev targets (c2_mixdev, c2_transfer_dev). NOT APPLIED. For the orchestrator to rule on.

Written 16 Oct 2026 by the G13-diagnosis agent. No change was made to `g13_c2.py`'s matching rules, to any gate bar, or to any
row. Evidence script (read-only, CPU): `c2_build/zed_orch/g13_dev_frame_diag.py <blocks>` (run from `lean/`).

## 1. Finding

The candidates batch (`logs/decontam_counts/c2_cand_<B>.json`, inputs unchanged since the run: every candidate and mixdev
sha256 matches) drops whole families almost entirely through ONE target, `c2_mixdev`:

| block | units | units hit by c2_mixdev | units hit only by other targets | G13 drop rows / rows |
|---|---|---|---|---|
| T06 | 1039 | 1039 | 0 | 1251 / 1251 |
| T07 | 898 | 898 | 0 | 1179 / 1179 |
| T28 | 2462 | 2053 | 0 | 2740 / 3151 |
| T29 | 2318 | 1952 | 2 | 2530 / 3001 |
| T26 | 1623 | 938 | 54 | 1297 / 2100 |
| T12 | 903 | 585 | 4 | 842 / 1154 |
| T23 | 846 | 661 | 2 | 835 / 1057 |
| T30 | 1544 | 787 | 12 | 990 / 1977 |
| T01 | 1870 | 84 | 44 | 184 / 2391 |
| T31 | 1127 | 32 | 9 | 58 / 1475 |

I re-derived the shared items independently of the engine (word 10-grams of `state`, segments of >= 5 words, options of >= 5
words, vs the 16 mixdev files). My "units with a shared item" equals the engine's c2_mixdev unit count in all 10 blocks, so the
three item kinds explain every c2_mixdev drop (tulu8 / MinHash / embed hits fall inside them).

**T06 in detail.** One 10-gram, "posted this notice at its checkout and on its website", is in 1039 of 1039 units and in all 150
mixdev rows. It is `NOTICE_TPL` (families/T06/plugin.py:257), a fixed program sentence used by S1-S5 alike. The next most common
shared 10-grams are the closed handover vocabulary ("handover delivered to a parcel locker and collected by the", 268 units;
plugin.py:82) and the order-record keys. They are program frame text, identical by design.

**Assets are disjoint for the large blocks.** Across the mixdev rows vs the candidates (meta ids):

| block | skin_id | register | card_id | domain_pack | wording_id | card text | instructions |
|---|---|---|---|---|---|---|---|
| T06, T12, T26, T29, T30 | 0 shared | 0 | 0 | 0 | 0 | 0 | 0 |
| T28 | 0 | 0 | 0 | 0 | 0 | 15 of 36 mixdev card texts equal a training card text (ids differ) | 0 |
| T07 | 0 | 0 | 0 | 0 | 6 of 33 (14 of 150 rows) | none | 0 |
| T01 | 0 | 0 | 0 | 8 of 8 | 55 of 55 (150/150 rows) | none | 0 |
| T23 | 0 | 0 | 0 | 6 of 6 | 63 of 64 (141/142 rows) | 2 of 18 | 7 of 87 |
| T31 | 0 | 0 | 0 | 0 | 67 of 68 (142/144 rows) | 15 of 15 | 12 of 91 |

So for T06, T12, T26, T29, T30 (and T28 by id) this is NOT a mixdev generation bug: the mixdev already uses dev-only skins,
registers, cards, packs and wordings (spec 7.1). Fix (a) was therefore not applied to them.

**Real reuse (a-type) exists for T01, T23, T31 (and 14 rows of T07).** The wording pools of these families have no held-out
wordings at all (T01 `wordings.jsonl`: 0 of 271 held_out), so `plugin.sample(S5)` falls back to training wordings. This cannot be
fixed in `gen_full_c2.py`: `build_mixdev` only calls the plugin; the wording and pack choice is made by the plugin and its pools.
It needs held-out wordings (and for T01/T23 held-out packs) authored by Haiku: an orchestrator task. Dropping the offending mixdev
rows is possible for T07 (136 of 150 rows would remain) but not for T01/T23/T31 (about all rows use a training wording).

## 2. Proposed narrow rule (draft text)

> **A53 (draft).** For the two C2-side dev targets only, `c2_mixdev` and `c2_transfer_dev`, a shared item (word 10-gram,
> segment or option of >= 5 words) between a training unit and a dev row is not a hit when it is a family *frame item*:
> (A) asset-independent: in the block's candidates it occurs in units spanning at least min(5, n) distinct values of each
> asset dimension (skin_id, wording_id, card_id, domain_pack) that has n >= 2 values; it therefore cannot belong to any one
> authored asset; or (C) tiled by the family's frozen program literals: its words partition into spans of >= 2 words, each a
> contiguous word run inside one string literal of the family's plugin, vocab or fixtures code cut at placeholders (single
> words only at the item's two ends or as a whole literal). Precondition, asserted by program per block: the block's mixdev
> rows share no skin_id, register or card_id with the candidates, and no wording_id or domain_pack where the pool has
> held-out entries. A block that fails the precondition gets no waiver. A unit with any non-waived shared item is dropped
> exactly as today, whichever method found it. The rule does not touch OHS-4, the sealed-side child, public, old-dev or
> any other target, nor seed/pool checks, nor G-TPL. The log records, per block, the waived and residual unit counts, the
> literal inventory sha256s (already in `inputs`) and the precondition result.

Why this is narrow: program frame text is the thing a dev set is *supposed* to share with training (A25 c already shares the
card and question wording on purpose). Anything that comes from a single authored asset, or is an authored stock sentence shared
with a dev skin, stays a binding hit.

## 3. What the rule would leave (units still dropped for c2_mixdev; evidence script, all 10 T blocks)

| block | units | c2_mixdev hit now | after A only | after C only | after A or C (proposed) |
|---|---|---|---|---|---|
| T06 | 1039 | 1039 | 404 | 1002 | **375** |
| T07 | 898 | 898 | 475 | 231 | **224** |
| T28 | 2462 | 2053 | 134 | 450 | **120** |
| T29 | 2318 | 1952 | 369 | 113 | **27** |
| T26 | 1623 | 938 | 628 | 322 | **217** |
| T12 | 903 | 585 | 41 | 40 | **40** |
| T23 | 846 | 661 | 474 | 497 | **254** |
| T30 | 1544 | 787 | 9 | 9 | **9** |
| T01 | 1870 | 84 | 84 | 35 | **35** |
| T31 | 1127 | 32 | 32 | 32 | **32** |

(Add the "hit only by other targets" column of section 1 for the full post-rule drop; those are public/sealed hits and unchanged.)

The residual is real authored overlap, for example "thank you for your help" (T30, T01), "how do i do that" and "i want to send
it back so please help me" (T06 skins vs dev skins), "our cfo is waiting on this and the cut off is close" (T26),
"items at final sale pricing are withheld from this benefit" (T07), "number of devices registered 1 device" (T23). They are stock
sentences that both a training skin or pack and a dev skin contain. Dropping their units is correct under G13.

Not modelled in my numbers: the precondition. Under it T01, T23, T31 (wording/pack ids shared) and T07 (6 wordings) get no
waiver until their mixdev is rebuilt with held-out wordings. T07's rows with a shared wording could be filtered out of its mixdev.

## 4. Alternatives for the ruling

1. **Adopt A53 as drafted.** Units kept (before the public/sealed-only drops of section 1): T06 664 of 1039 (64%), T07 674 of 898
   (75%), T26 about 1,350 of 1,623 (83%), T28 2,342 of 2,462, T29 2,289 of 2,318, T30 about 1,520 of 1,544, T12 about 860 of 903.
   T23, T01, T31 (and T07's 14 rows) wait on the precondition (held-out wordings and packs for their mixdev).
2. **Adopt A only** (no program-literal tiling): simpler to audit, T06 / T07 / T23 / T26 lose 404 / 475 / 474 / 628 units.
3. **No rule change**: T06 and T07 lose every row, T28 and T29 about 85% of rows. Families that fall below their spec 5.3 minimum
   would leave C2 with no refill (A37 d); that outcome would come from a dev-vs-frame artefact, not from data quality.
4. **Rebuild mixdev with fresh frame text**: not possible; the frame is the program.

## 5. Other items for the orchestrator

- `mix_c2.py` `DEV_SETS` still lists `c2_t37b_dev` (T37b is in C3, A52 a). `g13_c2.py` no longer has that target (removed, with
  a comment in the registry; its test updated). Edit `mix_c2.py` and `gate_c2.py` if they require the file.
- GB / GW (not analysed in depth): GB's c2_mixdev hits are card-label options and shared sentences (its mixdev shares all 41 card ids
  and instructions with its candidates by design, A25 c); no GB state equals a GB-mixdev state. GW shares group_id with the GB
  mixdev on 194 rows and 11 identical states: genuine overlap, drop as G13 does. MD has no c2_mixdev hit (its 131 drop rows are
  public/sealed-source hits).
- big_patent: A31 (a) already binds stream mode (`G13_BIGPAT_STREAM=1`); the seed-v3 run (g13_seed3.log) completed with it:
  169 files, 2,615,652 items, 26,697 s (7.4 h). No PREREG "G13-BIGPAT-RULING" line is needed or appropriate.
