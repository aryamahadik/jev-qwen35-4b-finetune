"""Build raw rows for star_next_action: which action should a flow-chart-driven support assistant take next?

Source : STAR (Rasa; Mosig, Mehri & Kober 2020, arXiv:2010.11853), GitHub RasaHQ/STAR pinned at commit REV
         (git fetch of that commit into cache/star_next_action/repo; a sha256 over the sorted dialogue + task files
         is recorded and checked). STAR ships no official split; the whole release counts as train.
Licence: MIT (LICENSE.txt in RasaHQ/STAR, "Copyright (c) 2020 Rasa Technologies GmbH").
Texts  : Wizard-of-Oz dialogues typed by MTurk workers (human user and human wizard). Wizard turns are the texts the
         wizard picked (flow-chart response templates) or typed.
Labels : the action label of the suggestion the human wizard picked (pick_suggestion.ActionLabel), or the wizard's own
         database query (RequestType Check / Book). The wizards follow a per-task flow chart (tasks/<task>/<task>.json
         "graph"); no model wrote any label.
Rows   : one decision point per dialogue. A decision point is kept only when the wizard's action is the one the flow
         chart prescribes at that point (so the gold is checkable from the transcript and the option definitions):
           (a) right after a database result: the inform action this task's chart uses for that outcome
               (available / unavailable / success / failure / nothing found / result);
           (b) after the user answered the wizard's previous step A: the chart successor graph[A] (asks, the final
               lookup, "anything else" after the final result); slot questions are dropped when the slot's value
               (taken from the dialogue's own queries) already appeared in an earlier user turn;
           (c) yes / no replies to the wizard's booking offer -> graph["yes"] / graph["no"]; "no" to "anything else?" ->
               goodbye; "can't remember" to the account-number / PIN question -> the security-question route.
         Greeting rows, out-of-scope rows and free-typed ("custom") wizard turns are never gold. Single-task, complete
         dialogues of the 16 transactional tasks only (search / trivia / weather / directions tasks have free-order
         optional filters and are skipped). The 550 dialogues used by the v0.13 breadth key "star" are excluded.
State  : the task's name, then the visible conversation so far (User / Assistant lines, and bracketed database
         lookups and results); hidden MTurk instructions and wizard drafts are never shown.
Options: all actions of that task's chart (10-17), with per-task Claude-written definitions (defs/<key>__<task>.json).
Deterministic (seed SEED).
"""
import collections
import hashlib
import json
import random
import re
import subprocess
from pathlib import Path

import _rd_common as C

KEY = "star_next_action"
SEED = 20260929
MAX_ROWS = 3600
GIT_URL = "https://github.com/RasaHQ/STAR.git"
REV = "3058975092cdd09798e4a3a9e4ae135755824545"
CONTENT_SHA = None  # filled after first fetch; checked on later runs (see PIN_FILE)
PIN_FILE = C.HERE / "pins_star_next_action.json"
LICENCE = "MIT (LICENSE.txt in github.com/RasaHQ/STAR @" + REV + ", 'Copyright (c) 2020 Rasa Technologies GmbH')"
BREADTH_STAR = C.LEAN / "data" / "v13_parts" / "raw" / "star.jsonl"

BYE = {"goodbye_1", "goodbye_2", "bank_bye", "doctor_bye", "party_bye", "ride_bye", "spaceship_bye"}
COMMON = {"hello": "greet the user", "ask_name": "ask for the user's name", "anything_else": "ask if anything else is needed",
          "out_of_scope": "say the request is out of scope", "query": "look it up in the system",
          "query_check": "check availability in the system", "query_book": "book it in the system",
          "BYE": "say goodbye"}

