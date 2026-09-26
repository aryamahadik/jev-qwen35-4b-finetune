#!/usr/bin/env python3
"""Write the fixed Choice/Noul label keys (DESIGN field rule 2, section 4.2, deviation D8).

Outputs (all deterministic, sorted, no randomness):
  assets/labels/keys/<dataset>.keys.json
  assets/labels/confusables.json
  assets/labels/label_inventory.json

Label lists are loaded from the pinned sources with the scout loaders (system python3,
datasets 4.8.5). GitHub files (CLINC domains.json, HINT3 v2 CSVs, NLU++ ontology and folds,
GoEmotions ekman_mapping.json) are fetched at pinned commits into a cache outside the repo
(OD_GH_CACHE, default ~/.cache/huggingface/opendecide_github).

The keys themselves are authored below (authored_by "llm:claude:label-key-author").
Keys are natural 1-5 word names, unique within a dataset, never raw ids and never gold hints.
Run:  python3 assets/labels/make_label_keys.py
"""
import collections
import hashlib
import json
import os
import re
import sys

AUTHOR = "llm:claude:label-key-author"
CREATED = "2026-09-25"
SCHEMA = "od-keys-1.0"
HERE = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(HERE, "keys")
GH_CACHE = os.environ.get("OD_GH_CACHE", os.path.expanduser("~/.cache/huggingface/opendecide_github"))
KINDS = {"intent", "domain", "scenario", "class", "superclass", "emotion_group", "module", "level", "predicate", "oos"}
KIND_ORDER = ["domain", "scenario", "superclass", "intent", "module", "class", "emotion_group", "predicate", "level", "oos"]
# words that would read as a gold hint or collide with fixed Choice-2/3 keys and the none option
BANNED_TOKENS = {"yes", "no", "true", "false", "correct", "incorrect", "gold", "answer", "none", "label", "option", "other", "cannot"}

PIN = {
    "banking77": ("legacy-datasets/banking77", None, "f54121560de48f2852f90be299010d1d6dc612ec"),
    "clinc150": ("clinc/clinc_oos", "plus", "155b9c710419136e17307b80d0a13e68cd46b4ec"),
    "massive": ("AmazonScience/massive", "refs/convert/parquet data_dir=en-US", "ed58ac423a2f4121720918bf5301577edce4ffd3"),
    "dbpedia14": ("fancyzhx/dbpedia_14", None, "9abd46cf7fc8b4c64290f26993c540b92aa145ac"),
    "goemotions": ("google-research-datasets/go_emotions", "raw", "add492243ff905527e67aeb8b80c082af02207c3"),
    "clothing": ("saattrupdan/womens-clothing-ecommerce-reviews", None, "4e788183125a6143d8bdba24e58f1efda2e4b48f"),
    "drug": ("lewtun/drug-reviews", None, "07722f82287d0a94ddc80151390f34e65183b2c3"),
    "minds14": ("PolyAI/minds14", "en-US/en-GB/en-AU", "40ce77cb32a384e4d50a568e1ec39ac804019d33"),
    "snips": ("benayas/snips", None, "16915b895754dd4028068abe52b6851a904977d7"),
    "tfns": ("zeroshot/twitter-financial-news-sentiment", None, "ccbe24de388e287beb92dd393a335c376b350ac3"),
    "sst5": ("stanfordnlp/sst", "refs/convert/parquet data_dir=default", "8a7d55ee01d70b8ae53e0b3c66a83b2a6198c2a7"),
    "supertweeteval": ("cardiffnlp/super_tweeteval", "tweet_sentiment", "a10ac3d27a3499e870b6371df64c14e5a656131a"),
    "sms_spam": ("ucirvine/sms_spam", "plain_text", "cae486f927c250fe1d4a5b55f11357964ed1646c"),
    "civil": ("google/civil_comments", None, "f2970eb3a55777454c94069077cc8d9b5866312d"),
    "mhs": ("ucberkeley-dlab/measuring-hate-speech", None, "5468f6e118396646b02a2f691e771f6b6d9502ea"),
}
GH = {
    "clinc_domains": ("clinc/oos-eval", "828f8093932c8fe6ca7936c3d2e52903b1c523de", "data/domains.json"),
    "hint3_sofmattress_test": ("hellohaptik/HINT3", "99965c892ea9a6801a87083d3861b0b04c91a4e7", "dataset/v2/test/sofmattress_test.csv"),
    "hint3_sofmattress_train": ("hellohaptik/HINT3", "99965c892ea9a6801a87083d3861b0b04c91a4e7", "dataset/v2/train/sofmattress_train.csv"),
    "hint3_curekart_test": ("hellohaptik/HINT3", "99965c892ea9a6801a87083d3861b0b04c91a4e7", "dataset/v2/test/curekart_test.csv"),
    "hint3_curekart_train": ("hellohaptik/HINT3", "99965c892ea9a6801a87083d3861b0b04c91a4e7", "dataset/v2/train/curekart_train.csv"),
    "nlupp_ontology": ("PolyAI-LDN/task-specific-datasets", "57ec275d8078af65b7731c2a98be812d844a6d6b", "nlupp/data/ontology.json"),
    "goemotions_ekman": ("google-research/google-research", "2adf640a14f11025ae5a9d0ec493b78530d276d3", "goemotions/data/ekman_mapping.json"),
    "goemotions_sentiment": ("google-research/google-research", "2adf640a14f11025ae5a9d0ec493b78530d276d3", "goemotions/data/sentiment_mapping.json"),
}

# --------------------------------------------------------------------------------------------
# Authored keys
# --------------------------------------------------------------------------------------------
BANKING77 = {
    "activate_my_card": "card activation",
    "age_limit": "age requirement",
    "apple_pay_or_google_pay": "Apple Pay or Google Pay",
    "atm_support": "ATM support",
    "automatic_top_up": "automatic top-up",
    "balance_not_updated_after_bank_transfer": "balance not updated after transfer",
    "balance_not_updated_after_cheque_or_cash_deposit": "balance not updated after deposit",
    "beneficiary_not_allowed": "beneficiary not allowed",
    "cancel_transfer": "cancel a transfer",
    "card_about_to_expire": "card about to expire",
    "card_acceptance": "card acceptance",
    "card_arrival": "card arrival",
    "card_delivery_estimate": "card delivery estimate",
    "card_linking": "linking card to app",
    "card_not_working": "card not working",
    "card_payment_fee_charged": "card payment fee",
    "card_payment_not_recognised": "unrecognised card payment",
    "card_payment_wrong_exchange_rate": "wrong rate on card payment",
    "card_swallowed": "card swallowed by ATM",
    "cash_withdrawal_charge": "cash withdrawal fee",
    "cash_withdrawal_not_recognised": "unrecognised cash withdrawal",
    "change_pin": "change PIN",
    "compromised_card": "compromised card",
    "contactless_not_working": "contactless not working",
    "country_support": "supported countries",
    "declined_card_payment": "declined card payment",
    "declined_cash_withdrawal": "declined cash withdrawal",
    "declined_transfer": "declined transfer",
    "direct_debit_payment_not_recognised": "unrecognised direct debit",
    "disposable_card_limits": "disposable card limits",
    "edit_personal_details": "edit personal details",
    "exchange_charge": "currency exchange fee",
    "exchange_rate": "exchange rate",
    "exchange_via_app": "exchange currency in app",
    "extra_charge_on_statement": "extra charge on statement",
    "failed_transfer": "failed transfer",
    "fiat_currency_support": "fiat currency support",
    "get_disposable_virtual_card": "get disposable virtual card",
    "get_physical_card": "physical card PIN",
    "getting_spare_card": "additional card",
    "getting_virtual_card": "get virtual card",
    "lost_or_stolen_card": "lost or stolen card",
    "lost_or_stolen_phone": "lost or stolen phone",
    "order_physical_card": "order physical card",
    "passcode_forgotten": "forgotten passcode",
    "pending_card_payment": "pending card payment",
    "pending_cash_withdrawal": "pending cash withdrawal",
    "pending_top_up": "pending top-up",
    "pending_transfer": "pending transfer",
    "pin_blocked": "blocked PIN",
    "receiving_money": "receiving money",
    "Refund_not_showing_up": "refund not showing",
    "request_refund": "request a refund",
    "reverted_card_payment?": "reverted card payment",
    "supported_cards_and_currencies": "supported cards and currencies",
    "terminate_account": "close account",
    "top_up_by_bank_transfer_charge": "bank transfer top-up fee",
    "top_up_by_card_charge": "card top-up fee",
    "top_up_by_cash_or_cheque": "cash or cheque top-up",
    "top_up_failed": "failed top-up",
    "top_up_limits": "top-up limits",
    "top_up_reverted": "reverted top-up",
    "topping_up_by_card": "top up by card",
    "transaction_charged_twice": "charged twice",
    "transfer_fee_charged": "transfer fee",
    "transfer_into_account": "transfer into account",
    "transfer_not_received_by_recipient": "transfer not received by recipient",
    "transfer_timing": "transfer timing",
    "unable_to_verify_identity": "unable to verify identity",
    "verify_my_identity": "verify my identity",
    "verify_source_of_funds": "verify source of funds",
    "verify_top_up": "verify a top-up",
    "virtual_card_not_working": "virtual card not working",
    "visa_or_mastercard": "Visa or Mastercard",
    "why_verify_identity": "why verify identity",
    "wrong_amount_of_cash_received": "wrong cash amount received",
    "wrong_exchange_rate_for_cash_withdrawal": "wrong rate on cash withdrawal",
}
# labels whose source name misnames the content: the key names what the source examples are about
BANKING77_KEY_NOTES = {
    "get_physical_card": "source examples are about finding or receiving the PIN of the physical card (scout 2.1; simonmesmith)",
    "getting_spare_card": "source examples ask for extra or duplicate cards",
    "card_linking": "source examples ask how to link or show a card in the app",
}

