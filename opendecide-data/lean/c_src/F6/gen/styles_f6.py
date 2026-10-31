"""Format-style and wording selection for F6 (label-independent: ids only).

Training styles only for S1-S4 (fmt1.pool.training_style); the 50 held-out styles feed S5 only (dev). Each sampler
uses the containers its G0 section 7 names and the skins the F6 G3 parser reads from the skins' published specs.
"""
from __future__ import annotations

from . import common  # noqa: F401  (sys.path for fmt1)

import json

from fmt1 import pool as fpool

from .common import FMT2, unit
from . import scan

SKINS = {
    "S1": ["memo.classic", "memo.notice", "memo.internal", "memo.briefing", "sop.numbered", "sop.stars", "sop.dots",
           "sop.nested", "kv.colon", "kv.dots", "kv.aligned_colon", "form.colon", "form.brackets", "form.numbered",
           "form.leaders", "email.single"],
    "S2": ["prose.plain", "prose.lines", "prose.numbered_paras", "md.pipes", "md.aligned", "md.headed",
           "md.bold_caption", "html.pretty", "html.compact", "html.dl_fields", "html.div_wrapped", "memo.classic",
           "memo.notice", "memo.internal", "memo.briefing", "email.single"],
    "S3": ["md.pipes", "md.aligned", "md.headed", "md.bold_caption", "csv.comma", "csv.semicolon", "csv.tab",
           "csv.pipe", "csv.fixed_width", "html.pretty", "html.compact", "html.div_wrapped", "json.array"],
    "S4": ["kv.colon", "kv.dots", "kv.aligned_colon", "form.colon", "form.brackets", "form.numbered", "form.leaders",
           "memo.classic", "memo.notice", "memo.internal", "memo.briefing", "sop.numbered", "sop.stars", "sop.dots",
           "prose.plain", "prose.lines"],
}
S5_SKINS = ["chat.pipe", "chat.block", "email.list_archive", "email.digest"]
NO_PARA = {"kv", "form", "csv", "json"}   # containers that cannot show a para block (attack lines)


def _chrome_ok(s: dict) -> bool:
    """Register chrome that lands in the record (greetings, closings, memo and form titles) passes the F6 record
    scan (3.1 banned list + completeness ban)."""
    reg = fpool.register(s["register"])
    parts = [reg.get("memo_title", ""), reg.get("form_title_fmt", "").replace("{title}", "")]
    if s["container"] == "email_thread":
        parts += [reg.get("email_greeting", "").replace("{to}", ""), reg.get("email_greeting_generic", ""),
                  reg.get("email_closing", "")]
    return not any(scan.banned_hits(p) or scan.completeness_hits(p) for p in parts if p)


def training_styles(sampler: str) -> list[dict]:
    sk = set(SKINS[sampler])
    return [s for s in fpool.styles(held_out=False) if s["skin"] in sk and _chrome_ok(s)]


def dev_styles() -> list[dict]:
    sk = set(S5_SKINS)
    return [s for s in fpool.styles(held_out=True) if s["skin"] in sk and _chrome_ok(s)]


def card_styles(sampler: str, card_id: str, n: int = 6) -> list[dict]:
    cands = dev_styles() if sampler == "S5" else training_styles(sampler)
    return fpool.card_style_set(cands, n, "F6", card_id)


def pick_style(styles: list[dict], *key) -> dict:
    return fpool.pick(styles, *key)


# ---------------------------------------------------------------- instruction wordings (formats-2; F6-R5-06 lint)

# Repair r1 (G11: approved pool >= 30; F6-QC-8): 7 of the 36 formats-2 F6 wordings fail F6's wording lint, so 29
# remain. Six neutral formats-2 F4 wordings (answer-format only, already decontaminated by formats-2, and passing
# F6's lint below) join the pool, which then holds 35. Like the rest of the pool they await the second-session
# approval of G0 s1.
EXTRA_WORDINGS = ["wd.F4.B.01", "wd.F4.C.03", "wd.F4.F.03", "wd.F4.A.06", "wd.F4.B.05", "wd.F4.C.02"]


def wording_pool() -> list[dict]:
    rows = [json.loads(l) for l in open(FMT2 / "wordings" / "family_pools.jsonl", encoding="utf-8") if l.strip()]
    f6 = [r for r in rows if r.get("family") == "F6" or r.get("id") in EXTRA_WORDINGS]
    return [r for r in f6 if not scan.wording_hits(r["text"]) and not scan.wording_hits(r["text_gb"])]


def failed_wordings() -> list[str]:
    rows = [json.loads(l) for l in open(FMT2 / "wordings" / "family_pools.jsonl", encoding="utf-8") if l.strip()]
    return [r["id"] for r in rows if r.get("family") == "F6" and
            (scan.wording_hits(r["text"]) or scan.wording_hits(r["text_gb"]))]


def card_wordings(card_id: str, yesno: bool, n: int = 6) -> list[dict]:
    pool = [w for w in wording_pool() if "any" in w["forms"] or (yesno and "yn" in w["forms"])
            or (not yesno and "choice" in w["forms"])]
    pool = sorted(pool, key=lambda w: unit("wording", card_id, w["id"]))
    return pool[:n]
