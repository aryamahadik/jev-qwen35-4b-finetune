"""Wikimedia sister projects (NOT Wikipedia): Wikibooks Cookbook, Wikivoyage, Wikinews.
Cookbook and Wikivoyage: page wikitext (50 pages per API call) + a regex wikitext cleaner.
Wikinews: TextExtracts intro (the whole article body sits before the first heading, "Sources").
Usage: python -I fetch_wiki.py {cookbook|voyage|news}"""
import html
import json
import random
import re
import sys
import time
import urllib.parse

sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/gblock/tools")
import common as C  # noqa: E402

DROP_SECTIONS = re.compile(r"(?i)^(see also|references|external links|sources|related news|sister links|notes|"
                           r"further reading|gallery|footnotes|bibliography|interviews?|related)$")


def api(host, **params):
    params.update({"format": "json", "formatversion": "2"})
    url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(params)
    time.sleep(1.0)
    return C.fetch_json(url)


def list_pages(host, ns):
    titles, cont = [], {}
    while True:
        d = api(host, action="query", list="allpages", apnamespace=ns, apfilterredir="nonredirects", aplimit="max",
                **cont)
        titles += [p["title"] for p in d["query"]["allpages"]]
        if "continue" not in d:
            break
        cont = {"apcontinue": d["continue"]["apcontinue"], "continue": d["continue"]["continue"]}
    return titles


def list_category(host, cat):
    titles, cont = [], {}
    while True:
        d = api(host, action="query", list="categorymembers", cmtitle=cat, cmnamespace=0, cmlimit="max",
                cmtype="page", **cont)
        titles += [p["title"] for p in d["query"]["categorymembers"]]
        if "continue" not in d:
            break
        cont = {"cmcontinue": d["continue"]["cmcontinue"], "continue": d["continue"]["continue"]}
    return titles


