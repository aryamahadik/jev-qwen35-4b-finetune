"""gen_msn_consent: consent and permission norms (yes/no, labels by construction, single-fact twins).

Shared norm stated in every item: using, lending or sharing something that belongs to someone else is okay only with
the owner's permission, and only within the limits of what the owner agreed to. Each item gives the owner's exact
words (a message), possibly a later message withdrawing it, and what the borrower actually did.

A permission covers the action only if ALL of these hold:
  granted by the owner (not a roommate or partner; silence and 'maybe' are not permission),
  same item, time inside the stated window (through <day>, weekends only, weekday afternoons, tomorrow only),
  purpose not excluded ('but not to drive to work'), done by the person who was given permission (unless the owner
  allowed sharing it; hosting guests, lending it on and sharing a password count as letting others use it), stated
  condition met ('as long as you text me first'), not withdrawn before the action.
Questions (qid): had ("Did X have <owner>'s permission for what was done?"), exceed ("Did X go beyond what <owner> had
agreed to?", negated polarity), est ("Do the messages establish that X had <owner>'s permission ...?": a condition
whose fulfilment is not stated -> no). Deterministic (seed 20261104).
"""
import copy
import random
import re

from gen_msn_rules import Schema, sty
from msn_common import WEEKDAYS, cap, edge_join, person, row, write_gen

KEY = "gen_msn_consent"
SEED = 20261104
N_PAIRS = 2500
PARTS = ["morning", "afternoon", "evening"]

