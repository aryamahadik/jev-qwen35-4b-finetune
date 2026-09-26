#!/usr/bin/env python3
"""Write the train/dev distractor banks (DESIGN 6.3, 4.4 L3, 3.2 dev filler, 11, 12).

Outputs (deterministic, no randomness, one JSON object per line, sorted by id):
  assets/distractor/train_dev/boilerplate_A.jsonl   40  train filler (CC0), 5 per category
  assets/distractor/train_dev/reference_A.jsonl     40  train hard-reference FAQ snippets
  assets/distractor/train_dev/boilerplate_C.jsonl   15  dev filler (CC0), same categories, different style

Every string below is authored by "llm:claude:train-dev-distractor-bank-author" (deviation D1).
This author never reads assets/distractor/eval/ (boilerplate B, reference B).

Rules enforced by check() (the script exits non-zero on any violation):
  * boilerplate carries no class signal: no label key of ANY keys file as a whole phrase, and none
    of the hand lists below (refund, urgency, spam/marketing, emotion, yes/no/negation cues,
    request/greeting words, third-party container markers, topical words of the train verticals);
  * reference snippets name >= 1 label of their dataset by its exact key, list those ids in
    named_label_ids, and contain no other key (intent, domain or scenario) of that dataset;
  * exact counts per bank and per category; unique ids and texts;
  * char 5-gram Jaccard < 0.5 inside each bank and between boilerplate A and C (the MinHash
    threshold DESIGN 6.3 sets between A and B, applied here to A vs C as well).

Run:  python3 assets/distractor/train_dev/make_train_dev_banks.py
"""
import glob
import json
import os
import re
import sys

AUTHOR = "llm:claude:train-dev-distractor-bank-author"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
KEYS_DIR = os.path.join(ROOT, "assets", "labels", "keys")

CATEGORIES = [
    "email_signature",
    "confidentiality_notice",
    "disclaimer",
    "cookie_banner",
    "sent_from_phone",
    "meeting_footer",
    "page_chrome",
    "log_header",
]

STYLE_A = "A: multi-line, sentence-case, formal corporate/web formatting"
STYLE_C = "C: compact single-line, lowercase or bracketed-tag formatting"

