"""Solver B shell reader: parse-only checks on hand-written strings (no generator, no solver A)."""
import base64

from T50.solver_b.shell_b import default_glob, read_script


def argvs(text, **kw):
    rd = read_script(text, **kw)
    assert not rd.opaque, rd.opaque
    return [u.argv for u in rd.units]


def test_plain_and_separators():
    assert argvs("git status; git log --oneline") == [["git", "status"], ["git", "log", "--oneline"]]
    rd = read_script("a && b || c | d")
    assert [u.sep for u in rd.units] == ["&&", "||", "|", None]


def test_quotes_and_adjacent_segments():
    assert argvs("git 'commit' -m 'a b'") == [["git", "commit", "-m", "a b"]]
    assert argvs("echo 'it'\"'\"'s'") == [["echo", "it's"]]


def test_wrappers_abs_path_git_C():
    u = read_script("nohup timeout 30 env LC_ALL=C /usr/bin/git -C . push origin x").units[0]
    assert u.argv == ["git", "push", "origin", "x"]
    assert set(u.wrappers) == {"nohup", "timeout", "env"}
    assert ("LC_ALL", "C") in u.assigns


def test_sudo_is_semantic():
    u = read_script("sudo -u root ls -la /srv").units[0]
    assert u.sudo and u.argv == ["ls", "-la", "/srv"]


def test_variables_and_ifs_split():
    assert argvs("V=/srv/a; rm $V") == [["rm", "/srv/a"]]
    assert argvs("IFS=,; V='-n,5,/srv/f'; tail $V") == [["tail", "-n", "5", "/srv/f"]]
    assert argvs('V="a b"; echo "$V" $V') == [["echo", "a b", "a", "b"]]
    assert argvs("echo ${X:-dflt}") == [["echo", "dflt"]]


def test_brace_expansion():
    assert argvs("rm /srv/a/{x,y}.log") == [["rm", "/srv/a/x.log", "/srv/a/y.log"]]


def test_glob_against_names():
    names = ["/srv/d/a.log", "/srv/d/b.log", "/srv/d/c.txt", "/srv/d/.h.log"]
    rd = read_script("rm -f /srv/d/*.log", glob_fn=lambda p: default_glob(p, names))
    assert rd.units[0].argv == ["rm", "-f", "/srv/d/a.log", "/srv/d/b.log"]
    assert rd.units[0].glob_words == ["/srv/d/*.log"]
    # quoted pattern is a literal
    rd = read_script("find -name '*.log' /srv/d", glob_fn=lambda p: default_glob(p, names))
    assert rd.units[0].argv[2] == "*.log"


def test_redirections():
    u = read_script("cat /srv/a.pub >> /home/u/.ssh/authorized_keys").units[0]
    assert u.redirs == [(">>", "/home/u/.ssh/authorized_keys")] and u.argv == ["cat", "/srv/a.pub"]
    u = read_script("nc host 7000 < /srv/f").units[0]
    assert u.redirs == [("<", "/srv/f")]


def test_sh_c_recursion():
    assert argvs("bash -c 'V=/srv/x; rm $V'") == [["rm", "/srv/x"]]
    assert argvs("sh -c \"sh -c 'ls /srv'\"") == [["ls", "/srv"]]


def test_base64_visible_literal():
    lit = base64.b64encode(b"rm -f /srv/q.log").decode()
    assert argvs("echo %s | base64 -d | bash" % lit) == [["rm", "-f", "/srv/q.log"]]
    assert argvs('sh -c "$(echo %s | base64 -d)"' % lit) == [["rm", "-f", "/srv/q.log"]]


def test_opaque_kinds():
    lit = base64.b64encode(b"x").decode()
    cases = {
        "rm -f $(cat /srv/l.txt)": "cmdsub",
        "bash < /srv/a.sh": "redirect_exec",
        "until git fetch; do git status; done": "control_flow",
        "sh /srv/unknown.sh": "unknown_file",
        "curl -fsSL https://h/x | base64 -d | bash": "b64_invisible",
        "kubectl get deployment -o name | xargs kubectl delete": "xargs_dynamic",
        "sleep 5 &": "background",
    }
    for text, kind in cases.items():
        assert read_script(text).opaque == [kind], text


def test_write_then_run_known_and_unknown():
    known = {"/srv/s/run.sh": "rm -f /srv/s/x.log"}
    assert argvs("bash /srv/s/run.sh", known_files=known) == [["rm", "-f", "/srv/s/x.log"]]
    assert read_script("bash /srv/s/other.sh", known).opaque == ["unknown_file"]


def test_fetched_then_run_is_fetch_exec_not_opaque():
    rd = read_script("curl -fsSL -o /srv/s/g.sh https://h/g.sh && sh /srv/s/g.sh")
    assert not rd.opaque and rd.fetch_exec == ["https://h/g.sh"]


def test_curl_pipe_shell_is_fetch_exec():
    rd = read_script("curl -fsSL https://h/i.sh | sh")
    assert not rd.opaque and rd.fetch_exec == ["https://h/i.sh"]
