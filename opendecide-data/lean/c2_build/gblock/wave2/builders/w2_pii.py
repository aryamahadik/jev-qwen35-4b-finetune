#!/usr/bin/env python3
"""W2: PII presence by type in real G-block texts (PREREG_FINAL A40 b). Gold = PROGRAM. CPU only; no network.

Each row asks one yes/no question "does this text contain <type>?" about one real G-block text (the W2 pool, see
common.pool_of), with the type defined on the card. The program decides the gold by what it inserted:
  inserted   (gold 1)  one synthetic, clearly fake PII item of the asked type, in a carrier sentence that ties it to a
                       made-up person, is inserted at the start, middle or end of the text;
  lookalike  (gold 0)  a look-alike of the asked type is inserted instead: an organisation's public contact line
                       (shared inbox, front-desk or booking phone line, venue or office address, published donation
                       account), or a code in the same shape (part / lot / catalogue numbers, tracking numbers, ISBNs,
                       booking references, version numbers, non-birth dates);
  cross      (gold 0)  a PII item of ANOTHER type is inserted (it must not fire the asked type's detector);
  none       (gold 0)  the text unchanged.
A text is only used for a type when that type's loose detector finds nothing in it (so "none" means none), and each
text is used once in W2. Per type: 50% inserted, 20% lookalike, 15% cross, 15% none (balanced yes/no).

Fake values: emails on reserved domains (RFC 2606 / 6761: example.com/.net/.org, *.example, *.test); phone numbers in
fictional ranges (US 555-0100..0199, UK Ofcom drama 07700 900xxx and 020 7946 0xxx, AU 0491 570 1xx); SSNs in
never-issued ranges (area 900-999 with group 01-49); payment cards = published test numbers or Luhn-valid numbers on
the 400000 test prefix; IPs in documentation ranges (192.0.2/24, 198.51.100/24, 203.0.113/24, 2001:db8::/32); IBANs
with a fictional bank code and a valid checksum, or the published documentation examples; made-up names and streets.

  ../../../../../.venv/bin/python -I builders/w2_pii.py [--per-type 190] [--dry-run]
"""
from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from builders import common as C  # noqa: E402

T = "W2"
PER_TYPE = 190
SHARES = (("inserted", 0.50), ("lookalike", 0.20), ("cross", 0.15), ("none", 0.15))
MIN_W, MAX_W = 40, 320

# ------------------------------------------------------------------------------------------------ fake material

FIRST = ("Dana Jordan Priya Mateo Aisha Tomasz Keiko Lars Amara Diego Hannah Omar Mei Lucas Fatima Noah Ingrid Ravi "
         "Chloe Kwame Sofia Ethan Leila Marcus Yuki Elena Samir Grace Felix Nadia Owen Zara Hugo Ana Tariq Mila Rory "
         "Ines Darius Lena Malik Rosa Theo Anika Joel Beatriz Ivan Clara Kofi Maren Arjun Sara Emil Talia Bruno "
         "Nora Kai Leah Viktor Esme").split()
LAST = ("Reyes Okafor Lindqvist Moreau Haddad Kowalski Tanaka Brennan Mensah Alvarez Schultz Patel Nakamura Fischer "
        "Dubois Rahman Costa Novak Byrne Achterberg Petrov Osei Hughes Ferreira Lindgren Castillo Abara Whitlock "
        "Vasquez Holm Delacroix Mbeki Sorensen Quint Ashby Romero Kaur Fairbanks Iqbal Larsen Pereira Oduya Marsh "
        "Kimura Bellamy Ortega Strand Varga Nwosu Calloway Ishikawa Rourke Halvorsen Mendes Dunmore Szabo").split()
STREETS = ("Alder Brookside Juniper Larkspur Wren Copperbeech Hollins Fernhill Marigold Ashcombe Thistle Kestrel "
           "Willowmere Quarry Orchard Bramble Linden Heron Saltmarsh Foxglove Tamarind Cobble Millrace Sorrel").split()
