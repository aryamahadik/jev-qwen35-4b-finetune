"""Identifier minting for generated modules. EVERY identifier (module stem, function, class, field, constant, local,
parameter, string constant, error marker) is drawn from namespace.py with the TRAINING salt. No hand-picked names.

Draws that collide with a reserved word, builtin or common library name of ANY of the five languages are redrawn
(the namespace's deny_check hook), so one identifier is legal in Python, JavaScript, TypeScript, Go and bash.
"""
import re

from . import paths  # noqa: F401
from namespace import NameSpace, NamespaceError  # noqa: E402

_PY = """False None True and as assert async await break class continue def del elif else except finally for from
global if import in is lambda nonlocal not or pass raise return try while with yield self cls print len int str bool
list dict set tuple range min max sum abs map filter zip any all sorted open input type object id hash iter next
format repr vars dir eval exec compile super property bytes float complex slice round pow divmod ord chr bin hex oct
enumerate reversed isinstance issubclass callable getattr setattr hasattr delattr globals locals exit quit help
copyright credits license""".split()
_JS = """break case catch class const continue debugger default delete do else enum export extends false finally for
function if import in instanceof new null return super switch this throw true try typeof var void while with yield
let static implements interface package private protected public await async of arguments eval undefined NaN Infinity
console process require module exports global window document name length constructor prototype toString valueOf
Object Array String Number Boolean Math JSON Date Map Set Symbol Promise Error assert test describe it parent top
self status event""".split()
_TS = """abstract any as asserts bigint boolean declare get infer is keyof module namespace never readonly number
object override satisfies set symbol type undefined unique unknown from global""".split()
_GO = """break default func interface select case defer go map struct chan else goto package switch const fallthrough
if range type continue for import return var append cap clear close complex copy delete imag len make max min new
panic print println real recover bool byte complex64 complex128 error float32 float64 int int8 int16 int32 int64
rune string uint uint8 uint16 uint32 uint64 uintptr true false iota nil main init fmt os strings strconv slices
testing reflect sort errors""".split()
_SH = """if then else elif fi case esac for select while until do done in function time coproc alias bg bind break
builtin caller cd command compgen complete compopt continue declare dirs disown echo enable eval exec exit export
false fc fg getopts hash help history jobs kill let local logout mapfile popd printf pushd pwd read readarray
readonly return set shift shopt source suspend test times trap true type typeset ulimit umask unalias unset wait
cat cut expr grep head printf seq sort tail tee tr uniq wc awk sed env ls rm cp mv ln mkdir touch chmod find ps df du
date id uname hostname ret RET IFS PATH HOME PWD OLDPWD SHELL USER UID EUID PPID RANDOM SECONDS LINENO BASH
FUNCNAME OPTARG OPTIND REPLY MAPFILE""".split()
RESERVED = frozenset(w.lower() for w in (_PY + _JS + _TS + _GO + _SH))

_STEM = re.compile(r"^[a-z][a-z0-9_]*$")


def reserved_hit(name):
    low = name.lower()
    if low in RESERVED:
        return True
    if low.startswith(("test", "conftest")) or low.endswith("test") or low.endswith("_test"):
        return True                      # runner discovery patterns (test_*.py, *_test.py / *_test.go) must never match a module file
    return any(part in RESERVED for part in low.split("_")) if "_" in low else False


class Idents:
    """One instance per module. `seed` makes the whole module reproducible; `tag` separates the three families."""

    def __init__(self, seed, tag):
        self.tag = tag
        self.ns = NameSpace("training", "%s:%s" % (tag, seed), deny_check=reserved_hit)
        self._used = set()
        self._cache = {}

    def _draw(self, kind, key, post=None):
        ck = (kind, key, post)
        if ck in self._cache:
            return self._cache[ck]
        for bump in range(64):
            k = key if bump == 0 else "%s#%d" % (key, bump)
            nm = self.ns.name(kind, "%s/%s" % (self.tag, k))
            nm = nm.replace("-", "_")
            if post:
                nm = post(nm)
            if nm.lower() in self._used or not _STEM.match(nm.lower()) or reserved_hit(nm):
                continue
            self._used.add(nm.lower())
            self._cache[ck] = nm
            return nm
        raise NamespaceError("could not mint a unique %s identifier for %s" % (kind, key))

    # snake_case two-stem names: functions, modules, constants (upper-cased at render time when wanted)
    def func(self, key):
        return self._draw("tool", "f:" + key)

    def module_stem(self, key):
        return self._draw("repo", "m:" + key)

    # one-stem names: variables, parameters, fields, string constants
    def var(self, key):
        return self._draw("user", "v:" + key)

    def field(self, key):
        return self._draw("user", "fl:" + key)

    def const(self, key):
        return self._draw("policy", "c:" + key)

    def strval(self, key):
        return self._draw("user", "s:" + key)

    def typename(self, key):
        return self._draw("user", "t:" + key, post=lambda s: s.capitalize())

    def package(self, key):
        return self._draw("user", "p:" + key)
