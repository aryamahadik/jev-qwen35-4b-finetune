# VOICE interfaces for solver B and for the L-0 / od-l4b job runners. Written by the solver-A builder, 18 Oct 2026.

Solver B (a separate Sonnet session) receives the VOICE G0-lite, the Opus rulings addendum and THIS file only. It writes CODE for
(1) the DENORMALISER, (2) the independent SPAN-SURVIVAL CHECKER, (3) an independent WER measurement. It never sees solver A's code,
tables, or planted suite sources. Everything below is an interface, not an implementation.

## 1. SpokenDoc (what the verbalizer produces; plain JSON)
| field | meaning |
|---|---|
| stratum | V-NL, V-DICT-LIT, V-DICT-NAT or V-NUM |
| source_text, source_tokens | the written utterance and its tokens (sentence punctuation split off the ends; punctuation inside a token stays) |
| tokens | the SPOKEN word tokens, lower case (what the TTS reads and the reference of the checker) |
| segments | `[{kind, tok:[a,b), src, style}]` covering every spoken token. kind: word, spelled, digits, sym, number, disfl. `src` = index into source_tokens (null for disfluency words). `style` for numbers: cardinal, digits, year, decimal, cardinal_frac, version, ordinal, date, and the prefixed forms comma_*, pct_*, neg_* |
| spans | decision-bearing spans: `{id, role, kind, canonical, src_text, tok:[lo,hi), src, partial, fallback}`; role in negation, number, entity, authority; kind e.g. negation, polarity, number, quantity, unit, date, name, path, flag, rule, statement |
| tts_text | spoken tokens joined, with the comma and full stop marks of the source |
| disfluency | list of applied disfluency operations |
Hidden from B: `source_text`, `source_tokens`, `spans`, and the segment field `char`. B's denormaliser gets `verbalizer.public_view(doc)` =
`{tokens, segments(kind, tok, src, style), stratum}`.

## 2. Denormaliser contract (gate V-C1)
`denormalise(view) -> list[str]`: the written source tokens, in order, recovered from the spoken tokens and the segment map only.
Compared with `source_tokens` lower-cased, TOKEN FOR TOKEN, on 100 percent of tokens over at least 5,000 program-built strings.
Inversion rules B must implement itself:
- word / word_hyphen: the word (hyphen style joins the parts with a hyphen).
- spelled: letter names back to letters (table below); `capital` before a letter marks an uppercase letter (compare lower case).
- digits (inside a code token): digit words to digits. sym: symbol words to characters (table below; two-word symbols exist).
- number segments by style: cardinal (parse), digits (digit by digit), year (twenty twenty six, two thousand five, nineteen oh five, eleven hundred),
  decimal (point, digits one by one), cardinal_frac (point, then a cardinal), version (cardinal parts joined by point), ordinal (the digits plus
  the standard suffix st/nd/rd/th), date (month name, ordinal day, year words -> ISO yyyy-mm-dd), comma_* (digits with thousands commas),
  pct_* (digits plus percent sign), neg_* (leading minus sign).
- one source token can have several segments (a path: sym, spelled, sym, word ...): concatenate in order.

Letter names (lower case):

| letter | spoken |
|---|---|
| a | ay |
| b | bee |
| c | see |
| d | dee |
| e | ee |
| f | eff |
| g | gee |
| h | aitch |
| i | eye |
| j | jay |
| k | kay |
| l | el |
| m | em |
| n | en |
| o | oh |
| p | pee |
| q | cue |
| r | are |
| s | ess |
| t | tee |
| u | you |
| v | vee |
| w | double you |
| x | ex |
| y | why |
| z | zee |

Symbol words:

| char | spoken |
|---|---|
| `/` | slash |
| `\` | backslash |
| `.` | dot |
| `-` | dash |
| `_` | underscore |
| `~` | tilde |
| `#` | hash |
| `:` | colon |
| `=` | equals |
| `*` | star |
| `@` | at |
| `+` | plus |
| `%` | percent |
| `&` | ampersand |
| `\|` | pipe |
| `<` | less than |
| `>` | greater than |
| `$` | dollar |
| `^` | caret |
| `,` | comma |
| `;` | semicolon |
| `!` | bang |
| `?` | question mark |
| `'` | apostrophe |
| `"` | quote |
| ``` | backtick |
| `(` | open paren |
| `)` | close paren |
| `[` | open bracket |
| `]` | close bracket |
| `{` | open brace |
| `}` | close brace |

## 3. Span-survival checker contract (gate V-C4; also used for every real variant)
`check(doc, hyp_text) -> kept: bool`. `doc` is the full SpokenDoc (B may read tokens, segments, spans). `hyp_text` is the raw ASR text. Rules:
- the variant is kept only if EVERY span survives and no negation word appears in the hypothesis that the reference lacks (and none is missing);
- negation / polarity spans: never recoverable; contractions are equivalent to their expansions (`don't` = `do not`, `cannot` = `can not`);
- number / quantity / date spans: equal if they denote the same canonical value in any written or spoken form (digits, cardinal, digit by digit,
  ordinal, decimal, version, year, date); extra adjacent digits make a longer, different number (altered);
