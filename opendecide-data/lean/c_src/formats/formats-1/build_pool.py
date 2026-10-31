#!/usr/bin/env python3
"""formats-1 authoring source: writes every data file under data/ (C_DATA_SPEC v4 section 6, step 4).

Claude-authored chrome, closed lexicons and layout specs only. No rows, no dataset text, no domain content.
Deterministic (seed 20261003, the A16 config seed). Re-running gives byte-identical files.

Outputs (JSONL, one object per line, every object has a stable "id" and its own "sha256"):
  data/containers.jsonl        14 containers (section 6 list)
  data/skins.jsonl             77 container skins (14 held-out-only: one per container)
  data/card_styles.jsonl       12 card styles (2 held-out-only)
  data/registers.jsonl         4 registers (chrome lexicon per register)
  data/instr_positions.jsonl   5 instruction positions
  data/fences.jsonl            4 fence forms for data containers
  data/styles.jsonl            400 styles = container skin x card style x register x instruction position (+ fence);
                               50 held out (mix-tuning dev only, never trained)
  data/defs_styles.jsonl       definition styles (6 canonical) and their render variants
  data/fewshot_templates.jsonl few-shot card templates
  data/inverted.jsonl          inverted-card frames, case-reference schemes, inverted question frames
  data/label_masks.jsonl       masked label-ID schemes
  data/swap_words.jsonl        familiar words for swapped label names
  data/label_notices.jsonl     optional "names are only names" card sentences
  data/label_rules.jsonl       masked / swapped label-name rules, choice-row visibility rules (LR14, LR15)

v1.1 (review formats-1): card styles and definition variants carry choice_visible / choice_route / on_choice_rows;
LR04 and LR07 require card.loader_check on choice rows; LR14 (every row) and LR15 (inverted rows) added.
"""
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
SEED = 20261003
VERSION = "formats-1 v1.1"

# ----------------------------------------------------------------------------------------------------------------------
# Registers: chrome lexicon only (titles, greetings, headings). Every string passes the negation and marker lints.
REGISTERS = [
    {"id": "RG-formal", "name": "formal",
     "memo_title": "MEMORANDUM", "form_title_fmt": "Form: {title}",
     "email_greeting": "Dear {to},", "email_greeting_generic": "Dear colleagues,",
     "email_closing": "Regards,", "closing_with_name": True, "q_prefix": "Question:",
     "headings": {"definitions": "Definitions", "rules": "Rules", "examples": "Examples", "task": "Task",
                  "notes": "Notes", "labels": "Labels", "levels": "Levels", "cases": "Cases",
                  "reading": "Reading rules", "options": "Options"}},
    {"id": "RG-casual", "name": "casual",
     "memo_title": "Quick memo", "form_title_fmt": "{title}",
     "email_greeting": "Hi {to},", "email_greeting_generic": "Hi all,",
     "email_closing": "Thanks,", "closing_with_name": True, "q_prefix": "",
     "headings": {"definitions": "What the labels mean", "rules": "The rules", "examples": "A few examples",
                  "task": "What to do", "notes": "Worth knowing", "labels": "Labels", "levels": "Levels",
                  "cases": "Cases", "reading": "How to read this", "options": "Choices"}},
    {"id": "RG-terse", "name": "terse",
     "memo_title": "MEMO", "form_title_fmt": "{title}",
     "email_greeting": "", "email_greeting_generic": "",
     "email_closing": "", "closing_with_name": False, "q_prefix": "Q:",
     "headings": {"definitions": "Defs", "rules": "Rules", "examples": "Ex.", "task": "Task", "notes": "Notes",
                  "labels": "Labels", "levels": "Levels", "cases": "Cases", "reading": "Reading",
                  "options": "Opts"}},
    {"id": "RG-verbose", "name": "verbose",
     "memo_title": "Internal memorandum", "form_title_fmt": "Form: {title}",
     "email_greeting": "Good morning {to},", "email_greeting_generic": "Good morning everyone,",
     "email_closing": "With thanks for your time,", "closing_with_name": True,
     "q_prefix": "The question to answer:",
     "headings": {"definitions": "Definitions used in this task", "rules": "Rules that apply",
                  "examples": "Worked examples", "task": "Your task", "notes": "Further notes",
                  "labels": "The available labels", "levels": "The levels of the scale", "cases": "The cases",
                  "reading": "How to read the material", "options": "The choices"}},
]

# ----------------------------------------------------------------------------------------------------------------------
# Instruction positions. The outer prompt layout (schema_branch_mark, cygnet) never changes: positions only order the
# family-supplied parts inside the instructions field, or move the family's card-level task line to the card head/tail.
INSTR_POSITIONS = [
    {"id": "IP1", "name": "wording_then_question_para", "order": ["wording", "question", "note"], "joiner": "\n\n",
     "q_prefix": True, "card_task": "keep"},
    {"id": "IP2", "name": "wording_then_question_inline", "order": ["wording", "question", "note"], "joiner": " ",
     "q_prefix": False, "card_task": "keep"},
    {"id": "IP3", "name": "question_then_wording_para", "order": ["question", "wording", "note"], "joiner": "\n\n",
     "q_prefix": True, "card_task": "keep"},
    {"id": "IP4", "name": "task_at_card_head", "order": ["wording", "question", "note"], "joiner": "\n",
     "q_prefix": False, "card_task": "head"},
    {"id": "IP5", "name": "task_at_card_tail", "order": ["wording", "question", "note"], "joiner": "\n\n",
     "q_prefix": False, "card_task": "tail"},
]

FENCES = [
    {"id": "FN-none", "name": "none", "open": "", "close": "", "indent": ""},
    {"id": "FN-bt", "name": "backticks", "open": "```", "close": "```", "indent": ""},
    {"id": "FN-btlang", "name": "backticks_lang", "open": "```{lang}", "close": "```", "indent": ""},
    {"id": "FN-ind4", "name": "indent4", "open": "", "close": "", "indent": "    "},
]

# ----------------------------------------------------------------------------------------------------------------------
# Containers (C_DATA_SPEC v4 section 6 list, in order). `accepts` = Doc IR block types the renderer handles natively.
CONTAINERS = [
    {"id": "CT01", "name": "prose", "accepts": ["para", "items", "steps", "section", "fields"], "fenceable": False,
     "typed": False, "attribution_frame": False, "lang": ""},
    {"id": "CT02", "name": "memo", "accepts": ["meta", "para", "items", "steps", "fields", "table", "section"],
     "fenceable": False, "typed": False, "attribution_frame": False, "lang": ""},
    {"id": "CT03", "name": "email_thread", "accepts": ["meta", "messages", "para", "items", "steps", "fields",
                                                       "section"],
     "fenceable": False, "typed": False, "attribution_frame": True, "lang": ""},
    {"id": "CT04", "name": "chat_log", "accepts": ["messages"], "fenceable": False, "typed": False,
     "attribution_frame": True, "lang": ""},
    {"id": "CT05", "name": "json", "accepts": ["meta", "para", "items", "steps", "fields", "table", "events",
                                               "messages", "section"],
     "fenceable": True, "typed": True, "attribution_frame": False, "lang": "json"},
    {"id": "CT06", "name": "yaml", "accepts": ["meta", "para", "items", "steps", "fields", "table", "events",
                                               "messages", "section"],
     "fenceable": True, "typed": True, "attribution_frame": False, "lang": "yaml"},
    {"id": "CT07", "name": "csv", "accepts": ["table", "fields", "events"], "fenceable": True, "typed": False,
     "attribution_frame": False, "lang": "csv"},
    {"id": "CT08", "name": "markdown_table", "accepts": ["meta", "para", "items", "steps", "fields", "table", "events",
                                                         "section"],
     "fenceable": False, "typed": False, "attribution_frame": False, "lang": ""},
    {"id": "CT09", "name": "html_snippet", "accepts": ["meta", "para", "items", "steps", "fields", "table", "events",
                                                       "section"],
     "fenceable": True, "typed": False, "attribution_frame": False, "lang": "html"},
    {"id": "CT10", "name": "key_value", "accepts": ["meta", "fields", "table", "events", "section"], "fenceable": True,
     "typed": False, "attribution_frame": False, "lang": "text"},
    {"id": "CT11", "name": "bullet_sop", "accepts": ["meta", "para", "items", "steps", "fields", "section"],
     "fenceable": False, "typed": False, "attribution_frame": False, "lang": ""},
    {"id": "CT12", "name": "log_lines", "accepts": ["events"], "fenceable": True, "typed": False,
     "attribution_frame": True, "lang": "text"},
    {"id": "CT13", "name": "diff", "accepts": ["changes"], "fenceable": True, "typed": False,
     "attribution_frame": False, "lang": "diff"},
    {"id": "CT14", "name": "form", "accepts": ["meta", "fields", "section", "para", "table"], "fenceable": False,
     "typed": False, "attribution_frame": False, "lang": ""},
]

