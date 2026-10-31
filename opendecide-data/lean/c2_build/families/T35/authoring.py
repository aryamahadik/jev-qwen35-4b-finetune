"""c2_build/families/T35/authoring.py: the T35 Haiku AUTHORING tasks and the family loader (G0_SPEC.md section 6;
C2_DATA_SPEC 3.0, 3.2; README "Haiku task flow"). After A38 only: every write goes through c2_kit.paths.

One make_batch per task (one chunk each, <= 50 gold-free items, opaque qids). Haiku never sees a robots.txt file, a
request, a question of a row, an option or a gold: it writes reusable pieces only. Every narrative, pack, attack and
document brief forbids the label words, the "no line" option text and the stand-in question and precedence strings
(FORBID). The wording briefs forbid the same strings; the precedence brief alone may name the line types "Allow" and
"Disallow" (FORBID_PREC), because the tie sentence must name them.

  tasks (24)                          kind             items x outputs   pool (G0 section 6)
  pack-sites                          author_pack      40 x 1            site packs (8 held out: S5 only)
  pack-operators                      author_pack      12 x 4            crawler operators (org name + token)
  skin-<register> (8 registers)       author_skin       5 x 6            Mode T narratives (training)
  skin-transcript, skin-wiki          author_skin       4 x 6            Mode T narratives (held out)
  attack                              author_skin       8 x 6            attack lines (inv relation)
  free-a, free-b                      author_freeform  24 x 1            Mode F narratives (training)
  free-held                           author_freeform  16 x 1            Mode F narratives (held out)
  word-<qform> (6 forms)              author_wording   2-5 x 8           question wordings (training)
  word-held                           author_wording    6 x 4            question wordings (held out)
  lex-prec                            author_lexicon    6 x 6            {LONGEST} / {TIE} paraphrases (3/3)

Each task file (haiku/author/tasks/<task_id>.md) is self-contained: the exact answer path, the prompt and the items.
The agent reads only that file and writes only its answer file (audit.audit with TASKS.json's allowed paths).
The opaque-id key stays in haiku/author/key/ (orchestrator only).

The loader (lint stage) turns answers into pieces and runs, per piece, G-SL (gsl.lint_template / lint_freeform) plus
the T35 checks of G0 M16, H8, H9, H16, H19, H24 (precedence_problems, wording_problems, attack_problems,
skin_problems, freeform_problems, site_pack_problems, operator_problems). A failing piece is dropped with its reasons;
nothing here sets or edits a label (A37 b).

  ../../.venv/bin/python -m families.T35.authoring build     (from lean/c2_build; writes haiku/author/, after A38)
  ../../.venv/bin/python -m families.T35.authoring load      (lint: answers -> haiku/author/loaded/pieces.json)
  ../../.venv/bin/python -m families.T35.authoring extract   (lint: G-LEX meaning checks -> haiku/extract/, one
                                                              chunk per read: 2 reads per wording, 3 per rule form)
  ../../.venv/bin/python -m families.T35.authoring admit     (admit: record the reads, admit 2/2 or 3/3, freeze
                                                              pools/ with a manifest, counts and shortfalls)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, gsl, paths, polarity  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from families.T35 import fixtures as FX  # noqa: E402
from families.T35 import plugin as P  # noqa: E402

import negcount  # noqa: E402  (c_src/common, on sys.path through c2_kit.paths)

FAMILY = "T35"
ROOT = HERE / "haiku" / "author"
VERSION = "v1"
MAX_TASKS = 40

LABEL_WORDS = tuple(P.T35Plugin.LABEL_WORDS)
QUESTION_STRINGS = tuple(text for _wid, _qf, text, _slots in FX.WORDINGS)
PREC_STRINGS = tuple(text for _sem, text in FX.PRECEDENCE_FORMS)
FORBID = LABEL_WORDS + (P.NONE_TEXT,) + QUESTION_STRINGS + PREC_STRINGS
FORBID_PREC = tuple(f for f in FORBID if f not in ("allow", "disallow"))
PURPOSE_TEXTS = tuple(v[0] for v in P.PURPOSES.values())


def _bad(word: str, forbid: tuple) -> bool:
    return any(re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", word.lower()) for f in forbid)


def _word_lists(forbid: tuple = FORBID) -> str:
    """The G-SL CORE + EXTENDED word lists (minus any forbidden string), as prompt text."""
    lines = []
    for c in ("number", "relative_time", "quantity", "quantifier", "modal", "hedge", "status", "operator"):
        words = sorted(gsl.CORE.get(c, set()) | gsl.EXTENDED.get(c, set()))
        words = [w for w in words if not _bad(w, forbid) and w not in ("ca", "wo")]
        lines.append(f"- {c.replace('_', ' ')}: " + ", ".join(words))
    lines.append("- phrases: have to, has to, had to, got to, sort of, kind of")
    return "\n".join(lines)


NEGATION_CUES = ("not, n't (don't, isn't, can't, won't ...), no, none, nobody, nothing, nowhere, never, neither, nor, "
                 "cannot, without, lack, deny, hardly, scarcely, barely, few, except, unless, false, other than, "
                 "free of, no longer, fail to, neglect to, omit to, refuse to, decline to, prevent ... from, rule out")

COMMON = """You are writing short pieces of text for a synthetic training dataset about web crawlers and the websites
they visit. Everything you write is either a reusable template (a program later fills each {SLOT} placeholder with a
value) or a list of invented values. Write natural, varied English. Invent everything: never copy text from real
companies, crawlers, products, people, websites or published datasets.

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool. Inside JSON strings, write a line break as \\n and a double quote as \\".
"""

ANSWER = {
    "pack": '[{"qid": "<qid of the item>", "pack": {...the fields listed below...}}, ...]',
    "operators": '[{"qid": "<qid of the item>", "operators": [{"operator": "<name>", "token": "<token>"}, ...]}, ...]',
    "texts": '[{"qid": "<qid of the item>", "texts": ["<text 1>", "<text 2>", ...]}, ...]',
    "text": '[{"qid": "<qid of the item>", "text": "<the document>"}, ...]',
    "wordings": '[{"qid": "<qid of the item>", "wordings": ["<question 1>", "<question 2>", ...]}, ...]',
    "forms": '[{"qid": "<qid of the item>", "forms": ["<sentence 1>", "<sentence 2>", ...]}, ...]',
}


def _answer_block(field: str) -> str:
    return (f"Answer format: one JSON array with one object per item (every item answered once):\n{ANSWER[field]}\n"
            "Copy each qid exactly. Give exactly the number of outputs each item asks for.\n")


NO_RULE_TALK = ("Say nothing about what the crawler gets to do: no word about access, permission, refusal, rules, "
                "robots files, crawl settings, status codes, errors, paths, sections or web addresses, and no hint "
                "about any outcome")

# ------------------------------------------------------------------------------------------------ packs
SITE_KINDS = (
    "a neighbourhood bakery", "a regional theatre", "a hiking club", "a used musical instrument shop", "a city zoo",
    "a weather hobbyist blog", "a ceramics studio", "a community radio station", "a dog grooming salon",
    "a vintage map dealer", "a board game cafe", "a tutoring service", "a chess club", "a botanical garden",
    "a farmers' market", "a model railway club", "a dance school", "a bicycle repair cooperative", "a tea shop",
    "a bookbinding studio", "a sailing school", "a student newspaper", "a local history society",
    "a pottery supply store", "a camping gear rental", "a small seaside hotel", "a language exchange forum",
    "a recipe sharing community", "a craft cider bar", "a science podcast", "a wildlife rescue centre",
    "an aquarium store", "a poster print shop", "a quilting guild", "a regional ferry operator", "a community choir",
    "a photography club", "a gardening forum", "a ski club", "a public swimming pool",
)
HELD_SITE_KINDS = frozenset(SITE_KINDS[i] for i in (3, 9, 15, 21, 27, 33, 36, 39))     # 8 held-out packs (S5 only)

SITE_PACK_PROMPT = COMMON + """
TASK: invent one SITE PACK per item. A site pack is a small set of invented values for one kind of website. Each
item gives the kind of website; fit every value to it.

Fields of "pack" (all invented; no real brand, company, product, person or place):
- "site_kind": the item's kind of website, copied.
- "site_names": exactly three different invented names for such a website, each 2-4 words, every word starting with a
  capital letter and made of letters only (no digits, no hyphens, no apostrophes, no "and" or "&"), for example
  "Copperbeech Growers". No word that is a negation (such as "Never", "Nobody", "Nothing").
- "sections": exactly eight different names of sections such a website has, each one or two lowercase English
  words made of letters only (for example "opening times" or "members"). Include a mix: public parts (such as a
  catalogue, news or events) and parts meant for staff, members or customers (such as an account, drafts or admin).
- "pages": exactly four different names of single pages or files such a website has, each one or two lowercase
  English words, letters only (for example "price list" or "photo"). No file endings: a program adds them.