# Per task: description, action names, slot fields for asks, outcome -> inform action, extra definitions.
TASKS = {
    "apartment_schedule": dict(
        desc="booking apartment viewings",
        names={"apartment_ask_apartment_name": "ask which apartment", "apartment_ask_day": "ask for the viewing day",
               "apartment_ask_start_time": "ask for the viewing start time",
               "apartment_ask_application_fee_paid": "ask whether the application fee is paid",
               "apartment_ask_custom_message": "ask for a message to the letting agency",
               "apartment_inform_viewing_available": "say the viewing slot is free and offer to book",
               "apartment_inform_viewing_unavailable": "say the viewing slot is not available",
               "apartment_inform_booking_successful": "confirm the viewing is booked",
               "apartment_inform_nothing_found": "say no matching apartment was found"},
        slots={"ask_name": "RenterName", "apartment_ask_apartment_name": "Name", "apartment_ask_day": "Day",
               "apartment_ask_start_time": "StartTimeHour", "apartment_ask_application_fee_paid": "ApplicationFeePaid",
               "apartment_ask_custom_message": "Message"},
        outcomes={"available": "apartment_inform_viewing_available", "unavailable": "apartment_inform_viewing_unavailable",
                  "success": "apartment_inform_booking_successful", "nothing": "apartment_inform_nothing_found"}),
    "bank_balance": dict(
        desc="telling customers their bank balance",
        names={"bank_ask_account_number": "ask for the account number", "bank_ask_pin": "ask for the PIN",
               "bank_ask_dob": "ask for the date of birth", "bank_ask_mothers_maiden_name": "ask for the mother's maiden name",
               "bank_ask_childhood_pets_name": "ask for the childhood pet's name",
               "bank_inform_cannot_authenticate": "say the customer cannot be authenticated",
               "bank_inform_balance": "tell the customer the balance",
               "bank_inform_nothing_found": "say no balance was found for the account"},
        slots={"ask_name": "FullName", "bank_ask_account_number": "AccountNumber", "bank_ask_pin": "PIN",
               "bank_ask_dob": "DateOfBirth", "bank_ask_mothers_maiden_name": "SecurityAnswer1",
               "bank_ask_childhood_pets_name": "SecurityAnswer2"},
        outcomes={"result": "bank_inform_balance", "failure": "bank_inform_cannot_authenticate",
                  "nothing": "bank_inform_nothing_found"}),
    "bank_fraud_report": dict(
        desc="taking bank fraud reports",
        names={"bank_ask_account_number": "ask for the account number", "bank_ask_pin": "ask for the PIN",
               "bank_ask_dob": "ask for the date of birth", "bank_ask_mothers_maiden_name": "ask for the mother's maiden name",
               "bank_ask_childhood_pets_name": "ask for the childhood pet's name",
               "bank_ask_fraud_details": "ask for the details of the fraud",
               "bank_inform_cannot_authenticate": "say the customer cannot be authenticated",
               "bank_inform_fraud_report_submitted": "confirm the fraud report was submitted",
               "bank_inform_nothing_found": "say the account could not be found"},
        slots={"ask_name": "FullName", "bank_ask_account_number": "AccountNumber", "bank_ask_pin": "PIN",
               "bank_ask_dob": "DateOfBirth", "bank_ask_mothers_maiden_name": "SecurityAnswer1",
               "bank_ask_childhood_pets_name": "SecurityAnswer2"},
        outcomes={"success": "bank_inform_fraud_report_submitted", "failure": "bank_inform_cannot_authenticate",
                  "nothing": "bank_inform_nothing_found"}),
    "doctor_followup": dict(
        desc="giving patients their doctor's follow-up instructions",
        names={"doctor_ask_doctor_name": "ask who the patient's doctor is",
               "doctor_inform_doctors_instructions": "tell the patient the doctor's instructions",
               "doctor_inform_nothing_found": "say no doctor is available"},
        slots={"ask_name": "PatientName", "doctor_ask_doctor_name": "Name"},
        outcomes={"result": "doctor_inform_doctors_instructions", "nothing": "doctor_inform_nothing_found"}),
    "doctor_schedule": dict(
        desc="booking doctor appointments",
        names={"doctor_ask_doctor_name": "ask which doctor", "doctor_ask_day": "ask for the appointment day",
               "doctor_ask_start_time": "ask for the appointment time", "doctor_ask_symptoms": "ask for the symptoms",
               "doctor_inform_booking_available": "say the doctor is free and offer to book",
               "doctor_inform_booking_unavailable": "say the doctor is not free then",
               "doctor_inform_booking_successful": "confirm the appointment is booked",
               "doctor_inform_nothing_found": "say no doctor is available"},
        slots={"ask_name": "PatientName", "doctor_ask_doctor_name": "Name", "doctor_ask_day": "Day",
               "doctor_ask_start_time": "StartTimeHour", "doctor_ask_symptoms": "Symptoms"},
        outcomes={"available": "doctor_inform_booking_available", "unavailable": "doctor_inform_booking_unavailable",
                  "success": "doctor_inform_booking_successful", "nothing": "doctor_inform_nothing_found"}),
    "hotel_book": dict(
        desc="reserving hotel rooms",
        names={"hotel_ask_hotel": "ask which hotel", "hotel_ask_date_from": "ask for the arrival date",
               "hotel_ask_date_to": "ask for the departure date",
               "hotel_ask_customer_request": "ask for any special requests",
               "hotel_unavailable": "say no room is available for those dates",
               "hotel_ask_confirm_booking": "say a room is free and offer to book",
               "hotel_reservation_succeeded": "confirm the reservation", "hotel_reservation_failed": "say the reservation failed",
               "hotel_inform_nothing_found": "say no matching hotel was found"},
        slots={"ask_name": "CustomerName", "hotel_ask_hotel": "Name", "hotel_ask_date_from": "StartDate",
               "hotel_ask_date_to": "EndDate", "hotel_ask_customer_request": "CustomerRequest"},
        outcomes={"available": "hotel_ask_confirm_booking", "unavailable": "hotel_unavailable",
                  "success": "hotel_reservation_succeeded", "failure": "hotel_reservation_failed",
                  "nothing": "hotel_inform_nothing_found"}),
    "hotel_service_request": dict(
        desc="hotel room-service requests",
        names={"hotel_ask_hotel": "ask which hotel the guest is staying at", "hotel_ask_room_number": "ask for the room number",
               "hotel_ask_service_request": "ask what service is wanted", "hotel_ask_time": "ask when the service is wanted",
               "hotel_inform_service_request_successful": "confirm the service request",
               "hotel_inform_service_request_failed": "say the service request failed",
               "hotel_inform_nothing_found": "say no matching service was found"},
        slots={"ask_name": "CustomerName", "hotel_ask_hotel": "Name", "hotel_ask_room_number": "RoomNumber",
               "hotel_ask_service_request": "CustomerRequest", "hotel_ask_time": "Time"},
        outcomes={"success": "hotel_inform_service_request_successful", "failure": "hotel_inform_service_request_failed",
                  "nothing": "hotel_inform_nothing_found"}),
    "meeting_schedule": dict(
        desc="scheduling meetings",
        names={"meeting_ask_guest_name": "ask who the meeting is with", "meeting_ask_day": "ask for the meeting day",
               "meeting_ask_start_time": "ask for the start time", "meeting_ask_end_time": "ask for the end time",
               "meeting_ask_reason": "ask for an optional meeting reason",
               "meeting_inform_confirmed": "confirm the meeting is scheduled",
               "meeting_inform_unavailable_ask_different_time": "say the guest cannot make it and offer another time",
               "meeting_inform_nothing_found": "say the guest is not in the system"},
        slots={"ask_name": "UserName", "meeting_ask_guest_name": "Name", "meeting_ask_day": "Day",
               "meeting_ask_start_time": "StartTimeHour", "meeting_ask_end_time": "EndTimeHour",
               "meeting_ask_reason": "MeetingReason"},
        outcomes={"success": "meeting_inform_confirmed", "unavailable": "meeting_inform_unavailable_ask_different_time",
                  "nothing": "meeting_inform_nothing_found"}),
    "party_plan": dict(
        desc="planning and booking parties at venues",
        names={"party_ask_venue": "ask which venue", "party_ask_number_of_guests": "ask how many guests",
               "party_ask_starting_time": "ask for the start time", "party_ask_day": "ask for the party day",
               "party_ask_food": "ask what food to order", "party_ask_drinks": "ask what drinks to serve",
               "party_inform_food_drink_criteria": "ask whether specific food or drinks are wanted",
               "party_venue_not_available": "say the venue is not available then",
               "party_no_venue_available": "say every venue is booked out",
               "party_ask_confirm_booking": "say the venue is free and offer to book",
               "party_booking_successful": "confirm the party is booked", "party_booking_failed": "say the booking failed"},
        slots={"ask_name": "HostName", "party_ask_venue": "Name", "party_ask_number_of_guests": "NumberGuests",
               "party_ask_starting_time": "StartTimeHour", "party_ask_day": "Day"},
        outcomes={"available": "party_ask_confirm_booking", "unavailable": "party_venue_not_available",
                  "success": "party_booking_successful", "failure": "party_booking_failed"}),
    "party_rsvp": dict(
        desc="RSVPing to parties",
        names={"party_ask_venue": "ask where the party is", "party_ask_host": "ask for the host's name",
               "party_ask_arrival_time": "ask for the arrival time", "party_ask_number_of_guests": "ask how many guests are coming along",
               "party_ask_parking_needed": "ask whether parking is needed",
               "party_ask_dietary_restrictions": "ask about dietary restrictions",
               "party_confirm_rsvp": "confirm the RSVP", "party_inform_nothing_found": "say no matching party was found"},
        slots={"ask_name": "GuestName", "party_ask_venue": "Name", "party_ask_host": "HostName",
               "party_ask_arrival_time": "ArrivalTime", "party_ask_number_of_guests": "NumberGuests",
               "party_ask_parking_needed": "NeedParking", "party_ask_dietary_restrictions": "DietaryRestrictions"},
        outcomes={"success": "party_confirm_rsvp", "nothing": "party_inform_nothing_found"}),
    "plane_book": dict(
        desc="reserving flights by flight ID",
        names={"plane_ask_flight_id": "ask for the flight ID",
               "plane_flight_available": "say the flight is available and offer to reserve",
               "plane_flight_unavailable": "say the flight is no longer available",
               "plane_reservation_succeeded": "confirm the flight is reserved",
               "plane_reservation_failed": "say the reservation failed",
               "plane_inform_nothing_found": "say no matching flight was found"},
        slots={"ask_name": "CustomerName", "plane_ask_flight_id": "id"},
        outcomes={"available": "plane_flight_available", "unavailable": "plane_flight_unavailable",
                  "success": "plane_reservation_succeeded", "failure": "plane_reservation_failed",
                  "nothing": "plane_inform_nothing_found"}),
    "restaurant_book": dict(
        desc="restaurant reservations",
        names={"restaurant_ask_restaurant": "ask which restaurant", "restaurant_ask_time": "ask for the reservation time",
               "restaurant_ask_size": "ask for the party size",
               "restaurant_inform_unavailable": "say the restaurant cannot take the booking",
               "restaurant_ask_confirm_booking": "say the restaurant can take them and offer to confirm",
               "restaurant_inform_booking_successful": "confirm the reservation",
               "restaurant_inform_booking_failed": "say the reservation failed",
               "restaurant_inform_nothing_found": "say no matching restaurant was found"},
        slots={"ask_name": "CustomerName", "restaurant_ask_restaurant": "Name", "restaurant_ask_time": "Time",
               "restaurant_ask_size": "PartySize"},
        outcomes={"available": "restaurant_ask_confirm_booking", "unavailable": "restaurant_inform_unavailable",
                  "success": "restaurant_inform_booking_successful", "failure": "restaurant_inform_booking_failed",
                  "nothing": "restaurant_inform_nothing_found"}),
    "ride_book": dict(
        desc="booking taxi rides",
        names={"ride_ask_destination": "ask for the destination", "ride_ask_departure": "ask for the pick-up point",
               "ride_ask_confirm_booking": "describe the ride found and offer to book",
               "ride_confirm_booking": "confirm the ride is booked with plate and booking ID",
               "ride_provide_driver_details": "tell the user the driver's name",
               "ride_inform_search_criteria": "mention the optional ride filters",
               "ride_inform_nothing_found": "say no ride matches"},
        slots={"ask_name": "CustomerName", "ride_ask_destination": "ArrivalLocation",
               "ride_ask_departure": "DepartureLocation"},
        outcomes={"available": "ride_ask_confirm_booking", "success": "ride_confirm_booking",
                  "nothing": "ride_inform_nothing_found"}),
    "ride_change": dict(
        desc="changing or cancelling booked rides",
        names={"ride_ask_change": "ask what should be changed", "ride_ask_booking_number": "ask for the booking ID",
               "ride_inform_changes_successful": "confirm the change was made",
               "ride_inform_changes_failed": "say the change could not be made",
               "ride_inform_nothing_found": "say no matching ride was found"},
        slots={"ask_name": "CustomerName", "ride_ask_booking_number": "id", "ride_ask_change": "ChangeDescription"},
        outcomes={"success": "ride_inform_changes_successful", "failure": "ride_inform_changes_failed",
                  "nothing": "ride_inform_nothing_found"}),
    "spaceship_access_codes": dict(
        desc="checking spaceship door access codes",
        names={"spaceship_ask_rank": "ask for the user's rank", "spaceship_ask_code": "ask for the code",
               "spaceship_ask_code_type": "ask for the code type",
               "spaceship_inform_outcome": "report the system's outcome message",
               "spaceship_inform_nothing_found": "say nothing matched the search"},
        slots={"ask_name": "UserName", "spaceship_ask_rank": "UserRank", "spaceship_ask_code": "Code",
               "spaceship_ask_code_type": "CodeType"},
        outcomes={"result": "spaceship_inform_outcome", "success": "spaceship_inform_outcome",
                  "failure": "spaceship_inform_outcome", "nothing": "spaceship_inform_nothing_found"}),
    "spaceship_life_support": dict(
        desc="restoring spaceship life support",
        names={"spaceship_ask_lock_manufacturer": "ask for the lock manufacturer",
               "spaceship_ask_colour_top_cable": "ask for the top cable's colour",
               "spaceship_ask_colour_second_cable": "ask for the second cable's colour",
               "spaceship_inform_outcome": "report the system's outcome message",
               "spaceship_inform_nothing_found": "say nothing matched the search"},
        slots={"spaceship_ask_lock_manufacturer": "LockManufacturer", "spaceship_ask_colour_top_cable": "ColorOfTopCable",
               "spaceship_ask_colour_second_cable": "ColorOfSecondCable"},
        outcomes={"result": "spaceship_inform_outcome", "success": "spaceship_inform_outcome",
                  "nothing": "spaceship_inform_nothing_found"}),
}
OUTCOME_PHRASE = {
    "available": "reports that the requested option is available",
    "unavailable": "reports that the requested option is unavailable, booked or conflicting",
    "success": "reports that the booking or request went through",
    "failure": "reports that the booking or request failed or the details could not be verified",
    "nothing": "returns no matching record at all",
    "result": "returns the requested information",
}
INTERNAL = {"yes", "no", "available", "unavailable", "query_success", "query_failure", "info_missing", "info_missing2"}
YES = re.compile(r"^\W*(yes|yeah|yep|yup|sure|ok|okay|please|go ahead|book it|do it|that works|sounds good|perfect|great|absolutely|definitely|correct|y)\b", re.I)
NO = re.compile(r"^\W*(no|nope|nah|not really|not now|that's all|that is all|nothing|i'm good|im good|i am good|all good|thanks|thank you)\b", re.I)
FORGOT = re.compile(r"(don'?t|do not|can'?t|cannot|can not) (remember|recall|find|know|have)|forgot|lost (my|it)|no idea", re.I)