# Skins: params read by fmt1/render.py; "grammar" = line regexes (Python re) that every rendered line of that kind
# matches, so a family can write its own G3 parser from the grammar, never from the renderer code.
SKINS = [
    # ---- prose
    {"id": "prose.plain", "container": "prose", "held_out_only": False,
     "params": {"title": "plain", "heading": "plain", "list_mode": "inline", "field_fmt": "{key}: {value}."},
     "flags": {}},
    {"id": "prose.titled_caps", "container": "prose", "held_out_only": False,
     "params": {"title": "caps", "heading": "colon", "list_mode": "inline", "field_fmt": "The {key_l} is {value}."},
     "flags": {}},
    {"id": "prose.numbered_paras", "container": "prose", "held_out_only": False,
     "params": {"title": "plain", "heading": "plain", "list_mode": "numbered_paras", "para_num": "{i}. ",
                "field_fmt": "{key}: {value}."},
     "flags": {"adds_numbers": True}},
    {"id": "prose.lines", "container": "prose", "held_out_only": False,
     "params": {"title": "underline", "heading": "plain", "list_mode": "lines", "field_fmt": "{key}: {value}."},
     "flags": {}},
    {"id": "prose.section_signs", "container": "prose", "held_out_only": True,
     "params": {"title": "plain", "heading": "section_sign", "list_mode": "inline", "field_fmt": "{key}: {value}."},
     "flags": {"adds_numbers": True, "unicode_chrome": True}},
    # ---- memo
    {"id": "memo.classic", "container": "memo", "held_out_only": False,
     "params": {"header_fmt": "{label}: {value}", "rule": "=" * 32, "heading": "caps", "bullet": "- ",
                "step": "{i}. ", "table": "aligned", "title_slot": "top"},
     "flags": {"labelled_lines": True}},
    {"id": "memo.notice", "container": "memo", "held_out_only": False,
     "params": {"header_fmt": "{label}: {value}", "rule": "", "heading": "colon", "bullet": "• ",
                "step": "{i}) ", "table": "aligned", "title_slot": "top"},
     "flags": {"labelled_lines": True, "unicode_chrome": True}},
    {"id": "memo.internal", "container": "memo", "held_out_only": False,
     "params": {"header_fmt": "{label} | {value}", "rule": "", "heading": "plain", "bullet": "* ",
                "step": "{i}. ", "table": "pipe", "title_slot": "inline"},
     "flags": {"labelled_lines": True}},
    {"id": "memo.briefing", "container": "memo", "held_out_only": False,
     "params": {"header_fmt": "[{label}] {value}", "rule": "", "heading": "numbered", "bullet": "- ",
                "step": "{i}. ", "table": "aligned", "title_slot": "top"},
     "flags": {"labelled_lines": True, "adds_numbers": True}},
    {"id": "memo.circular", "container": "memo", "held_out_only": True,
     "params": {"header_fmt": "{LABEL} {dots} {value}", "rule": "*" * 24, "heading": "caps", "bullet": "+ ",
                "step": "({i}) ", "table": "aligned", "title_slot": "top"},
     "flags": {"labelled_lines": True}},
    # ---- email_thread
    {"id": "email.newest_quoted", "container": "email_thread", "held_out_only": False,
     "params": {"order": "newest_first", "quote": "> ", "attribution": "On {ts}, {speaker} wrote:",
                "headers": ["From", "To", "Date", "Subject"]},
     "flags": {"speaker_prefix": True, "labelled_lines": True}},
    {"id": "email.oldest_blocks", "container": "email_thread", "held_out_only": False,
     "params": {"order": "oldest_first", "separator": "*" * 20, "headers": ["From", "To", "Date", "Subject"]},
     "flags": {"speaker_prefix": True, "labelled_lines": True}},
    {"id": "email.single", "container": "email_thread", "held_out_only": False,
     "params": {"order": "single", "headers": ["From", "To", "Date", "Subject"], "bullet": "- ", "step": "{i}. "},
     "flags": {"labelled_lines": True}},
    {"id": "email.digest", "container": "email_thread", "held_out_only": False,
     "params": {"order": "oldest_first", "separator": "", "counter": "Message {i} of {n}",
                "headers": ["From", "To", "Sent", "Subject"]},
     "flags": {"speaker_prefix": True, "labelled_lines": True, "adds_numbers": True}},
    {"id": "email.list_archive", "container": "email_thread", "held_out_only": True,
     "params": {"order": "oldest_first", "separator": "=" * 20, "headers": ["Sender", "To", "Posted", "Subject"],
                "subject_prefix": "[{title}] "},
     "flags": {"speaker_prefix": True, "labelled_lines": True}},
    # ---- chat_log
    {"id": "chat.bracket_time", "container": "chat_log", "held_out_only": False,
     "params": {"line": "[{ts}] {speaker}: {text}", "needs_ts": True, "block": False, "ts_fmt": "%Y-%m-%d %H:%M"},
     "flags": {"speaker_prefix": True}},
    {"id": "chat.name_time", "container": "chat_log", "held_out_only": False,
     "params": {"line": "{speaker} ({ts}): {text}", "needs_ts": True, "block": False, "ts_fmt": "%d %b %Y %H:%M"},
     "flags": {"speaker_prefix": True}},
    {"id": "chat.plain", "container": "chat_log", "held_out_only": False,
     "params": {"line": "{speaker}: {text}", "needs_ts": False, "block": False, "ts_fmt": None},
     "flags": {"speaker_prefix": True}},
    {"id": "chat.angle", "container": "chat_log", "held_out_only": False,
     "params": {"line": "<{speaker}> {text}", "needs_ts": False, "block": False, "ts_fmt": None},
     "flags": {"speaker_prefix": True}},
    {"id": "chat.block", "container": "chat_log", "held_out_only": False,
     "params": {"line": "{speaker}  {ts}\n{text}", "needs_ts": True, "block": True, "ts_fmt": "%d %b %Y %H:%M"},
     "flags": {"speaker_prefix": True}},
    {"id": "chat.pipe", "container": "chat_log", "held_out_only": True,
     "params": {"line": "{ts} | {speaker} | {text}", "needs_ts": True, "block": False, "ts_fmt": "%Y-%m-%d %H:%M"},
     "flags": {"speaker_prefix": True}},
    # ---- json
    {"id": "json.pretty2", "container": "json", "held_out_only": False,
     "params": {"indent": 2, "key_case": "snake", "layout": "object", "vocab": "v1"}, "flags": {"rewrites_keys": True}},
    {"id": "json.pretty4", "container": "json", "held_out_only": False,
     "params": {"indent": 4, "key_case": "as_given", "layout": "object", "vocab": "v2"}, "flags": {}},
    {"id": "json.compact", "container": "json", "held_out_only": False,
     "params": {"indent": None, "key_case": "snake", "layout": "object", "vocab": "v1"},
     "flags": {"rewrites_keys": True}},
    {"id": "json.lines", "container": "json", "held_out_only": False,
     "params": {"indent": None, "key_case": "snake", "layout": "lines", "vocab": "v1"},
     "flags": {"rewrites_keys": True, "single_collection": True}},
    {"id": "json.array", "container": "json", "held_out_only": False,
     "params": {"indent": 2, "key_case": "snake", "layout": "array", "vocab": "v2"},
     "flags": {"rewrites_keys": True, "single_collection": True}},
    {"id": "json.camel", "container": "json", "held_out_only": True,
     "params": {"indent": 2, "key_case": "camel", "layout": "object", "vocab": "v2"}, "flags": {"rewrites_keys": True}},
    # ---- yaml
    {"id": "yaml.block", "container": "yaml", "held_out_only": False,
     "params": {"indent": 2, "seq_indent": False, "key_case": "snake", "rows": "block", "title": "key", "vocab": "v1"},
     "flags": {"rewrites_keys": True}},
    {"id": "yaml.indented", "container": "yaml", "held_out_only": False,
     "params": {"indent": 2, "seq_indent": True, "key_case": "snake", "rows": "block", "title": "key", "vocab": "v2"},
     "flags": {"rewrites_keys": True}},
    {"id": "yaml.flow_rows", "container": "yaml", "held_out_only": False,
     "params": {"indent": 2, "seq_indent": False, "key_case": "snake", "rows": "flow", "title": "key", "vocab": "v1"},
     "flags": {"rewrites_keys": True}},
    {"id": "yaml.comment_title", "container": "yaml", "held_out_only": False,
     "params": {"indent": 2, "seq_indent": True, "key_case": "as_given", "rows": "block", "title": "comment",
                "vocab": "v2"},
     "flags": {}},
    {"id": "yaml.four", "container": "yaml", "held_out_only": True,
     "params": {"indent": 4, "seq_indent": True, "key_case": "snake", "rows": "block", "title": "key", "vocab": "v1"},
     "flags": {"rewrites_keys": True}},
    # ---- csv (delimited and aligned text tables)
    {"id": "csv.comma", "container": "csv", "held_out_only": False,
     "params": {"delim": ",", "quote_all": False, "fixed": False, "vocab": "v1"}, "flags": {"tabular": True}},
    {"id": "csv.semicolon", "container": "csv", "held_out_only": False,
     "params": {"delim": ";", "quote_all": False, "fixed": False, "vocab": "v2"}, "flags": {"tabular": True}},
    {"id": "csv.tab", "container": "csv", "held_out_only": False,
     "params": {"delim": "\t", "quote_all": False, "fixed": False, "vocab": "v1"}, "flags": {"tabular": True}},
    {"id": "csv.pipe", "container": "csv", "held_out_only": False,
     "params": {"delim": "|", "quote_all": False, "fixed": False, "vocab": "v2"}, "flags": {"tabular": True}},
    {"id": "csv.fixed_width", "container": "csv", "held_out_only": False,
     "params": {"delim": "  ", "quote_all": False, "fixed": True, "vocab": "v1"}, "flags": {"tabular": True}},
    {"id": "csv.quoted_all", "container": "csv", "held_out_only": True,
     "params": {"delim": ",", "quote_all": True, "fixed": False, "vocab": "v2"}, "flags": {"tabular": True}},
    # ---- markdown_table
    {"id": "md.pipes", "container": "markdown_table", "held_out_only": False,
     "params": {"table": "md", "align": False, "title": "hash2", "heading": "hash3", "bullet": "- ", "step": "{i}. ",
                "caption": "plain", "vocab": "v1"},
     "flags": {"tabular": True, "markdown": True}},
    {"id": "md.aligned", "container": "markdown_table", "held_out_only": False,
     "params": {"table": "md", "align": True, "title": "hash2", "heading": "hash3", "bullet": "* ", "step": "{i}. ",
                "caption": "plain", "vocab": "v2"},
     "flags": {"tabular": True, "markdown": True}},
    {"id": "md.headed", "container": "markdown_table", "held_out_only": False,
     "params": {"table": "md", "align": False, "title": "hash1", "heading": "hash2", "bullet": "- ", "step": "{i}. ",
                "caption": "hash3", "vocab": "v1"},
     "flags": {"tabular": True, "markdown": True}},
    {"id": "md.bold_caption", "container": "markdown_table", "held_out_only": False,
     "params": {"table": "md", "align": True, "title": "bold", "heading": "bold", "bullet": "- ", "step": "{i}. ",
                "caption": "bold", "vocab": "v2"},
     "flags": {"tabular": True, "markdown": True}},
    {"id": "md.grid", "container": "markdown_table", "held_out_only": True,
     "params": {"table": "grid", "align": False, "title": "hash2", "heading": "hash3", "bullet": "- ", "step": "{i}. ",
                "caption": "plain", "vocab": "v1"},
     "flags": {"tabular": True}},
    # ---- html_snippet
    {"id": "html.pretty", "container": "html_snippet", "held_out_only": False,
     "params": {"pretty": True, "fields": "table", "wrapper": "", "title_tag": "h2", "heading_tag": "h3",
                "thead": True, "vocab": "v1"},
     "flags": {"html": True, "tabular": True}},
    {"id": "html.compact", "container": "html_snippet", "held_out_only": False,
     "params": {"pretty": False, "fields": "table", "wrapper": "", "title_tag": "h3", "heading_tag": "h4",
                "thead": True, "vocab": "v2"},
     "flags": {"html": True, "tabular": True}},
    {"id": "html.dl_fields", "container": "html_snippet", "held_out_only": False,
     "params": {"pretty": True, "fields": "dl", "wrapper": "", "title_tag": "h2", "heading_tag": "h3",
                "thead": True, "vocab": "v1"},
     "flags": {"html": True, "tabular": True}},
    {"id": "html.div_wrapped", "container": "html_snippet", "held_out_only": False,
     "params": {"pretty": True, "fields": "table", "wrapper": "div", "title_tag": "h3", "heading_tag": "h4",
                "thead": False, "vocab": "v2"},
     "flags": {"html": True, "tabular": True}},
    {"id": "html.article", "container": "html_snippet", "held_out_only": True,
     "params": {"pretty": True, "fields": "row_th", "wrapper": "article", "title_tag": "h2", "heading_tag": "h3",
                "thead": True, "caption_tag": True, "vocab": "v1"},
     "flags": {"html": True, "tabular": True}},
    # ---- key_value
    {"id": "kv.colon", "container": "key_value", "held_out_only": False,
     "params": {"line": "{key}: {value}", "key_case": "as_given", "align": False, "section": "bracket", "vocab": "v1"},
     "flags": {"labelled_lines": True}},
    {"id": "kv.equals", "container": "key_value", "held_out_only": False,
     "params": {"line": "{key} = {value}", "key_case": "snake", "align": False, "section": "hash", "vocab": "v1"},
     "flags": {"labelled_lines": True, "rewrites_keys": True}},
    {"id": "kv.dots", "container": "key_value", "held_out_only": False,
     "params": {"line": "{key} {dots} {value}", "key_case": "as_given", "align": True, "section": "caps", "vocab": "v1"},
     "flags": {"labelled_lines": True}},
    {"id": "kv.ini", "container": "key_value", "held_out_only": False,
     "params": {"line": "{key}={value}", "key_case": "snake", "align": False, "section": "ini", "vocab": "v1"},
     "flags": {"labelled_lines": True, "rewrites_keys": True}},
    {"id": "kv.aligned_colon", "container": "key_value", "held_out_only": False,
     "params": {"line": "{key}:{pad} {value}", "key_case": "as_given", "align": True, "section": "hash", "vocab": "v1"},
     "flags": {"labelled_lines": True}},
    {"id": "kv.double_colon", "container": "key_value", "held_out_only": True,
     "params": {"line": "{key} :: {value}", "key_case": "snake", "align": False, "section": "colon", "vocab": "v1"},
     "flags": {"labelled_lines": True, "rewrites_keys": True}},
    # ---- bullet_sop
    {"id": "sop.numbered", "container": "bullet_sop", "held_out_only": False,
     "params": {"step": "{i}. ", "bullet": "- ", "heading": "colon", "nested": False, "title": "plain"},
     "flags": {}},
    {"id": "sop.stars", "container": "bullet_sop", "held_out_only": False,
     "params": {"step": "Step {i}: ", "bullet": "* ", "heading": "equals", "nested": False, "title": "plain"},
     "flags": {}},
    {"id": "sop.dots", "container": "bullet_sop", "held_out_only": False,
     "params": {"step": "{i}) ", "bullet": "• ", "heading": "caps", "nested": False, "title": "caps"},
     "flags": {"unicode_chrome": True}},
    {"id": "sop.nested", "container": "bullet_sop", "held_out_only": False,
     "params": {"step": "{i}. ", "bullet": "- ", "heading": "bullet", "nested": True, "title": "plain"},
     "flags": {}},
    {"id": "sop.parens", "container": "bullet_sop", "held_out_only": True,
     "params": {"step": "({i}) ", "bullet": "+ ", "heading": "bracket", "nested": False, "title": "bracket"},
     "flags": {}},
    # ---- log_lines
    {"id": "log.iso", "container": "log_lines", "held_out_only": False,
     "params": {"ts_fmt": "%Y-%m-%dT%H:%M:%S", "parts": ["ts", "level", "actor_colon", "text"], "level_case": "upper"},
     "flags": {"speaker_prefix": True}},
    {"id": "log.bracket", "container": "log_lines", "held_out_only": False,
     "params": {"ts_fmt": "%Y-%m-%d %H:%M:%S", "parts": ["ts_br", "level_br", "actor_angle", "text"],
                "level_case": "upper"},
     "flags": {"speaker_prefix": True}},
    {"id": "log.logfmt", "container": "log_lines", "held_out_only": False,
     "params": {"ts_fmt": "%Y-%m-%dT%H:%M:%S", "parts": ["logfmt"], "level_case": "lower"},
     "flags": {"speaker_prefix": True}},
    {"id": "log.pipe", "container": "log_lines", "held_out_only": False,
     "params": {"ts_fmt": "%Y-%m-%d %H:%M", "parts": ["pipe"], "level_case": "upper"},
     "flags": {"speaker_prefix": True}},
    {"id": "log.dayfirst", "container": "log_lines", "held_out_only": False,
     "params": {"ts_fmt": "%d %b %Y %H:%M:%S", "parts": ["ts", "actor_colon", "level_paren", "text"],
                "level_case": "lower"},
     "flags": {"speaker_prefix": True}},
    {"id": "log.tabbed", "container": "log_lines", "held_out_only": True,
     "params": {"ts_fmt": "%Y%m%d %H%M%S", "parts": ["tab"], "level_case": "upper"},
     "flags": {"speaker_prefix": True}},
    # ---- diff (changes blocks: ordered entries, each a context line or a change)
    {"id": "diff.unified_path", "container": "diff", "held_out_only": False,
     "params": {"form": "unified", "header": "path", "hunk": True},
     "flags": {"carries_path": True, "adds_numbers": True}},
    {"id": "diff.unified_labels", "container": "diff", "held_out_only": False,
     "params": {"form": "unified", "header": "labels", "hunk": False, "labels": ["old", "new"]},
     "flags": {}},
    {"id": "diff.word", "container": "diff", "held_out_only": False,
     "params": {"form": "word"}, "flags": {}},
    {"id": "diff.table", "container": "diff", "held_out_only": False,
     "params": {"form": "table", "columns": ["Field", "Before", "After"]}, "flags": {"tabular": True}},
    {"id": "diff.changelog", "container": "diff", "held_out_only": False,
     "params": {"form": "changelog", "changed": "Changed {key} from {old} to {new}.", "added": "Added {key}: {new}.",
                "removed": "Removed {key} (was {old}).", "same": "Kept {key}: {value}."},
     "flags": {}},
    {"id": "diff.normal", "container": "diff", "held_out_only": True,
     "params": {"form": "normal"}, "flags": {}},
    # ---- form
    {"id": "form.colon", "container": "form", "held_out_only": False,
     "params": {"field": "{label}: {value}", "heading": "underline", "numbered": False, "checkbox": False,
                "caps_labels": False},
     "flags": {"labelled_lines": True}},
    {"id": "form.brackets", "container": "form", "held_out_only": False,
     "params": {"field": "{label}: [ {value} ]", "heading": "caps", "numbered": False, "checkbox": False,
                "caps_labels": False},
     "flags": {"labelled_lines": True}},
    {"id": "form.numbered", "container": "form", "held_out_only": False,
     "params": {"field": "{n}. {label}: {value}", "heading": "colon", "numbered": True, "checkbox": False,
                "caps_labels": False},
     "flags": {"labelled_lines": True, "adds_numbers": True}},
    {"id": "form.checkbox", "container": "form", "held_out_only": False,
     "params": {"field": "{label}: {value}", "heading": "caps", "numbered": False, "checkbox": True,
                "caps_labels": False},
     "flags": {"labelled_lines": True}},
    {"id": "form.leaders", "container": "form", "held_out_only": False,
     "params": {"field": "{label} {dots} {value}", "heading": "underline", "numbered": False, "checkbox": False,
                "caps_labels": False},
     "flags": {"labelled_lines": True}},
    {"id": "form.caps_labels", "container": "form", "held_out_only": True,
     "params": {"field": "{LABEL}: {value}", "heading": "bracket", "numbered": False, "checkbox": True,
                "caps_labels": True},
     "flags": {"labelled_lines": True}},
]

