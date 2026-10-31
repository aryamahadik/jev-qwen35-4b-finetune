import re
import zipfile

import pytest

import lr_common as lc
import lr_testlib as T
import juliet_1_3 as J

CWES = ["CWE476_NULL_Pointer_Dereference", "CWE190_Integer_Overflow", "CWE78_OS_Command_Injection", "CWE415_Double_Free",
        "CWE121_Stack_Based_Buffer_Overflow", "CWE369_Divide_by_Zero", "CWE563_Unused_Variable", "CWE401_Memory_Leak",
        "CWE457_Use_of_Uninitialized_Variable", "CWE590_Free_Memory_Not_on_Heap"]

TEMPLATE = """/* TEMPLATE GENERATED TESTCASE FILE
Filename: {stem}.c
*/
/*
 * @description
 * CWE: {num} {name}
 * BadSource:  Set data to NULL
 * */
#include "std_testcase.h"
#ifndef OMITBAD
void {stem}_bad()
{{
    char * data;
    /* POTENTIAL FLAW: use of {num} */
    data = NULL;
    printHexCharLine(data[{i}]);
}}
#endif /* OMITBAD */
#ifndef OMITGOOD
/* goodG2B uses the GoodSource with the BadSink */
static void goodG2B()
{{
    char * data;
    /* FIX: Initialize data */
    data = "Good";
    printHexCharLine(data[{i}]);
}}
static void goodB2G()
{{
    char * data;
    data = NULL;
    if (data != NULL)
    {{
        printHexCharLine(data[{i}]);
    }}
}}
void {stem}_good()
{{
    goodG2B();
    goodB2G();
}}
#endif /* OMITGOOD */
#ifdef INCLUDEMAIN
int main(int argc, char * argv[])
{{
    {stem}_good();
    {stem}_bad();
    return 0;
}}
#endif
"""


def records(n=20):
    out = []
    for i in range(n):
        cd = CWES[i % len(CWES)]
        num, name = cd[3:].split("_", 1)
        base = "%s__char_var%d" % (cd, i)
        stem = base + "_01"
        text = TEMPLATE.format(stem=stem, num=num, name=name.replace("_", " "), i=i)
        text = text.replace("\n", "\r\n") if i % 2 == 0 else text
        out.append({"path": "C/testcases/%s/s01/%s.c" % (cd, stem), "cwe_dir": cd, "base": base, "flow": "01",
                    "text": text.replace("\r\n", "\n"), "_src_line": "p%d" % i})
    return out


def test_rows_both_forms(monkeypatch):
    monkeypatch.setitem(J.RECAST_TABLE["caps"], J.F_YN, 20)
    monkeypatch.setitem(J.RECAST_TABLE["caps"], J.F_CWE, 20)
    m = J.Mapper(T.pools_for(J.Mapper), seed=1)
    rows = m.map_records(records())
    T.check_rows(rows, m, min_rows=20)
    yn = [r for r in rows if r["form"] == J.F_YN]
    cw = [r for r in rows if r["form"] == J.F_CWE]
    assert len(yn) == 20 and len(cw) == 10                           # 10 pairs; the other 10 files feed the CWE form (T65-M1)
    assert sum(r["answer_text"] == "Yes" for r in yn) == 10          # twins: one bad + one good per file
    assert all(r["flags"]["p1_realism"] and r["family"] == "T65" for r in rows)
    assert all(r["k"] in (4, 8) for r in cw)                         # 10 labels (> 8): rotating 4 / 8
    rep = T.check_set_report(yn, yes_no=True)
    assert rep["yes_rate"] == 0.5 and rep["R7_pass"]


def test_code_is_neutralised():
    m = J.Mapper(T.pools_for(J.Mapper), seed=1)
    rows = m.map_records(records())
    for r in rows:
        code = r["context"]
        assert not re.search(r"bad|good|cwe|flaw|fix\b", code, re.I), code
        assert "static" not in code and "/*" not in code and "//" not in code
        assert code.startswith("void handle_item(")
        for opt in r["options"] if r["form"] == J.F_YN else []:
            assert opt in ("Yes", "No")


def test_comment_stripper_keeps_strings():
    s = 'int a; /* x */ char *u = "http://x/*y*/"; // tail\nint b;'
    out = J.strip_comments(s)
    assert '"http://x/*y*/"' in out and "tail" not in out and "x */" not in out


