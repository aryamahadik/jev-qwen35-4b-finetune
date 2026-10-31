"""fmt1: the formats-1 format style pool and renderers for OpenDecide C (C_DATA_SPEC v4 section 6; step 4).

What is here (data in ../data, every object with a stable id and its own sha256):
  - 400 format styles (FS-0001..FS-0400) = container skin x card style x register x instruction position (+ fence for
    data containers). 50 are held out: mix-tuning dev only (S5 samplers, dev items), NEVER a training row. Every
    held-out style uses a never-trained element (a held-out-only skin or card style), so dev formats are truly unseen.
    pool.styles() returns training styles by default; pool.styles(held_out=True) the 50 dev styles.
  - definition styles (DS-*, canonical meta.defs_style names) and render variants (DV*), few-shot templates (FT*),
    inverted-card frames, case references and question frames (IVC*, IVN*, IVQ*), masked ID schemes (MS*),
    swap words (SW*), label notices (LN*) and the masked / swapped rules (LR*).

Row fields a family fills (spec 2.4): meta.format_style = the style id; meta.defs_style = the canonical DS name
(one_line, one_line_examples, rubric_table, decision_list, short, none); record the DV / FT / IVQ / MS ids in the
family's side manifest or edge tags as its G0 spec says. Locale (spelling, dates, currencies, units) and the
instruction wording pools are formats-2's; this pool draws neither.

What the prompt shows (v1.1): C trains and serves in decoder_io's cygnet style and schema_branch_mark layout. A yes/no
row shows the whole card; a choice row shows only "- {option text}: {definition}" card lines (appended to the option
lines). card.render_row_text(qtype=...) handles both: on choice rows it writes option definitions as those lines
(card.render_choice_defs) and moves every other card block into instructions. card.loader_check(row) renders the row
with decoder_io.user_msg under a random option order and proves that the card, definitions, examples and rules are
visible and that the gold letter maps back. Every family row passes it (label rules LR04, LR07, LR14, LR15).

Use:
    from fmt1 import pool, render, card, labels
    st = pool.pick(pool.styles(compat="F4"), family, card_id, row_key)      # label-independent; training styles only
    st = pool.training_style(row_style_id)                                   # raises on the 50 held-out ids
    fields = card.render_row_text(st, doc=doc, question=q, qtype="choice", card=card_ir, options=opts,
                                  wording=w, note=n)                         # state, instructions, card
    res = card.loader_check({**fields, "id": rid, "qtype": "choice", "options": opts, "gold": g},
                            must_show=card.must_show(card_ir, question=q, wording=w, note=n))   # res["ok"]
    form = labels.label_form(family, card_id, row_key)                       # plain / masked / swapped
    pool.refuse_held_out(training_rows)                                      # mixer guard (or python -m fmt1.guard)

Renderer guarantees (tests/test_fmt1.py): no invented content, no dropped content (raise instead), no missing-value
marker written by the renderer (XF06), no number reformatting, JSON / YAML / CSV / HTML parse back with standard
parsers, deterministic output. Each skin's `params` and `grammar`-relevant fields are data, so a family's G3 parser
is written from the skin spec, never from this code.
"""
from . import card, guard, labels, pool, render  # noqa: F401

__all__ = ["card", "guard", "labels", "pool", "render"]
