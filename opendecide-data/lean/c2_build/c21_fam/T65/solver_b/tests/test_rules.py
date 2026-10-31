"""Fixtures per fact class and per rule branch, plus the neutraliser-class x treatment truth table (G0-lite 2.1: a step counts only if made for THAT class,
applied to the value that reaches the sink, before it on every path, result used)."""
import itertools

import pytest

from T65.solver_b import hook
from T65.solver_b import rules as R
from views import HEADIMPORTS, cwe_view, vuln_view


def run(code, cls, **kw):
    return hook.solver_b(vuln_view(HEADIMPORTS + "\n\n" + code, cls, **kw))


def expect(code, cls, label, **kw):
    res = run(code, cls, **kw)
    assert res["status"] == "ok", res
    assert res["label"] == label, res
    want = "A" if (label == "YES") == kw.get("yes_first", True) else "B"
    assert res["letter"] == want


# ---- dynamic classes: truth table ------------------------------------------------------------------------------------------------------------------
NEUT = {"CWEC-22": lambda v: 'os.path.basename(%s)' % v, "CWEC-78": lambda v: 'shlex.quote(%s)' % v, "CWEC-79": lambda v: 'html.escape(%s)' % v,
        "CWEC-89": lambda v: '%s.replace("\'", "\'\'")' % v, "CWEC-117": lambda v: r'%s.replace("\n", " ")' % v, "CWEC-601": lambda v: '"/" + %s.lstrip("/")' % v}
SINK = {
    "CWEC-22": '    path = os.path.join("srv/files", v)\n    fh = open(path)\n    out = fh.read()\n    fh.close()\n',
    "CWEC-78": '    res = subprocess.run("echo " + v, shell=True, capture_output=True, text=True)\n    out = res.stdout\n',
    "CWEC-79": '    out = "<p>" + v + "</p>"\n',
    "CWEC-89": ('    conn = sqlite3.connect(":memory:")\n    cur = conn.cursor()\n    cur.execute("CREATE TABLE users (id TEXT, name TEXT)")\n'
                '    cur.execute("SELECT name FROM users WHERE id = \'" + v + "\'")\n    out = cur.fetchall()\n'),
    "CWEC-117": '    out = "INFO user=" + v\n',
    "CWEC-601": '    out = v + "#top"\n',
}


def build(cls, treat, wrong=None):
    n = NEUT[cls]
    defs, pre, post, src = "", [], [], "    v = p\n"
    if treat == "none":
        pass
    elif treat == "own":
        pre = ["v = " + n("v")]
    elif treat == "wrong":
        pre = ["v = " + NEUT[wrong]("v")]
    elif treat == "other_var":
        pre = ["w = v", "w = " + n("w")]
    elif treat == "after":
        post = ["v = " + n("v")]
    elif treat == "discard":
        pre = [n("v")]
    elif treat == "branch":
        pre = ["if len(v) < 5:", "    v = " + n("v")]
    elif treat == "replaced":
        pre = ["v = " + n("v"), "v = p"]
    elif treat == "helper_real":
        defs = "def clean_a(x):\n    return %s\n\n\ndef step_a(x):\n    return clean_a(x)\n\n\n" % n("x")
        pre = ["v = step_a(v)"]
    elif treat == "helper_noop":
        defs = "def clean_a(x):\n    return x\n\n\ndef step_a(x):\n    return clean_a(x)\n\n\n"
        pre = ["v = step_a(v)"]
    elif treat == "allow_in":
        pre = ['if v not in ("a", "b"):', '    raise ValueError("no")']
    elif treat == "allow_eq":
        pre = ['if v != "a":', '    raise ValueError("no")']
    elif treat == "allow_const_name":
        defs = 'OK_VALUES = ("a", "b")\n\n\n'
        pre = ['if v not in OK_VALUES:', '    raise ValueError("no")']
    elif treat == "allow_pos":
        pre = ['if v in ("a", "b"):', '    v = v']
    elif treat == "const":
        src = '    v = "fixed"\n'
    elif treat == "container_own":
        pre = ["v = " + n("v"), 'd = {"k": v}', 'v = d["k"]']
    elif treat == "container_raw":
        pre = ['d = {"k": v}', 'v = d["k"]']
    elif treat == "format_after_own":
        pre = ["v = " + n("v"), 'v = "item " + v']
    elif treat == "format_before_own":
        pre = ['v = "item " + v', "v = " + n("v")]
    elif treat == "transforms_then_own":
        pre = ["v = v.strip()", "v = v.lower()", "v = " + n("v")]
    elif treat == "own_then_transforms":
        pre = ["v = " + n("v"), "v = v.strip()", "v = v.lower()"]
    elif treat == "own_on_branch_both":
        pre = ["if len(v) < 5:", "    v = " + n("v"), "else:", "    v = " + n("v")]
    elif treat == "own_in_return_branch":
        pre = ["if len(v) < 5:", '    raise ValueError("short")', "v = " + n("v")]
    else:
        raise AssertionError(treat)
    body = defs + "def entry_fn(p):\n" + src
    body += "".join("    " + l + "\n" for l in pre) + SINK[cls] + "".join("    " + l + "\n" for l in post) + "    return out\n"
    return body