# Grammars: what a family's own G3 parser reads (never this repo's renderer code). `lines` maps a line kind to a
# Python regex; `full_cover` = every non-empty line of the rendered container (inside its fence) matches one of them.
SP = r"[^:\[\]<>|()\t]+?"
G_TS_ISO = r"(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})"
GRAMMARS = {
    "prose.plain": {"parser": "paragraphs", "full_cover": False, "para_sep": "\n\n",
                    "lists": "items/steps/field sentences joined by one space in one paragraph",
                    "lines": {"field_sentence": r"(?P<key>[^:]+): (?P<value>.+)\."}},
    "prose.titled_caps": {"parser": "paragraphs", "full_cover": False, "para_sep": "\n\n",
                          "lists": "joined by one space in one paragraph", "title": "upper case first paragraph",
                          "lines": {"heading": r"^(?P<heading>[^\n]+):$",
                                    "field_sentence": r"The (?P<key>.+?) is (?P<value>.+)\."}},
    "prose.numbered_paras": {"parser": "paragraphs", "full_cover": False, "para_sep": "\n\n",
                             "lists": "each item its own numbered paragraph",
                             "lines": {"numbered_para": r"^(?P<i>\d+)\. (?P<text>.+)$"}},
    "prose.lines": {"parser": "paragraphs", "full_cover": False, "para_sep": "\n\n",
                    "lists": "one item per line inside one paragraph",
                    "lines": {"title_rule": r"^=+$"}},
    "prose.section_signs": {"parser": "paragraphs", "full_cover": False, "para_sep": "\n\n",
                            "lists": "joined by one space in one paragraph",
                            "lines": {"heading": "^§ (?P<n>\\d+) (?P<heading>.+)$"}},
    "memo.classic": {"parser": "header_body", "full_cover": False,
                     "lines": {"header": r"^(?P<label>[^:]+): (?P<value>.+)$", "rule": r"^={32}$",
                               "bullet": r"^- (?P<item>.+)$", "step": r"^(?P<i>\d+)\. (?P<item>.+)$"}},
    "memo.notice": {"parser": "header_body", "full_cover": False,
                    "lines": {"header": r"^(?P<label>[^:]+): (?P<value>.+)$", "bullet": "^• (?P<item>.+)$",
                              "step": r"^(?P<i>\d+)\) (?P<item>.+)$", "heading": r"^(?P<heading>.+):$"}},
    "memo.internal": {"parser": "header_body", "full_cover": False,
                      "lines": {"title": r"^(?P<word>.+?) \| (?P<title>.+)$",
                                "header": r"^(?P<label>[^|]+) \| (?P<value>.+)$", "bullet": r"^\* (?P<item>.+)$",
                                "step": r"^(?P<i>\d+)\. (?P<item>.+)$"}},
    "memo.briefing": {"parser": "header_body", "full_cover": False,
                      "lines": {"header": r"^\[(?P<label>[^\]]+)\] (?P<value>.+)$", "bullet": r"^- (?P<item>.+)$",
                                "heading": r"^(?P<n>\d+)\. (?P<heading>.+)$"}},
    "memo.circular": {"parser": "header_body", "full_cover": False,
                      "lines": {"header": r"^(?P<label>[^.]+?) \.{3,} (?P<value>.+)$", "rule": r"^\*{24}$",
                                "bullet": r"^\+ (?P<item>.+)$", "step": r"^\((?P<i>\d+)\) (?P<item>.+)$"}},
    "email.newest_quoted": {"parser": "email", "full_cover": False,
                            "lines": {"header": r"^(?P<name>From|To|Date|Subject): (?P<value>.+)$",
                                      "attribution": r"^(?:> )*On (?P<ts>.+?), (?P<speaker>.+) wrote:$",
                                      "quoted": r"^(?P<depth>(?:> ?)+)(?P<text>.*)$"}},
    "email.oldest_blocks": {"parser": "email", "full_cover": False,
                            "lines": {"header": r"^(?P<name>From|To|Date|Subject): (?P<value>.+)$",
                                      "separator": r"^\*{20}$"}},
    "email.single": {"parser": "email", "full_cover": False,
                     "lines": {"header": r"^(?P<label>[^:]+): (?P<value>.+)$", "bullet": r"^- (?P<item>.+)$"}},
    "email.digest": {"parser": "email", "full_cover": False,
                     "lines": {"counter": r"^Message (?P<i>\d+) of (?P<n>\d+)$",
                               "header": r"^(?P<name>From|To|Sent|Subject): (?P<value>.+)$"}},
    "email.list_archive": {"parser": "email", "full_cover": False,
                           "lines": {"header": r"^(?P<name>Sender|To|Posted|Subject): (?P<value>.+)$",
                                     "separator": r"^={20}$"}},
    "chat.bracket_time": {"parser": "lines", "full_cover": True,
                          "lines": {"message": r"^\[(?P<ts>[^\]]+)\] (?P<speaker>" + SP + r"): (?P<text>.+)$"}},
    "chat.name_time": {"parser": "lines", "full_cover": True,
                       "lines": {"message": r"^(?P<speaker>" + SP + r") \((?P<ts>[^)]+)\): (?P<text>.+)$"}},
    "chat.plain": {"parser": "lines", "full_cover": True,
                   "lines": {"message": r"^(?P<speaker>" + SP + r"): (?P<text>.+)$"}},
    "chat.angle": {"parser": "lines", "full_cover": True,
                   "lines": {"message": r"^<(?P<speaker>[^<>]+)> (?P<text>.+)$"}},
    "chat.block": {"parser": "blocks", "full_cover": True, "block_sep": "\n\n",
                   "lines": {"head": r"^(?P<speaker>" + SP + r")  (?P<ts>\S.*)$", "text": r"^(?P<text>.+)$"}},
    "chat.pipe": {"parser": "lines", "full_cover": True,
                  "lines": {"message": r"^(?P<ts>[^|]+?) \| (?P<speaker>[^|]+?) \| (?P<text>.+)$"}},
    "json.pretty2": {"parser": "json", "full_cover": True, "layout": "object", "lines": {}},
    "json.pretty4": {"parser": "json", "full_cover": True, "layout": "object", "lines": {}},
    "json.compact": {"parser": "json", "full_cover": True, "layout": "object", "lines": {}},
    "json.lines": {"parser": "jsonl", "full_cover": True, "layout": "one object per line", "lines": {}},
    "json.array": {"parser": "json", "full_cover": True, "layout": "top-level array", "lines": {}},
    "json.camel": {"parser": "json", "full_cover": True, "layout": "object", "lines": {}},
    "yaml.block": {"parser": "yaml_safe_load", "full_cover": True, "lines": {}},
    "yaml.indented": {"parser": "yaml_safe_load", "full_cover": True, "lines": {}},
    "yaml.flow_rows": {"parser": "yaml_safe_load", "full_cover": True, "lines": {}},
    "yaml.comment_title": {"parser": "yaml_safe_load", "full_cover": True, "title": "first line '# <title>'",
                           "lines": {}},
    "yaml.four": {"parser": "yaml_safe_load", "full_cover": True, "lines": {}},
    "csv.comma": {"parser": "csv", "full_cover": True, "delimiter": ",", "quoting": "minimal", "lines": {}},
    "csv.semicolon": {"parser": "csv", "full_cover": True, "delimiter": ";", "quoting": "minimal", "lines": {}},
    "csv.tab": {"parser": "csv", "full_cover": True, "delimiter": "\t", "quoting": "minimal", "lines": {}},
    "csv.pipe": {"parser": "csv", "full_cover": True, "delimiter": "|", "quoting": "minimal", "lines": {}},
    "csv.fixed_width": {"parser": "fixed_width", "full_cover": True, "col_sep": r" {2,}", "lines": {}},
    "csv.quoted_all": {"parser": "csv", "full_cover": True, "delimiter": ",", "quoting": "all", "lines": {}},
    "md.pipes": {"parser": "markdown", "full_cover": False,
                 "lines": {"row": r"^\| (?P<cells>.*) \|$", "sep": r"^\|(?: :?-{3,}:? \|)+$",
                           "heading": r"^#{2,4} (?P<heading>.+)$", "bullet": r"^- (?P<item>.+)$"}},
    "md.aligned": {"parser": "markdown", "full_cover": False,
                   "lines": {"row": r"^\| (?P<cells>.*) \|$", "sep": r"^\|(?: :?-{3,}:? \|)+$",
                             "heading": r"^#{2,4} (?P<heading>.+)$", "bullet": r"^\* (?P<item>.+)$"}},
    "md.headed": {"parser": "markdown", "full_cover": False,
                  "lines": {"row": r"^\| (?P<cells>.*) \|$", "sep": r"^\|(?: :?-{3,}:? \|)+$",
                            "heading": r"^#{1,4} (?P<heading>.+)$", "bullet": r"^- (?P<item>.+)$"}},
    "md.bold_caption": {"parser": "markdown", "full_cover": False,
                        "lines": {"row": r"^\| (?P<cells>.*) \|$", "sep": r"^\|(?: :?-{3,}:? \|)+$",
                                  "heading": r"^\*\*(?P<heading>.+)\*\*$", "bullet": r"^- (?P<item>.+)$"}},
    "md.grid": {"parser": "markdown_grid", "full_cover": False,
                "lines": {"border": r"^\+(?:-+\+)+$", "head_sep": r"^\+(?:=+\+)+$", "row": r"^\| (?P<cells>.*) \|$",
                          "heading": r"^#{2,4} (?P<heading>.+)$"}},
    "html.pretty": {"parser": "html", "full_cover": True, "lines": {}},
    "html.compact": {"parser": "html", "full_cover": True, "lines": {}},
    "html.dl_fields": {"parser": "html", "full_cover": True, "lines": {}},
    "html.div_wrapped": {"parser": "html", "full_cover": True, "lines": {}},
    "html.article": {"parser": "html", "full_cover": True, "lines": {}},
    "kv.colon": {"parser": "lines", "full_cover": True,
                 "lines": {"pair": r"^(?P<key>[^:\[\]]+): (?P<value>.+)$", "blank": r"^(?P<key>[^:\[\]]+):$",
                           "section": r"^\[(?P<section>[^\]]+)\]$"}},
    "kv.equals": {"parser": "lines", "full_cover": True,
                  "lines": {"pair": r"^(?P<key>[a-z0-9_]+) = (?P<value>.+)$", "blank": r"^(?P<key>[a-z0-9_]+) =$",
                            "section": r"^# (?P<section>.+)$"}},
    "kv.dots": {"parser": "lines", "full_cover": True,
                "lines": {"pair": r"^(?P<key>.+?) \.{3,} (?P<value>.+)$", "blank": r"^(?P<key>.+?) \.{3,}$",
                          "section": r"^(?P<section>[^.a-z]+)$"}},
    "kv.ini": {"parser": "lines", "full_cover": True,
               "lines": {"pair": r"^(?P<key>[a-z0-9_]+)=(?P<value>.+)$", "blank": r"^(?P<key>[a-z0-9_]+)=$",
                         "section": r"^\[(?P<section>[a-z0-9_]+)\]$"}},
    "kv.aligned_colon": {"parser": "lines", "full_cover": True,
                         "lines": {"pair": r"^(?P<key>[^:#]+?): +(?P<value>\S.*)$", "blank": r"^(?P<key>[^:#]+?):$",
                                   "section": r"^# (?P<section>.+)$"}},
    "kv.double_colon": {"parser": "lines", "full_cover": True,
                        "lines": {"pair": r"^(?P<key>[a-z0-9_]+) :: (?P<value>.+)$",
                                  "blank": r"^(?P<key>[a-z0-9_]+) ::$", "section": r"^(?P<section>[^:]+):$"}},
    "sop.numbered": {"parser": "list_doc", "full_cover": False,
                     "lines": {"step": r"^(?P<i>\d+)\. (?P<item>.+)$", "bullet": r"^- (?P<item>.+)$",
                               "heading": r"^(?P<heading>.+):$"}},
    "sop.stars": {"parser": "list_doc", "full_cover": False,
                  "lines": {"step": r"^Step (?P<i>\d+): (?P<item>.+)$", "bullet": r"^\* (?P<item>.+)$",
                            "heading": r"^== (?P<heading>.+) ==$"}},
    "sop.dots": {"parser": "list_doc", "full_cover": False,
                 "lines": {"step": r"^(?P<i>\d+)\) (?P<item>.+)$", "bullet": "^• (?P<item>.+)$"}},
    "sop.nested": {"parser": "list_doc", "full_cover": False,
                   "lines": {"step": r"^(?:  )?(?P<i>\d+)\. (?P<item>.+)$", "bullet": r"^(?:  )?- (?P<item>.+)$"}},
    "sop.parens": {"parser": "list_doc", "full_cover": False,
                   "lines": {"step": r"^\((?P<i>\d+)\) (?P<item>.+)$", "bullet": r"^\+ (?P<item>.+)$",
                             "heading": r"^\[(?P<heading>.+)\]$"}},
    "log.iso": {"parser": "lines", "full_cover": True, "variant_by": "card states whether actor and level appear",
                "lines": {"actor_level": "^" + G_TS_ISO + r" (?P<level>\S+) (?P<actor>[^:<>|\t\[\]()]+): (?P<text>.+)$",
                          "actor": "^" + G_TS_ISO + r" (?P<actor>[^:<>|\t\[\]()]+): (?P<text>.+)$",
                          "level": "^" + G_TS_ISO + r" (?P<level>\S+) (?P<text>.+)$",
                          "plain": "^" + G_TS_ISO + r" (?P<text>.+)$"}},
    "log.bracket": {"parser": "lines", "full_cover": True,
                    "lines": {"event": r"^\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\](?: \[(?P<level>[^\]\s]+)\])?"
                                       r"(?: <(?P<actor>[^<>]+)>)? (?P<text>.+)$"}},
    "log.logfmt": {"parser": "lines", "full_cover": True,
                   "lines": {"event": r'^time=(?P<ts>\S+)(?: level=(?P<level>\S+))?'
                                      r'(?: actor=(?P<actor>"(?:[^"\\]|\\.)*"|\S+))?'
                                      r' msg=(?P<text>"(?:[^"\\]|\\.)*"|\S+)$'}},
    "log.pipe": {"parser": "lines", "full_cover": True, "variant_by": "card states whether actor and level appear",
                 "lines": {"event": r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2})(?: \| (?P<f2>[^|]+?))?"
                                    r"(?: \| (?P<f3>[^|]+?))? \| (?P<text>[^|]+)$"}},
    "log.dayfirst": {"parser": "lines", "full_cover": True,
                     "variant_by": "card states whether actor and level appear",
                     "lines": {"actor_level": r"^(?P<ts>\d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2}) "
                                              r"(?P<actor>[^:<>|\t\[\]()]+): \((?P<level>\S+)\) (?P<text>.+)$",
                               "actor": r"^(?P<ts>\d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2}) "
                                        r"(?P<actor>[^:<>|\t\[\]()]+): (?P<text>.+)$",
                               "level": r"^(?P<ts>\d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2}) \((?P<level>\S+)\) "
                                        r"(?P<text>.+)$",
                               "plain": r"^(?P<ts>\d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2}) (?P<text>.+)$"}},
    "log.tabbed": {"parser": "lines", "full_cover": True, "variant_by": "card states whether actor and level appear",
                   "lines": {"event": r"^(?P<ts>\d{8} \d{6})(?:\t(?P<f2>[^\t]+))?(?:\t(?P<f3>[^\t]+))?\t(?P<text>[^\t]+)$"}},
    "diff.unified_path": {"parser": "lines", "full_cover": True,
                          "lines": {"old_file": r"^--- a/(?P<path>.+)$", "new_file": r"^\+\+\+ b/(?P<path>.+)$",
                                    "hunk": r"^@@ -1,(?P<n_old>\d+) \+1,(?P<n_new>\d+) @@$",
                                    "line": r"^(?P<op>[ +-])(?P<key>[^:]+): (?P<value>.+)$"}},
    "diff.unified_labels": {"parser": "lines", "full_cover": True,
                            "lines": {"old_file": r"^--- old$", "new_file": r"^\+\+\+ new$",
                                      "line": r"^(?P<op>[ +-])(?P<key>[^:]+): (?P<value>.+)$"}},
    "diff.word": {"parser": "lines", "full_cover": True,
                  "lines": {"changed": r"^(?P<key>[^:\[{]+): \[-(?P<old>.+?)-\]\{\+(?P<new>.+?)\+\}$",
                            "added": r"^\{\+(?P<key>[^:]+): (?P<new>.+)\+\}$",
                            "removed": r"^\[-(?P<key>[^:]+): (?P<old>.+)-\]$",
                            "kept": r"^(?P<key>[^:\[{]+): (?P<value>[^\[{].*)$"}},
    "diff.table": {"parser": "aligned_table", "full_cover": True,
                   "lines": {"rule": r"^=+(?:  =+)*$", "row": r"^\S.*$"}},
    "diff.changelog": {"parser": "lines", "full_cover": True,
                       "lines": {"changed": r"^Changed (?P<key>.+?) from (?P<old>.+) to (?P<new>.+?)\.?$",
                                 "added": r"^Added (?P<key>[^:]+): (?P<new>.+?)\.?$",
                                 "removed": r"^Removed (?P<key>.+?) \(was (?P<old>.+)\)\.$",
                                 "kept": r"^Kept (?P<key>[^:]+): (?P<value>.+?)\.?$"}},
    "diff.normal": {"parser": "lines", "full_cover": True,
                    "lines": {"kept": r"^  (?P<key>[^:]+): (?P<value>.+)$", "old": r"^< (?P<key>[^:]+): (?P<value>.+)$",
                              "new": r"^> (?P<key>[^:]+): (?P<value>.+)$"}},
    "form.colon": {"parser": "form", "full_cover": False,
                   "lines": {"field": r"^(?P<label>[^:]+): (?P<value>.+)$", "blank": r"^(?P<label>[^:]+):$",
                             "heading_rule": r"^=+$"}},
    "form.brackets": {"parser": "form", "full_cover": False,
                      "lines": {"field": r"^(?P<label>[^:]+): \[ (?P<value>.+) \]$",
                                "blank": r"^(?P<label>[^:]+): \[ \]$"}},
    "form.numbered": {"parser": "form", "full_cover": False,
                      "lines": {"field": r"^(?P<n>\d+)\. (?P<label>[^:]+): (?P<value>.+)$",
                                "blank": r"^(?P<n>\d+)\. (?P<label>[^:]+):$", "heading": r"^(?P<heading>.+):$"}},
    "form.checkbox": {"parser": "form", "full_cover": False,
                      "lines": {"choice": r"^(?P<label>[^:]+): (?P<boxes>\[[x ]\] .+?(?:  \[[x ]\] .+?)*)$",
                                "field": r"^(?P<label>[^:]+): (?P<value>.+)$", "blank": r"^(?P<label>[^:]+):$"}},
    "form.leaders": {"parser": "form", "full_cover": False,
                     "lines": {"field": r"^(?P<label>.+?) \.{3,} (?P<value>.+)$", "blank": r"^(?P<label>.+?) \.{3,}$",
                               "heading_rule": r"^=+$"}},
    "form.caps_labels": {"parser": "form", "full_cover": False,
                         "lines": {"choice": r"^(?P<label>[^a-z:]+): (?P<boxes>\[[x ]\] .+?(?:  \[[x ]\] .+?)*)$",
                                   "field": r"^(?P<label>[^a-z:]+): (?P<value>.+)$",
                                   "heading": r"^\[(?P<heading>.+)\]$"}},
}