# ---------------------------------------------------------------------------------------------
# Boilerplate A (train, CC0): 8 categories x 5
# ---------------------------------------------------------------------------------------------
BOILERPLATE_A = {
    "email_signature": [
        "--\nRenata Okafor\nSenior Research Engineer | Materials Group\nOakmere Engineering Ltd\n"
        "T +44 20 7946 0321\nwww.oakmere-eng.example",
        "Tobias Lindqvist\nProgramme Coordinator\nLindqvist Instruments AB\nTel: +46 8 555 012 45\n"
        "lindqvist-instruments.example",
        "--\nPriya Raman, PhD\nPrincipal Statistician, Survey Methods Unit\nFairholm Analytics\n"
        "+1 (555) 014-2290 | fairholm.example",
        "Marco Bellini\nFacilities Coordinator, Floor 3 North\nPemberton & Shaw LLP\n"
        "Switchboard +1 555 0100, ext. 4417",
        "Aiko Tanaka (she/her)\nTechnical Writer, Documentation Team\nCorvel Systems\n"
        "corvel.example/docs\nHandle: @atanaka",
    ],
    "confidentiality_notice": [
        "CONFIDENTIALITY NOTICE: This message and any attachments are intended solely for the "
        "addressee named above and may contain privileged or confidential material. Copies that "
        "reached anyone outside the named distribution are to be erased, and the sender is to be "
        "informed. Use, copying or distribution by others is prohibited.",
        "The contents of this transmission are confidential and intended only for the individual "
        "or entity to whom it is addressed. Retransmission, dissemination or use of this material "
        "by parties outside the intended distribution is prohibited.",
        "PRIVILEGED & CONFIDENTIAL. This communication may contain legally privileged material "
        "and is intended for the use of the addressee alone. Any copy held by a third party "
        "through misdirection is to be erased along with the original.",
        "Classification: INTERNAL. Circulation outside internal staff requires clearance from "
        "the data owner. Handle in line with the records policy, section 4.",
        "Notice: the material in this message is confidential and may be legally privileged. "
        "Disclosure, copying or distribution to third parties requires the prior consent of "
        "the sender.",
    ],
    "disclaimer": [
        "Views and opinions expressed in this message belong solely to the sender and represent "
        "the sender's individual position, separate from any official position.",
        "The material on this page is provided for discussion purposes only. Anyone relying on it "
        "should first seek guidance from a qualified professional.",
        "Figures in this document are rounded and may differ slightly from those in the audited "
        "annex. The annex is the authoritative source.",
        "Printed copies of this message are uncontrolled; the electronic version is "
        "authoritative. Printing is kept to a minimum for environmental reasons.",
        "Portions of this summary were drafted with automated tools and edited by staff. The "
        "source records remain the authoritative version.",
    ],
    "cookie_banner": [
        "This website uses cookies to keep it running and to see which pages are visited. "
        "Strictly necessary cookies are always active. Optional cookies can be adjusted in "
        "Preferences at any stage.\n[Preferences]   [Continue]",
        "Cookie notice\nThis site keeps small data files in your browser. Essential files keep "
        "the site secure and functional; analytics files count visits. Details are in the "
        "Privacy Policy.",
        "By continuing to browse this site, you consent to the use of essential and analytics "
        "cookies as described in the Cookie Policy.",
        "Your privacy choices\nStrictly necessary cookies: always active\nPerformance cookies: "
        "active\nFunctional cookies: inactive\n[Done]",
        "This portal sets first-party cookies for session handling and load balancing. "
        "Third-party cookies are disabled by default. Cookie policy version 3.2.",
    ],
    "sent_from_phone": [
        "Sent from my mobile",
        "Sent from my tablet",
        "--\nSent from a handheld. Short replies by design.",
        "Typed on a small screen, so brevity is intended.",
        "Sent from my mobile. Formatting may differ from the desktop version.",
    ],
    "meeting_footer": [
        "________________________________\nJoin online: https://conf.example.net/j/58204417\n"
        "Conference ID: 582 044 17\nDial-in: +1 555 0142,,58204417#\n"
        "Video endpoints: 58204417@vc.example.net\n________________________________",
        "Conference bridge\nWeb link: https://bridge.example.org/r/7731-0045\n"
        "Dial-in numbers by region: https://bridge.example.org/numbers\nParticipant code: "
        "7731 0045",
        "Agenda and minutes: https://wiki.example.org/proj-atlas/notes\nThis invitation was "
        "generated automatically by the conferencing system.",
        "-- Conference bridge --\nHost: R. Okafor\nWeb: https://conf.example.net/j/90312266\n"
        "Dial-in: +44 20 7946 0999, code 903 122 66\n-- End of conference bridge --",
        "Web lobby: https://lobby.example.com/atlas-weekly\nLobby enabled; the host admits "
        "participants.\nDial-in: +1 555 0163, access 4471#",
    ],
    "page_chrome": [
        "Jump to main content\nDocs › Guides › Configuration\nOn this page: Overview "
        "· Parameters · Examples\n↑ Start of page",
        "« Previous article | Index | Following article »\n© 2024 Oakmere "
        "Engineering Ltd. All rights reserved. | Privacy | Terms of use | Sitemap",
        "Results 21–40 of 312\nSort by: relevance ▾   Per page: 20 ▾\n"
        "‹ 1 2 3 4 5 … 16 ›",
        "Print this page · Download PDF · Cite this page\nRevised 3 May 2023",
        "Table of contents\n1 Introduction\n2 Background\n3 Method\n4 Procedure\n5 Records\n"
        "Appendix A",
    ],
    "log_header": [
        "==== run log ====\nhost: build-agent-07\npid: 48213\nstart: 2023-06-14T09:15:02Z\n"
        "command: ./run_pipeline --shard 3/8 --config prod.yaml\nlevel: DEBUG\n=================",
        "2021-02-03T11:20:47.118Z DEBUG [main] bootstrap: loading configuration from "
        "/etc/indexer/indexer.conf",
        "### Session trace\n### hostname=node-31 build=7f3c2a1 go1.21.4 linux/amd64\n"
        "### flags: -v=2 -logtostderr",
        "---- worker 4 of 16 | pid 7712 | uptime 00:00:03 ----",
        "[boot] kernel 6.1.0-18-amd64 · cpus 8 · mem 15.6 GiB · init systemd 252",
    ],
}