SAFE_TREATS = {"own", "helper_real", "allow_in", "allow_eq", "allow_const_name", "const", "container_own", "format_after_own", "format_before_own",
               "transforms_then_own", "own_then_transforms", "own_on_branch_both", "own_in_return_branch"}
FLAWED_TREATS = {"none", "allow_pos", "other_var", "after", "discard", "branch", "replaced", "helper_noop", "container_raw"}


@pytest.mark.parametrize("cls", R.DYNAMIC)
@pytest.mark.parametrize("treat", sorted(SAFE_TREATS | FLAWED_TREATS))
def test_truth_table_own_class(cls, treat):
    expect(build(cls, treat), cls, "NO" if treat in SAFE_TREATS else "YES")


@pytest.mark.parametrize("cls,wrong", [(c, w) for c in R.DYNAMIC for w in R.DYNAMIC if w != c])
def test_wrong_class_neutraliser_is_still_flawed(cls, wrong):
    expect(build(cls, "wrong", wrong), cls, "YES")


@pytest.mark.parametrize("cls,wrong", [(c, w) for c in R.DYNAMIC for w in R.DYNAMIC if w != c])
def test_own_after_wrong_class_is_sound(cls, wrong):
    code = build(cls, "own").replace("    v = p\n", "    v = p\n    v = %s\n" % NEUT[wrong]("v"))
    expect(code, cls, "NO")


def test_allow_list_positive_branch_holds_the_sink():
    sink = SINK["CWEC-22"].replace("\n    ", "\n        ").replace("    path", "        path", 1)
    code = 'def entry_fn(p):\n    v = p\n    out = ""\n    if v in ("a", "b"):\n' + sink + '    return out\n'
    expect(code, "CWEC-22", "NO")
    code = 'def entry_fn(p):\n    v = p\n    out = ""\n    if v not in ("a", "b"):\n' + sink + '    return out\n'
    expect(code, "CWEC-22", "YES")


def test_flags_are_independent_of_option_order():
    expect(build("CWEC-22", "none"), "CWEC-22", "YES", yes_first=False)
    expect(build("CWEC-22", "own"), "CWEC-22", "NO", yes_first=False)


def test_sql_parameterised_and_argv_are_sound():
    code = build("CWEC-89", "none").replace("""cur.execute("SELECT name FROM users WHERE id = '" + v + "'")""", 'cur.execute("SELECT name FROM users WHERE id = ?", (v,))')
    expect(code, "CWEC-89", "NO")
    code = build("CWEC-78", "none").replace('subprocess.run("echo " + v, shell=True,', 'subprocess.run(["echo", v],')
    expect(code, "CWEC-78", "NO")
    code = build("CWEC-78", "none").replace("shell=True, ", "")
    expect(code, "CWEC-78", "NO")                     # a string command without a shell: no shell metacharacter is interpreted