# Default JSON/YAML/CSV/HTML vocabulary for keys the renderer must name itself (never record/log words, F8 lint).
VOCAB = {
    "v1": {"title": "title", "notes": "notes", "items": "items", "steps": "steps", "rows": "rows",
           "details": "details", "events": "events", "messages": "messages", "time": "time", "actor": "actor",
           "level": "level", "text": "text", "from": "from", "to": "to", "subject": "subject",
           "field": "field", "value": "value"},
    "v2": {"title": "name", "notes": "summary", "items": "points", "steps": "procedure", "rows": "entries",
           "details": "attributes", "events": "timeline", "messages": "thread", "time": "at", "actor": "by",
           "level": "severity_level", "text": "message", "from": "sender", "to": "recipient", "subject": "topic",
           "field": "attribute", "value": "setting"},
}

# ----------------------------------------------------------------------------------------------------------------------
# Card styles (layout of the card field). Two are held-out-only (never in a training style).
CARD_STYLES = [
    {"id": "CS01", "name": "plain_colon", "held_out_only": False, "title": "{title}", "heading": "{heading}:",
     "underline": "", "item": "- ", "step": "{i}. ", "table": "aligned", "wrapper": "none", "blank_between": True,
     "def_fmt": "{name}: {text}", "def_layout": "line"},
    {"id": "CS02", "name": "markdown", "held_out_only": False, "title": "## {title}", "heading": "### {heading}",
     "underline": "", "item": "- ", "step": "{i}. ", "table": "md", "wrapper": "none", "blank_between": True,
     "def_fmt": "**{name}**: {text}", "def_layout": "line"},
    {"id": "CS03", "name": "caps_headings", "held_out_only": False, "title": "{TITLE}", "heading": "{HEADING}",
     "underline": "", "item": "* ", "step": "{i}) ", "table": "aligned", "wrapper": "none", "blank_between": True,
     "def_fmt": "{name}: {text}", "def_layout": "line"},
    {"id": "CS04", "name": "numbered_sections", "held_out_only": False, "title": "{title}", "heading": "{n}. {heading}",
     "underline": "", "item": "- ", "step": "{n}.{i} ", "table": "pipe", "wrapper": "none", "blank_between": True,
     "def_fmt": "{name} = {text}", "def_layout": "line"},
    {"id": "CS05", "name": "bracket_labels", "held_out_only": False, "title": "[{title}]", "heading": "[{heading}]",
     "underline": "", "item": "• ", "step": "Step {i}: ", "table": "pipe", "wrapper": "none",
     "blank_between": True, "def_fmt": "{name} :: {text}", "def_layout": "line"},
    {"id": "CS06", "name": "underlined", "held_out_only": False, "title": "{title}", "heading": "{heading}",
     "underline": "=", "item": "- ", "step": "{i}. ", "table": "aligned", "wrapper": "none", "blank_between": True,
     "def_fmt": "{name}", "def_layout": "next_line"},
    {"id": "CS07", "name": "compact", "held_out_only": False, "title": "{title}", "heading": "{heading}:",
     "underline": "", "item": "* ", "step": "{i}) ", "table": "pipe", "wrapper": "none", "blank_between": False,
     "def_fmt": "{name}: {text}", "def_layout": "line"},
    {"id": "CS08", "name": "xml_tags", "held_out_only": False, "title": "{title}", "heading": "<{tag}>",
     "underline": "", "item": "- ", "step": "{i}. ", "table": "md", "wrapper": "xml", "blank_between": True,
     "def_fmt": "{name}: {text}", "def_layout": "line"},
    {"id": "CS09", "name": "blockquote", "held_out_only": False, "title": "**{title}**", "heading": "**{heading}**",
     "underline": "", "item": "- ", "step": "{i}. ", "table": "md", "wrapper": "quote", "blank_between": True,
     "def_fmt": "{name}: {text}", "def_layout": "line"},
    {"id": "CS10", "name": "hash_plain", "held_out_only": False, "title": "{title}", "heading": "# {heading}",
     "underline": "", "item": "+ ", "step": "{i}. ", "table": "pipe", "wrapper": "none", "blank_between": True,
     "def_fmt": "{name} | {text}", "def_layout": "line"},
    {"id": "CS11", "name": "rst", "held_out_only": True, "title": "{title}", "heading": "{heading}",
     "underline": "^", "item": "* ", "step": "{i}. ", "table": "grid", "wrapper": "none", "blank_between": True,
     "def_fmt": "{name}", "def_layout": "next_line"},
    {"id": "CS12", "name": "indent_outline", "held_out_only": True, "title": "{title}", "heading": "{heading}",
     "underline": "", "item": "· ", "step": "{i}. ", "table": "aligned", "wrapper": "indent",
     "blank_between": True, "def_fmt": "{name} → {text}", "def_layout": "line"},
]

