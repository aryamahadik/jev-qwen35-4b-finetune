"""rt_env: request bodies and surface templates (envelopes) for gen_routing.

Body = issue blocks (open issues: main sentence + one sentence per fact; decoys: resolved / declined mentions), with
optional small talk, context lines, keyword decoys and a closer, laid out as prose, a numbered list or terse text.
Envelopes (44 Claude-written surface templates): emails with and without headers, reply threads, web forms with a
sender-chosen topic, live chat, chatbot hand-off, call notes, voicemail transcripts, SMS, social DMs, letters,
in-app feedback, ticket exports, forwarded mail, counter escalations, surveys, relay calls, on-behalf messages,
WhatsApp, internal portal tickets, internal email, Slack / Teams threads, walk-up notes, manager escalations, HR case
forms, kiosk submissions, and more.  Every envelope is deterministic given the scenario seed.
"""
import datetime as dt
import re

from rt_core import R, cap, fdate, ftime, lcfirst

FIRST = ["Amara", "Bilal", "Chen", "Daniela", "Emeka", "Farah", "Gustavo", "Hana", "Ibrahim", "Jolene", "Kenji",
         "Leilani", "Mateo", "Nadia", "Oluwaseun", "Priya", "Quentin", "Rosa", "Sipho", "Tamar", "Umar", "Valentina",
         "Wojtek", "Ximena", "Yusuf", "Zanele", "Aarav", "Brigid", "Carlos", "Dilnoza", "Eero", "Fatima", "Giorgos",
         "Halima", "Isaac", "Jia", "Kwame", "Lucia", "Marcus", "Noor", "Oskar", "Paloma", "Rahul", "Svetlana",
         "Tomasz", "Uzma", "Viktor", "Wren", "Yara", "Zeke", "Alex", "Sam", "Jordan", "Riley", "Aiyana", "Bongani",
         "Celine", "Dmitri", "Esperanza", "Finn", "Grace", "Hamza", "Ingrid", "Javier", "Keiko", "Liam", "Mei",
         "Nikolai", "Olga", "Pedro", "Rania", "Stefan", "Thandiwe", "Tariq", "Ulla", "Vikram", "Winifred", "Xavier",
         "Yetunde", "Zoltan", "Anika", "Benedikt", "Chiara", "Deshawn", "Elif", "Felipe", "Gulnara", "Hiroshi",
         "Imani", "Jakob", "Maya", "Tobias", "Ayesha", "Diego", "Nomvula", "Arjun", "Freya", "Kofi", "Linh",
         "Mohammed", "Sofia", "Ravi", "Beatriz", "Colm", "Dana", "Eleni", "Femi", "Greta", "Hector", "Irina",
         "Joon", "Katarina", "Lars", "Mariam", "Nils", "Odette", "Pavel", "Rukmini", "Soren", "Teodora", "Vusi",
         "Wanjiru", "Yosef", "Zara", "Aoife", "Bruno", "Camille", "Declan", "Esther", "Farid", "Gemma", "Idris",
         "June", "Kamal", "Lena", "Moses", "Nia", "Orla", "Patrick", "Rosalind", "Selin", "Trevor", "Una"]
LAST = ["Okafor", "Haddad", "Lindqvist", "Moreau", "Nakamura", "Oyelaran", "Petrov", "Quinn", "Ramirez", "Schmidt",
        "Tanaka", "Uddin", "Varga", "Walsh", "Xu", "Yilmaz", "Zielinski", "Abara", "Brennan", "Castillo", "Dimitrov",
        "Eriksen", "Fontaine", "Gallagher", "Horvath", "Iqbal", "Jovanovic", "Kowalski", "Laurent", "Mbeki",
        "Novak", "O'Brien", "Pereira", "Rahman", "Sato", "Thorne", "Usman", "Vasquez", "Whitfield", "Yamada",
        "Zhou", "Adeyemi", "Bauer", "Chowdhury", "Delgado", "Eze", "Fischer", "Gonzalez", "Holm", "Ito", "Jensen",
        "Kaur", "Lopez", "Mensah", "Nguyen", "Olsen", "Patel", "Rossi", "Silva", "Takahashi", "Vogel", "Wang",
        "Asante", "Bianchi", "Cohen", "Duarte", "Engel", "Farouk", "Grant", "Hassan", "Ivanova", "Jimenez", "Kim",
        "Lebedev", "Murphy", "Nair", "Ortega", "Park", "Reyes", "Sorensen", "Tran", "Umeh", "Volkov", "Wilson",
        "Aziz", "Byrne", "Costa", "Dunne", "Ekwueme", "Fraser", "Guerrero", "Hughes", "Ibarra", "Kagame", "Levy",
        "Moyo", "Nkosi", "Osei", "Pham", "Quispe", "Richter", "Stein", "Toure", "Ueda", "Vance", "Wiśniewski",
        "Achebe", "Barros", "Carver", "Dahl", "Ellis", "Ferrari", "Gupta", "Hale", "Ionescu", "Joshi", "Keane"]
