"""families/T32/vocab.py: T32 closed value sets that BOTH solvers read (pure data, no logic; G0_SPEC.md R4, R13).

These are the pool-level value sets a parser needs to read a slot back: the task phrases (category TASK), the events
a conditional commitment depends on (category COND) and the chat topics (category TOPIC). The decision rules (event
semantics, the status order, the card text) are NOT here: solver A (plugin.py) and solver B (solver_b.py) each keep
their own copy, written from G0_SPEC.md.

Stand-in status (A37 f, before A38): every phrase below is a Claude-written placeholder so the code and the in-memory
tests run. After A38 they are replaced by the frozen, G13-seed-clean Haiku packs (spec 3.0: >= 25 packs); the shape
stays fixed: tasks are infinitive verb phrases ("return the drill"), events are noun phrases that "go ahead" or "are
called off", topics are noun phrases. Every surface is lower-case, unique across all three sets, digit-free and free
of negation cues, status words and label words.
"""
from __future__ import annotations

FAMILY = "T32"

# pack -> (task keys, event keys, topic keys); a card draws one pack
PACKS = {
    "home": (("water_plants", "return_drill", "book_plumber", "collect_parcel", "clear_gutter", "mow_lawn",
              "drop_spare_key", "pay_window_cleaner"),
             ("street_party", "school_trip", "family_barbecue", "boiler_inspection", "garden_open_day"),
             ("house_move", "spring_cleanup", "garden_project")),
    "rental": (("fix_boiler", "send_renewal", "repaint_hallway", "return_deposit", "replace_smoke_alarm",
                "pay_rent_topup", "clean_stairs", "change_door_lock"),
               ("building_survey", "council_inspection", "flat_viewing", "roof_repair_visit", "meter_reading_visit"),
               ("flat_repairs", "lease_renewal", "move_out_checklist")),
    "freelance": (("send_logo_drafts", "share_invoice", "deliver_final_edit", "review_contract", "upload_photo_set",
                   "update_landing_page", "send_source_files", "draft_press_release"),
                  ("client_workshop", "product_launch", "photo_shoot", "budget_review", "trade_fair"),
                  ("website_launch", "brand_refresh", "video_project")),
    "team": (("write_release_notes", "fix_login_bug", "update_onboarding_doc", "run_backup_test", "book_meeting_room",
              "send_progress_report", "prepare_demo", "review_pull_request"),
             ("sprint_review", "client_demo", "team_offsite", "security_audit", "board_meeting"),
             ("quarterly_release", "office_move", "hiring_push")),
    "club": (("order_club_shirts", "book_minibus", "print_match_flyers", "collect_raffle_prizes", "set_up_sound",
              "bake_stall_cakes", "update_members_list", "arrange_trophy_engraving"),
             ("charity_run", "summer_fair", "away_match", "quiz_night", "awards_dinner"),
             ("fair_planning", "club_anniversary", "fundraising_drive")),
    "family": (("pick_up_prescription", "book_cottage", "sort_birthday_present", "fix_bike_chain",
                "call_insurer", "renew_car_tax", "frame_wedding_photos", "pack_camping_gear"),
               ("camping_trip", "wedding_rehearsal", "cousins_visit", "school_play", "beach_day"),
               ("summer_holiday", "family_reunion", "anniversary_party")),
}
PACK_ORDER = ("home", "rental", "freelance", "team", "club", "family")

TASKS = {
    "water_plants": "water the plants", "return_drill": "return the drill", "book_plumber": "book the plumber",
    "collect_parcel": "collect the parcel", "clear_gutter": "clear the gutter", "mow_lawn": "mow the back lawn",
    "drop_spare_key": "drop off the spare key", "pay_window_cleaner": "pay the window cleaner",
    "fix_boiler": "fix the boiler", "send_renewal": "send the tenancy renewal", "repaint_hallway": "repaint the hallway",
    "return_deposit": "return the deposit", "replace_smoke_alarm": "replace the smoke alarm",
    "pay_rent_topup": "pay the rent top-up", "clean_stairs": "clean the shared stairs",
    "change_door_lock": "change the front door lock",
    "send_logo_drafts": "send the logo drafts", "share_invoice": "share the invoice",
    "deliver_final_edit": "deliver the final edit", "review_contract": "review the contract",
    "upload_photo_set": "upload the photo set", "update_landing_page": "update the landing page",
    "send_source_files": "send the source files", "draft_press_release": "draft the press release",
    "write_release_notes": "write the release notes", "fix_login_bug": "fix the login bug",
    "update_onboarding_doc": "update the onboarding doc", "run_backup_test": "run the backup test",
    "book_meeting_room": "book the meeting room", "send_progress_report": "send the progress report",
    "prepare_demo": "prepare the demo", "review_pull_request": "review the pull request",
    "order_club_shirts": "order the club shirts", "book_minibus": "book the minibus",
    "print_match_flyers": "print the match flyers", "collect_raffle_prizes": "collect the raffle prizes",
    "set_up_sound": "set up the sound system", "bake_stall_cakes": "bake the cakes for the stall",
    "update_members_list": "update the members list", "arrange_trophy_engraving": "arrange the trophy engraving",
    "pick_up_prescription": "pick up the prescription", "book_cottage": "book the holiday cottage",
    "sort_birthday_present": "sort the birthday present", "fix_bike_chain": "fix the bike chain",
    "call_insurer": "call the insurance company", "renew_car_tax": "renew the car tax",
    "frame_wedding_photos": "frame the wedding photos", "pack_camping_gear": "pack the camping gear",
}
CONDS = {
    "street_party": "the street party", "school_trip": "the school trip", "family_barbecue": "the family barbecue",
    "boiler_inspection": "the boiler inspection", "garden_open_day": "the garden open day",
    "building_survey": "the building survey", "council_inspection": "the council inspection",
    "flat_viewing": "the flat viewing", "roof_repair_visit": "the roof repair visit",
    "meter_reading_visit": "the meter reading visit",
    "client_workshop": "the client workshop", "product_launch": "the product launch", "photo_shoot": "the photo shoot",
    "budget_review": "the budget review", "trade_fair": "the trade fair",
    "sprint_review": "the sprint review", "client_demo": "the client demo", "team_offsite": "the team offsite",
    "security_audit": "the security audit", "board_meeting": "the board meeting",
    "charity_run": "the charity run", "summer_fair": "the summer fair", "away_match": "the away match",
    "quiz_night": "the quiz night", "awards_dinner": "the awards dinner",
    "camping_trip": "the camping trip", "wedding_rehearsal": "the wedding rehearsal",
    "cousins_visit": "the visit from the cousins", "school_play": "the school play", "beach_day": "the beach day",
}
TOPICS = {
    "house_move": "the house move", "spring_cleanup": "the spring clean-up", "garden_project": "the garden project",
    "flat_repairs": "the flat repairs", "lease_renewal": "the lease renewal",
    "move_out_checklist": "the move-out checklist",
    "website_launch": "the website launch", "brand_refresh": "the brand refresh", "video_project": "the video project",
    "quarterly_release": "the quarterly release", "office_move": "the office move", "hiring_push": "the hiring push",
    "fair_planning": "the fair planning", "club_anniversary": "the club anniversary",
    "fundraising_drive": "the fundraising drive",
    "summer_holiday": "the summer holiday", "family_reunion": "the family reunion",
    "anniversary_party": "the anniversary party",
}