# v1.1 (review formats-1): what a choice row shows. decoder_io (cygnet, schema_branch_mark; 908c08d7) prints the whole
# card on yes/no rows only. On a choice row it prints no card text except lines "- {option text}: {definition}", which
# it appends to the matching option line. fmt1.card.render_row_text(qtype="choice") writes option definitions as such
# lines (card.render_choice_defs, the same for every card style) and lays every other card block out in this card style
# inside instructions, in the instruction position's order. card.loader_check proves it on every row.
CS_ON_CHOICE_ROWS = ("option definitions -> '- {option}: {definition}' card lines (render_choice_defs, style-free); "
                     "every other block -> instructions, laid out in this card style")
DV_CHOICE_ROUTE = {"one_line": "option_lines", "one_line_examples": "option_lines", "rubric_table": "instructions",
                   "decision_list": "instructions", "short": "instructions", "none": "none"}
DV_CHOICE_NOTE = {
    "option_lines": "entries named by an exact option text -> '- {option}: {definition}' lines with examples inline "
                    "' (e.g. ex1; ex2)'; other entries (terms) -> instructions in this variant's layout",
    "instructions": "the whole block -> instructions in this variant's layout (order and columns kept; option lines "
                    "would lose rule order under the option shuffle)",
    "none": "no defs block",
}