def test_sink_variants_dynamic():
    expect(build("CWEC-78", "none").replace('subprocess.run("echo " + v, shell=True, capture_output=True, text=True)', 'os.system("echo " + v)'), "CWEC-78", "YES")
    expect(build("CWEC-79", "none").replace('"<p>" + v + "</p>"', 'f"<p>{v}</p>"'), "CWEC-79", "YES")
    expect(build("CWEC-79", "none").replace('"<p>" + v + "</p>"', '"<p>%s</p>" % v'), "CWEC-79", "YES")
    expect(build("CWEC-79", "none").replace('"<p>" + v + "</p>"', '"<p>{}</p>".format(v)'), "CWEC-79", "YES")
    expect(build("CWEC-117", "none").replace('"INFO user=" + v', '"WARNING user=" + v'), "CWEC-117", "YES")
    expect(build("CWEC-601", "none").replace('v + "#top"', 'v'), "CWEC-601", "YES")


def test_source_is_only_the_named_parameter():
    code = build("CWEC-79", "none").replace("def entry_fn(p):", "def entry_fn(p, q):").replace('"<p>" + v + "</p>"', '"<p>" + q + "</p>"')
    expect(code, "CWEC-79", "NO")            # q is not the request parameter: nothing an attacker controls reaches the sink
    code = build("CWEC-79", "none").replace("def entry_fn(p):", "def entry_fn(q, p):")
    expect(code, "CWEC-79", "YES")


def test_code_after_return_is_unreachable():
    code = build("CWEC-22", "none").replace("    return out\n", "    return out\n    v = os.path.basename(v)\n")
    expect(code, "CWEC-22", "YES")
    code = build("CWEC-22", "own").replace("    return out\n", "    return out\n    fh = open(p)\n    return fh.read()\n")
    expect(code, "CWEC-22", "NO")             # the raw open after the return can never run
    code = build("CWEC-22", "own").replace("    fh = open(path)", "    return 'x'\n    fh = open(path)")
    assert run(code, "CWEC-22")["status"] == "abstain"          # no reachable operation of the class: nothing to label


def test_sanitiser_on_the_other_branch_only_both_paths_needed():
    code = build("CWEC-22", "none").replace("    path =", "    if len(v) < 9:\n        v = os.path.basename(v)\n    else:\n        v = v.lower()\n    path =")
    expect(code, "CWEC-22", "YES")


# ---- static classes -----------------------------------------------------------------------------------------------------------------------------
TLS_BAD = "    c = ssl.create_default_context()\n    c.check_hostname = False\n    c.verify_mode = ssl.CERT_NONE\n"
TLS_FIX = "    c.verify_mode = ssl.CERT_REQUIRED\n    c.check_hostname = True\n"


