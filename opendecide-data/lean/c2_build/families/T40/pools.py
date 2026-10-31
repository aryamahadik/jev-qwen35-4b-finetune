"""families/T40/pools.py: tool domains (typed parameter templates), naming styles and value pools for T40 CALL-GATE.

A tool is one line of a tiny DSL: (verb, noun, purpose, "param; param; ..."), a param is "words:type:label" with a
trailing * on the words when required. Types: city, email, date, path, slug, text(<pool>), int(lo,hi), num(lo,hi),
enum(a,b,c), id(prefix_). Registries are generated programmatically from these templates (never hand-written rows).
Held out for the sealed split (S5): HELD_OUT_DOMAINS and HELD_OUT_STYLES. Nothing here is gold.
"""
from __future__ import annotations

import re

DOMAINS = {
    "weather": (("skyhub", "meteo", "windly"), (
        ("get", "forecast", "look up the forecast", "city*:city:city to check; days:int(1,7):number of days; units:enum(metric,imperial):unit system"),
        ("get", "alerts", "check weather alerts", "region*:text(place):region to watch; level:enum(minor,major,severe):alert level"),
        ("get", "history", "pull the weather history", "city*:city:city to review; start*:date:first day; end*:date:last day"),
        ("set", "alarm", "schedule a weather alarm", "city*:city:city to monitor; threshold*:num(0,60):trigger value; channel:enum(sms,push,mail):delivery channel"),
        ("list", "stations", "list the nearby stations", "city*:city:city to search near; limit:int(1,20):station limit"))),
    "mail": (("postbox", "letterly", "mailroom"), (
        ("send", "email", "send an email message", "to*:email:recipient address; subject*:text(subject):subject line; body*:text(body):message text; cc:email:copy address"),
        ("read", "inbox", "read the inbox", "folder*:enum(inbox,sent,drafts):folder name; limit:int(1,50):message limit"),
        ("search", "mail", "search the mailbox", "query*:text(subject):search words; since:date:earliest date"),
        ("delete", "draft", "discard a draft", "draft id*:id(drf_):draft number"),
        ("add", "label", "tag a message", "message id*:id(msg_):message number; label*:enum(urgent,billing,travel,personal):tag name"))),
    "calendar": (("calsync", "agendo", "timely"), (
        ("create", "event", "create a calendar event", "title*:text(title):event title; start*:date:start date; days:int(1,30):length in days; room:text(room):meeting room"),
        ("list", "events", "list the events", "from*:date:range start; to*:date:range end"),
        ("cancel", "event", "remove a calendar event", "event id*:id(evt_):event number"),
        ("invite", "guest", "invite a guest", "event id*:id(evt_):event number; guest*:email:guest address"),
        ("move", "event", "reschedule an event", "event id*:id(evt_):event number; new start*:date:new start date"))),
    "tickets": (("deskly", "tracker", "supportly"), (
        ("open", "ticket", "file a support ticket", "title*:text(title):ticket title; severity*:enum(low,medium,high):severity level; reporter:email:reporter address"),
        ("close", "ticket", "close a support ticket", "ticket id*:id(tkt_):ticket number; reason:text(reason):closing note"),
        ("assign", "ticket", "assign a support ticket", "ticket id*:id(tkt_):ticket number; owner*:email:owner address"),
        ("comment", "ticket", "add a ticket comment", "ticket id*:id(tkt_):ticket number; text*:text(note):comment text"),
        ("list", "tickets", "list open tickets", "queue*:enum(billing,tech,sales):queue name; limit:int(1,100):ticket limit"))),
    "files": (("vaultfs", "diskly", "stash"), (
        ("read", "file", "read a stored file", "path*:path:file path; max lines:int(1,500):line limit"),
        ("write", "file", "write a stored file", "path*:path:file path; content*:text(body):file content"),
        ("delete", "file", "delete a stored file", "path*:path:file path"),
        ("copy", "file", "copy a stored file", "source*:path:source path; target*:path:target path"),
        ("list", "folder", "list a folder", "folder*:path:folder path; depth:int(1,5):folder depth"))),
    "crm": (("leadnest", "cliently", "dealbox"), (
        ("create", "contact", "create a contact record", "name*:text(person):full name; email*:email:email address; company:text(org):company name"),
        ("find", "contact", "find a contact record", "name*:text(person):full name"),
        ("update", "stage", "move a deal stage", "deal id*:id(dl_):deal number; stage*:enum(lead,qualified,proposal,closed):stage name"),
        ("log", "call", "log a sales call", "contact id*:id(ct_):contact number; minutes*:int(1,240):call length; note:text(note):call summary"),
        ("list", "deals", "list the deals", "stage*:enum(lead,qualified,proposal,closed):stage name; limit:int(1,50):deal limit"))),
    "payments": (("paywave", "coinly", "ledgerpay"), (
        ("create", "invoice", "create an invoice", "customer id*:id(cus_):customer number; amount*:num(1,5000):invoice amount; due*:date:due date; memo:text(note):invoice memo"),
        ("refund", "payment", "refund a payment", "payment id*:id(pay_):payment number; amount:num(1,5000):refund amount"),
        ("get", "balance", "check an account balance", "account id*:id(acc_):account number"),
        ("list", "charges", "list recent charges", "customer id*:id(cus_):customer number; limit:int(1,50):charge limit"),
        ("void", "invoice", "void an invoice", "invoice id*:id(inv_):invoice number; reason:text(reason):void reason"))),
    "travel": (("tripmate", "airly", "stayhub"), (
        ("search", "flights", "search for flights", "origin*:city:departure city; destination*:city:arrival city; day*:date:travel date; seats:int(1,9):seat count"),
        ("book", "flight", "book a flight", "offer id*:id(ofr_):offer number; passenger*:text(person):passenger name"),
        ("search", "hotels", "search for hotels", "city*:city:city to stay in; check in*:date:arrival date; nights*:int(1,30):night count"),
        ("cancel", "booking", "cancel a booking", "booking id*:id(bkg_):booking number"),
        ("rent", "car", "reserve a rental car", "city*:city:pickup city; start*:date:pickup date; days*:int(1,30):rental length"))),
    "music": (("tunebox", "wavely", "songhub"), (
        ("play", "track", "play a track", "track*:text(song):track title; volume:int(0,100):volume level"),
        ("queue", "album", "queue an album", "album*:text(album):album title"),
        ("create", "playlist", "create a playlist", "name*:text(playlist):playlist name; mood:enum(calm,upbeat,focus):mood tag"),
        ("skip", "song", "skip the song", "count*:int(1,10):skip count"),
        ("rate", "track", "rate a track", "track id*:id(trk_):track number; stars*:int(1,5):star rating"))),
    "inventory": (("stockly", "warehub", "binrack"), (
        ("check", "stock", "check the stock level", "sku*:id(sku_):item code; site:enum(north,south,east,west):warehouse site"),
        ("add", "stock", "receive new stock", "sku*:id(sku_):item code; quantity*:int(1,1000):unit count"),
        ("move", "stock", "transfer stock between sites", "sku*:id(sku_):item code; quantity*:int(1,1000):unit count; to site*:enum(north,south,east,west):destination site"),
        ("reorder", "item", "place a reorder", "sku*:id(sku_):item code; quantity*:int(1,1000):unit count; supplier:text(org):supplier name"),
        ("count", "shelf", "record a shelf count", "shelf*:id(shl_):shelf number; counted*:int(0,1000):counted units"))),
    "hr": (("peoplely", "staffbase", "hrwave"), (
        ("request", "leave", "request time off", "employee*:email:staff address; start*:date:first day off; days*:int(1,30):days off"),
        ("approve", "leave", "sign off a leave request", "request id*:id(lv_):request number"),
        ("lookup", "staff", "look up a staff profile", "email*:email:staff address"),
        ("post", "job", "post a job opening", "title*:text(title):job title; site*:enum(north,south,east,west):office site; salary:num(20000,200000):salary figure"),
        ("update", "title", "change a staff title", "employee*:email:staff address; title*:text(title):new title"))),
    "git": (("codehub", "gitly", "forgebox"), (
        ("open", "issue", "open a repository issue", "repo*:slug:repo name; title*:text(title):issue title; labels:enum(bug,docs,idea):issue label"),
        ("merge", "branch", "merge a branch", "repo*:slug:repo name; branch*:slug:branch name"),
        ("list", "commits", "list the commits", "repo*:slug:repo name; limit:int(1,100):commit limit"),
        ("tag", "release", "tag a release", "repo*:slug:repo name; version*:id(v_):release tag"),
        ("close", "issue", "close a repository issue", "repo*:slug:repo name; issue*:int(1,9999):issue number"))),
    "analytics": (("datacube", "querybox", "tablely"), (
        ("run", "query", "run a saved query", "query id*:id(qry_):query number; rows:int(1,1000):row limit"),
        ("export", "table", "export a table", "table*:slug:table name; format*:enum(csv,json,parquet):file format"),
        ("create", "table", "create a table", "table*:slug:table name; columns*:int(1,50):column count"),
        ("drop", "table", "drop a table", "table*:slug:table name"),
        ("refresh", "view", "refresh a view", "view*:slug:view name"))),
    # held out for the sealed split (S5 only)
    "shipping": (("portlink", "cargoly", "shipnet"), (
        ("track", "parcel", "track a parcel", "parcel id*:id(prc_):parcel number"),
        ("book", "freight", "book freight space", "origin*:city:origin port; destination*:city:destination port; tons*:num(1,500):cargo weight"),
        ("print", "label", "print a shipping label", "parcel id*:id(prc_):parcel number; size:enum(small,medium,large):label size"),
        ("reroute", "parcel", "reroute a parcel", "parcel id*:id(prc_):parcel number; destination*:city:new port"),
        ("quote", "rate", "quote a shipping rate", "origin*:city:origin port; destination*:city:destination port; tons:num(1,500):cargo weight"))),
    "astronomy": (("starwatch", "orbitly", "skyatlas"), (
        ("schedule", "scope", "schedule a telescope session", "target*:text(body_obj):target object; night*:date:observing night; hours:int(1,12):session length"),
        ("fetch", "catalog", "fetch a star catalog", "catalog*:slug:catalog name; limit:int(1,500):row limit"),
        ("predict", "transit", "predict a planet transit", "planet*:text(body_obj):planet name; from*:date:window start; to*:date:window end"),
        ("log", "sighting", "log a sky sighting", "target*:text(body_obj):target object; magnitude*:num(0,20):brightness value"),
        ("cancel", "session", "cancel a telescope session", "session id*:id(ses_):session number"))),
    "veterinary": (("petcare", "vetline", "clinicly"), (
        ("book", "visit", "book a vet visit", "pet*:text(pet):pet name; day*:date:visit date; reason:text(reason):visit reason"),
        ("record", "dose", "record a medicine dose", "pet id*:id(pet_):pet number; drug*:enum(amoxil,rimadyl,cerenia):drug name; mg*:num(1,500):dose size"),
        ("lookup", "owner", "look up a pet owner", "pet id*:id(pet_):pet number"),
        ("send", "reminder", "send a vaccine reminder", "owner*:email:owner address; vaccine*:enum(rabies,distemper,bordetella):vaccine name"),
        ("cancel", "visit", "cancel a vet visit", "visit id*:id(vis_):visit number"))),
    "library": (("booknook", "shelfwise", "readly"), (
        ("find", "book", "find a book", "title*:text(book):book title; author:text(person):author name"),
        ("borrow", "book", "borrow a book", "book id*:id(bk_):book number; member*:email:member address"),
        ("return", "book", "return a book", "book id*:id(bk_):book number"),
        ("renew", "loan", "renew a loan", "loan id*:id(ln_):loan number; days:int(1,28):extra days"),
        ("reserve", "room", "reserve a study room", "room*:enum(alpha,beta,gamma):room name; day*:date:booking date; hours*:int(1,8):hour count"))),
}
HELD_OUT_DOMAINS = ("shipping", "astronomy", "veterinary", "library")
TRAIN_DOMAINS = tuple(d for d in DOMAINS if d not in HELD_OUT_DOMAINS)