# ----------------------------------------------------------------------------------------------------------------------
# Definition styles: canonical names used in meta.defs_style; variants are render forms chosen per card.
DEFS_STYLES = [
    {"id": "DS-one_line", "kind": "defs_style", "name": "one_line",
     "spec": "Each label or term gets one line: its name and its definition."},
    {"id": "DS-one_line_examples", "kind": "defs_style", "name": "one_line_examples",
     "spec": "One line per label, plus 1-2 examples on some labels (spec 2.1: on about 50% of cards)."},
    {"id": "DS-rubric_table", "kind": "defs_style", "name": "rubric_table",
     "spec": "A table: one row per label or level, columns set by the family (name, definition, criteria)."},
    {"id": "DS-decision_list", "kind": "defs_style", "name": "decision_list",
     "spec": "Numbered or named rules. Order semantics (first match or every rule) are stated by the family card."},
    {"id": "DS-short", "kind": "defs_style", "name": "short",
     "spec": "Names only, or the family's core lines only (spec 2.1: short or no card on about 15% of rows)."},
    {"id": "DS-none", "kind": "defs_style", "name": "none", "spec": "The card has no definitions block."},
]
DEFS_VARIANTS = [
    # one_line
    {"id": "DV01", "style": "one_line", "layout": "line", "fmt": "{name}: {text}", "marker": False},
    {"id": "DV02", "style": "one_line", "layout": "line", "fmt": "{name} = {text}", "marker": False},
    {"id": "DV03", "style": "one_line", "layout": "line", "fmt": "{name}: {text}", "marker": True},
    {"id": "DV04", "style": "one_line", "layout": "next_line", "fmt": "{name}", "indent": "    ", "marker": False},
    {"id": "DV05", "style": "one_line", "layout": "line", "fmt": "{name} | {text}", "marker": False},
    {"id": "DV06", "style": "one_line", "layout": "card", "marker": False},
    # one_line_examples
    {"id": "DV11", "style": "one_line_examples", "layout": "card", "marker": False,
     "ex_fmt": "  Example: {ex}", "ex_mode": "lines"},
    {"id": "DV12", "style": "one_line_examples", "layout": "line", "fmt": "{name}: {text}", "marker": False,
     "ex_fmt": " (e.g. {ex})", "ex_mode": "inline", "ex_join": "; "},
    {"id": "DV13", "style": "one_line_examples", "layout": "next_line", "fmt": "{name}", "indent": "    ",
     "marker": False, "ex_fmt": "    For example: {ex}", "ex_mode": "lines"},
    {"id": "DV14", "style": "one_line_examples", "layout": "line", "fmt": "{name} = {text}", "marker": False,
     "ex_fmt": "  Sample: {ex}", "ex_mode": "lines"},
    {"id": "DV15", "style": "one_line_examples", "layout": "card", "marker": True,
     "ex_fmt": "    Example {i}: {ex}", "ex_mode": "lines"},
    {"id": "DV16", "style": "one_line_examples", "layout": "line", "fmt": "{name}: {text}", "marker": True,
     "ex_fmt": "    Illustration: {ex}", "ex_mode": "lines"},
    # rubric_table (columns come from the family; table form from the card style unless forced)
    {"id": "DV21", "style": "rubric_table", "table": "card"},
    {"id": "DV22", "style": "rubric_table", "table": "md"},
    {"id": "DV23", "style": "rubric_table", "table": "aligned"},
    {"id": "DV24", "style": "rubric_table", "table": "blocks", "cell_fmt": "  {col}: {cell}"},
    {"id": "DV25", "style": "rubric_table", "table": "card", "ex_fmt": "{name}: {ex}", "ex_mode": "after_table"},
    # decision_list
    {"id": "DV31", "style": "decision_list", "num_fmt": "{i}. {text}"},
    {"id": "DV32", "style": "decision_list", "num_fmt": "Rule {i}: {text}"},
    {"id": "DV33", "style": "decision_list", "num_fmt": "({i}) {text}"},
    {"id": "DV34", "style": "decision_list", "num_fmt": "R{i}. {text}"},
    {"id": "DV35", "style": "decision_list", "num_fmt": "{name}: {text}", "named": True},
    # short
    {"id": "DV41", "style": "short", "form": "list"},
    {"id": "DV42", "style": "short", "form": "inline", "sep": "; "},
    {"id": "DV43", "style": "short", "form": "inline", "sep": " / "},
    {"id": "DV44", "style": "short", "form": "inline", "sep": ", "},
    # none
    {"id": "DV50", "style": "none"},
]

# ----------------------------------------------------------------------------------------------------------------------
# Few-shot card templates (spec 2.1: 1-3 worked examples on 5-10% of cards). Answers are option TEXT (label name, code,
# level text or Yes/No), never an option letter: the trainer re-shuffles letters (recipe "Option shuffling").
FEWSHOT = [
    {"id": "FT01", "header": "Worked examples", "item": "Example {i}\n{case}\nAnswer: {answer}", "case": "block"},
    {"id": "FT02", "header": "Solved cases", "item": "Case {i}:\n{case}\nCorrect choice: {answer}", "case": "block"},
    {"id": "FT03", "header": None, "item": "Q: {case}\nA: {answer}", "case": "block"},
    {"id": "FT04", "header": "Examples", "item": "| {case} | {answer} |", "case": "inline",
     "table_head": "| Case | Answer |\n| --- | --- |"},
    {"id": "FT05", "header": "Sample input and output", "item": "Input:\n{case}\nOutput: {answer}", "case": "block"},
    {"id": "FT06", "header": "Reference decisions", "item": "{i}) {answer}\n{case}", "case": "block"},
    {"id": "FT07", "header": None, "item": "For the case below, the answer is {answer}.\n{case}", "case": "block"},
    {"id": "FT08", "header": None, "item": "<example>\n<case>\n{case}\n</case>\n<answer>{answer}</answer>\n</example>",
     "case": "block"},
    {"id": "FT09", "header": "Examples", "item": "{i}. {case} => {answer}", "case": "inline"},
    {"id": "FT10", "header": "Worked example", "item": "Example {i}\n{case}\nDecision: {answer}\nWhy: {note}",
     "case": "block", "needs_note": True},
    {"id": "FT11", "header": "Past cases and their outcomes", "item": "Past case {i}\n{case}\nOutcome: {answer}",
     "case": "block"},
    {"id": "FT12", "header": "Practice items with answers", "item": "Item {i}.\n{case}\nAnswer key: {answer}",
     "case": "block"},
    {"id": "FT13", "header": "Examples", "item": "Example {i} ({answer})\n{case}", "case": "block"},
    {"id": "FT14", "header": None, "item": "Here is a case.\n{case}\nIts answer: {answer}", "case": "block"},
    {"id": "FT15", "header": "Illustrations", "item": "{case}\n=> {answer}", "case": "block"},
    {"id": "FT16", "header": "Calibration examples", "item": "Example {i}: \"{case}\" gives {answer}.",
     "case": "inline"},
    {"id": "FT17", "header": "Examples", "item": "{json}", "case": "inline", "json_keys": ["case", "answer"]},
    {"id": "FT18", "header": "Examples with reasons", "item": "{i}. {case}\n   Answer: {answer}\n   Reason: {note}",
     "case": "block", "needs_note": True},
]

# ----------------------------------------------------------------------------------------------------------------------
# Inverted cards (spec 2.1: 10-15% of cards; "which of these cases meets rule X?").
INV_CARD_FRAMES = [
    {"id": "IVC01", "text": "Each option describes a case. The question names a rule; choose the case that meets it.",
     "cases_in": "options", "asserts_exactly_one": False, "presumes_a_match": True},
    {"id": "IVC02", "text": "The options are cases, written out in full. Exactly one of them meets the rule named in "
                            "the question.",
     "cases_in": "options", "asserts_exactly_one": True, "presumes_a_match": True},
    {"id": "IVC03", "text": "Each option is a short case description. Pick the one that the named label fits.",
     "cases_in": "options", "asserts_exactly_one": False, "presumes_a_match": True},
    {"id": "IVC04", "text": "The text lists several cases by reference. The options give those references; choose "
                            "the case that meets the stated rule.",
     "cases_in": "text", "asserts_exactly_one": False, "presumes_a_match": True},
    {"id": "IVC05", "text": "Read each case against the rule in the question. One case meets it.",
     "cases_in": "any", "asserts_exactly_one": True, "presumes_a_match": True},
    {"id": "IVC06", "text": "This card works backwards: the outcome is given, and you choose the case that leads to "
                            "it.",
     "cases_in": "any", "asserts_exactly_one": False, "presumes_a_match": True},
    {"id": "IVC07", "text": "The question gives a label. Choose the case that the definitions assign to that label.",
     "cases_in": "any", "asserts_exactly_one": False, "presumes_a_match": True},
    {"id": "IVC08", "text": "Cases appear in the options. Compare each one with the rule; the answer is the case the "
                            "rule covers.",
     "cases_in": "options", "asserts_exactly_one": False, "presumes_a_match": True},
    {"id": "IVC09", "text": "Each option is a case. Choose the case that meets the rule named in the question, if any "
                            "option does.",
     "cases_in": "options", "asserts_exactly_one": False, "presumes_a_match": False},
    {"id": "IVC10", "text": "The options list cases. At most one of them meets the named rule.",
     "cases_in": "options", "asserts_exactly_one": False, "presumes_a_match": False},
]
# v1.1: inverted rows are always choice rows, so the frame sentence and the rule it names never stay in the card field
# (decoder_io hides card text on choice rows); render_row_text(qtype="choice") moves them to instructions (LR15).
INV_ON_CHOICE_ROWS = "instructions (card.render_row_text qtype='choice'); every inverted row passes card.loader_check"
INV_CASE_REFS = [
    {"id": "IVN01", "fmt": "Case {id}"}, {"id": "IVN02", "fmt": "Scenario {id}"}, {"id": "IVN03", "fmt": "Item {id}"},
    {"id": "IVN04", "fmt": "Entry {id}"}, {"id": "IVN05", "fmt": "Situation {id}"}, {"id": "IVN06", "fmt": "Profile {id}"},
    {"id": "IVN07", "fmt": "Matter {id}"}, {"id": "IVN08", "fmt": "Request {id}"},
]
INV_QUESTIONS = [
    ("IVQ01", "Which case meets {target}?", "rule"),
    ("IVQ02", "Which of these cases does {target} apply to?", "rule"),
    ("IVQ03", "Which case would {target} cover?", "rule"),
    ("IVQ04", "Which scenario satisfies {target}?", "rule"),
    ("IVQ05", "Which case gets {target} under the card?", "label"),
    ("IVQ06", "Pick the case that qualifies under {target}.", "rule"),
    ("IVQ07", "Which option describes a case that meets {target}?", "rule"),
    ("IVQ08", "For which case does {target} hold?", "rule"),
    ("IVQ09", "Which case is an instance of {target}?", "label"),
    ("IVQ10", "Select the case to which {target} applies.", "rule"),
    ("IVQ11", "Which of the listed cases falls under {target}?", "any"),
    ("IVQ12", "Which case should be assigned {target}?", "label"),
    ("IVQ13", "Identify the case that meets {target}.", "rule"),
    ("IVQ14", "Which case matches {target}?", "any"),
    ("IVQ15", "Under the card's definitions, which case counts as {target}?", "label"),
    ("IVQ16", "Which of these would count as {target}?", "label"),
    ("IVQ17", "Choose the case that {target} picks out.", "rule"),
    ("IVQ18", "Of the cases shown, which one does {target} describe?", "label"),
    ("IVQ19", "Which case lands in {target}?", "label"),
    ("IVQ20", "Which case is covered by {target}?", "rule"),
    ("IVQ21", "{target}: which case meets it?", "rule"),
    ("IVQ22", "Find the case that fits {target}.", "any"),
    ("IVQ23", "Which case would be classed under {target}?", "label"),
    ("IVQ24", "Which one of the cases satisfies {target}?", "rule"),
]