@pytest.mark.parametrize("name,body,label", [
    ("disabled", TLS_BAD + "    return c\n", "YES"),
    ("fixed", TLS_BAD + TLS_FIX + "    return c\n", "NO"),
    ("default", "    c = ssl.create_default_context()\n    return c\n", "NO"),
    ("unverified_ctor", "    c = ssl._create_unverified_context()\n    return c\n", "YES"),
    ("after_return", TLS_BAD + "    return c\n" + TLS_FIX, "YES"),
    ("other_ctx", TLS_BAD + "    d = ssl.create_default_context()\n    d.verify_mode = ssl.CERT_REQUIRED\n    d.check_hostname = True\n    return c\n", "YES"),
    ("other_ctx_returned", TLS_BAD + "    d = ssl.create_default_context()\n    return d\n", "NO"),
    ("branch_only", TLS_BAD + "    if p == '':\n        c.verify_mode = ssl.CERT_REQUIRED\n    return c\n", "YES"),
    ("discarded_expr", TLS_BAD + "    ssl.CERT_REQUIRED\n    return c\n", "YES"),
    ("replaced", TLS_BAD + "    c.verify_mode = ssl.CERT_REQUIRED\n    c.verify_mode = ssl.CERT_NONE\n    return c\n", "YES"),
    ("wrong_attr", TLS_BAD + "    c.minimum_version = ssl.TLSVersion.TLSv1_2\n    return c\n", "YES"),
    ("both_branches_fixed", TLS_BAD + "    if p:\n        c.verify_mode = ssl.CERT_REQUIRED\n        c.check_hostname = True\n    else:\n        c.verify_mode = ssl.CERT_REQUIRED\n        c.check_hostname = True\n    return c\n", "NO"),
    ("hostname_only_off", "    c = ssl.create_default_context()\n    c.check_hostname = False\n    return c\n", "YES"),
])
def test_tls(name, body, label):
    expect(HEADIMPORTS + "\n\ndef entry_fn(p):\n" + body, "CWEC-295", label)


def test_tls_helpers():
    real = "def fix_a(x):\n    x.verify_mode = ssl.CERT_REQUIRED\n    x.check_hostname = True\n    return x\n\n\ndef step_a(x):\n    return fix_a(x)\n\n\n"
    noop = "def fix_a(x):\n    return x\n\n\ndef step_a(x):\n    return fix_a(x)\n\n\n"
    tail = "def entry_fn(p):\n" + TLS_BAD + "    c = step_a(c)\n    return c\n"
    expect(HEADIMPORTS + "\n\n" + real + tail, "CWEC-295", "NO")
    expect(HEADIMPORTS + "\n\n" + noop + tail, "CWEC-295", "YES")
    branch = ("def fix_a(x, y):\n    if y:\n        x.verify_mode = ssl.CERT_REQUIRED\n        x.check_hostname = True\n    return x\n\n\n"
              "def entry_fn(p):\n" + TLS_BAD + "    c = fix_a(c, p)\n    return c\n")
    expect(HEADIMPORTS + "\n\n" + branch, "CWEC-295", "YES")           # re-enabled on one path only


HASH_SALT = 'SALT_A = b"salt"\n\n\n'


@pytest.mark.parametrize("name,body,label", [
    ("md5_pw", "    d = hashlib.md5(password.encode()).hexdigest()\n    return d\n", "YES"),
    ("sha1_pw", "    d = hashlib.sha1(password.encode()).hexdigest()\n    return d\n", "YES"),
    ("sha256_plain", "    d = hashlib.sha256(password.encode()).hexdigest()\n    return d\n", "YES"),
    ("sha256_salted_prefix", "    d = hashlib.sha256(SALT_A + password.encode()).hexdigest()\n    return d\n", "YES"),
    ("pbkdf2", '    d = hashlib.pbkdf2_hmac("sha256", password.encode(), SALT_A, 100000).hex()\n    return d\n', "NO"),
    ("scrypt", "    d = hashlib.scrypt(password.encode(), salt=SALT_A, n=16384, r=8, p=1).hex()\n    return d\n", "NO"),
    ("md5_filename", "    d = hashlib.md5(filename.encode()).hexdigest()\n    return d\n", "NO"),
    ("both_unused_md5", '    a = hashlib.pbkdf2_hmac("sha256", password.encode(), SALT_A, 100000).hex()\n    b = hashlib.md5(password.encode()).hexdigest()\n    return a\n', "NO"),
    ("both_returns_md5", '    a = hashlib.pbkdf2_hmac("sha256", password.encode(), SALT_A, 100000).hex()\n    b = hashlib.md5(password.encode()).hexdigest()\n    return b\n', "YES"),
    ("pbkdf2_discarded", '    hashlib.pbkdf2_hmac("sha256", password.encode(), SALT_A, 100000).hex()\n    d = hashlib.md5(password.encode()).hexdigest()\n    return d\n', "YES"),
    ("replaced", '    d = hashlib.pbkdf2_hmac("sha256", password.encode(), SALT_A, 100000).hex()\n    d = hashlib.md5(password.encode()).hexdigest()\n    return d\n', "YES"),
    ("branch_only", '    d = hashlib.md5(password.encode()).hexdigest()\n    if len(password) < 8:\n        d = hashlib.pbkdf2_hmac("sha256", password.encode(), SALT_A, 100000).hex()\n    return d\n', "YES"),
    ("after_return", '    d = hashlib.md5(password.encode()).hexdigest()\n    return d\n    d = hashlib.pbkdf2_hmac("sha256", password.encode(), SALT_A, 100000).hex()\n', "YES"),
    ("fixed_after_md5", '    d = hashlib.md5(password.encode()).hexdigest()\n    d = hashlib.pbkdf2_hmac("sha256", password.encode(), SALT_A, 100000).hex()\n    return d\n', "NO"),
])
def test_password_hash(name, body, label):
    param = "filename" if "filename" in body else "password"
    expect(HEADIMPORTS + "\n" + HASH_SALT + "def entry_fn(%s):\n" % param + body, "CWEC-327", label)