# ---------------------------------------------------------------------------------------------
# Boilerplate C (dev, CC0): same categories, different (compact) style; 2 per category except
# sent_from_phone (1) -> 15
# ---------------------------------------------------------------------------------------------
BOILERPLATE_C = {
    "email_signature": [
        "j. marlowe · systems analyst · oakridge labs · +61 2 5550 1234",
        "[ Ines Moreira | Field Hydrologist | Riverbend Survey Co-op | ext. 2208 ]",
    ],
    "confidentiality_notice": [
        "[confidential] for the named addressee only; if misdirected, notify the sender and "
        "erase it.",
        "*** RESTRICTED - internal circulation only; copying needs the sender's prior "
        "clearance ***",
    ],
    "disclaimer": [
        "(individual views only; figures approximate)",
        "disclaimer: interim draft, subject to revision; the signed version governs.",
    ],
    "cookie_banner": [
        "cookies: essential + analytics only. [more] [continue]",
        "(i) this site keeps one session cookie and one analytics cookie -> /privacy",
    ],
    "sent_from_phone": [
        "(sent via mobile)",
    ],
    "meeting_footer": [
        "join: conf.example.org/r/77120 | dial-in: +1 555 0187 then 77120#",
        "~~ bridge 4410-2291 · host key held by the organiser · minutes -> "
        "wiki/notes/2291 ~~",
    ],
    "page_chrome": [
        "↑ start | print | index | « back",
        "sec 3.2 — p. 14/40 — rev C — uncontrolled if printed",
    ],
    "log_header": [
        '{"svc":"ingest","host":"n-04","pid":1187,"lvl":"debug","ts":"2022-11-02T17:03:44Z",'
        '"msg":"boot"}',
        "ingest-worker[1187]: boot seq=0 build=a91c0e2 cfg=/srv/ingest.toml",
    ],
}
C_COUNTS = {c: 2 for c in CATEGORIES}
C_COUNTS["sent_from_phone"] = 1