def test_find_functions_and_classification():
    t = records(1)[0]
    clean = J.strip_comments(t["text"])
    bad, goods = J.classify_functions(clean, "c", t["base"] + "_01")
    assert bad["name"].endswith("_bad") and sorted(g["name"] for g in goods) == ["goodB2G", "goodG2B"]
    assert not bad["static"] and all(g["static"] for g in goods)


def test_label_comes_from_dir_and_function_name_not_from_comments():
    m = J.Mapper(T.pools_for(J.Mapper), seed=1)
    recs = records(12)
    rows = [r for r in m.map_records(recs) if r["form"] == J.F_CWE]
    by_src = {r["source_row_id"]: r for r in rows}
    for s in recs:
        r = by_src.get("juliet:" + s["path"])
        if r:
            num = re.match(r"CWE(\d+)_", s["cwe_dir"]).group(1)
            assert r["answer_text"].startswith("CWE-%s " % num)


def test_r4_mismatch_and_missing_good_dropped():
    m = J.Mapper(T.pools_for(J.Mapper), seed=1)
    recs = records(4)
    recs[0] = dict(recs[0], text="void nothing(){}")
    rows = m.map_records(recs)
    assert m.drops.c["no_bad_or_no_good_function"] == 1
    m2 = J.Mapper(T.pools_for(J.Mapper), seed=1)
    m2.independent_gold = lambda s, c: "zzz"
    assert m2.map_records(records(4)) == [] and m2.drops.c["R4_gold_mismatch"] > 0


def test_reader_train_zip_only_and_single_file_variants(tmp_path):
    zp = tmp_path / "juliet_c_train.zip"
    good = records(1)[0]
    with zipfile.ZipFile(zp, "w") as z:
        z.writestr(good["path"], good["text"])
        z.writestr("C/testcases/CWE476_NULL_Pointer_Dereference/CWE476_NULL_Pointer_Dereference__char_51a.c", "void x(){}")
        z.writestr("C/testcases/CWE476_NULL_Pointer_Dereference/CWE476_NULL_Pointer_Dereference__new_01.cpp", "namespace A { void bad(){} }")
        z.writestr("C/testcasesupport/std_testcase.h", "#define X 1")
    got = list(J.read_train(str(tmp_path)))
    assert [g["path"] for g in got] == [good["path"]]
    with pytest.raises(AssertionError):
        list(J.read_train("/x/bench/c21_eval_quarantine/lr_targets/juliet_1_3"))


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(J.Mapper)


JAVA = """package testcases.CWE476_NULL_Pointer_Dereference;
import testcasesupport.*;
public class {stem} extends AbstractTestCase
{{
    public void bad() throws Throwable
    {{
        /* FLAW: dereference null */
        String myString = null;
        IO.writeLine("Benign, fixed string");
        IO.writeLine(myString.length() + {i});
    }}
    private void goodG2B() throws Throwable
    {{
        /* FIX: use a good source */
        String myString = "Good";
        IO.writeLine("Benign, fixed string");
        IO.writeLine(myString.length() + {i});
    }}
    private void good1() throws Throwable
    {{
        String myString = null;
        if (myString != null)
        {{
            IO.writeLine(myString.length());
        }}
    }}
    public void good() throws Throwable
    {{
        goodG2B();
        good1();
    }}
}}
"""

CSHARP = """using TestCaseSupport;
namespace testcases.CWE190_Integer_Overflow
{{
class {stem} : AbstractTestCase
{{
#if (!OMITBAD)
    public override void Bad()
    {{
        byte data = 0;
        /* POTENTIAL FLAW: overflow */
        byte result = (byte)(data + {i});
        IO.WriteLine("INT_OVERFLOW_RESULT: " + result);
    }}
#endif
#if (!OMITGOOD)
    public override void Good()
    {{
        GoodG2B();
    }}
    private void GoodG2B()
    {{
        byte data = 2;
        byte result = (byte)(data + {i});
        IO.WriteLine("result: " + result);
    }}
#endif
}}
}}
"""


def java_records(n=6):
    out = []
    for i in range(n):
        cd = CWES[i % 3]
        stem = "CWE%s__var%d_01" % (cd[3:].split("_", 1)[0], i)
        out.append({"lang": "java", "path": "Java/src/testcases/%s/%s.java" % (cd, stem), "cwe_dir": cd,
                    "base": stem[:-3], "flow": "01", "text": JAVA.format(stem=stem, i=i), "_src_line": "j%d" % i})
    return out