SUFFIX = ("Lane", "Way", "Court", "Drive", "Road", "Street", "Close", "Terrace", "Avenue", "Place")
TOWNS = ("Fairhollow", "Brackenridge", "East Wendover", "Kestrel Bay", "Millbrook Falls", "Ashgrove", "Port Ellery",
         "Halden Cross", "Northmere", "Saltcombe Vale", "Thornbury Green", "Westlake Hollow", "Larchmont Ridge",
         "Cinder Hill", "Ravensworth", "Oakhurst Springs")
STATES = ("NY", "OH", "OR", "TX", "VT", "WA", "CO", "MN", "GA", "AZ")
VENUES = ("Riverside Community Hall", "Northgate Public Library", "Oak Hollow Visitor Centre", "Maple Street Market Hall",
          "Harbour View Arts Centre", "Linden Park Pavilion", "Eastside Recreation Center", "Old Mill Heritage Museum",
          "Cedar Ridge Nature Center", "Town Square Civic Centre", "Brookfield Youth Club", "Southbank Learning Hub")
ORGS = ("Friends of Linden Park", "Riverside Food Bank", "Northgate Library Trust", "Harbour Arts Collective",
        "Cedar Ridge Conservancy", "Eastside Youth Football Club", "Old Mill Heritage Society", "Brookfield Tenants Union")
EMAIL_DOMAINS = ("example.com", "example.net", "example.org", "mail.example", "inbox.test", "post.example",
                 "webmail.example", "home.test")
ROLE_LOCAL = ("info", "help", "bookings", "events", "volunteer", "press", "office", "support", "hello", "enquiries",
              "admissions", "frontdesk", "team", "contact")
MONTHS = ("January February March April May June July August September October November December").split()
TEST_CARDS = ("4111 1111 1111 1111", "4242 4242 4242 4242", "4012 8888 8888 1881", "4000 0566 5566 5556",
              "5555 5555 5555 4444", "5105 1051 0510 5100", "2223 0031 2200 3222", "5200 8282 8282 8210",
              "3782 822463 10005", "3714 496353 98431", "6011 1111 1111 1117", "6011 0009 9013 9424",
              "3530 1113 3330 0000", "3056 9309 0259 04", "6200 0000 0000 0005")
DOC_IBANS = ("GB82 WEST 1234 5698 7654 32", "DE89 3704 0044 0532 0130 00", "FR14 2004 1010 0505 0001 3M02 606",
             "NL91 ABNA 0417 1643 00", "ES91 2100 0418 4502 0005 1332")


def _name(r):
    return f"{r.choice(FIRST)} {r.choice(LAST)}"


def luhn_ok(digits: str) -> bool:
    d = [int(x) for x in digits if x.isdigit()]
    s = 0
    for i, x in enumerate(reversed(d)):
        if i % 2 == 1:
            x *= 2
            if x > 9:
                x -= 9
        s += x
    return s % 10 == 0


def _luhn_complete(prefix: str) -> str:
    for c in "0123456789":
        if luhn_ok(prefix + c):
            return prefix + c
    raise AssertionError


def iban_check(country: str, bban: str) -> str:
    """ISO 13616 mod-97 check digits for country + bban."""
    s = bban + country + "00"
    num = "".join(str(int(ch, 36)) for ch in s)
    return f"{98 - int(num) % 97:02d}"


def iban_ok(iban: str) -> bool:
    s = iban.replace(" ", "")
    s = s[4:] + s[:4]
    return int("".join(str(int(ch, 36)) for ch in s)) % 97 == 1


def _group4(s: str) -> str:
    return " ".join(s[i:i + 4] for i in range(0, len(s), 4))


def fake_email(r, first, last):
    f, l = first.lower(), last.lower()
    local = r.choice([f"{f}.{l}", f"{f}.{l}{r.randint(1, 99)}", f"{f[0]}{l}", f"{f}{l[0]}{r.randint(70, 99)}",
                      f"{f}_{l}", f"{l}.{f}"])
    return f"{local}@{r.choice(EMAIL_DOMAINS)}"