# ---------------------------------------------------------------------------------------------
# Reference A (train hard-reference FAQ snippets): banking77 15, clinc150 15, massive 10.
# Each tuple: (label_ids named by key, text). The key appears verbatim (case-insensitive).
# ---------------------------------------------------------------------------------------------
REFERENCE_A = {
    "banking77": [
        (["activate_my_card"],
         "Help centre › Cards › Card activation\nA newly issued card stays inactive until it is switched on. "
         "Open the Cards tab, select the new card and choose Activate, then enter the six-digit "
         "code printed on the carrier letter. Activation completes within a few seconds, after "
         "which the card is ready for chip and online use."),
        (["atm_support"],
         "Help centre › Cash › ATM support\nThe card can be used at cash machines that "
         "display the network logo printed on the front of the card. The map in the Cards tab "
         "lists nearby machines run by partner networks, with opening hours for machines located "
         "inside shops or stations."),
        (["apple_pay_or_google_pay"],
         "Help centre › Wallets › Apple Pay or Google Pay\nThe card can be added to a "
         "handset wallet from the card screen: select the card, choose Add to wallet and follow "
         "the prompts from the wallet provider. Purchases are then made by holding the handset "
         "near the terminal and confirming with face or fingerprint recognition."),
        (["change_pin"],
         "Help centre › Security › Change PIN\nThe PIN can be changed at any cash "
         "machine that offers PIN services: insert the card, choose PIN services, then enter the "
         "current PIN followed by the new one twice. The new PIN applies to chip payments and "
         "cash machines from the next use of the card."),
        (["country_support"],
         "Help centre › Eligibility › Supported countries\nAccounts are available to "
         "residents of the European Economic Area, the United Kingdom, Switzerland, Australia and "
         "the United States. Residents of further countries can join a waiting list in the app. "
         "The list of supported countries is revised each quarter."),
        (["age_limit"],
         "Help centre › Eligibility › Age requirement\nThe main account is open to "
         "customers aged 18 and over. Teenagers aged 13 to 17 can hold a linked junior account "
         "managed by a parent or guardian, with spending limits set by the adult holder."),
        (["automatic_top_up"],
         "Help centre › Top-ups › Automatic top-up\nAutomatic top-up adds a chosen "
         "amount from a linked card whenever the balance falls below a threshold set by the "
         "customer. The feature is switched on under Account › Top-up rules, where both the "
         "threshold and the amount can be edited at any stage."),
        (["getting_virtual_card"],
         "Help centre › Cards › Get virtual card\nA virtual card is created instantly "
         "in the Cards tab by choosing Add card › Virtual. It has its own number, expiry and "
         "security code, and can be frozen or deleted separately from the plastic card. Virtual "
         "cards are intended for online purchases."),
        (["verify_my_identity"],
         "Help centre › Identity checks › How to verify my identity\nIdentity checks "
         "are completed in the app with a photo of a passport, national identity card or driving "
         "licence, followed by a short selfie video. Most checks finish within ten minutes, and "
         "progress is shown under Profile › Identity."),
        (["terminate_account"],
         "Help centre › Account › Close account\nAn account can be closed from Profile "
         "› Close account once the remaining balance has been moved out. Statements from the "
         "past six years remain downloadable after closure."),
        (["edit_personal_details"],
         "Help centre › Profile › Edit personal details\nName, home address and contact "
         "number are changed under Profile › Edit personal details. A change of legal name "
         "needs a supporting document, such as a marriage certificate or deed poll, uploaded in "
         "the same screen."),
        (["exchange_rate"],
         "Help centre › Currencies › Exchange rate\nThe exchange rate shown in the app "
         "follows the interbank market rate and refreshes every few seconds during market hours. "
         "The rate for a conversion is fixed at the moment the conversion is confirmed."),
        (["lost_or_stolen_phone"],
         "Help centre › Security › Lost or stolen phone\nIf the handset with the banking "
         "app goes missing, log in from a computer and choose Security › Sign out all "
         "sessions. Sessions on the missing handset end at once, and a new handset can be "
         "registered after a fresh identity check."),
        (["visa_or_mastercard"],
         "Help centre › Cards › Visa or Mastercard\nCards issued in Europe run on the "
         "Mastercard network; cards issued in the United States and Australia run on Visa. The "
         "network is printed on the front of the card and shown in Card details. Both networks "
         "are accepted by the same merchants in almost all regions."),
        (["transfer_timing"],
         "Help centre › Transfers › Transfer timing\nTransfers between customers of the "
         "bank arrive instantly. Domestic bank transfers usually arrive within two hours on "
         "working days, and international SWIFT transfers take one to five working days "
         "depending on the intermediary banks."),
    ],
    "clinc150": [
        (["routing"],
         "Assistant help › Routing number\nThe assistant can read out the nine-digit routing "
         "number of a linked account. The same number appears in the account details section of "
         "the bank's website."),
        (["credit_limit"],
         "Assistant help › Credit limit\nFor a linked card, the assistant reports the current "
         "credit limit and the remaining available credit. Limits are set by the issuer; the "
         "assistant reads the figure from the most recent statement sync."),
        (["redeem_rewards"],
         "Assistant help › Redeem rewards\nPoints earned on a linked card can be redeemed for "
         "statement credits or airline miles through the issuer's portal. The assistant opens the "
         "portal and lists the redemption options available."),
        (["plug_type"],
         "Assistant help › Plug type\nThe assistant names the socket standard and mains "
         "voltage for a destination country, for example Type G at 230 V in the United Kingdom "
         "and Type A or B at 120 V in the United States, and says whether an adapter is needed."),
        (["lost_luggage"],
         "Assistant help › Lost luggage\nFor a delayed or missing bag, the assistant gives the "
         "airline's baggage desk hours and a link to the online claim form. A property "
         "irregularity report filed at the airport speeds up tracing."),
        (["tire_pressure"],
         "Assistant help › Tire pressure\nWith a connected vehicle, the assistant reads each "
         "tire's pressure in psi and compares it with the value on the door-jamb placard. "
         "Readings are most accurate on cold tires, before driving more than a mile."),
        (["update_playlist"],
         "Assistant help › Update playlist\nSongs can be added to or removed from a saved "
         "playlist by naming the song and the playlist. Changes sync to the linked streaming "
         "account within a minute."),
        (["ingredient_substitution"],
         "Assistant help › Ingredient substitution\nThe assistant suggests common swaps, such "
         "as plain yogurt for sour cream or applesauce for oil in baking, along with the quantity "
         "to use. Substitutions made for allergy reasons are marked with a caution symbol."),
        (["food_last"],
         "Assistant help › Food shelf life\nThe assistant gives typical storage durations, "
         "for example three to five days for cooked rice in the fridge or up to a year for hard "
         "cheese in the freezer. Figures follow published food-safety guidance."),
        (["timer"],
         "Assistant help › Set a timer\nTimers run on the speaker or phone and can be named, "
         "for example a pasta timer. Several timers can run at once, and each announces its name "
         "when it finishes."),
        (["pto_balance"],
         "Assistant help › Time-off balance\nFor employers connected to the HR system, the "
         "assistant reports remaining vacation days and sick-leave hours for the current year, "
         "as recorded in the latest payroll run."),
        (["w2"],
         "Assistant help › W-2 form\nThe assistant states when the employer posts the W-2 "
         "form in the payroll portal, usually by the end of January, and can open the portal page "
         "where the PDF is downloaded for filing."),
        (["change_language"],
         "Assistant settings › Change language\nThe spoken and display language of the "
         "assistant can be switched to any of 24 supported languages. After switching, wake-word "
         "detection may ask for a short retraining sample."),
        (["whisper_mode"],
         "Assistant settings › Whisper mode\nIn whisper mode the assistant answers quietly "
         "when spoken to in a whisper, which suits late hours. The mode is switched on in the "
         "device settings and stays active until it is switched off."),
        (["tell_joke"],
         "Assistant help › Tell a joke\nOn request the assistant will tell a joke from a "
         "curated collection of family-friendly one-liners and puns. Repeated requests draw from "
         "the collection without repeats until it is exhausted."),
    ],
    "massive": [
        (["alarm_set"],
         "Voice assistant guide › Set alarm\nAn alarm can be set for a specific clock hour or "
         "relative to the present moment, and can repeat on chosen weekdays. Each alarm has a "
         "label and a sound, both editable from the companion screen."),
        (["play_podcasts"],
         "Voice assistant guide › Play podcast\nThe assistant can play podcast episodes from "
         "the linked provider by show name or episode number, and resumes from the last position "
         "heard on any linked speaker."),
        (["takeaway_order"],
         "Voice assistant guide › Order takeaway\nWith a linked delivery service, the "
         "assistant can reorder a previous takeaway meal or read out the menu of a saved "
         "restaurant before placing the new order. Payment uses the card stored with the service."),
        (["iot_hue_lightdim"],
         "Voice assistant guide › Dim lights\nConnected bulbs can be dimmed by percentage or "
         "by named scene, per room or across the whole house. Dimming below 10 percent is "
         "supported only by bulbs with a low-level driver."),
        (["transport_taxi"],
         "Voice assistant guide › Book a taxi\nThe assistant can book a taxi through the "
         "linked ride provider, confirming the pickup point and the estimated fare before sending "
         "the booking. Driver arrival updates are read out on request."),
        (["datetime_convert"],
         "Voice assistant guide › Time zone conversion\nThe assistant converts a clock "
         "reading between cities, for example 9:00 in Chicago to the equivalent hour in Singapore, "
         "and accounts for daylight-saving changes on the given day."),
        (["audio_volume_mute"],
         "Voice assistant guide › Mute audio\nMute audio silences the speaker output while "
         "keeping the microphone active, so the wake word still works. Saying the wake word "
         "followed by unmute restores the previous level."),
        (["recommendation_movies"],
         "Voice assistant guide › Movie recommendation\nThe assistant can suggest films by "
         "genre, actor or decade, drawing on the watch history of the linked streaming profile, "
         "and gives showtimes at nearby cinemas on request."),
        (["iot_coffee"],
         "Voice assistant guide › Make coffee\nA connected coffee machine can brew a preset "
         "drink by voice, such as a single espresso or a large filter cup. The machine needs "
         "water and beans loaded, and the assistant reports when brewing starts."),
        (["lists_remove"],
         "Voice assistant guide › Remove from list\nItems can be deleted from a named "
         "shopping or to-do list by saying the item and the list name. Deleted items stay in a "
         "recently-deleted section for thirty days."),
    ],
}
REF_COUNTS = {"banking77": 15, "clinc150": 15, "massive": 10}