STYLES = ("snake_vn", "snake_nv", "camel_vn", "pascal_vn", "dotted_vn", "camel_nv", "dotted_nv", "kebab_vn")
HELD_OUT_STYLES = ("camel_nv", "dotted_nv", "kebab_vn")
TRAIN_STYLES = tuple(s for s in STYLES if s not in HELD_OUT_STYLES)

# purposes no registry tool offers: out-of-world ones (domain-near ones are drawn from tools left out of a registry)
UNSUPPORTED = ("translate a contract", "water the office plants", "order lunch for the team", "tune a guitar",
               "paint the garden fence", "predict next season sales", "knit a scarf", "repair a bicycle tire",
               "schedule a window cleaning", "compose a poem", "sharpen the kitchen knives", "walk the dog",
               "bake a sourdough loaf", "design a company logo", "organise the garage", "polish the trophies")

CITIES = ("Lisbon", "Porto", "Oslo", "Bergen", "Kyoto", "Osaka", "Quito", "Lima", "Nairobi", "Accra", "Hanoi", "Hue",
          "Perth", "Darwin", "Tallinn", "Riga", "Split", "Zadar", "New Haven", "Santa Cruz", "Cape Town",
          "Buenos Aires", "Addis Ababa", "Santa Fe")
FIRST = ("ana", "ben", "chloe", "dev", "elif", "femi", "gus", "hana", "ivan", "joy", "kofi", "lena")
LAST = ("ruiz", "okoye", "marsh", "patel", "kaya", "adeyemi", "lindqvist", "sato", "petrov", "quinn")
ORGS = ("lab", "harbor", "redwood", "summit", "northwind", "bluebird")
SLUGS = ("orbit-api", "lumen-docs", "atlas-web", "pixel-forge", "sales-daily", "user-events", "orders-raw",
         "metrics-hourly", "billing-core", "search-index")