AGENTS = ["Sam R.", "Priya K.", "Luis M.", "Dana T.", "Kofi A.", "Mia S.", "Jonah P.", "Aisha B.", "Tom W.", "Lena F.",
          "Ravi N.", "Grace O.", "Mateus C.", "Helen D.", "Yuki H.", "Omar Z."]
DEPTS = ["Finance", "Marketing", "Operations", "Legal", "Sales", "Engineering", "Customer Success", "Procurement",
         "Facilities", "Research", "Communications", "Logistics", "Quality Assurance", "Data & Analytics"]
SITES = ["Chicago office", "Leeds office", "Toronto office", "Austin office", "Dublin office", "Denver office",
         "Singapore office", "Rotterdam office", "home (remote)", "Atlanta office", "Glasgow office"]
TITLES = ["Analyst", "Senior Analyst", "Coordinator", "Engineer", "Account Manager", "Specialist", "Team Lead",
          "Associate", "Project Manager", "Designer", "Accountant", "Paralegal"]
RELS = ["mother", "father", "grandmother", "grandfather", "aunt", "uncle", "neighbour", "brother", "sister"]
GENERIC_SUBJ = ["Help please", "Question", "Need some help", "Following up", "Hello", "Request", "Quick question",
                "Please read", "(no subject)", "Issue", "Can you help?", "Two things", "Assistance needed",
                "Getting in touch", "Re: my account", "Problem", "Hoping you can sort this", "A few things"]
CLOSERS = ["Thanks.", "Thanks in advance.", "Appreciate the help.", "Hope you can sort this out.",
           "Please get back to me when you can.", "Thank you for your time.", "Looking forward to hearing back.",
           "Cheers.", "Many thanks.", "Let me know what you need from me."]
GREETS = ["Hi,", "Hello,", "Hi there,", "Good morning,", "Good afternoon,", "Hello {org} team,", "Dear {org},",
          "Hi team,", "To whom it may concern,", "Hey,"]
CONNECT = ["Also, ", "Separately, ", "On top of that, ", "While I have you: ", "Another thing: ", "One more thing: ",
           "Second, ", "And ", "In addition, ", "Unrelated, but ", "Besides that, "]
RESOLVED = ["{Past} was sorted out {when}, so that part is done.",
            "Your team already took care of {past} {when} - thanks, no action needed on that.",
            "(Just so you know, {past} was resolved {when}, so please ignore that.)",
            "I did have a problem with {past} {when}, but it has since been fixed.",
            "My earlier request about {past} is closed and fine now.",
            "{Past} is no longer an issue; it was dealt with {when}.",
            "Thanks for handling {past} {when}; that one is completely resolved."]
WHEN = ["last week", "last month", "a few weeks ago", "earlier this month", "back in the spring", "in January",
        "on my last call", "two weeks ago", "yesterday"]
FIXED = ["That has since been taken care of, though, so please ignore it.",
         "(Update: that part is already sorted.)",
         "Please ignore that part - it has since been dealt with.",
         "Actually, someone already helped me with that one, so no action is needed.",
         "That one was resolved yesterday, so there's nothing to do there.",
         "Scratch that - it was sorted out this morning."]
DECLINED = ["I'm not asking for {neg}.", "To be clear, I don't want {neg}.", "This isn't a request for {neg}.",
            "I don't need {neg}.", "Please note I am not looking for {neg}.", "Just to be clear: no need for {neg}.",
            "I'm not after {neg} here."]


def _sub(t, f):
    def rep(m):
        k = m.group(1)
        if k in f:
            return f[k]
        raise KeyError(k)
    return re.sub(r"\{(\w+)\}", rep, t)