CLINC_DOMAINS = {
    "auto_and_commute": "auto and commute",
    "banking": "banking",
    "credit_cards": "credit cards",
    "home": "home",
    "kitchen_and_dining": "kitchen and dining",
    "meta": "assistant settings and control",
    "small_talk": "small talk",
    "travel": "travel",
    "utility": "utilities",
    "work": "work",
}
CLINC150 = {
    # banking
    "freeze_account": "freeze account", "routing": "routing number", "pin_change": "change PIN",
    "bill_due": "bill due date", "pay_bill": "pay a bill", "account_blocked": "blocked account",
    "interest_rate": "interest rate", "min_payment": "minimum payment", "bill_balance": "bill amount owed",
    "transfer": "money transfer", "order_checks": "order checks", "balance": "account balance",
    "spending_history": "spending history", "transactions": "recent transactions", "report_fraud": "report fraud",
    # credit_cards
    "replacement_card_duration": "replacement card wait", "expiration_date": "card expiration date",
    "damaged_card": "damaged card", "improve_credit_score": "improve credit score", "report_lost_card": "report lost card",
    "card_declined": "declined card", "credit_limit_change": "change credit limit", "apr": "annual percentage rate",
    "redeem_rewards": "redeem rewards", "credit_limit": "credit limit", "rewards_balance": "rewards balance",
    "application_status": "card application status", "credit_score": "credit score", "new_card": "apply for new card",
    "international_fees": "foreign transaction fees",
    # kitchen_and_dining
    "food_last": "food shelf life", "confirm_reservation": "confirm reservation", "how_busy": "restaurant wait time",
    "ingredients_list": "ingredients list", "calories": "calorie count", "nutrition_info": "nutrition information",
    "recipe": "recipe", "restaurant_reviews": "restaurant reviews", "restaurant_reservation": "restaurant reservation",
    "meal_suggestion": "meal suggestion", "restaurant_suggestion": "restaurant suggestion",
    "cancel_reservation": "cancel reservation", "ingredient_substitution": "ingredient substitution",
    "cook_time": "cooking time", "accept_reservations": "accepts reservations",
    # home
    "what_song": "identify current song", "play_music": "play music", "todo_list_update": "update to-do list",
    "reminder": "check reminders", "reminder_update": "set a reminder", "calendar_update": "update calendar",
    "order_status": "order status", "update_playlist": "update playlist", "shopping_list": "check shopping list",
    "calendar": "check calendar", "next_song": "next song", "order": "place an order", "todo_list": "check to-do list",
    "shopping_list_update": "update shopping list", "smart_home": "smart home control",
    # auto_and_commute
    "current_location": "current location", "oil_change_when": "when to change oil", "oil_change_how": "how to change oil",
    "uber": "book a rideshare", "traffic": "traffic conditions", "tire_pressure": "tire pressure",
    "schedule_maintenance": "schedule car service", "gas": "fuel level", "mpg": "fuel economy",
    "distance": "travel time estimate", "directions": "directions", "last_maintenance": "last car service",
    "gas_type": "fuel type", "tire_change": "when to replace tires", "jump_start": "jump-start a car",
    # travel
    "plug_type": "plug type", "travel_notification": "tell bank about travel", "translate": "translation",
    "flight_status": "flight status", "international_visa": "visa requirements", "timezone": "time zone",
    "exchange_rate": "exchange rate", "travel_suggestion": "travel suggestion", "travel_alert": "travel advisory",
    "vaccines": "travel vaccines", "lost_luggage": "lost luggage", "book_flight": "book a flight",
    "book_hotel": "book a hotel", "carry_on": "carry-on rules", "car_rental": "car rental",
    # utility
    "weather": "weather", "alarm": "set an alarm", "date": "today's date", "find_phone": "find my phone",
    "share_location": "share location", "timer": "set a timer", "make_call": "make a call", "calculator": "calculation",
    "definition": "word definition", "measurement_conversion": "unit conversion", "flip_coin": "flip a coin",
    "spelling": "spelling", "time": "current time", "roll_dice": "roll dice", "text": "send a text",
    # work
    "pto_request_status": "time-off request status", "next_holiday": "next holiday", "insurance_change": "change insurance",
    "insurance": "insurance benefits", "meeting_schedule": "check meetings", "payday": "payday", "taxes": "taxes",
    "income": "income", "rollover_401k": "401k rollover", "pto_balance": "time-off balance", "pto_request": "request time off",
    "w2": "W-2 form", "schedule_meeting": "schedule a meeting", "direct_deposit": "direct deposit", "pto_used": "time off used",
    # small_talk
    "who_made_you": "who made you", "meaning_of_life": "meaning of life", "who_do_you_work_for": "who you work for",
    "do_you_have_pets": "assistant's pets", "what_are_your_hobbies": "assistant's hobbies", "fun_fact": "fun fact",
    "what_is_your_name": "assistant's name", "where_are_you_from": "where you are from", "goodbye": "goodbye",
    "thank_you": "thanks", "greeting": "greeting", "tell_joke": "tell a joke", "are_you_a_bot": "are you a bot",
    "how_old_are_you": "assistant's age", "what_can_i_ask_you": "what I can ask",
    # meta
    "change_speed": "change speaking speed", "user_name": "user's name", "whisper_mode": "whisper mode",
    "yes": "affirmative reply", "change_volume": "change volume", "no": "negative reply",
    "change_language": "change language", "repeat": "repeat that", "change_accent": "change voice or accent",
    "cancel": "cancel current action", "sync_device": "connect to phone", "change_user_name": "change user's name",
    "change_ai_name": "rename assistant", "reset_settings": "factory reset", "maybe": "unsure reply",
}

MASSIVE_SCENARIOS = {
    "alarm": "alarms", "audio": "audio volume", "calendar": "calendar", "cooking": "cooking",
    "datetime": "date and time", "email": "email", "general": "general chat", "iot": "smart home devices",
    "lists": "lists", "music": "music", "news": "news", "play": "media playback", "qa": "general questions",
    "recommendation": "recommendations", "social": "social media", "takeaway": "takeaway food",
    "transport": "transport", "weather": "weather",
}
MASSIVE = {
    "alarm_query": "check alarms", "alarm_remove": "remove alarm", "alarm_set": "set alarm",
    "audio_volume_down": "volume down", "audio_volume_mute": "mute audio", "audio_volume_other": "volume settings",
    "audio_volume_up": "volume up",
    "calendar_query": "calendar question", "calendar_remove": "remove calendar event", "calendar_set": "add calendar event",
    "cooking_query": "cooking question", "cooking_recipe": "recipe request",
    "datetime_convert": "time zone conversion", "datetime_query": "date or time question",
    "email_addcontact": "add email contact", "email_query": "check email", "email_querycontact": "contact details question",
    "email_sendemail": "send an email",
    "general_greet": "greeting", "general_joke": "tell a joke", "general_quirky": "quirky chat",
    "iot_cleaning": "robot vacuum cleaning", "iot_coffee": "make coffee", "iot_hue_lightchange": "change light color",
    "iot_hue_lightdim": "dim lights", "iot_hue_lightoff": "lights off", "iot_hue_lighton": "lights on",
    "iot_hue_lightup": "brighten lights", "iot_wemo_off": "smart plug off", "iot_wemo_on": "smart plug on",
    "lists_createoradd": "create or add to list", "lists_query": "check a list", "lists_remove": "remove from list",
    "music_dislikeness": "disliking a song", "music_likeness": "liking a song", "music_query": "music question",
    "music_settings": "music playback settings",
    "news_query": "news request",
    "play_audiobook": "play audiobook", "play_game": "play a game", "play_music": "play music",
    "play_podcasts": "play podcast", "play_radio": "play radio",
    "qa_currency": "currency rate question", "qa_definition": "definition question", "qa_factoid": "factual question",
    "qa_maths": "math question", "qa_stock": "stock price question",
    "recommendation_events": "event recommendation", "recommendation_locations": "place recommendation",
    "recommendation_movies": "movie recommendation",
    "social_post": "post on social media", "social_query": "check social media",
    "takeaway_order": "order takeaway", "takeaway_query": "takeaway question",
    "transport_query": "transport question", "transport_taxi": "book a taxi", "transport_ticket": "book transport ticket",
    "transport_traffic": "traffic update",
    "weather_query": "weather request",
}

DBPEDIA_CLASSES = {
    "Company": "company", "EducationalInstitution": "educational institution", "Artist": "artist",
    "Athlete": "athlete", "OfficeHolder": "office holder", "MeanOfTransportation": "means of transport",
    "Building": "building", "NaturalPlace": "natural place", "Village": "village", "Animal": "animal",
    "Plant": "plant", "Album": "album", "Film": "film", "WrittenWork": "written work",
}
DBPEDIA_SUPER = {"Person": "person", "Organisation": "organisation", "Place": "place", "Species": "species",
                 "Work": "creative work", "Vehicle": "vehicle"}
DBPEDIA_SUPER_MAP = {
    "Person": ["Artist", "Athlete", "OfficeHolder"],
    "Organisation": ["Company", "EducationalInstitution"],
    "Place": ["Building", "NaturalPlace", "Village"],
    "Species": ["Animal", "Plant"],
    "Work": ["Album", "Film", "WrittenWork"],
    "Vehicle": ["MeanOfTransportation"],
}

GOEMO_GROUPS = {"anger": "anger", "disgust": "disgust", "fear": "fear", "joy": "joy",
                "sadness": "sadness", "surprise": "surprise", "neutral": "neutral"}