def action_defs(task, spec, graph, replies):
    """Claude-written definition templates filled from this task's flow chart (graph) and the names above."""
    names = dict(COMMON)
    names.update(spec["names"])
    acts = [a for a in replies if a not in INTERNAL and not a.startswith("goodbye") and not a.endswith("_bye")]
    acts = [a for a in acts if a in names] + ["BYE"]
    pred = collections.defaultdict(list)
    for a, b in graph.items():
        pred[b].append(a)
    chain, cur, seen = [], graph.get("hello"), set()
    while cur and cur not in seen and cur not in ("query", "query_check"):
        seen.add(cur)
        chain.append(cur)
        cur = graph.get(cur)
    asked = ", ".join(names[a].replace("ask for ", "").replace("ask about ", "").replace("ask ", "").replace("the user's name", "name") for a in chain if a.startswith(("ask", "bank_ask", "party_ask", "doctor_ask", "hotel_ask", "meeting_ask", "plane_ask", "restaurant_ask", "ride_ask", "spaceship_ask", "apartment_ask"))) or "the required details"
    out = {}
    offer = [a for a in (spec["outcomes"].get("available"),) if a]
    for a in acts:
        n = names[a]
        if a == "hello":
            d = "Open with 'Hello, how can I help?'; only for the assistant's very first turn, before anything else is done."
        elif a == "BYE":
            d = "Say goodbye: when the user indicates they need nothing more, typically answering no to 'is there anything else?'."
        elif a == "anything_else":
            d = "Ask whether the user needs anything else: right after the task's final result (confirmation, failure or information) has been told to the user."
        elif a == "out_of_scope":
            d = f"Say the assistant can only help with {spec['desc']}: when the user asks for something outside that task."
        elif a in ("query", "query_check"):
            verb = "check availability in the system" if a == "query_check" else "submit the lookup to the system"
            d = f"{verb[0].upper() + verb[1:]}: once all details the chart collects ({asked}) are known; say nothing about the result before it."
        elif a == "query_book":
            d = "Book it in the system: only after the user has said yes to the assistant's offer to book the option that was found available."
        elif a in spec["outcomes"].values():
            outs = [o for o, x in spec["outcomes"].items() if x == a]
            ph = " or ".join(OUTCOME_PHRASE[o] for o in outs)
            d = f"{n[0].upper() + n[1:]}: when the most recent system lookup {ph}."
        elif a == "bank_ask_dob":
            d = "Ask for the date of birth: the security-question route, used when the customer says they cannot remember their account number or PIN."
        elif a == "bank_ask_mothers_maiden_name":
            d = "Ask for the mother's maiden name: the security-question step right after the date of birth has been given."
        elif a == "bank_ask_childhood_pets_name":
            d = "Ask for the childhood pet's name: the last security question, right after the mother's maiden name has been given."
        elif a == "bank_ask_fraud_details":
            d = ("Ask for a detailed fraud report: in this flow chart it comes right after the PIN; it is asked even if the "
                 "customer mentioned the fraud earlier, because the report is taken only after identification.")
        elif a == "ride_inform_search_criteria":
            d = "Mention the optional ride filters (provider, driver, car model): the step after the pick-up point is known, before searching for rides."
        elif a == "ride_provide_driver_details":
            d = "Tell the user the driver's name: only when the user asks who the driver is, after a ride has been found or booked."
        elif a == "party_inform_food_drink_criteria":
            d = "Ask whether specific food or drinks are wanted: the step after the number of guests is known, before checking the venue."
        elif a in ("party_ask_food", "party_ask_drinks"):
            d = f"{n[0].upper() + n[1:]}: only after the user has said they want specific {'food' if a.endswith('food') else 'drinks'} at the party."
        else:
            ps = [p for p in pred.get(a, []) if p not in INTERNAL]
            if ps == ["hello"]:
                d = (f"{n[0].upper() + n[1:]}: the first step after the greeting; choose it once the user has said what "
                     f"they want, unless they already gave this information.")
            elif ps:
                d = (f"{n[0].upper() + n[1:]}: comes right after '{names.get(ps[0], ps[0])}' in this flow chart; choose it "
                     f"once earlier steps are settled and the user has not yet given this.")
            elif a == "party_no_venue_available":
                d = ("Say every venue is booked out: only when the lookups show that no venue at all can host the party at the "
                     "requested day and time, not just that one venue is taken.")
            else:
                d = f"{n[0].upper() + n[1:]}: only when the flow chart reaches this step and the user has not yet given this information."
            if "no" in graph and graph["no"] == a and offer:
                d += " Also used when the user declines the offered booking."
        out[n] = d
    return out, {a: names[a] for a in acts}


