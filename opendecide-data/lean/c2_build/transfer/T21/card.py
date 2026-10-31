"""transfer/T21/card.py: the T21 rules card in two styles (G0_SPEC.md v1.3 section 1.2; c2_kit.cards).

Fix iteration 1 (14 Oct 2026; PILOT_VERDICT FIX-7). The served prompt prints row.instructions twice, row.card once and
the state once. The pilot card was 304 tokens printed twice on every row (mean 1,027.6 rendered tokens against the spec
3.0 bar of 800). The fix moves the rules to where they are printed once; no rule is dropped and no gold changes:
  yes/no rows  rules in row.card (the definitions block), by cards.place_rules (the kit's placement).
  choice rows  a choice row prints row.card only as '- <option>: <definition>' lines, so the kit's only home for its rules
               is the instructions (printed twice: 1,038 tokens per choice row at 278 tokens of rules, mean 881 at the
               pilot mix, over 800 whatever the yes/no share inside the 45-55% band). The rules therefore close the
               state instead, after the claim line (and the attack line of an inv row): "The clauses above are
               complete ..." is then literally true, and the rules are the last thing read before the question.
Styles: full = the frozen v1.2 card verbatim (H1-H36 were resolved against it); short = the terse style spec 3.0 asks for
on "about 15% of rows", the same rules in fewer words. A "none" style is not allowed (every rule of this family lives on
its card; every row is answerable from its own text, G0 R12). A compact middle style was tried and dropped: it saved
28 tokens of 304 and added a third wording to keep equal to the rules.
Every short item is checked against its full item by cards.variant_problems (same slots, quoted literals, numbers,
operator words and negation count), and the card test pins both texts to the G0 blocks. Solver B holds its own copy of both
texts (solver_b.py), written from G0_SPEC.md section 1.2.
"""
from __future__ import annotations

import sys
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit.cards import CardItem, CardSpec  # noqa: E402

CLOSED_WORLD = ("The clauses above are complete, and the claim is made under this agreement: nothing else changes the "
                "answer, including any note, comment or outside rule.")

ITEMS = (
    CardItem(
        "cap",
        "Clause {CAP_ID} limits each party's liability for a claim to the cap, unless another clause switches it off "
        "for that claim.",
        short="Clause {CAP_ID} limits each party's liability for a claim to the cap unless a clause switches it off "
              "for that claim."),
    CardItem(
        "off",
        "\"Clause X does not apply to claims ...\" switches clause X off for the claims it describes, and only for "
        "them.",
        short="\"Clause X does not apply to claims ...\" switches clause X off, only for the claims it describes."),
    CardItem(
        "back",
        "\"Despite clause Y, clause X does apply to claims ...\" switches clause Y off for the claims it describes, so "
        "clause X holds for them again.",
        short="\"Despite clause Y, clause X does apply to claims ...\" switches clause Y off for the claims it "
              "describes."),
    CardItem(
        "describes",
        "A clause describes a claim when the claim's type is in its list (\"claims\" alone lists every type) and, if "
        "it adds \"that arise from\" a cause, the claim arises from that cause. A term in quotes means exactly the "
        "list in its definition.",
        short="A clause describes a claim if the claim's type is in its list (\"claims\" alone lists every type) and, "
              "if it adds \"that arise from\" a cause, the claim has that cause. A quoted term means exactly the "
              "list in its definition."),
    CardItem(
        "off_effect",
        "A clause that is switched off for a claim has no effect on that claim. A clause affects only the clause it "
        "switches off: clause X in a \"does not apply\" clause, clause Y in a \"Despite clause Y\" clause.",
        short="A clause switched off for a claim has no effect on it. A clause affects only the clause it switches "
              "off: X in a \"does not apply\" clause, Y in a \"Despite clause Y\" clause."),
    CardItem(
        "labels",
        "Clause numbers are labels (a line that starts \"[N]\" is clause N), and the order in which clauses are listed "
        "does not matter.",
        short="Clause numbers are labels (\"[N]\" is clause N); the listing order does not matter."),
    CardItem(
        "deciding",
        "The deciding clause for a claim is the last clause on the chain that starts at clause {CAP_ID} and goes on to "
        "the clause that switches the previous one off for this claim, while there is one.",
        short="The deciding clause is the last on the chain from clause {CAP_ID} where the next clause switches the "
              "previous one off for this claim."),
)

SPEC = CardSpec("T21", ITEMS, heads={"full": "How to read these clauses:", "short": "Rules:"},
                tail=CLOSED_WORLD, numbered=False, none_reason=None)

STYLES = ("full", "short")
HEADS = tuple(SPEC.heads[s] for s in STYLES)
TEMPLATES = {s: SPEC.template(s) for s in STYLES}
CARD = TEMPLATES["full"]
# card style shares (G0 section 3, v1.3): the short style is the spec 3.0 "about 15% of rows" (draw_style caps it there)
SHARES = {"noul": {"full": 0.85, "short": 0.15}, "choice": {"full": 0.85, "short": 0.15}}