def fake_role_email(r):
    org = re.sub(r"[^a-z]+", "-", r.choice(VENUES + ORGS).lower()).strip("-")
    return f"{r.choice(ROLE_LOCAL)}@{org}.{r.choice(('example', 'example.org', 'test'))}"


def fake_phone(r):
    k = r.randrange(5)
    if k == 0:
        return f"({r.choice(('202', '312', '415', '503', '617', '720'))}) 555-01{r.randint(0, 99):02d}"
    if k == 1:
        return f"+1 {r.choice(('206', '305', '512', '614', '802'))}-555-01{r.randint(0, 99):02d}"
    if k == 2:
        return f"07700 900{r.randint(0, 999):03d}"
    if k == 3:
        return f"020 7946 0{r.randint(0, 999):03d}"
    return f"0491 570 1{r.randint(10, 59):02d}"


def fake_address(r, uk=None):
    uk = r.random() < 0.35 if uk is None else uk
    st = f"{r.randint(2, 980)} {r.choice(STREETS)} {r.choice(SUFFIX)}"
    if uk:
        pc = f"{r.choice('BCDHKLMNPRST')}{r.choice('ABEHLMNPRSTW')}{r.randint(1, 19)} {r.randint(1, 9)}" \
             f"{r.choice('ABDEFGHJLNPQRSTUWXYZ')}{r.choice('ABDEFGHJLNPQRSTUWXYZ')}"
        return f"{st}, {r.choice(TOWNS)} {pc}"
    return f"{st}, {r.choice(TOWNS)}, {r.choice(STATES)} {r.randint(10000, 99899)}"


def fake_date(r, lo=1940, hi=2008, style=None):
    y, m, d = r.randint(lo, hi), r.randint(1, 12), r.randint(1, 28)
    style = r.randrange(4) if style is None else style
    return [f"{d} {MONTHS[m - 1]} {y}", f"{MONTHS[m - 1]} {d}, {y}", f"{y}-{m:02d}-{d:02d}", f"{m:02d}/{d:02d}/{y}"][style]


def fake_ssn(r):
    return f"{r.randint(900, 999)}-{r.randint(1, 49):02d}-{r.randint(1, 9999):04d}"


def fake_card(r):
    if r.random() < 0.4:
        return r.choice(TEST_CARDS)
    return _group4(_luhn_complete("400000" + "".join(str(r.randint(0, 9)) for _ in range(9))))


def fake_passport(r):
    k = r.randrange(3)
    if k == 0:
        return "".join(str(r.randint(0, 9)) for _ in range(9))
    if k == 1:
        return r.choice("CFGHJKLMNPRTVWXYZ") + "".join(r.choice("0123456789CFGHJKLMNPRTVWXYZ") for _ in range(8))
    return r.choice("ABEKLMNPRSTUX") + "".join(str(r.randint(0, 9)) for _ in range(7))


def fake_iban(r):
    if r.random() < 0.25:
        return r.choice(DOC_IBANS)
    country = r.choice(("GB", "DE", "NL", "IE"))
    if country in ("GB", "IE"):
        bban = r.choice(("XMPL", "TSTB", "FKBK", "DEMO")) + "".join(str(r.randint(0, 9)) for _ in range(14))
    elif country == "NL":
        bban = r.choice(("XMPL", "TSTB", "DEMO")) + "".join(str(r.randint(0, 9)) for _ in range(10))
    else:
        bban = "".join(str(r.randint(0, 9)) for _ in range(18))
    return _group4(country + iban_check(country, bban) + bban)


def fake_ip(r):
    k = r.randrange(4)
    if k == 3:
        return f"2001:db8:{r.randint(1, 0xffff):x}:{r.randint(1, 0xffff):x}::{r.randint(1, 0xfff):x}"
    return f"{('192.0.2', '198.51.100', '203.0.113')[k]}.{r.randint(1, 254)}"


# ------------------------------------------------------------------------------------------------- the 9 types
# question wordings, card (yes, no), loose detector (pre-screen), carriers for inserted / lookalike items