def body_layout(blocks, extras, rng, style):
    """blocks: list of (role, [sentences]); role 'open' | 'decoy'. extras: dict(filler=..., ctx=[...], kw=..., closer=...).
    Returns (paragraph text, lines)."""
    opens = [b for b in blocks if b[0] == "open"]
    lines = []
    head = []
    closing_filler = None
    f = extras.get("filler")
    if f and re.match(r"(?i)(thank|thanks|please|hope someone|hope you can|looking forward)", f):
        closing_filler = f  # a closing remark goes at the end and replaces the closer
    elif f:
        head.append(f)
    head += extras.get("ctx", [])
    items = []
    k = 0
    for role, sents in blocks:
        s = list(sents)
        if role == "open":
            if k > 0 and style != "bullets":
                s[0] = rng.choice(CONNECT) + lcfirst(s[0])
            k += 1
        items.append((role, " ".join(s)))
    tail = []
    if extras.get("kw"):
        tail.append(extras["kw"])
    if closing_filler:
        tail.append(closing_filler)
    elif extras.get("closer") and style != "terse":
        tail.append(extras["closer"])
    if style == "bullets" and len(opens) >= 2:
        pre = [t for r, t in items if r != "open"]
        num = [t for r, t in items if r == "open"]
        fmt = rng.choice(["{i}. {t}", "{i}) {t}", "- {t}", "({i}) {t}"])
        intro = rng.choice(["I have {n} things:", "A few points:", "Here's what I need:", "Issues:", "Details below."])
        intro = intro.format(n=len(num))
        paras = []
        if head or pre:
            paras.append(" ".join(head + pre))
        paras.append(intro + "\n" + "\n".join(fmt.format(i=i + 1, t=t) for i, t in enumerate(num)))
        if tail:
            paras.append(" ".join(tail))
        text = "\n\n".join(paras)
        lines = [x for x in (head + pre) if x] + num + tail
        return text, lines
    seq = head + [t for _, t in items] + tail
    lines = list(seq)
    if style == "para2" and len(seq) >= 3:
        cut = rng.randrange(1, len(seq))
        text = " ".join(seq[:cut]) + "\n\n" + " ".join(seq[cut:])
    elif style == "blocks" and len(items) >= 2:
        paras = []
        if head:
            paras.append(" ".join(head))
        paras += [t for _, t in items]
        if tail:
            paras.append(" ".join(tail))
        text = "\n\n".join(paras)
    else:
        text = " ".join(seq)
    return text, lines


def voice(text, rng):
    t = text.replace("\n", " ")
    t = re.sub(r"[;()\"]", "", t)
    t = re.sub(r"(?<!\d),|,(?!\d)", "", t)
    t = re.sub(r"\s+-\s+", " ", t)
    words = t.split(" ")
    out = []
    for w in words:
        if w in ("I", "I'm", "I've", "I'd", "I'll") or re.match(r"^[A-Z]{2,}", w) or re.search(r"\d", w):
            out.append(w)
        else:
            out.append(w.lower())
    t = " ".join(out)
    sents = re.split(r"(?<=[.?!])\s+", t)
    if len(sents) > 2:
        i = rng.randrange(1, len(sents))
        sents[i] = rng.choice(["um ", "uh ", "um ", "uh "]) + sents[i]
    return " ".join(sents)


# ============================================================================================= envelopes
def q(s):
    return "\"" + s + "\""


def E(id, side, fn, date=False, reported=False, topic=False, style=("para", "para2", "blocks", "bullets"),
      lines=False, voice_=False):
    return {"id": id, "side": side, "fn": fn, "date": date, "reported": reported, "topic": topic, "style": style,
            "lines": lines, "voice": voice_}


def _chat(pk, who_fmt="[{t}] {who}: {x}", start=None):
    rng = pk["rng"]
    m = start if start is not None else rng.randrange(8 * 60, 21 * 60)
    out = []
    for x in pk["lines"]:
        m += rng.randrange(0, 3)
        out.append(who_fmt.format(t=ftime(m, 0), who=pk["first"], x=x))
    return out, m


def env_email_hdr(pk):
    return (f"From: {pk['name']} <{pk['email']}>\nTo: {pk['support']}\nDate: {pk['date_long']}\nSubject: {pk['subject']}"
            f"\n\n{pk['greet']}\n\n{pk['body']}\n\n{pk['signoff']}\n{pk['sig']}")


def env_email_min(pk):
    return f"Subject: {pk['subject']}\n\n{pk['body']}\n\n{pk['first']}"


def env_email_sig(pk):
    return f"{pk['greet']}\n\n{pk['body']}\n\nKind regards,\n{pk['sig']}\n{pk['phone']}"