# ----------------------------------------------------------------------------------------------------------------------
# Masked label IDs. {L} letters without I and O; {D} digits 2-9 (no 0/1 look-alikes). Every scheme carries a digit,
# so an ID is never a bare option letter and never an English word.
MASK_SCHEMES = [
    ("MS01", "Category {L}{D}"), ("MS02", "Code {L}{L}-{D}{D}"), ("MS03", "Class {D}{L}"), ("MS04", "Type {L}{D}{D}"),
    ("MS05", "Group {L}{D}"), ("MS06", "Label {D}{D}{D}"), ("MS07", "Bin {L}{D}"), ("MS08", "Tag {L}{L}{D}"),
    ("MS09", "Code {D}{D}"), ("MS10", "{L}{D}"), ("MS11", "{L}{L}{D}"), ("MS12", "Class {L}{D}{L}"),
    ("MS13", "Set {D}{L}{D}"), ("MS14", "Code {L}{D}{D}{D}"), ("MS15", "Category #{D}{D}"), ("MS16", "Series {L}{D}"),
    ("MS17", "Cluster {L}{D}{D}"), ("MS18", "{L}{D}{D}{L}"), ("MS19", "Bucket {D}{L}"), ("MS20", "Token {L}{D}{D}"),
]
MASK_LETTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ"
MASK_DIGITS = "23456789"

# Familiar words for swapped label names. ordered groups carry a rough rank (1 = low end) for the monotone check.
SWAP_GROUPS = {
    "severity": (True, [("trivial", 1), ("minor", 2), ("mild", 2), ("moderate", 3), ("notable", 3), ("serious", 4),
                        ("major", 4), ("severe", 5), ("critical", 6), ("grave", 6)]),
    "priority": (True, [("low", 1), ("routine", 1), ("normal", 2), ("standard", 2), ("elevated", 3), ("high", 4),
                        ("express", 4), ("rush", 5), ("urgent", 5), ("immediate", 6)]),
    "quality": (True, [("poor", 1), ("weak", 1), ("fair", 2), ("adequate", 2), ("sound", 3), ("good", 3),
                       ("strong", 4), ("excellent", 5), ("superior", 5), ("prime", 5)]),
    "size": (True, [("tiny", 1), ("small", 2), ("compact", 2), ("medium", 3), ("regular", 3), ("large", 4),
                    ("bulky", 4), ("huge", 5), ("massive", 5), ("jumbo", 5)]),
    "speed": (True, [("sluggish", 1), ("slow", 1), ("leisurely", 1), ("steady", 2), ("brisk", 3), ("prompt", 3),
                     ("quick", 4), ("fast", 4), ("rapid", 5), ("swift", 5)]),
    "risk": (True, [("safe", 1), ("secure", 1), ("stable", 2), ("guarded", 3), ("exposed", 4), ("fragile", 4),
                    ("risky", 5), ("precarious", 5), ("volatile", 6), ("hazardous", 6)]),
    "temperature": (True, [("frozen", 1), ("icy", 1), ("cold", 2), ("chilly", 2), ("cool", 3), ("tepid", 4),
                           ("lukewarm", 4), ("warm", 5), ("heated", 6), ("hot", 6)]),
    "mood": (True, [("hostile", 1), ("bitter", 1), ("sour", 1), ("gloomy", 2), ("mixed", 3), ("content", 4),
                    ("cheerful", 5), ("upbeat", 5), ("positive", 5), ("sunny", 5)]),
    "status": (False, [("approved", 0), ("accepted", 0), ("cleared", 0), ("verified", 0), ("dormant", 0),
                       ("flagged", 0), ("held", 0), ("released", 0), ("suspended", 0), ("archived", 0),
                       ("settled", 0), ("parked", 0)]),
    "colour": (False, [("red", 0), ("amber", 0), ("green", 0), ("blue", 0), ("grey", 0), ("white", 0), ("black", 0),
                       ("gold", 0), ("silver", 0), ("violet", 0), ("teal", 0), ("crimson", 0), ("ivory", 0),
                       ("olive", 0), ("navy", 0)]),
    "material": (False, [("stone", 0), ("timber", 0), ("copper", 0), ("glass", 0), ("paper", 0), ("cotton", 0),
                         ("steel", 0), ("clay", 0), ("linen", 0), ("marble", 0)]),
    "weather": (False, [("cloudy", 0), ("stormy", 0), ("calm", 0), ("windy", 0), ("foggy", 0), ("rainy", 0),
                        ("frosty", 0), ("humid", 0), ("breezy", 0), ("misty", 0)]),
    "animal": (False, [("falcon", 0), ("otter", 0), ("badger", 0), ("heron", 0), ("lynx", 0), ("beaver", 0),
                       ("sparrow", 0), ("walrus", 0), ("gecko", 0), ("bison", 0)]),
    "plant": (False, [("oak", 0), ("maple", 0), ("fern", 0), ("cedar", 0), ("willow", 0), ("birch", 0), ("ivy", 0),
                      ("moss", 0), ("juniper", 0), ("aspen", 0)]),
    "shape": (False, [("round", 0), ("square", 0), ("narrow", 0), ("wide", 0), ("flat", 0), ("steep", 0),
                      ("hollow", 0), ("solid", 0), ("curved", 0), ("straight", 0)]),
    "outcome": (False, [("pass", 0), ("win", 0), ("success", 0), ("refund", 0), ("credit", 0), ("bonus", 0),
                        ("reward", 0), ("penalty", 0), ("warning", 0), ("waiver", 0)]),
    "scope": (False, [("retail", 0), ("wholesale", 0), ("domestic", 0), ("export", 0), ("internal", 0),
                      ("external", 0), ("primary", 0), ("secondary", 0), ("central", 0), ("remote", 0)]),
}
# Groups whose everyday sense overlaps family semantics: a family may exclude them (hint, not a ban).
SWAP_GROUP_HINTS = {"outcome": "money and decision words: F2, F8, F12 may exclude",
                    "status": "workflow-state words: F1, F3, F6 may exclude",
                    "scope": "jurisdiction-like words: F1 may exclude"}

LABEL_NOTICES = [
    ("LN01", "Label names are only names; decide by the definitions."),
    ("LN02", "The names below are arbitrary. Use the definitions."),
    ("LN03", "Read the definitions; a label's name may mean something else in everyday use."),
    ("LN04", "Each label means exactly what its definition says, whatever its everyday sense."),
    ("LN05", "Treat each name as a code word for its definition."),
    ("LN06", "The definitions override the usual meaning of each word."),
    ("LN07", "Names are tags; the definitions decide."),
    ("LN08", "Use the definition of a label, even where its name suggests another meaning."),
]

LABEL_RULES = [
    ("LR01", "rate_masked", "Masked label names (neutral IDs) on 10-15% of choice rows per family (target 12%); "
                            "F10: 40% of F10 choice rows.", "spec 2.1, F10"),
    ("LR02", "rate_swapped", "Swapped label names (familiar word, different definition) on about 5% of choice rows "
                             "(4-6%); F10: 30% of F10 choice rows.", "spec 2.1, F10"),
    ("LR03", "label_independent_draw", "The label form (plain, masked, swapped) is drawn by fmt1.labels.label_form "
                                       "from a hash of (family, card_id, row key) and rates only. It never reads "
                                       "gold, options order or difficulty.", "G6, G7, G10"),
    ("LR04", "masked_scope", "A masked row shows no label name anywhere: card, state, instructions and options use "
                             "the IDs only. Definitions keep their full text. One scheme per card; IDs drawn by "
                             "seeded shuffle; for 3 or more IDs the IDs are never in ascending or descending order "
                             "of definition order. On choice rows the ID definitions are '- {ID}: {definition}' card "
                             "lines from card.render_choice_defs (the name is the exact option text) or sit in "
                             "instructions, and every masked choice row passes card.loader_check.",
     "spec 2.1, F11 A25, review formats-1"),
    ("LR05", "masked_form", "Every masked ID carries a digit; letters exclude I and O; digits exclude 0 and 1; "
                            "never a bare single letter (option letters); IDs in one card are distinct and, when "
                            "the scheme allows, differ in at least 2 positions.", "G15"),
    ("LR06", "ordinal_rows", "Ordinal rows (meta.option_level) keep the level number in every option. Masking "
                             "there replaces only the level's name; swapped names are never used on ordinal rows.",
     "spec 2.4 A1, F7"),
    ("LR07", "swapped_choice", "A swapped name differs from its own definition's natural name and from every other "
                               "name, term and code on the card; no two names in a card share a 4-letter prefix; "
                               "perm mode is a derangement of the card's natural names. On choice rows each swapped "
                               "word's definition is a '- {word}: {definition}' card line from card.render_choice_defs "
                               "(the exact option text) or sits in instructions, so the definition is shown with the "
                               "word, and every swapped choice row passes card.loader_check.",
     "spec 2.1, review formats-1"),
    ("LR08", "swapped_monotone", "On a card whose labels have an order (a scale), swapped words from an ordered "
                                 "group must not follow that order: for 4 or more labels |Spearman rho| < 0.5 between "
                                 "word rank and label order; for 3 labels the ranks are neither increasing nor "
                                 "decreasing.", "G7"),
    ("LR09", "swapped_lexicon", "Swap words carry 0 negation cues (negcount k_all 0), are never an XF06 marker or "
                                "family-local marker word, and never an F8 record-status word.", "XF02, XF06, F8"),
    ("LR10", "notices_balanced", "A label notice (data/label_notices.jsonl) is optional. A family that uses one puts "
                                 "it on plain, masked and swapped cards at the same rate (+/- 2 pp), so it is no "
                                 "cue.", "G7"),
    ("LR11", "one_map_per_row", "Within one row, card, state, instructions and options use one name map. "
                                "meta.option_level and the gold key the rendered option text.", "G15"),
    ("LR12", "row_level_render", "Masked and swapped renders are row-level card renders under the same card_id, "
                                 "tagged 'masked' / 'swapped' in meta.edge; their quotas are counted on rows.",
     "F11-R2-10"),
    ("LR13", "tested_feature", "The label form is a G6 (d) metadata feature and a G7 feature; gold letter is "
                               "uniform within each label form (G10).", "G6, G7, G10"),
    ("LR14", "loader_visible", "Every row passes card.loader_check: rendered by decoder_io.user_msg (cygnet, "
                               "schema_branch_mark, pinned sha256) under a random option order, every non-empty card "
                               "line, definition, example and rule sentence is in the prompt, and the gold letter maps "
                               "back to the gold option. On choice rows the card field holds only '- {option}: "
                               "{definition}' lines; everything else goes to instructions (render_row_text qtype="
                               "'choice'). Yes/no cards hold no '- Yes: ' or '- No: ' line (decoder_io would glue it to "
                               "the option).", "recipe v4 layout, decoder_io 908c08d7, review formats-1"),
    ("LR15", "inverted_choice_rows", "Inverted rows are choice rows: the frame sentence, the rule or label "
                                     "definitions the question names and any card case list go to instructions "
                                     "(render_row_text qtype='choice' moves them in the instruction position's "
                                     "order) or to '- {option}: {definition}' lines; every inverted row passes "
                                     "card.loader_check.", "spec 2.1, review formats-1"),
]