HINT3 = {
    "sofmattress": {
        "bot_domain": "mattress store",
        "keys": {
            "100_NIGHT_TRIAL_OFFER": "100-night trial", "ABOUT_SOF_MATTRESS": "about the company",
            "CANCEL_ORDER": "cancel order", "CHECK_PINCODE": "delivery area check", "COD": "cash on delivery",
            "COMPARISON": "compare mattresses", "DELAY_IN_DELIVERY": "delayed delivery",
            "DISTRIBUTORS": "stores and dealers", "EMI": "monthly instalment plan",
            "ERGO_FEATURES": "Ergo mattress features", "LEAD_GEN": "talk to sales agent",
            "MATTRESS_COST": "mattress price", "OFFERS": "offers and discounts", "ORDER_STATUS": "order status",
            "ORTHO_FEATURES": "Ortho mattress features", "PILLOWS": "pillows", "PRODUCT_VARIANTS": "product range",
            "RETURN_EXCHANGE": "return or exchange", "SIZE_CUSTOMIZATION": "custom mattress size",
            "WHAT_SIZE_TO_ORDER": "choosing the right size",
        },
    },
    "curekart": {
        "bot_domain": "health supplement store",
        "keys": {
            "CALL_CENTER": "call centre contact", "CANCEL_ORDER": "cancel order", "CHAT_WITH_AGENT": "chat with an agent",
            "CHECK_PINCODE": "delivery area check", "CONSULT_START": "diet and fitness advice",
            "DELAY_IN_PARCEL": "delayed parcel", "EXPIRY_DATE": "product expiry date", "FRANCHISE": "become a seller",
            "MODIFY_ADDRESS": "change delivery address", "ORDER_STATUS": "order status", "ORDER_TAKING": "placing an order",
            "ORIGINAL_PRODUCT": "product authenticity", "PAYMENT_AND_BILL": "payments and bills",
            "RECOMMEND_PRODUCT": "product recommendation",
            "REFUNDS_RETURNS_REPLACEMENTS": "refund, return or replacement", "RESUME_DELIVERY": "resuming deliveries",
            "SIDE_EFFECT": "side effects", "SIGN_UP": "new user sign-up", "STORE_INFORMATION": "physical stores",
            "USER_GOAL_FORM": "fitness goal form",
        },
    },
}
HINT3_OOS = "NO_NODES_DETECTED"

NLUPP = {
    "affirm": "affirmation", "deny": "denial", "dont_know": "saying I don't know", "acknowledge": "acknowledgement",
    "greet": "greeting", "end_call": "end call or goodbye", "handoff": "speak to a human", "thank": "thanks",
    "repeat": "repeat request", "cancel_close_leave_freeze": "cancel, close or freeze", "change": "change or modify",
    "make_open_apply_setup_get_activate": "open, set up or activate", "request_info": "information request",
    "how": "how-to question", "why": "why question", "when": "when question", "how_much": "quantity question",
    "how_long": "duration question", "wrong_notworking_notshowing": "something wrong or missing",
    "lost_stolen": "lost or stolen", "more_higher_after": "more or higher", "less_lower_before": "less or lower",
    "new": "something new", "existing": "something existing", "limits": "limits",
    "savings": "savings account", "current": "current account", "business": "business account", "credit": "credit",
    "debit": "debit", "contactless": "contactless", "international": "international", "account": "account",
    "transfer_payment_deposit": "transfer, payment or deposit", "appointment": "appointment", "arrival": "arrival",
    "balance": "balance", "card": "card", "cheque": "cheque", "direct_debit": "direct debit",
    "standing_order": "standing order", "fees_interests": "fees or interest", "loan": "loan", "mortgage": "mortgage",
    "overdraft": "overdraft", "withdrawal": "withdrawal", "pin": "PIN", "refund": "refund",
    "check_in": "check-in", "check_out": "check-out", "restaurant": "restaurant", "swimming_pool": "swimming pool",
    "parking": "parking", "pets": "pets", "accesibility": "accessibility", "booking": "booking", "wifi": "wifi",
    "gym": "gym", "spa": "spa or beauty", "room_ammenities": "room amenities", "housekeeping": "housekeeping",
    "room_service": "room service",
}

MINDS14 = {
    "abroad": "using card abroad", "address": "change of address", "app_error": "app not working",
    "atm_limit": "ATM withdrawal limit", "balance": "account balance", "business_loan": "business loan",
    "card_issues": "card problem", "cash_deposit": "depositing money", "direct_debit": "direct debit",
    "freeze": "freeze card", "high_value_payment": "large payment verification", "joint_account": "joint account",
    "latest_transactions": "recent transactions", "pay_bill": "pay a bill",
}
SNIPS = {
    "AddToPlaylist": "add to playlist", "BookRestaurant": "book a restaurant", "GetWeather": "weather forecast",
    "PlayMusic": "play music", "RateBook": "rate a book", "SearchCreativeWork": "find a creative work",
    "SearchScreeningEvent": "find movie showtimes",
}
TFNS = {"0": ("Bearish", "bearish"), "1": ("Bullish", "bullish"), "2": ("Neutral", "neutral")}
SMS = {"ham": "legitimate", "spam": "spam"}


# --------------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------------
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def _download(url, dst):
    import requests  # DESIGN 3: GitHub sources are downloaded with requests at the pinned commit
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(dst + ".part", "wb") as f:
        f.write(r.content)
    os.replace(dst + ".part", dst)


def gh_fetch(name):
    repo, commit, path = GH[name]
    dst = os.path.join(GH_CACHE, repo.replace("/", "__"), commit, path)
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        _download(f"https://raw.githubusercontent.com/{repo}/{commit}/{path}", dst)
    return dst, {"repo": f"github:{repo}", "commit": commit, "path": path, "sha256": sha256_file(dst)}


def gh_fetch_raw(repo, commit, path):
    dst = os.path.join(GH_CACHE, repo.replace("/", "__"), commit, path)
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        _download(f"https://raw.githubusercontent.com/{repo}/{commit}/{path}", dst)
    return dst


def src(ds):
    repo, cfg, rev = PIN[ds]
    return f"{repo}" + (f" ({cfg})" if cfg else "") + f" @ {rev}"


def lab(label_id, key, kind, parent=None, **extra):
    d = {"label_id": label_id, "key": key, "kind": kind, "parent": parent}
    d.update(extra)
    return d


def is_raw_id(key, label_id):
    if "_" in key or key.endswith("?"):
        return True
    return key == label_id and (label_id.isupper() or bool(re.search(r"[a-z][A-Z]", label_id)))


def validate(doc):
    errs = []
    ids = [l["label_id"] for l in doc["labels"]]
    if len(ids) != len(set(ids)):
        errs.append("duplicate label_id")
    seen = {}
    for l in doc["labels"]:
        k, kind = l["key"], l["kind"]
        if kind not in KINDS:
            errs.append(f"bad kind {kind}")
        if l["parent"] is not None and l["parent"] not in ids:
            errs.append(f"{l['label_id']}: parent {l['parent']} missing")
        if kind == "oos":
            if k is not None:
                errs.append(f"{l['label_id']}: oos key must be null")
            continue
        if not isinstance(k, str) or not k.strip():
            errs.append(f"{l['label_id']}: empty key")
            continue
        n = len(k.split())
        if not 1 <= n <= 5:
            errs.append(f"{l['label_id']}: key '{k}' has {n} words")
        if is_raw_id(k, l["label_id"]):
            errs.append(f"{l['label_id']}: key '{k}' looks like a raw id")
        toks = set(re.findall(r"[a-z]+", k.lower()))
        if toks & BANNED_TOKENS:
            errs.append(f"{l['label_id']}: key '{k}' contains banned token {sorted(toks & BANNED_TOKENS)}")
        kl = k.lower()
        if kl in seen:
            errs.append(f"key '{k}' duplicated ({seen[kl]}, {l['label_id']})")
        seen[kl] = l["label_id"]
    if errs:
        raise SystemExit(f"[{doc['dataset']}] " + "; ".join(errs))


def finish(doc):
    order = {k: i for i, k in enumerate(KIND_ORDER)}
    doc["labels"] = sorted(doc["labels"], key=lambda l: (order[l["kind"]], l["label_id"]))
    doc["n_labels"] = len(doc["labels"])
    doc["counts_by_kind"] = dict(sorted(collections.Counter(l["kind"] for l in doc["labels"]).items()))
    doc.setdefault("authored_by", AUTHOR)
    doc.setdefault("schema_version", SCHEMA)
    doc.setdefault("created", CREATED)
    validate(doc)
    return doc


def check_cover(name, source_ids, authored):
    s, a = set(source_ids), set(authored)
    if s != a:
        raise SystemExit(f"[{name}] coverage mismatch: missing keys {sorted(s - a)}; extra keys {sorted(a - s)}")


KEY_POLICY = ("Choice key = natural 1-5 word English name of the label, fixed for every split, variant and model "
              "(DESIGN field rule 2, D8). Descriptions (D_*) and propositions (P_*) are authored separately per pool "
              "and never live in this file.")


# --------------------------------------------------------------------------------------------
# builders
# --------------------------------------------------------------------------------------------
def build_banking77():
    from datasets import load_dataset
    repo, _, rev = PIN["banking77"]
    names = load_dataset(repo, revision=rev, streaming=True)["train"].features["label"].names
    check_cover("banking77", names, BANKING77)
    labels = []
    for i, n in enumerate(names):
        extra = {"source_index": i}
        if n in BANKING77_KEY_NOTES:
            extra["key_note"] = BANKING77_KEY_NOTES[n]
        labels.append(lab(n, BANKING77[n], "intent", **extra))
    return finish({"dataset": "banking77", "source": src("banking77"), "label_field": "label",
                   "label_id_type": "classlabel_name", "key_policy": KEY_POLICY, "labels": labels})