# item: noun used in questions, verb phrase for the owner's item and for a different item of the owner's,
# purposes [(key, phrase)], indices of purposes that may be excluded, conditions [(key, 'as long as ...', met, not met)]
ITEMS = [
    {"item": "car", "verb": "took {O}'s car", "other": "took {O}'s motorbike",
     "purposes": [("shop", "to do the weekly grocery shopping"), ("work", "to drive to work"),
                  ("airport", "to drive a friend to the airport"), ("move", "to help a friend move house")], "excl": [1, 2, 3],
     "conds": [("as long as you text me before you take it", "{X} had texted {O} before taking it.", "{X} did not text {O} before taking it."),
               ("as long as you refill the tank afterwards", "{X} refilled the tank afterwards.", "{X} returned it with less fuel and did not refill it.")]},
    {"item": "bike", "verb": "rode {O}'s bike", "other": "rode {O}'s electric scooter",
     "purposes": [("class", "to get to class"), ("work", "to work"), ("trail", "on a long mountain trail"),
                  ("errands", "to run errands in town")], "excl": [1, 2],
     "conds": [("as long as you text me first", "{X} had texted {O} first.", "{X} did not text {O} first."),
               ("as long as you always lock it with the D-lock", "{X} locked it with the D-lock whenever it was parked.",
                "{X} left it unlocked outside a shop for a while.")]},
    {"item": "laptop", "verb": "used {O}'s laptop", "other": "used {O}'s tablet",
     "purposes": [("essay", "to write an essay"), ("games", "to play video games"), ("paid", "for paid freelance work"),
                  ("films", "to watch films")], "excl": [1, 2],
     "conds": [("as long as you log out of my accounts afterwards", "{X} logged out of {O}'s accounts afterwards.",
                "{X} stayed logged in to {O}'s accounts."),
               ("as long as you ask me first each time", "{X} asked {O} first and got a yes.", "{X} did not ask {O} first.")]},
    {"item": "camera", "verb": "used {O}'s camera", "other": "used {O}'s tripod",
     "purposes": [("wedding", "to take photos at a friend's wedding"), ("paid", "for a paid photo shoot"),
                  ("holiday", "on a short trip to the coast"), ("concert", "at a concert")], "excl": [1, 3],
     "conds": [("as long as you charge the battery before returning it", "{X} charged the battery before returning it.",
                "{X} returned it with a flat battery."),
               ("as long as you check with me first", "{X} checked with {O} first.", "{X} did not check with {O} first.")]},
    {"item": "flat", "verb": "stayed in {O}'s flat", "other": "stayed in {O}'s holiday cottage",
     "purposes": [("alone", "alone"), ("dinner", "and hosted a small dinner for three friends"),
                  ("work", "and worked from there"), ("guest", "and had a friend stay overnight")], "excl": [1, 3],
     "conds": [("as long as you water the plants", "{X} watered the plants.", "{X} forgot to water the plants."),
               ("as long as you leave the keys with the neighbour when you go", "{X} left the keys with the neighbour when leaving.",
                "{X} took the keys home instead of leaving them with the neighbour.")]},
    {"item": "drill", "verb": "borrowed {O}'s power drill", "other": "borrowed {O}'s circular saw",
     "purposes": [("shelf", "to put up a shelf"), ("deck", "to build a deck"), ("lend", "and lent it to a friend for a day"),
                  ("tiles", "to drill through bathroom tiles")], "excl": [1, 2, 3],
     "conds": [("as long as you bring it back the same day", "{X} brought it back the same day.", "{X} kept it for three days."),
               ("as long as you text me when you take it", "{X} texted {O} when taking it.", "{X} did not text {O}.")]},
    {"item": "jacket", "verb": "wore {O}'s leather jacket", "other": "wore {O}'s wool coat",
     "purposes": [("wedding", "to a wedding"), ("concert", "to a concert"), ("hike", "on a rainy hike"), ("work", "to work")],
     "excl": [2, 3],
     "conds": [("as long as you get it cleaned if it gets dirty", "It got muddy, and {X} had it cleaned.",
                "It got muddy, and {X} returned it without cleaning it."),
               ("as long as you ask me the day before", "{X} had asked {O} the day before.", "{X} did not ask {O} beforehand.")]},
    {"item": "film-streaming account", "verb": "logged into {O}'s film-streaming account", "other": "logged into {O}'s music-streaming account",
     "purposes": [("self", "to watch a series"), ("share", "and gave the password to a friend"), ("tv", "on the living-room TV"),
                  ("download", "to download films for a flight")], "excl": [1, 3],
     "conds": [("as long as you use the guest profile, not mine", "{X} used the guest profile.", "{X} used {O}'s own profile."),
               ("as long as you tell me when you've used it", "{X} told {O} afterwards.", "{X} never mentioned it to {O}.")]},
]
DONT = {"work": "use it to get to work", "airport": "drive to the airport with it", "move": "use it for moving house",
        "trail": "take it on mountain trails", "games": "play games on it", "paid": "use it for paid work",
        "concert": "take it to concerts", "dinner": "host dinners there",
        "guest": "have anyone stay overnight", "deck": "use it for big building jobs like a deck", "lend": "lend it to anyone",
        "tiles": "drill into tiles with it", "hike": "wear it hiking", "share": "give the password to anyone",
        "download": "download films on it"}

# purposes in which other people use or share the item: covered only when the owner allowed letting a friend use it
OTHERS = {"dinner", "guest", "lend", "share"}

WINDOWS = [
    ("any", "any time this week"),
    ("thru", "through {D} (that day included)"),
    ("wkend", "on the weekend (Saturday and Sunday) only"),
    ("wkaft", "on weekday afternoons this week only"),
    ("tmrw", "tomorrow (Tuesday) only"),
]


def slot(day, part):
    return day * 3 + part