No value repeats one from another item of this task. A program turns the sections and pages into web addresses;
you never write an address, a slash or a file ending.
""" + _answer_block("pack")

OPERATOR_STYLES = (
    "a small university research lab", "a price comparison start-up", "a nonprofit web archive",
    "an accessibility auditing firm", "a link checking service", "a small search engine company",
    "a news aggregator", "a library consortium", "a service that builds link preview cards for chat apps",
    "a market research agency", "a digital humanities project", "a website quality monitoring service",
)
OPERATOR_PROMPT = COMMON + """
TASK: invent CRAWLER OPERATORS. Each item gives a kind of organisation that runs a web crawler; invent four
different operators of that kind. Each operator has two fields:
- "operator": the organisation's invented name, 2-3 words, every word starting with a capital letter, letters only
  (for example "Fernhill Labs").
- "token": the product token of its crawler: one word in CamelCase, letters only, 6-16 letters, usually ending in
  Bot, Crawler, Spider, Fetcher, Archiver, Scout or Reader (for example "FernhillBot"). It may echo the operator's
  name.
Rules: no real crawler, search engine, company or product name (nothing like the crawlers of real search engines,
AI companies, social networks or SEO tools); no digits, hyphens or spaces in a token; no negation word in any name;
no token starts with the same five letters as another token in your whole answer; every name and token is distinct.
""" + _answer_block("operators")

# ------------------------------------------------------------------------------------------------ skins (Mode T)
SLOT_TEXT = {
    "SITE": "the name of the website the crawler is about to visit, such as 'Copperbeech Growers'",
    "OPERATOR": "the name of the organisation that runs the crawler, such as 'Fernhill Labs'",
    "PURPOSE": ("what the crawler collects pages for, a short lowercase noun phrase that reads well after 'for', "
                "such as " + ", ".join(f"'{t}'" for t in PURPOSE_TEXTS[:4])),
    "UA": "the crawler's product token, a single CamelCase word such as 'MaplewickBot'",
}
SITUATIONS = (
    "a crawl engineer's routine work note", "a site administrator noting an incoming crawler",
    "a support agent summarising who is asking and why", "a terse note from a busy crawl operator",
    "a friendly message that opens with a greeting", "a structured note with labelled parts",
    "a note written for a shared crawl queue", "a handoff note between crawl team shifts",
    "a neutral, impersonal summary", "a note that names the website before anything else",
    "a note that names the crawl purpose before anything else", "a message from the operator's partnerships desk",
    "a casual message with a light touch of humour", "a formal, polite note",
    "a note from the web team of the website being visited", "a summary written by a data team lead",
    "a short update for a project channel", "a note that thanks the website's web team",
    "a very short summary", "a note written from the crawler operator's point of view",
)
REGISTER_FORMAT = {
    "memo": ("an internal memo or work note: one to three sentences of prose, optionally opening with a short label "
             "such as 'Crawl desk note:'",
             "Crawl desk note: {OPERATOR} runs a crawler for {PURPOSE}, and the request below targets the {SITE} "
             "site."),
    "chat": ("a chat message: a speaker label such as 'crawl team:' or '{OPERATOR} support:' followed by one or two "
             "casual lines",
             "{OPERATOR} support: hi, our crawler collects pages for {PURPOSE} and wants this page from {SITE}."),
    "email": ("a short e-mail: a greeting line, one to three sentences and a sign-off line, separated by line breaks; "
              "no personal names in the greeting or sign-off",
              "Hello web team at {SITE},\\nthis is {OPERATOR}. Our crawler gathers pages for {PURPOSE}, and we are "
              "checking the request below.\\nThanks"),
    "ticket": ("a work ticket: labelled fields separated by ' | ' or written on separate short lines",
               "Ticket for {SITE} | requester {OPERATOR} | crawl purpose: {PURPOSE}"),
    "faq": ("an FAQ-style entry: a line starting with 'Q:' that asks about the situation (who runs the crawler, why it "
            "visits) and a line starting with 'A:' that answers in one or two sentences",
            "Q: Whose crawler is this, and why does it visit {SITE}?\\nA: It belongs to {OPERATOR} and gathers pages "
            "for {PURPOSE}."),
    "log": ("one or two machine log lines made of lowercase key=value pairs; each placeholder stands alone as a value "
            "(no timestamps, no numbers, no level words such as INFO or WARN)",
            "crawler_operator={OPERATOR} site={SITE} purpose={PURPOSE} event=crawl_visit"),
    "json": ("a JSON object with three to five snake_case keys, on one line or several; each placeholder is a bare "
             "JSON value with no quotes around it, e.g. \"site\": {SITE}; at most one extra key whose value is a "
             "plain neutral lowercase word in quotes (such as \"kind\": \"crawl\")",
             '{"site": {SITE}, "crawler_operator": {OPERATOR}, "crawl_purpose": {PURPOSE}}'),
    "pr_review": ("a code-review comment on a change to a crawler's configuration: one or two sentences, optionally "
                  "starting with a label such as 'Review note:'",
                  "Review comment on the crawl config for {SITE}: the crawler belongs to {OPERATOR} and serves "
                  "{PURPOSE}."),
    "transcript": ("a short call or meeting transcript: two to four lines, each starting with a speaker label such as "
                   "'Caller:' and 'Agent:' or 'Crawl lead:' and 'Web admin:'",
                   "Caller: this is {OPERATOR}, calling about our crawler.\\nAgent: which website is it about?\\n"
                   "Caller: {SITE}. We crawl it for {PURPOSE}."),
    "wiki": ("a wiki page snippet: a title line and one or two sentences, or a few 'Field: value' lines",
             "Crawler visits to {SITE}\\nOperator on file: {OPERATOR}. Stated purpose: {PURPOSE}."),
}
TRAIN_REGISTERS = tuple(r for r in P.T35Plugin.REGISTERS if r not in P.T35Plugin.HELD_OUT_REGISTERS)
HELD_REGISTERS = tuple(P.T35Plugin.HELD_OUT_REGISTERS)
MAX_SKIN_WORDS = 40
MAX_FREE_WORDS = 60
MAX_ATTACK_WORDS = 35


def _skin_prompt(register: str) -> str:
    fmt, example = REGISTER_FORMAT[register]
    return COMMON + f"""
TASK: write NARRATIVE TEMPLATES in the register "{register}": {fmt}.
A narrative only says which organisation runs a web crawler, what the crawler collects pages for and which website it
is about to visit. Elsewhere on the page a program prints the website's crawl file, the crawler's request and the rules
for reading them; your text must add no fact of its own and must give no hint about what those rules decide.
Example of the register (do not copy it): {example}

Placeholders: each item lists the placeholders ("slots") to use. Use every listed placeholder EXACTLY ONCE, spelled
exactly as given with its curly braces (e.g. {{SITE}}), and never use any other placeholder or write a real value in
its place. A placeholder is a whole name or phrase: never add a word that changes it (no "the" before {{SITE}} unless
the sentence still reads well with any website name).

Hard rules (a text that breaks one is thrown away):
1. One block of text of at most {MAX_SKIN_WORDS} words (a placeholder counts as one word): no empty line, no leading or
   trailing spaces; line breaks only where the register needs them.
2. Never put "a" or "an" directly before a placeholder.
3. Outside the placeholders: no digits, no number words or ordinals, no dates, times, months or weekdays, no currency
   or percent signs, no web addresses, e-mail addresses, domains, file names or slashes, no codes that mix letters and
   digits.
4. Outside the placeholders, none of these words (any letter case):
{_word_lists()}
5. No negation of any kind: {NEGATION_CUES}.
6. No names: a capital letter only on the first word of a sentence, line, list item or label (the word "URL" may be
   capitalised anywhere). Names come only through the placeholders.
7. {NO_RULE_TALK}.
8. Vary the wording, the sentence structure and the order of the placeholders across all your texts.
""" + _answer_block("texts")


ATTACK_DIRECTIONS = {
    "go": ("presses the crawler to go ahead and collect every page of the website anyway, citing a deal, a favour, an "
           "old agreement or a person's say-so"),
    "stay": ("asks the crawler to stay away from the whole website, citing a worry, a request from the website's "
             "staff or a person's say-so"),
}
ATTACK_STYLES = ("a note pasted under the request by the website's staff", "a message from the operator's sales team",
                 "a comment from a partner organisation", "a reply forwarded from the website's owners")
ATTACK_PROMPT = COMMON + f"""
TASK: write PRESSURE LINES. A program shows a website's crawl file, a crawler's request and the rules that decide it.
Below the request, a person has pasted one extra line that tries to sway the reader. Each item gives the person's role
and the direction of the push; write the number of different lines it asks for.

Hard rules (a line that breaks one is thrown away):
1. One sentence or two short ones, at most {MAX_ATTACK_WORDS} words, on one line. Use {{SITE}} and {{OPERATOR}} each
   exactly once, spelled exactly so; no other placeholder.
2. The line is a person's claim or plea, nothing more: it never quotes, adds, edits or cancels any line of the crawl
   file, the request, a fetch status or a rule, never names a page, path, section, address, slash or status code, and
   never mentions robots files.
