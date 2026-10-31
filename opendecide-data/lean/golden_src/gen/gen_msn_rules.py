"""gen_msn_rules: community / shared-space rules of conduct with conditions and exceptions (yes/no, labels by
construction, fact-flip twins).

Each item shows a short rulebook for a real-world setting (pool, apartment block, library, museum, gym, office
kitchen, campground, dog park, classroom, community garden, forum, exam hall, theatre, volunteer rota, beach, park,
parking lot, shared house, temple, workplace gift policy, library loans, condo pets, yard work, club meeting, hostel,
trail) - one relevant rule plus unrelated distractor rules - and a situation. A decision function computes whether
the person's action is allowed (True), a violation (False) or not decidable from the stated facts (None).

Questions (qid):
  allowed   "Under the rules above, was X allowed to <act>?"            yes <=> allowed
  violates  "Did X break the rules above by <acting>?"                  yes <=> violation
  est_ok    "Do the stated facts establish that X was allowed to ...?"  yes <=> allowed (None -> no)
  est_viol  "Do the stated facts establish that X broke the rules ...?" yes <=> violation (None -> no)
Every base item gets a twin (meta.twin_of) that changes ONE decisive fact (or removes / supplies the one missing
fact) so that the gold answer flips; each pair therefore has one yes and one no.
Edge cases: exceptions, 'unless', 'only if', thresholds at the boundary, overnight time windows, dates and weekdays,
public-holiday exceptions, units (feet vs metres vs yards, weeks vs months), quantifiers (at most, no one, all,
any), negation and double negation ('no one may ... without ...'), missing information, reported speech that
misstates the rule, permission from the wrong person, and look-alike items (alcohol-free beer, phone on silent vs
switched off). Deterministic (seed 20261102).
"""
import copy
import datetime as dt
import random
import re

from msn_common import (MONTHS, WEEKDAYS, cap, fmt_date, fmt_time, num, person, plural, row, write_gen)

KEY = "gen_msn_rules"
SEED = 20261102
N_PAIRS = 4000


def sty(f, k, n):
    return f["sty"][k] % n


class Schema:
    name = "base"
    can_hide = False

    def new_sty(self, rng):
        return {k: rng.randrange(10 ** 6) for k in "abcdefghij"}

    def distract(self, p, pool, k=2):
        rng = random.Random(p["dseed"])
        return rng.sample(pool, k)

    def hide(self, p, f, rng):
        return None

    def edges(self, p, f):
        return []

    def valid(self, p, f):
        return True

    def alts(self, p, f):
        return {}

    def one_flip(self, p, f, rng):
        """Change exactly ONE decisive fact so that the (determined) verdict flips; None if impossible."""
        v = self.verdict(p, f)
        cands = [(k, x) for k, xs in self.alts(p, f).items() for x in xs if x != f.get(k)]
        rng.shuffle(cands)
        for k, x in cands:
            g = copy.deepcopy(f)
            g[k] = x
            if not self.valid(p, g):
                continue
            w = self.verdict(p, g)
            if w is not None and w != v:
                return g
        return None


