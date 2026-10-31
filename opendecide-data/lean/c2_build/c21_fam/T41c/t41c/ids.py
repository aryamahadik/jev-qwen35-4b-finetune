"""T41c identifiers (G0-lite section 6) and the frozen-allow-list check.

Every id here is copied from T41c/G0_LITE.md section 6. The guard categories (policy, tool, language,
runner, carrier) must all be on l0/NAMES_MANIFEST_V1.json; `check_ids_on_manifest` refuses anything else.
Labels, source tags, task classes, goal/benign classes, wrapper styles, placement bins, visibility and
delegation modes are family vocabulary (recorded in the manifest, not guard categories).
"""
import hashlib
import json
import os

C2B = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_L0 = os.path.join(C2B, "zed_orch", "c21", "l0")
# v1.1 (frozen, v1 plus the v3.2 additions, nothing removed or renamed) is the allow-list a v3.2 row job is checked
# against; v1 stays importable for the conformance test that every T41c id is on both.
MANIFEST_V1_PATH = os.path.join(_L0, "NAMES_MANIFEST_V1.json")
MANIFEST_V1_SHA_PATH = os.path.join(_L0, "NAMES_MANIFEST_V1.sha256")
MANIFEST_PATH = os.path.join(_L0, "NAMES_MANIFEST_V1_1.json")
MANIFEST_SHA_PATH = os.path.join(_L0, "NAMES_MANIFEST_V1_1.sha256")

# ---- labels ---------------------------------------------------------------------------------------------
ALLOW, ALLOW_BENIGN, ASK, BLOCK = "ALLOW", "ALLOW_BENIGN", "ASK", "BLOCK"
LABELS = (ALLOW, ALLOW_BENIGN, ASK, BLOCK)
SEVERITY = {ALLOW: 0, ALLOW_BENIGN: 1, ASK: 2, BLOCK: 3}
LOW, SOFT, HARD = "LOW", "SOFT", "HARD"

POLICY_ID = "policy.taint_four_way"

# ---- source tags (8) and attributes -----------------------------------------------------------------------
SRC_USER = "src.user"
SRC_SYSTEM = "src.system_developer"
SRC_USER_FILE = "src.user_repo_file"
SRC_THIRD_FILE = "src.third_party_repo_file"
SRC_TOOL = "src.tool_result"
SRC_MCP_DESC = "src.mcp_description"
SRC_MCP_RESP = "src.mcp_response"
SRC_CI = "src.ci_log"
SOURCE_TAGS = (SRC_USER, SRC_SYSTEM, SRC_USER_FILE, SRC_THIRD_FILE, SRC_TOOL, SRC_MCP_DESC, SRC_MCP_RESP, SRC_CI)
ATTR_DECLARED_POLICY = "attr.declared_policy"
ATTR_NESTED = "attr.nested"

# ---- carrier types (12), formats (7) ------------------------------------------------------------------------
CARRIER_TYPES = ("car.readme", "car.contributing_guide", "car.issue_body", "car.review_comment", "car.code_comment",
                 "car.rules_file", "car.ci_log", "car.ci_config", "car.tool_json", "car.tool_text",
                 "car.mcp_description", "car.mcp_response")
FORMATS = ("fmt.markdown", "fmt.json", "fmt.yaml", "fmt.plain", "fmt.html", "fmt.log_lines", "fmt.toml")

# Rule (G0-lite section 6): each format used by >= 3 carrier types, each carrier type available in >= 2 formats,
# so holding out a format is not holding out a type. car.ci_config has a generic synthetic schema (closed keys).
CARRIER_FORMATS = {
    "car.readme": ("fmt.markdown", "fmt.plain", "fmt.html"),
    "car.contributing_guide": ("fmt.markdown", "fmt.plain", "fmt.html"),
    "car.issue_body": ("fmt.markdown", "fmt.plain", "fmt.json"),
    "car.review_comment": ("fmt.markdown", "fmt.plain", "fmt.json"),
    "car.code_comment": ("fmt.plain", "fmt.markdown"),
    "car.rules_file": ("fmt.markdown", "fmt.plain", "fmt.yaml", "fmt.toml"),
    "car.ci_log": ("fmt.log_lines", "fmt.plain", "fmt.json"),
    "car.ci_config": ("fmt.yaml", "fmt.toml", "fmt.json"),
    "car.tool_json": ("fmt.json", "fmt.yaml", "fmt.toml"),
    "car.tool_text": ("fmt.plain", "fmt.markdown", "fmt.log_lines"),
    "car.mcp_description": ("fmt.json", "fmt.yaml", "fmt.markdown", "fmt.plain"),
    "car.mcp_response": ("fmt.json", "fmt.plain", "fmt.markdown", "fmt.html", "fmt.log_lines"),
}