class Consent(Schema):
    name = "consent"
    can_hide = True

    def params(self, rng):
        it = rng.randrange(len(ITEMS))
        item = ITEMS[it]
        win = rng.randrange(len(WINDOWS))
        thru = rng.randrange(1, 5)
        excl = rng.choice([None, rng.choice(item["excl"])])
        cond = rng.choice([None, rng.randrange(len(item["conds"]))])
        return {"it": it, "win": win, "thru": thru, "excl": excl, "cond": cond, "deleg": rng.random() < 0.25,
                "phr": rng.randrange(3), "dseed": rng.randrange(10 ** 6)}

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["owner"] = person(rng, exclude=(f["who"][0],))
        f["third"] = person(rng, exclude=(f["who"][0], f["owner"][0]))
        f["grant"] = rng.choice(["owner", "owner", "owner", "owner", "roommate", "noreply", "maybe"])
        f["day"] = rng.choice([0, 1, 2, 3, 4, 5, 6, 8])
        f["part"] = rng.randrange(3)
        f["purpose"] = rng.randrange(len(ITEMS[p["it"]]["purposes"]))
        f["actor"] = rng.choice(["self", "self", "self", "friend"])
        f["cond_met"] = rng.random() < 0.6
        f["revoke"] = rng.choice([None, None, None, slot(rng.randrange(1, 6), 1)])
        f["same_item"] = rng.random() < 0.9
        return f

    def in_window(self, p, f):
        w = WINDOWS[p["win"]][0]
        d, part = f["day"], f["part"]
        if d > 6:
            return False  # following week: every window is 'this week'
        if w == "any":
            return True
        if w == "thru":
            return d <= p["thru"]
        if w == "wkend":
            return d >= 5
        if w == "wkaft":
            return d <= 4 and part == 1
        return d == 1

    def verdict(self, p, f):
        if f["grant"] != "owner" or not f["same_item"]:
            return False
        if not self.in_window(p, f):
            return False
        if f["revoke"] is not None and f["revoke"] < slot(f["day"], f["part"]):
            return False
        if p["excl"] is not None and f["purpose"] == p["excl"]:
            return False
        pk = ITEMS[p["it"]]["purposes"][f["purpose"]][0]
        if (f["actor"] != "self" or pk in OTHERS) and not p["deleg"]:
            return False  # 'just for you, not for anyone else' also rules out guests, lending and password sharing
        if p["deleg"] and f["actor"] != "self" and pk in OTHERS:
            return False  # audit fix 29 Sep: the one allowed friend may not pass it on to further people
        if p["deleg"] and pk == "dinner":
            return False  # audit fix 29 Sep: permission for 'a friend' (one) does not cover hosting three friends
        if p["cond"] is not None:
            if f["cond_met"] == "unknown":
                return None
            return bool(f["cond_met"])
        return True

    def valid(self, p, f):
        if f["revoke"] is not None and f["revoke"] == slot(f["day"], f["part"]):
            return False
        if f["revoke"] is not None and f["grant"] != "owner":
            return False
        if p["cond"] is None and f["cond_met"] is not True and f["cond_met"] is not False:
            return False
        return True

    def alts(self, p, f):
        item = ITEMS[p["it"]]
        return {"grant": ["owner", "roommate", "noreply", "maybe"], "day": [0, 1, 2, 3, 5, 6, 8], "part": [0, 1, 2],
                "purpose": list(range(len(item["purposes"]))), "actor": ["self", "friend"],
                "cond_met": [True, False] if p["cond"] is not None else [],
                "revoke": [None, slot(1, 1), slot(3, 1), slot(5, 1)], "same_item": [True, False]}

    # ------------------------------------------------------------------ rendering
    def permission_text(self, p, f):
        it = ITEMS[p["it"]]
        item = it["item"]
        win = WINDOWS[p["win"]][1].replace("{D}", WEEKDAYS[p["thru"]])
        first = {"flat": f"You can stay in my flat {win}.", "film-streaming account": f"You can use my film-streaming account {win}."}.get(
            item, f"You can borrow my {item} {win}.")
        out = [first]
        if p["excl"] is not None:
            key = it["purposes"][p["excl"]][0]
            out.append([f"Please don't {DONT[key]}, though.", f"Just don't {DONT[key]}."][p["phr"] % 2])
        if p["cond"] is not None:
            out.append(f"That's fine {it['conds'][p['cond']][0]}.")
        out.append(["You're welcome to share it with a friend too.", "Feel free to let a friend use it as well."][p["phr"] % 2] if p["deleg"] else
                   ["It's just for you - don't share it with anyone else or let anyone else use it.",
                    "Only you, please - nobody else should use it or share it."][p["phr"] % 2])
        return " ".join(out)

    def rules(self, p):
        return "Shared norm", ["Using, lending or sharing something that belongs to someone else is okay only with the owner's "
                               "permission, and only within the limits of what the owner agreed to."]

    def story(self, p, f, rng=None):
        it = ITEMS[p["it"]]
        item = it["item"]
        X, O, Th = f["who"], f["owner"], f["third"]
        s = [[f"On Monday morning {X[0]} asked {O[0]} whether {X[1]} could use {O[0]}'s {item} this week.",
              f"{X[0]} messaged {O[0]} on Monday morning asking to use {O[0]}'s {item}."][sty(f, "a", 2)]]
        g = f["grant"]
        if g == "owner":
            s.append(f"{O[0]} replied: \"{self.permission_text(p, f)}\"")
        elif g == "roommate":
            s.append(f"{O[0]} did not answer, but {O[0]}'s roommate {Th[0]} told {X[0]}: \"I'm sure {O[0]} won't mind - go "
                     f"ahead and use the {item} this week.\"")
        elif g == "noreply":
            s.append(f"{O[0]} read the message but never replied.")
        else:
            s.append(f"{O[0]} replied: \"Maybe - let me think about it and get back to you.\" {O[0]} did not message again.")
        if f["revoke"] is not None:
            rd, rp = divmod(f["revoke"], 3)
            s.append(f"On {WEEKDAYS[rd]} {PARTS[rp]}, {O[0]} texted {X[0]}: \"Sorry, I need the {item} back - please don't use it any more.\"")
        day = f["day"]
        when = (f"On {WEEKDAYS[day]} {PARTS[f['part']]}" if day <= 6 else f"The following {WEEKDAYS[day - 7]} {PARTS[f['part']]}")
        v = (it["verb"] if f["same_item"] else it["other"]).format(O=O[0])
        purpose = it["purposes"][f["purpose"]][1]
        if f["actor"] == "self":
            s.append(f"{when}, {X[0]} {v} {purpose}.")
        else:
            poss = {"he": "his", "she": "hers", "they": "theirs"}[X[1]]
            fr = [f"a friend of {poss}", f"{X[3]} close friend", f"an old friend of {poss}"][sty(f, "b", 3)]
            s.append(f"{when}, {X[0]} passed it on to {fr}, who {v} {purpose}.")
        if p["cond"] is not None and f["cond_met"] != "unknown" and g == "owner":
            c = it["conds"][p["cond"]]
            s.append((c[1] if f["cond_met"] else c[2]).format(X=X[0], O=O[0]))
        return " ".join(s)

    def act(self, p, f):
        return None

    def edges(self, p, f):
        t = []
        own = f["grant"] == "owner"
        if own and (p["excl"] is not None or p["cond"] is not None or p["deleg"]):
            t.append("exception")
        if WINDOWS[p["win"]][0] != "any" or f["day"] > 6 or f["revoke"] is not None:
            t.append("temporal")
        if f["grant"] in ("roommate", "noreply", "maybe"):
            t.append("implicit")
        if f["actor"] != "self" or ITEMS[p["it"]]["purposes"][f["purpose"]][0] in OTHERS:
            t.append("multi_hop")
        if f["cond_met"] == "unknown":
            t.append("missing_info")
        if own and p["excl"] is not None:
            t.append("negation")
        return t

    def hide(self, p, f, rng):
        if p["cond"] is not None and f["cond_met"] in (True, False):
            g = copy.deepcopy(f)
            g["cond_met"] = "unknown"
            return g if self.verdict(p, g) is None else None
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["cond_met"] = bool(want)
        return g