# ---------------------------------------------------------------------------------------------
# Class-signal blocklist for boilerplate (whole-word, case-insensitive; stems end with '*').
# ---------------------------------------------------------------------------------------------
BLOCK_GROUPS = {
    "refund": ["refund*", "reimburs*", "chargeback*", "money back", "return", "returns",
               "returned", "compensation"],
    "urgency": ["urgent*", "asap", "immediate*", "promptly", "deadline*", "priority",
                "critical", "emergency", "time-sensitive", "quickly", "soon", "now", "hurry",
                "important", "overdue", "final notice", "action required"],
    "spam_marketing": ["free", "offer*", "win", "winner*", "won", "prize*", "claim*", "click*",
                       "subscribe*", "unsubscribe*", "opt-out", "opt out", "promo*",
                       "discount*", "deal", "deals", "sale", "sales", "buy*", "purchase*",
                       "limited", "exclusive*", "bonus*", "gift*", "voucher*", "cash",
                       "reward*", "congratulation*", "guarantee*", "cheap*", "newsletter*",
                       "advert*", "ads", "marketing", "personalis*", "personaliz*", "special",
                       "txt", "stop", "reply", "call", "calls", "shop*", "price*", "cost*",
                       "spam", "save", "savings", "£", "$", "€", "%"],
    "emotion": ["happy", "happi*", "glad", "joy*", "delight*", "pleas*ed", "pleasure", "love*",
                "lovely", "like", "liked", "enjoy*", "excit*", "thrill*", "grateful",
                "gratitude", "thank*", "appreciat*", "sad*", "unhappy", "sorry", "regret*",
                "apolog*", "afraid", "fear*", "scared", "worr*", "anxi*", "nervous*", "angry",
                "anger", "annoy*", "frustrat*", "furious", "upset", "disappoint*", "disgust*",
                "hate*", "surpris*", "shock*", "amazing", "awesome", "wonderful", "terrible",
                "awful", "horrible", "proud", "pride", "relie*", "hope*", "optimis*", "curious",
                "confus*", "embarrass*", "grief", "griev*", "caring", "care", "admir*", "amus*",
                "fun", "funny", "joke*", "lol", "kind", "warm*", "welcome*", "dear", "hi",
                "hello", "cheers", "best", "great", "good", "bad", "excellent", "nice",
                "perfect", "sincere*", "mood", "feel*", "emotion*", "wish*", "remorse", "desire*",
                "approv*", "disapprov*", "interest*", "positive", "negative", "neutral"],
    "polarity_negation": ["yes", "no", "not", "never", "nothing", "none", "cannot", "can't",
                          "n't", "true", "false", "maybe", "unsure", "correct", "incorrect",
                          "other than", "wrong"],
    "request_greeting": ["please", "kindly", "greeting*", "goodbye", "bye", "regards",
                         "request*", "question*", "help", "support", "how", "why", "when",
                         "what", "where", "who", "ask*"],
    "container_markers": ["forward*", "fwd", "wrote:", "original message", "from:", "to:",
                          "subject:", "sent:", "quoted", "reference", "retrieved"],
    "topical": ["account*", "card*", "pin", "passcode*", "password*", "transfer*", "payment*",
                "pay", "paid", "fee", "fees", "charge*", "balance", "bank*", "money", "top-up",
                "deposit*", "withdraw*", "loan*", "credit*", "debit*", "exchange*", "currenc*",
                "identity", "verif*", "fraud*", "unauthori*", "stolen", "lost", "phone*",
                "device*", "app", "apps", "email*", "e-mail*", "mail*", "contact*", "text*",
                "sms", "meeting*", "calendar*", "schedul*", "remind*", "event*", "alarm*",
                "timer*", "time", "times", "date", "dates", "today", "tomorrow", "weather",
                "forecast*", "travel*", "flight*", "hotel*", "home", "work", "office*",
                "company", "companies", "building*", "place*", "person*", "people", "film*",
                "movie*", "album*", "artist*", "music*", "song*", "play*", "news", "list",
                "lists", "recipe*", "cook", "cooks", "cooked", "cooking", "cookery", "food*", "restaurant*", "order*", "deliver*",
                "address", "location*", "language*", "translat*", "update*", "next", "share*",
                "social", "recommend*", "review*", "rating*", "rate", "stars", "toxic*",
                "insult*", "legitimate", "audio", "volume", "light", "lights", "voice",
                "chat*", "room", "rooms", "service*", "check*", "status", "report*",
                "sign-up", "sign up", "sign in", "log in", "login", "store", "stores",
                "product*", "skip", "information", "info", "error*", "fail*", "declin*",
                "pending", "expir*", "direct", "personal", "statement*", "advice", "about",
                "reader*", "recipient*", "received", "receive*", "allowed", "reject*",
                "accept*", "settings", "setting", "wifi", "parking", "gym", "pets", "spa",
                "insurance", "tax", "taxes", "income", "salary", "payday", "holiday*",
                "vacation*", "definition*", "spelling", "calculat*", "directions", "traffic",
                "fuel", "gas", "tire*", "car", "cars", "taxi", "train", "ticket*", "game*",
                "podcast*", "radio", "audiobook*", "coffee", "vacuum", "plug*", "currency",
                "stock*", "mortgage", "overdraft", "cheque*", "withdrawal*", "atm", "visa",
                "mastercard", "limit", "limits", "clinical", "medic*", "drug*", "side effect*",
                "doctor*", "health*", "symptom*", "delete*", "remove*", "cancel*", "freeze*",
                "frozen", "block*", "compromis*", "security", "secure"],
}
# Words from BLOCK_GROUPS that one authored boilerplate category legitimately needs; each
# exemption is listed with its reason and applies only to that category.
EXEMPT = {
    # "secure" in the cookie banner describes what essential cookies do; it names no label and
    # no verifier question asks about security.
    ("cookie_banner", "secure"),
}