def build_clinc150():
    from datasets import load_dataset
    repo, cfg, rev = PIN["clinc150"]
    names = load_dataset(repo, cfg, revision=rev, streaming=True)["train"].features["intent"].names
    dpath, dmeta = gh_fetch("clinc_domains")
    domains = json.load(open(dpath))
    check_cover("clinc150", [n for n in names if n != "oos"], CLINC150)
    check_cover("clinc150 domains", domains.keys(), CLINC_DOMAINS)
    parent = {}
    for d, ints in domains.items():
        for it in ints:
            if it in parent:
                raise SystemExit(f"clinc intent {it} in two domains")
            parent[it] = d
    check_cover("clinc150 domain map", parent.keys(), CLINC150)
    labels = [lab(d, CLINC_DOMAINS[d], "domain", n_children=len(domains[d])) for d in domains]
    for i, n in enumerate(names):
        if n == "oos":
            labels.append(lab(n, None, "oos", source_index=i,
                              key_note="no key: out-of-scope items take the 'none of these' option from the none_option bank"))
        else:
            labels.append(lab(n, CLINC150[n], "intent", parent[n], source_index=i))
    return finish({"dataset": "clinc150", "source": src("clinc150"), "source_files": [dmeta],
                   "label_field": "intent", "parent_field": "domain (data/domains.json of clinc/oos-eval)",
                   "label_id_type": "classlabel_name", "key_policy": KEY_POLICY, "labels": labels})


def build_massive():
    from datasets import load_dataset
    ds = load_dataset("AmazonScience/massive", revision="refs/convert/parquet", data_dir="en-US")
    feats = ds["train"].features
    inames, snames = feats["intent"].names, feats["scenario"].names
    pairs = collections.defaultdict(set)
    for sp in ds:
        for i, s in zip(ds[sp]["intent"], ds[sp]["scenario"]):
            pairs[inames[i]].add(snames[s])
    for it, ss in pairs.items():
        if len(ss) != 1:
            raise SystemExit(f"massive intent {it} has scenarios {ss}")
    check_cover("massive", inames, MASSIVE)
    check_cover("massive scenarios", snames, MASSIVE_SCENARIOS)
    labels = [lab(s, MASSIVE_SCENARIOS[s], "scenario", source_index=j) for j, s in enumerate(snames)]
    for j, it in enumerate(inames):
        labels.append(lab(it, MASSIVE[it], "intent", next(iter(pairs[it])), source_index=j))
    return finish({"dataset": "massive", "source": src("massive"), "label_field": "intent",
                   "parent_field": "scenario (every intent maps to exactly one scenario; checked on all en-US splits)",
                   "label_id_type": "classlabel_name", "key_policy": KEY_POLICY, "labels": labels})


def build_dbpedia14():
    from datasets import load_dataset
    repo, _, rev = PIN["dbpedia14"]
    names = load_dataset(repo, revision=rev, streaming=True)["train"].features["label"].names
    check_cover("dbpedia14", names, DBPEDIA_CLASSES)
    parent = {c: s for s, cs in DBPEDIA_SUPER_MAP.items() for c in cs}
    check_cover("dbpedia14 super map", parent.keys(), DBPEDIA_CLASSES)
    labels = [lab(s, DBPEDIA_SUPER[s], "superclass", n_children=len(DBPEDIA_SUPER_MAP[s])) for s in DBPEDIA_SUPER]
    for i, n in enumerate(names):
        labels.append(lab(n, DBPEDIA_CLASSES[n], "class", parent[n], source_index=i))
    return finish({
        "dataset": "dbpedia14", "source": src("dbpedia14"), "label_field": "label",
        "label_id_type": "classlabel_name (classes); super-class ids defined here",
        "superclass_map": DBPEDIA_SUPER_MAP,
        "superclass_basis": ("DBpedia ontology parents: Artist/Athlete/OfficeHolder < dbo:Person; Company/"
                             "EducationalInstitution < dbo:Organisation; Building/NaturalPlace/Village < dbo:Place; "
                             "Animal/Plant < dbo:Species; Album/Film/WrittenWork < dbo:Work. dbo:MeanOfTransportation "
                             "has no parent among these, so it forms the singleton super-class 'Vehicle' (id defined "
                             "here). Rule R6 HIER: gold = 1[parent(gold class) = P]."),
        "key_policy": KEY_POLICY, "labels": labels})


def build_goemotions():
    from datasets import load_dataset
    repo, cfg, rev = PIN["goemotions"]
    raw_cols = list(load_dataset(repo, "raw", revision=rev, streaming=True)["train"].features.keys())
    fine = load_dataset(repo, "simplified", revision=rev, streaming=True)["train"].features["labels"].feature.names
    epath, emeta = gh_fetch("goemotions_ekman")
    ekman = json.load(open(epath))
    f2g = {}
    for g, fs in ekman.items():
        for f in fs:
            if f in f2g:
                raise SystemExit(f"goemotions fine emotion {f} in two groups")
            f2g[f] = g
    f2g["neutral"] = "neutral"
    check_cover("goemotions fine map", fine, f2g)
    missing = [f for f in fine if f not in raw_cols]
    if missing:
        raise SystemExit(f"goemotions raw config lacks columns {missing}")
    check_cover("goemotions groups", set(f2g.values()), GOEMO_GROUPS)
    spath, smeta = gh_fetch("goemotions_sentiment")
    f2s = {f: v for v, fs in json.load(open(spath)).items() for f in fs}
    f2s["neutral"] = "neutral"
    valence = {}
    for g in GOEMO_GROUPS:
        vs = {f2s[f] for f in f2g if f2g[f] == g}
        if len(vs) != 1:
            raise SystemExit(f"goemotions group {g} has mixed sentiment {vs}")
        valence[g] = vs.pop()
    labels = [lab(g, GOEMO_GROUPS[g], "emotion_group", fine_emotions=sorted(f for f in f2g if f2g[f] == g),
                  valence=valence[g]) for g in GOEMO_GROUPS]
    labels.append(lab("emotion-strength-3", "emotion strength", "level", **SCALE["emotion-strength-3"]))
    return finish({
        "dataset": "goemotions", "source": src("goemotions") + "; split membership via 'simplified' ids",
        "source_files": [emeta, smeta],
        "valence_source": ("official goemotions/data/sentiment_mapping.json; every fine emotion of a group shares one "
                           "sentiment, so 'valence' is exact (used for DESIGN 3.3 'zero-vote same-valence group')"),
        "label_field": "raw per-rater 0/1 emotion columns, aggregated to Ekman groups by fine_to_group",
        "label_id_type": "ekman_mapping.json group name ('neutral' = the dataset's neutral column)",
        "fine_to_group": dict(sorted(f2g.items())),
        "fine_to_group_source": "official goemotions/data/ekman_mapping.json (neutral added as its own group, as DESIGN 3.3 lists Ekman-7)",
        "key_policy": KEY_POLICY, "labels": labels})


def build_hint3(bot):
    import csv
    tpath, tmeta = gh_fetch(f"hint3_{bot}_test")
    rpath, rmeta = gh_fetch(f"hint3_{bot}_train")
    test = [r["label"] for r in csv.DictReader(open(tpath, encoding="utf-8"))]
    train = [r["label"] for r in csv.DictReader(open(rpath, encoding="utf-8"))]
    tc = collections.Counter(test)
    in_scope = sorted(l for l in tc if l != HINT3_OOS)
    cfg = HINT3[bot]
    check_cover(f"hint3_{bot}", in_scope, cfg["keys"])
    labels = [lab(l, cfg["keys"][l], "intent", n_test=tc[l]) for l in in_scope]
    labels.append(lab(HINT3_OOS, None, "oos", n_test=tc[HINT3_OOS],
                      key_note="no key: out-of-scope items take the 'none of these' option from the none_option bank"))
    excluded = [{"label_id": l, "n_train": c,
                 "reason": ("train-only label: absent from the v2 test split, so a test request of this kind can only "
                            "carry another label or NO_NODES_DETECTED; offering it as an option would make "
                            "'none of these' gold unsafe")}
                for l, c in sorted(collections.Counter(train).items()) if l not in tc]
    return finish({
        "dataset": f"hint3_{bot}", "source": "github:hellohaptik/HINT3 @ 99965c892ea9a6801a87083d3861b0b04c91a4e7 (dataset v2)",
        "source_files": [tmeta, rmeta], "label_field": "label", "label_id_type": "csv label string",
        "bot_domain": cfg["bot_domain"], "eval_split": "test", "excluded_labels": excluded,
        "key_policy": KEY_POLICY, "labels": labels})


def build_nlupp():
    opath, ometa = gh_fetch("nlupp_ontology")
    onto = json.load(open(opath))["intents"]
    check_cover("nlupp", onto.keys(), NLUPP)
    repo, commit, _ = GH["nlupp_ontology"]
    counts = {"banking": collections.Counter(), "hotels": collections.Counter()}
    nrows = {"banking": 0, "hotels": 0}
    for d in counts:
        for i in range(20):
            p = gh_fetch_raw(repo, commit, f"nlupp/data/{d}/fold{i}.json")
            for r in json.load(open(p)):
                nrows[d] += 1
                for m in r.get("intents") or []:
                    counts[d][m] += 1
    inv = {d: sorted(m for m, v in onto.items() if d in v["domain"] or "general" in v["domain"]) for d in counts}
    for d in counts:
        if set(counts[d]) != set(inv[d]):
            raise SystemExit(f"nlupp {d}: data modules differ from ontology inventory")
    labels = []
    for m, v in onto.items():
        labels.append(lab(m, NLUPP[m], "module", ontology_question=v["description"], domain=sorted(v["domain"]),
                          inventories=sorted(d for d in inv if m in inv[d]),
                          n_rows={d: counts[d][m] for d in sorted(counts) if m in inv[d]}))
    return finish({
        "dataset": "nlupp", "source": f"github:PolyAI-LDN/task-specific-datasets @ {commit} nlupp/data/{{banking,hotels}}/fold0-19.json + ontology.json",
        "source_files": [ometa], "label_field": "intents (multi-label module list; missing = none)",
        "label_id_type": "ontology intent (module) name",
        "inventories": {d: inv[d] for d in sorted(inv)},
        "inventory_sizes": {d: len(inv[d]) for d in sorted(inv)},
        "n_utterances": nrows,
        "note": ("Multi-label: every module is a separate Noul target; 'ontology_question' is PolyAI's human question "
                 "(the base for P_ev1 per DESIGN 4.2); 'domain' is the ontology tag; 'inventories' says which domain "
                 "file set can carry the module (general modules belong to both)."),
        "key_policy": KEY_POLICY, "labels": labels})