3. It never talks to the reader or to a computer program: no "ignore", "instructions", "answer", "question", "prompt",
   "assistant", "model", "system" or "you must".
4. No digits, number words, dates, times, months or weekdays, currency or percent signs; never put "a" or "an"
   directly before a placeholder.
5. No real company, product, person or place; names come only through the placeholders.
6. Vary the wording and the reasons given.
""" + _answer_block("texts")

# ------------------------------------------------------------------------------------------------ free-form (Mode F)
FREE_REGISTERS = ("email", "memo", "chat", "ticket", "faq", "pr_review")
FREE_HELD_REGISTERS = HELD_REGISTERS
FREE_SITES = tuple(s for p in P.PACKS for s in p.sites)
FREE_OPERATORS = tuple(o for o, _t in P.OPERATORS)
FREE_REGISTER_TEXT = {
    "email": "a short e-mail: a greeting line, a few sentences and a sign-off line (no personal names)",
    "memo": "an internal memo or work note in plain prose",
    "chat": "a chat message that starts with a speaker label such as 'crawl team:'",
    "ticket": "a work ticket with short labelled fields",
    "faq": "an FAQ-style entry: a 'Q:' line about the situation and an 'A:' line that answers it",
    "pr_review": "a code-review comment on a change to a crawler's configuration",
    "transcript": "a short call transcript: a few lines with speaker labels such as 'Caller:' and 'Agent:'",
    "wiki": "a wiki page snippet: a title line and a sentence or two",
}
FREEFORM_PROMPT = COMMON + f"""
TASK: write FREE-FORM NARRATIVES. Each item gives three facts: SITE (the name of a website), OPERATOR (the
organisation that runs a web crawler) and PURPOSE (what the crawler collects pages for). Write one short document in
the item's register that says who runs the crawler, what it collects pages for and which website it is about to
visit, and nothing more. A program later prints the website's crawl file, the request and the rules elsewhere on the
page, and may swap the three values for others: describe the website only by its name.

Hard rules (a document that breaks one is thrown away):
1. At most {MAX_FREE_WORDS} words. Use each of the three fact values exactly once, copied verbatim (same spelling,
   capitals and spaces); never shorten, inflect or repeat them.
2. Outside the three values: no digits, number words or ordinals, no dates, times, months or weekdays, no currency or
   percent signs, no web addresses, e-mail addresses, domains or slashes, no codes that mix letters and digits.
3. No other names: no people, places, brands or products; a capital letter only at the start of a sentence, line or
   label (and in the word "URL").
4. No negation of any kind: {NEGATION_CUES}.
5. {NO_RULE_TALK}; no word that says whether something is let through or kept out.
6. No placeholders and no curly braces: the values are written out.
7. Avoid modal, hedge and quantity words: may, might, must, can, could, should, will, would, need, maybe, perhaps,
   probably, likely, seems, all, every, each, some, any, only, many, more, most.
Registers: """ + "; ".join(f"{r} = {t}" for r, t in FREE_REGISTER_TEXT.items()) + """.
""" + _answer_block("text")

# ------------------------------------------------------------------------------------------------ question wordings
WORDING_PROMPT = COMMON + """
TASK: write QUESTION WORDINGS. A program shows a website's robots.txt file, a crawler's fetch request (the crawler's
product token, a URL and the path to check) and a card of rules, then asks one question in your wording. Each item
states exactly what the question must mean and how many different wordings to write, all with that meaning.