- entity / name / path / flag / rule / statement spans: equal after folding spoken symbols to characters, letter names to letters, digit words to digits
  and dropping fillers (um, uh, er, erm, hmm, mm) and case; a letter run may be spelled, joined, or written as the identifier;
- a span deleted, garbled or replaced by a DIFFERENT valid value is not surviving, even if the true value appears elsewhere in the row;
- the context-recoverable exception is OFF. It applies only if (a) the span role is not authority and (b) re-running the SOURCE family's gold function with the span removed from the user turn gives the same label. Rows on fallback spans never use it.
The planted suite (alterations that must be dropped, equivalences that must be kept) is produced on request with
`planted.planted_suite(n_alter, n_benign, seed)` and handed to B as JSON by the orchestrator. Bars for each of A and B: recall on at least 2,000 planted
alterations >= 99 percent with Wilson lower bound >= 97 percent; false alarms on equivalents <= 1 percent; A-versus-B verdict agreement >= 99.5 percent.

## 4. WER definition (bands, V-C9, V-D5, V-D7)
Unit-level WER against the WRITTEN reference. Reference words: the written source tokens in spoken order plus the spoken disfluency words, fillers excluded
(`span_check.written_reference`). Hypothesis words: the ASR text lower-cased, fillers removed, clause punctuation dropped (a '.' or ',' attached to the end of a word),
tokens kept as words / digit groups / single symbols. Alignment at reference-word level: a reference word may be matched by a contiguous run of hypothesis tokens
(a path dictated as `slash tmp slash build` matches `/tmp/build`; `eight zero eight zero` matches `8080`; `March 14th 2026` matches `2026-03-14`).
Errors: substituted word = number of hypothesis tokens it consumed (at least 1); deleted word = 1; inserted hypothesis token = 1. WER = errors / reference words.
Bands: under 3, 3 to 8, 8 to 15, 15 to 25 percent; over 25 percent excluded. V-D7: the median absolute difference between A's and B's WER on the same variants <= 1 pp.

## 5. Measurements the L4 jobs must produce for the data-production gates (consumed by pool.py)
V-D1 counts of digit-form and word-form numbers in the raw ASR of 100 utterances; V-D2 for each trailing silence in {0, 160, 320, 560, 1120} ms the share of >= 100 utterances whose last three words equal the 1120 ms
reference; V-D3 for 500 pilot variants: condition fields, measured WER, band; V-D4 the clean-condition WER of the under-20-token utterances.
Training variants use only the LOCKED 560 ms chunk with forced flush (160 and 1,120 ms are dev-only).

## 6. Closed tables owned by the lane (hashed by `vcommon.table_hashes`, re-exported at every change)
symbol table, letter names, symbol aliases, fillers (in code); number-form rules (in `numwords.py` and `verbalizer.py`); disfluency rule table (JSON, `disfluency.TEST_TABLE` is a test table);
dictated-NATURAL phrase table (JSON: `ops`, `folder_words`, `file_words`, `flag_phrases`, see `verbalizer.NaturalPhraseTable`); confusion table (JSON from `noiser.harvest_table`).
Authors of the two JSON tables (Haiku medium): original plain wording, no benchmark text, no model-written transcripts.

## 7. Skeptic additions (18 Oct 2026; the build skeptic of lane L-G)

- CHECK AT CREATION. A variant leaves the lane only through `voice_check.check_and_stamp`: source eligibility and stamp currency (a0), B's denormaliser on THIS
  utterance (a1), both span checkers (a2), the context-recoverable exception OFF (a3), generator rules (a4), B's WER band and the token rule (a5), PII and the
  C_DATA_SPEC literals (a6), the G13 stamp of the transcript AND the whole row in batches of <= 500 (b), the stamp record (c). `mix_guard` refuses a voice row
  whose clean twin is not in the mix. No hook, no variant (`StampServiceRequired`).
- GLOBAL POLARITY SIGNATURE. A polarity word (only, except, unless, always, allow, deny, block) that appears or vanishes anywhere in the transcript drops the
  variant, in A (`span_check.pol_sig`) and in B (`vb_hyp.polarity_signature`). Before, only the spans' own words were checked. `nothing`, `nobody`, `nowhere`
  count as negation words in A as they already did in B.
- GENERATOR SHARES. A 55 / B 45 until a passing V-C11 dictionary-licence record exists (`vcommon.dictionary_licence_ok`); then A 50 / B 30 / C 20.
  Generator C is not built. `pool.select_kept(shares=...)` skips a generator that is not in the share table.
- DICTATED-NATURAL. Only the path operations delete, move, rename, copy, create, edit, open, close are eligible (the table calls every target a folder or a
  file); an operation outside that list, or a flag with no phrase, raises `VoiceError` (the paraphrase would change what the instruction targets or silently drop
  a flag). Six template swaps and two flag phrases removed in `pools/natural_phrase_table.json`: `-n` and `-p` mean different things in different tools.
- CONFUSION TABLE. `noiser.harvest_table(..., splits=[...])` refuses any split that is not a LibriSpeech TRAIN split; a table without named splits is TEST-ONLY.