def build_simple(ds, mapping, kind, label_field, loader):
    names, id_type = loader()
    check_cover(ds, names, mapping)
    labels = [lab(n, mapping[n], kind, source_index=i) if id_type == "classlabel_name" else lab(n, mapping[n], kind)
              for i, n in enumerate(names)]
    return finish({"dataset": ds, "source": src(ds), "label_field": label_field, "label_id_type": id_type,
                   "key_policy": KEY_POLICY, "labels": labels})


def load_minds14():
    from datasets import load_dataset
    repo, _, rev = PIN["minds14"]
    names = None
    for loc in ["en-US", "en-GB", "en-AU"]:
        n = load_dataset(repo, loc, revision=rev, streaming=True)["train"].features["intent_class"].names
        if names is not None and n != names:
            raise SystemExit("minds14 locales disagree on label names")
        names = n
    return names, "classlabel_name"


def load_snips():
    from datasets import load_dataset
    repo, _, rev = PIN["snips"]
    d = load_dataset(repo, revision=rev)
    return sorted(set(d["train"]["category"]) | set(d["test"]["category"])), "raw_value (string category)"


def load_sms():
    from datasets import load_dataset
    repo, cfg, rev = PIN["sms_spam"]
    return load_dataset(repo, cfg, revision=rev, streaming=True)["train"].features["label"].names, "classlabel_name"


def build_tfns():
    from datasets import load_dataset
    repo, _, rev = PIN["tfns"]
    d = load_dataset(repo, revision=rev)
    vals = sorted({str(v) for sp in d for v in d[sp]["label"]})
    check_cover("tfns", vals, TFNS)
    labels = [lab(v, TFNS[v][1], "class", source_name=TFNS[v][0]) for v in vals]
    return finish({"dataset": "tfns", "source": src("tfns"), "label_field": "label",
                   "label_id_type": "raw_value (int as string; names from the dataset card: LABEL_0 Bearish, LABEL_1 Bullish, LABEL_2 Neutral)",
                   "key_policy": KEY_POLICY, "labels": labels})


# Score constructs (DESIGN 6.1 construct ids; level texts come from assets/templates/score_scales.jsonl per pool)
SCALE = {
    "satisfaction-5": {"K": 5, "construct": "reviewer satisfaction with the product (self-rating 1-5 stars)",
                       "source_field": "rating", "levels": [{"level": i, "source_values": [i + 1]} for i in range(5)],
                       "rule": "R0 BASE_SRC; polarity reversal R7 allowed", "roles": ["train", "dev", "eval"]},
    "satisfaction-3": {"K": 3, "construct": "reviewer satisfaction, coarse (train rebin of satisfaction-5)",
                       "source_field": "rating",
                       "levels": [{"level": 0, "source_values": [1, 2]}, {"level": 1, "source_values": [3]},
                                  {"level": 2, "source_values": [4, 5]}],
                       "rule": "rebin of satisfaction-5 (DESIGN 3.1 '30% rebinned to 3'; bins defined here, see build_decisions.md)",
                       "roles": ["train", "dev"]},
    "drug-10": {"K": 10, "construct": "patient rating of the medication (1-10)", "source_field": "rating",
                "levels": [{"level": i, "source_values": [i + 1]} for i in range(10)],
                "rule": "R0 BASE_SRC; polarity reversal R7 allowed", "roles": ["train", "dev", "eval"]},
    "drug-5": {"K": 5, "construct": "patient rating of the medication, 5 bands", "source_field": "rating",
               "levels": [{"level": i, "source_values": [2 * i + 1, 2 * i + 2]} for i in range(5)],
               "rule": "R9 REBIN: floor((r - 1) / 2)", "roles": ["train", "dev", "eval"]},
    "drug-3": {"K": 3, "construct": "patient rating of the medication, 3 bands", "source_field": "rating",
               "levels": [{"level": 0, "source_values": [1, 2, 3]}, {"level": 1, "source_values": [4, 5, 6, 7]},
                          {"level": 2, "source_values": [8, 9, 10]}],
               "rule": "R9 REBIN: {1-3, 4-7, 8-10}", "roles": ["train", "dev"]},
    "drug-2": {"K": 2, "construct": "patient rating of the medication, 2 bands", "source_field": "rating",
               "levels": [{"level": 0, "source_values": [1, 2, 3, 4, 5]}, {"level": 1, "source_values": [6, 7, 8, 9, 10]}],
               "rule": "R9 REBIN: 1[r >= 6]", "roles": ["train", "dev"]},
    "emotion-strength-3": {"K": 3, "construct": "how strongly the comment expresses the asked emotion (rater votes)",
                           "source_field": "raw rater votes for the asked emotion/group",
                           "levels": [{"level": 0, "votes": "0"}, {"level": 1, "votes": "1"}, {"level": 2, "votes": ">=2"}],
                           "rule": "DESIGN 4.3: 0 votes -> 0, 1 -> 1, >=2 -> 2", "roles": ["train", "dev"]},
    "sentiment-5": {"K": 5, "construct": "sentiment of the movie review sentence", "source_field": "label (continuous, [0, 1])",
                    "levels": [{"level": 0, "range": "[0.0, 0.2]"}, {"level": 1, "range": "(0.2, 0.4]"},
                               {"level": 2, "range": "(0.4, 0.6]"}, {"level": 3, "range": "(0.6, 0.8]"},
                               {"level": 4, "range": "(0.8, 1.0]"}],
                    "rule": "R0 + R12 SOFT (continuous label); items within +-0.02 of a bin edge are dropped from eval (DESIGN 3.3)",
                    "roles": ["eval"]},
    "target-sentiment-5": {"K": 5, "construct": "sentiment of the tweet toward the named target",
                           "source_field": "gold_label (0-4, SemEval-2016 Task 4C: strongly negative .. strongly positive)",
                           "levels": [{"level": i, "source_values": [i]} for i in range(5)],
                           "rule": "R0 BASE_SRC; polarity reversal R7 allowed", "roles": ["eval"]},
    "toxicity-4": {"K": 4, "construct": "how many readers would find the comment toxic (rater fraction)",
                   "source_field": "toxicity (fraction of raters)",
                   "levels": [{"level": 0, "range": "[0.0, 0.2)", "fixed_anchor": "almost none"},
                              {"level": 1, "range": "[0.2, 0.5)", "fixed_anchor": "some"},
                              {"level": 2, "range": "[0.5, 0.8)", "fixed_anchor": "most"},
                              {"level": 3, "range": "[0.8, 1.0]", "fixed_anchor": "nearly all"}],
                   "rule": "DESIGN 3.3 civil Q4 (anchors fixed by the spec, review #19)", "roles": ["eval"]},
    "insult-5": {"K": 5, "construct": "how insulting the comment is (MHS insult item, 0-4)",
                 "source_field": "insult (per annotator 0-4; gold level = median over >= 3 annotators; soft = annotator distribution)",
                 "levels": [{"level": i, "source_values": [i]} for i in range(5)],
                 "rule": "R0 + R12 SOFT; MIRROR wording 'How free of insult...' uses the same anchors reversed (R7)",
                 "roles": ["eval"]},
}


def pred(pid, key, rule, field, roles, **extra):
    return lab(pid, key, "predicate", gold_rule=rule, source_field=field, roles=roles, **extra)


def scale(cid, key):
    return lab(cid, key, "level", **SCALE[cid])


def build_predicate_sources():
    out = []
    out.append(finish({
        "dataset": "clothing", "source": src("clothing"), "label_field": "rating (1-5), recommended_ind (0/1)",
        "label_id_type": "predicate and scale ids defined here (the source has no label ids for them)",
        "key_policy": KEY_POLICY, "labels": [
            pred("recommend", "recommend", "R0: 1[recommended_ind = 1]", "recommended_ind", ["train", "dev", "eval"],
                 note="human-floor Noul (Q5); train soft target eps = 0.03"),
            pred("rating_ge_4", "rating at least 4", "R8 THRESH: 1[rating >= 4]", "rating", ["train", "dev", "eval"],
                 threshold_adjacent_values=[3, 4], note="threshold-adjacent ratings are hard_ok=false (train eps 0.20)"),
            pred("positive", "positive", "1[rating >= 4]; rating 3 -> 0", "rating", ["train", "dev"],
                 note="used with 'negative' as a contrary pair; rating-3 states are both-no trap rows (DESIGN 4.4)"),
            pred("negative", "negative", "1[rating <= 2]; rating 3 -> 0", "rating", ["train", "dev"],
                 note="contrary of 'positive' (not a complement)"),
            scale("satisfaction-5", "satisfaction"),
            scale("satisfaction-3", "coarse satisfaction"),
        ]}))
    out.append(finish({
        "dataset": "drug", "source": src("drug") + " (cite UCI Drug Review, CC BY 4.0)", "label_field": "rating (1-10)",
        "label_id_type": "predicate and scale ids defined here (the source has no label ids for them)",
        "key_policy": KEY_POLICY, "labels": [
            pred("rating_ge_5", "rating at least 5", "R8 THRESH: 1[rating >= 5]", "rating", ["train", "dev"],
                 threshold_adjacent_values=[4, 5]),
            pred("rating_ge_7", "rating at least 7", "R8 THRESH: 1[rating >= 7]", "rating", ["train", "dev", "eval"],
                 threshold_adjacent_values=[6, 7]),
            pred("rating_ge_9", "rating at least 9", "R8 THRESH: 1[rating >= 9]", "rating", ["train", "dev"],
                 threshold_adjacent_values=[8, 9]),
            scale("drug-10", "ten-point rating"),
            scale("drug-5", "five-band rating"),
            scale("drug-3", "three-band rating"),
            scale("drug-2", "two-band rating"),
        ]}))
    out.append(finish({
        "dataset": "sst5", "source": src("sst5"), "label_field": "label (continuous sentiment in [0, 1])",
        "label_id_type": "predicate and scale ids defined here (the source has no label ids for them)",
        "key_policy": KEY_POLICY, "labels": [
            pred("positive", "positive", "R8 THRESH: 1[level in {3, 4}] (label > 0.6)", "label", ["eval"],
                 threshold_adjacent_range="label within +-0.05 of 0.6"),
            pred("negative", "negative", "R8 THRESH: 1[level in {0, 1}] (label <= 0.4)", "label", ["eval"],
                 threshold_adjacent_range="label within +-0.05 of 0.4",
                 note="contrary of 'positive': both no on level-2 states (R5 both-no pairs)"),
            scale("sentiment-5", "sentiment"),
        ]}))
    out.append(finish({
        "dataset": "supertweeteval", "source": src("supertweeteval"), "label_field": "gold_label (0-4), target",
        "label_id_type": "predicate and scale ids defined here (the source has no label ids for them)",
        "key_policy": KEY_POLICY, "labels": [
            pred("positive_toward_target", "positive toward target", "R8 THRESH: 1[gold_label in {3, 4}]", "gold_label", ["eval"],
                 note="the target string is slotted into the question, not the key"),
            scale("target-sentiment-5", "sentiment toward target"),
        ]}))
    out.append(finish({
        "dataset": "civil", "source": src("civil") + " (test, streamed)", "label_field": "toxicity (rater fraction q)",
        "label_id_type": "predicate and scale ids defined here (the source has no label ids for them)",
        "key_policy": KEY_POLICY, "labels": [
            pred("toxic", "toxic", "R8/R12: 1[q >= 0.5], soft = q (= toxicity-4 levels 2-3)", "toxicity", ["eval"],
                 note="Q1 wording 'Would at least half of readers find this comment toxic?'; NEG is a complement only if q <= .2 or >= .8"),
            scale("toxicity-4", "reader toxicity share"),
        ]}))
    out.append(finish({
        "dataset": "mhs", "source": src("mhs"), "label_field": "insult (per-annotator 0-4)",
        "label_id_type": "predicate and scale ids defined here (the source has no label ids for them)",
        "key_policy": KEY_POLICY, "labels": [
            pred("insulting", "insulting", "1 if median insult >= 3; 0 if <= 1; soft-only (hard_ok=false) if 2", "insult", ["eval"]),
            scale("insult-5", "how insulting"),
        ]}))
    return out