def test_password_hash_helper_chain_and_role_through_calls():
    chain = "def h_a(x):\n    return %s\n\n\ndef h_b(x):\n    return h_a(x)\n\n\n"
    tail = "def entry_fn(password):\n    d = h_b(password)\n    return d\n"
    expect(HEADIMPORTS + "\n" + HASH_SALT + chain % "hashlib.md5(x.encode()).hexdigest()" + tail, "CWEC-327", "YES")
    expect(HEADIMPORTS + "\n" + HASH_SALT + chain % 'hashlib.pbkdf2_hmac("sha256", x.encode(), SALT_A, 100000).hex()' + tail, "CWEC-327", "NO")
    tail2 = "def entry_fn(label):\n    d = h_b(label)\n    return d\n"
    expect(HEADIMPORTS + "\n" + HASH_SALT + chain % "hashlib.md5(x.encode()).hexdigest()" + tail2, "CWEC-327", "NO")


@pytest.mark.parametrize("name,body,label", [
    ("mktemp", "    t = tempfile.mktemp(suffix='.log')\n    return t\n", "YES"),
    ("mkstemp", "    fd, t = tempfile.mkstemp(suffix='.log')\n    return t\n", "NO"),
    ("mkdtemp_join", "    d = tempfile.mkdtemp()\n    t = d + '/' + 'name'\n    return t\n", "NO"),
    ("shared_dir_name", "    d = tempfile.gettempdir()\n    t = d + '/' + 'name'\n    return t\n", "YES"),
    ("shared_dir_unused", "    d = tempfile.gettempdir()\n    fd, t = tempfile.mkstemp()\n    return t\n", "NO"),
    ("mktemp_unused", "    t = tempfile.mktemp()\n    fd, u = tempfile.mkstemp()\n    return u\n", "NO"),
    ("mkstemp_then_mktemp", "    fd, t = tempfile.mkstemp()\n    t = tempfile.mktemp()\n    return t\n", "YES"),
    ("mktemp_then_mkstemp", "    t = tempfile.mktemp()\n    fd, t = tempfile.mkstemp()\n    return t\n", "NO"),
    ("branch_only", "    t = tempfile.mktemp()\n    if p:\n        fd, t = tempfile.mkstemp()\n    return t\n", "YES"),
    ("after_return", "    t = tempfile.mktemp()\n    return t\n    fd, t = tempfile.mkstemp()\n", "YES"),
    ("discarded", "    tempfile.mkstemp()\n    t = tempfile.mktemp()\n    return t\n", "YES"),
    ("tuple_return_helper_bad", "    a, b = mk_b()\n    return b\n", "YES"),
    ("tuple_return_helper_good", "    return tempfile.mkstemp(suffix='.x')\n", "NO"),
    ("opened_name", "    t = tempfile.mktemp()\n    f = open(t, 'w')\n    f.write('x')\n    f.close()\n    return 'ok'\n", "YES"),
])
def test_temp_files(name, body, label):
    helper = "def mk_a():\n    return None, tempfile.mktemp(suffix='.log')\n\n\ndef mk_b():\n    return mk_a()\n\n\n" if "mk_b" in body else ""
    expect(HEADIMPORTS + "\n\n" + helper + "def entry_fn(p):\n" + body, "CWEC-377", label)