# source tag(s) a carrier type may carry (the carrier span's own tag)
CARRIER_SOURCES = {
    "car.readme": (SRC_USER_FILE, SRC_THIRD_FILE),
    "car.contributing_guide": (SRC_USER_FILE, SRC_THIRD_FILE),
    "car.issue_body": (SRC_TOOL, SRC_THIRD_FILE),
    "car.review_comment": (SRC_TOOL, SRC_THIRD_FILE),
    "car.code_comment": (SRC_USER_FILE, SRC_THIRD_FILE),
    "car.rules_file": (SRC_USER_FILE, SRC_THIRD_FILE),
    "car.ci_log": (SRC_CI,),
    "car.ci_config": (SRC_USER_FILE, SRC_THIRD_FILE),
    "car.tool_json": (SRC_TOOL,),
    "car.tool_text": (SRC_TOOL,),
    "car.mcp_description": (SRC_MCP_DESC,),
    "car.mcp_response": (SRC_MCP_RESP,),
}
# user-owned file types that can quote vendored third-party text (nested provenance)
NESTABLE_CARRIERS = ("car.readme", "car.contributing_guide", "car.code_comment", "car.rules_file", "car.ci_config")

# ---- languages (carrier content only, nothing executed) -----------------------------------------------------
LANGS = ("python", "javascript", "typescript", "go", "bash")   # manifest spelling (lang.<x> aliases in the G0-lite)

# ---- task classes (12), tool roles (10) ---------------------------------------------------------------------
TASK_CLASSES = ("task.fix_failing_test", "task.summarise_issue", "task.update_dependency", "task.review_change",
                "task.answer_from_docs", "task.triage_ci_failure", "task.write_docs", "task.refactor_function",
                "task.run_build", "task.onboarding_setup", "task.search_codebase", "task.use_mcp_tool")
TOOL_ROLES = ("tool.shell_run", "tool.file_read", "tool.file_write", "tool.file_delete", "tool.http_request",
              "tool.pkg_install", "tool.git_op", "tool.mcp_invoke", "tool.search_code", "tool.run_tests")

# ---- directive classes ------------------------------------------------------------------------------------------
GOAL_CLASSES = ("goal.exfiltrate", "goal.destroy", "goal.weaken_security", "goal.supply_chain_install",
                "goal.redirect_permission", "goal.persistence_hook", "goal.resource_exhaustion", "goal.scope_widening")
BENIGN_CLASSES = ("ben.install_declared_deps", "ben.run_declared_tests", "ben.run_declared_build", "ben.lint_task_files",
                  "ben.auth_declared_service", "ben.read_declared_docs", "ben.set_task_env_flag",
                  "ben.apply_local_migration", "ben.checkout_declared_branch")
# non-agent-directed content (rule 2): security write-up, fixture, quoted example, lint pragma, human-addressed note
MENTION_CLASSES = ("men.security_writeup", "men.fixture", "men.quoted_example", "men.lint_pragma", "men.human_note")

SUBTYPES = ("sub.delegated", "sub.ambient", "sub.trigger_security", "sub.human_offtopic", "sub.clean_twin", "sub.noise")
# attack-side metadata buckets (family-internal, metadata only)
ATTACK_BUCKETS = ("att.unrequested_high", "att.unrequested_low", "att.hard_delegated_or_necessary",
                  "ask.delegated_soft", "ask.necessary_soft", "ask.nested")

WRAPPERS = ("wrap.plain_imperative", "wrap.authority_framing", "wrap.urgency", "wrap.fake_system_tag", "wrap.role_play",
            "wrap.preauthorised_disguise", "wrap.conditional_trigger", "wrap.hidden")
HIDDEN_VARIANTS = ("hid.html_comment", "hid.alt_text", "hid.zero_width", "hid.base64", "hid.split_chunks")
PLACEMENTS = ("place.p0", "place.p1", "place.p2", "place.p3", "place.p4")
VISIBILITY = ("vis.user_visible", "vis.agent_only")
DELEG_MODES = ("deleg.none", "deleg.source_pointer", "deleg.step_pointer")

# facts-absent names (9.1)
FACTS_PRESENT, FACTS_ABSENT = "facts.present", "facts.absent"
FACT_FIELDS = ("fact.declared_hosts", "fact.declared_manifest", "fact.declared_workspace", "fact.declared_targets",
               "fact.declared_tools", "fact.repo_remotes", "fact.visible_manifest_file")

# namespace slot ids (G0-lite section 6)
NS_SLOTS = ("ns.org", "ns.repo", "ns.package", "ns.host", "ns.service", "ns.handle", "ns.path_stem", "ns.branch",
            "ns.envvar", "ns.ticket", "ns.project", "ns.endpoint", "ns.mcp_server", "ns.mcp_tool")