def outcome_of(task, e):
    it = e.get("Item")
    if not it:
        return "nothing" if e.get("TotalItems") in (0, "0", None) else None
    if not isinstance(it, dict):
        return None
    msg = str(it.get("Message") or "")
    for k in ("ReservationStatus", "RequestStatus", "ChangeStatus"):
        if k in it:
            v = str(it[k]).lower()
            return "failure" if ("fail" in v or "unable" in v) else "success"
    if "Confirmation" in it:
        return "success"
    if msg:
        m = msg.lower()
        if task.startswith("spaceship"):
            return "result"
        if "too small" in m:
            return None
        if m.startswith("you must provide"):
            return "failure"
        if m in ("unavailable",) or "unavailable" in m or "conflicting" in m or "booked at that time" in m:
            return "unavailable"
        if m == "available" or "is available" in m:
            return "available"
        if "success" in m or "confirmed" in m or m.startswith("ride booked") or "thank you for your rsvp" in m:
            return "success"
        if "failed" in m:
            return "failure"
        if task == "doctor_followup":
            return "result"
        return None
    if task == "bank_balance" and "BankBalance" in it:
        return "result"
    if task == "ride_book" and "ArrivalLocation" in it:
        return "available"
    return None


def fmt_constraints(cons):
    parts = []
    for c in cons or []:
        for k, v in c.items():
            if k == "RequestType":
                continue
            v = re.sub(r'^api\.\w+\((.*)\)$', r"\1", str(v)).strip('"').replace('\\"', '"').replace('"', "")
            parts.append(f"{k}={v}")
    return ", ".join(parts)