def wikitext(host, titles):
    out = {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        d = api(host, action="query", prop="revisions", rvprop="content", rvslots="main", titles="|".join(chunk))
        for p in d["query"].get("pages", []):
            revs = p.get("revisions") or []
            if revs:
                out[p["title"]] = {"pageid": p.get("pageid"), "wikitext": revs[0]["slots"]["main"]["content"]}
        if (i // 50) % 10 == 0:
            print(f"  {host}: {i + len(chunk)}/{len(titles)}", flush=True)
    return out


def intro_extracts(host, titles):
    out = {}
    for i in range(0, len(titles), 20):
        chunk = titles[i:i + 20]
        d = api(host, action="query", prop="extracts", exintro=1, explaintext=1, exlimit=20, titles="|".join(chunk))
        for p in d["query"].get("pages", []):
            if p.get("extract"):
                out[p["title"]] = {"pageid": p.get("pageid"), "extract": p["extract"]}
        if (i // 20) % 25 == 0:
            print(f"  {host}: {i + len(chunk)}/{len(titles)}, {len(out)} with text", flush=True)
    return out


def from_dump(wiki, pred, cap, seed):
    """Sample up to `cap` main-namespace, non-redirect pages from the local XML dump (raw/dumps/), keeping those
    whose wikitext passes `pred`. Pages are drawn by a seeded hash order (deterministic)."""
    import bz2
    import hashlib
    import xml.etree.ElementTree as ET
    path = C.RAW / "dumps" / f"{wiki}-latest-pages-articles.xml.bz2"
    keep = []
    with bz2.open(path, "rb") as f:
        title = pid = ns = text = None
        redirect = False
        for ev, el in ET.iterparse(f, events=("end",)):
            tag = el.tag.rsplit("}", 1)[-1]
            if tag == "title":
                title = el.text
            elif tag == "ns":
                ns = el.text
            elif tag == "id" and pid is None:
                pid = el.text
            elif tag == "redirect":
                redirect = True
            elif tag == "text":
                text = el.text or ""
            elif tag == "page":
                if ns == "0" and not redirect and text and pred(title, text):
                    h = hashlib.sha1(f"{seed}:{title}".encode()).hexdigest()
                    keep.append((h, {"title": title, "pageid": int(pid) if pid else None, "wikitext": text}))
                title = pid = ns = text = None
                redirect = False
                el.clear()
    keep.sort(key=lambda x: x[0])
    print(f"  {wiki}: {len(keep)} pages pass the filter; keeping {min(cap, len(keep))}", flush=True)
    return [r for _, r in keep[:cap]]


# ------------------------------------------------------------------ wikitext -> plain text
LINK_TPL = re.compile(r"(?i)^(w|wp|wikipedia|wiktionary|wikt|cookbook|lang|nowrap|nobr|smallcaps|small|big|"
                      r"marker|iata|station|rint|flag|ingredient|cookbook:[^|]*)$")


def _strip_templates(s):
    for _ in range(12):
        new = re.sub(r"\{\{([^{}]*)\}\}", _tpl_repl, s)
        if new == s:
            break
        s = new
    return s


GAP = "\u27c2"   # sentinel for a removed template; a sentence that contains one is dropped (no broken sentences)


def _tpl_repl(m):
    parts = m.group(1).split("|")
    name = parts[0].strip()
    lname = name.lower()
    if lname in ("convert", "cvt") and len(parts) >= 3:
        a = [x.strip() for x in parts[1:] if "=" not in x]
        if len(a) >= 4 and a[1] in ("-", "to", "–", "and", "and(-)", "or"):
            return f"{a[0]}{'–' if a[1] in ('-', '–') else ' ' + a[1] + ' '}{a[2]} {a[3]}"
        return f"{a[0]} {a[1]}" if len(a) >= 2 else GAP
    if LINK_TPL.match(name) and len(parts) >= 2:
        args = [a for a in parts[1:] if "=" not in a]
        if name.lower() == "marker":
            named = dict(a.split("=", 1) for a in parts[1:] if "=" in a)
            return named.get("name", "").strip()
        return args[-1].strip() if args else GAP
    return GAP


def _strip_tables(s):
    for _ in range(6):
        new = re.sub(r"(?s)\{\|(?:(?!\{\|).)*?\|\}", "", s)
        if new == s:
            break
        s = new
    return s


def _strip_links(s):
    # files / categories / interwiki (with nested links inside captions)
    for _ in range(4):
        s = re.sub(r"(?is)\[\[(file|image|category|media|[a-z]{2,3}(-[a-z]+)?):(?:[^\[\]]|\[\[[^\[\]]*\]\])*\]\]", "", s)
    s = re.sub(r"\[\[([^\[\]|]*)\|([^\[\]]*)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\[\]]*)\]\]", lambda m: m.group(1).split(":")[-1].split("#")[0], s)
    s = re.sub(r"\[(?:https?:)?//[^\s\]]+\s+([^\]]+)\]", r"\1", s)
    s = re.sub(r"\[(?:https?:)?//[^\]]+\]", "", s)
    return s


def wiki_to_text(w):
    s = re.sub(r"(?s)<!--.*?-->", "", w)
    s = re.sub(r"(?is)<ref[^>/]*/>", "", s)
    s = re.sub(r"(?is)<ref[^>]*>.*?</ref>", "", s)
    for tag in ("gallery", "math", "syntaxhighlight", "source", "pre", "timeline", "noinclude", "score", "imagemap",
                "templatedata", "code", "poem"):
        s = re.sub(rf"(?is)<{tag}[^>]*>.*?</{tag}>", "", s)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = _strip_templates(s)
    s = _strip_tables(s)
    s = _strip_links(s)
    s = re.sub(r"'{2,5}", "", s)
    s = re.sub(r"__[A-Z]+__", "", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    lines = []
    for ln in s.split("\n"):
        ln = ln.rstrip()
        if re.match(r"^\s*[\*#]+", ln):
            ln = "- " + re.sub(r"^\s*[\*#:;]+\s*", "", ln)
        elif re.match(r"^\s*[:;]+", ln):
            ln = re.sub(r"^\s*[:;]+\s*", "", ln)
        if re.fullmatch(r"-\s*", ln):
            continue
        lines.append(ln)
    s = "\n".join(lines)
    out = []
    for ln in s.split("\n"):
        if GAP in ln:
            if not re.sub(rf"[{GAP}\s\W]", "", ln):
                continue                                  # a line that was only templates
            if re.match(r"^\s*=", ln):
                ln = ln.replace(GAP, "")
            else:
                pre = re.match(r"^(- )", ln)
                sents = [st for st in C._SENT.split(ln) if GAP not in st]
                if not sents:
                    continue
                ln = " ".join(sents)
                if pre and not ln.startswith("- "):
                    ln = "- " + ln
        out.append(ln)
    s = "\n".join(out)
    s = re.sub(r"\(\s*[,;]?\s*\)", "", s)
    s = re.sub(r" +([,.;:])", r"\1", s)
    return C.clean_ws(s)


def sections(text):
    """[(heading, body)] with the lead as heading ''."""
    parts = re.split(r"(?m)^(={2,6})\s*(.*?)\s*\1\s*$", text)
    out = [("", parts[0])]
    for j in range(1, len(parts), 3):
        out.append((parts[j + 1].strip(), parts[j + 2] if j + 2 < len(parts) else ""))
    return [(h, C.clean_ws(b)) for h, b in out]


# ------------------------------------------------------------------ sources
def cookbook():
    host = "en.wikibooks.org"
    raw = C.load_raw("wikibooks_cookbook")
    if raw is None:
        titles = list_pages(host, 102)
        print("cookbook pages:", len(titles), flush=True)
        wt = wikitext(host, titles)
        raw = [{"title": t, **v} for t, v in wt.items()]
        C.save_raw("wikibooks_cookbook", raw)
    items = []
    for r in raw:
        if re.search(r"(?i)\{\{\s*(delete|speedy|cleanup|stub)", r["wikitext"]):
            continue
        secs = sections(wiki_to_text(r["wikitext"]))
        heads = [h.lower() for h, _ in secs]
        if not any(h.startswith("ingredient") for h in heads):
            continue
        if not any(h.startswith(("procedure", "preparation", "method", "direction", "instruction", "steps"))
                   for h in heads):
            continue
        parts = []
        for h, b in secs:
            if not b or DROP_SECTIONS.match(h):
                continue
            parts.append((h + ":\n" if h else "") + b)
        title = r["title"].split(":", 1)[-1]
        body = "\n".join(parts)
        cats = [c.strip() for ln in body.split("\n") if ln.lstrip().startswith("|")
                for c in ln.split("|") if c.strip()]
        body = "\n".join(ln for ln in body.split("\n") if not ln.lstrip().startswith("|"))
        items.append({"key": r["title"], "text": f"{title}\n" + body,
                      "meta": {"title": r["title"], "pageid": r.get("pageid"), "page_categories": cats}})
    print("recipe pages:", len(items))
    st = C.finish("recipes", "Wikibooks Cookbook (en.wikibooks.org, Cookbook namespace)",
                  "https://creativecommons.org/licenses/by-sa/4.0/", items)
    print(json.dumps(st))


PROSE = re.compile(r"(?i)^(understand|history|climate|get in|get around|stay safe|stay healthy|respect|cope|talk|"
                   r"connect|see|do|buy|eat|drink|sleep|orient|landscape|people|culture|by plane|by train|"
                   r"by bus|by car|by boat|prepare|tourist information|holidays|flora and fauna|"
                   r"visitor information|fees and permits|when to go)$")


def voyage():
    host = "en.wikivoyage.org"
    raw = C.load_raw("wikivoyage")
    if raw is None:
        raw = from_dump("enwikivoyage", lambda t, w: True, 7000, 2)
        C.save_raw("wikivoyage", raw)
    rng = random.Random(3)
    items = []
    for r in raw:
        if re.search(r"(?i)\{\{\s*(disamb|vfd|stub|title-index)", r["wikitext"]):
            continue
        cands = []
        for h, b in sections(wiki_to_text(r["wikitext"])):
            if not b or not (h == "" or PROSE.match(h)):
                continue
            paras = [p for p in b.split("\n") if p and not p.lstrip().startswith("-") and C.nwords(p) >= 8]
            body = "\n".join(paras)
            if 40 <= C.nwords(body) <= 600:
                cands.append((h, body))
        if not cands:
            continue
        h, body = rng.choice(cands)
        head = r["title"] + (f" - {h}" if h else "")
        items.append({"key": f"{r['title']}#{h}", "text": f"{head}\n{body}",
                      "meta": {"title": r["title"], "section": h, "pageid": r.get("pageid")}})
    print("voyage passages:", len(items))
    st = C.finish("travel", "Wikivoyage (en.wikivoyage.org)", "https://creativecommons.org/licenses/by-sa/4.0/", items)
    print(json.dumps(st))


def news():
    host = "en.wikinews.org"
    raw = C.load_raw("wikinews")
    if raw is None:
        raw = from_dump("enwikinews", lambda t, w: re.search(r"(?i)\{\{\s*publish", w) is not None, 6000, 4)
        C.save_raw("wikinews", raw)
    items = []
    for r in raw:
        body = re.split(r"(?m)^==\s*(sources|related news|external links|see also)\s*==", r["wikitext"],
                        flags=re.I)[0]
        txt = wiki_to_text(body)
        txt = "\n".join(p for p in txt.split("\n") if not re.match(r"^(Monday|Tuesday|Wednesday|Thursday|Friday|"
                                                                   r"Saturday|Sunday),", p))
        dm = re.search(r"\{\{\s*date\s*\|\s*([A-Za-z]+ \d{1,2},? \d{4})", r["wikitext"], re.I)
        pub = None
        if dm:
            from datetime import datetime
            for fmt in ("%B %d, %Y", "%B %d %Y"):
                try:
                    pub = datetime.strptime(dm.group(1), fmt).date().isoformat()
                    break
                except ValueError:
                    pass
        if pub and pub < "2005-09-25":
            lic = "https://en.wikinews.org/wiki/Wikinews:Copyright (public domain: published before 2005-09-25)"
        elif pub and pub > "2024-12-16":
            lic = "https://creativecommons.org/licenses/by/4.0/"
        else:
            lic = "https://creativecommons.org/licenses/by/2.5/"
        items.append({"key": r["title"], "text": f"{r['title']}\n{txt}", "licence_url": lic,
                      "meta": {"title": r["title"], "pageid": r.get("pageid"), "published": pub}})
    st = C.finish("news", "Wikinews (en.wikinews.org, published articles)",
                  "per article date (Wikinews:Copyright)", items, drop_fn=C.private_person_risk)
    print(json.dumps(st))


SKIP_V = re.compile(r"(?i)^(quiz|assignments?|activities|exercises?|readings?|resources|links|discussion|"
                    r"see also|references|external links|further reading|notes|bibliography|sources|footnotes|"
                    r"navigation|contents|syllabus|schedule|course outline|lessons?|related|categories)$")


def versity():
    host = "en.wikiversity.org"
    raw = C.load_raw("wikiversity")
    if raw is None:
        raw = from_dump("enwikiversity", lambda t, w: t.count("/") <= 2 and len(w) > 800, 12000, 8)
        C.save_raw("wikiversity", raw)
    rng = random.Random(9)
    items = []
    for r in raw:
        if re.search(r"(?i)\{\{\s*(delete|speedy|proposed deletion|disambig|stub|draft|test)", r["wikitext"]):
            continue
        if re.search(r"(?i)<quiz|\{\|", r["wikitext"][:2000]) and C.nwords(r["wikitext"]) < 300:
            continue
        cands = []
        for h, b in sections(wiki_to_text(r["wikitext"])):
            if not b or SKIP_V.match(h):
                continue
            paras = [p for p in b.split("\n") if p and not p.lstrip().startswith("-") and C.nwords(p) >= 12
                     and not re.search(r"[{}|=<>]", p)]
            body = "\n".join(paras)
            if 40 <= C.nwords(body) <= 600:
                cands.append((h, body))
        if not cands:
            continue
        h, body = rng.choice(cands)
        head = r["title"].split("/")[-1] + (f" - {h}" if h else "")
        items.append({"key": f"{r['title']}#{h}", "text": f"{head}\n{body}",
                      "meta": {"title": r["title"], "section": h, "pageid": r.get("pageid")}})
    print("wikiversity passages:", len(items))
    st = C.finish("learning", "Wikiversity learning resources (en.wikiversity.org)",
                  "https://creativecommons.org/licenses/by-sa/4.0/", items, drop_fn=C.private_person_risk)
    print(json.dumps(st))


if __name__ == "__main__":
    {"cookbook": cookbook, "voyage": voyage, "news": news, "versity": versity}[sys.argv[1]]()
