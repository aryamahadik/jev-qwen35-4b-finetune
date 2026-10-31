# G-block sources (PREREG_FINAL A39 b): fresh real text, 11 sources, 11 domains

Built 13 Oct 2026 (about 16:45-17:35 UTC). No labels exist in this folder. Haiku has not run yet. The card-authoring
tasks are in `cards/tasks/` and their answers will go to `cards/answers/`.

**What is here**

- **Texts.** `texts/<domain>/texts.jsonl` holds one JSON object per line with `{text_id, domain, source, licence_url,
  text}`. Each text is 40-400 words. Texts are cleaned, deduplicated within and across domains, screened for
  personal data and checked to be English.
- **Upstream metadata.** `audit/<domain>_meta.jsonl` holds the upstream metadata for each kept text, keyed by
  `text_id`: categories, departments, classifications, dates and similar.
  - Any human labels a source carries live only in this file.
  - They are **report-only audit data and are never used as targets** (A39 b).
- **Downloads.** `raw/` holds the downloads. They are untrusted data, and `raw/` is git-ignored (660 MB, including
  three Wikimedia XML dumps).
- **Code and checks.** `tools/` holds all the code, run with `.venv/bin/python -I`. `checks/` holds every check input
  and output.

## Sources

| Domain | Texts | Source (upstream) | Licence, as verified on the upstream record |
|---|---|---|---|
| `recipes` | 2,407 | Wikibooks Cookbook namespace, en.wikibooks.org (MediaWiki API wikitext, regex-cleaned) | CC BY-SA 4.0 (siteinfo `rightsinfo`) |
| `travel` | 2,500 | Wikivoyage, en.wikivoyage.org (XML dump of 1 Oct 2026; one prose section per article) | CC BY-SA 4.0 (siteinfo `rightsinfo`) |
| `news` | 2,500 | Wikinews published articles, en.wikinews.org (XML dump of 1 Oct 2026; `{{publish}}` pages; body before "Sources") | Per article date, from `Wikinews:Copyright`. 2,273 CC BY 2.5 (25 Sep 2005 - 16 Dec 2024); 23 CC BY 4.0 (after 16 Dec 2024); 204 public domain (before 25 Sep 2005) |
| `learning` | 2,500 | Wikiversity learning resources, en.wikiversity.org (XML dump of 1 Oct 2026; one prose section per page) | CC BY-SA 4.0 (site footer) |
| `gov_news` | 2,500 | News Releases Issued by Government of Nova Scotia, data.novascotia.ca dataset `xcif-vvr3` (34,282 releases) | Nova Scotia Open Government Licence (`licenseId` OGL_NOVA_SCOTIA on the Socrata record; terms http://novascotia.ca/opendata/licence.asp) |
| `office_help` | 1,642 | Ask LibreOffice community Q&A, ask.libreoffice.org: question posts only (Discourse `posts.json`; code blocks and link previews removed) | CC BY-SA 3.0 ("all text and images on this website", from the site's `/tos`) |
| `sci_abstracts` | 2,209 | bioRxiv preprint abstracts, api.biorxiv.org: 400 random days in 2021-2025, records with `license` cc_by or cc0 only | Per record: 2,119 CC BY 4.0, 90 CC0 (the `license` field of each record) |
| `museum` | 2,499 | Art Institute of Chicago public API, artwork `description` field (api.artic.edu) | CC BY 4.0, from the API's own `info.license_text` ("The `description` field ... is licensed under ... CC-By"); saved in `raw/aic/licence_info.json` |
| `park_programs` | 667 | Delaware State Park Programs, data.delaware.gov dataset `pu7t-3gai` | Public Domain (Socrata record `license`) |
| `volunteer_posts` | 878 | Montgomery County (MD) Volunteer Center Registered Opportunities, data.montgomerycountymd.gov dataset `rrpb-g5ks` | Public Domain (Socrata record `license`) |
| `open_data` | 2,500 | Socrata Discovery API, api.us.socrata.com: dataset name and description from 84 government portals | Per record, permissive only: Public Domain 1,336; Public Domain U.S. Government 643; ODC PDDL 204; CC0 153; CC BY 4.0 115; CC BY-SA 4.0 25; CC BY-SA 3.0 24 |

**Totals and size**

- **Totals:** 11 sources, 11 domains, **22,802 texts**.
- **Median length:** from 61 words (`park_programs`) to 283 words (`gov_news`).
- **Per-domain size:** each domain holds at most 2,500 texts, the "up to ~2,500" target. Three domains are smaller
  because their upstream is small after dedup:
  - `park_programs`: 4,077 rows, 2,614 near-duplicate recurring programmes;
  - `volunteer_posts`: 1,071 rows;
  - `office_help`: 2,776 questions fetched, 567 not English and 507 under 40 words.

**Domain spread.** The 11 domains fall into at least 8 non-adjacent groups even when read conservatively:

1. food (recipes);
2. leisure and outings (`travel`, `park_programs`);
3. journalism and public announcements (`news`, `gov_news`);
4. software help (`office_help`);
5. biology research (`sci_abstracts`);
6. art and museums (`museum`);
7. volunteering and work postings (`volunteer_posts`);
8. learning materials (`learning`);
9. dataset documentation (`open_data`).

## Checks

1. **Deny-list program.** I ran `c_src/common/denylist.py check` as a program and never opened its inputs.
   - **Final result:** 11/11 pass, 0 hits, 0 OHS-3 hits, 0 sealed hits.
   - **Files:** query `checks/denylist_query_final.json`, verdicts `checks/denylist_verdicts_final.json`.
   - **Built list:** `--denylist checks/denylist_built.json`, sha256 52b91ef3799c393c....
   - **Candidate screening:** 28 candidates were checked first (`checks/denylist_verdicts_candidates.json`).
     - Mozilla SUMO (KB and forum) was denied ("Mozilla SUMO support forum").
2. **Not a C1 training source.** I derived the C1 source names by program, names only, from
   `data/v14_parts/golden_train.jsonl` (`source`, `meta.dataset`, `meta.hf_id`). The result is 330 names, in
   `checks/c1_source_names.json` (`tools/c1_sources.py`).
   - Each source's name and host keys were matched against them (`checks/c1_overlap.json`): 0 overlaps.
   - The key "artic" first matched "ParticleMedia" as a substring. That is a false positive, replaced by
     "art institute" / "artic.edu".
3. **Excluded classes.**
   - **Not used:** Wikipedia/NQ, the Federal Register, eCFR and EDGAR. Wikibooks, Wikivoyage, Wikinews and
     Wikiversity are separate Wikimedia projects with their own content.
   - **Also avoided:** DI, JevBench, ejs-5, LongBench and OHS sources. arXiv and Project Gutenberg were avoided as a
     precaution, because LongBench-style suites draw academic papers and novels from them.
4. **OHS-4 sealed hashes, used only at the hash level and only on real C2 text (CHECKERS.md / FORMAT.md rules).**
   - **Keyword hashes vs every source name and host** (`tools/kwcheck.py`, `checks/sealed_keyword_hash_final.json`).
     - Final result: 0 hits for all 11.
     - GOV.UK was a candidate and hit 2 keyword hashes. It was dropped as a likely OHS-4 G source.
   - **Text hashes vs every text** (`tools/source_checks.py texts`): word 10-/12-grams, full text and sentence
     hashes.
     - First run: `recipes` had 93 sentence-hash hits (0 n-gram hits, so these are short generic sentences, not a
       shared source); `museum` had 1 n-gram hit; `volunteer_posts` had 1 sentence hit.
     - All 95 texts were dropped. The final run has 0 hits in all 11 domains (`checks/sealed_text_hash_runs.jsonl`,
       `checks/sealed_text_hash_hits.json`).
     - No source has an n-gram hit rate above 1%, so none looks like an OHS-4 source.
   - The full G13 decontamination (`c2_build/g13_c2.py` plus the sealed-side `g13_ohs4_check.py`) still runs later on
     the built rows (A39 b).
5. **Licence verified upstream** (table above). Rejected on licence or access:
   - OpenStax osbooks repos: every collection is now CC BY-NC-SA 4.0 (`checks/openstax_rejected_licences.json`).
   - NYC Jobs postings: no licence on the record.
   - Canada Job Bank: OGL, but no free text.
   - iNaturalist: almost no descriptions of 40 words or more.
   - NPS alerts: too short and rate-limited.
   - Wikimedia Phabricator: the API needs a login.
   - BCcampus Pressbooks: bot wall.
6. **Cleaning and personal data** (`tools/common.py`).
   - **Contact details.** Any sentence with an email address, phone number, user home path or IP address is removed.
     Afterwards 0 texts contain any of these (`tools/finalize.py` re-checks).
   - **Handles and URLs** are stripped.
   - **News-like domains** (`news`, `gov_news`, `learning`; `open_data` and `volunteer_posts` for honorifics only):
     a text is dropped when it names someone with an honorific (Mr/Ms/Mrs ...) or is about crime, courts, deaths,
     abuse or similar. In these contexts private persons' data is most likely. Drops: news 2,474, gov_news 1,754,
     learning 170.
   - **Contact lines.** Contact-instruction sentences are removed from `park_programs` and `volunteer_posts`.
   - **Length.** Texts over 400 words are cut at a sentence or paragraph boundary.
   - **English.** A text must be at least 97% ASCII letters and pass a stop-word check.
   - **Dedup.** Exact duplicates (normalised) are dropped, and so is any text with 50% or more of its word 8-grams
     already seen in that domain. Exact duplicates across domains are also checked (0 found).
   - **Wikitext.** Templates are removed, and any sentence a removed template would have broken is dropped (no gaps).
7. **Sampling.** Every random draw is seeded (sampling seed 20261013, plus fixed per-source seeds in the tools).
   Re-running `tools/fetch_*.py <source>` rebuilds from the raw cache. After any rebuild, re-run
   `tools/source_checks.py texts` and then `tools/finalize.py`.

## Card-authoring tasks (A39 c): Haiku 5.5 authors wording only

- **Task set.** `tools/make_card_tasks.py` writes 33 tasks (3 per domain): `cards/tasks/<domain>_<k>.json`.
- **Content of each task:**
  - 12 sample texts with opaque ids `s01`..`s12` (396 distinct texts in all; no labels, no text ids, no source ids);
  - an "angle": 1 handling, 2 fit, 3 content;
  - a request for 2 cards: card 1 is yes/no with "yes" and "no" defined; card 2 is a choice of 2-8 options, each
    with a one-sentence definition;
  - the exact answer path: `cards/answers/<domain>_<k>.json`;
  - `allowed_read` and `allowed_write` lists for the file-access audit.
- **Task-to-text mapping.** `cards/tasks_key.json` maps tasks to sample `text_id`s and is never shown to the agent.
  The instruction template sha256 is in both files.
- **Rules given to the agent:**
  - plain everyday language;
  - real decisions, answerable from the text alone;
  - balanced options;
  - no label sets copied from public benchmarks;
  - no questions about people's identity or health;
  - do not label the examples.
- **Not done here.** These steps come later, under A39 c-d: G-LEX 2/2 extraction of each card's options, a
  deny-list schema check, conversion to the cygnet `card` string (`- label: definition` lines), and labels from the
  Haiku → Opus cascade.

## Caveats

- **Forum and wiki text.** `office_help` and `learning` are community-written. Some posts may themselves be
  machine-assisted, and the deny-list cannot see that. Text quality varies.
- **Names in news.** `news` and `gov_news` still name public officials and organisations. The person filter is a
  heuristic, not a guarantee.
- **Run side effect.** The first `denylist.py check` call, without `--denylist`, rebuilt the program's default output
  `lean/data/c_parts/denylist.json`. That file is untracked and deterministic: the same sha256 prefix, 52b91ef3....
  Every later call wrote to `checks/denylist_built.json` instead.
