"""t37b/fixtures.py: in-memory stand-ins for the T37b tests (A37 f: no file is written; no replay row is read).

NOT replay data. Every row below is a Claude-written stand-in in the golden_train yes/no format (qtype noul, role aff,
card "- yes: ... / - no: ...", the builder's question as instructions) with invented texts, so the tests can run the
selection, the polarity programs and the row builder in memory. Each SPECS line also holds the declarative a truth
frame takes, the "fail to" form and one paraphrase; stand_in_pool() turns the paraphrases into a stand-in ADMITTED equiv
pool (slot templates, as the Haiku pool would hold them) so the tests never call Haiku.
"""
from __future__ import annotations

import hashlib

CHECK_COVID_CARD = ("- yes: The evidence sentences back up the claim's central assertion, with the same direction of "
                    "effect and compatible numbers.\n- no: The evidence contradicts the claim or a decisive detail of "
                    "it, so it does not support the claim as stated.")
COMVE_CARD = ("- yes: The asked-about statement is the one of the two that goes against common sense.\n"
              "- no: The asked-about statement is the sensible one of the two; the other statement goes against "
              "common sense.")
HOTPOT_CARD = ("- yes: Read together, the paragraphs show the answer is yes: what the question asks holds for every "
               "entity it names.\n- no: The paragraphs do not bear out a yes: at least one named entity lacks the "
               "property or the two values differ.")
BOOK_CARD = ("- yes: The assistant states that the requested reservation was booked successfully.\n"
             "- no: The assistant says the booking could not be made, even if it offers another day.")
CRASH_CARD = ("- yes: The complaint says the vehicle actually collided in the incident it describes.\n"
              "- no: The complaint reports no actual collision of this vehicle: only a defect or a near miss.")
FIRE_CARD = ("- yes: The complaint says the vehicle actually caught fire, burned or had flames.\n"
             "- no: The complaint reports no actual fire in this vehicle: only smoke or a burning smell.")
SC_ACC_CARD = ("- yes: Most people would see the action being judged as okay, expected or good.\n"
               "- no: Most people would see the action being judged as bad or very bad: rude, unkind or harmful.")
SC_WRONG_CARD = ("- yes: Most people would see the action being judged as bad or very bad: rude, unkind or harmful.\n"
                 "- no: Most people would see the action being judged as okay, expected or good.")
SEMTAB_CARD = ("- yes: Everything the statement says is true according to the table's cells, caption and notes.\n"
               "- no: The table shows the statement is false: a value, count or comparison is wrong.")
TM1_CARD = ("- yes: The assistant's last message confirms this value as booked or available for the transaction.\n"
            "- no: The assistant's last message says this value is unavailable, sold out or cannot be done.")
TM3_CARD = ("- yes: The agent completes a ticket purchase for the customer within this conversation.\n"
            "- no: No tickets are bought in this conversation: the customer declines or postpones.")
ONET_CARD = ("- yes: The duties are tasks of the named occupation.\n"
             "- no: The duties describe a different occupation's characteristic work.")
CARDS_CARD = ("- yes: The paragraph itself argues the contrarian claim that the sun drives recent warming.\n"
              "- no: The paragraph does not make this contrarian claim: it gives background or another argument.")
HATE_CARD = ("- yes: The post expresses hatred toward a protected group, in words or emoji.\n"
             "- no: Not hateful: it may name a group, quote or condemn hate, or be neutral.")
INJURY_CARD = ("- yes: The complaint says at least one person was actually hurt in the incident.\n"
               "- no: The complaint reports nobody hurt.")

