"""Identifier provenance (K15): every identifier in a rendered module must have been minted by Idents (namespace.py,
TRAINING salt). Language keywords/builtins used by the renderers are not identifiers of the module and are not listed.
"""
from . import ir as I


def module_identifiers(mod):
    names = set(mod["files"])
    for f in mod["funcs"]:
        names.add(f["name"])
        names.update(p[0] for p in f["params"])
        for _, n in I.walk(f["body"]):
            if n[0] in ("let", "popto", "shiftto", "for", "each") and isinstance(n[1], str):
                names.add(n[1])
    for c in mod["consts"]:
        names.add(c["name"])
    if mod["cls"]:
        names.add(mod["cls"]["name"])
        names.update(f["name"] for f in mod["cls"]["fields"])
    meta = mod.get("meta", {})
    names.add(meta.get("package", ""))
    names.update((meta.get("scaf") or {}).values())
    names.update(x for x in (meta.get("reset_name"), meta.get("has_name")) if x)
    for info in mod["errors"].values():
        names.add(info.get("go", ""))
        if info.get("python_custom"):
            names.add(info["python"])
        if info.get("js_custom"):
            names.add(info["javascript"])
    names.discard("")
    return names


def foreign_identifiers(mod, ids):
    """Identifiers of `mod` that `ids` did not mint (should be empty)."""
    minted = ids._used
    return sorted(n for n in module_identifiers(mod) if n.lower() not in minted)
