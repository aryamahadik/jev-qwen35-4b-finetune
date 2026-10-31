"""The G13 call boundary and the production guards shared by the GEN and VOICE check-at-creation pipelines (plan 16.1 steps 0, 2, 6).
Same shapes as tool_engine/row_pipeline.StampHook, so L-0b's single stamp service plugs into every lane. CODE ONLY: no file, no network, no model."""
import os


class RowGuardRequired(RuntimeError):
    """A production run was started outside the row-start guard (c21_infra/row_start_guard.py --exec) or with an allow-list that is not the pinned one."""


class StampServiceRequired(RuntimeError):
    """No G13 stamp hook was supplied: no row may enter a pool unstamped."""


class ConformanceRecordRequired(RuntimeError):
    """A production run needs the signed ruling-to-code conformance record for the current code sha (plan 16.1 step 0)."""


class TemplateHashStale(RuntimeError):
    """The live code / pool files no longer match HASH_EXPORT.json: a template change needs a NEW hash export and re-made rows (step 6)."""


GUARD_VARS = ("OD_ROWGUARD_FREEZE_SHA", "OD_ROWGUARD_REGISTRY_SHA", "OD_ROWGUARD_ALLOWLIST_SHA")


def guard_facts(allowlist_file_sha, environ=None):
    env = os.environ if environ is None else environ
    missing = [v for v in GUARD_VARS if not env.get(v)]
    if missing:
        raise RowGuardRequired("not started through the row-start guard: missing %s" % ", ".join(missing))
    if allowlist_file_sha is not None and env["OD_ROWGUARD_ALLOWLIST_SHA"] != allowlist_file_sha:
        raise RowGuardRequired("the allow-list in use is not the one the guard pinned")
    return {"freeze_sha": env["OD_ROWGUARD_FREEZE_SHA"], "registry_sha": env["OD_ROWGUARD_REGISTRY_SHA"], "allowlist_sha": env["OD_ROWGUARD_ALLOWLIST_SHA"]}


# ---- the G13 call boundary (same shape as tool_engine/row_pipeline.StampHook, so L-0b's one service plugs into every lane) ------------------
class StampHook(object):
    """stamp(items) -> {row_id: verdict}; items = [{"row_id", "family", "text", "generator_sha"}];
    verdict = {"verdict": "clean" | "hit" | "error", "hits": [{"target", "method", "exempt": None | "scaffolding_only" | "freeze_collision"}],
               "registry_sha", "method_set_version"}. Implementations must not return matched text."""
    registry_sha = None
    method_set_version = None

    def stamp(self, items):
        raise NotImplementedError


class RefusingHook(StampHook):
    def stamp(self, items):
        raise StampServiceRequired("the G13 stamp service is not wired; no row may enter a pool unstamped")


class TestDoubleHook(StampHook):
    """TEST DOUBLE ONLY: clean except the listed ids. It inspects nothing and is refused by a production run."""
    __test__ = False
    is_test_double = True

    def __init__(self, hit_ids=(), error_ids=(), exempt_ids=(), registry_sha="0" * 64):
        self.hit_ids, self.error_ids, self.exempt_ids = set(hit_ids), set(error_ids), set(exempt_ids)
        self.registry_sha = registry_sha
        self.method_set_version = "test-double"
        self.calls = 0

    def stamp(self, items):
        self.calls += 1
        out = {}
        for it in items:
            rid = it["row_id"]
            v = {"verdict": "clean", "hits": [], "registry_sha": self.registry_sha, "method_set_version": self.method_set_version}
            if rid in self.error_ids:
                v["verdict"] = "error"
            elif rid in self.hit_ids:
                v.update(verdict="hit", hits=[{"target": "target.test", "method": "method.test", "exempt": None}])
            elif rid in self.exempt_ids:
                v.update(verdict="hit", hits=[{"target": "target.scaffold", "method": "method.test", "exempt": "scaffolding_only"}])
            out[rid] = v
        return out