# (source, question, card, state, gold, declarative-with-not after the frame, fail-to / lack form, paraphrase)
SPECS = (
    ("gd_check_covid", "Does the evidence support the claim?", CHECK_COVID_CARD,
     "Evidence (from the abstract of a scientific article):\nMasks reduced droplet spread in the chamber trial.\n\n"
     "Claim: Masks cut droplet spread.", 1,
     " the evidence does not support the claim", "Does the evidence fail to support the claim?",
     "Is the claim backed up by the evidence?"),
    ("gd_check_covid", "Does the evidence contradict the claim?", CHECK_COVID_CARD.replace("back up", "show false"),
     "Evidence (from the abstract of a scientific article):\nThe vaccine group had fewer admissions.\n\n"
     "Claim: The vaccine group had more admissions.", 1,
     " the evidence does not contradict the claim", "Does the evidence fail to contradict the claim?",
     "Is the claim at odds with the evidence?"),
    ("gd_comve", "Of these two statements, does Statement 1 go against common sense?", COMVE_CARD,
     "Statement 1: He put the elephant in his pocket.\nStatement 2: He put the coin in his pocket.", 1,
     ", of these two statements, Statement 1 does not go against common sense", None,
     "Of these two statements, is Statement 1 the one that goes against common sense?"),
    ("gd_comve", "Of these two statements, does Statement 2 go against common sense?", COMVE_CARD,
     "Statement 1: She drank a glass of water.\nStatement 2: She drank a glass of sand.", 1,
     ", of these two statements, Statement 2 does not go against common sense", None,
     "Of these two statements, is Statement 2 the one that goes against common sense?"),
    ("gd_hotpotqa_yesno", "Were Ana Ruiz and Tomas Feld both born in Portugal?", HOTPOT_CARD,
     "Ana Ruiz: a painter born in Lisbon, Portugal.\n\nTomas Feld: a sculptor born in Porto, Portugal.", 1,
     " Ana Ruiz and Tomas Feld were not both born in Portugal", None,
     "Is Portugal the country of birth of both Ana Ruiz and Tomas Feld?"),
    ("gd_hotpotqa_yesno", "Were Corran Rail and Halvard Bank both founded before 1950?", HOTPOT_CARD,
     "Corran Rail: a railway line opened in 1871.\n\nHalvard Bank: a savings bank founded in 1902.", 1,
     " Corran Rail and Halvard Bank were not both founded before 1950", None,
     "Was each of Corran Rail and Halvard Bank founded before 1950?"),
    ("gd_multiwoz21_sysacts",
     "Does the assistant's reply confirm that the booking the customer asked for was actually made?", BOOK_CARD,
     "Customer: a table for two on Friday, please.\nAssistant: Done, your table is booked; reference KX42.", 1,
     " the assistant's reply does not confirm that the booking the customer asked for was actually made",
     "Does the assistant's reply fail to confirm that the booking the customer asked for was actually made?",
     "Does the reply from the assistant confirm that the booking the customer asked for really went through?"),
    ("gd_nhtsa_complaints",
     "Does this vehicle safety complaint report that the vehicle was actually involved in a crash?", CRASH_CARD,
     "The brake pedal went soft on the highway and I nearly hit the car in front.", 0,
     " this vehicle safety complaint does not report that the vehicle was actually involved in a crash",
     "Does this vehicle safety complaint fail to report that the vehicle was actually involved in a crash?",
     "Does this vehicle safety complaint state that the vehicle was actually involved in a crash?"),
    ("gd_nhtsa_complaints", "Does this vehicle safety complaint report that the vehicle actually caught fire?",
     FIRE_CARD, "Smoke came from the dashboard vents and the cabin smelled of burning plastic.", 0,
     " this vehicle safety complaint does not report that the vehicle actually caught fire",
     "Does this vehicle safety complaint fail to report that the vehicle actually caught fire?",
     "Does this vehicle safety complaint state that the vehicle actually caught fire?"),
    ("gd_nhtsa_complaints",
     "Does this vehicle safety complaint report that at least one person was actually injured?", INJURY_CARD,
     "The airbag went off and my passenger broke a wrist.", 1, None, None,
     "Does this vehicle safety complaint state that at least one person was actually injured?"),
    ("gd_sc101", "Is the action being judged acceptable according to common social norms?", SC_ACC_CARD,
     "Situation: returning a lost wallet.\nAction being judged: returning a lost wallet to its owner.", 1,
     " the action being judged is not acceptable according to common social norms", None,
     "According to common social norms, is the action being judged acceptable?"),
    ("gd_sc101", "Is the action being judged wrong according to common social norms?", SC_WRONG_CARD,
     "Situation: reading a partner's diary.\nAction being judged: reading a partner's private diary.", 1,
     " the action being judged is not wrong according to common social norms", None,
     "According to common social norms, is the action being judged wrong?"),
    ("gd_semtabfacts_sci", "Is the statement supported by the table?", SEMTAB_CARD,
     "Table caption: Yields by plot.\n| plot | yield |\n| A | 12 |\n| B | 9 |\n\nStatement: Plot A has the highest "
     "yield.", 1, " the statement is not supported by the table", None, "Does the table support the statement?"),
    ("gd_taskmaster1",
     "According to the assistant's last message, is \"Friday at 7 pm\" confirmed for the customer's restaurant "
     "booking?",
     TM1_CARD, "Customer: Friday at 7 pm for four.\nAssistant: Friday at 7 pm is fully booked, sorry.", 0,
     ", according to the assistant's last message, \"Friday at 7 pm\" is not confirmed for the customer's "
     "restaurant booking", None,
     "Does the assistant's last message confirm \"Friday at 7 pm\" for the customer's restaurant booking?"),
    ("gd_taskmaster3", "By the end of this conversation, has the customer actually bought movie tickets?", TM3_CARD,
     "User: two tickets for the late show.\nAgent: purchased, enjoy the film.", 1,
     ", by the end of this conversation, the customer has not actually bought movie tickets", None,
     "Has the customer actually bought movie tickets by the end of this conversation?"),
    ("gd_onet_occupation", "Are the listed duties part of the job of the occupation named above?", ONET_CARD,
     "Occupation: Baker.\nDuties: knead dough; bake bread; clean ovens.", 1,
     " the listed duties are not part of the job of the occupation named above", None,
     "Do the listed duties belong to the job of the occupation named above?"),
    ("gd_cards", "Does this paragraph make the contrarian climate claim that the sun drives recent warming?",
     CARDS_CARD, "Solar output has been flat for decades while temperatures rose, the authors note.", 0,
     " this paragraph does not make the contrarian climate claim that the sun drives recent warming",
     "Does this paragraph fail to make the contrarian climate claim that the sun drives recent warming?",
     "Does this paragraph put forward the contrarian climate claim that the sun drives recent warming?"),
    ("gd_hatemoji_build_v14", "Is this post hateful?", HATE_CARD, "Great match today, well played everyone.", 0,
     " this post is not hateful", None, "Does this post express hate?"),
)


