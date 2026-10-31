# packs-3 shared seed banks (Claude-written). Used by build_packs.py to replace cross-pack duplicates.
# FILLER_BANK: inert office trivia for the F7 disjointness list; none mentions cleaning, money, dates, people's
# conduct, safety, health, vehicles or any domain decision, so a filler cannot imply a rubric factor.
FILLER_BANK = """
desk lamps rewired; staff photo board rearranged; lobby clock battery changed; meeting room whiteboard rehung;
visitor badges reprinted; kitchen fridge magnets sorted; corridor artwork rotated; printer paper trays relabelled;
coat hooks screwed in; staff mugs labelled; bookshelf in the break room levelled; pin board frames painted;
reception pens restocked; office calendar hung in the hallway; seminar room chairs restacked; noticeboard ribbon renewed;
lobby rug turned; lift music playlist changed; staff quiz trophy polished up; sticky note supply topped up;
meeting room projector remote found; filing cabinet keys copied; desk drawer handles tightened; break room radio moved;
lobby sofa cushions plumped; staff birthday list updated; office stapler refilled; paper clip jar refilled;
window seat cushion recovered; tea selection box restocked; corridor plant pots turned; water jug lids matched;
team photo reframed; staff room board game shelf sorted; spare chargers boxed; desk name plates engraved;
lanyard rack mounted; lobby welcome sign reworded; staff library book swap started; stationery cupboard door rehung;
coffee mug tree bought; office map redrawn for visitors; meeting room clock moved; whiteboard eraser replaced;
pen holder set bought; bulletin pins colour-coded; ceiling fan pull cord lengthened; reception bell polished up;
lunch table rearranged; corridor mirror rehung; staff room curtains rehemmed; desk calendar stand bought;
umbrella stand moved to the entrance; postcard wall started in the break room; staff room clock set to radio time;
filing labels typed; hallway chairs paired up; kettle cord tidy fitted; board game night poster drawn;
spare keyboard stored; desk tidy trays bought; office plant names written on tags; book ends added to shelves;
staff room jigsaw finished; magazine rack emptied of old issues; lobby leaflet stand turned; wall map pins replaced;
desk mats ordered; staff room cushions swapped; printer tray rollers changed; meeting room name plates fixed;
recipe swap folder started; team mascot plush washed; break room chalkboard redrawn; staff photo day planned;
corridor picture lights angled; window boxes repotted; staff room bunting stored; desk risers handed out;
whiteboard pens sorted by colour; spare chairs labelled; lobby guestbook replaced; staff poll on biscuits held;
reception plant trimmed; office paperweights collected; post tray stacked; staff room teapot glued;
noticeboard border renewed; corridor clock repainted; wall planner laminated; spare lanyards boxed;
stationery order list typed; lobby music volume lowered; staff room shelf brackets added; filing tray stickers printed;
book trolley wheel squeak oiled; desk fan grille straightened; meeting room blinds cord shortened; tea towel rail fitted;
staff room radio station changed; lobby fish named by staff; mug rack hooks added; desk phone cords tidied;
window latch painted; hallway rug rolled for storage; reception chair height adjusted; office quiz questions written;
staff room fruit bowl bought; paper recycling tray emptied into the bin room; whiteboard magnets counted; office bell tuned
"""
# INERT_BANK: generic civic-office inert fact types for F13 (purpose, contacts, schedules); no case attribute,
# condition, threshold or decision appears in any of them.
INERT_BANK = """
office opening hours; public counter location; general enquiries line; mailing address for correspondence;
staff training calendar; accessibility arrangements at the counter; translation and interpreting help;
records retention schedule; privacy notice reference; website section for forms; visitor parking at the office;
complaints procedure contact; public holiday closure list; reception floor plan; office newsletter title;
switchboard extension list; lost property desk hours; staff directory location; postal collection times;
building entrance for deliveries; meeting room booking contact; public wifi access notes; cafeteria opening times;
annual report publication month; office relocation history; department mission statement; organisation chart location;
visitor sign-in procedure; fire assembly point location; first aid room location; bicycle parking location;
bus stops near the office; office phone menu options; staff dress code notes; printing service location;
public notice board location; minutes archive location; data request contact; media enquiries contact;
volunteer programme contact; internship programme contact; customer charter title; service standards booklet title;
office lift locations; baby changing facilities location; prayer room location; quiet room location;
document drop box location; payment kiosk location; queue ticket machine location; waiting area seating notes;
evening appointment availability; weekend service notes; online chat service hours; email response guidance;
social media account names; office history plaque wording; partner agencies list; citizen panel contact;
public consultation page title; forms translation list; large print forms availability; hearing loop availability;
guide dog policy notes; signage languages list; staff name badge style; office photography rules
"""


def split_bank(text):
    return [x.strip() for x in " ".join(text.split()).split(";") if x.strip()]

# Combinatorial filler parts (Claude-written): object + action + place, used after FILLER_BANK runs out.
FILLER_OBJECTS = ["desk lamp", "notice frame", "coat hook", "mug rack", "pin board", "wall clock", "filing tray",
                  "pen pot", "door wedge", "umbrella stand", "book trolley", "tea caddy", "plant pot", "chair cushion",
                  "paper tray", "key rack", "wall map", "name plate", "magazine rack", "radio", "fruit bowl",
                  "calendar", "bookcase", "footstool", "spare monitor", "flower vase", "picture frame", "table lamp",
                  "letter tray", "cushion cover", "rug", "bench", "side table", "shelf bracket", "clipboard rack",
                  "wall planner", "hat stand", "biscuit tin", "tea towel rail", "kettle stand"]
FILLER_ACTIONS = ["shifted to the {loc}", "relabelled in the {loc}", "repainted in the {loc}", "swapped in the {loc}",
                  "rehung in the {loc}", "bought for the {loc}", "lent to the {loc}", "taken to the {loc}",
                  "tidied in the {loc}", "counted in the {loc}"]
FILLER_PLACES = ["break room", "reception area", "upper corridor", "staff kitchen", "post room", "east corridor",
                 "west stairwell", "training suite", "archive annex", "back office"]