# reviewer fix: questions no longer name the lent item, because in 'different item' stories (same_item=False) nothing was
# done with that item and an item-specific question was ill-posed
QUESTIONS = {
    "had": ["Did {X} have {O}'s permission for what was done?", "Was what happened covered by {O}'s permission?"],
    "exceed": ["Did {X} go beyond what {O} had agreed to?", "Did what happened go beyond what {O} had agreed to?"],
    "est": ["Do the messages and events above establish that {O} had given permission for what was done?"],
}
DEFS = {
    "had": {"yes": "A permission given by the owner in words covered this exact use: same item, inside the stated time window, "
                   "an allowed purpose, only allowed people (guests, lending, password sharing count), condition met, not withdrawn first.",
            "no": "The use was not covered: permission came from someone other than the owner, was never clearly given (silence "
                  "or 'maybe'), was withdrawn earlier, or the use fell outside its item, time, purpose, person or condition."},
    "exceed": {"yes": "The use was not covered: permission came from someone other than the owner, was never clearly given "
                      "(silence or 'maybe'), was withdrawn earlier, or the use fell outside its item, time, purpose, person or condition.",
               "no": "A permission given by the owner in words covered this exact use: same item, inside the stated time "
                     "window, an allowed purpose, only allowed people (guests, lending, password sharing count), condition met, not withdrawn first."},
    "est": {"yes": "The stated messages and events are enough to show that the owner's permission covered this exact use, "
                   "including any condition the owner attached.",
            "no": "Either the use was outside the permission, or whether a condition the owner attached was met is not stated, "
                  "so coverage is not established."},
}