def fmt_item(it):
    if not it:
        return "no matching record"
    if isinstance(it, dict):
        msg = it.get("Message")
        rest = {k: v for k, v in it.items() if k not in ("APIName", "Message", "id") and not isinstance(v, (list, dict))}
        s = "; ".join(f"{k}: {v}" for k, v in list(rest.items())[:8])
        return (str(msg) + (" (" + s + ")" if s else "")) if msg else s
    return str(it)[:300]


def slot_values(events, field):
    vals = set()
    for e in events:
        if e["Action"] == "query":
            for c in e.get("Constraints") or []:
                if field in c:
                    v = re.sub(r'^api\.\w+\((.*)\)$', r"\1", str(c[field]))
                    for x in re.findall(r'[^"\[\],]+', v):
                        x = x.strip().lower()
                        if len(x) >= 3 and x not in ("null", "none", "true", "false", "yes", "no"):
                            vals.add(x)
    return vals


def ensure_repo():
    repo = C.CACHE / KEY / "repo"
    if not (repo / ".git").exists():
        repo.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "remote", "add", "origin", GIT_URL], cwd=repo, check=True)
        subprocess.run(["git", "fetch", "-q", "--depth", "1", "origin", REV], cwd=repo, check=True)
        subprocess.run(["git", "checkout", "-q", "FETCH_HEAD"], cwd=repo, check=True)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    assert head == REV, head
    h = hashlib.sha256()
    for p in sorted(list((repo / "dialogues").glob("*.json")) + list((repo / "tasks").glob("*/*.json"))):
        h.update(p.name.encode())
        h.update(p.read_bytes())
    digest = h.hexdigest()
    pins = json.loads(PIN_FILE.read_text()) if PIN_FILE.exists() else {}
    if "content_sha256" in pins:
        assert pins["content_sha256"] == digest, "STAR content digest changed"
    else:
        PIN_FILE.write_text(json.dumps({"rev": REV, "content_sha256": digest}, indent=1) + "\n")
    return repo, digest


