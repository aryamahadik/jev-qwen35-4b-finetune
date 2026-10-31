"""T60 BACKGROUND NOTES (the length mechanism, G0-lite section 5 `m.t60.length`; Opus ruling Q6). CODE ONLY.
A group reaches its planned length level with neutral notes that carry no decision-bearing content: no digit, no number word, no order word,
no step / plan / fact / keep / drop vocabulary, no second person, no instruction. Both members of a group carry the IDENTICAL notes (the notes are
never an edit-owned span), so they cannot be padding of one label; the notes are drawn from the same closed vocabulary for every head and label.
"""
import re

SUBJ = ("The project team", "The review group", "The support desk", "The planning committee", "The platform group", "The operations team",
        "The data group", "The release manager", "The editorial board", "The facilities office", "The finance group", "The training team")
VERB = ("reviewed", "discussed", "summarised", "revisited", "archived", "compared", "annotated", "circulated", "approved", "refreshed",
        "tidied", "catalogued")
OBJ = ("the quarterly overview", "the shared calendar", "the onboarding notes", "the style guide", "the meeting schedule", "the equipment list",
       "the training outline", "the travel policy", "the office layout", "the newsletter draft", "the vendor summary", "the welcome packet",
       "the safety reminders", "the reading list", "the budget summary", "the visitor guide")
WHEN = ("on Monday", "on Tuesday", "on Wednesday", "on Thursday", "on Friday", "during the morning session", "during the afternoon session",
        "at the weekly meeting", "over the long weekend", "at the start of the month", "at the end of the quarter", "during the open hour")
TAIL = ("", "", "", ", which is unrelated to the work described here", ", and nothing in it changes the work described here",
        ", and the notes were filed with the usual records", ", as part of the routine upkeep", ", in the usual way")
LABEL = "Background notes:"
SENT_PER_LINE = 3
_WORD = re.compile(r"\w+|[^\w\s]")


def n_words(text):
    return len(_WORD.findall(text))


def sentence(rng):
    return "%s %s %s %s%s." % (rng.choice(SUBJ), rng.choice(VERB), rng.choice(OBJ), rng.choice(WHEN), rng.choice(TAIL))


def note_lines(rng, n):
    """n distinct note lines (SENT_PER_LINE sentences each, no sentence repeated inside the batch)."""
    seen, out = set(), []
    while len(out) < n:
        parts = []
        while len(parts) < SENT_PER_LINE:
            s = sentence(rng)
            if s not in seen:
                seen.add(s)
                parts.append(s)
        out.append(" ".join(parts))
    return out


def tokens_of(words):
    import math
    return int(math.ceil(words * 1.3))


def choose(rng, base_words, bands, max_lines=40, tries=120):
    """-> list of note lines such that member i (base word count base_words[i]) lands in bands[i] = (lo, hi) tokens, or None when no count fits.
    k = 0 (no notes) is returned as []. A set of notes that overshoots a band is replaced by another random set (`tries` sets at most)."""
    for _ in range(tries):
        lines = note_lines(rng, max_lines)
        extra = 0
        for k in range(0, max_lines + 1):
            if k:
                extra = n_words(LABEL) + sum(n_words(x) for x in lines[:k])
            toks = [tokens_of(b + extra) for b in base_words]
            if all(lo <= t <= hi for t, (lo, hi) in zip(toks, bands)):
                return lines[:k]
            if any(t > hi for t, (lo, hi) in zip(toks, bands)):
                break
        else:
            return None
        if k == 0 and any(t > hi for t, (lo, hi) in zip(toks, bands)):
            return None                                          # no notes can shorten a row
    return None