# per task class: the benign action classes that sit on its critical path ("necessary" step set; program table).
# Every ben.* class is necessary for >= 1 task class and every task class has >= 1 necessary step.
NECESSARY_STEPS = {
    "task.fix_failing_test": ("ben.run_declared_tests", "ben.install_declared_deps", "ben.set_task_env_flag",
                              "ben.apply_local_migration"),
    "task.summarise_issue": ("ben.read_declared_docs",),
    "task.update_dependency": ("ben.install_declared_deps", "ben.run_declared_tests", "ben.run_declared_build"),
    "task.review_change": ("ben.checkout_declared_branch", "ben.lint_task_files", "ben.run_declared_tests",
                           "ben.read_declared_docs"),
    "task.answer_from_docs": ("ben.read_declared_docs",),
    "task.triage_ci_failure": ("ben.run_declared_tests", "ben.run_declared_build", "ben.read_declared_docs",
                               "ben.checkout_declared_branch"),
    "task.write_docs": ("ben.read_declared_docs", "ben.lint_task_files"),
    "task.refactor_function": ("ben.run_declared_tests", "ben.lint_task_files"),
    "task.run_build": ("ben.install_declared_deps", "ben.run_declared_build", "ben.set_task_env_flag"),
    "task.onboarding_setup": ("ben.install_declared_deps", "ben.run_declared_tests", "ben.auth_declared_service",
                              "ben.apply_local_migration", "ben.set_task_env_flag", "ben.checkout_declared_branch",
                              "ben.run_declared_build"),
    "task.search_codebase": ("ben.read_declared_docs",),
    "task.use_mcp_tool": ("ben.auth_declared_service",),
}

# tool role per directive class (stable internal ids, never rendered)
CLASS_TOOL = {
    "ben.install_declared_deps": "tool.pkg_install", "ben.run_declared_tests": "tool.run_tests",
    "ben.run_declared_build": "tool.shell_run", "ben.lint_task_files": "tool.shell_run",
    "ben.auth_declared_service": "tool.http_request", "ben.read_declared_docs": "tool.file_read",
    "ben.set_task_env_flag": "tool.shell_run", "ben.apply_local_migration": "tool.shell_run",
    "ben.checkout_declared_branch": "tool.git_op",
}

GUARD_CATEGORIES = ("policy", "tool", "language", "runner", "carrier")


def job_names(carriers=CARRIER_TYPES, formats=FORMATS, tools=TOOL_ROLES, langs=LANGS):
    """The five guard categories this family declares (runners: none)."""
    return {"policy": [POLICY_ID], "tool": list(tools), "language": list(langs), "runner": [],
            "carrier": list(carriers) + list(formats)}


def load_manifest_names(path=MANIFEST_PATH, sha_path=MANIFEST_SHA_PATH, verify_sha=True):
    """Return {category: frozenset(names)} from the frozen names-only manifest. Verifies the file sha against
    the .sha256 record and the frozen flag; raises ValueError otherwise."""
    with open(path, "rb") as f:
        raw = f.read()
    if verify_sha:
        with open(sha_path, "r", encoding="utf-8") as f:
            want = f.read().split()[0].strip().lower()
        got = hashlib.sha256(raw).hexdigest()
        if got != want:
            raise ValueError("NAMES_MANIFEST sha mismatch: %s != %s" % (got[:12], want[:12]))
    obj = json.loads(raw.decode("utf-8"))
    if obj.get("frozen") is not True:
        raise ValueError("names manifest is not frozen")
    names = obj["names"]
    return {c: frozenset(names[c]) for c in GUARD_CATEGORIES}


def check_ids_on_manifest(job, allow=None):
    """job: {category: [ids]} (all five categories). Returns a list of violation strings (empty = ok)."""
    allow = allow or load_manifest_names()
    bad = []
    for cat in GUARD_CATEGORIES:
        if cat not in job:
            bad.append("NAMES_INCOMPLETE: category %r not declared" % cat)
            continue
        for nm in job[cat]:
            if nm not in allow[cat]:
                bad.append("NAME_OFF_ALLOWLIST: %s=%r" % (cat, nm))
    for cat in job:
        if cat not in GUARD_CATEGORIES:
            bad.append("UNKNOWN_CATEGORY: %r" % cat)
    return bad


def spec_guard_names(spec):
    """Guard-category ids a single row spec uses (policy, the tool roles of its directives, the carrier type and
    format, the code-comment language when present)."""
    tools = sorted({d.action.tool_role for d in spec.directives if d.action is not None})
    langs = [spec.code_lang] if getattr(spec, "code_lang", None) else []
    return {"policy": [POLICY_ID], "tool": tools, "language": langs, "runner": [],
            "carrier": [spec.carrier_type, spec.carrier_format]}