PATHS = ("reports/summary.txt", "notes/plan.md", "data/orders.csv", "docs/guide.md", "logs/app.log", "backup/old.zip",
         "drafts/letter.txt", "assets/logo.png", "exports/month.csv", "config/app.yaml")
TEXTS = {
    "subject": ("Budget review", "Quarterly plan", "Team offsite", "Contract draft", "Launch checklist", "Travel notes",
                "Vendor intro", "Weekly sync", "Hiring update", "Press kit"),
    "body": ("Draft attached for review", "Please confirm the schedule", "Notes from the meeting", "The report is ready",
             "See the summary below", "Thanks for the quick reply", "Here is the updated outline", "Details follow"),
    "title": ("Printer jams again", "Login page slow", "Update the guide", "Sync with finance", "Plan the demo",
              "Refresh the slides", "Fix the footer", "Review the budget", "Order new badges", "Tidy the wiki"),
    "place": ("Northern coast", "Inland valley", "Harbor district", "Mountain pass", "River delta", "Salt flats"),
    "person": ("Ana Ruiz", "Ben Okoye", "Chloe Marsh", "Dev Patel", "Elif Kaya", "Femi Adeyemi", "Gus Lindqvist",
               "Hana Sato"),
    "org": ("Northwind Labs", "Blue Harbor", "Redwood Works", "Pine Street Co", "Summit Foods", "Cedar Freight"),
    "song": ("Morning Light", "Slow River", "Paper Boats", "Night Train", "Glass Garden", "Copper Hills"),
    "album": ("Quiet Hours", "Long Roads", "Small Fires", "Open Water", "Tin Rooftops"),
    "playlist": ("Road trip mix", "Sunday morning", "Deep work", "Evening wind down", "Gym warmup"),
    "note": ("Called back after lunch", "Needs a follow up", "Waiting on the vendor", "Sent the quote",
             "Left a voicemail", "Shared the agenda"),
    "reason": ("Duplicate entry", "Customer request", "Filed in error", "Resolved by phone", "Moved to another team"),
    "room": ("Atrium", "Cedar room", "Harbor room", "Studio B", "Garden room"),
    "body_obj": ("Vega", "Mizar", "Kepler Prime", "Rigel", "Altair", "Deneb"),
    "pet": ("Biscuit", "Maple", "Otto", "Juno", "Pepper", "Ziggy"),
    "book": ("The Quiet Orchard", "River of Salt", "Maps of Rain", "A Garden Atlas", "Winter Ledger"),
}