def _pattern(word):
    esc = re.escape(word.rstrip("*"))
    esc = esc.replace(r"\ ", r"\s+")
    left = r"(?<![\w])" if word[0].isalnum() else ""
    if word.endswith("*"):
        right = r""
    elif word[-1].isalnum():
        right = r"(?![\w])"
    else:
        right = ""
    return re.compile(left + esc + right, re.IGNORECASE)


def load_keys():
    """{dataset: [(label_id, key, kind, parent)]} for every keys file."""
    out = {}
    for path in sorted(glob.glob(os.path.join(KEYS_DIR, "*.keys.json"))):
        d = json.load(open(path, encoding="utf-8"))
        rows = []
        for lab in d["labels"]:
            if lab.get("key"):
                rows.append((lab["label_id"], lab["key"], lab.get("kind"), lab.get("parent")))
        out[d["dataset"]] = rows
    return out


def key_hits(text, rows):
    hits = []
    for label_id, key, _kind, _parent in rows:
        pat = re.compile(r"(?<![\w])" + re.escape(key).replace(r"\ ", r"\s+") + r"(?![\w])",
                         re.IGNORECASE)
        if pat.search(text):
            hits.append(label_id)
    return sorted(set(hits))


def shingles(text, n=5):
    t = re.sub(r"\s+", " ", text.lower()).strip()
    if len(t) < n:
        return {t}
    return {t[i:i + n] for i in range(len(t) - n + 1)}