def env_reply_quote(pk):
    return (f"Subject: Re: {pk['old_subject']}\nSent: {pk['date_long']}\n\n{pk['body']}\n\n{pk['first']}\n\n"
            f"> On {pk['old_date']}, {pk['org']} wrote:\n> Thank you for contacting us. Your case {pk['old_ticket']} has "
            f"been closed. If you need anything else, simply reply to this email.")


def env_webform(pk):
    return (f"Contact form - {pk['org']}\nName: {pk['name']}\nEmail: {pk['email']}\n{pk['acct']}\n"
            f"Topic (selected by the sender): {pk['topic']}\nMessage:\n{pk['body']}")


def env_webform2(pk):
    return (f"[Web form] submitted {pk['date_iso']} {pk['time']}\nFull name: {pk['name']}\nReason for contact "
            f"(drop-down, chosen by sender): {pk['topic']}\nDetails: {pk['body']}\nPreferred reply: email")


def env_webform3(pk):
    return (f"Online enquiry\n----------------\nFrom: {pk['name']} ({pk['phone']})\nCategory the customer picked: "
            f"{pk['topic']}\nReference: {pk['ref']}\n\n{pk['body']}")


def env_chat(pk):
    rng = pk["rng"]
    m = rng.randrange(8 * 60, 21 * 60)
    head = f"[{ftime(m, 0)}] Agent ({pk['agent']}): Hi, thanks for reaching out to {pk['org']}! How can I help today?"
    ls, _ = _chat(pk, start=m + 1)
    return f"Live chat transcript - {pk['org']} website\n" + head + "\n" + "\n".join(ls)


def env_bot(pk):
    ls = pk["lines"]
    first, rest = ls[0], ls[1:]
    s = f"[Virtual assistant] Hi! Tell me briefly what you need help with.\n[Customer] {first}"
    if rest:
        s += "\n[Virtual assistant] Got it. Anything else before I pass you to a person?\n[Customer] " + " ".join(rest)
    return s + "\n[Virtual assistant] Thanks - connecting you to the next available agent."


def env_call(pk):
    return (f"Phone call log - {pk['date_long']}, agent {pk['agent']}\nCaller: {pk['name']} ({pk['phone']})\n"
            f"Caller's account of the problem, noted in their own words during the call:\n{q(pk['body'])}\n"
            f"Caller asked for a follow-up by email.")


def env_call_bullets(pk):
    out = [f"Inbound call {pk['time']} - notes by {pk['agent']}", f"- Caller: {pk['name']}"]
    out += [f"- Said: {q(x)}" for x in pk["lines"]]
    return "\n".join(out)


def env_voicemail(pk):
    return (f"Voicemail left on the {pk['org']} line on {pk['date_long']} at {pk['time']} (transcribed):\n"
            f"{q('hi this is ' + pk['first'].lower() + ' ' + pk['vbody'])}")


def env_sms(pk):
    return f"Text messages to {pk['org']} ({pk['short']}) from {pk['phone']}:\n" + "\n".join("> " + x for x in pk["lines"])


def env_dm(pk):
    return f"Direct message to @{pk['org_handle']} from @{pk['handle']}:\n{pk['body']}"


def env_letter(pk):
    return (f"{pk['addr']}\n\n{pk['date_long']}\n\nDear Sir or Madam,\n\n{pk['body']}\n\nYours faithfully,\n{pk['name']}")


def env_app(pk):
    return f"In-app message ({pk['platform']}) - contact me: yes\n{pk['body']}"


def env_ticket_kv(pk):
    body = pk["body"].replace("\n", "\n  ")
    return (f"ticket: {pk['ticket']}\nchannel: email\ncreated: {pk['date_iso']} {pk['time']}\n"
            f"customer_priority: {pk['cprio']}\nrequester: {pk['email']}\ndescription: |\n  {body}")


def env_forward(pk):
    return (f"Hi team - this landed in my own inbox, forwarding so it gets handled. {pk['colleague']}\n\n"
            f"---------- Forwarded message ---------\nFrom: {pk['name']} <{pk['email']}>\nDate: {pk['date_long']}\n"
            f"Subject: {pk['subject']}\n\n{pk['body']}")


def env_counter(pk):
    return (f"Escalation from {pk['branch']} ({pk['date_long']}), logged by {pk['agent']}: {pk['name']} came to the "
            f"counter and wrote down the following:\n{q(pk['body'])}")


