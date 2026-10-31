"""VOICE solver B: closed tables, restated by solver B from VOICE/SCHEMA.md (letter names and symbol words) and from plain English
(number words, month names, fillers, negation words). Python 3 standard library only. Imports NOTHING from solver A."""

LETTER_NAME = {   # spoken name -> letter  ("double you" is two tokens: handled by the readers)
    "ay": "a", "bee": "b", "see": "c", "dee": "d", "ee": "e", "eff": "f", "gee": "g", "aitch": "h", "eye": "i", "jay": "j", "kay": "k",
    "el": "l", "em": "m", "en": "n", "oh": "o", "pee": "p", "cue": "q", "are": "r", "ess": "s", "tee": "t", "you": "u", "vee": "v",
    "ex": "x", "why": "y", "zee": "z",
}
# one-word readings of letters that are ALSO ordinary words; a hypothesis may use the plain letter instead of the name
DOUBLE_YOU = ("double", "you")

SYMBOL_PHRASE = {   # spoken words (tuple) -> character
    ("slash",): "/", ("backslash",): "\\", ("dot",): ".", ("dash",): "-", ("underscore",): "_", ("tilde",): "~", ("hash",): "#",
    ("colon",): ":", ("equals",): "=", ("star",): "*", ("at",): "@", ("plus",): "+", ("percent",): "%", ("ampersand",): "&",
    ("pipe",): "|", ("less", "than"): "<", ("greater", "than"): ">", ("dollar",): "$", ("caret",): "^", ("comma",): ",",
    ("semicolon",): ";", ("bang",): "!", ("question", "mark"): "?", ("apostrophe",): "'", ("quote",): '"', ("backtick",): "`",
    ("open", "paren"): "(", ("close", "paren"): ")", ("open", "bracket"): "[", ("close", "bracket"): "]", ("open", "brace"): "{",
    ("close", "brace"): "}",
}
SYMBOL_WORD1 = dict((k[0], v) for k, v in SYMBOL_PHRASE.items() if len(k) == 1)
SYMBOL_PAIRS = dict((k, v) for k, v in SYMBOL_PHRASE.items() if len(k) == 2)

DIGIT_WORD = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
TEENS = {"ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
         "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
SCALES = {"hundred": 100, "thousand": 1000, "million": 1000000, "billion": 1000000000}
UNITS_TO_19 = dict(DIGIT_WORD)
UNITS_TO_19.update(TEENS)

ORDINAL_WORD = {   # ordinal word -> (cardinal value)
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
    "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14, "fifteenth": 15, "sixteenth": 16, "seventeenth": 17,
    "eighteenth": 18, "nineteenth": 19, "twentieth": 20, "thirtieth": 30, "fortieth": 40, "fiftieth": 50, "sixtieth": 60,
    "seventieth": 70, "eightieth": 80, "ninetieth": 90, "hundredth": 100, "thousandth": 1000, "millionth": 1000000,
}
MONTH = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9,
         "october": 10, "november": 11, "december": 12}
MONTH_ABBR = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12}

FILLERS = frozenset(["um", "uh", "er", "erm", "hmm", "mm"])
NEGATION_WORDS = frozenset(["not", "no", "never", "none", "nothing", "nobody", "nowhere", "neither", "nor", "without"])
POLARITY_WORDS = frozenset(["only", "except", "unless", "always", "allow", "deny", "block"])      # words that flip what an instruction permits