def gold(qid, v):
    if qid in ("had", "est"):
        return "yes" if v is True else "no"
    return "yes" if v is False else "no"


def main():
    rng = random.Random(SEED)
    s = Consent()
    rows, seen = [], set()
    made, tries = 0, 0
    while made < N_PAIRS and tries < 10 ** 6:
        tries += 1
        p = s.params(rng)
        f = s.facts(rng, p)
        if not s.valid(p, f):
            continue
        r = rng.random()
        qid = "had" if r < 0.40 else "exceed" if r < 0.76 else "est"
        if qid == "est" and rng.random() < 0.8:
            h = s.hide(p, f, rng)
            if h is None:
                continue
            base, twin = h, s.fill(p, h, want=True)
        else:
            if s.verdict(p, f) is None:
                continue
            base, twin = f, s.one_flip(p, f, rng)
            if twin is None:
                continue
        diff = [k for k in set(base) | set(twin) if base.get(k) != twin.get(k)]
        assert len(diff) == 1, diff
        vb, vt = s.verdict(p, base), s.verdict(p, twin)
        if qid != "est" and (vb is None or vt is None):
            continue
        gb, gt = gold(qid, vb), gold(qid, vt)
        if gb == gt:
            continue
        item_q = ITEMS[p["it"]]["item"]
        qv = rng.randrange(4)
        tmpl = QUESTIONS[qid][qv % len(QUESTIONS[qid])]
        q = tmpl.format(X=f["who"][0], O=f["owner"][0], item=item_q)
        sb = f"{s.rules(p)[1][0]}\n\n{s.story(p, base)}"
        st = f"{s.rules(p)[1][0]}\n\n{s.story(p, twin)}"
        if sb == st or sb in seen or st in seen:
            continue
        seen.update({sb, st})
        rid = f"{KEY}-{made:05d}"
        dims = {"window": WINDOWS[p["win"]][0], "excluded_purpose": p["excl"] is not None, "condition": p["cond"] is not None,
                "delegation_allowed": p["deleg"]}
        rows.append(row(KEY, rid, sb, q, gb, qid, edge_join(sorted(set(x for x in s.edges(p, base) if x))),
                        {"covered": vb, **dims}, f"consent:{qid}"))
        rows.append(row(KEY, rid + "-twin", st, q, gt, qid, edge_join(sorted(set(x for x in s.edges(p, twin) if x))),
                        {"covered": vt, "changed": diff[0], **dims}, f"consent:{qid}", twin_of=rid))
        made += 1
    print("pairs:", made, "tries:", tries)
    pairs = [rows[i:i + 2] for i in range(0, len(rows), 2)]
    rng.shuffle(pairs)
    rows = [r for pr in pairs for r in pr]
    write_gen(KEY, rows, DEFS,
              notes=("program-generated consent/permission scope: owner vs non-owner grants, silence and 'maybe' are not "
                     "consent, time windows (through a day, weekends only, weekday afternoons, tomorrow only, next week), "
                     "excluded purposes, no passing on unless allowed, conditions ('as long as ...'), withdrawal before use; "
                     "single-fact twins flip the answer (meta.twin_of)."),
              dataset_desc="gen_msn_consent (program generator, golden_src/gen/gen_msn_consent.py)")


if __name__ == "__main__":
    main()