def env_survey(pk):
    return (f"Customer survey ({pk['date_iso']}) - Q7 'Is there anything else you want us to know?'\nAnswer: {pk['body']}\n"
            f"Q8 'May we contact you about your answer?' Yes ({pk['email']})")


def env_plain(pk):
    return pk["body"]


def env_relay(pk):
    return (f"Relay call transcript (the relay operator types the caller's words), {pk['date_long']}:\n"
            f"CALLER: {pk['body']}\nOPERATOR: Caller asks for a reply by text GA")


def env_behalf(pk):
    return (f"{pk['greet']}\n\nI'm writing for my {pk['rel']}, {pk['name']}, who asked me to send this in their own "
            f"words:\n\n{q(pk['body'])}\n\nThank you,\n{pk['helper']}")


def env_whatsapp(pk):
    ls, _ = _chat(pk, who_fmt="[{t}] {who}: {x}")
    return f"WhatsApp Business chat with {pk['org']}, {pk['date_long']}\n" + "\n".join(ls)


def env_subject_body(pk):
    return f"{pk['subject']} - {pk['body']}"


def env_postcard(pk):
    return f"Note left in the {pk['org']} feedback box ({pk['date_long']}):\n{pk['body']}\n- {pk['first']}"


def env_email_thread2(pk):
    return (f"From: {pk['email']}\nDate: {pk['date_long']}\nSubject: {pk['subject']}\n\n{pk['body']}\n\n"
            f"Sent from my phone")


def env_dm_public(pk):
    return (f"Reply to @{pk['org_handle']} on social media, moved to private messages by the social team:\n"
            f"@{pk['handle']}: {pk['body']}")


def env_intake_form(pk):
    return (f"New enquiry form\nName: {pk['name']}\nPhone: {pk['phone']}\nWhat is this about? (sender's own words "
            f"or choice): {pk['topic']}\nTell us what happened:\n{pk['body']}")


def env_call_summary(pk):
    return (f"Call summary written by {pk['agent']} ({pk['date_long']}). Caller {pk['name']} explained, and I quote "
            f"what they said: {q(pk['body'])}")


# ---- internal (employees)
def env_portal(pk):
    return (f"Service portal ticket {pk['ticket']}\nRequester: {pk['name']} ({pk['dept']}, {pk['site']})\n"
            f"Category chosen by requester: {pk['topic']}\nShort description: {pk['subject']}\nDetails:\n{pk['body']}")


def env_int_email(pk):
    return (f"To: {pk['desk_email']}\nFrom: {pk['name']}, {pk['dept']}\nDate: {pk['date_long']}\nSubject: "
            f"{pk['subject']}\n\n{pk['greet']}\n\n{pk['body']}\n\nThanks,\n{pk['first']}")


def env_slack(pk):
    rng = pk["rng"]
    m = rng.randrange(8 * 60, 18 * 60)
    out = [f"#{pk['channel']}"]
    for i, x in enumerate(pk["lines"]):
        out.append(f"{pk['first']} {pk['last']}  {ftime(m + i, 2)}\n{x}")
    return "\n".join(out)


def env_walkup(pk):
    return (f"Walk-up at the {pk['site']} {pk['desk']} desk, {pk['date_long']}, logged by {pk['agent'].rstrip('.')}. "
            f"{pk['name']} ({pk['dept']}) said:\n{q(pk['body'])}")


def env_manager(pk):
    return (f"{pk['greet']}\n\nRaising this for {pk['name']} in my team, who is {pk['away']} today. Their note to me, word "
            f"for word:\n{q(pk['body'])}\n\n{pk['mgr']}\n{pk['dept']} manager")


def env_int_phone(pk):
    return (f"Call to the {pk['desk']} line, {pk['date_long']} {pk['time']}. Caller: {pk['name']}, ext. {pk['ext']}.\n"
            f"Notes (caller's own words): {q(pk['body'])}")


def env_case_form(pk):
    return (f"Case submitted through {pk['portal']}\nEmployee ID: {pk['eid']}\nCase type (employee's choice): "
            f"{pk['topic']}\nDescription: {pk['body']}\nConfidential: {pk['conf']}")


def env_teams(pk):
    ls = pk["lines"]
    out = [f"[Teams chat with the {pk['desk']} desk]", f"Agent: Hi {pk['first']}, what can we do for you?"]
    out += [f"{pk['first']}: {x}" for x in ls]
    return "\n".join(out)