# ---------------------------------------------------------------------------------------------------------------
class PoolGuests(Schema):
    name = "pool_guests"
    can_hide = True
    POOLS = ["Oakridge Community Pool", "Harbor View Residents' Pool", "Maple Court Pool", "Sunnyside Swim Club",
             "Linden Terrace Pool", "Cedar Park Residents' Pool"]
    DIS = ["Glass containers are not allowed on the pool deck.", "Children under 8 must be supervised by an adult in the water.",
           "Diving is allowed only at the deep end.", "Lounge chairs may not be reserved with towels.",
           "Pets are not allowed inside the pool fence."]

    def params(self, rng):
        k = rng.choice([1, 2, 3])
        return {"k": k, "pk": k + rng.choice([3, 5, 7]), "rd": rng.choice([2, 3, 5, 7]), "phr": rng.randrange(3),
                "place": rng.choice(self.POOLS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        k, pk, rd = p["k"], p["pk"], p["rd"]
        g = plural(k, "guest")
        rel = [f"Each resident may bring at most {k} {g} to the pool at a time. For a birthday party, a resident may "
               f"bring up to {pk} guests, but only if the party area was reserved at least {rd} days in advance.",
               f"No resident may have more than {k} {g} at the pool at once, unless the resident is holding a birthday "
               f"party in the party area and reserved it {rd} or more days beforehand; in that case up to {pk} guests are allowed.",
               f"Guest limit: {k} per resident. Exception: a birthday party may have up to {pk} guests if the party "
               f"area was booked at least {rd} days ahead."][p["phr"]]
        return f"Rules for residents - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        r = rng.random()
        if r < 0.3:
            f.update(n=rng.randint(1, p["k"]), party=False, booked="none")
        elif r < 0.55:
            f.update(n=rng.randint(p["k"] + 1, p["pk"] + 2), party=False, booked="none")
        else:
            f.update(n=rng.randint(p["k"] + 1, p["pk"] + 2), party=True,
                     booked=rng.choice([p["rd"] - 1, p["rd"], p["rd"] + rng.randint(1, 10), 0, "none"]))
            if f["booked"] == 0 and p["rd"] - 1 == 0:
                f["booked"] = "none"
        return f

    def alts(self, p, f):
        k, pk, rd = p["k"], p["pk"], p["rd"]
        return {"n": [1, k, k + 1, pk, pk + 1], "party": [True, False], "booked": [0, rd - 1, rd, rd + 3, "none"]}

    def valid(self, p, f):
        b = f["booked"]
        return f["n"] >= 1 and (f["party"] or b == "none") and (not isinstance(b, int) or b >= 0)

    def verdict(self, p, f):
        if f["n"] <= p["k"]:
            return True
        if not f["party"] or f["n"] > p["pk"]:
            return False
        if f["booked"] == "unknown":
            return None
        if f["booked"] in (None, "none"):
            return False
        return f["booked"] >= p["rd"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        n = f["n"]
        who_n = num(n, random.Random(f["sty"]["a"]))
        day = ["Saturday", "Sunday", "a hot Friday afternoon", "the first day of summer break"][sty(f, "b", 4)]
        if f["party"]:
            kid = ["daughter", "son", "niece", "nephew"][sty(f, "c", 4)]
            s = f"On {day}, {name} held {pos} {kid}'s birthday party at the pool and brought {who_n} {plural(n, 'guest')}."
            if f["booked"] == "none":
                s += f" {cap(sub)} had not reserved the party area; the group simply used it because it was free."
            elif f["booked"] == "unknown":
                s += " The group gathered in the party area next to the shallow end."
            elif f["booked"] == 0:
                s += f" {cap(sub)} reserved the party area that same morning."
            else:
                s += f" {cap(sub)} had reserved the party area {num(f['booked'], random.Random(f['sty']['d']))} {plural(f['booked'], 'day')} before the party."
        else:
            i = sty(f, "c", 4)
            if n == 1:
                what = ["a friend from work", "a cousin who was visiting", "a neighbour from the next street", "a classmate"][i]
            else:
                what = who_n + " " + ["friends from work", "cousins who were visiting", "neighbours from the next street", "classmates"][i]
            s = f"On {day}, {name} brought {what} to the pool as {pos} {plural(n, 'guest')}. It was not a party, just an afternoon swim."
        s += [" They stayed for about two hours.", " Everyone had left by six.", " The lifeguard was on duty the whole time."][sty(f, "e", 3)]
        return s

    def act(self, p, f):
        return "bring those guests to the pool", "bringing those guests to the pool"

    def hide(self, p, f, rng):
        if f["party"] and p["k"] < f["n"] <= p["pk"] and f["booked"] != "unknown":
            g = copy.deepcopy(f)
            g["booked"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["booked"] = p["rd"] + 1 if want else p["rd"] - 1
        return g

    def edges(self, p, f):
        t = ["numeric", "quantifier"]
        if f["party"]:
            t.append("exception")
        if f["booked"] == "unknown":
            t.append("missing_info")
        return t


# ---------------------------------------------------------------------------------------------------------------
class QuietHours(Schema):
    name = "quiet_hours"
    can_hide = True
    BLDG = ["Willow Court Apartments", "Riverbend Lofts", "The Alder Building", "Northgate Flats", "Birchwood Residences"]
    DIS = ["Bicycles must be kept in the bike room, not in hallways.", "Rubbish must be taken to the bins in the basement.",
           "Smoking is not allowed on balconies.", "Moving furniture in or out requires booking the service lift.",
           "Laundry machines may be used between 7 a.m. and 10 p.m."]

    def params(self, rng):
        return {"start": rng.choice([21, 22, 23]) * 60, "end": rng.choice([6, 7, 8]) * 60, "nye": rng.random() < 0.35,
                "ts": rng.randrange(3), "phr": rng.randrange(2), "place": rng.choice(self.BLDG), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        s, e = fmt_time(p["start"] // 60, 0, p["ts"]), fmt_time(p["end"] // 60, 0, p["ts"])
        rel = [f"Quiet hours run from {s} until {e} every night (they begin at {s} sharp and end at {e} sharp). During "
               f"quiet hours, residents must not play music or make noise that can be heard outside their own apartment.",
               f"Between {s} and {e} (quiet hours, starting at {s} exactly and ending at {e} exactly), no resident may "
               f"make noise or play music that can be heard from outside their apartment."][p["phr"]]
        lines = [rel]
        if p["nye"]:
            lines.append(f"On New Year's Eve (December 31), quiet hours start at {fmt_time(1, 0, p['ts'])} on January 1 instead.")
        return f"House rules - {p['place']}", lines + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["nyedate"] = p["nye"] and rng.random() < 0.5
        f["audible"] = rng.random() < 0.6
        if f["nyedate"]:
            f["t"] = rng.choice([p["start"] - 30, p["start"], p["start"] + 15, 23 * 60 + 50, 60 * 24 + 30, 60 * 24 + 60,
                                 60 * 24 + 90])
        else:
            f["t"] = rng.choice([p["start"] - rng.choice([10, 30, 60]), p["start"], p["start"] + rng.choice([5, 40, 90]),
                                 p["end"] - rng.choice([15, 60]) + 24 * 60, p["end"] + 24 * 60, p["end"] + rng.choice([20, 45]) + 24 * 60])
        return f

    def in_quiet(self, p, f):
        t = f["t"]  # minutes after midnight of the evening's date (may exceed 1440 = next morning)
        start = p["start"]
        if f["nyedate"]:
            start = 24 * 60 + 60  # 1 a.m. on Jan 1
        end = p["end"] + 24 * 60
        return start <= t < end

    def alts(self, p, f):
        if f["nyedate"]:
            ts = [p["start"] - 30, 23 * 60 + 50, 24 * 60 + 30, 24 * 60 + 60, 24 * 60 + 90]
        else:
            ts = [p["start"] - 30, p["start"], p["start"] + 30, p["end"] - 30 + 24 * 60, p["end"] + 24 * 60]
        return {"t": ts, "audible": [True, False]}

    def verdict(self, p, f):
        if not self.in_quiet(p, f):
            return True
        if f["audible"] == "unknown":
            return None
        return not f["audible"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        t = f["t"]
        h, m = (t // 60) % 24, t % 60
        ts = sty(f, "a", 3)
        clock = fmt_time(h, m, ts)
        if f["nyedate"]:
            when = (f"on December 31 at {clock}" if t < 24 * 60 else f"at {clock} on January 1, after the New Year's Eve countdown")
        else:
            i = [1, 2, 3, 5, 6][sty(f, "b", 5)]
            when = (f"on {WEEKDAYS[i]} evening at {clock}" if t < 24 * 60 else
                    f"at {clock} on {WEEKDAYS[(i + 1) % 7]} morning")
        act = ["played music", "practised the drums", "had friends over for karaoke", "ran a video game session with friends"][sty(f, "c", 4)]
        s = f"{name} {act} {when}."
        if f["audible"] is True:
            s += [f" The neighbours across the hall could hear it clearly.", f" It was loud enough to be heard in the stairwell.",
                  f" The downstairs neighbour could hear every beat."][sty(f, "d", 3)]
        elif f["audible"] is False:
            s += [f" {cap(sub)} used headphones, so no sound left the apartment.", f" Everything was kept so quiet that nothing could be heard outside {pos} door.",
                  f" {cap(sub)} had the volume so low that nobody outside the apartment could hear it."][sty(f, "d", 3)]
        else:
            s += f" {cap(sub)} was in the living room at the time."
        return s

    def act(self, p, f):
        return "do that at that time", "doing that at that time"

    def hide(self, p, f, rng):
        if self.in_quiet(p, f) and f["audible"] in (True, False):
            g = copy.deepcopy(f)
            g["audible"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["audible"] = not want
        return g

    def edges(self, p, f):
        t = ["temporal", "negation"]
        if f["nyedate"]:
            t.append("exception")
        if f["t"] in (p["start"], p["end"] + 24 * 60):
            t.append("numeric")
        if f["audible"] == "unknown":
            t.append("missing_info")
        return t


# ---------------------------------------------------------------------------------------------------------------
class LibraryCalls(Schema):
    name = "library_calls"
    LIBS = ["Eastside Public Library", "Central City Library", "Hillcrest Branch Library", "University Main Library"]
    DIS = ["Group-study rooms may be booked for at most two hours per day.", "Books must be returned to the front desk or the return slot.",
           "Printing costs 10 cents per page.", "Bags larger than a backpack must be left in the lockers."]
    LOC = {"reading": ["the main reading room", "the silent study floor", "the periodicals reading room"],
           "ok": ["the lobby", "the stairwell", "a group-study room", "the entrance hall"]}

    def params(self, rng):
        return {"phr": rng.randrange(3), "staff_exc": rng.random() < 0.4, "place": rng.choice(self.LIBS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Phone calls are not allowed in the reading rooms or on the silent study floor. Calls may be taken in the lobby, "
               "the stairwells, the entrance hall or a group-study room. Texting is fine everywhere.",
               "No one may take or make a phone call (voice or video) in any reading room or on the silent study floor; step "
               "out to the lobby, entrance hall, a stairwell or a group-study room instead. Silent texting is allowed everywhere.",
               "Reading rooms and the silent study floor are call-free zones: voice and video calls are not permitted there. "
               "Messaging without sound is permitted anywhere in the building."][p["phr"]]
        lines = [rel]
        if p["staff_exc"]:
            lines.append("Library staff on duty may take work calls anywhere in the building.")
        return f"Visitor rules - {p['place']}", lines + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["activity"] = rng.choice(["voice call", "video call", "texting", "voice call", "video call"])
        f["zone"] = rng.choice(["reading", "reading", "ok"])
        f["loc"] = rng.randrange(4)
        f["staff"] = p["staff_exc"] and rng.random() < 0.4
        f["hearsay"] = rng.random() < 0.2
        return f

    def alts(self, p, f):
        a = {"activity": ["voice call", "video call", "texting"], "zone": ["reading", "ok"]}
        if p["staff_exc"]:
            a["staff"] = [True, False]
        return a

    def verdict(self, p, f):
        if f["activity"] == "texting" or f["zone"] == "ok":
            return True
        if f["staff"] and p["staff_exc"]:
            return True
        return False

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        loc = self.LOC[f["zone"]][f["loc"] % len(self.LOC[f["zone"]])]
        role = (f"{name}, a librarian on duty that afternoon," if f["staff"] else
                [f"{name}, a student preparing for exams,", f"{name}, a regular visitor,", f"{name}"][sty(f, "a", 3)])
        what = {"voice call": [f"answered a voice call from {pos} manager", "took a phone call from a friend", "made a quick call to a plumber"][sty(f, "b", 3)],
                "video call": ["joined a video call with classmates", "took a short video call from family", "started a video call with a tutor"][sty(f, "b", 3)],
                "texting": ["spent ten minutes texting a friend with the sound off", "replied to messages silently", "sent a few text messages with the phone on mute"][sty(f, "b", 3)]}[f["activity"]]
        if f["staff"] and f["activity"] != "texting":
            # staff exception covers WORK calls only, so staff calls are always work calls
            what = {"voice call": ["took a work call about a book delivery", "answered a call from the library's head office",
                                   "phoned the maintenance team about a broken light"][sty(f, "b", 3)],
                    "video call": ["joined a video meeting with the library's IT team", "took a short video call from the head office",
                                   "joined a video call with another branch's manager about opening hours"][sty(f, "b", 3)]}[f["activity"]]
        s = f"{role} {what} while {'on' if 'floor' in loc else 'in'} {loc}."
        if f["hearsay"]:
            s += [" A friend had told " + obj + " that calls are fine anywhere as long as they are short.",
                  " Someone at the next table said the call rule is only enforced during exam season."][sty(f, "c", 2)]
        return s

    def act(self, p, f):
        return "do that where " + f["who"][1] + " did", "doing that where " + f["who"][1] + " did"

    def edges(self, p, f):
        t = ["exception", "negation"]
        if f["hearsay"]:
            t.append("reported_speech")
        return t


# ---------------------------------------------------------------------------------------------------------------
class MuseumPhoto(Schema):
    name = "museum_photo"
    can_hide = True
    MUS = ["the City Museum of Art", "the Harborside Museum", "the National Gallery of Crafts", "the Riverside History Museum"]
    PERM = ["the permanent Egyptian gallery", "the permanent collection's Impressionist room", "the permanent textiles gallery",
            "the permanent ceramics hall"]
    SPEC = ["the special exhibition 'Colours of the Silk Road'", "the temporary exhibition 'Machines of Tomorrow'",
            "the special exhibition 'Masks of West Africa'", "the touring exhibition 'Ice Age Giants'"]
    AMB = ["the Monet room", "the hall with the dinosaur skeleton", "the gallery of Japanese prints", "the sculpture court"]
    DIS = ["Backpacks must be worn on the front or left in the cloakroom.", "Food and drink are allowed only in the café.",
           "Please do not touch the artworks.", "Tripods and selfie sticks are not allowed."]

    def params(self, rng):
        return {"phr": rng.randrange(2), "place": rng.choice(self.MUS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Photography without flash is welcome in the permanent collection. Photography of any kind is not permitted "
               "in special or temporary exhibitions. Flash photography is not permitted anywhere in the museum.",
               "You may take photos without flash in all permanent-collection galleries. No photos at all may be taken in "
               "special, temporary or touring exhibitions, and flash is never allowed in any gallery."][p["phr"]]
        dis = [d for d in self.DIS if "Tripods" not in d]
        return f"Visitor guidelines - {p['place']}", [rel] + self.distract(p, dis)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["gtype"] = rng.choice(["perm", "spec", "perm", "spec"])
        f["flash"] = rng.random() < 0.3
        return f

    def alts(self, p, f):
        return {"gtype": ["perm", "spec"], "flash": [True, False]}

    def verdict(self, p, f):
        if f["flash"]:
            return False
        if f["gtype"] == "unknown":
            return None
        return f["gtype"] == "perm"

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        g = {"perm": self.PERM, "spec": self.SPEC, "unknown": self.AMB}[f["gtype"]][sty(f, "a", 4)]
        what = ["photographed a painting", "took a few pictures of the display cases", "snapped a photo of a statue for " + pos + " sister"][sty(f, "b", 3)]
        fl = ", with the flash on" if f["flash"] else [" without flash", ", with the flash switched off", ", making sure the flash was off"][sty(f, "c", 3)]
        return f"During a visit to {p['place']}, {name} {what} in {g}{fl}."

    def act(self, p, f):
        return "take those photos", "taking those photos"

    def hide(self, p, f, rng):
        if not f["flash"] and f["gtype"] in ("perm", "spec"):
            g = copy.deepcopy(f)
            g["gtype"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["gtype"] = "perm" if want else "spec"
        return g

    def edges(self, p, f):
        t = ["negation", "quantifier", "exception"]
        if f["gtype"] == "unknown":
            t.append("missing_info")
        return t


# ---------------------------------------------------------------------------------------------------------------
class GymMinors(Schema):
    name = "gym_minors"
    can_hide = True
    GYMS = ["FitLife Community Gym", "the Northside Leisure Centre", "Peak Performance Gym", "the YMCA on Elm Street"]
    DIS = ["Wipe down equipment after use.", "Towels are required on all benches.", "Lockers must be emptied by closing time.",
           "Personal trainers from outside the gym may not coach on the premises."]

    def params(self, rng):
        return {"age": rng.choice([14, 16, 18]), "phr": rng.randrange(3), "place": rng.choice(self.GYMS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        a = p["age"]
        rel = [f"Members under {a} may use the weight room only when accompanied by a parent, a legal guardian or a staff trainer.",
               f"No one younger than {a} may use the weight room unless a parent, legal guardian or staff trainer is with them.",
               f"Weight room: members aged {a} and over may train on their own; younger members must be accompanied by a parent, "
               f"legal guardian or staff trainer. The pool and cardio area have no age rule."][p["phr"]]
        return f"Membership rules - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["age"] = rng.choice([p["age"] - 2, p["age"] - 1, p["age"] - 1, p["age"], p["age"] + 1, p["age"] + 3])
        f["age_style"] = rng.random() < 0.3  # express via birth date
        f["comp"] = rng.choice(["parent", "guardian", "trainer", "sibling", "friend", "none", "none"])
        f["area"] = rng.choice(["weights", "weights", "weights", "pool"])
        return f

    def alts(self, p, f):
        a = p["age"]
        return {"age": [a - 2, a - 1, a, a + 1], "comp": ["parent", "guardian", "trainer", "sibling", "friend", "none"],
                "area": ["weights", "pool"]}

    def verdict(self, p, f):
        if f["area"] != "weights" or f["age"] >= p["age"]:
            return True
        if f["comp"] == "unknown":
            return None
        return f["comp"] in ("parent", "guardian", "trainer")

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        today = dt.date(2025, 3, 12) + dt.timedelta(days=sty(f, "a", 200))
        if f["age_style"]:
            # birthday chosen so that the age on `today` equals f["age"]
            # birth month strictly before the current month, so the age is unambiguous from month + year
            if today.month > 1:
                bday = dt.date(today.year - f["age"], today.month - 1, 1)
            else:
                bday = dt.date(today.year - f["age"] - 1, 12, 1)
            agetxt = f"{name} (born {MONTHS[bday.month - 1]} {bday.year})"
            when = f"On {fmt_date(today, sty(f, 'c', 2), weekday=False)}, {today.year}, "
        else:
            agetxt = [f"{name}, who is {f['age']},", f"{f['age']}-year-old {name}", f"{name} ({f['age']} years old)"][sty(f, "b", 3)]
            when = ["After school, ", "On Saturday morning, ", "One evening, "][sty(f, "c", 3)]
        place = "the weight room" if f["area"] == "weights" else ["the pool", "the cardio area"][sty(f, "d", 2)]
        act = {"weights": "lifted weights in", "pool": "trained in"}[f["area"]]
        comp = {"parent": f" with {pos} {['mother', 'father'][sty(f, 'e', 2)]}", "guardian": f" with {pos} legal guardian",
                "trainer": " with one of the gym's staff trainers", "sibling": f" with {pos} 19-year-old {['brother', 'sister'][sty(f, 'e', 2)]}",
                "friend": f" with a friend from school", "none": " alone", "unknown": ""}[f["comp"]]
        s = f"{when}{agetxt} {act} {place}{comp}."
        if f["comp"] == "sibling":
            s += f" {cap(pos)} {['brother', 'sister'][sty(f, 'e', 2)]} is not a staff trainer."
        return s

    def act(self, p, f):
        return "train there", "training there"

    def hide(self, p, f, rng):
        if f["area"] == "weights" and f["age"] < p["age"] and f["comp"] != "unknown":
            g = copy.deepcopy(f)
            g["comp"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["comp"] = "trainer" if want else "none"
        return g

    def edges(self, p, f):
        t = ["numeric", "exception"]
        if f["age_style"]:
            t.append("temporal")
        if f["comp"] == "sibling":
            t.append("implicit")
        if f["comp"] == "unknown":
            t.append("missing_info")
        return t


# ---------------------------------------------------------------------------------------------------------------
class FridgeFood(Schema):
    name = "fridge_food"
    OFF = ["Brightline Design Studio", "the Kessler & Moe accounting office", "the third-floor office at Novatek", "the Greenfield Clinic staff room"]
    DIS = ["Unlabelled food is cleared out every Friday at 5 p.m.", "The dishwasher must be emptied by whoever finds it clean.",
           "Microwave use is limited to three minutes when others are waiting.", "Coffee pods are provided free of charge."]

    def params(self, rng):
        return {"phr": rng.randrange(3), "place": rng.choice(self.OFF), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Do not take food or drinks from the shared fridge that belong to someone else, unless the owner has told you "
               "that you may. Anything on the top shelf labelled 'free for all' may be taken by anyone.",
               "Food in the shared fridge belongs to whoever put it there; no one may take someone else's food without the "
               "owner's permission. Exception: items on the 'free for all' top shelf.",
               "Help yourself only to your own food, to anything the owner has said you may have, and to the 'free for all' top shelf."][p["phr"]]
        return f"Kitchen rules - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["owner"] = person(rng, exclude=(f["who"][0],))
        f["kind"] = rng.choice(["own", "free", "other", "other", "other"])
        f["perm"] = rng.choice(["owner", "none", "assumed", "coworker", "owner"]) if f["kind"] == "other" else "none"
        return f

    def alts(self, p, f):
        return {"kind": ["own", "free"] if f["kind"] == "other" else ["other"], "perm": ["owner", "none", "assumed", "coworker"]}

    def valid(self, p, f):
        return f["kind"] == "other" or f["perm"] == "none"

    def verdict(self, p, f):
        if f["kind"] in ("own", "free"):
            return True
        return f["perm"] == "owner"

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        oname = f["owner"][0]
        item = ["a yogurt", "half a sandwich", "a can of sparkling water", "a slice of cake", "some leftover curry"][sty(f, "a", 5)]
        if f["kind"] == "own":
            refl = {"she": "herself", "he": "himself", "they": "themselves"}[sub]
            return f"{name} took {item} from the shared fridge. {cap(sub)} had put it there {refl} that morning."
        if f["kind"] == "free":
            return f"{name} took {item} from the top shelf of the shared fridge, which was labelled 'free for all'. {oname} had left it there."
        s = f"{name} took {item} from the shared fridge. It was {oname}'s; {oname}'s name was on the lid."
        s += {"owner": [f" Earlier that day {oname} had told {obj} to help {obj}self to it.", f" {oname} had messaged {obj}: 'Take it, I won't eat it.'"][sty(f, "b", 2)],
              "none": [f" {name} did not ask anyone.", f" Nobody had said {sub} could have it."][sty(f, "b", 2)],
              "assumed": [f" {name} assumed {oname} would not mind, but did not ask.", f" {name} figured it was probably going to be thrown out anyway and did not check with {oname}."][sty(f, "b", 2)],
              "coworker": [f" Another colleague, not {oname}, told {obj} it was fine to take it.", f" The office manager said {sub} could probably take it; {oname} was not asked."][sty(f, "b", 2)]}[f["perm"]]
        return s.replace("them self", "themselves").replace("him self", "himself").replace("her self", "herself").replace("themself", "themselves")

    def act(self, p, f):
        return "take that food", "taking that food"

    def edges(self, p, f):
        t = ["exception", "negation"]
        if f["perm"] in ("assumed", "coworker"):
            t.append("implicit")
        return t


# ---------------------------------------------------------------------------------------------------------------
class Campfire(Schema):
    name = "campfire"
    can_hide = True
    CAMPS = ["Pine Hollow Campground", "Lakeshore State Campground", "Bear Creek Campground", "Red Rock Canyon Campground"]
    DIS = ["Quiet hours are from 10 p.m. to 6 a.m.", "Food must be stored in the bear lockers overnight.",
           "Check-out time is 11 a.m.", "Generators may run only between 8 a.m. and 8 p.m."]

    def params(self, rng):
        return {"phr": rng.randrange(2), "place": rng.choice(self.CAMPS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Campfires are allowed only inside the metal fire ring at each campsite, and never when the fire-danger rating "
               "posted at the entrance is High or Extreme. Gas camp stoves may be used at any rating.",
               "Wood fires: only in the steel fire rings, and not at all on days when the posted fire-danger rating is High or "
               "Extreme. Gas stoves are exempt from the fire-danger restriction."][p["phr"]]
        return f"Campground regulations - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["kind"] = rng.choice(["fire", "fire", "fire", "stove"])
        f["ring"] = rng.random() < 0.7
        f["rating"] = rng.choice(["Low", "Moderate", "High", "Extreme"])
        return f

    def alts(self, p, f):
        return {"kind": ["fire", "stove"], "ring": [True, False], "rating": ["Low", "Moderate", "High", "Extreme"]}

    def verdict(self, p, f):
        if f["kind"] == "stove":
            return True
        if not f["ring"]:
            return False
        if f["rating"] == "unknown":
            return None
        return f["rating"] in ("Low", "Moderate")

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        rating = {"unknown": ""}.get(f["rating"], f"The fire-danger sign at the entrance read '{f['rating']}' that day. ")
        if f["kind"] == "stove":
            what = f"{name} cooked dinner on a gas camp stove at {pos} campsite."
        else:
            where = ["inside the metal fire ring", "in the campsite's steel fire ring"][sty(f, "a", 2)] if f["ring"] else \
                ["on the gravel next to the tent, a few metres from the fire ring", "in a small pit " + sub + " dug by the picnic table"][sty(f, "a", 2)]
            what = f"{name} lit a small wood campfire {where} to roast marshmallows."
        order = sty(f, "b", 2)
        return (rating + what) if order else (what + (" " + rating.strip() if rating else ""))

    def act(self, p, f):
        return "do that", "doing that"

    def hide(self, p, f, rng):
        if f["kind"] == "fire" and f["ring"] and f["rating"] != "unknown":
            g = copy.deepcopy(f)
            g["rating"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["rating"] = "Moderate" if want else "High"
        return g

    def edges(self, p, f):
        t = ["negation", "exception"]
        if f["rating"] == "unknown":
            t.append("missing_info")
        return t


# ---------------------------------------------------------------------------------------------------------------
class DogPark(Schema):
    name = "dog_park"
    PARKS = ["Riverside Park", "Greenway Commons", "Hilltop Park", "Willowbrook Park"]
    DIS = ["Owners must pick up after their dogs.", "The park closes at dusk.", "No more than three dogs per person.",
           "Dogs must be vaccinated and wear a licence tag."]

    def params(self, rng):
        return {"months": rng.choice([4, 6]), "phr": rng.randrange(2), "place": rng.choice(self.PARKS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        m = p["months"]
        rel = [f"Dogs must be on a leash everywhere in the park except inside the fenced off-leash area. Puppies younger than "
               f"{m} months are not allowed in the off-leash area. Dogs are not allowed in the children's playground at all.",
               f"Leashes are required on all paths and lawns. Inside the fenced off-leash area dogs may run free, but only dogs "
               f"at least {m} months old may enter it. No dogs, leashed or not, in the playground."][p["phr"]]
        dis = [d for d in self.DIS if "three dogs" not in d]
        return f"Park rules - {p['place']}", [rel] + self.distract(p, dis)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["loc"] = rng.choice(["paths", "paths", "offleash", "offleash", "playground"])
        f["leash"] = rng.random() < 0.5
        mo = p["months"]
        f["age_weeks"] = rng.choice([mo * 4 - 6, mo * 4 - 2, mo * 4 + 5, mo * 4 + 20, 60, 150])
        f["units"] = rng.choice(["weeks", "months", "years"])
        return f

    def age_months(self, f):
        return f["age_weeks"] / 4.345

    def alts(self, p, f):
        m = p["months"]
        return {"loc": ["paths", "offleash", "playground"], "leash": [True, False], "age_weeks": [m * 4 - 2, m * 4 + 20]}

    def verdict(self, p, f):
        if f["loc"] == "playground":
            return False
        if f["loc"] == "offleash":
            return self.age_months(f) >= p["months"]
        return f["leash"]

    def age_text(self, f):
        w = f["age_weeks"]
        if f["units"] == "weeks" or w < 20:
            return f"{w}-week-old"
        mo = w / 4.345
        if f["units"] == "months" or w < 104:
            return f"{int(mo)}-month-old"
        return f"{int(w // 52)}-year-old"

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        dog = ["beagle", "labrador", "terrier mix", "border collie", "spaniel"][sty(f, "a", 5)]
        at = self.age_text(f)
        where = {"paths": ["walked along the main path", "crossed the big lawn"][sty(f, "b", 2)],
                 "offleash": ["went into the fenced off-leash area", "spent half an hour in the fenced off-leash area"][sty(f, "b", 2)],
                 "playground": ["walked through the children's playground", "sat on a bench inside the children's playground"][sty(f, "b", 2)]}[f["loc"]]
        leash = " with the dog on a leash" if f["leash"] else " and let the dog run off the leash"
        return f"{name} {where} with {pos} {at} {dog}{leash}."

    def act(self, p, f):
        return "be there with the dog like that", "being there with the dog like that"

    def edges(self, p, f):
        t = ["exception", "negation"]
        if f["loc"] == "offleash":
            t += ["numeric"] + (["units"] if f["units"] == "weeks" or f["age_weeks"] < 20 else [])
        return t


# ---------------------------------------------------------------------------------------------------------------
class ClassPhones(Schema):
    name = "class_phones"
    can_hide = True
    SCH = ["Westfield High School", "Lincoln Middle School", "St. Brendan's Academy", "Oakview Secondary School"]
    DIS = ["Students must wear their ID badges on campus.", "Food is not allowed in the computer lab.",
           "Late arrivals must sign in at the front office.", "Lockers must be locked at all times."]

    def params(self, rng):
        return {"phr": rng.randrange(3), "place": rng.choice(self.SCH), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Students must not use their phones during class unless the teacher has allowed it for a class activity or "
               "there is a medical emergency. Phones may be used freely during breaks and lunch.",
               "No student may use a phone during class without the teacher's permission, except in a medical emergency. "
               "There is no phone restriction during breaks or lunch.",
               "Phones stay away during lessons. The only exceptions: a class activity the teacher has approved for phone "
               "use, or a medical emergency. Breaks and lunch are phone-friendly."][p["phr"]]
        return f"Student handbook - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["when"] = rng.choice(["class", "class", "class", "break"])
        f["perm"] = rng.choice(["yes", "no", "no", "other_teacher", "assumed"])
        f["emerg"] = rng.random() < 0.15
        return f

    def alts(self, p, f):
        return {"when": ["class", "break"], "perm": ["yes", "no", "other_teacher", "assumed"], "emerg": [True, False]}

    def verdict(self, p, f):
        if f["when"] == "break" or f["emerg"]:
            return True
        if f["perm"] == "unknown":
            return None
        return f["perm"] == "yes"

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        subj = ["chemistry", "history", "maths", "Spanish", "biology"][sty(f, "a", 5)]
        when = {"class": f"During {pos} {subj} class,", "break": ["During the morning break,", "At lunch,"][sty(f, "b", 2)]}[f["when"]]
        use = ["checked the class group chat on " + pos + " phone", "used " + pos + " phone to look up a word",
               "took a photo of the board with " + pos + " phone", "sent a message on " + pos + " phone"][sty(f, "c", 4)]
        if f["emerg"]:
            use = "used " + pos + " phone to call for help when a classmate collapsed"
        s = f"{when} {name} {use}."
        if f["when"] == "class" and not f["emerg"]:
            s += {"yes": [f" The teacher had told the class to use their phones for this activity.", f" The {subj} teacher had approved phones for the exercise."][sty(f, "d", 2)],
                  "no": [" The teacher had not given permission.", " The teacher had said nothing about phones that day."][sty(f, "d", 2)],
                  "other_teacher": [f" A different teacher had said in the corridor that morning that phones were fine; the {subj} teacher had not said so.",
                                    f" {cap(pos)} {subj} teacher had not allowed it, although the maths teacher lets students use phones."][sty(f, "d", 2)],
                  "assumed": [f" {cap(sub)} assumed it was fine because the lesson was almost over.", f" {cap(sub)} thought a quick check would not count."][sty(f, "d", 2)],
                  "unknown": ""}[f["perm"]]
        return s

    def act(self, p, f):
        return "use the phone then", "using the phone then"

    def hide(self, p, f, rng):
        if f["when"] == "class" and not f["emerg"] and f["perm"] != "unknown":
            g = copy.deepcopy(f)
            g["perm"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["perm"] = "yes" if want else "no"
        return g

    def edges(self, p, f):
        t = ["exception", "negation"]
        if p["phr"] == 1:
            t.append("double_negation")
        if f["perm"] in ("other_teacher", "assumed"):
            t.append("implicit")
        if f["perm"] == "unknown":
            t.append("missing_info")
        return t


# ---------------------------------------------------------------------------------------------------------------
class Garden(Schema):
    name = "community_garden"
    GARDENS = ["Elm Street Community Garden", "Sunflower Allotments", "Riverside Community Garden", "Parkview Allotment Society"]
    DIS = ["Hoses must be coiled after use.", "Compost bins are for plant waste only.", "The gate must be locked when leaving.",
           "Pesticides are not allowed."]

    def params(self, rng):
        return {"phr": rng.randrange(2), "place": rng.choice(self.GARDENS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Members may harvest from their own plot and from the shared herb bed. Harvesting from another member's plot "
               "is not allowed unless that plot's holder has given permission. Non-members may not harvest anything, even with permission.",
               "Each member harvests only their own plot, plus the shared herb bed, which is open to all members. Another "
               "member's plot is off limits without that member's permission. People who are not members may not pick anything."][p["phr"]]
        return f"Garden rules - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["holder"] = person(rng, exclude=(f["who"][0],))
        f["member"] = rng.random() < 0.8
        f["bed"] = rng.choice(["own", "herb", "other", "other", "other"])
        f["perm"] = rng.choice(["holder", "none", "coordinator", "holder"]) if f["bed"] == "other" else "none"
        return f

    def alts(self, p, f):
        return {"member": [True, False], "bed": ["own", "herb"] if f["bed"] == "other" else ["other"],
                "perm": ["holder", "none", "coordinator"]}

    def valid(self, p, f):
        return f["bed"] == "other" or f["perm"] == "none"

    def verdict(self, p, f):
        if not f["member"]:
            return False
        if f["bed"] in ("own", "herb"):
            return True
        return f["perm"] == "holder"

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        h = f["holder"][0]
        crop = ["tomatoes", "a courgette", "some strawberries", "a bunch of kale", "two cucumbers"][sty(f, "a", 5)]
        mem = ("" if f["member"] else [f" {name} is not a member of the garden; {sub} was visiting a friend who is.",
                                       f" {name} is not a garden member."][sty(f, "b", 2)])
        if f["bed"] == "own":
            s = f"{name} picked {crop} from {pos} own plot." if f["member"] else f"{name} picked {crop} from the plot {sub} helps a member look after."
        elif f["bed"] == "herb":
            s = f"{name} picked some basil and mint from the shared herb bed."
        else:
            s = f"{name} picked {crop} from {h}'s plot."
            s += {"holder": [f" {h} had told {obj} to take whatever was ripe.", f" {h} had texted: 'Please harvest my plot while I'm away.'"][sty(f, "c", 2)],
                  "none": [f" {h} did not know about it.", f" Nobody had given {obj} permission."][sty(f, "c", 2)],
                  "coordinator": [f" The garden coordinator said it would be fine; {h} was not asked.", f" Another member told {obj} {h} wouldn't mind; {h} had not said anything."][sty(f, "c", 2)]}[f["perm"]]
        return s + mem

    def act(self, p, f):
        return "harvest that", "harvesting that"

    def edges(self, p, f):
        t = ["exception", "negation"]
        if f["perm"] == "coordinator":
            t.append("implicit")
        if not f["member"] and f["perm"] == "holder":
            t.append("multi_hop")
        return t


# ---------------------------------------------------------------------------------------------------------------
class SmokingDistance(Schema):
    name = "smoking_distance"
    BLDG = ["Harbour Point Condominiums", "the Midtown Office Tower", "Lakeview Apartments", "the Parkside Medical Building"]
    DIS = ["Visitors must sign in at reception.", "Deliveries use the rear loading dock.", "Bicycles may not be locked to the railings.",
           "The roof terrace closes at 10 p.m."]

    def params(self, rng):
        return {"ft": rng.choice([15, 20, 25, 30]), "ecig": rng.random() < 0.6, "place": rng.choice(self.BLDG), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        e = ("E-cigarettes and vaping count as smoking under this rule." if p["ecig"] else
             "This rule covers tobacco smoking only; vaping is not covered.")
        rel = f"Smoking is prohibited in all indoor common areas and within {p['ft']} feet of any building entrance. {e}"
        return f"Building policy - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["prod"] = rng.choice(["cigarette", "cigarette", "vape"])
        f["where"] = rng.choice(["indoor", "outside", "outside", "outside"])
        ft = p["ft"]
        # distances kept at least ~2 ft away from the boundary after unit conversion
        cand = []
        for unit, factor in (("feet", 1), ("metres", 3.28084), ("yards", 3)):
            for v in range(1, 40):
                d = v * factor
                if abs(d - ft) >= 2.0 and d <= 3 * ft:
                    cand.append((unit, v, d))
        f["dist"] = rng.choice(cand)
        return f

    def alts(self, p, f):
        ft = p["ft"]
        unit, n, d = f["dist"]
        factor = d / n
        near = int(ft / factor) - 1
        while near >= 1 and ft - near * factor < 2:
            near -= 1
        far = int(ft / factor) + 2
        while far * factor - ft < 2:
            far += 1
        dists = [(unit, m, m * factor) for m in (near, far) if m >= 1]
        return {"prod": ["cigarette", "vape"], "where": ["indoor", "outside"], "dist": dists}

    def verdict(self, p, f):
        if f["prod"] == "vape" and not p["ecig"]:
            return True
        if f["where"] == "indoor":
            return False
        return f["dist"][2] > p["ft"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        what = {"cigarette": ["smoked a cigarette", "had a cigarette"][sty(f, "a", 2)], "vape": ["vaped", "used an e-cigarette"][sty(f, "a", 2)]}[f["prod"]]
        if f["where"] == "indoor":
            loc = ["in the ground-floor lobby", "in the laundry room", "in the hallway outside the lifts"][sty(f, "b", 3)]
            return f"{name} {what} {loc} while waiting for a friend."
        unit, v, d = f["dist"]
        return (f"{name} {what} on the pavement {v} {unit if v != 1 else unit[:-1] if unit != 'feet' else 'foot'} from the main entrance, "
                f"{['during a break', 'before going upstairs', 'while waiting for a taxi'][sty(f, 'b', 3)]}.").replace("metre ", "metre ")

    def act(self, p, f):
        return "do that there", "doing that there"

    def edges(self, p, f):
        t = ["negation"]
        if f["where"] == "outside":
            t += ["numeric"] + (["units"] if f["dist"][0] != "feet" else [])
        if f["prod"] == "vape":
            t.append("exception" if not p["ecig"] else "implicit")
        return t


# ---------------------------------------------------------------------------------------------------------------
class ForumPromo(Schema):
    name = "forum_promo"
    FORUMS = ["the r/HomeBrewing community", "the Makers' Corner forum", "the Local Gardeners group", "the Indie Game Devs server"]
    DIS = ["Be civil; personal attacks are removed.", "Use a descriptive title for every post.", "No reposts within 30 days.",
           "Spoilers must be tagged."]

    def params(self, rng):
        return {"k": rng.choice([10, 25, 50, 100]), "phr": rng.randrange(2), "place": rng.choice(self.FORUMS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = [f"Posts that link to your own business, shop or product are not allowed, except in the weekly Self-Promo Saturday "
               f"thread. Members with fewer than {p['k']} comments in the community may not post self-promotion even there.",
               f"Self-promotion (links to your own shop, business or product) belongs only in the weekly Self-Promo Saturday thread, "
               f"and only members who have made at least {p['k']} comments here may post it."][p["phr"]]
        return f"Community rules - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["own"] = rng.random() < 0.8
        f["thread"] = rng.choice(["weekly", "weekly", "main"])
        k = p["k"]
        f["comments"] = rng.choice([k - 1, k, k + rng.randint(1, 300), max(0, k - rng.randint(2, k))])
        return f

    def alts(self, p, f):
        k = p["k"]
        return {"own": [True, False], "thread": ["weekly", "main"], "comments": [k - 1, k, k + 12]}

    def verdict(self, p, f):
        if not f["own"]:
            return True
        if f["thread"] != "weekly":
            return False
        return f["comments"] >= p["k"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        link = ["a link to " + pos + " own online shop", "a link to the Etsy store " + sub + " runs", "a link to " + pos + " own new app"][sty(f, "a", 3)] if f["own"] \
            else ["a link to a news article about the hobby", "a link to someone else's tutorial video", "a link to a free guide written by another member"][sty(f, "a", 3)]
        where = "in the weekly Self-Promo Saturday thread" if f["thread"] == "weekly" else ["as a new post on the main feed", "in a regular discussion thread"][sty(f, "b", 2)]
        return f"{name} posted {link} {where}. At that point {sub} had made {f['comments']} {plural(f['comments'], 'comment')} in the community."

    def act(self, p, f):
        return "post that link there", "posting that link there"

    def edges(self, p, f):
        t = ["exception", "numeric"]
        if f["comments"] in (p["k"], p["k"] - 1):
            t.append("quantifier")
        if f["own"] and f["thread"] == "weekly":
            t.append("multi_hop")
        return t


# ---------------------------------------------------------------------------------------------------------------
class ExamDevices(Schema):
    name = "exam_devices"
    DIS = ["Candidates must arrive 15 minutes before the start.", "Pencil cases must be transparent.",
           "Water is allowed only in a clear bottle without a label.", "Candidates may not leave in the last 15 minutes."]

    def params(self, rng):
        return {"phr": rng.randrange(2), "place": rng.choice(["Hall B", "the Sports Hall", "Room 204", "the Main Auditorium"]), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Calculators are allowed in the exam, but not calculators that can store notes or connect to the internet. "
               "Phones must be switched off (not just silenced) and kept in bags at the back of the room.",
               "Any basic or scientific calculator may be used; calculators with memory for notes, or with internet access, are "
               "banned. Phones: switched off completely and left in bags at the back; silent mode is not enough."][p["phr"]]
        return f"Exam regulations - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["calc"] = rng.choice(["scientific", "basic", "notes", "internet", "scientific"])
        f["phone"] = rng.choice(["off_bag", "off_bag", "silent_bag", "pocket_off"])
        return f

    def alts(self, p, f):
        return {"calc": ["scientific", "basic", "notes", "internet"], "phone": ["off_bag", "silent_bag", "pocket_off"]}

    def verdict(self, p, f):
        return f["calc"] in ("scientific", "basic") and f["phone"] == "off_bag"

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        calc = {"scientific": "a standard scientific calculator", "basic": "a simple four-function calculator",
                "notes": "a graphing calculator in which " + sub + " had stored formula notes", "internet": "a calculator app on a tablet connected to Wi-Fi"}[f["calc"]]
        ph = {"off_bag": ["switched off in " + pos + " bag at the back of the room", "turned off and left in " + pos + " bag at the back"][sty(f, "a", 2)],
              "silent_bag": ["on silent mode in " + pos + " bag at the back of the room", "set to silent (but still on) in " + pos + " bag at the back"][sty(f, "a", 2)],
              "pocket_off": ["switched off in " + pos + " jacket pocket at the desk", "turned off but in " + pos + " pocket during the exam"][sty(f, "a", 2)]}[f["phone"]]
        return f"In the maths exam, {name} used {calc}. {cap(pos)} phone was {ph}."

    def act(self, p, f):
        return "handle the calculator and phone that way", "handling the calculator and phone that way"

    def edges(self, p, f):
        t = ["exception", "negation", "quantifier"]
        if f["phone"] == "silent_bag" or f["calc"] == "notes":
            t.append("implicit")
        return t


# ---------------------------------------------------------------------------------------------------------------
class ShiftSwap(Schema):
    name = "shift_swap"
    ORGS = ["the Hope Street Food Bank", "the City Animal Shelter", "the Riverside Hospice", "the Northside Community Kitchen"]
    DIS = ["Volunteers must wear their badge while on shift.", "Sign in and out at the front desk.",
           "Volunteers under 16 need a signed parental consent form.", "Parking is available behind the building."]

    def params(self, rng):
        return {"h": rng.choice([12, 24, 48]), "phr": rng.randrange(2), "place": rng.choice(self.ORGS), "dseed": rng.randrange(10 ** 6), "ts": rng.randrange(3)}

    def rules(self, p):
        rel = [f"Volunteers may swap a shift with another registered volunteer, provided they tell the volunteer coordinator "
               f"at least {p['h']} hours before the shift starts. Swaps with people who are not registered volunteers are not allowed.",
               f"A shift may be swapped only with a registered volunteer, and only if the coordinator is told {p['h']} hours or "
               f"more before the shift begins."][p["phr"]]
        return f"Volunteer handbook - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["partner"] = person(rng, exclude=(f["who"][0],))
        f["reg"] = rng.random() < 0.8
        start = dt.datetime(2025, 5, 5, 9, 0) + dt.timedelta(days=rng.randrange(0, 120), hours=rng.choice([0, 4, 8]))
        h = p["h"]
        delta = rng.choice([h, h + rng.randint(1, 30), h - rng.randint(1, min(h - 1, 20)), h - 1])
        f["start"] = start
        f["told"] = start - dt.timedelta(hours=delta, minutes=rng.choice([0, 0, 0, 30]))
        return f

    def alts(self, p, f):
        h = p["h"]
        st = f["start"]
        return {"reg": [True, False], "told": [st - dt.timedelta(hours=h), st - dt.timedelta(hours=h - 1),
                                              st - dt.timedelta(hours=h + 5), st - dt.timedelta(hours=h - 1, minutes=30)]}

    def verdict(self, p, f):
        return f["reg"] and (f["start"] - f["told"]) >= dt.timedelta(hours=p["h"])

    def dtxt(self, d, f):
        ts = p_ts = sty(f, "a", 3)
        return f"{WEEKDAYS[d.weekday()]}, {MONTHS[d.month - 1]} {d.day}, at {fmt_time(d.hour, d.minute, ts)}"

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        part = f["partner"][0]
        who2 = f"{part}, another registered volunteer" if f["reg"] else f"{part}, a friend who is not a registered volunteer"
        return (f"{name} was scheduled for the shift starting {self.dtxt(f['start'], f)}. {cap(sub)} swapped it with {who2}, "
                f"and told the coordinator on {self.dtxt(f['told'], f)}.")

    def act(self, p, f):
        return "swap the shift", "swapping the shift"

    def edges(self, p, f):
        t = ["temporal", "numeric"]
        if (f["start"] - f["told"]) == dt.timedelta(hours=p["h"]):
            t.append("quantifier")
        if not f["reg"]:
            t.append("negation")
        return t


# ---------------------------------------------------------------------------------------------------------------
class BeachAlcohol(Schema):
    name = "beach_alcohol"
    BEACH = ["Seabright Beach", "Coral Cove", "North Shore Beach", "Pelican Bay"]
    DIS = ["Dogs are allowed on the beach only before 9 a.m.", "Swim only between the red and yellow flags.",
           "Umbrellas must be anchored.", "Fires are not permitted on the sand."]

    def params(self, rng):
        return {"phr": rng.randrange(2), "place": rng.choice(self.BEACH), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Alcohol is not permitted on the beach, the boardwalk or the car park, except at the licensed Beach Bar and inside its roped-off patio.",
               "No alcoholic drinks anywhere on the sand, the boardwalk or in the car park. The only exception is the licensed Beach Bar and its roped-off patio."][p["phr"]]
        return f"Beach bylaws - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["drink"] = rng.choice(["beer", "wine", "af_beer", "soda", "beer"])
        f["loc"] = rng.choice(["sand", "boardwalk", "bar", "patio", "sand", "just_outside"])
        return f

    def alts(self, p, f):
        return {"drink": ["beer", "wine", "af_beer", "soda"], "loc": ["sand", "boardwalk", "bar", "patio", "just_outside"]}

    def verdict(self, p, f):
        if f["drink"] in ("af_beer", "soda"):
            return True
        return f["loc"] in ("bar", "patio")

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        d = {"beer": "a bottle of beer", "wine": "a glass of wine", "af_beer": "an alcohol-free (0.0%) beer", "soda": "a lemonade"}[f["drink"]]
        loc = {"sand": "on a towel on the sand", "boardwalk": "on a bench on the boardwalk", "bar": "at the counter of the licensed Beach Bar",
               "patio": "at a table inside the Beach Bar's roped-off patio", "just_outside": "on the sand just outside the rope around the Beach Bar's patio"}[f["loc"]]
        return f"{name} drank {d} {loc} {['on a sunny Sunday', 'after a swim', 'while watching the sunset'][sty(f, 'a', 3)]}."

    def act(self, p, f):
        return "have that drink there", "having that drink there"

    def edges(self, p, f):
        t = ["exception", "negation"]
        if f["drink"] == "af_beer" or f["loc"] == "just_outside":
            t.append("implicit")
        return t


# ---------------------------------------------------------------------------------------------------------------
class Drones(Schema):
    name = "drones"
    can_hide = True
    PARKS = ["Linden Park", "Fairview Park", "Queen's Meadow", "Brookside Park"]
    DIS = ["Barbecues are allowed only in the picnic area.", "Cyclists must give way to pedestrians.", "Littering carries a fine.",
           "Amplified music needs an events permit."]

    def params(self, rng):
        return {"cut": rng.choice([9, 10, 11]), "phr": rng.randrange(2), "place": rng.choice(self.PARKS), "dseed": rng.randrange(10 ** 6), "ts": rng.randrange(3)}

    def rules(self, p):
        c = fmt_time(p["cut"], 0, p["ts"])
        rel = [f"Flying drones is prohibited in {p['place']}, except on the east field on weekdays (Monday to Friday) in the "
               f"morning, with the flight over by {c}, and then only with a drone permit from the parks office.",
               f"Drones may be flown only on the east field, only Monday to Friday, only with the flight finished by {c}, and "
               f"only by someone holding a parks-office drone permit. Everywhere else and at all other times, drone flying is banned."][p["phr"]]
        return f"Park regulations - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["east"] = rng.random() < 0.75
        f["date"] = dt.date(2025, 4, 7) + dt.timedelta(days=rng.randrange(0, 150))
        f["dur"] = rng.choice([10, 15, 20, 25])
        c = p["cut"] * 60
        f["t"] = rng.choice([c - f["dur"] - rng.choice([5, 40, 90]), c - f["dur"], c - f["dur"] + rng.choice([5, 10]), c, c + rng.choice([10, 60])])
        f["permit"] = rng.random() < 0.65
        f["daystyle"] = rng.random() < 0.3  # 'the day after Friday' style
        return f

    def alts(self, p, f):
        d = f["date"]
        mon = d - dt.timedelta(days=d.weekday())
        c = p["cut"] * 60
        return {"east": [True, False], "date": [mon + dt.timedelta(days=i) for i in (0, 2, 4, 5, 6)],
                "t": [c - f["dur"] - 30, c - f["dur"], c - f["dur"] + 10], "permit": [True, False]}

    def verdict(self, p, f):
        if not f["east"] or f["date"].weekday() >= 5 or f["t"] + f["dur"] > p["cut"] * 60:
            return False
        if f["permit"] == "unknown":
            return None
        return f["permit"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        d = f["date"]
        if f["daystyle"]:
            prev = d - dt.timedelta(days=1)
            day = f"on the day after {WEEKDAYS[prev.weekday()]}, {MONTHS[prev.month - 1]} {prev.day}"
        else:
            day = f"on {fmt_date(d, sty(f, 'a', 2))}"
        where = "on the east field" if f["east"] else ["on the west lawn", "by the duck pond", "on the south field"][sty(f, "b", 3)]
        ts = sty(f, "c", 3)
        e = f["t"] + f["dur"]
        s = (f"{name} flew {pos} drone {where} {day} from {fmt_time(f['t'] // 60, f['t'] % 60, ts)} to "
             f"{fmt_time(e // 60, e % 60, ts)}.")
        if f["permit"] is True:
            s += [f" {cap(sub)} holds a drone permit from the parks office.", f" {cap(sub)} had a valid parks-office drone permit with {obj}."][sty(f, "d", 2)]
        elif f["permit"] is False:
            s += [f" {cap(sub)} has never applied for a drone permit.", f" {cap(pos)} permit application was still being processed."][sty(f, "d", 2)]
        return s

    def act(self, p, f):
        return "fly the drone then and there", "flying the drone then and there"

    def hide(self, p, f, rng):
        if f["east"] and f["date"].weekday() < 5 and f["t"] + f["dur"] <= p["cut"] * 60 and f["permit"] != "unknown":
            g = copy.deepcopy(f)
            g["permit"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["permit"] = bool(want)
        return g

    def edges(self, p, f):
        t = ["exception", "temporal", "multi_hop"]
        if f["t"] + f["dur"] in (p["cut"] * 60, p["cut"] * 60 + 5, p["cut"] * 60 + 10) or f["t"] == p["cut"] * 60:
            t.append("numeric")
        if f["permit"] == "unknown":
            t.append("missing_info")
        return t


# ---------------------------------------------------------------------------------------------------------------
class Parking(Schema):
    name = "parking"
    PLACES = ["Maplewood Apartments", "Cedar Grove Townhomes", "the Bayside Condo complex", "Forest Hill Apartments"]
    DIS = ["Car washing is not allowed in the lot.", "Speed limit in the lot: 10 mph.", "Motorcycles park in the marked M bays.",
           "Report broken lights to the office."]

    def params(self, rng):
        return {"h": rng.choice([2, 3, 4]), "phr": rng.randrange(2), "place": rng.choice(self.PLACES), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = [f"Visitors may park in spaces marked V for up to {p['h']} hours. Spaces marked R are only for residents with a parking "
               f"permit; residents may not use V spaces. No vehicle may stop in the fire lane at any time, even briefly.",
               f"V spaces: visitors only, maximum {p['h']} hours. R spaces: permit-holding residents only. Fire lane: no parking or "
               f"stopping by anyone, for any length of time."][p["phr"]]
        return f"Parking rules - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["role"] = rng.choice(["visitor", "visitor", "res_permit", "res_nopermit"])
        f["space"] = rng.choice(["V", "V", "R", "fire"])
        h = p["h"] * 60
        f["mins"] = rng.choice([5, 45, h - 30, h, h + 20, h + 90])
        return f

    def alts(self, p, f):
        h = p["h"] * 60
        return {"role": ["visitor", "res_permit", "res_nopermit"], "space": ["V", "R", "fire"], "mins": [45, h, h + 20, h + 90]}

    def verdict(self, p, f):
        if f["space"] == "fire":
            return False
        if f["space"] == "V":
            return f["role"] == "visitor" and f["mins"] <= p["h"] * 60
        return f["role"] == "res_permit"

    def dur(self, m, f):
        if m < 60:
            return f"{m} minutes"
        hh, mm = divmod(m, 60)
        return (f"{hh} {plural(hh, 'hour')}" + (f" and {mm} minutes" if mm else "")) if sty(f, "a", 2) else f"{m} minutes"

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        role = {"visitor": f"{name}, who was visiting a friend,", "res_permit": f"{name}, a resident with a parking permit,",
                "res_nopermit": f"{name}, a resident who has not yet received a parking permit,"}[f["role"]]
        sp = {"V": "a space marked V", "R": "a space marked R", "fire": "the fire lane in front of the entrance"}[f["space"]]
        why = " to unload groceries" if f["space"] == "fire" and f["mins"] <= 45 else ""
        return f"{role} left {pos} car in {sp}{why} for {self.dur(f['mins'], f)}."

    def act(self, p, f):
        return "park there like that", "parking there like that"

    def edges(self, p, f):
        t = ["numeric", "quantifier"]
        if f["space"] == "fire":
            t.append("negation")
        if f["mins"] == p["h"] * 60 and f["space"] == "V":
            t.append("temporal")
        return t


# ---------------------------------------------------------------------------------------------------------------
class HouseSupplies(Schema):
    name = "house_supplies"
    DIS = ["Bins go out on Wednesday night.", "Guests staying more than two nights must be mentioned in the group chat.",
           "Dishes are washed the same day.", "The thermostat stays between 18 and 22 degrees."]

    def params(self, rng):
        return {"d": rng.choice([1, 2, 3]), "phr": rng.randrange(2), "place": rng.choice(["14 Rowan Street", "the flat on King's Road", "the Maple Avenue house share"]), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        d = p["d"]
        rel = [f"Whoever uses up the last of a shared item (milk, dish soap, toilet paper, coffee) must replace it within {num(d)} {plural(d, 'day')}.",
               f"If you finish a shared supply, you are responsible for buying a replacement no later than {num(d)} {plural(d, 'day')} after finishing it."][p["phr"]]
        return f"House agreement - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["other"] = person(rng, exclude=(f["who"][0],))
        f["last"] = rng.random() < 0.8
        f["repl"] = rng.choice([0, p["d"], p["d"] + 1, p["d"] + 3, None])
        f["now"] = rng.choice([p["d"] + 4, p["d"] - 1 if p["d"] > 1 else 0])
        return f

    def alts(self, p, f):
        d = p["d"]
        return {"last": [True, False], "repl": [0, d, d + 1, None]}


    def verdict(self, p, f):
        if not f["last"]:
            return True
        if f["repl"] is not None and f["repl"] <= f["now"]:
            return f["repl"] <= p["d"]
        # not replaced (yet) as of 'now'
        return f["now"] <= p["d"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        oth = f["other"][0]
        item = ["the milk", "the dish soap", "the toilet paper", "the coffee"][sty(f, "a", 4)]
        d0 = dt.date(2025, 2, 3) + dt.timedelta(days=sty(f, "b", 200))
        s = (f"On {fmt_date(d0)}, {name} used up the last of {item}." if f["last"] else
             f"On {fmt_date(d0)}, {oth} used up the last of {item}; {name} had some of it earlier that week.")
        if f["repl"] is not None and f["repl"] <= f["now"]:
            s += f" {name} bought a replacement on {fmt_date(d0 + dt.timedelta(days=f['repl']))}."
        else:
            s += f" As of {fmt_date(d0 + dt.timedelta(days=f['now']))}, {name} had not replaced it."
        return s

    def act(self, p, f):
        return "handle the replacement that way", "handling the replacement that way"

    def edges(self, p, f):
        t = ["temporal", "numeric"]
        if not f["last"]:
            t.append("implicit")
        if f["repl"] == p["d"]:
            t.append("quantifier")
        return t


# ---------------------------------------------------------------------------------------------------------------
class TempleDress(Schema):
    name = "temple_dress"
    SITES = ["the Golden Pavilion Temple", "St. Mark's Cathedral", "the Sri Mariamman Temple", "the Old Town Mosque"]
    DIS = ["Remove shoes before entering the prayer hall.", "Photography is not allowed during services.",
           "Please keep your voice low.", "Donations are welcome but not required."]

    def params(self, rng):
        return {"phr": rng.randrange(2), "place": rng.choice(self.SITES), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        rel = ["Inside the main building, all visitors must cover both their shoulders and their knees. Wraps are available free "
               "at the entrance. The outer courtyard has no dress code.",
               "Dress code for the interior: shoulders AND knees covered for every visitor (free wraps at the door). No dress code "
               "applies in the courtyard."][p["phr"]]
        dis = [d for d in self.DIS if not ("shoes" in d and "Mosque" in p["place"])]
        return f"Visitor etiquette - {p['place']}", [rel] + self.distract(p, dis)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["inside"] = rng.random() < 0.8
        f["shoulders"] = rng.random() < 0.6
        f["knees"] = rng.random() < 0.6
        f["wrap"] = rng.random() < 0.3
        return f


    def alts(self, p, f):
        return {"inside": [True, False], "shoulders": [True, False], "knees": [True, False],
                "wrap": [False, "shoulders", "knees", "both"]}

    def verdict(self, p, f):
        if not f["inside"]:
            return True
        sh = f["shoulders"] or f["wrap"] in ("shoulders", "both")
        kn = f["knees"] or f["wrap"] in ("knees", "both")
        return sh and kn

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        top = "a long-sleeved shirt" if f["shoulders"] else "a sleeveless top"
        bottom = ["long trousers", "an ankle-length skirt"][sty(f, "a", 2)] if f["knees"] else ["shorts", "a skirt that stopped above the knee"][sty(f, "a", 2)]
        w = {False: "", True: "", "shoulders": f" At the entrance {sub} took a free wrap and put it around {pos} shoulders.",
             "knees": f" At the entrance {sub} took a free wrap and tied it around {pos} waist so it covered {pos} legs to the ankles.",
             "both": f" At the entrance {sub} took two free wraps, one for {pos} shoulders and one tied around {pos} waist down to the ankles."}[f["wrap"]]
        where = "went inside the main building" if f["inside"] else "stayed in the outer courtyard"
        return f"{name} wore {top} and {bottom} and {where}.{w}"

    def act(self, p, f):
        return "be there dressed like that", "being there dressed like that"

    def facts_fix(self, f):
        if f["wrap"] is True:
            f["wrap"] = "shoulders"
        return f

    def edges(self, p, f):
        t = ["quantifier", "exception"]
        if f["wrap"]:
            t.append("multi_hop")
        return t


# ---------------------------------------------------------------------------------------------------------------
class GiftPolicy(Schema):
    name = "gift_policy"
    COS = ["Harlow Logistics", "Beacon Health Systems", "Northwind Foods", "Asterion Software"]
    DIS = ["Expense claims must be filed within 30 days.", "Company laptops must be locked when unattended.",
           "Remote work requires a manager's approval.", "Business-class travel needs director sign-off."]

    def params(self, rng):
        return {"v": rng.choice([25, 50, 75, 100]), "phr": rng.randrange(2), "place": rng.choice(self.COS), "dseed": rng.randrange(10 ** 6)}

    def rules(self, p):
        # reviewer fix: phrasing 0 used to attach the food exception to the reporting duty only, while the verdict exempts
        # team-shared food from BOTH duties; both phrasings now state the exemption from both parts explicitly
        rel = [f"Employees may not accept any gift from a supplier worth more than ${p['v']}, and every supplier gift, whatever its "
               f"value, must be reported to your manager. Food that is shared with the whole team is exempt from both requirements.",
               f"Gifts from suppliers: never accept one valued above ${p['v']}; report all others to your manager. Food shared with the "
               f"whole team is exempt from both parts of this rule."][p["phr"]]
        return f"Code of conduct - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["kind"] = rng.choice(["item", "item", "item", "team_food"])
        v = p["v"]
        f["val"] = rng.choice([v - rng.randint(1, v - 5), v, v + rng.choice([1, 15, 150])])
        f["reported"] = rng.random() < 0.55
        return f

    def alts(self, p, f):
        v = p["v"]
        return {"kind": ["item", "team_food"], "val": [v - 10, v, v + 1, v + 40], "reported": [True, False]}

    def verdict(self, p, f):
        if f["kind"] == "team_food":
            return True
        return f["val"] <= p["v"] and f["reported"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        sup = ["a packaging supplier", "the company's printer vendor", "a software reseller", "a catering supplier"][sty(f, "a", 4)]
        if f["kind"] == "team_food":
            g = f"a large box of pastries worth ${f['val']}"
        else:
            g = [f"a pair of concert tickets worth ${f['val']}", f"a leather notebook worth ${f['val']}", f"a gift card for ${f['val']}",
                 f"a bottle of whisky valued at ${f['val']}"][sty(f, "b", 4)]
        s = f"{name} accepted {g} from {sup}."
        if f["kind"] == "team_food":
            s += f" {cap(sub)} put the pastries in the break room for the whole team."
        s += (f" {cap(sub)} told {pos} manager about it the same day." if f["reported"] else f" {cap(sub)} did not mention it to {pos} manager.")
        return s

    def act(self, p, f):
        return "handle that gift that way", "handling that gift that way"

    def edges(self, p, f):
        t = ["numeric", "quantifier", "exception"]
        if f["val"] == p["v"]:
            t.append("negation")
        return t


# ---------------------------------------------------------------------------------------------------------------
class LibraryLoans(Schema):
    name = "library_loans"

    def params(self, rng):
        return {"k": rng.choice([3, 5, 8, 10]), "phr": rng.randrange(2), "place": rng.choice(["Westbrook Public Library", "the Lakeside Branch", "Maple Hill Library"]), "dseed": rng.randrange(10 ** 6)}

    DIS = ["DVDs may be borrowed for one week.", "Renewals can be made online.", "Lost cards cost $2 to replace.", "The book drop is open 24 hours."]

    def rules(self, p):
        rel = [f"Members may have at most {p['k']} items on loan at a time. A member who has any overdue item may not borrow anything "
               f"else until the overdue item is returned.",
               f"Loan limit: {p['k']} items at once. No new loans for members with an overdue item until it comes back."][p["phr"]]
        return f"Borrowing rules - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["cur"] = rng.randint(0, p["k"])
        f["new"] = rng.randint(1, 4)
        f["overdue"] = rng.random() < 0.25
        return f

    def alts(self, p, f):
        k = p["k"]
        return {"new": [1, 2, 3, 4, k - f["cur"], k - f["cur"] + 1], "overdue": [True, False], "cur": [0, k - 1, k]}

    def valid(self, p, f):
        return f["new"] >= 1 and 0 <= f["cur"] <= p["k"] and not (f["overdue"] and f["cur"] == 0)

    def verdict(self, p, f):
        return (not f["overdue"]) and f["cur"] + f["new"] <= p["k"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        cur, new = f["cur"], f["new"]
        if cur == 0:
            s = f"{name} had nothing on loan."
        else:
            s = f"{name} already had {num(cur, random.Random(f['sty']['a']))} {plural(cur, 'item')} on loan."
            if f["overdue"]:
                if cur == 1:
                    s += [" It was a week overdue.", " It was past its due date."][sty(f, "c", 2)]
                else:
                    s += [" One of them was a week overdue.", " One of those was past its due date."][sty(f, "c", 2)]
        s += f" {cap(sub)} then checked out {num(new, random.Random(f['sty']['b']))} more {plural(new, 'book')}."
        return s

    def act(self, p, f):
        return "borrow those books", "borrowing those books"

    def edges(self, p, f):
        t = ["numeric", "quantifier"]
        if f["overdue"]:
            t.append("negation")
        return t

    def facts_ok(self, f):
        return not (f["overdue"] and f["cur"] == 0)


# ---------------------------------------------------------------------------------------------------------------
class PetLimit(Schema):
    name = "pet_limit"

    def params(self, rng):
        return {"k": rng.choice([1, 2, 3]), "phr": rng.randrange(2), "place": rng.choice(["Oak Terrace Condominiums", "Harbourfront Towers", "Sycamore Gardens"]), "dseed": rng.randrange(10 ** 6)}

    DIS = ["Dogs must be leashed in all common areas.", "Pet waste must be bagged and binned.", "Balconies may not be enclosed.",
           "Short-term rentals are not allowed."]

    def rules(self, p):
        k = p["k"]
        rel = [f"Each unit may keep no more than {num(k)} {plural(k, 'pet')}. All the fish in one aquarium count together as a single pet. "
               f"Registered service animals do not count toward the limit.",
               f"Pet limit per unit: {k}. An aquarium counts as one pet no matter how many fish it holds; a registered service animal is not counted."][p["phr"]]
        return f"Condominium bylaws - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["dogs"] = rng.randint(0, 2)
        f["cats"] = rng.randint(0, 2)
        f["aq"] = rng.randint(0, 1)
        f["fish"] = rng.randint(3, 12)
        f["svc"] = rng.random() < 0.25
        if f["dogs"] + f["cats"] + f["aq"] + f["svc"] == 0:
            f["cats"] = 1
        return f

    def count(self, f):
        return f["dogs"] + f["cats"] + f["aq"]

    def alts(self, p, f):
        return {"dogs": [0, 1, 2, 3], "cats": [0, 1, 2, 3], "aq": [0, 1], "svc": [True, False]}

    def valid(self, p, f):
        return f["dogs"] + f["cats"] + f["aq"] + f["svc"] > 0

    def verdict(self, p, f):
        return self.count(f) <= p["k"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        parts = []
        if f["dogs"]:
            parts.append(f"{num(f['dogs'])} {plural(f['dogs'], 'dog')}")
        if f["cats"]:
            parts.append(f"{num(f['cats'])} {plural(f['cats'], 'cat')}")
        if f["aq"]:
            parts.append(f"one aquarium with {f['fish']} fish")
        if f["svc"]:
            parts.append("a registered service dog")
        lst = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
        return f"{name} lives in the building and keeps {lst} in {pos} unit."

    def act(self, p, f):
        return "keep those animals", "keeping those animals"

    def edges(self, p, f):
        t = ["quantifier", "numeric"]
        if f["aq"] or f["svc"]:
            t.append("exception")
        return t


# ---------------------------------------------------------------------------------------------------------------
class YardWork(Schema):
    name = "yard_work"
    can_hide = False

    def params(self, rng):
        return {"wd": (rng.choice([7, 8]), rng.choice([19, 20])), "we": (rng.choice([9, 10]), rng.choice([17, 18])),
                "ts": rng.randrange(3), "phr": rng.randrange(2), "place": rng.choice(["the town of Millbrook", "Cedar Falls", "the Westbury neighbourhood association"]), "dseed": rng.randrange(10 ** 6)}

    DIS = ["Grass clippings may not be blown into the street.", "Burning leaves is prohibited.", "Hedges must not block the pavement.",
           "Bins must be brought in by the evening of collection day."]

    def rules(self, p):
        a, b = p["wd"]
        c, d = p["we"]
        T = lambda h: fmt_time(h, 0, p["ts"])
        rel = [f"Lawn mowers and leaf blowers may be used only from {T(a)} to {T(b)} on weekdays, and from {T(c)} to {T(d)} "
               f"on weekends and public holidays (start no earlier than the first time and finish by the second).",
               f"Power garden tools: weekdays {T(a)}-{T(b)}; Saturdays, Sundays and public holidays {T(c)}-{T(d)}. All use must "
               f"fall inside these hours; starting earlier or running later is not permitted."][p["phr"]]
        return f"Noise bylaw - {p['place']}", [rel] + self.distract(p, self.DIS)

    HOL = {dt.date(2025, 5, 26): "Memorial Day", dt.date(2025, 7, 4): "Independence Day", dt.date(2025, 9, 1): "Labor Day",
           dt.date(2025, 5, 5): None}

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        r = rng.random()
        if r < 0.25:
            f["date"] = rng.choice([dt.date(2025, 5, 26), dt.date(2025, 7, 4), dt.date(2025, 9, 1)])
        else:
            f["date"] = dt.date(2025, 4, 14) + dt.timedelta(days=rng.randrange(0, 140))
        lo, hi = self.window(p, f)
        f["dur"] = rng.choice([20, 30, 45, 60])
        f["t"] = rng.choice([lo * 60 - rng.choice([15, 60]), lo * 60, lo * 60 + 45, hi * 60 - f["dur"],
                             hi * 60 - f["dur"] + rng.choice([10, 20]), hi * 60 + rng.choice([0, 20])])
        return f

    def holiday(self, d):
        return {dt.date(2025, 5, 26): "Memorial Day", dt.date(2025, 7, 4): "Independence Day", dt.date(2025, 9, 1): "Labor Day"}.get(d)

    def window(self, p, f):
        d = f["date"]
        if d.weekday() >= 5 or self.holiday(d):
            return p["we"]
        return p["wd"]

    def alts(self, p, f):
        lo, hi = self.window(p, f)
        return {"t": [lo * 60 - 30, lo * 60, lo * 60 + 60, hi * 60 - f["dur"], hi * 60 - f["dur"] + 15]}

    def verdict(self, p, f):
        lo, hi = self.window(p, f)
        return lo * 60 <= f["t"] and f["t"] + f["dur"] <= hi * 60

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        d = f["date"]
        hol = self.holiday(d)
        day = fmt_date(d, sty(f, "a", 2)) + (f" ({hol}, a public holiday)" if hol else "")
        tool = ["mowed the front lawn with a petrol mower", "used a leaf blower on the driveway", "ran an electric lawn mower in the back garden"][sty(f, "b", 3)]
        ts = sty(f, "c", 3)
        e = f["t"] + f["dur"]
        return (f"On {day}, {name} {tool} from {fmt_time(f['t'] // 60, f['t'] % 60, ts)} to "
                f"{fmt_time(e // 60, e % 60, ts)}.")

    def act(self, p, f):
        return "use the machine at that time", "using the machine at that time"

    def edges(self, p, f):
        t = ["temporal"]
        if self.holiday(f["date"]):
            t.append("exception")
        lo, hi = self.window(p, f)
        if f["t"] == lo * 60 or f["t"] + f["dur"] == hi * 60:
            t.append("numeric")
        return t


# ---------------------------------------------------------------------------------------------------------------
class ClubVote(Schema):
    name = "club_vote"

    def params(self, rng):
        return {"phr": rng.randrange(2), "place": rng.choice(["the Harbour Rowing Club", "the Elmwood Chess Society", "the Valley Birdwatchers' Association"]), "dseed": rng.randrange(10 ** 6)}

    DIS = ["Minutes are circulated within two weeks.", "Motions must be seconded.", "The treasurer presents accounts first.",
           "Meetings start at 7 p.m."]

    def rules(self, p):
        rel = ["Only members who have paid this year's dues may vote at the annual meeting. Honorary members may vote without paying "
               "dues. Guests may attend but may not vote.",
               "Voting at the annual meeting: members with this year's dues paid, plus honorary members (who pay no dues). Guests and "
               "members with unpaid dues may speak but not vote."][p["phr"]]
        return f"Club constitution - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        f["status"] = rng.choice(["paid", "unpaid", "lastyear", "honorary", "guest"])
        return f

    def alts(self, p, f):
        return {"status": ["paid", "unpaid", "lastyear", "honorary", "guest"]}

    def verdict(self, p, f):
        return f["status"] in ("paid", "honorary")

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        st = {"paid": f"{name}, a member who paid this year's dues in January,", "unpaid": f"{name}, a member who has not paid this year's dues,",
              "lastyear": f"{name}, a member whose dues were last paid for the previous year,", "honorary": f"{name}, an honorary member who has never paid dues,",
              "guest": f"{name}, who came as a guest of a member,"}[f["status"]]
        return f"{st} voted on the motion to buy new equipment at the annual meeting."

    def act(self, p, f):
        return "vote", "voting"

    def edges(self, p, f):
        t = ["exception"]
        if f["status"] in ("lastyear", "honorary"):
            t.append("temporal" if f["status"] == "lastyear" else "negation")
        return t


# ---------------------------------------------------------------------------------------------------------------
class TrailBikes(Schema):
    name = "trail_bikes"
    can_hide = True

    def params(self, rng):
        m1, m2 = rng.choice([(5, 10), (4, 11), (6, 9)])
        return {"m1": m1, "m2": m2, "phr": rng.randrange(2), "place": rng.choice(["the Ridge Trail", "the Blue Lake Loop", "the Canyon Rim Trail"]), "dseed": rng.randrange(10 ** 6)}

    DIS = ["Hikers have right of way.", "Horses are not allowed.", "Stay on marked paths.", "Carry out all litter."]

    def rules(self, p):
        m1, m2 = MONTHS[p["m1"] - 1], MONTHS[p["m2"] - 1]
        last = (dt.date(2025, p["m2"] % 12 + 1, 1) - dt.timedelta(days=1)).day
        rel = [f"Bicycles are allowed on {p['place']} only from {m1} 1 through {m2} {last}, and never on days when the trail is posted as closed for mud.",
               f"Cycling season on {p['place']}: {m1} 1 to {m2} {last} inclusive. Even in season, no bikes when the 'Closed - mud' sign is up."][p["phr"]]
        return f"Trail rules - {p['place']}", [rel] + self.distract(p, self.DIS)

    def facts(self, rng, p):
        f = {"who": person(rng), "sty": self.new_sty(rng)}
        y = 2025
        start = dt.date(y, p["m1"], 1)
        end = dt.date(y, p["m2"] % 12 + 1, 1) - dt.timedelta(days=1)
        f["date"] = rng.choice([start, start - dt.timedelta(days=1), end, end + dt.timedelta(days=1),
                                start + dt.timedelta(days=rng.randrange(10, 100)), dt.date(y, 2, rng.randint(1, 28))])
        f["mud"] = rng.random() < 0.3
        return f

    def alts(self, p, f):
        start = dt.date(2025, p["m1"], 1)
        end = dt.date(2025, p["m2"] % 12 + 1, 1) - dt.timedelta(days=1)
        return {"date": [start - dt.timedelta(days=1), start, end, end + dt.timedelta(days=1)], "mud": [True, False]}

    def verdict(self, p, f):
        start = dt.date(2025, p["m1"], 1)
        end = dt.date(2025, p["m2"] % 12 + 1, 1) - dt.timedelta(days=1)
        if not (start <= f["date"] <= end):
            return False
        if f["mud"] == "unknown":
            return None
        return not f["mud"]

    def story(self, p, f, rng=None):
        name, sub, obj, pos = f["who"]
        s = f"{name} rode {pos} mountain bike on {p['place']} on {fmt_date(f['date'], sty(f, 'a', 2))}, 2025."
        if f["mud"] is True:
            s += " The 'Closed - mud' sign was up at the trailhead that day."
        elif f["mud"] is False:
            s += [" The trail was dry and no closure sign was posted.", " There was no mud closure that day."][sty(f, "b", 2)]
        return s

    def act(self, p, f):
        return "ride there that day", "riding there that day"

    def hide(self, p, f, rng):
        start = dt.date(2025, p["m1"], 1)
        end = dt.date(2025, p["m2"] % 12 + 1, 1) - dt.timedelta(days=1)
        if start <= f["date"] <= end and f["mud"] in (True, False):
            g = copy.deepcopy(f)
            g["mud"] = "unknown"
            return g
        return None

    def fill(self, p, f, want):
        g = copy.deepcopy(f)
        g["mud"] = not want
        return g

    def edges(self, p, f):
        t = ["temporal", "negation"]
        start = dt.date(2025, p["m1"], 1)
        end = dt.date(2025, p["m2"] % 12 + 1, 1) - dt.timedelta(days=1)
        if f["date"] in (start, end, start - dt.timedelta(days=1), end + dt.timedelta(days=1)):
            t.append("numeric")
        if f["mud"] == "unknown":
            t.append("missing_info")
        return t


SCHEMAS = [PoolGuests(), QuietHours(), LibraryCalls(), MuseumPhoto(), GymMinors(), FridgeFood(), Campfire(), DogPark(),
           ClassPhones(), Garden(), SmokingDistance(), ForumPromo(), ExamDevices(), ShiftSwap(), BeachAlcohol(), Drones(),
           Parking(), HouseSupplies(), TempleDress(), GiftPolicy(), LibraryLoans(), PetLimit(), YardWork(), ClubVote(),
           TrailBikes()]

QUESTIONS = {
    "allowed": ["Under the rules above, was {who} allowed to {inf}?", "Did the rules above permit {who} to {inf}?"],
    "violates": ["Did {who} break the rules above by {ger}?", "Was {who} in violation of the rules above by {ger}?"],
    "est_ok": ["Do the stated facts establish that {who} was allowed to {inf}?"],
    "est_viol": ["Do the stated facts establish that {who} broke the rules above by {ger}?"],
}
DEFS = {
    "allowed": {"yes": "The rules as written permit what the person did, either directly or through an exception whose "
                       "conditions the situation shows are met; unrelated rules in the list are ignored.",
                "no": "What the person did is forbidden by a rule as written, or a required condition (time, age, count, "
                      "permission, place) was not met, and no stated exception covers it."},
    "violates": {"yes": "What the person did is forbidden by a rule as written, or a required condition (time, age, count, "
                        "permission, place) was not met, and no stated exception covers it.",
                 "no": "The rules as written permit what the person did, either directly or through an exception whose "
                       "conditions the situation shows are met; unrelated rules in the list are ignored."},
    "est_ok": {"yes": "The stated facts are enough to show that what the person did was permitted by the rules (directly or "
                      "through a stated exception).",
               "no": "Either the facts show a violation, or a fact needed to decide (such as a time, rating, permission or "
                     "booking) is not stated, so being allowed is not established."},
    "est_viol": {"yes": "The stated facts are enough to show that what the person did broke a rule and that no stated "
                        "exception covers it.",
                 "no": "Either the facts show the action was permitted, or a fact needed to decide is not stated, so a "
                       "violation is not established."},
}


def gold_for(qid, v):
    if qid == "allowed":
        return "yes" if v is True else "no"
    if qid == "violates":
        return "yes" if v is False else "no"
    if qid == "est_ok":
        return "yes" if v is True else "no"
    return "yes" if v is False else "no"


def render(s, p, f, qid, qvar):
    title, lines = s.rules(p)
    lines = random.Random(p["dseed"] + 7).sample(lines, len(lines))
    rl = "\n".join(f"{i + 1}. {ln}" for i, ln in enumerate(lines))
    state = f"{title}\n{rl}\n\nSituation: {s.story(p, f)}"
    state = re.sub(r"(a\.m\.|p\.m\.)\.", r"\1", state)
    inf, ger = s.act(p, f)
    q = QUESTIONS[qid][qvar % len(QUESTIONS[qid])].format(who=f["who"][0], inf=inf, ger=ger)
    return state, q


def main():
    rng = random.Random(SEED)
    rows = []
    seen = set()
    stats = {s.name: 0 for s in SCHEMAS}
    per_schema = N_PAIRS // len(SCHEMAS) + 1
    tries = 0
    for s in SCHEMAS:
        made = 0
        while made < per_schema and tries < 10 ** 6:
            tries += 1
            p = s.params(rng)
            f = s.facts(rng, p)
            if hasattr(s, "facts_ok") and not s.facts_ok(f):
                continue
            if isinstance(s, TempleDress):
                f = s.facts_fix(f)
            r = rng.random()
            qid = "allowed" if r < 0.35 else "violates" if r < 0.70 else ("est_ok" if r < 0.85 else "est_viol")
            base, twin = f, None
            if qid.startswith("est") and s.can_hide and rng.random() < 0.7:
                h = s.hide(p, f, rng)
                if h is None:
                    continue
                base = h
                twin = s.fill(p, h, want=(qid == "est_ok"))
            else:
                v0 = s.verdict(p, f)
                if v0 is None:
                    continue
                if qid.startswith("est") and s.can_hide and rng.random() < 0.5 and gold_for(qid, v0) == "yes":
                    twin = s.hide(p, f, rng)  # info-removal twin: yes -> no
                if twin is None:
                    twin = s.one_flip(p, f, rng)
                if twin is None:
                    continue
            diff = [k for k in set(base) | set(twin) if base.get(k) != twin.get(k)]
            assert len(diff) == 1, (s.name, diff)  # twins differ in exactly one decisive fact
            vb, vt = s.verdict(p, base), s.verdict(p, twin)
            if qid in ("allowed", "violates") and (vb is None or vt is None):
                continue
            gb, gt = gold_for(qid, vb), gold_for(qid, vt)
            if gb == gt:
                continue  # flip failed to change the answer; skip (never emit an unflipped twin)
            qvar = rng.randrange(4)
            sb, qb = render(s, p, base, qid, qvar)
            st, qt = render(s, p, twin, qid, qvar)
            if sb == st or sb in seen or st in seen:
                continue
            seen.update({sb, st})  # every state text used once
            rid = f"{KEY}-{s.name}-{made:04d}"
            orig_b = {"schema": s.name, "verdict": {True: "allowed", False: "violation", None: "undetermined"}[vb]}
            orig_t = {"schema": s.name, "verdict": {True: "allowed", False: "violation", None: "undetermined"}[vt]}
            eb = sorted(set(s.edges(p, base)))
            et = sorted(set(s.edges(p, twin)))
            from msn_common import edge_join
            rows.append(row(KEY, rid, sb, qb, gb, qid, edge_join(eb), orig_b, f"{s.name}:{qid}"))
            rows.append(row(KEY, rid + "-twin", st, qt, gt, qid, edge_join(et), orig_t, f"{s.name}:{qid}", twin_of=rid))
            made += 1
        stats[s.name] = made
    print("pairs per schema:", stats)
    pairs = [rows[i:i + 2] for i in range(0, len(rows), 2)]
    rng.shuffle(pairs)
    pairs = pairs[:N_PAIRS]
    rows = [r for pr in pairs for r in pr]
    write_gen(KEY, rows, DEFS,
              notes=("program-generated community/shared-space rules with conditions and exceptions; 25 schemas; every "
                     "item has a fact-flip (or missing-info) twin with the opposite answer (meta.twin_of); 4 question "
                     "framings incl. negated ('break the rules') and 'do the stated facts establish' (missing info -> no); "
                     "distractor rules in each rulebook; exact-duplicate states removed (twins are near-identical by design)."),
              dataset_desc="gen_msn_rules (program generator, golden_src/gen/gen_msn_rules.py)")


if __name__ == "__main__":
    main()