BAD_ENUM = ("kelvin", "purple", "other", "auto", "legacy", "custom", "default")

_NUMERIC = re.compile(r"-?\d+(?:\.\d+)?")


def numeric_token(tok: str) -> bool:
    return _NUMERIC.fullmatch(tok) is not None


def words_to_name(words: str, style: str, *, param: bool = False) -> str:
    """Identifier for a space-separated word list in a naming style (params: snake / camel only)."""
    ws = words.split()
    camel = style.startswith(("camel", "pascal"))
    if param:
        return ws[0] + "".join(w.capitalize() for w in ws[1:]) if camel else "_".join(ws)
    return "_".join(ws)


def tool_name(verb: str, noun: str, style: str, ns: str) -> str:
    v, n = verb, noun
    if style == "snake_vn":
        return f"{v}_{n}"
    if style == "snake_nv":
        return f"{n}_{v}"
    if style == "camel_vn":
        return v + n.capitalize()
    if style == "camel_nv":
        return n + v.capitalize()
    if style == "pascal_vn":
        return v.capitalize() + n.capitalize()
    if style == "dotted_vn":
        return f"{ns}.{v}_{n}"
    if style == "dotted_nv":
        return f"{ns}.{n}.{v}"
    if style == "kebab_vn":
        return f"{v}-{n}"
    raise ValueError(style)


def parse_params(spec: str) -> list:
    out = []
    for part in [p.strip() for p in spec.split(";") if p.strip()]:
        words, typ, label = [x.strip() for x in part.split(":", 2)]
        req = words.endswith("*")
        out.append({"words": words.rstrip("*").strip(), "type": typ, "label": label, "req": req})
    return out


def type_schema(typ: str) -> dict:
    """JSON-schema of a DSL type."""
    if typ in ("city", "path", "slug") or typ.startswith("text("):
        return {"type": "string"}
    if typ == "email":
        return {"type": "string", "format": "email"}
    if typ == "date":
        return {"type": "string", "format": "date"}
    m = re.fullmatch(r"(int|num)\((-?\d+),(-?\d+)\)", typ)
    if m:
        return {"type": "integer" if m.group(1) == "int" else "number", "minimum": int(m.group(2)),
                "maximum": int(m.group(3))}
    m = re.fullmatch(r"enum\(([^)]*)\)", typ)
    if m:
        return {"type": "string", "enum": m.group(1).split(",")}
    m = re.fullmatch(r"id\(([a-z]+_)\)", typ)
    if m:
        return {"type": "string", "pattern": f"^{m.group(1)}[0-9]+$"}
    raise ValueError(f"type {typ!r}")