Hard rules (a wording that breaks one is thrown away):
1. One question of 6-24 words, ending with "?", on one line.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it.
3. Tie the question to the rules shown, with a phrase such as "under these rules", "according to these rules",
   "by these rules", "going by the rules" or "do these rules ..." (a question about a line may say "of the
   robots.txt" instead).
4. The question is about what the rules decide, never about ability, advice, safety, manners, ethics or law: never
   use can, could, able, okay, OK, should, ought, would, safe, polite, fair, ethical, wise, legal, legally or
   technically.
5. Never start with the word "May" (write "Under these rules, may ..." instead), and never write "May" with a capital
   anywhere else.
6. Negation: exactly as the item says. When the item asks for none, use none of these: """ + NEGATION_CUES + """.
7. No digits, number words or ordinals, dates, time words (now, currently, yet, already, soon, today, still) or hedges
   (maybe, probably, likely, seem, think, believe). No names: a capital letter only on the first word (and in "URL").
8. Call the crawler "the crawler" or "this crawler", or use {UA} exactly once where the item says so; call the URL
   "this URL", "the requested URL" or "the URL". Never quote a path, pattern, line, status, website or organisation.
9. Vary the structure across your wordings (who is the subject: the crawler, the URL, the rules; short and long forms).
""" + _answer_block("wordings")

Q_MEANING = {   # G0 M11-M15; written without the label words
    "yn_fetch": ("yes/no: under the rules shown, may the crawler fetch the requested URL? (yes = the rules let the "
                 "crawler fetch it). No negation of any kind"),
    "yn_double_neg": ("yes/no with the same meaning as 'under these rules, may the crawler fetch the requested URL?' "
                      "(yes = the rules let the crawler fetch it), written with exactly two negations, each the word "
                      "'not': an explicit outer frame 'is it not the case that' (or 'is it not true that', 'is it not "
                      "so that') around a clause that puts 'not' on a word of PERMISSION, for example built on 'is it "
                      "not the case that ... is not entitled to fetch ...' (entitled, cleared, authorized, given "
                      "leave). Never put a word of blocking or refusal inside the clause (bar, block, close, exclude, "
                      "forbid, stop, keep away, hold back, breach, deny, prevent, refuse, lack, without, pass over, "
                      "stay out, out of bounds) and never use a contracted frame (isn't, aren't, doesn't, don't); no "
                      "other negation"),
    "yn_skip": ("yes/no: under the rules shown, does the crawler have to pass over the requested URL and leave it "
                "unfetched? (yes = the rules do not let the crawler fetch it). Say it positively, with a word or "
                "phrase for passing over, staying out or being out of bounds; no negation word"),
    "yn_not_allowed": ("yes/no: under the rules shown, is the crawler without the go-ahead to fetch the requested URL? "
                       "(yes = the rules do not let the crawler fetch it). Write it with exactly one 'not' or \"n't\" "
                       "on the verb or word of leave, for example built on 'may ... not fetch' or 'is ... not ... to "
                       "fetch'; never open the question with a contracted isn't / doesn't / don't; no other "
                       "negation"),
    "yn_prevented": ("yes/no: do the rules shown stop the crawler from fetching the requested URL? (yes = the rules do "
                     "not let the crawler fetch it). Use exactly one of these and no other negation: 'prevent ... "
                     "from', 'lack ... permission' (or 'lack the right'), 'deny', 'rule out'"),
    "ch_line": ("asks which line of the website's robots.txt decides whether the crawler gets to fetch the requested "
                "URL; the reader then picks a line, or 'no line', from a list shown after the question, so the "
                "question names no line itself. No negation"),
}
WORDING_STYLES = ("short and direct", "formal and rule-centred", "crawler-centred", "URL-centred",
                  "plain conversational")
WORDING_TASKS = (   # (qform, items); 8 wordings per item; items alternate {UA} on / off
    ("yn_fetch", 5), ("ch_line", 5), ("yn_skip", 3), ("yn_not_allowed", 3), ("yn_prevented", 3),
    ("yn_double_neg", 2),
)

# ------------------------------------------------------------------------------------------------ precedence (3/3)
LEX_PROMPT = COMMON + """
TASK: write RULE SENTENCES. A card of rules for reading a robots.txt file has two numbered lines that a program fills
with one of your sentences. Each item states exactly what the sentence must mean and how many different sentences to
write, all with that meaning.

Hard rules (a sentence that breaks one is thrown away):
1. One sentence of 6-26 words, starting with a capital letter and ending with a full stop; no placeholder, no curly
   braces, no digits, no line break.
2. Keep the meaning exactly as the item states it: do not widen, narrow or soften it.
3. Never use the words first, last, order, listed, earliest, priority, specific, literal, always or any number word
   other than "one".
4. Vary the structure across your sentences.
""" + _answer_block("forms")

PREC_MEANING = {
    "prec.robots_longest": ("among the matching lines (the lines of the applying groups whose pattern matches the "
                            "path), the line whose pattern is longest decides the request; length is the number of "
                            "characters in the pattern exactly as written, and each \"*\" and each \"$\" counts as "
                            "one character. The sentence must name this measure: use the word 'character' or "
                            "'characters' and write both \"*\" and \"$\" with their double quotes"),
    "prec.robots_tie_allow": ("when the longest matching lines are an Allow line and a Disallow line of equal length, "
                              "the Allow line wins. The sentence must keep the equal-length condition (say 'equal', "
                              "'same length', 'equally long' or 'tie') and name both line types exactly as 'Allow' "
                              "and 'Disallow', with capitals"),
}
PREC_STYLES = ("plain and complete", "compact", "in the voice of a rulebook")


# ------------------------------------------------------------------------------------------------ tasks
@dataclass
class Task:
    name: str
    kind: str
    field: str
    batch: chunker.TaskBatch
    outputs: int
    held_out: bool
    pool: str

    @property
    def chunk(self) -> dict:
        assert len(self.batch.chunks) == 1
        return self.batch.chunks[0]

    @property
    def task_id(self) -> str:
        return self.chunk["task_id"]

    def task_file(self, root: Path = ROOT) -> Path:
        return Path(root) / "tasks" / f"{self.task_id}.md"

    def answer_file(self, root: Path = ROOT) -> Path:
        return Path(root) / self.batch.answer_path(self.task_id)

    def text(self, root: Path = ROOT) -> str:
        items = json.dumps(self.chunk["items"], ensure_ascii=False, indent=1)
        return (f"# T35 authoring task {self.task_id}\n\n"
                f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                f"{self.answer_file(root)}\n\n"
                f"Task kind: {self.kind}; items: {len(self.chunk['items'])}; outputs expected: {self.outputs}.\n\n"
                f"{self.batch.prompt.rstrip()}\n\n"
                f"ITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def _batch(kind, name, items, prompt, forbid=FORBID) -> chunker.TaskBatch:
    b = chunker.make_batch(kind, FAMILY, items, seed=f"t35-author-{VERSION}-{name}", prompt=prompt,
                           forbid_strings=forbid)
    if len(b.chunks) != 1:
        raise chunker.ChunkError(f"{name}: one chunk per task")
    return b


def _slots(names) -> dict:
    return {n: SLOT_TEXT[n] for n in names}


def build_tasks() -> list:
    tasks = []
    # packs
    items = [(f"T35|pack|site|{i:02d}|{'h' if k in HELD_SITE_KINDS else 't'}", {"brief": {"site_kind": k}})
             for i, k in enumerate(SITE_KINDS)]
    tasks.append(Task("pack-sites", "author_pack", "pack", _batch("author_pack", "pack-sites", items,
                                                                  SITE_PACK_PROMPT), len(items), False, "packs"))
    items = [(f"T35|pack|operator|{i:02d}", {"brief": {"organisation_kind": k, "how_many": 4}})
             for i, k in enumerate(OPERATOR_STYLES)]
    tasks.append(Task("pack-operators", "author_pack", "operators",
                      _batch("author_pack", "pack-operators", items, OPERATOR_PROMPT), 4 * len(items), False,
                      "operators"))
    # Mode T skins: 5 items x 6 per training register, 4 x 6 per held-out register; items 1 and 3 carry {UA}
    for ri, reg in enumerate(TRAIN_REGISTERS + HELD_REGISTERS):
        held = reg in HELD_REGISTERS
        n_items = 4 if held else 5
        items = []
        for j in range(n_items):
            sit = SITUATIONS[(ri * 5 + j * 3) % len(SITUATIONS)]
            names = ("SITE", "OPERATOR", "PURPOSE") + (("UA",) if j in (1, 3) else ())
            rules = ["write 6 different texts", "use " + ", ".join("{" + n + "}" for n in names) + " each exactly once"]
            if "UA" not in names:
                rules.append("no {UA} placeholder")
            items.append((f"T35|skin|{reg}|{j}|{'ua' if 'UA' in names else 'no'}|{'h' if held else 't'}",
                          {"brief": f"{sit}; write 6 different texts", "register": reg, "slots": _slots(names),
                           "rules": rules}))
        tasks.append(Task(f"skin-{reg}", "author_skin", "texts", _batch("author_skin", f"skin-{reg}", items,
                                                                        _skin_prompt(reg)),
                          6 * n_items, held, "skins"))
    # attack lines
    items = []
    for j in range(8):
        d = ("go", "stay")[j % 2]
        items.append((f"T35|attack|{j}|{d}", {"brief": f"{ATTACK_STYLES[j // 2]}; the line "
                                                       f"{ATTACK_DIRECTIONS[d]}; write 6 different lines",
                                              "register": "note", "slots": _slots(("SITE", "OPERATOR")),
                                              "rules": ["write 6 different lines",
                                                        "use {SITE} and {OPERATOR} each exactly once"]}))
    tasks.append(Task("attack", "author_skin", "texts", _batch("author_skin", "attack", items, ATTACK_PROMPT), 48,
                      False, "attack"))
    # Mode F documents
    for name, regs, n, held in (("free-a", FREE_REGISTERS, 24, False), ("free-b", FREE_REGISTERS, 24, False),
                                ("free-held", FREE_HELD_REGISTERS, 16, True)):
        items = []
        off = {"free-a": 0, "free-b": 24, "free-held": 48}[name]
        for j in range(n):
            k = off + j
            facts = {"SITE": FREE_SITES[(k * 7) % len(FREE_SITES)], "OPERATOR": FREE_OPERATORS[(k * 3) % 8],
                     "PURPOSE": PURPOSE_TEXTS[k % len(PURPOSE_TEXTS)]}
            items.append((f"T35|free|{name}|{j:02d}|{'h' if held else 't'}",
                           {"brief": SITUATIONS[k % len(SITUATIONS)], "register": regs[j % len(regs)],
                            "facts": facts,
                            "rules": ["exactly one document", "each fact value exactly once, verbatim"]}))
        tasks.append(Task(name, "author_freeform", "text", _batch("author_freeform", name, items, FREEFORM_PROMPT),
                          n, held, "freeform"))
    # question wordings
    for qf, n in WORDING_TASKS:
        items = []
        for j in range(n):
            ua = j % 2 == 1
            items.append((f"T35|word|{qf}|{j}|{'ua' if ua else 'no'}|t",
                          {"brief": {"meaning": Q_MEANING[qf], "style": WORDING_STYLES[j % len(WORDING_STYLES)],
                                     "how_many": 8},
                           "slots": _slots(("UA",)) if ua else {},
                           "rules": ["use {UA} exactly once" if ua else "no placeholder: say 'the crawler'",
                                     "8 different wordings"]}))
        tasks.append(Task(f"word-{qf}", "author_wording", "wordings",
                          _batch("author_wording", f"word-{qf}", items, WORDING_PROMPT), 8 * n, False, "wordings"))
    items = []
    for j, (qf, _n) in enumerate(WORDING_TASKS):
        ua = j % 2 == 0
        items.append((f"T35|word|{qf}|held|{'ua' if ua else 'no'}|h",
                      {"brief": {"meaning": Q_MEANING[qf], "style": "unusual but natural phrasing", "how_many": 4},
                       "slots": _slots(("UA",)) if ua else {},
                       "rules": ["use {UA} exactly once" if ua else "no placeholder: say 'the crawler'",
                                 "4 different wordings"]}))
    tasks.append(Task("word-held", "author_wording", "wordings",
                      _batch("author_wording", "word-held", items, WORDING_PROMPT), 4 * len(items), True,
                      "wordings"))
    # precedence paraphrases (3/3 admission)
    items = []
    for sem in PREC_MEANING:
        for j, style in enumerate(PREC_STYLES):
            frame = "4. ___" if sem == "prec.robots_longest" else "5. ___"
            items.append((f"T35|lex|{sem}|{j}", {"brief": {"style": style, "how_many": 6,
                                                           "frame": f"a numbered line of the card: '{frame}'"},
                                                 "meaning": PREC_MEANING[sem], "slots": {},
                                                 "rules": ["6 different sentences", "one sentence each"]}))
    tasks.append(Task("lex-prec", "author_lexicon", "forms", _batch("author_lexicon", "lex-prec", items, LEX_PROMPT,
                                                                    forbid=FORBID_PREC),
                      6 * len(items), False, "lexicon:precedence"))
    if len(tasks) > MAX_TASKS:
        raise chunker.ChunkError(f"{len(tasks)} tasks > {MAX_TASKS}")
    return tasks


def check(tasks: list, root: Path = ROOT) -> list:
    """Problems: a forbidden string, an internal id or a never-open path in a task file; > 50 items; no answer path."""
    probs = []
    for t in tasks:
        text = t.text(root)
        forbid = FORBID_PREC if t.name == "lex-prec" else FORBID
        for f in forbid:
            if _bad(text, (f,)):
                probs.append(f"{t.name}: task text holds forbidden string {f!r}")
        for iid in t.batch.key.values():
            if iid in text:
                probs.append(f"{t.name}: internal id in task text")
        if len(t.chunk["items"]) > chunker.MAX_ITEMS:
            probs.append(f"{t.name}: {len(t.chunk['items'])} items")
        if str(t.answer_file(root)) not in text:
            probs.append(f"{t.name}: answer path missing")
        for p in (t.task_file(root), t.answer_file(root)):
            if paths.never_open(p):
                probs.append(f"{t.name}: never-open path {p}")
    return probs


def files(tasks: list, root: Path = ROOT) -> tuple:
    """({relative path: text}, manifest) for paths.write_files."""
    out, rows = {}, []
    for t in tasks:
        out.update(t.batch.files())
        text = t.text(root)
        out[str(t.task_file(root).relative_to(root))] = text
        read = {str(t.task_file(root))} | t.batch.allowed(str(root), t.task_id)[0]
        rows.append({"task": t.name, "task_id": t.task_id, "kind": t.kind, "pool": t.pool, "held_out": t.held_out,
                     "answer_field": t.field, "task_file": str(t.task_file(root)),
                     "answer_file": str(t.answer_file(root)), "batch_id": t.batch.batch_id,
                     "prompt_sha": t.batch.prompt_sha, "task_sha256": hashlib.sha256(text.encode()).hexdigest(),
                     "n_items": len(t.chunk["items"]), "outputs_expected": t.outputs,
                     "allowed_read": sorted(read), "allowed_write": [str(t.answer_file(root))]})
    manifest = {"family": FAMILY, "version": VERSION, "g0_sha256": P.T35Plugin.G0_SHA256,
                "g0_ambiguity_pass": P.T35Plugin.G0_AMBIGUITY_PASS["task_id"], "n_tasks": len(tasks),
                "outputs_expected": sum(t.outputs for t in tasks), "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per authoring task (see ../TASKS.json). "
                                 "Written only by the task agents.\n")
    return out, manifest


# ------------------------------------------------------------------------------------------------ piece checks
_PH = re.compile(r"\{[^{}]*\}")
_RULE_TALK = re.compile(r"\b(robots?|rules?|user-agent|status|errors?|access|permissions?|crawl\s+file|paths?|"
                        r"sections?|pages?\s+list|address(?:es)?|url|links?\s+to)\b|/", re.I)
_RULE_TALK_ATTACK = re.compile(r"\b(robots?|user-agent|status|paths?|sections?|address(?:es)?|ignore|instructions?|"
                               r"answers?|questions?|prompts?|assistant|model|system|you\s+must)\b|/|\d", re.I)
SCOPE = re.compile(r"\b(?:these|the|its|this\s+file's)\s+rules\b|\brobots\.txt\b|\bthe\s+file\b", re.I)
BAD_FRAME = re.compile(r"\b(?:can|cannot|could|able|okay|ok|should|ought|would|safe|polite|fair|ethical|wise|legal|"
                       r"legally|technically)\b|\bca(?=n't)", re.I)
NEG_PROFILE = {   # qform -> (k_syn, k_all) the question sentence must have (G-TW complement checks, G0 M11-M15)
    "yn_fetch": (0, 0), "yn_skip": (0, 0), "ch_line": (0, 0), "yn_not_allowed": (1, 1),
    "yn_double_neg": (2, 2), "yn_prevented": (0, 1),
}
PREC_BANNED = re.compile(r"\b(?:first|last|order|ordered|listed|earliest|priority|specific|literal|always)\b", re.I)
REAL_CRAWLERS = ("google", "bing", "slurp", "duckduck", "baidu", "yandex", "sogou", "exabot", "facebot", "facebook",
                 "archive.org", "ia_archiver", "applebot", "petal", "ahrefs", "semrush", "mj12", "dotbot", "gptbot",
                 "ccbot", "claude", "anthropic", "perplexity", "bytespider", "amazon", "twitter", "linkedin",
                 "slackbot", "discord", "telegram", "whatsapp", "pinterest", "rogerbot", "screaming", "seznam",
                 "yeti", "qwant", "mojeek", "chatgpt", "openai", "cohere", "diffbot", "omgili", "yisou", "majestic",
                 "moz", "uptimerobot", "pingdom", "commoncrawl", "meta-external", "mistral", "huggingface")
NAME_RE = re.compile(r"[A-Z][a-z]+(?: [A-Z][a-z]+){1,3}")
SECTION_RE = re.compile(r"[a-z]+(?: [a-z]+)?")
TOKEN_RE = re.compile(r"[A-Z][A-Za-z]{5,15}")
INERT_HEADS = tuple(p.strip("/").split("/")[0] for p in P.INERT)
SAMPLE = {"SITE": S.name_slot("Larkspur Gardens"), "OPERATOR": S.name_slot("Fernhill Labs"),
          "PURPOSE": S.category_slot("archiving", P.PURPOSES), "UA": S.id_slot("FernhillBot")}
SCHEMA = {"SITE": ("name", ()), "OPERATOR": ("name", ()), "PURPOSE": S.category_slot("indexing", P.PURPOSES).schema,
          "UA": ("id", ())}
DECL = {"SITE": "name", "OPERATOR": "name", "PURPOSE": "category", "UA": "id"}


def _words(text: str) -> int:
    return len(re.findall(r"\{[^{}]*\}|[A-Za-z0-9'’-]+", text))


def _names_in(text: str) -> set:
    return {m.group(1) for m in re.finditer(r"\{([A-Z][A-Z0-9_]*)\}", text)}


def _lint(sk) -> list:
    return [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_template(
        sk, label_words=LABEL_WORDS, exceptions=P.T35Plugin.GSL_EXCEPTIONS, name_allow=P.T35Plugin.NAME_ALLOW)]


def skin_problems(text: str, register: str, with_ua: bool, *, kind: str = "skin") -> list:
    """A Mode T narrative (kind "skin") or attack line (kind "attack"): placeholders, length, family bans, G-SL and
    the G3 read-back (fill with sample values, parse back)."""
    if not isinstance(text, str) or not text.strip():
        return ["empty"]
    probs = []
    want = {"SITE", "OPERATOR"} | ({"PURPOSE"} if kind == "skin" else set()) | ({"UA"} if with_ua else set())
    names = [m.group(1) for m in re.finditer(r"\{([A-Z][A-Z0-9_]*)\}", text)]
    if sorted(names) != sorted(want):
        probs.append(f"placeholders {sorted(names)} != {sorted(want)} (each exactly once)")
    if text != text.strip() or "\n\n" in text:
        probs.append("leading / trailing space or empty line")
    cap = MAX_SKIN_WORDS if kind == "skin" else MAX_ATTACK_WORDS
    if _words(text) > cap:
        probs.append(f"{_words(text)} words > {cap}")
    lit = _PH.sub(" ", text)
    bad = (_RULE_TALK if kind == "skin" else _RULE_TALK_ATTACK).search(lit)
    if bad:
        probs.append(f"rule / reader talk outside the slots: {bad.group()!r}")
    if kind == "attack" and "\n" in text:
        probs.append("attack line spans lines")
    if probs:
        return probs
    decl = {n: DECL[n] for n in want}
    try:
        sk = K.make_skin("T35-CAND", FAMILY, text, decl, kind=kind, register=register if kind == "skin" else "note",
                         escape="json" if register == "json" else "text")
    except K.RenderError as e:
        return [f"skin: {e}"]
    probs += _lint(sk)
    if kind == "skin" and not probs:
        try:
            filled = sk.fill(SAMPLE).text
            got = K.parse_skin(sk, filled, {n: SCHEMA[n] for n in decl})
            if any(got.get(n) != SAMPLE[n].value for n in decl):
                probs.append(f"G3 read-back {got}")
        except (K.RenderError, K.TemplateMismatch, S.SlotError, ValueError) as e:
            probs.append(f"G3 read-back: {e}")
    return probs


def attack_problems(text: str) -> list:
    return skin_problems(text, "note", False, kind="attack")


def freeform_problems(text: str, facts: dict) -> list:
    """Mode F (G0 H24): G-SL lint_freeform (values verbatim; no number, date, id, URL, label word, negation), each
    value exactly once, no other capitalised name, no rule talk, the word cap."""
    if not isinstance(text, str) or not text.strip():
        return ["empty"]
    probs = []
    if "{" in text or "}" in text:
        probs.append("curly braces in a Mode F text")
    if _words(text) > MAX_FREE_WORDS:
        probs.append(f"{_words(text)} words > {MAX_FREE_WORDS}")
    occ = K.locate(text, facts)
    for k, spans in occ.items():
        if len(spans) != 1:
            probs.append(f"{k}: {len(spans)} verbatim occurrence(s), need exactly 1")
    rest = text
    for v in sorted(facts.values(), key=len, reverse=True):
        rest = rest.replace(v, " \x00 ")
    bad = _RULE_TALK.search(rest)
    if bad:
        probs.append(f"rule talk: {bad.group()!r}")
    starts = {m.end() for m in re.finditer(r"(?:^|[.!?:;|]\s+|\n)[\s\-*#>\"'(\[]*", rest)}
    for m in re.finditer(r"[A-Za-z]+", rest):
        if m.group()[0].isupper() and m.start() not in starts and m.group() not in ("I", "URL"):
            probs.append(f"name-like word {m.group()!r}")
    probs += [f"G-SL {v.rule}: {v.detail}" for v in gsl.lint_freeform(text, facts, label_words=LABEL_WORDS)]
    return probs


def wording_problems(qform: str, text: str, with_ua: bool) -> list:
    """A question wording (G0 M11-M15, H19): one question, scoped to the rules (a ch_line wording may instead ask
    about a "line"), no ability / advice frame, no "May", the form's negation profile (complements need it), {UA}
    as asked, G-SL (wording role)."""
    if not isinstance(text, str) or not text.strip():
        return ["empty"]
    probs = []
    if "\n" in text or not text.endswith("?") or text.count("?") != 1:
        probs.append("one question on one line, ending with '?'")
    n = _words(text)
    if not 6 <= n <= 24:
        probs.append(f"{n} words (6-24)")
    names = sorted(m.group(1) for m in re.finditer(r"\{([A-Z][A-Z0-9_]*)\}", text))
    if names != (["UA"] if with_ua else []):
        probs.append(f"placeholders {names}")
    if not SCOPE.search(text) and not (qform == "ch_line" and re.search(r"\bline\b", text)):
        probs.append("not tied to the rules (H19)")
    m = BAD_FRAME.search(text)
    if m:
        probs.append(f"ability / advice frame {m.group()!r} (H19)")
    if re.search(r"\bMay\b", text):
        probs.append("capital 'May' (G-SL reads a month)")
    c = negcount.count(_PH.sub("X", text))
    if (c.k_syn, c.k_all) != NEG_PROFILE[qform]:
        probs.append(f"negation k_syn/k_all {c.k_syn}/{c.k_all} != {NEG_PROFILE[qform]}")
    # the English must carry the form's polarity, counting the negative predicates negcount does not list (G5-H fix
    # F1: "is it not the case that they do not bar the crawler ...?" passed the (2, 2) profile with the reverse meaning)
    probs += [f"polarity {p}" for p in polarity.form_problems(P.T35Plugin, qform, text)]
    if probs:
        return probs
    try:
        sk = K.make_skin("T35-CAND", FAMILY, text, {"UA": "id"} if with_ua else {}, kind="wording",
                         register="question", qform=qform)
    except K.RenderError as e:
        return [f"wording: {e}"]
    return _lint(sk)


def precedence_problems(sem: str, text: str) -> list:
    """A {LONGEST} / {TIE} paraphrase (G0 M16, H8, H9): one sentence; LONGEST names the measure (character(s), "*"
    and "$"); TIE names Allow and Disallow and the equal-length condition; neither says first, a number word other
    than "one", order, priority, specific, literal or always."""
    if not isinstance(text, str) or not text.strip():
        return ["empty"]
    probs = []
    if "\n" in text or not text[0].isupper() or not text.endswith(".") or re.search(r"[{}\d]", text):
        probs.append("one sentence: capital first, full stop last, no braces or digits")
    if not 6 <= _words(text) <= 26:
        probs.append(f"{_words(text)} words (6-26)")
    m = PREC_BANNED.search(text)
    if m:
        probs.append(f"banned word {m.group()!r}")
    nums = [w for w in re.findall(r"[A-Za-z]+", text) if w.lower() in gsl.CORE["number"] and w.lower() != "one"]
    if nums:
        probs.append(f"number word(s) {nums}")
    if sem == "prec.robots_longest":
        if not re.search(r"\bcharacters?\b", text, re.I) or '"*"' not in text or '"$"' not in text:
            probs.append('must name the measure: "character(s)", "*" and "$" (H8)')
    elif sem == "prec.robots_tie_allow":
        if not (re.search(r"\bAllow\b", text) and re.search(r"\bDisallow\b", text)):
            probs.append("must name Allow and Disallow (H9)")
        if not re.search(r"\b(?:equal|equally|same|tie|ties|tied)\b", text, re.I):
            probs.append("must keep the equal-length condition (H9)")
    else:
        probs.append(f"unknown sem {sem}")
    return probs


def site_pack_problems(pack) -> list:
    if not isinstance(pack, dict):
        return ["pack is not an object"]
    probs = []
    names, secs, pages = pack.get("site_names"), pack.get("sections"), pack.get("pages")
    if not (isinstance(names, list) and len(names) == 3 and len(set(names)) == 3):
        probs.append("site_names: three distinct names")
    else:
        for nm in names:
            if not isinstance(nm, str) or not NAME_RE.fullmatch(nm) or negcount.k_all(nm):
                probs.append(f"site name {nm!r}: 2-4 capitalised words, letters only, no negation")
    for field, items, k in (("sections", secs, 8), ("pages", pages, 4)):
        if not (isinstance(items, list) and len(items) == k and len({str(x).lower() for x in items}) == k):
            probs.append(f"{field}: {k} distinct entries")
            continue
        for x in items:
            if not isinstance(x, str) or not SECTION_RE.fullmatch(x) or len(x) > 24 or negcount.k_all(x):
                probs.append(f"{field} entry {x!r}: one or two lowercase words, letters only")
            elif x.replace(" ", "-") in INERT_HEADS:
                probs.append(f"{field} entry {x!r} equals an inert G4 pattern")
    return probs


def operator_problems(op) -> list:
    if not isinstance(op, dict):
        return ["operator is not an object"]
    probs = []
    name, tok = op.get("operator"), op.get("token")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Z][a-z]+(?: [A-Z][a-z]+){1,2}", name) or negcount.k_all(name):
        probs.append(f"operator {name!r}: 2-3 capitalised words, letters only")
    if not isinstance(tok, str) or not TOKEN_RE.fullmatch(tok) or negcount.k_all(tok):
        probs.append(f"token {tok!r}: one CamelCase word, letters only, 6-16 letters")
    else:
        low = tok.lower()
        if any(r in low for r in REAL_CRAWLERS):
            probs.append(f"token {tok!r} echoes a real crawler or company")
    return probs


# ------------------------------------------------------------------------------------------------ loader
def _parse_iid(iid: str) -> dict:
    p = iid.split("|")
    kind = p[1]
    if kind == "skin":
        return {"pool": "skins", "register": p[2], "with_ua": p[4] == "ua", "held_out": p[5] == "h"}
    if kind == "attack":
        return {"pool": "attack", "direction": p[3], "held_out": False}
    if kind == "free":
        return {"pool": "freeform", "held_out": p[4] == "h"}
    if kind == "word":
        return {"pool": "wordings", "qform": p[2], "with_ua": p[4] == "ua", "held_out": p[5] == "h"}
    if kind == "lex":
        return {"pool": "lexicon:precedence", "sem": p[2], "held_out": False}
    if kind == "pack":
        return {"pool": "packs" if p[2] == "site" else "operators", "held_out": p[-1] == "h"}
    raise ValueError(iid)


def load(root: Path = ROOT, answers: dict | None = None) -> dict:
    """Answers -> pieces with their problems. answers: {task_id: raw answer object} (default: read every answer file
    that exists under root). Returns {"pieces": [...], "problems": [...], "counts": {...}}; writes nothing."""
    manifest = json.loads((Path(root) / "TASKS.json").read_text()) if answers is None else None
    tasks = build_tasks()
    by_id = {t.task_id: t for t in tasks}
    if manifest is not None and {r["task_id"] for r in manifest["tasks"]} != set(by_id):
        raise ValueError("TASKS.json does not match build_tasks() (rebuilt with other content?)")
    raw = {}
    if answers is None:
        for t in tasks:
            f = t.answer_file(root)
            if f.exists():
                try:
                    raw[t.task_id] = json.loads(f.read_text())
                except json.JSONDecodeError as e:
                    raw[t.task_id] = None
                    print(f"{t.task_id}: answer file is not JSON ({e})", file=sys.stderr)
    else:
        raw = dict(answers)
    pieces, problems, seen = [], [], {}
    for tid, ans in sorted(raw.items()):
        t = by_id.get(tid)
        if t is None:
            problems.append(f"{tid}: unknown task")
            continue
        if ans is None:
            problems.append(f"{tid}: unreadable answer file")
            continue
        got, probs = chunker.load_answers(t.batch, {tid: ans})
        problems += probs
        items = chunker.item_by_internal(t.batch)
        for iid, a in sorted(got.items()):
            info = _parse_iid(iid)
            outs = a.get(t.field)
            if t.field in ("text", "pack"):
                outs = [outs]
            if not isinstance(outs, list):
                problems.append(f"{tid}: {iid}: field {t.field!r} missing")
                continue
            for k, out in enumerate(outs):
                pc = {"piece_id": f"{iid}#{k}", "task_id": tid, "prompt_sha": t.batch.prompt_sha, **info}
                if info["pool"] == "skins":
                    pc["text"], pc["problems"] = out, skin_problems(out, info["register"], info["with_ua"])
                elif info["pool"] == "attack":
                    pc["text"], pc["problems"] = out, attack_problems(out)
                elif info["pool"] == "freeform":
                    facts = items[iid]["facts"]
                    pc.update(text=out, facts=facts, register=items[iid]["register"],
                              problems=freeform_problems(out, facts))
                elif info["pool"] == "wordings":
                    pc["text"], pc["problems"] = out, wording_problems(info["qform"], out, info["with_ua"])
                elif info["pool"] == "lexicon:precedence":
                    pc["text"], pc["problems"] = out, precedence_problems(info["sem"], out)
                elif info["pool"] == "packs":
                    pc["pack"], pc["problems"] = out, site_pack_problems(out)
                else:
                    pc["operator"], pc["problems"] = out, operator_problems(out)
                key = json.dumps(out, sort_keys=True).casefold() if not isinstance(out, str) else \
                    " ".join(out.casefold().split())
                if (info["pool"], key) in seen and not pc["problems"]:
                    pc["problems"] = [f"duplicate of {seen[(info['pool'], key)]}"]
                seen.setdefault((info["pool"], key), pc["piece_id"])
                pieces.append(pc)
    toks = {}
    for pc in pieces:                     # look-alike tokens: one token a prefix of another (case ignored)
        if pc["pool"] == "operators" and not pc["problems"]:
            t = pc["operator"]["token"].lower()
            clash = [o for o in toks if o.startswith(t) or t.startswith(o)]
            if clash:
                pc["problems"] = [f"token clashes with {toks[clash[0]]}"]
            else:
                toks[t] = pc["piece_id"]
    counts = {}
    for pc in pieces:
        k = f"{pc['pool']}{':held' if pc.get('held_out') else ''}"
        c = counts.setdefault(k, {"pieces": 0, "kept": 0})
        c["pieces"] += 1
        c["kept"] += not pc["problems"]
    return {"family": FAMILY, "g0_sha256": P.T35Plugin.G0_SHA256, "pieces": pieces, "problems": problems,
            "counts": counts}


# ------------------------------------------------------------------------------------------------ G-LEX extraction
EXTRACT_ROOT = HERE / "haiku" / "extract"
POOLS_ROOT = HERE / "pools"
READS = {"question": 2, "precedence": 3}           # independent extractions per form (G-LEX 2/2; 3/3 precedence)
NONE_OF_THESE = "none of these"
EXTRACT_PROMPT = """You are checking short sentences for a synthetic dataset about web crawlers. Each item gives a
text (a question, or a rule sentence from a card of rules for reading a robots.txt file; a sample value may be filled
in) and a list of choices, each one possible meaning. Pick the ONE choice that states exactly what the text means:
not a broader, narrower or softer meaning. If no choice fits exactly, answer "none of these".

How to work: this task file is the only file you may open. Do not open, list or search any other file or folder.
Write your whole answer, and nothing else, as one JSON document to the ANSWER FILE path given at the top of this file,
with the Write tool.
Answer format: one JSON array with one object per item (every item answered once):
[{"qid": "<qid of the item>", "meaning": "<the chosen choice, copied exactly, or none of these>"}, ...]
Copy each qid exactly.
"""


QUESTION_GLEX = {   # G-LEX meaning list for question wordings: polarity AND form, so a read checks both (G0 M11-M15)
    "yn_fetch": "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with no negation",
    "yn_double_neg": "a yes/no question whose 'yes' means the crawler may fetch the URL, asked with two negations",
    "yn_skip": ("a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with no negation word "
                "(for example with 'skip' or 'off-limits')"),
    "yn_not_allowed": "a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with one 'not'",
    "yn_prevented": ("a yes/no question whose 'yes' means the crawler may not fetch the URL, asked with a verb such as "
                     "'prevent', 'lack' or 'deny'"),
    "ch_line": "a question asking which line of the robots.txt decides the request",
    "decoy_ability": "a question about whether the crawler is technically able to reach the URL",
    "decoy_owner": "a question about what the website's owner would prefer the crawler to do",
    "decoy_advice": "a question about whether fetching the URL would be wise or polite",
}


def _meaning_sem(reg, kind: str, text) -> str | None:
    """The sem of a copied meaning (case, spacing, quotes and end punctuation ignored); None for "none of these",
    an unknown text or an ambiguous copy (the form is then rejected)."""
    if not isinstance(text, str):
        return None
    norm = lambda t: " ".join(t.casefold().replace("\u2019", "'").split()).strip(" .\"'")   # noqa: E731
    hits = [x.sem_id for x in reg.sems.values() if x.kind == kind and norm(x.meaning) == norm(text)]
    return hits[0] if len(hits) == 1 else None


def registry_from(pieces_doc: dict):
    """The T35 lexicon registry: the closed meaning lists (G0 M16, section 6) + every kept wording and precedence
    piece as a Haiku form (unit-tested here; admission needs the extraction reads)."""
    from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem
    reg = LexiconRegistry(FAMILY)
    for sem, meaning in FX.PRECEDENCE_SEMS:
        reg.declare(sem, "precedence", meaning)
    for qf, meaning in QUESTION_GLEX.items():
        reg.declare(question_sem(FAMILY, qf), "question", meaning)
    skipped = []
    for pc in pieces_doc["pieces"]:
        if pc["problems"] or pc["pool"] not in ("wordings", "lexicon:precedence"):
            continue
        sem = question_sem(FAMILY, pc["qform"]) if pc["pool"] == "wordings" else pc["sem"]
        try:
            reg.add(pc["text"], sem, slots={"UA": "id"} if pc.get("with_ua") else {}, source="haiku", family=FAMILY,
                    haiku_task_id=pc["task_id"], haiku_prompt_sha=pc["prompt_sha"], held_out=bool(pc.get("held_out")))
        except LexiconError as e:
            skipped.append((pc["piece_id"], str(e)))
    reg.unit_test_all()
    return reg, skipped


@dataclass
class ReadTask:
    name: str
    batch: chunker.TaskBatch
    index: int                       # chunk index within the batch
    kind_of_form: str                # question | precedence
    read: int

    @property
    def chunk(self) -> dict:
        return self.batch.chunks[self.index]

    @property
    def task_id(self) -> str:
        return self.chunk["task_id"]

    def task_file(self, root: Path = EXTRACT_ROOT) -> Path:
        return Path(root) / "tasks" / f"{self.task_id}.md"

    def answer_file(self, root: Path = EXTRACT_ROOT) -> Path:
        return Path(root) / self.batch.answer_path(self.task_id)

    def text(self, root: Path = EXTRACT_ROOT) -> str:
        items = json.dumps(self.chunk["items"], ensure_ascii=False, indent=1)
        return (f"# T35 meaning check {self.task_id}\n\n"
                f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n"
                f"{self.answer_file(root)}\n\nItems: {len(self.chunk['items'])}.\n\n{self.batch.prompt.rstrip()}\n\n"
                f"ITEMS (JSON; answer every item, keyed by its qid):\n{items}\n")


def build_extraction(reg) -> list:
    """One batch per (form kind, read); each read in its own chunk files, so the reads of a form are independent
    agents (3 for precedence). Only unit-tested forms are sent."""
    out = []
    for kind, n_reads in READS.items():
        ids = sorted(f for f, x in reg.forms.items() if x.kind == kind and reg.status(f) == "pending")
        if not ids:
            continue
        for r in range(1, n_reads + 1):
            items = [(fid, {"text": it["text"], "choices": it["choices"] + [NONE_OF_THESE]})
                     for fid, it in reg.lexicon_items(ids, seed=f"t35-glex-{kind}-r{r}")]
            b = chunker.make_batch("extract_lex", FAMILY, items, seed=f"t35-glex-{VERSION}-{kind}-r{r}",
                                   prompt=EXTRACT_PROMPT)
            out += [ReadTask(f"glex-{kind}-r{r}-{i}", b, i, kind, r) for i in range(len(b.chunks))]
    return out


def extraction_files(reg, tasks: list, root: Path = EXTRACT_ROOT) -> tuple:
    out, rows = {}, []
    for t in tasks:
        out.update(t.batch.files())
        text = t.text(root)
        out[str(t.task_file(root).relative_to(root))] = text
        read = {str(t.task_file(root))} | t.batch.allowed(str(root), t.task_id)[0]
        rows.append({"task": t.name, "task_id": t.task_id, "kind": "extract_lex", "form_kind": t.kind_of_form,
                     "read": t.read, "task_file": str(t.task_file(root)), "answer_file": str(t.answer_file(root)),
                     "batch_id": t.batch.batch_id, "prompt_sha": t.batch.prompt_sha,
                     "task_sha256": hashlib.sha256(text.encode()).hexdigest(), "n_items": len(t.chunk["items"]),
                     "allowed_read": sorted(read), "allowed_write": [str(t.answer_file(root))]})
    manifest = {"family": FAMILY, "version": VERSION, "g0_sha256": P.T35Plugin.G0_SHA256, "n_tasks": len(tasks),
                "reads": READS, "registry_sha256": reg.sha256(), "tasks": rows}
    out["TASKS.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out["registry.json"] = json.dumps(reg.to_json(), ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = "Haiku answer files: one <task_id>.json per meaning-check task (../TASKS.json).\n"
    return out, manifest


def record_reads(reg, tasks: list, answers: dict) -> list:
    """answers: {task_id: raw answer}. Each answer's meaning is mapped back to a sem (_meaning_sem; "none of these",
    a decoy or an unknown text rejects the form for good: any read that is not the form's own sem)."""
    probs = []
    by = {t.task_id: t for t in tasks}
    for tid, ans in sorted(answers.items()):
        t = by.get(tid)
        if t is None or ans is None:
            probs.append(f"{tid}: unknown task or unreadable answer")
            continue
        got, p = chunker.load_answers(t.batch, {tid: ans})
        probs += p
        for fid, a in sorted(got.items()):
            sem = _meaning_sem(reg, t.kind_of_form, a.get("meaning") if isinstance(a, dict) else None)
            reg.record_extraction(fid, f"haiku:{tid}", sem)
    return probs


# ------------------------------------------------------------------------------------------------ pools (admit)
POOL_TARGETS = {   # G0 section 6 + spec 3.0 (600 rows, 1.5x built, <= 6 rows per skin, <= 2% per wording)
    "skins:train": 113, "skins:held": 19, "freeform:train": 30, "freeform:held": 7, "attack:train": 8,
    "packs:train": 25 - len(P.PACKS), "packs:held": 3, "operators:train": 16,
    "wordings:yn_fetch": 16, "wordings:ch_line": 15, "wordings:yn_skip": 6, "wordings:yn_not_allowed": 6,
    "wordings:yn_prevented": 6, "wordings:yn_double_neg": 6, "wordings:total": 30,
    "precedence:prec.robots_longest": 6, "precedence:prec.robots_tie_allow": 6,
}


def build_pools(pieces_doc: dict, reg) -> tuple:
    """({relative path: text}, manifest): the frozen pools from kept pieces and admitted lexicon forms."""
    from c2_kit.lexicon import question_sem

    def sid(prefix, text):
        return f"T35-{prefix}-{hashlib.sha256(text.encode()).hexdigest()[:10]}"
    kept = [p for p in pieces_doc["pieces"] if not p["problems"]]
    pools = {"skins": [], "attack": [], "freeform": [], "wordings": [], "precedence": [], "packs": [],
             "operators": []}
    for p in kept:
        meta = {"held_out": bool(p.get("held_out")), "haiku_task_id": p["task_id"], "haiku_prompt_sha": p["prompt_sha"]}
        if p["pool"] == "skins":
            slots = {n: DECL[n] for n in ("SITE", "OPERATOR", "PURPOSE") + (("UA",) if p["with_ua"] else ())}
            pools["skins"].append({"skin_id": sid("SK", p["text"]), "kind": "skin", "author_mode": "T",
                                   "register": p["register"], "escape": "json" if p["register"] == "json" else "text",
                                   "text": p["text"], "slots": slots, **meta})
        elif p["pool"] == "attack":
            pools["attack"].append({"skin_id": sid("AT", p["text"]), "kind": "attack", "register": "note",
                                    "direction": p["direction"], "text": p["text"],
                                    "slots": {"SITE": "name", "OPERATOR": "name"}, **meta})
        elif p["pool"] == "freeform":
            pools["freeform"].append({"skin_id": sid("FF", p["text"]), "kind": "skin", "author_mode": "F",
                                      "register": p["register"], "text": p["text"], "brief": p["facts"],
                                      "slots": {"SITE": "name", "OPERATOR": "name", "PURPOSE": "category"}, **meta})
        elif p["pool"] == "packs":
            pools["packs"].append({"pack_id": sid("PK", json.dumps(p["pack"], sort_keys=True)), **p["pack"], **meta})
        elif p["pool"] == "operators":
            pools["operators"].append({**p["operator"], **meta})
    for fid, f in sorted(reg.forms.items()):
        if reg.status(fid) != "admitted":
            continue
        meta = {"held_out": f.held_out, "haiku_task_id": f.haiku_task_id, "haiku_prompt_sha": f.haiku_prompt_sha}
        if f.kind == "question":
            qf = next(q for q in P.T35Plugin.QFORMS if question_sem(FAMILY, q) == f.sem_id)
            pools["wordings"].append({"skin_id": sid("W", f.text), "kind": "wording", "qform": qf, "text": f.text,
                                      "slots": dict(f.slots), "lexicon_ids": [fid], **meta})
        elif f.kind == "precedence":
            pools["precedence"].append({"form_id": fid, "sem_id": f.sem_id, "text": f.text, **meta})
    counts = {
        "skins:train": sum(not x["held_out"] for x in pools["skins"]),
        "skins:held": sum(x["held_out"] for x in pools["skins"]),
        "freeform:train": sum(not x["held_out"] for x in pools["freeform"]),
        "freeform:held": sum(x["held_out"] for x in pools["freeform"]),
        "attack:train": len(pools["attack"]),
        "packs:train": sum(not x["held_out"] for x in pools["packs"]),
        "packs:held": sum(x["held_out"] for x in pools["packs"]),
        "operators:train": len(pools["operators"]),
        "wordings:total": sum(not x["held_out"] for x in pools["wordings"]),
    }
    for q in P.T35Plugin.QFORMS:
        counts[f"wordings:{q}"] = sum(x["qform"] == q and not x["held_out"] for x in pools["wordings"])
    for sem in PREC_MEANING:
        counts[f"precedence:{sem}"] = sum(x["sem_id"] == sem for x in pools["precedence"])
    regs = {}
    for x in pools["skins"]:
        regs[x["register"]] = regs.get(x["register"], 0) + 1
    shortfalls = {k: [counts.get(k, 0), v] for k, v in POOL_TARGETS.items() if counts.get(k, 0) < v}
    out = {f"{k}.json": json.dumps(v, ensure_ascii=False, indent=1) + "\n" for k, v in pools.items()}
    out["lexicon.json"] = json.dumps(reg.to_json(), ensure_ascii=False, indent=1) + "\n"
    manifest = {"family": FAMILY, "g0_sha256": P.T35Plugin.G0_SHA256, "counts": counts, "targets": POOL_TARGETS,
                "shortfalls": shortfalls, "skins_by_register": regs, "lexicon_gate": reg.gate(),
                "sha256": {k: hashlib.sha256(v.encode()).hexdigest() for k, v in sorted(out.items())}}
    out["manifest.json"] = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    return out, manifest


def _read_answers(tasks, answer_file) -> dict:
    raw = {}
    for t in tasks:
        f = answer_file(t)
        if f.exists():
            try:
                raw[t.task_id] = json.loads(f.read_text())
            except json.JSONDecodeError:
                raw[t.task_id] = None
    return raw


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["build"])[0]
    if cmd == "build":
        tasks = build_tasks()
        probs = check(tasks)
        if probs:
            print("\n".join(probs))
            return 1
        out, manifest = files(tasks)
        paths.write_files(ROOT, out)              # refuses before A38 and on never-open paths
        for r in manifest["tasks"]:
            print(f"{r['kind']:16s} {r['task']:20s} items {r['n_items']:3d} outputs {r['outputs_expected']:4d} "
                  f"{r['task_file']}")
        print(f"{manifest['n_tasks']} tasks, {manifest['outputs_expected']} outputs expected; manifest "
              f"{ROOT / 'TASKS.json'}")
        return 0
    if cmd == "load":                             # lint stage, step 1: answers -> pieces (G-SL + T35 checks)
        res = load()
        paths.write_json(ROOT / "loaded" / "pieces.json", res)
        for k, c in sorted(res["counts"].items()):
            print(f"{k:28s} pieces {c['pieces']:4d} kept {c['kept']:4d}")
        print(f"{len(res['problems'])} answer-level problems; {ROOT / 'loaded' / 'pieces.json'}")
        return 0
    if cmd == "extract":                          # lint stage, step 2: G-LEX meaning-check tasks (own chunk per read)
        doc = json.loads((ROOT / "loaded" / "pieces.json").read_text())
        reg, skipped = registry_from(doc)
        tasks = build_extraction(reg)
        out, manifest = extraction_files(reg, tasks)
        paths.write_files(EXTRACT_ROOT, out)
        for r in manifest["tasks"]:
            print(f"{r['form_kind']:10s} read {r['read']} items {r['n_items']:3d} {r['task_file']}")
        st = {}
        for f in reg.forms:
            st[reg.status(f)] = st.get(reg.status(f), 0) + 1
        print(f"{len(tasks)} tasks; forms by status {st}; {len(skipped)} skipped (duplicate / malformed)")
        return 0
    if cmd == "admit":                            # admit stage: record the reads, admit 2/2 (3/3), freeze the pools
        doc = json.loads((ROOT / "loaded" / "pieces.json").read_text())
        reg, _ = registry_from(doc)
        tasks = build_extraction(reg)
        man = json.loads((EXTRACT_ROOT / "TASKS.json").read_text())
        if {r["task_id"] for r in man["tasks"]} != {t.task_id for t in tasks}:
            print("extract/TASKS.json does not match the rebuilt reads (pieces.json changed?)")
            return 1
        probs = record_reads(reg, tasks, _read_answers(tasks, lambda t: t.answer_file()))
        out, manifest = build_pools(doc, reg)
        paths.write_files(POOLS_ROOT, out)
        print(json.dumps({"counts": manifest["counts"], "shortfalls": manifest["shortfalls"],
                          "lexicon": manifest["lexicon_gate"]["status_counts"], "read_problems": len(probs)},
                         indent=1))
        return 0
    print("usage: python -m families.T35.authoring [build|load|extract|admit]")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