def _id(i: int) -> str:
    return f"r_gd_fixture_{i}"


def rows() -> list:
    out = []
    for i, (src, q, card, state, gold, *_rest) in enumerate(SPECS):
        gid = f"g:gd:{src[3:]}:fx{i}"
        out.append({"id": _id(i), "group_id": gid, "call_id": "c_" + hashlib.sha1(gid.encode()).hexdigest()[:12],
                    "split": "train", "track": "GD", "source": src, "state": state, "qtype": "noul",
                    "instructions": q, "options": None, "gold": gold, "role": "aff", "card": card,
                    "meta": {"dataset": "fixture stand-in", "licence": "CC BY 4.0 (fixture stand-in)",
                             "domain": src[3:], "family": "fixture"}})
    return out


def many_rows(n_per: int) -> list:
    """n_per distinct stand-in rows per fixture question (own id, group and call_id; the state gets a counter so the
    normalised states differ; the gold alternates with the copy, so the plan can balance the partner gold), for the
    share and cap tests."""
    out = []
    for k in range(n_per):
        for r in rows():
            gid = f"{r['group_id']}:{k}"
            out.append(dict(r, id=f"{r['id']}_{k}", group_id=gid,
                            call_id="c_" + hashlib.sha1(gid.encode()).hexdigest()[:12],
                            gold=r["gold"] if k % 2 == 0 else 1 - r["gold"],      # both golds in every cell (A1-5)
                            state=r["state"] + f"\n(case {k})"))
    return out


def bad_rows() -> list:
    """Rows that must NOT become bases, each with the reason the selector gives."""
    base = rows()[0]

    def v(i, reason, **kw):
        r = dict(base, id=f"r_gd_bad_{i}", group_id=f"g:gd:bad:{i}", call_id=f"c_bad_{i}", **kw)
        return r, reason

    out = [
        v(0, "vote-share or teacher target (meta.teacher)", meta={**base["meta"], "teacher": {"yes": 0.8}}),
        v(1, "not C1's own question (role != aff)", role="neg"),
        v(2, "attacked row", meta={**base["meta"], "attack_target": "no"}),
        v(3, "source excluded", source="gd_feverous"),
        v(4, "question matches no binary-predicate entry", instructions="Does the evidence mention the claim?"),
        v(5, "card is not exactly", card=base["card"] + "\n- maybe: unclear"),
        v(6, "not a yes/no row", qtype="choice", options=["yes", "no"]),
        v(7, "source excluded", source="gd_gen_logic_negation"),
        v(8, "source excluded", source="hard_nli_a"),
    ]
    twin = dict(base, id="r_gd_bad_twin_a", group_id="g:gd:bad:twin", call_id="c_bad_twin")
    out.append((twin, "call_id shared"))
    out.append((dict(twin, id="r_gd_bad_twin_b"), "call_id shared"))
    out.append((dict(base, id="r_gd_bad_rel", group_id="g:gd:bad:rel", call_id="c_bad_rel"), "already in a relation"))
    out.append((dict(base, id="r_gd_bad_old", group_id="g:gd:bad:old", call_id="c_bad_old"), "old slice"))
    hot = rows()[4]
    out.append((dict(hot, id="r_gd_bad_hotswap", group_id="g:gd:bad:hs", call_id="c_bad_hs", source="gd_sc101",
                     instructions="Is this action against the law in most places?",
                     card=HOTPOT_CARD), "card names an answer word"))
    return out


BAD_RELS = [{"a": "r_gd_bad_rel", "b": "r_gd_bad_rel_x", "type": "inv"}]
OLD_IDS = {"r_gd_bad_old"}


def keep_all(source: str, verified=frozenset()) -> bool:
    """Stand-in status for the tests (the real one reads the replay register lists; see test_t37b)."""
    return True


def stand_in_pool() -> list:
    """Admitted pool records: each fixture paraphrase as a pool template (slot values -> {SLOT}), one record per
    distinct template, with a stand-in task id and two stand-in 'same' reads (tests only; the real pool is
    author_pool's)."""
    from t37b import author_pool as AP
    from t37b import sources as SRC
    out, seen = [], set()
    for src, q, *_x, para in SPECS:
        e = SRC.entry_for({"source": src, "instructions": q})
        vals = SRC.slot_values(e, q)
        if vals is None:
            continue
        tpl = para
        for slot, v in vals.items():
            tpl = tpl.replace(v, "{" + slot + "}", 1)
        assert SRC.fill(tpl, vals) == para, (tpl, para)
        if (e.key, tpl) in seen:
            continue
        seen.add((e.key, tpl))
        out.append(AP.record(e.key, tpl, "T37b-author_wording-standin-000", "0" * 64)
                   | {"reads": ["same", "same"], "status": "admitted"})
    return out
