"""Shared path-skip rule for every C2.1 L-0 tool (plan v3.1, skeptic 30).

Every data/** glob or directory walk in the L-0 programs must skip
  - data/ohs3*   and  ohs3_parts/
  - any ohs* / *sealed* path.
The rule is deliberately broad: a path component that contains "ohs" or "sealed" (any case) is skipped.
This module never opens a file; it only looks at path strings and directory listings.
"""
import os
import re
import tempfile

__all__ = ["is_skipped_name", "is_skipped_rel", "is_skipped_path", "glob_to_regex", "safe_walk", "safe_glob"]


def is_skipped_name(name):
    n = name.lower()
    return "ohs" in n or "sealed" in n


def _temp_prefix_parts():
    out = []
    for t in {tempfile.gettempdir(), os.path.realpath(tempfile.gettempdir())}:
        out.append([c for c in os.path.abspath(t).split(os.sep) if c])
    return out


def _bars(path):
    parts = [c for c in path.split(os.sep) if c]
    for tp in _temp_prefix_parts():
        if tp and parts[:len(tp)] == tp:
            parts = parts[len(tp):]
            break
    return any(is_skipped_name(c) for c in parts)


def is_skipped_path(path):
    """True if ANY component of the whole absolute path, or of its symlink-resolved path, contains ohs/sealed
    (case-insensitive).

    The system temp directory prefix is ignored (its random folder names are not project paths), so a
    random temp name can never bar a path by accident. Used for files a tool is about to open (manifest,
    allow-list, registry), where the old 'last four components' check let a deeper sealed path through and a
    symlink named innocently could point into a sealed directory. realpath looks at link metadata only.
    """
    ab = os.path.abspath(path)
    if _bars(ab):
        return True
    try:
        return _bars(os.path.realpath(ab))
    except OSError:
        return False


def is_skipped_rel(parts, only_below_data=False):
    """parts: path components RELATIVE to the walk root.

    Default: any component that contains ohs/sealed is skipped.
    only_below_data=True (used for transcript discovery, where lane labels may legitimately appear in
    file names): ohs3*/ohs3_parts are skipped anywhere, other ohs*/sealed components only below a
    component named "data".
    """
    seen_data = False
    for p in parts:
        low = p.lower()
        if not only_below_data:
            if is_skipped_name(low):
                return True
        else:
            if low.startswith("ohs3") or low == "ohs3_parts":
                return True
            if seen_data and is_skipped_name(low):
                return True
        if low == "data":
            seen_data = True
    return False


def glob_to_regex(pattern):
    """'**' matches across '/', '*' and '?' do not; a trailing '/**' also matches the directory itself."""
    i, n, out = 0, len(pattern), []
    while i < n:
        c = pattern[i]
        if c == "*":
            if pattern[i:i + 2] == "**":
                if pattern[i - 1:i] == "/" or i == 0:
                    if pattern[i + 2:i + 3] == "/":
                        out.append("(?:.*/)?")
                        i += 3
                        continue
                    if i + 2 == n:
                        if out and out[-1] == "/":
                            out.pop()
                            out.append("(?:/.*)?")
                        else:
                            out.append(".*")
                        i += 2
                        continue
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(c))
        i += 1
    return re.compile("^" + "".join(out) + "$")


def safe_walk(root, only_below_data=False):
    """Yield absolute file paths under root, pruning skipped directories and files. Symlinks not followed."""
    root = os.path.abspath(root)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        rel = os.path.relpath(dirpath, root)
        base = [] if rel == "." else rel.split(os.sep)
        dirnames[:] = sorted(
            d for d in dirnames
            if not is_skipped_rel(base + [d], only_below_data) and not os.path.islink(os.path.join(dirpath, d))
        )
        for f in sorted(filenames):
            if is_skipped_rel(base + [f], only_below_data):
                continue
            full = os.path.join(dirpath, f)
            if os.path.islink(full):
                continue
            yield full


def safe_glob(root, pattern, only_below_data=False):
    """Glob 'pattern' (relative to root, '**' allowed) over files, with the skip rule applied."""
    root = os.path.abspath(root)
    rx = glob_to_regex(pattern.replace(os.sep, "/"))
    hits = []
    for full in safe_walk(root, only_below_data):
        rel = os.path.relpath(full, root).replace(os.sep, "/")
        if rx.match(rel):
            hits.append(full)
    return hits
