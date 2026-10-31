"""What the Haiku wording-pool writers must produce (names only; no wording is written here).

pool_requirements() lists every user-turn FORM (slots, roles, doc) registered by T50, T51 and T53 and every LEXICON id a
turn refers to as `lex:<id>`. A pool must give >= 50 wordings per form from the start, none used > 2% of a family's rows
(K11), and each lexicon id needs several surface forms. The AUTHORITY roles are fixed by the form, not by the pool, so a
pool author cannot change which spans carry them (G10). Writers get the question forms and slots, never the literal-ban list.
"""
from .canon import sha_obj
from .wording import FORMS

T50_OPS = ["read_credentials", "delete", "overwrite", "discard", "push", "merge", "force_push", "reset_hard", "clean", "infra_apply",
           "infra_delete", "infra_scale", "infra_modify", "sql_insert", "sql_update", "sql_delete", "sql_drop", "sql_truncate", "sql_alter",
           "sql_grant", "run_remote_script", "run_image", "install", "tls_off", "perm_open", "open_firewall", "isolation_off", "skip_hook",
           "kill", "sudo", "upload", "publish", "send"]
T50_DOMAINS = ["fs", "git", "infra", "sql", "pkg_net", "process", "wtr", "opaque"]
T53_TOPICS = ["http_post_file", "credential_in_url", "git_push", "bucket_upload", "log_or_telemetry", "package_publish", "mcp_call", "egress"]
KINDS = ["branch", "job", "service", "bucket", "file"]


def lexicon_ids():
    ids = ["op." + o for o in T50_OPS] + ["topic." + d for d in T50_DOMAINS] + ["topic." + t for t in T53_TOPICS]
    ids += ["op.delete", "neg.keep", "neg.revoke", "neg.only", "when.stale"]
    ids += ["desc." + k for k in KINDS] + ["task." + k for k in KINDS] + ["task.implied." + k for k in KINDS]
    return sorted(set(ids))


def pool_requirements():
    # import for the side effect of registering the forms
    import T50.generator  # noqa: F401
    import T51.generator  # noqa: F401
    import T53.generator  # noqa: F401
    forms = {fid: {"family": m["family"], "slots": m["slots"], "doc": m["doc"]} for fid, m in sorted(FORMS.items())
             if m["family"] in ("T50", "T51", "T53")}
    spec = {"version": "v1", "min_wordings_per_form": 50, "max_share_per_wording": 0.02, "forms": forms, "lexicon_ids": lexicon_ids(),
            "hard_op_pattern": "op.<program>.<subcommand>: T50 hard quads name a free-form operation as <program>.<subcommand> "
                               "(e.g. rm.run, git.push); the pool needs a verb phrase for each program and subcommand on the closed T50 list",
            "slot_value_notes": {"lex:<id>": "the renderer replaces the slot value by one of the lexicon surfaces"}}
    spec["sha256"] = sha_obj(spec)
    return spec