def main():
    repo, digest = ensure_repo()
    breadth = set()
    if BREADTH_STAR.exists():
        breadth = {json.loads(l)["rid"] for l in open(BREADTH_STAR)}
    specs = {}
    for task, spec in TASKS.items():
        tj = json.loads((repo / "tasks" / task / f"{task}.json").read_text())
        defs, names = action_defs(task, spec, tj["graph"], tj["replies"])
        assert len(set(names.values())) == len(names), task
        specs[task] = (tj["graph"], defs, names)
    stats = collections.Counter()
    cands = []  # (dialogue_id, task, gold_action, state)
    for p in sorted((repo / "dialogues").glob("*.json"), key=lambda p: int(p.stem)):
        d = json.loads(p.read_text())
        sc = d["Scenario"]
        did = str(d["DialogueID"])
        if sc.get("MultiTask") or d.get("CompletionLevel") != "Complete":
            continue
        task = sc["WizardCapabilities"][0]["Task"]
        if task not in specs:
            continue
        if did in breadth:
            stats["breadth_excluded"] += 1
            continue
        graph, defs, names = specs[task]
        ev = d["Events"]
        lines = []          # visible transcript so far
        last_act = None     # last wizard action label (or query_check / query_book / query)
        since = []          # visible events since last wizard action
        last_outcome = None
        for i, e in enumerate(ev):
            act, ag = e["Action"], e["Agent"]
            gold = None
            if ag == "Wizard" and act == "pick_suggestion":
                gold = e.get("ActionLabel")
            elif ag == "Wizard" and act == "query":
                rt = [str(list(c.values())[0]).strip('"') for c in e.get("Constraints") or [] if "RequestType" in c]
                gold = ("query_book" if rt == ["Book"] else "query_check" if rt == ["Check"] else "query"
                        if not rt else None)
                if gold in ("query_book", "query_check") and "query_check" not in graph.values() and "query_book" not in graph.values():
                    gold = None
            if gold is not None:
                g = "BYE" if gold in BYE else gold
                ok = False
                via_no = False  # review fix: edge 'negation' only when the gold follows the user's "no"
                users = [x for x in since if x[0] == "user"]
                kinds = {x[0] for x in since}
                if g in names and g not in ("hello", "out_of_scope") and "wizard_utter" not in kinds:
                    if last_outcome is not None and not users:
                        ok = TASKS[task]["outcomes"].get(last_outcome) == g
                    elif last_act is not None and users and "kb" not in kinds:
                        u = users[-1][1]
                        succ = graph.get(last_act)
                        if last_act in TASKS[task]["outcomes"].values() and last_act == TASKS[task]["outcomes"].get("available"):
                            if YES.search(u) and not NO.search(u):
                                ok = g == graph.get("yes", "query_book") or (g == "query_book")
                            elif NO.search(u) and not YES.search(u):
                                ok = "no" in graph and g == graph["no"]
                                via_no = ok
                        elif last_act == "anything_else":
                            ok = g == "BYE" and bool(NO.search(u))
                        elif last_act in ("bank_ask_account_number", "bank_ask_pin") and FORGOT.search(u):
                            ok = g == "bank_ask_dob"
                        elif succ is not None and g == succ and not FORGOT.search(u):
                            ok = True
                        if ok and g in TASKS[task]["slots"]:
                            vals = slot_values(ev, TASKS[task]["slots"][g])
                            prior = " ".join(x[1] for x in lines_user(lines)).lower()
                            if any(v in prior for v in vals):
                                ok = False
                                stats["slot_already_given"] += 1
                    elif (last_act is None and users and g == graph.get("hello")
                          and not any(k == "wizard" for k, _ in lines)):
                        ok = True  # first step after the user stated the request (no greeting pick yet)
                        if g in TASKS[task]["slots"]:
                            vals = slot_values(ev, TASKS[task]["slots"][g])
                            prior = " ".join(x[1] for x in lines_user(lines)).lower()
                            if any(v in prior for v in vals):
                                ok = False
                                stats["slot_already_given"] += 1
                if ok and lines:
                    state = f"Assistant's task: {TASKS[task]['desc']}.\n" + "\n".join(l for _, l in lines)
                    cands.append((did, task, g, state, via_no))
                    stats["cand"] += 1
                # now apply the action to the transcript
                if act == "pick_suggestion":
                    lines.append(("wizard", "Assistant: " + re.sub(r"\s+", " ", e.get("Text", "")).strip()))
                    last_act = e.get("ActionLabel")
                    if last_act == "custom":
                        last_act = None
                else:
                    kind = {"query_book": "BOOK", "query_check": "CHECK"}.get(gold, "LOOKUP")
                    lines.append(("kb", f"[Assistant sends a {kind} request to the system: {fmt_constraints(e.get('Constraints'))}]"))
                    last_act = gold
                since, last_outcome = [], None
                continue
            if ag == "Wizard" and act == "pick_suggestion":  # custom picks with no usable label
                lines.append(("wizard", "Assistant: " + re.sub(r"\s+", " ", e.get("Text", "")).strip()))
                since, last_act, last_outcome = [("wizard_utter", "")], None, None
            elif ag == "Wizard" and act == "utter":
                lines.append(("wizard", "Assistant: " + re.sub(r"\s+", " ", e.get("Text", "")).strip()))
                since.append(("wizard_utter", ""))
                last_act, last_outcome = None, None
            elif ag == "User" and act == "utter":
                t = re.sub(r"\s+", " ", e.get("Text", "")).strip()
                lines.append(("user", "User: " + t))
                since.append(("user", t))
            elif act == "return_item":
                lines.append(("kb", f"[System result: {fmt_item(e.get('Item'))}]"))
                last_outcome = outcome_of(task, e)
                since.append(("kbres", ""))
    # one decision point per dialogue, balanced over actions; seeded order
    rng = random.Random(SEED)
    by_dlg = collections.defaultdict(list)
    for c in cands:
        by_dlg[c[0]].append(c)
    order = sorted(by_dlg, key=lambda x: hashlib.md5(f"{SEED}:{x}".encode()).hexdigest())
    counts = collections.Counter()
    chosen = []
    for did in order:
        opts = by_dlg[did]
        best = min(opts, key=lambda c: (counts[c[2]], hashlib.md5(f"{SEED}:{did}:{c[3]}".encode()).hexdigest()))
        counts[best[2]] += 1
        chosen.append(best)
    # cap very common action types so no generic action dominates
    per_type_cap = 220
    kept, tc = [], collections.Counter()
    for c in chosen:
        if tc[c[2]] >= per_type_cap:
            continue
        tc[c[2]] += 1
        kept.append(c)
    rows, seen = [], set()
    for did, task, g, state, via_no in kept:
        n = C.norm(state)
        if n in seen:
            continue
        seen.add(n)
        graph, defs, names = specs[task]
        opts = sorted(defs)
        gold = names[g]
        edge = None
        if g == "bank_ask_dob":
            edge = "missing_info"
        elif via_no or (g == "BYE"):
            edge = "negation"
        if edge is None and len(state) > 1200:
            edge = "long_context"
        rows.append({
            "key": KEY, "rid": did, "state": state,
            "instructions": f"Following its flow chart for {TASKS[task]['desc']}, what should the assistant do next?",
            "options": opts, "gold": gold, "soft": None,
            "meta": {"dataset": "STAR (RasaHQ/STAR, Mosig et al. 2020)", "config": f"task={task}; next wizard action",
                     "revision": f"git:{REV}; content-sha256:{digest}", "licence": LICENCE, "split": "train",
                     "orig_label": {"task": task, "action": g}, "family": C.FAMILY, "edge": edge, "defs": task,
                     "seed": SEED}})
    rng.shuffle(rows)
    rows = rows[:MAX_ROWS]
    rows = C.cap_label(rows, lambda r: r["gold"], 0.5)
    rows = C.near_dedupe(rows, lambda r: " ".join(l for l in r["state"].split("\n") if l.startswith("User: ")))
    out, rows = C.write_rows(rows, KEY)
    for task, (graph, defs, names) in specs.items():
        C.write_defs(defs, KEY, task)
    print(dict(stats))
    print(f"candidates={len(cands)} dialogues_with_cands={len(by_dlg)} wrote {len(rows)} -> {out}")
    C.report(rows, qkey=lambda r: r["meta"]["defs"])
    print("action types:", collections.Counter(r["meta"]["orig_label"]["action"] for r in rows).most_common())


def lines_user(lines):
    return [(k, l[len("User: "):]) for k, l in lines if k == "user"]


if __name__ == "__main__":
    main()