def env_int_terse(pk):
    return f"{pk['subject']}: {pk['body']}\n- {pk['first']} ({pk['dept']})"


def env_int_thread(pk):
    return (f"Subject: RE: {pk['old_subject']}\nFrom: {pk['name']}\nDate: {pk['date_long']}\n\n{pk['body']}\n\n"
            f"{pk['first']}\n\n-----Original Message-----\nFrom: {pk['desk']} desk\nSent: {pk['old_date']}\n"
            f"Your request {pk['old_ticket']} has been completed and closed.")


def env_kiosk(pk):
    return (f"Self-service kiosk submission ({pk['site']}, {pk['date_iso']} {pk['time']})\nBadge: {pk['eid']}\n"
            f"Free text: {pk['body']}")


def env_one_on_one(pk):
    return (f"Notes from a 1:1 on {pk['date_long']} ({pk['mgr']}, manager). {pk['name']} asked me to log this for them "
            f"exactly as they put it: {q(pk['body'])}")


def env_int_form_short(pk):
    return (f"Request form\nName: {pk['name']}\nTeam: {pk['dept']}\nLocation: {pk['site']}\nWhat do you need?\n"
            f"{pk['body']}")


def env_int_voicemail(pk):
    return (f"Voicemail to the {pk['desk']} desk, {pk['date_long']} {pk['time']} (transcribed): "
            f"{q('hi it is ' + pk['first'].lower() + ' from ' + pk['dept'].lower() + ' ' + pk['vbody'])}")


ENVS = [
    E("email_hdr", "ext", env_email_hdr, date=True),
    E("email_min", "ext", env_email_min),
    E("email_sig", "ext", env_email_sig),
    E("reply_quote", "ext", env_reply_quote, date=True),
    E("webform", "ext", env_webform, topic=True),
    E("webform2", "ext", env_webform2, date=True, topic=True),
    E("webform3", "ext", env_webform3, topic=True),
    E("chat", "ext", env_chat, lines=True, style=("lines",)),
    E("bot", "ext", env_bot, lines=True, style=("lines",)),
    E("call", "ext", env_call, date=True, reported=True),
    E("call_bullets", "ext", env_call_bullets, reported=True, lines=True, style=("lines",)),
    E("voicemail", "ext", env_voicemail, date=True, voice_=True, style=("para",)),
    E("sms", "ext", env_sms, lines=True, style=("lines",)),
    E("dm", "ext", env_dm),
    E("letter", "ext", env_letter, date=True),
    E("app", "ext", env_app),
    E("ticket_kv", "ext", env_ticket_kv, date=True),
    E("forward", "ext", env_forward, date=True, reported=True),
    E("counter", "ext", env_counter, date=True, reported=True),
    E("survey", "ext", env_survey, date=True),
    E("plain", "ext", env_plain, style=("para", "para2", "terse")),
    E("relay", "ext", env_relay, date=True, reported=True, style=("para",)),
    E("behalf", "ext", env_behalf, reported=True),
    E("whatsapp", "ext", env_whatsapp, date=True, lines=True, style=("lines",)),
    E("subject_body", "ext", env_subject_body, style=("para", "terse")),
    E("postcard", "ext", env_postcard, date=True),
    E("email_phone", "ext", env_email_thread2, date=True),
    E("dm_public", "ext", env_dm_public),
    E("intake_form", "ext", env_intake_form, topic=True),
    E("call_summary", "ext", env_call_summary, date=True, reported=True),
    E("portal", "int", env_portal, topic=True),
    E("int_email", "int", env_int_email, date=True),
    E("slack", "int", env_slack, lines=True, style=("lines",)),
    E("walkup", "int", env_walkup, date=True, reported=True),
    E("manager", "int", env_manager, reported=True),
    E("int_phone", "int", env_int_phone, date=True, reported=True),
    E("case_form", "int", env_case_form, topic=True),
    E("teams", "int", env_teams, lines=True, style=("lines",)),
    E("int_terse", "int", env_int_terse, style=("para", "terse")),
    E("int_thread", "int", env_int_thread, date=True),
    E("kiosk", "int", env_kiosk, date=True),
    E("one_on_one", "int", env_one_on_one, date=True, reported=True),
    E("int_form_short", "int", env_int_form_short),
    E("int_voicemail", "int", env_int_voicemail, date=True, voice_=True, style=("para",)),
]
ENV_BY = {e["id"]: e for e in ENVS}
assert len(ENV_BY) == len(ENVS)