TYPES = {
    "email": {
        "q": ("Does this text contain a personal email address?",
              "Is there an email address of an individual person in this text?"),
        "yes": "the text contains an email address that belongs to an individual person (personal or work), such as "
               "a name-based address.",
        "no": "the text has no such address; shared addresses of an organisation or team (info@, bookings@, help@ "
              "and similar) do not count, and other personal details do not count.",
        "detect": r"[\w.+-]+@[\w-]+\.[\w.-]+|\[at\]|\(at\)|\be-?mail\b",
    },
    "phone": {
        "q": ("Does this text contain a personal phone number?", "Is there an individual's phone number in this text?"),
        "yes": "the text contains a phone number that belongs to an individual person (their mobile, home or "
               "personal number).",
        "no": "no such number; public phone lines of an organisation (offices, help desks, booking or information "
              "lines), other numbers that only look like phone numbers, and other personal details do not count.",
        "detect": r"(?<!\d)(\+?\d{1,3}[\s.-]?)?(\(\d{2,4}\)|\d{2,5})[\s.-]\d{3,4}[\s.-]?\d{3,4}(?!\d)|\b(phone|tel|"
                  r"call|mobile|cell|fax)\b[^.\n]{0,20}\d",
    },
    "home_address": {
        "q": ("Does this text contain someone's home address?",
              "Is a private person's home street address given in this text?"),
        "yes": "the text contains the street address of a private person's home (where someone lives or receives "
               "personal mail).",
        "no": "no such address; addresses of businesses, venues, offices, parks or public buildings do not count, "
              "nor do other personal details.",
        "detect": r"\b\d{1,5}[A-Za-z]?\s+(?:[A-Z][\w'.-]*\s+){1,4}(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|"
                  r"Way|Court|Ct|Boulevard|Blvd|Place|Pl|Terrace|Close|Crescent|Highway|Hwy|Pike|Parkway|Pkwy|"
                  r"Circle|Cir|Row|Square|Sq)\b|\bP\.?\s?O\.? Box\b|\bhome address\b|\blives? at\b",
    },
    "date_of_birth": {
        "q": ("Does this text contain a person's date of birth?", "Is someone's full birth date given in this text?"),
        "yes": "the text gives a specific person's full date of birth (day, month and year).",
        "no": "no full birth date of a person; other dates (events, deadlines, openings, updates), years alone and "
              "other personal details do not count.",
        "detect": r"(?i)\b(born|birth\w*|DOB|d\.o\.b|b\.\s*\d)",
    },
    "ssn": {
        "q": ("Does this text contain a Social Security number?",
              "Is a person's US Social Security number given in this text?"),
        "yes": "the text contains a US Social Security number given as a person's SSN (nine digits, often written "
               "123-45-6789).",
        "no": "no such number; numbers in the same shape that are part, catalogue, lot, form or order numbers do not "
              "count, nor do other personal details.",
        "detect": r"(?<!\d)\d{3}[- ]\d{2}[- ]\d{4}(?!\d)|(?i:\bSSN\b|social security|\bTIN\b|taxpayer)",
    },
    "payment_card": {
        "q": ("Does this text contain a payment card number?", "Is a credit or debit card number given in this text?"),
        "yes": "the text contains a payment card number (a credit or debit card number, usually 13 to 19 digits).",
        "no": "no card number; tracking, order, serial, barcode or book numbers do not count, nor do other personal "
              "details.",
        "detect": r"(?<![\d-])(?:\d[ -]?){12,22}\d(?![\d-])|(?i:credit card|debit card|card number|\bVisa\b|"
                  r"Mastercard|\bAmex\b|\bCVV\b|\bCVC\b)",
    },
    "passport": {
        "q": ("Does this text contain a passport number?", "Is someone's passport number given in this text?"),
        "yes": "the text contains a person's passport number.",
        "no": "no passport number; booking references, permit, model, room, flight or course codes do not count, "
              "nor do other personal details.",
        "detect": r"(?i)passport|\b[A-Z]{1,2}\d{6,9}\b|(?<!\d)\d{9}(?!\d)",
    },
    "bank_account": {
        "q": ("Does this text contain a personal bank account number?",
              "Is an individual's bank account number or IBAN given in this text?"),
        "yes": "the text contains a bank account number or IBAN that belongs to an individual person.",
        "no": "no such account; an organisation's published bank details for payments or donations, invoice or "
              "reference codes, and other personal details do not count.",
        "detect": r"(?i)\bIBAN\b|account (no|number|#)|routing|sort code|\bBIC\b|\bSWIFT\b|"
                  r"\b[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){3,7}\b|(?<!\d)\d{8,17}(?!\d)",
    },
    "ip_address": {
        "q": ("Does this text contain an IP address linked to a person?",
              "Is an IP address of someone's device or connection given in this text?"),
        "yes": "the text contains an IP address (such as 203.0.113.7 or an IPv6 address) linked to a person's device, "
               "account or connection.",
        "no": "no such IP address; version, section or rule numbers with dots and other personal details do not "
              "count.",
        "detect": r"\b\d{1,3}(\.\d{1,3}){3}\b|\b[0-9a-fA-F]{1,4}(:[0-9a-fA-F]{0,4}){2,7}\b|(?i:\bIP\b|IPv[46])",
    },
}
for _k, _v in TYPES.items():
    _v["rx"] = re.compile(_v["detect"])