def _sha(obj: dict) -> str:
    body = {k: v for k, v in obj.items() if k != "sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _write(name: str, rows: list[dict]) -> None:
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), f"duplicate ids in {name}"
    with open(DATA / name, "w", encoding="utf-8") as f:
        for r in rows:
            r = dict(r)
            r["version"] = VERSION
            r["sha256"] = _sha(r)
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def _deck_draw(rng: random.Random, values: list, n: int) -> list:
    """Near-uniform draw: shuffled decks, refilled when empty."""
    out, deck = [], []
    while len(out) < n:
        if not deck:
            deck = list(values)
            rng.shuffle(deck)
        out.append(deck.pop())
    return out


OMISSION_ALLOWED = {
    # F10 ST5 reading: key left out only in key-value, JSON, YAML and prose; null only in JSON/YAML; tables: words.
    "json": ["null", "key_left_out", "not recorded", "unknown"],
    "yaml": ["null", "key_left_out", "not recorded", "unknown"],
    "key_value": ["key_left_out", "not recorded", "unknown"],
    "prose": ["key_left_out", "not recorded", "unknown"],
}
F4_CONTAINERS = {"prose", "memo", "bullet_sop", "markdown_table", "csv", "html_snippet", "json", "yaml"}
HO_FOUR = {"prose", "memo", "bullet_sop", "markdown_table", "csv", "html_snippet", "json", "yaml"}


def build_styles() -> list[dict]:
    skins_by_c = {}
    for s in SKINS:
        skins_by_c.setdefault(s["container"], []).append(s)
    cs_train = [c for c in CARD_STYLES if not c["held_out_only"]]
    cs_ho = [c for c in CARD_STYLES if c["held_out_only"]]
    regs = [r["name"] for r in REGISTERS]
    ips = [p["id"] for p in INSTR_POSITIONS]
    styles = []
    n = 0
    for ci, ct in enumerate(CONTAINERS):
        cname = ct["name"]
        rng = random.Random(SEED * 100 + ci)
        sk_train = [s for s in skins_by_c[cname] if not s["held_out_only"]]
        sk_ho = [s for s in skins_by_c[cname] if s["held_out_only"]]
        assert len(sk_ho) == 1
        fences = [f["id"] for f in FENCES] if ct["fenceable"] else ["FN-none"]
        omits = OMISSION_ALLOWED.get(cname, ["not recorded", "unknown"])
        # ---- 25 training styles: near-uniform (shuffled decks) over skin, card style, register, position, fence
        sk_d = _deck_draw(rng, [s["id"] for s in sk_train], 25)
        cs_d = _deck_draw(rng, [c["id"] for c in cs_train], 25)
        rg_d = _deck_draw(rng, regs, 25)
        ip_d = _deck_draw(rng, ips, 25)
        fn_d = _deck_draw(rng, fences, 25)
        combos = []
        seen = set()
        for i in range(25):
            key = (sk_d[i], cs_d[i], rg_d[i], ip_d[i], fn_d[i])
            j = 0
            while key in seen:  # rotate the card style until unique (rare)
                j += 1
                key = (sk_d[i], cs_d[(i + j) % 25], rg_d[i], ip_d[i], fn_d[i])
            seen.add(key)
            combos.append(key)
        om_d = _deck_draw(rng, omits, 25 + 4)
        # ---- held-out styles: every one has a never-trained element (held-out skin or held-out card style)
        n_ho = 4 if cname in HO_FOUR else 3
        ho = []
        plan = [("ho_skin", "train_cs"), ("ho_skin", "ho_cs"), ("train_skin", "ho_cs"), ("ho_skin", "train_cs")]
        for k in range(n_ho):
            sk_kind, cs_kind = plan[k]
            sk = sk_ho[0]["id"] if sk_kind == "ho_skin" else rng.choice(sk_train)["id"]
            cs = (rng.choice(cs_ho) if cs_kind == "ho_cs" else rng.choice(cs_train))["id"]
            rg = regs[(k + ci) % 4]
            ip = ips[(k * 2 + ci) % 5]
            fn = fences[(k + ci) % len(fences)]
            key = (sk, cs, rg, ip, fn)
            while key in seen:
                cs = rng.choice(cs_ho if cs_kind == "ho_cs" else cs_train)["id"]
                key = (sk, cs, rg, ip, fn)
            seen.add(key)
            ho.append(key)
        for idx, (key, held) in enumerate([(c, False) for c in combos] + [(c, True) for c in ho]):
            n += 1
            sk, cs, rg, ip, fn = key
            styles.append({"id": f"FS-{n:04d}", "kind": "format_style", "held_out": held, "container": cname,
                           "skin": sk, "card_style": cs, "register": rg, "instr_position": ip, "fence": fn,
                           "omission_marker": om_d[idx]})
    assert len(styles) == 400, len(styles)
    assert sum(s["held_out"] for s in styles) == 50
    return styles


def enrich_styles(styles: list[dict]) -> list[dict]:
    skin = {s["id"]: s for s in SKINS}
    ct = {c["name"]: c for c in CONTAINERS}
    cs = {c["id"]: c for c in CARD_STYLES}
    out = []
    for s in styles:
        sk = skin[s["skin"]]
        c = ct[s["container"]]
        card = cs[s["card_style"]]
        flags = {
            "attribution_frame": bool(c["attribution_frame"]),
            "speaker_prefix": bool(sk["flags"].get("speaker_prefix")),
            "labelled_lines": bool(sk["flags"].get("labelled_lines")),
            "adds_numbers": bool(sk["flags"].get("adds_numbers")),
            "carries_path": bool(sk["flags"].get("carries_path")),
            "rewrites_keys": bool(sk["flags"].get("rewrites_keys")),
            "typed_values": bool(c["typed"]),
            "tabular": bool(sk["flags"].get("tabular")),
            "markdown": bool(sk["flags"].get("markdown")) or card["id"] in ("CS02", "CS09"),
            "html": bool(sk["flags"].get("html")),
            "fenced": s["fence"] != "FN-none",
            "single_collection": bool(sk["flags"].get("single_collection")),
            "unicode_chrome": bool(sk["flags"].get("unicode_chrome")) or card["id"] in ("CS05", "CS12"),
            "card_xml_tags": card["wrapper"] == "xml",
            "card_numbered_headings": card["id"] == "CS04",
            "uses_never_trained_element": bool(sk["held_out_only"] or card["held_out_only"]),
        }
        compat = {
            # F4 section 4 container list (G0 F4: prose incl. memo and case-file prose, bullets, md/CSV/HTML tables,
            # JSON, YAML). Memo only without author header pairs (the family's meta), which the family checks.
            "F4": c["name"] in F4_CONTAINERS,
            # COMMIT A59: route and message-only rows take containers that carry no path and no stats.
            "COMMIT_route_or_message_only": c["name"] != "diff" and not flags["carries_path"],
        }
        assert not (s["held_out"] is False and flags["uses_never_trained_element"]), s
        out.append({**s, "accepts": c["accepts"], "flags": flags, "compat_hints": compat})
    return out


def main() -> None:
    DATA.mkdir(exist_ok=True)
    _write("registers.jsonl", [{**r, "kind": "register"} for r in REGISTERS])
    _write("instr_positions.jsonl", [{**p, "kind": "instr_position"} for p in INSTR_POSITIONS])
    _write("fences.jsonl", [{**f, "kind": "fence"} for f in FENCES])
    _write("containers.jsonl", [{**c, "kind": "container"} for c in CONTAINERS])
    assert set(GRAMMARS) == {s["id"] for s in SKINS}, set(GRAMMARS) ^ {s["id"] for s in SKINS}
    _write("skins.jsonl", [{**s, "kind": "skin", "vocab": VOCAB.get(s["params"].get("vocab", ""), None),
                            "grammar": GRAMMARS[s["id"]]} for s in SKINS])
    _write("card_styles.jsonl", [{**c, "kind": "card_style", "choice_visible": True,
                                  "on_choice_rows": CS_ON_CHOICE_ROWS} for c in CARD_STYLES])
    styles = enrich_styles(build_styles())
    _write("styles.jsonl", styles)
    _write("defs_styles.jsonl", [dict(d) for d in DEFS_STYLES] + [
        {**v, "kind": "defs_variant", "choice_visible": True, "choice_route": DV_CHOICE_ROUTE[v["style"]],
         "on_choice_rows": DV_CHOICE_NOTE[DV_CHOICE_ROUTE[v["style"]]]} for v in DEFS_VARIANTS])
    _write("fewshot_templates.jsonl", [{**t, "kind": "fewshot_template", "answer_is": "option text, never a letter"}
                                       for t in FEWSHOT])
    inv = ([{**f, "kind": "inverted_card_frame", "row_qtype": "choice", "on_choice_rows": INV_ON_CHOICE_ROWS}
            for f in INV_CARD_FRAMES]
           + [{**r, "kind": "inverted_case_ref", "id_source": "fmt1.labels.masked_ids (unordered IDs)"}
              for r in INV_CASE_REFS]
           + [{"id": i, "kind": "inverted_question", "text": t, "target_kind": k} for i, t, k in INV_QUESTIONS])
    _write("inverted.jsonl", inv)
    _write("label_masks.jsonl", [{"id": i, "kind": "mask_scheme", "pattern": p, "letters": MASK_LETTERS,
                                  "digits": MASK_DIGITS} for i, p in MASK_SCHEMES])
    words = []
    k = 0
    all_words = [w for _, lst in SWAP_GROUPS.values() for w, _ in lst]
    assert len(all_words) == len(set(all_words)), "duplicate swap word"
    for g, (ordered, lst) in SWAP_GROUPS.items():
        for w, rank in lst:
            k += 1
            words.append({"id": f"SW{k:03d}", "kind": "swap_word", "word": w, "group": g, "ordered": ordered,
                          "rank": rank if ordered else None, "group_hint": SWAP_GROUP_HINTS.get(g)})
    _write("swap_words.jsonl", words)
    _write("label_notices.jsonl", [{"id": i, "kind": "label_notice", "text": t} for i, t in LABEL_NOTICES])
    _write("label_rules.jsonl", [{"id": i, "kind": "label_rule", "name": n, "rule": t, "source": s}
                                 for i, n, t, s in LABEL_RULES])
    print("wrote", sorted(p.name for p in DATA.glob("*.jsonl")))


if __name__ == "__main__":
    main()