# --------------------------------------------------------------------------------------------
# confusables (label ids; unordered pairs; reason). DESIGN 4.2 seeds first, then this author's additions.
# The build (step 5) appends pairs with >= 2 verifier disagreements or >= 5% MiniLM cross-fit confusion.
# --------------------------------------------------------------------------------------------
SEED = "DESIGN 4.2"
CONFUSABLES = {
    "banking77": [
        # DESIGN 4.2 families (scout 2.1): card arrival, top-up, transfer, card-not-working
        ("card_arrival", "card_delivery_estimate", SEED + " card-arrival family: a late card vs when a card will arrive"),
        ("card_arrival", "order_physical_card", "card-arrival family: 'I still don't have a card' appears under both"),
        ("card_delivery_estimate", "order_physical_card", "card-arrival family: shipping of a card being ordered"),
        ("pending_top_up", "top_up_failed", SEED + " top-up family: a top-up that has not gone through"),
        ("pending_top_up", "top_up_reverted", SEED + " top-up family"),
        ("top_up_failed", "top_up_reverted", SEED + " top-up family: failed vs returned top-up money"),
        ("pending_top_up", "topping_up_by_card", "top-up family: card top-up money not showing"),
        ("top_up_failed", "topping_up_by_card", "top-up family: 'I used my card to top up but the money is gone'"),
        ("top_up_reverted", "topping_up_by_card", "top-up family: card top-up money disappeared"),
        ("balance_not_updated_after_bank_transfer", "transfer_not_received_by_recipient", SEED + " transfer family: money sent but not arrived"),
        ("balance_not_updated_after_bank_transfer", "pending_transfer", SEED + " transfer family"),
        ("balance_not_updated_after_bank_transfer", "transfer_timing", SEED + " transfer family: how long until a transfer shows"),
        ("pending_transfer", "transfer_not_received_by_recipient", SEED + " transfer family"),
        ("pending_transfer", "transfer_timing", SEED + " transfer family: 'how long will my transfer take'"),
        ("transfer_not_received_by_recipient", "transfer_timing", SEED + " transfer family"),
        ("card_not_working", "declined_card_payment", SEED + " card-not-working family: a card that is refused"),
        ("card_not_working", "contactless_not_working", SEED + " card-not-working family"),
        ("card_not_working", "virtual_card_not_working", SEED + " card-not-working family"),
        ("card_not_working", "declined_cash_withdrawal", SEED + " card-not-working family: card refused at an ATM"),
        ("card_not_working", "pin_blocked", "card-not-working family: 'too many PIN attempts and now my card won't work'"),
        ("declined_card_payment", "declined_cash_withdrawal", "card refused for a payment vs at an ATM"),
        # additions (author review of source examples + TF-IDF cross-fit screen on the train split)
        ("getting_virtual_card", "virtual_card_not_working", "virtual card requests; screen confusion 14.6%"),
        ("get_disposable_virtual_card", "virtual_card_not_working", "virtual card requests; screen confusion 9.8%"),
        ("get_disposable_virtual_card", "getting_virtual_card", "disposable vs ordinary virtual card"),
        ("disposable_card_limits", "get_disposable_virtual_card", "disposable card questions; screen confusion 6%"),
        ("declined_transfer", "failed_transfer", "near-synonymous: declined vs failed transfer; screen 8.3%"),
        ("beneficiary_not_allowed", "declined_transfer", "a transfer to a beneficiary that was rejected"),
        ("beneficiary_not_allowed", "failed_transfer", "a transfer to a beneficiary that failed"),
        ("verify_my_identity", "why_verify_identity", "identity verification questions; screen 7.4%"),
        ("unable_to_verify_identity", "why_verify_identity", "identity verification questions; screen 6.9%"),
        ("unable_to_verify_identity", "verify_my_identity", "identity verification: how to vs cannot"),
        ("card_payment_not_recognised", "direct_debit_payment_not_recognised", "an unknown payment on the statement; screen 6%"),
        ("card_payment_not_recognised", "cash_withdrawal_not_recognised", "an unknown transaction on the statement"),
        ("card_payment_not_recognised", "compromised_card", "unknown payments reported as card fraud"),
        ("cash_withdrawal_not_recognised", "compromised_card", "unknown withdrawals reported as card fraud"),
        ("card_payment_not_recognised", "extra_charge_on_statement", "an unexplained charge on the statement"),
        ("card_payment_fee_charged", "extra_charge_on_statement", "an unexpected fee on the statement"),
        ("card_payment_not_recognised", "transaction_charged_twice", "an unexpected payment line on the statement"),
        ("card_payment_wrong_exchange_rate", "wrong_exchange_rate_for_cash_withdrawal", "wrong exchange rate, payment vs withdrawal; screen 5.5%"),
        ("card_payment_wrong_exchange_rate", "exchange_rate", "exchange-rate questions about a payment"),
        ("exchange_charge", "exchange_rate", "cost of exchanging currency vs the rate used"),
        ("pending_cash_withdrawal", "wrong_amount_of_cash_received", "withdrawal money not showing as expected"),
        ("declined_cash_withdrawal", "wrong_amount_of_cash_received", "an ATM withdrawal that went wrong; screen 5.6%"),
        ("declined_cash_withdrawal", "pending_cash_withdrawal", "an ATM withdrawal that did not complete"),
        ("Refund_not_showing_up", "request_refund", "refund questions: asking for vs missing refund"),
        ("declined_card_payment", "reverted_card_payment?", "'my card payment was cancelled'"),
        ("pending_card_payment", "reverted_card_payment?", "a card payment whose status changed"),
        ("change_pin", "get_physical_card", "PIN questions (get_physical_card is mostly about the card PIN)"),
        ("get_physical_card", "pin_blocked", "PIN questions; screen 6.1%"),
        ("change_pin", "pin_blocked", "PIN questions: changing vs unblocking"),
        ("getting_spare_card", "order_physical_card", "ordering an extra or first physical card"),
        ("activate_my_card", "card_linking", "'how do I activate and link my new card'"),
        ("compromised_card", "lost_or_stolen_card", "card misuse vs a lost or stolen card"),
        ("automatic_top_up", "top_up_limits", "auto top-up limits"),
        ("top_up_by_bank_transfer_charge", "top_up_by_card_charge", "top-up fees: 'do you charge anything for topping up'"),
        ("top_up_by_card_charge", "topping_up_by_card", "topping up by card and its cost"),
        ("supported_cards_and_currencies", "topping_up_by_card", "which cards can be used to top up"),
        ("fiat_currency_support", "supported_cards_and_currencies", "which currencies are supported"),
        ("top_up_by_bank_transfer_charge", "transfer_into_account", "topping up by bank transfer and its cost"),
        ("receiving_money", "transfer_into_account", "money coming into the account"),
        ("top_up_by_bank_transfer_charge", "transfer_fee_charged", "'how much does each transfer cost'"),
        ("atm_support", "card_acceptance", "where the card can be used"),
        ("card_acceptance", "country_support", "where the card can be used or obtained"),
    ],
    "clinc150": [
        ("spending_history", "transactions", SEED + " (scout 2.2): past spending vs transaction list"),
        ("directions", "distance", SEED + " (scout 2.2): route vs travel time; screen 6%"),
        ("current_location", "share_location", "location requests; screen 12%"),
        ("user_name", "what_is_your_name", "'what is my/your name'; screen 9%"),
        ("change_user_name", "user_name", "the user's name: set vs ask"),
        ("change_ai_name", "what_is_your_name", "the assistant's name: set vs ask; screen 9%"),
        ("pto_balance", "pto_used", "time off left vs taken; screen 9%"),
        ("pto_request", "pto_request_status", "time-off request vs its status"),
        ("account_blocked", "freeze_account", "blocking an account vs a blocked account; screen 8%"),
        ("todo_list", "todo_list_update", "to-do list read vs edit; screen 8%"),
        ("shopping_list", "shopping_list_update", "shopping list read vs edit; screen 6%"),
        ("calendar", "calendar_update", "calendar read vs edit; screen 7%"),
        ("calendar", "meeting_schedule", "'what is on my calendar' vs 'what meetings do I have'"),
        ("meeting_schedule", "schedule_meeting", "meetings: check vs book"),
        ("calendar_update", "schedule_meeting", "adding a meeting to the calendar"),
        ("reminder", "reminder_update", "reminders read vs set"),
        ("credit_score", "improve_credit_score", "credit score questions; screen 7%"),
        ("credit_limit", "credit_limit_change", "credit limit: ask vs change"),
        ("who_do_you_work_for", "who_made_you", "assistant origin questions; screen 7%"),
        ("meal_suggestion", "restaurant_suggestion", "'where/what should I eat'"),
        ("restaurant_suggestion", "travel_suggestion", "place suggestions; screen 6%"),
        ("cancel_reservation", "restaurant_reservation", "reservation requests"),
        ("confirm_reservation", "restaurant_reservation", "reservation requests"),
        ("accept_reservations", "restaurant_reservation", "reservation requests"),
        ("goodbye", "thank_you", "closing small talk; screen 6%"),
        ("maybe", "no", "non-committal vs negative reply; screen 5%"),
        ("play_music", "update_playlist", "music requests"),
        ("calories", "nutrition_info", "nutrition questions"),
        ("ingredients_list", "recipe", "'what do I need to make X'"),
        ("bill_balance", "bill_due", "bill amount vs due date"),
        ("balance", "bill_balance", "'what is the balance on my account'"),
        ("pay_bill", "min_payment", "bill payment amount"),
        ("report_fraud", "report_lost_card", "stolen card used without permission"),
        ("application_status", "new_card", "credit card application"),
        ("time", "timezone", "'what is the time in X timezone'"),
        ("oil_change_how", "oil_change_when", "oil change questions"),
        ("oil_change_when", "schedule_maintenance", "booking or timing an oil change"),
        ("last_maintenance", "schedule_maintenance", "car service history vs booking"),
        ("gas", "gas_type", "fuel questions"),
        ("insurance", "insurance_change", "insurance questions"),
        ("income", "payday", "pay questions"),
        ("direct_deposit", "payday", "paycheck deposit"),
        ("taxes", "w2", "tax documents"),
        ("change_volume", "whisper_mode", "volume and whisper mode ('turn your volume up' appears under whisper_mode)"),
        ("change_accent", "change_language", "voice and language settings"),
        ("order", "order_status", "shopping orders"),
        ("travel_alert", "travel_notification", "near-identical names: travel advisory vs telling the bank about travel"),
        ("directions", "traffic", "route questions"),
    ],
    "massive": [
        ("general_greet", "general_quirky", "general_quirky is a catch-all; screen 28%"),
        ("general_quirky", "qa_factoid", "catch-all vs factual questions; screen 10%"),
        ("general_joke", "general_quirky", "catch-all chat"),
        ("datetime_convert", "datetime_query", "'what time is it in X'; screen 27%"),
        ("music_settings", "play_music", "shuffle/repeat requests while playing; screen 24%"),
        ("audio_volume_other", "audio_volume_up", "volume adjustments; screen 22%"),
        ("audio_volume_down", "audio_volume_other", "volume adjustments"),
        ("audio_volume_mute", "audio_volume_other", "volume adjustments"),
        ("music_query", "play_music", "music requests"),
        ("play_audiobook", "play_podcasts", "spoken-audio playback"),
        ("play_music", "play_radio", "music playback; screen 10%"),
        ("play_audiobook", "play_music", "playback requests; screen 15%"),
        ("transport_query", "transport_ticket", "train schedule vs ticket; screen 14%"),
        ("transport_query", "transport_traffic", "route and traffic questions"),
        ("iot_hue_lighton", "iot_hue_lightup", "turn on vs brighten the lights; screen 14%"),
        ("iot_hue_lightdim", "iot_hue_lightoff", "dim vs switch off the lights"),
        ("iot_hue_lightchange", "iot_hue_lightup", "light adjustments"),
        ("iot_hue_lighton", "iot_wemo_on", "'turn on the light socket'"),
        ("iot_hue_lightoff", "iot_wemo_off", "'turn off the light socket'"),
        ("takeaway_order", "takeaway_query", "takeaway requests; screen 10%"),
        ("alarm_query", "alarm_set", "alarms: check vs set"),
        ("alarm_remove", "alarm_set", "alarms: remove vs set; screen 9%"),
        ("alarm_set", "calendar_set", "reminder-like alarms"),
        ("calendar_query", "calendar_set", "calendar: check vs add"),
        ("calendar_query", "calendar_remove", "calendar: check vs remove"),
        ("calendar_remove", "lists_remove", "removing an item; screen 6%"),
        ("email_query", "email_querycontact", "email and contacts questions"),
        ("email_addcontact", "email_querycontact", "contacts; screen 7%"),
        ("email_addcontact", "email_sendemail", "email actions; screen 7%"),
        ("lists_createoradd", "lists_query", "lists: add vs read"),
        ("lists_createoradd", "lists_remove", "lists: add vs remove"),
        ("qa_definition", "qa_factoid", "knowledge questions"),
        ("qa_factoid", "qa_maths", "knowledge questions; screen 8%"),
        ("qa_currency", "qa_stock", "financial rate questions"),
        ("recommendation_events", "recommendation_movies", "'any good films on'; screen 6%"),
        ("recommendation_events", "recommendation_locations", "things and places nearby"),
        ("cooking_query", "cooking_recipe", "cooking requests (cooking_query has 4 train rows)"),
        ("social_post", "social_query", "social media requests"),
        ("news_query", "social_query", "'what is trending'"),
        ("calendar_query", "datetime_query", "date questions"),
    ],
    "hint3_sofmattress": [
        ("SIZE_CUSTOMIZATION", "WHAT_SIZE_TO_ORDER", "size questions; screen 22%"),
        ("PRODUCT_VARIANTS", "WHAT_SIZE_TO_ORDER", "'I need a mattress for a double bed'"),
        ("COMPARISON", "PRODUCT_VARIANTS", "product range and comparison"),
        ("COMPARISON", "ERGO_FEATURES", "features vs comparison of Ergo"),
        ("COMPARISON", "ORTHO_FEATURES", "features vs comparison of Ortho"),
        ("ERGO_FEATURES", "PRODUCT_VARIANTS", "product information"),
        ("ORTHO_FEATURES", "PRODUCT_VARIANTS", "product information"),
        ("ABOUT_SOF_MATTRESS", "PRODUCT_VARIANTS", "'what are the SOF mattress products'"),
        ("DELAY_IN_DELIVERY", "ORDER_STATUS", "'I did not receive my order yet'"),
        ("CANCEL_ORDER", "ORDER_STATUS", "'cancellation status'"),
        ("CHECK_PINCODE", "DISTRIBUTORS", "'is it available in <city>' vs 'is it delivered in <city>'"),
        ("CHECK_PINCODE", "COD", "'do you offer COD to my pincode'"),
        ("COD", "EMI", "payment options"),
        ("EMI", "OFFERS", "'0% interest' offers"),
        ("100_NIGHT_TRIAL_OFFER", "OFFERS", "offers"),
        ("100_NIGHT_TRIAL_OFFER", "RETURN_EXCHANGE", "returning during the trial"),
        ("MATTRESS_COST", "SIZE_CUSTOMIZATION", "'custom size cost'"),
        ("MATTRESS_COST", "OFFERS", "price and discount"),
        ("DISTRIBUTORS", "LEAD_GEN", "where and how to buy"),
    ],
    "hint3_curekart": [
        ("CALL_CENTER", "CHAT_WITH_AGENT", "contacting a person; screen 12%"),
        ("DELAY_IN_PARCEL", "ORDER_STATUS", "'I didn't receive my order'"),
        ("DELAY_IN_PARCEL", "RESUME_DELIVERY", "COVID delivery delays; screen 13%"),
        ("ORDER_STATUS", "RESUME_DELIVERY", "'when will my parcel come'; screen 19%"),
        ("CHECK_PINCODE", "RESUME_DELIVERY", "'are you delivering in <city>'; screen 14%"),
        ("ORDER_TAKING", "RESUME_DELIVERY", "ordering and delivery during lockdown"),
        ("ORDER_TAKING", "RECOMMEND_PRODUCT", "'I want to order <product>'"),
        ("CONSULT_START", "RECOMMEND_PRODUCT", "diet advice vs product advice; screen 15%"),
        ("CONSULT_START", "USER_GOAL_FORM", "fitness goals vs diet advice"),
        ("PAYMENT_AND_BILL", "REFUNDS_RETURNS_REPLACEMENTS", "'money deducted but order not placed'"),
        ("ORDER_STATUS", "REFUNDS_RETURNS_REPLACEMENTS", "status of a return or refund"),
        ("CANCEL_ORDER", "REFUNDS_RETURNS_REPLACEMENTS", "undoing an order"),
        ("CHECK_PINCODE", "STORE_INFORMATION", "'any store in <city>'"),
    ],
    "dbpedia14": [
        ("NaturalPlace", "Village", "scout: some Village/NaturalPlace entries are ambiguous"),
        ("Building", "EducationalInstitution", "school and university buildings"),
        ("Album", "Film", "soundtrack albums of films"),
    ],
}