def jaccard(a, b):
    sa, sb = shingles(a), shingles(b)
    return len(sa & sb) / max(1, len(sa | sb))


def build():
    keys = load_keys()
    bA, bC, rA = [], [], []
    for cat in CATEGORIES:
        for i, text in enumerate(BOILERPLATE_A[cat], 1):
            bA.append({
                "id": f"boilerplate_A.{cat}.{i:02d}", "pool": "train", "corpus": "boilerplate_A",
                "category": cat, "style": STYLE_A, "text": text, "n_chars": len(text),
                "named_label_ids": [], "licence": "CC0-1.0", "authored_by": AUTHOR,
            })
        for i, text in enumerate(BOILERPLATE_C[cat], 1):
            bC.append({
                "id": f"boilerplate_C.{cat}.{i:02d}", "pool": "dev", "corpus": "boilerplate_C",
                "category": cat, "style": STYLE_C, "text": text, "n_chars": len(text),
                "named_label_ids": [], "licence": "CC0-1.0", "authored_by": AUTHOR,
            })
    for ds in sorted(REFERENCE_A):
        idx = {lid: (key, kind, parent) for lid, key, kind, parent in keys[ds]}
        for i, (named, text) in enumerate(REFERENCE_A[ds], 1):
            rA.append({
                "id": f"reference_A.{ds}.{i:02d}", "pool": "train", "corpus": "reference_A",
                "category": f"faq_{ds}", "dataset": ds, "text": text, "n_chars": len(text),
                "named_label_ids": sorted(named),
                "named_keys": [idx[lid][0] for lid in sorted(named)],
                "parent_label_ids": sorted({idx[lid][2] for lid in named if idx[lid][2]}),
                "licence": "CC-BY-4.0", "authored_by": AUTHOR,
            })
    return keys, sorted(bA, key=lambda r: r["id"]), sorted(bC, key=lambda r: r["id"]), \
        sorted(rA, key=lambda r: r["id"])