def csharp_records(n=6):
    out = []
    for i in range(n):
        cd = "CWE190_Integer_Overflow" if i % 2 == 0 else "CWE191_Integer_Underflow"
        stem = "CWE190_Integer_Overflow__Byte_var%d_01" % i
        out.append({"lang": "csharp", "path": "src/testcases/%s/s01/%s.cs" % (cd, stem), "cwe_dir": cd, "base": stem[:-3],
                    "flow": "01", "text": CSHARP.format(stem=stem, i=i), "_src_line": "c%d" % i})
    return out


def test_java_and_csharp_functions_found_and_classified():
    j = java_records(1)[0]
    bad, goods = J.classify_functions(J.strip_comments(j["text"]), "java", j["base"] + "_01")
    assert bad["name"] == "bad" and sorted(g["name"] for g in goods) == ["good1", "goodG2B"]
    c = csharp_records(1)[0]
    bad, goods = J.classify_functions(J.strip_comments(c["text"]), "csharp", c["base"] + "_01")
    assert bad["name"] == "Bad" and [g["name"] for g in goods] == ["GoodG2B"]


def test_three_languages_scrubbed_and_shares():
    m = J.Mapper(T.pools_for(J.Mapper), seed=1)
    recs = records(8) + java_records(6) + csharp_records(6)
    rows = m.map_records(recs)
    T.check_rows(rows, m, min_rows=30)
    by = {}
    for r in rows:
        by.setdefault(r["extra"]["lang"], []).append(r)
    assert set(by) == {"c", "java", "csharp"}
    for r in rows:
        code = r["context"]
        assert not re.search(r"bad|good|cwe|flaw|fix|benign|safe|vuln", code, re.I), code      # identifiers AND string literals
        assert "throws" not in code and "public" not in code and "override" not in code and "static" not in code
        assert code.startswith(("void handle_item(", "handle_item(")) or " handle_item(" in code.splitlines()[0]
    yn = [r for r in rows if r["form"] == J.F_YN]
    assert sum(r["answer_text"] == "Yes" for r in yn) == len(yn) // 2


def test_cwe_form_scrubs_class_words_from_strings_and_macros():
    code = 'void f() { printLine("Integer overflow detected"); int x = INT_OVERFLOW_LIMIT + OTHER_CONST; printLine("ok"); }'
    words = tuple(J.class_words("CWE-190 Integer Overflow"))
    assert words == ("integer", "overflow")
    out = J.neutralise(code, words)
    assert "Integer overflow" not in out and "INT_OVERFLOW_LIMIT" not in out and "OTHER_CONST" in out and '"ok"' in out
    # without class words (yes/no form) the macro and the string are kept
    assert "INT_OVERFLOW_LIMIT" in J.neutralise(code, ())


def test_marker_string_literal_replaced_consistently():
    out = J.neutralise('a("Benign, fixed string"); b("Benign, fixed string"); c("hello");')
    assert out.count('"str_1"') == 2 and '"hello"' in out


def test_reader_reads_each_language_zip(tmp_path):
    for lang, name, text in (("c", "C/testcases/CWE476_NULL_Pointer_Dereference/CWE476_NULL_Pointer_Dereference__char_01.c", "void x(){}"),
                              ("java", "Java/src/testcases/CWE476_NULL_Pointer_Dereference/CWE476_NULL_Pointer_Dereference__x_01.java", "class A{}"),
                              ("csharp", "src/testcases/CWE190_Integer_Overflow/s01/CWE190_Integer_Overflow__Byte_x_01.cs", "class A{}")):
        with zipfile.ZipFile(tmp_path / ("juliet_%s_train.zip" % lang), "w") as z:
            z.writestr(name, text)
            z.writestr(name.replace("_01.", "_51a."), "class B{}")           # multi-file variant, never read
    got = list(J.read_train(str(tmp_path)))
    assert sorted(g["lang"] for g in got) == ["c", "csharp", "java"] and all(g["flow"] == "01" for g in got)


def test_cwe_form_uses_files_not_used_by_vuln_form(monkeypatch):
    monkeypatch.setitem(J.RECAST_TABLE["caps"], J.F_YN, 20)
    monkeypatch.setitem(J.RECAST_TABLE["caps"], J.F_CWE, 20)
    m = J.Mapper(T.pools_for(J.Mapper), seed=1)
    rows = m.map_records(records(20))
    yn_files = {r["extra"]["pair"].replace("juliet:", "") for r in rows if r["form"] == J.F_YN}
    cw_files = {r["source_row_id"].replace("juliet:", "") for r in rows if r["form"] == J.F_CWE}
    assert yn_files and cw_files and not (yn_files & cw_files)             # T65-M1