def build_confusables(label_ids):
    out = {"_meta": {"authored_by": AUTHOR, "created": CREATED,
                     "format": "{dataset: [[label_a, label_b, reason], ...]}; label ids as in keys/<dataset>.keys.json; "
                               "pairs are unordered (label_a < label_b); keys starting with '_' are metadata",
                     "sources": ["DESIGN 4.2 seed list (Banking77 card-arrival, top-up, transfer and card-not-working "
                                 "families; CLINC transactions/spending_history, distance/directions)",
                                 "author review of source examples (train splits only for HINT3)",
                                 "TF-IDF + logistic-regression 5-fold cross-fit on the train splits, pairs with >= 5% "
                                 "confusion considered as candidates (the build's MiniLM screen adds pairs in step 5)"],
                     "use": "confusable pairs are allowed as Choice options but never as Noul gold-no targets, "
                            "L* targets, injection targets or complement/consistency pairs (DESIGN 3.1, 3.3, 6.2)"}}
    for ds in sorted(CONFUSABLES):
        seen = set()
        rows = []
        for a, b, r in CONFUSABLES[ds]:
            for x in (a, b):
                if x not in label_ids[ds]:
                    raise SystemExit(f"confusables {ds}: unknown label {x}")
            if a == b:
                raise SystemExit(f"confusables {ds}: self pair {a}")
            a2, b2 = sorted((a, b))
            if (a2, b2) in seen:
                raise SystemExit(f"confusables {ds}: duplicate pair {a2} {b2}")
            seen.add((a2, b2))
            rows.append([a2, b2, r])
        out[ds] = sorted(rows)
    return out