# ---- CWE head rows ---------------------------------------------------------------------------------------------------------------------------------
ALL_NEAR = {"CWEC-22": ["CWEC-22", "CWEC-78", "CWEC-601", "CWEC-377"], "CWEC-78": ["CWEC-89", "CWEC-22", "CWEC-78", "CWEC-117"],
            "CWEC-79": ["CWEC-117", "CWEC-79", "CWEC-601", "CWEC-89"], "CWEC-89": ["CWEC-78", "CWEC-79", "CWEC-89", "CWEC-117"],
            "CWEC-117": ["CWEC-79", "CWEC-89", "CWEC-78", "CWEC-117"], "CWEC-601": ["CWEC-79", "CWEC-22", "CWEC-295", "CWEC-601"],
            "CWEC-295": ["CWEC-327", "CWEC-601", "CWEC-295", "CWEC-377"], "CWEC-327": ["CWEC-295", "CWEC-377", "CWEC-89", "CWEC-327"],
            "CWEC-377": ["CWEC-22", "CWEC-327", "CWEC-295", "CWEC-377"]}
STATIC_CODE = {"CWEC-295": "def entry_fn(p):\n" + TLS_BAD + "    return c\n", "CWEC-327": "def entry_fn(password):\n    d = hashlib.md5(password.encode()).hexdigest()\n    return d\n",
               "CWEC-377": "def entry_fn(p):\n    t = tempfile.mktemp()\n    return t\n"}


@pytest.mark.parametrize("cls", R.CLASSES)
@pytest.mark.parametrize("rot", [0, 2])
def test_cwe_head_picks_the_class_word(cls, rot):
    code = HEADIMPORTS + "\n\n" + (STATIC_CODE[cls] if cls in STATIC_CODE else build(cls, "none"))
    order = ALL_NEAR[cls][rot:] + ALL_NEAR[cls][:rot]
    v = cwe_view(code, order)
    res = hook.solver_b(v)
    assert res["status"] == "ok", res
    assert res["label"] == R.CLASS_WORDS[cls]
    assert dict((o["letter"], o["text"]) for o in v["options"])[res["letter"]] == R.CLASS_WORDS[cls]
    assert res["cls"] == cls


def test_cwe_head_abstains_without_a_flaw_or_with_two():
    sound = HEADIMPORTS + "\n\n" + build("CWEC-22", "own")
    assert hook.solver_b(cwe_view(sound))["status"] == "abstain"
    two = HEADIMPORTS + "\n\n" + "def entry_fn(p):\n    v = p\n    path = os.path.join('srv/files', v)\n    fh = open(path)\n    out = fh.read()\n    fh.close()\n" \
        "    res = subprocess.run('echo ' + v, shell=True, capture_output=True, text=True)\n    return out\n"
    assert hook.solver_b(cwe_view(two))["status"] == "abstain"
    # the class named by no option cannot be answered
    assert hook.solver_b(cwe_view(HEADIMPORTS + "\n\n" + build("CWEC-79", "none"), ["CWEC-22", "CWEC-78", "CWEC-89", "CWEC-117"]))["status"] == "abstain"