def check(keys, bA, bC, rA):
    errs = []
    all_rows = [row for rows in keys.values() for row in rows]
    compiled = [(g, w, _pattern(w)) for g, ws in BLOCK_GROUPS.items() for w in ws]
    # counts
    if len(bA) != 40 or len(bC) != 15 or len(rA) != 40:
        errs.append(f"counts A={len(bA)} C={len(bC)} ref={len(rA)}")
    for cat in CATEGORIES:
        na = sum(r["category"] == cat for r in bA)
        nc = sum(r["category"] == cat for r in bC)
        if na != 5 or nc != C_COUNTS[cat]:
            errs.append(f"category {cat}: A={na} C={nc}")
    for ds, n in REF_COUNTS.items():
        if sum(r["dataset"] == ds for r in rA) != n:
            errs.append(f"reference dataset {ds} count")
    everything = bA + bC + rA
    if len({r["id"] for r in everything}) != len(everything):
        errs.append("duplicate ids")
    if len({r["text"] for r in everything}) != len(everything):
        errs.append("duplicate texts")
    # boilerplate: no class signal
    for r in bA + bC:
        hits = key_hits(r["text"], all_rows)
        if hits:
            errs.append(f"{r['id']}: label key hit {hits}")
        for g, w, pat in compiled:
            if (r["category"], w.rstrip("*")) in EXEMPT:
                continue
            m = pat.search(r["text"])
            if m:
                errs.append(f"{r['id']}: blocklist[{g}] '{w}' -> '{m.group(0)}'")
    # reference: named keys present, no other key of the same dataset
    ref_block = [(g, w, _pattern(w)) for g in ("urgency", "emotion", "polarity_negation",
                                              "container_markers", "spam_marketing")
                 for w in BLOCK_GROUPS[g]]
    ref_allow = {"offer*", "claim*", "limited", "reward*", "cash", "save", "savings", "call",
                 "shop*", "purchase*", "stop", "sale", "sales", "now", "%", "$", "£",
                 "€", "gift*", "price*", "cost*"}
    for r in rA:
        hits = key_hits(r["text"], keys[r["dataset"]])
        if hits != r["named_label_ids"]:
            errs.append(f"{r['id']}: key hits {hits} != named {r['named_label_ids']}")
        if not r["named_label_ids"]:
            errs.append(f"{r['id']}: names no label")
        masked = r["text"]
        for key in r["named_keys"]:
            masked = re.sub(re.escape(key), " ", masked, flags=re.IGNORECASE)
        for g, w, pat in ref_block:
            if w in ref_allow:
                continue
            m = pat.search(masked)
            if m:
                errs.append(f"{r['id']}: reference blocklist[{g}] '{w}' -> '{m.group(0)}'")
    # near-duplicates
    for bank, name in ((bA, "A"), (bC, "C"), (rA, "ref")):
        for i in range(len(bank)):
            for j in range(i + 1, len(bank)):
                jac = jaccard(bank[i]["text"], bank[j]["text"])
                if jac >= 0.5:
                    errs.append(f"{name} near-dup {bank[i]['id']} ~ {bank[j]['id']} {jac:.2f}")
    worst = 0.0
    for a in bA:
        for c in bC:
            jac = jaccard(a["text"], c["text"])
            worst = max(worst, jac)
            if jac >= 0.5:
                errs.append(f"A~C {a['id']} ~ {c['id']} {jac:.2f}")
    return errs, worst


def write(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    keys, bA, bC, rA = build()
    errs, worst = check(keys, bA, bC, rA)
    if errs:
        print("\n".join(errs))
        print(f"{len(errs)} violations; nothing written")
        sys.exit(1)
    write(os.path.join(HERE, "boilerplate_A.jsonl"), bA)
    write(os.path.join(HERE, "boilerplate_C.jsonl"), bC)
    write(os.path.join(HERE, "reference_A.jsonl"), rA)
    print(f"ok: boilerplate_A={len(bA)} boilerplate_C={len(bC)} reference_A={len(rA)}; "
          f"max A~C 5-gram Jaccard={worst:.3f}")


if __name__ == "__main__":
    main()