PTYPES = tuple(TYPES)


def detects(ptype: str, text: str) -> bool:
    return bool(TYPES[ptype]["rx"].search(text))


# carriers: functions r -> (sentence, value). Inserted carriers tie the value to a made-up person.

def _ins_email(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n, e = f"{f} {l}", fake_email(r, f, l)
    return r.choice([
        f"Submitted by {n} ({e}).", f"If you have questions, email me directly at {e}. - {f}",
        f"Contact person: {n}, {e}", f"Forwarded from {n} <{e}>:", f"Please send your RSVP to {f} at {e} by Friday.",
        f"{n} can be reached at {e} for carpool arrangements.", f"cc: {n} ({e})",
        f"Sign-up questions? My personal email is {e}.", f"Note from the editor: replies to {n} should go to {e}.",
    ]), e


def _look_email(r):
    e = fake_role_email(r)
    v = r.choice(VENUES)
    return r.choice([
        f"General enquiries: {e}.", f"For group bookings, email the {v} at {e}.", f"Press office: {e}",
        f"Questions about this programme can be sent to {e} (monitored on weekdays).",
        f"To report a problem with this page, write to {e}.", f"Our front desk inbox, {e}, is answered within two "
        f"working days.",
    ]), e


def _ins_phone(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n, p = f"{f} {l}", fake_phone(r)
    return r.choice([
        f"If you can't make it, text me on my mobile: {p}. - {f}", f"Emergency contact: {n} (mobile) {p}",
        f"Call {f} on {p} after 6 pm to arrange pickup.", f"Contact: {n}, cell {p}",
        f"{n}'s home number is {p} if the office is closed.", f"My personal number is {p}; please don't share it.",
        f"Leave a voicemail for {n} at {p}.",
    ]), p


def _look_phone(r):
    p, v = fake_phone(r), r.choice(VENUES)
    if r.random() < 0.3:
        code = f"{r.randint(1000, 9999)}-{r.randint(100, 999)}-{r.randint(1000, 9999)}"
        return r.choice([f"Item code {code} is out of stock until next month.", f"Order reference: {code}",
                         f"Use catalogue number {code} when reordering."]), code
    return r.choice([
        f"For bookings, call the {v} office at {p}.", f"Visitor information line: {p} (Monday to Friday, 9 am to 5 pm).",
        f"Call our help desk on {p} for opening times.", f"The ticket office of the {v} can be reached on {p}.",
        f"Main switchboard: {p}",
    ]), p


def _ins_address(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n, a = f"{f} {l}", fake_address(r)
    return r.choice([
        f"Please drop off donations at my home: {n}, {a}.", f"Mail the signed form to {n}, {a}.",
        f"Pickup will be from {f}'s house at {a}.", f"New home address for {n}: {a}",
        f"The meeting moved to my place, {a} - ring the side door. ({f})", f"Ship to: {n}, {a}",
    ]), a


def _look_address(r):
    a, v = fake_address(r), r.choice(VENUES)
    return r.choice([
        f"The event takes place at the {v}, {a}.", f"Our office is located at {a}, on the second floor.",
        f"Parking is available behind the {v} at {a}.", f"Visitor centre: {a} (open daily).",
        f"Returns can be sent to our warehouse, {a}.",
    ]), a


def _ins_dob(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n = f"{f} {l}"
    d = fake_date(r)
    return r.choice([
        f"Name: {n} | Date of birth: {d}", f"{n} (born {d}) will lead the group.", f"Applicant: {n}, DOB {d}",
        f"Please confirm your date of birth ({d}) when you check in, {f}.", f"Record updated: {n}, born on {d}.",
        f"{f} was born on {d}, so the junior rate applies.",
    ]), d


def _look_dob(r):
    d, v = fake_date(r, 1950, 2027), r.choice(VENUES)
    return r.choice([
        f"Applications close on {d}.", f"The site first opened to the public on {d}.",
        f"This page was last updated on {d}.", f"The next session is scheduled for {d}.",
        f"The {v} was dedicated on {d}.", f"The {v} marks its founding day on {d}.",
    ]), d


def _ins_ssn(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n, s = f"{f} {l}", fake_ssn(r)
    return r.choice([
        f"Employee: {n}, SSN {s}", f"For the background check, {f}'s Social Security number is {s}.",
        f"SSN: {s} (on file for {n})", f"Please verify the Social Security number {s} for {n} before payroll runs.",
    ]), s


def _look_ssn(r):
    x = f"{r.randint(100, 899)}-{r.randint(10, 99)}-{r.randint(1000, 9999)}"
    return r.choice([
        f"Part no. {x} fits both models.", f"Catalogue number: {x}", f"Lot {x} was inspected on site last week.",
        f"File form {x} with the county clerk.", f"Inventory tag {x} is attached to the projector.",
    ]), x


def _ins_card(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n, c = f"{f} {l}", fake_card(r)
    return r.choice([
        f"Card number: {c}, exp {r.randint(1, 12):02d}/{r.randint(27, 31)}, name on card {n}.",
        f"Please charge the deposit to my card, {c}. - {f}", f"{n} paid with card {c}.",
        f"Billing: {n}, credit card {c}", f"My debit card is {c}, can you put the booking on that?",
    ]), c


def _look_card(r):
    k = r.randrange(4)
    if k == 0:
        x = _group4("9400" + "".join(str(r.randint(0, 9)) for _ in range(18)))
        return f"Tracking number: {x}", x
    if k == 1:
        x = f"978-{r.randint(0, 1)}-{r.randint(100, 999)}-{r.randint(10000, 99999)}-{r.randint(0, 9)}"
        return r.choice([f"ISBN {x}", f"Reading list: ISBN {x} (paperback)."]), x
    if k == 2:
        x = _group4("".join(str(r.randint(0, 9)) for _ in range(16)))
        return r.choice([f"Serial no. {x} (printed under the base).", f"Device serial: {x}"]), x
    x = "".join(str(r.randint(0, 9)) for _ in range(13))
    return r.choice([f"Barcode {x}", f"Scan barcode {x} at the self-checkout."]), x


def _ins_passport(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n, p = f"{f} {l}", fake_passport(r)
    return r.choice([
        f"Traveller: {n}, passport no. {p}, expires {fake_date(r, 2027, 2034)}.",
        f"Please bring the passport ({p}) that {f} used for the booking.", f"{n}'s passport number is {p}.",
        f"Passport: {p} - issued to {n}",
    ]), p


def _look_passport(r):
    pnr = "".join(r.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(6))
    code = r.choice("ABCDEFGHKLMPRSTW") + "".join(str(r.randint(0, 9)) for _ in range(8))
    return r.choice([
        (f"Booking reference: {pnr}", pnr), (f"Event permit no. {code} is displayed at the entrance.", code),
        (f"Model {code} replaces the older unit.", code), (f"Course code {code[:3]}-{code[3:6]}", code),
        (f"Flight {r.choice(('XQ', 'ZV', 'QK'))}{r.randint(100, 9999)} boards at gate 4.", pnr),
    ])


def _ins_bank(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n, i = f"{f} {l}", fake_iban(r)
    return r.choice([
        f"Please transfer my refund to my account: IBAN {i} ({n}).", f"Bank details for {n}: IBAN {i}",
        f"{f} asked to be paid into account {i}.", f"Account holder: {n}, IBAN {i}.",
    ]), i


def _look_bank(r):
    if r.random() < 0.5:
        i, o = fake_iban(r), r.choice(ORGS)
        return r.choice([f"Donations to {o}: IBAN {i}.", f"Pay the hall hire fee to {o}, IBAN {i}, quoting your "
                                                              f"booking date."]), i
    x = f"INV-{r.randint(2019, 2027)}-{r.randint(1000, 99999):05d}"
    return r.choice([f"Invoice reference {x}", f"Quote reference {x} on any payment."]), x


def _ins_ip(r):
    f, l = r.choice(FIRST), r.choice(LAST)
    n, ip = f"{f} {l}", fake_ip(r)
    user = (f[0] + l).lower()
    return r.choice([
        f"New sign-in to {f}'s account from IP address {ip}.", f"Log: user {user} connected from {ip} at 14:02.",
        f"{n} reported that their home router's public IP is {ip}.", f"Blocked login attempt for {n} from {ip}.",
    ]), ip


def _look_ip(r):
    v = f"{r.randint(1, 12)}.{r.randint(0, 9)}.{r.randint(0, 20)}.{r.randint(1, 99)}"
    return r.choice([f"Update the firmware to version {v}.", f"See section {v} of the handbook.",
                     f"Rule {v} applies to all members.", f"Release {v} fixes the login bug."]), v


CARRIERS = {
    "email": (_ins_email, _look_email), "phone": (_ins_phone, _look_phone),
    "home_address": (_ins_address, _look_address), "date_of_birth": (_ins_dob, _look_dob),
    "ssn": (_ins_ssn, _look_ssn), "payment_card": (_ins_card, _look_card),
    "passport": (_ins_passport, _look_passport), "bank_account": (_ins_bank, _look_bank),
    "ip_address": (_ins_ip, _look_ip),
}

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")


def insert(text: str, sentence: str, r) -> tuple:
    """(new text, position) with `sentence` as its own paragraph at the start / end, or between paragraphs or after a
    sentence in the middle. The original text is otherwise unchanged."""
    paras = text.split("\n")
    u = r.random()
    if u < 0.2:
        return sentence + "\n" + text, "start"
    if u < 0.65:
        return text + "\n" + sentence, "end"
    if len(paras) >= 2:
        k = r.randint(1, len(paras) - 1)
        return "\n".join(paras[:k] + [sentence] + paras[k:]), "middle"
    sents = _SENT.split(text)
    if len(sents) >= 2:
        k = r.randint(1, len(sents) - 1)
        return " ".join(sents[:k]) + "\n" + sentence + "\n" + " ".join(sents[k:]), "middle"
    return text + "\n" + sentence, "end"


def make_one(host: dict, ptype: str, variant: str, *, cross_type: str | None = None) -> dict | None:
    """One W2 row (or None when the constraints cannot hold, e.g. a cross item that fires the asked detector)."""
    r = C.rng_for(T, host["text_id"], ptype, variant)
    text = host["text"]
    if detects(ptype, text):
        return None
    cons = {"pii_type": ptype, "variant": variant}
    if variant == "none":
        state, gold = text, 0
    else:
        if variant == "inserted":
            sent, val = CARRIERS[ptype][0](r)
            gold = 1
        elif variant == "lookalike":
            sent, val = CARRIERS[ptype][1](r)
            gold = 0
        elif variant == "cross":
            assert cross_type and cross_type != ptype
            sent, val = CARRIERS[cross_type][0](r)
            if detects(ptype, sent):
                return None
            cons["inserted_type"] = cross_type
            gold = 0
        else:
            raise ValueError(variant)
        state, pos = insert(text, sent, r)
        cons.update({"inserted_sentence": sent, "inserted_value": val, "position": pos})
    spec = TYPES[ptype]
    qi = C.pick_wording(spec["q"], T, host["text_id"], ptype)
    row = C.make_row(T, f"{host['text_id']}:{ptype}:{variant}", host["text_id"], state, spec["q"][qi],
                     qtype="noul", gold=gold, card=C.yesno_card(spec["yes"], spec["no"]), gold_method="program",
                     construction=cons,
                     extra_meta={"wording_id": f"{ptype}.q{qi}", **C.text_meta(host),
                                 "licence": f"text: {host.get('licence_url')}; inserted wording: {C.LICENCE_AUTHORED}"})
    return row


def plan(per_type: int) -> list:
    """[(ptype, variant)] with exact per-type shares (largest remainder)."""
    out = []
    for p in PTYPES:
        raw = [(v, per_type * s) for v, s in SHARES]
        n = {v: int(x) for v, x in raw}
        rest = per_type - sum(n.values())
        for v, x in sorted(raw, key=lambda vx: -(vx[1] - int(vx[1])))[:rest]:
            n[v] += 1
        out += [(p, v) for v, _ in SHARES for _ in range(n[v])]
    return out


def build(texts: dict, per_type: int = PER_TYPE, checker=None) -> tuple:
    hosts = C.pick_texts(texts, T, len(PTYPES) * per_type * 3, min_w=MIN_W, max_w=MAX_W, tag="hosts")
    jobs = [pv for _, pv in sorted(enumerate(plan(per_type)),
                                   key=lambda ipv: C.key_hash(C.SEED, T, "job", ipv[0]))]
    avail = list(hosts)              # seeded order; a host that does not fit a job stays for later jobs
    rows, short = [], Counter()
    for ptype, variant in jobs:
        made = None
        for j, h in enumerate(avail[:300]):
            cross = None
            if variant == "cross":
                others = [p for p in PTYPES if p != ptype]
                cross = others[C.key_hash(C.SEED, T, "cross", h["text_id"], ptype) % len(others)]
            made = make_one(h, ptype, variant, cross_type=cross)
            if made is not None:
                del avail[j]
                break
        if made is None:
            short[f"{ptype}/{variant}"] += 1
            continue
        rows.append(made)
    kept, drops, toks = C.check_all(rows, checker)
    stats = {
        "type": T, "gold_method": "program", "per_type_target": per_type, "shares": dict(SHARES),
        "candidates": len(rows), "kept_after_render": len(kept), "render_drops": drops[:50],
        "n_render_drops": len(drops), "unfilled_jobs": dict(short), "tokens_min_med_max_mean": C.token_stats(toks),
        "labels": C.label_stats(kept),
        "per_type": {p: dict(Counter(r["meta"]["construction"]["variant"] for r in kept
                                     if r["meta"]["construction"]["pii_type"] == p)) for p in PTYPES},
        "domains": dict(Counter(r["meta"]["domain"] for r in kept)),
        "positions": dict(Counter(r["meta"]["construction"].get("position", "-") for r in kept)),
    }
    return kept, stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    per = int(argv[argv.index("--per-type") + 1]) if "--per-type" in argv else PER_TYPE
    rows, stats = build(C.load_texts(), per)
    print(f"W2 rows {len(rows)} labels {stats['labels']} unfilled {stats['unfilled_jobs']} "
          f"tokens {stats['tokens_min_med_max_mean']} render drops {stats['n_render_drops']}")
    if "--dry-run" not in argv:
        C.write_outputs(T, rows, stats)
    return rows, stats


if __name__ == "__main__":
    main()