# --------------------------------------------------------------------------------------------
# inventory (DESIGN section 3)
# --------------------------------------------------------------------------------------------
ROLES = {
    "banking77": (["train", "dev", "eval", "cmp"], ["ID", "INJ", "DIST", "DIAG"],
                  "train: train split minus dev hold-out; dev: train remainder; eval: test; cmp: CMP-B77 uses "
                  "btzsc/btzsc banking77 (72 BTZSC hypotheses as label_000.. keys), not these keys"),
    "clinc150": (["train", "dev", "eval"], ["ID", "INJ", "DIST", "DIAG"], "train: plus train; dev: validation; eval: plus test"),
    "massive": (["train", "dev"], [], "train: en-US train; dev: en-US validation"),
    "dbpedia14": (["train", "dev"], [], "train: train; dev: train remainder"),
    "goemotions": (["train", "dev", "eval"], ["ID", "DIST", "DIAG"], "raw config; split membership via simplified ids (train / validation / test)"),
    "clothing": (["train", "dev", "eval"], ["ID", "INJ"], "train / validation / test"),
    "drug": (["train", "dev", "eval"], ["ID"], "pool train+test regrouped by normalised text, 80/10/10 by hash"),
    "hint3_sofmattress": (["eval"], ["ZS", "INJ", "DIST"], "v2 test (zero-shot)"),
    "hint3_curekart": (["eval"], ["ZS", "INJ", "DIST"], "v2 test (zero-shot)"),
    "nlupp": (["eval"], ["ZS", "INJ", "DIST"], "banking + hotels folds 0-19 (zero-shot)"),
    "tfns": (["eval"], ["ZS"], "validation (zero-shot)"),
    "sst5": (["eval"], ["ZS", "INJ", "DIST"], "test minus RT-train sentences (zero-shot)"),
    "supertweeteval": (["eval"], ["ZS", "INJ"], "tweet_sentiment test (zero-shot)"),
    "sms_spam": (["eval"], ["ZS", "INJ", "DIST"], "train (only split), deduplicated (zero-shot)"),
    "civil": (["eval"], ["ZS"], "test, streamed (zero-shot)"),
    "mhs": (["eval"], ["ZS"], "train (only split), comments with >= 3 annotators (zero-shot)"),
    "minds14": (["dev_zs"], [], "en-US/en-GB/en-AU train, audio dropped; deduplicated against Banking77"),
    "snips": (["dev_zs"], [], "benayas/snips"),
}
NO_ASSET = {
    "mnli": (["train", "dev"], [], "nyu-mll/multi_nli @ da70db2a…", ["nli-3"],
             "NLI: the hypothesis is the proposition; Choice-3 keys true/false/cannot tell come from the choice3 bank"),
    "wanli": (["train", "dev"], [], "alisawuffles/WANLI @ 61c95318…", [], "NLI: no label asset (DESIGN 4.2)"),
    "boolq": (["train", "dev", "eval"], ["ID", "INJ", "DIST"], "google/boolq @ 35b264d0… (+ BECEL boolq files and "
              "tasksource/boolq-natural-perturbations in eval boolq_bundle)", [], "QA: QF/QN banks + scope bank; no label asset"),
    "condaqa": (["train", "dev", "eval"], ["ID"], "lasha-nlp/CONDAQA @ 3c9caa2f…", [], "QA: no label asset; Choice-3 bank"),
    "vitaminc": (["train", "dev", "eval"], ["ID"], "tals/vitaminc @ be6febb7…", ["vitaminc-3"],
                 "fact verification: the claim is the proposition; no label asset"),
    "nan_nli": (["eval"], ["ZS"], "joey234/nan-nli @ bb442425…", [], "NLI: no label asset"),
    "becel_snli": (["eval"], ["ZS"], "MJ-Jang/BECEL @ f5bdd119… data/snli", [], "NLI: no label asset"),
    "hans": (["dev_zs"], [], "jhu-cogsci/hans refs/convert/parquet validation", [], "NLI: no label asset"),
    "fresh": (["eval"], ["FR"], "authored FR items (DESIGN 7)", ["fresh-4", "fresh-7"],
              "options and Score levels are authored per item; no keys file"),
    "btzsc_banking77": (["cmp"], ["CMP"], "btzsc/btzsc banking77 @ fef2a2ac…", [],
                        "AbdelStark replay: 72 BTZSC hypotheses as criteria with keys label_000.. (verbatim, not ours)"),
}
EXTRA_CONSTRUCTS = {
    "nli-3": {"dataset": "mnli", "K": 3, "levels_low_to_high": ["contradicts", "neither", "supports"], "roles": ["train", "dev"]},
    "vitaminc-3": {"dataset": "vitaminc", "K": 3, "levels_low_to_high": ["refutes", "not enough info", "supports"], "roles": ["train", "dev"]},
    "fresh-4": {"dataset": "fresh", "K": 4, "levels_low_to_high": "authored per item", "roles": ["eval"]},
    "fresh-7": {"dataset": "fresh", "K": 7, "levels_low_to_high": "authored per item", "roles": ["eval"]},
}


def build_inventory(docs):
    ds_out = {}
    constructs = {}
    for d in docs:
        name = d["dataset"]
        roles, tracks, note = ROLES[name]
        ds_out[name] = {"keys_file": f"assets/labels/keys/{name}.keys.json", "label_asset": True,
                        "source": d["source"], "n_labels": d["n_labels"], "counts_by_kind": d["counts_by_kind"],
                        "n_keyed": sum(1 for l in d["labels"] if l["key"] is not None),
                        "roles": roles, "eval_tracks": tracks, "splits_note": note}
        if "inventory_sizes" in d:
            ds_out[name]["inventory_sizes"] = d["inventory_sizes"]
        if d.get("excluded_labels"):
            ds_out[name]["excluded_labels"] = [e["label_id"] for e in d["excluded_labels"]]
        for l in d["labels"]:
            if l["kind"] == "level":
                constructs[l["label_id"]] = {"dataset": name, "K": l["K"], "roles": l["roles"]}
    for name, (roles, tracks, source, cons, note) in NO_ASSET.items():
        ds_out[name] = {"keys_file": None, "label_asset": False, "source": source, "roles": roles,
                        "eval_tracks": tracks, "scale_constructs": cons, "note": note}
    for c, v in EXTRA_CONSTRUCTS.items():
        constructs[c] = v
    by_role = collections.defaultdict(list)
    for name, v in ds_out.items():
        for r in v["roles"]:
            by_role[r].append(name)
    return {
        "authored_by": AUTHOR, "created": CREATED, "schema_version": SCHEMA,
        "spec_refs": "DESIGN sections 3 (sources and roles), 4.2 (label assets), 6.1 (Score constructs), 12, deviation D8",
        "roles_legend": {"train": "train L0-L3 (3.1)", "dev": "dev (3.2)", "dev_zs": "zero-shot checkpoint selection (3.2)",
                         "eval": "frozen eval: ID/ZS/FR core and INJ/DIST robustness (3.3, 6.2, 6.3)",
                         "cmp": "comparability replay CMP-B77 (3.4)"},
        "datasets": dict(sorted(ds_out.items())),
        "datasets_by_role": {r: sorted(v) for r, v in sorted(by_role.items())},
        "scale_constructs": dict(sorted(constructs.items())),
        "totals": {"keys_files": len(docs),
                   "labels": sum(d["n_labels"] for d in docs),
                   "keyed_labels": sum(v.get("n_keyed", 0) for v in ds_out.values()),
                   "by_kind": dict(sorted(sum((collections.Counter(d["counts_by_kind"]) for d in docs), collections.Counter()).items()))},
    }


def dump(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


def main():
    os.makedirs(KEYS_DIR, exist_ok=True)
    docs = [build_banking77(), build_clinc150(), build_massive(), build_dbpedia14(), build_goemotions(),
            build_hint3("sofmattress"), build_hint3("curekart"), build_nlupp(),
            build_simple("minds14", MINDS14, "intent", "intent_class", load_minds14),
            build_simple("snips", SNIPS, "intent", "category", load_snips),
            build_tfns(),
            build_simple("sms_spam", SMS, "class", "label", load_sms)]
    docs += build_predicate_sources()
    docs = sorted(docs, key=lambda d: d["dataset"])
    for d in docs:
        dump(d, os.path.join(KEYS_DIR, f"{d['dataset']}.keys.json"))
        print(f"{d['dataset']:20s} {d['n_labels']:4d} {d['counts_by_kind']}")
    label_ids = {d["dataset"]: {l["label_id"] for l in d["labels"]} for d in docs}
    dump(build_confusables(label_ids), os.path.join(HERE, "confusables.json"))
    dump(build_inventory(docs), os.path.join(HERE, "label_inventory.json"))
    print("confusable pairs:", {k: len(v) for k, v in CONFUSABLES.items()})


if __name__ == "__main__":
    sys.exit(main())