# ---- abstain, never guess ---------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("body", [
    "    for i in range(3):\n        v = v + 'x'\n    out = '<p>' + v\n    return out\n",
    "    with open('f') as fh:\n        out = fh.read()\n    return '<p>' + v\n",
    "    try:\n        out = '<p>' + v\n    except ValueError:\n        out = ''\n    return out\n",
    "    out = '<p>' + mystery.call(v)\n    return out\n",
    "    out = '<p>' + int(v)\n    return out\n",
    "    out = '<p>' + v.replace('a', 'b')\n    return out\n",
    "    out = [x for x in v]\n    return out\n",
    "    return '<p>' + unknown_name\n",
])
def test_unmodelled_constructs_abstain(body):
    res = run("import mystery\n\n\ndef entry_fn(p):\n    v = p\n" + body, "CWEC-79")
    assert res["status"] == "abstain" and res["label"] is None, res


def test_bad_inputs_abstain_or_error_not_guess():
    good = vuln_view(HEADIMPORTS + "\n\n" + build("CWEC-79", "none"), "CWEC-79")
    bad = dict(good, rendered=dict(good["rendered"], context=good["rendered"]["context"].replace("Function (", "Fn (")))
    assert hook.solver_b(bad)["status"] == "abstain"
    bad = dict(good, options=[{"letter": "A", "text": "NO"}, {"letter": "B", "text": "YES"}])
    assert hook.solver_b(bad)["status"] == "abstain"              # option list contradicts the rendered options text
    bad = dict(good, rendered=dict(good["rendered"], context=good["rendered"]["context"].replace("def entry_fn(p):", "def entry_fn(p)")))
    assert hook.solver_b(bad)["status"] == "abstain"              # code does not parse
    bad = {k: v for k, v in good.items() if k != "rendered"}
    assert hook.solver_b(bad)["status"] in ("abstain", "error")
    no_note = vuln_view(HEADIMPORTS + "\n\n" + build("CWEC-79", "none"), "CWEC-79", notes=False)
    assert hook.solver_b(no_note)["status"] == "abstain"
    wrong_class = vuln_view(HEADIMPORTS + "\n\n" + build("CWEC-79", "none"), "CWEC-22")
    assert hook.solver_b(wrong_class)["status"] == "abstain"      # flaw found is another class than the sub-block


def test_no_operation_of_the_class_abstains():
    res = run("def entry_fn(p):\n    v = p\n    return len(v)\n", "CWEC-22")
    assert res["status"] == "abstain"


def test_letters_recovered_from_rendered_options():
    res = hook.solver_b(vuln_view(HEADIMPORTS + "\n\n" + build("CWEC-22", "none"), "CWEC-22", yes_first=False))
    assert (res["label"], res["letter"]) == ("YES", "B")


def _with_question(view, q):
    r = dict(view["rendered"], question=q)
    r["text"] = r["context"] + "\n\n" + q + "\n\n" + r["options_text"]
    return dict(view, rendered=r)


def test_entry_function_is_the_one_the_question_names():
    base = HEADIMPORTS + "\n\n" + build("CWEC-22", "none") + "\n\ndef spare_fn(x):\n    return x\n"
    v = vuln_view(base, "CWEC-22")
    assert hook.solver_b(v)["status"] == "abstain"                              # without the question: the last uncalled def is spare_fn, which has no request parameter
    named = hook.solver_b(_with_question(v, "Does the function entry_fn contain the flaw?"))
    assert named["status"] == "ok" and named["label"] == "YES"
    helper_named = HEADIMPORTS + "\n\ndef clean_a(x):\n    return os.path.basename(x)\n\n\n" + build("CWEC-22", "none").replace("v = p", "v = clean_a(p)")
    v = _with_question(vuln_view(helper_named, "CWEC-22"), "Does the function clean_a contain the flaw?")
    assert hook.solver_b(v)["status"] == "abstain"                              # the question names a helper that the entry calls: ambiguous, not guessed
