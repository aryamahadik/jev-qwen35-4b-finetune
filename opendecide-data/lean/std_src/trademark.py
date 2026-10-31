"""STD domain 'trademark': the Abercrombie distinctiveness spectrum (v0.11 parts).

Each item is an invented use of a mark on stated goods or services, with 1-3 sentences of
context, labelled generic / descriptive / suggestive / arbitrary / fanciful. Many items are
boundary cases (descriptive vs suggestive, arbitrary vs suggestive, arbitrary vs fanciful,
generic vs descriptive, made-up words built from meaningful parts), and many marks come as
twins: the same word used for different goods (same group_id). A few cross-mark minimal pairs
share one context (also grouped). A small set of yes/no ('noul') probes reuse item states.
All text is newly written by Claude as the teacher (no external model, no dataset text).

Writes:
  data/v11_parts/std/trademark.jsonl        (with gold)
  data/v11_parts/std/trademark.blind.jsonl  (identical rows, gold removed)
Deterministic and re-runnable.
"""
import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "data" / "v11_parts" / "std"
DOMAIN = "trademark"
SRC = f"std_{DOMAIN}"
SEED = 20261115

G, D, S, A, F = "generic", "descriptive", "suggestive", "arbitrary", "fanciful"
SCALE = [G, D, S, A, F]
CODE = {"G": G, "D": D, "S": S, "A": A, "F": F}
DEFS = {
    G: "the common name of the product or service itself, or of the class it belongs to; it "
       "tells buyers what the thing is rather than who makes it. Misspellings and "
       "foreign-language equivalents of such a name count as the name itself.",
    D: "directly describes a quality, feature, ingredient, purpose, function, characteristic, "
       "intended user, or geographic origin of the goods or services, including plain laudatory "
       "terms; a buyer needs no imagination to see what it says about them. Misspellings, "
       "translations, and run-together combinations of such words count the same way.",
    S: "hints at a quality or characteristic of the goods or services, but a buyer needs "
       "imagination, thought, or a mental leap to connect the mark to them.",
    A: "a real word (including an obscure, foreign, or misspelled one, judged by its meaning) "
       "whose ordinary meaning has no relation to the goods or services it is used for.",
    F: "an invented word with no meaning of its own, created to serve as a mark. A made-up word "
       "built from recognizable meaningful parts is judged by what those parts convey.",
}

# (key, mark, goods/services, gold code, difficulty 1-3, boundary tag or "", context)
ITEMS = [
    # ---------------- generic ----------------
    ("g_lantern", "LANTERN", "battery-powered lanterns for camping", "G", 1, "",
     "The rechargeable LED light has a carry handle and a hook for hanging from a tent loop. "
     "Outdoor stores shelve it next to other companies' lanterns."),
    ("g_velvet", "VELVET", "upholstery fabric sold by the yard", "G", 2, "G/D",
     "The mill weaves a cotton fabric with a short, dense, soft pile that the textile trade calls "
     "velvet, and that is the only fabric it sells under the name. Designers order it by color "
     "from a swatch book."),
    ("g_compass", "COMPASS", "baseplate navigation instruments for hikers and orienteers", "G", 1, "",
     "Each unit is a magnetized needle in a liquid-filled capsule mounted on a clear plastic "
     "baseplate with a rotating bezel. Scout troops buy them in bulk for map-reading lessons."),
    ("g_pebble", "PEBBLE", "bagged decorative stone for landscaping", "G", 1, "",
     "The bags hold small, water-smoothed river stones about the size of a thumbnail. Customers "
     "spread them in flower beds and along garden paths."),
    ("g_nectar", "NECTAR", "bottled peach, pear, and apricot fruit drinks", "G", 3, "G/D",
     "The drinks are thick, pulpy blends of fruit puree, water, and sugar. Food labeling rules "
     "and competing brands use the same word as the name for this style of drink."),
    ("g_beacon", "BEACON", "personal emergency locator devices for hikers and sailors", "G", 2, "G/D",
     "When the user presses a button, the device transmits a distress signal with GPS "
     "coordinates to search-and-rescue satellites. Outdoor magazines review it alongside other "
     "companies' personal locator beacons."),
    ("g_bridge", "BRIDGE", "custom dental prostheses supplied to dentists", "G", 2, "",
     "A dental lab fabricates fixed replacements for one or more missing teeth that anchor to the "
     "neighboring teeth. Dentists and patients call this kind of fixed prosthesis a bridge."),
    ("g_mint", "MINT", "breath-freshening candies sold in tins", "G", 1, "",
     "The product is small pressed peppermint candies. Convenience stores sell it at the register "
     "beside other companies' mints."),
    ("g_anvil", "ANVIL", "forged steel blocks for blacksmithing and farrier work", "G", 1, "",
     "The company sells 100- to 300-pound forged steel blocks with a horn and a hardy hole, on "
     "which smiths hammer hot metal into shape."),
    ("g_hammock", "HAMMOCK", "hanging rope and fabric beds for backyards", "G", 1, "",
     "The product is a woven cotton bed suspended between two trees or from a steel stand. The "
     "applicant sells it in several colors at garden centers."),
    ("g_sponge", "SPONGE", "cellulose scrubbing pads for washing dishes", "G", 1, "",
     "The soft, porous cellulose blocks soak up water and soap and have a scouring layer on one "
     "side. They are sold in packs of six in the cleaning aisle."),
    ("g_magnet", "MAGNET", "decorative novelty items that stick to refrigerator doors", "G", 1, "",
     "Each piece is a painted resin figure glued to a small magnetic disc. Gift shops sell them "
     "on spinning racks next to postcards."),
    ("g_pillow", "PILLOW", "U-shaped travel neck cushions", "G", 1, "",
     "The foam cushion wraps around the neck to support the head while sitting upright on planes "
     "and trains. Airport shops stock similar cushions from many makers."),
    ("g_cactus", "CACTUS", "potted desert plants sold online", "G", 1, "",
     "The nursery ships spiny, water-storing desert plants such as barrel and prickly pear "
     "species in small clay pots."),
    ("g_ruby", "RUBY", "loose red corundum gemstones sold to jewelers", "G", 2, "G/D",
     "The company imports and cuts red corundum stones and sells them unset to jewelry "
     "manufacturers by the carat."),
    ("g_bamboo", "BAMBOO", "live plants sold for privacy screening", "G", 2, "",
     "The nursery sells fast-growing clumping grasses with woody, hollow stems that reach twenty "
     "feet tall. Homeowners plant them along fences to block the view from neighbors."),
    ("g_granite", "GRANITE", "stone slabs sold to countertop fabricators", "G", 2, "",
     "The quarry cuts slabs of a coarse-grained igneous rock made of quartz and feldspar and "
     "ships them to shops that fabricate kitchen countertops."),
    ("g_citrus", "CITRUS", "fresh oranges, lemons, and limes", "G", 2, "G/D",
     "A grower-packer ships mixed cases of the fruit to grocery chains. The label on each case "
     "shows the grower's county."),
    ("g_umbrella", "UMBRELLA", "personal excess liability insurance policies", "G", 3, "G/S",
     "The policy pays liability claims above the limits of a customer's auto and homeowners "
     "coverage. Insurance agents, regulators, and competitors all refer to this type of coverage "
     "as umbrella insurance."),
    ("g_kombucha", "KOMBUCHA", "bottled fermented tea beverages", "G", 2, "",
     "The applicant was the first company to sell the lightly fizzy fermented tea in its state "
     "and argues that local shoppers learned the word from its labels. Grocery stores now carry "
     "the same kind of drink from a dozen producers."),
    ("g_airfryer", "AIR FRYER", "countertop convection cooking appliances", "G", 2, "G/D",
     "The applicant says it sold the first such appliance under this name in 2010. Today dozens "
     "of manufacturers sell similar hot-air cookers, and cooking magazines review them head to "
     "head."),
    ("g_fromage", "FROMAGE", "soft-ripened cheeses", "G", 3, "G/A",
     "The mark is the French word for cheese. The company sells brie-style and camembert-style "
     "cheeses to U.S. grocery chains."),
    ("g_kidzkloz", "KIDZ KLOZ", "retail store services featuring children's clothing", "G", 3, "G/F",
     "The shop sells shirts, pants, and jackets for kids ages two to twelve. The owner says the "
     "playful spelling makes the name stand out."),
    ("g_skooter", "SKOOTER", "two-wheeled kick scooters for children", "G", 2, "G/F",
     "The name is pronounced exactly like the everyday word for the product. Each scooter has a "
     "standing deck, a handlebar, and two small wheels."),
    ("g_icemelt", "ICE MELT", "granular de-icing pellets for sidewalks and driveways", "G", 3, "G/D",
     "The product is a blend of calcium chloride and magnesium chloride pellets sold in 25-pound "
     "jugs. Hardware stores stock several companies' pellets on a winter shelf with a sign "
     "bearing those same two words."),
    ("g_ebike", "E-BIKE", "bicycles with electric pedal-assist motors", "G", 2, "",
     "The bicycles have a mid-drive motor and a removable battery. Cycling magazines and city "
     "bike-lane rules use the same term for this class of vehicle."),
    ("g_smartring", "SMART RING", "finger rings with sleep and heart-rate sensors", "G", 3, "G/D",
     "The applicant launched its ring in 2019, before most competitors. Several companies now "
     "sell sensor rings, and tech reviewers compare them in roundups under this name."),
    ("g_chai", "CHAI", "spiced black tea concentrate", "G", 2, "",
     "The concentrate is brewed from black tea, cardamom, cinnamon, and ginger and is meant to be "
     "mixed with milk. Coffee shops across the country list the drink on their menus by this "
     "word."),
    ("g_guasha", "GUA SHA", "flat stone facial massage tools", "G", 2, "",
     "The tools are smooth jade or rose-quartz plates used to scrape and massage the face and "
     "neck, a technique rooted in traditional Chinese medicine. Beauty retailers list many "
     "brands' tools under the same term."),
    ("g_rashguard", "RASH GUARD", "long-sleeved stretch swim shirts", "G", 3, "G/D",
     "The tight, quick-drying tops protect surfers from board chafing and sun. Surf shops carry "
     "them from many makers, and customers ask for them by these two words."),
    ("g_trailmix", "TRAIL MIX", "packaged snack blends of nuts, raisins, and chocolate candies", "G", 1, "",
     "The company sells resealable bags of the blend at gas stations and trailheads. Many other "
     "snack makers sell similar blends."),
    ("g_dashcam", "DASH CAM", "cameras that mount on a car windshield and record the road ahead", "G", 2, "",
     "Drivers use the footage after accidents and for insurance claims. Electronics stores sell "
     "dozens of similar cameras, and car-review sites use this term for the whole product type."),
    ("g_weighted", "WEIGHTED BLANKET", "blankets filled with glass beads", "G", 3, "G/D",
     "The blankets weigh 10 to 25 pounds and are marketed to anxious sleepers. The applicant "
     "argues the phrase only mentions a feature, but competing sellers title their listings with "
     "it and sleep studies use it for this whole class of bedding."),
    ("g_bikeshop", "THE BIKE SHOP", "retail store and repair services for bicycles", "G", 1, "",
     "The store sells new bicycles and parts and runs a repair counter. It is one of four bicycle "
     "stores in town."),
    ("g_taxprep", "TAX PREP", "income tax return preparation services", "G", 2, "G/D",
     "The firm prepares individual and small-business returns from a storefront office during "
     "filing season. Its ads show a friendly accountant at a desk."),
    ("g_bubbletea", "BUBBLE TEA", "cafe services featuring sweet tea drinks with chewy tapioca pearls", "G", 1, "",
     "The cafe serves milk teas and fruit teas with tapioca pearls. Several nearby shops sell the "
     "same kind of drink."),
    ("g_cattree", "CAT TREE", "carpeted climbing towers for house cats", "G", 1, "",
     "The towers have sisal-wrapped posts, perches, and a hideaway box. Pet stores stock them "
     "from many makers in the furniture section."),
    ("g_sourdough", "SOURDOUGH", "bread loaves", "G", 2, "G/D",
     "The bakery sells only naturally leavened loaves made with a wild-yeast starter it has kept "
     "since 1998. Other bakeries in town sell the same style of bread."),

    # ---------------- descriptive ----------------
    ("d_marathon", "MARATHON", "lightweight racing shoes", "D", 3, "D/S",
     "The shoe is built for runners competing in 26.2-mile road races, and the product page "
     "lists the big-city races where it has been worn. It has a carbon plate and a thick foam "
     "midsole."),
    ("d_feather", "FEATHER", "bed pillows", "D", 3, "D/G",
     "The pillows are stuffed with duck feathers and a small amount of down, and the label lists "
     "the fill by percentage."),
    ("d_mint", "MINT", "toothpaste", "D", 2, "D/G",
     "The toothpaste is spearmint-flavored, and the tube lists spearmint oil among its "
     "ingredients. Competing toothpastes come in cinnamon, charcoal, and unflavored versions."),
    ("d_ruby", "RUBY", "lipstick", "D", 3, "D/S",
     "The lipstick is sold in a single deep, glossy red shade. Makeup artists and fashion "
     "magazines regularly use the word for that shade of red."),
    ("d_bamboo", "BAMBOO", "bath towels", "D", 2, "",
     "The towels are woven from viscose fiber made from bamboo pulp, and the care label lists "
     "that fiber. Competitors sell cotton, linen, and microfiber towels."),
    ("d_volt", "VOLT", "non-contact electrical testers for electricians", "D", 2, "D/S",
     "The pen-shaped tool lights up and beeps when held near a live wire carrying 12 to 1,000 "
     "volts."),
    ("d_zebra", "ZEBRA", "area rugs", "D", 2, "D/S",
     "The machine-woven polypropylene rugs are printed with bold black-and-white stripes. No "
     "animal hide is used, and the rugs come only in that pattern."),
    ("d_citrus", "CITRUS", "liquid dish soap", "D", 2, "",
     "The soap is scented with lemon and orange oils, and the bottle shows sliced fruit. The "
     "company sells its unscented formula under a different name."),
    ("d_copper", "COPPER", "pots and pans", "D", 2, "",
     "The cookware has solid copper bodies lined with stainless steel, and the listing "
     "highlights how evenly copper conducts heat."),
    ("d_papaya", "PAPAYA", "chewable digestive enzyme tablets", "D", 2, "",
     "Each tablet contains papain, an enzyme extracted from papaya fruit, and the label says "
     "'made from real papaya.'"),
    ("d_snail", "SNAIL", "facial serums", "D", 2, "",
     "The serum's main active ingredient is snail secretion filtrate, a common ingredient in "
     "Korean skincare, listed first on the label after water."),
    ("d_tortoise", "TORTOISE", "eyeglass and sunglass frames", "D", 3, "D/S",
     "Every frame in the line is made of mottled brown-and-amber acetate. Opticians use the word "
     "as the standard name for that frame pattern."),
    ("d_juniper", "JUNIPER", "gin", "D", 2, "D/G",
     "The gin is distilled with juniper berries as its dominant botanical, and the bottle shows "
     "a sprig of the berries."),
    ("d_raven", "RAVEN", "permanent hair dye", "D", 3, "D/S",
     "The dye comes in a single glossy blue-black shade. Hair colorists and fashion writers "
     "routinely use the word as the name of that shade."),
    ("d_steel", "STEEL", "insulated water bottles", "D", 2, "",
     "The double-walled bottles are made entirely of stainless steel, and the marketing stresses "
     "that there is no plastic liner."),
    ("d_quikpatch", "QUIKPATCH", "drywall repair kits", "D", 2, "D/F",
     "The kit contains a self-adhesive mesh patch and fast-setting spackle for fixing small "
     "holes in about ten minutes."),
    ("d_fogless", "FOGLESS", "shower mirrors", "D", 1, "",
     "The mirror has a coating that keeps steam from condensing on it, so it stays clear during "
     "hot showers."),
    ("d_alldaygrip", "ALL-DAY GRIP", "overgrip tape for tennis racquets", "D", 1, "",
     "According to the company's lab tests, the tape stays tacky through long matches in humid "
     "weather."),
    ("d_premier", "PREMIER PLUMBING", "residential plumbing repair services", "D", 2, "D/S",
     "The company fixes leaks, clears drains, and installs water heaters for homeowners. Its ads "
     "promise top-quality work."),
    ("d_bigsur", "BIG SUR", "honey", "D", 2, "D/A",
     "The honey is produced from hives kept along the Big Sur coast of California, and the label "
     "mentions the wildflowers of that region."),
    ("d_rapido", "RAPIDO", "same-day courier services", "D", 3, "D/A",
     "The word means 'fast' in Spanish and Italian, languages spoken by many of the company's "
     "customers. The courier promises delivery within three hours anywhere in the city."),
    ("d_softstep", "SOFT STEP", "cushioned gel shoe insoles", "D", 1, "",
     "The insoles have a gel layer under the heel and forefoot that cushions each step."),
    ("d_fastcharge", "FASTCHARGE", "phone chargers", "D", 1, "",
     "The wall charger supports 65-watt charging and brings a phone from empty to half full in "
     "15 minutes."),
    ("d_nightvision", "NIGHT VISION", "trail cameras for hunters", "D", 2, "D/G",
     "The cameras use infrared LEDs to record clear images of deer and other animals in total "
     "darkness."),
    ("d_leakproof", "LEAKPROOF", "reusable food containers", "D", 1, "",
     "The containers have silicone-gasket lids and four locking tabs so soups and sauces do not "
     "spill in a bag."),
    ("d_fiveminute", "FIVE MINUTE", "two-part epoxy adhesive", "D", 1, "",
     "Once the resin and hardener are mixed, the glue sets in about five minutes."),
    ("d_onecoat", "ONE COAT", "interior wall paint", "D", 1, "",
     "The paint is formulated to cover most previous colors in a single application."),
    ("d_stainguard", "STAINGUARD", "fabric protectant spray", "D", 1, "",
     "The spray leaves a water- and oil-repellent layer on upholstery and carpets so spills bead "
     "up instead of soaking in."),
    ("d_speedylube", "SPEEDY LUBE", "automobile oil change services", "D", 1, "",
     "Drivers can get an oil and filter change in about fifteen minutes without an appointment."),
    ("d_midtowndental", "MIDTOWN DENTAL", "general dentistry services", "D", 2, "D/G",
     "The practice is located in the Midtown district of the city and offers cleanings, "
     "fillings, and crowns."),
    ("d_aquaheat", "AQUAHEAT", "tankless water heaters", "D", 3, "D/F",
     "The founders made up the word by joining 'aqua,' Latin for water, with 'heat.' The unit "
     "heats water on demand as it flows through the pipes."),
    ("d_hydracalm", "HYDRACALM", "after-sun gel", "D", 3, "D/S",
     "The name joins 'hydra,' as in hydrating, with 'calm.' The aloe-based gel is sold to "
     "moisturize and soothe sunburned skin."),
    ("d_kidsafe", "KIDSAFE", "household cleaning sprays", "D", 2, "",
     "The sprays are made without bleach or ammonia, and the label says they are formulated for "
     "homes with young children."),
    ("d_seniormovers", "SENIOR MOVERS", "moving and downsizing services", "D", 2, "D/G",
     "The company packs and relocates older adults moving from family homes into apartments or "
     "assisted-living facilities."),
    ("d_cooltouch", "COOL TOUCH", "bed pillows", "D", 1, "",
     "The pillows have a gel-infused top layer that feels cool against the skin when the sleeper "
     "lies down."),
    ("d_allweather", "ALL-WEATHER", "passenger car tires", "D", 1, "",
     "The tires are rated for rain, snow, and summer heat, and carry the mountain-snowflake "
     "symbol for severe winter conditions."),
    ("d_handsfree", "HANDS-FREE", "car mounts for mobile phones", "D", 1, "",
     "The dashboard mount holds the phone in view so drivers can use navigation and calls "
     "without holding the device."),
    ("d_purespring", "PURE SPRING", "bottled drinking water", "D", 2, "",
     "The water is drawn from a spring in Vermont and filtered, and the label stresses that it "
     "has no additives."),

    # ---------------- suggestive ----------------
    ("s_tundra", "TUNDRA", "chest freezers", "S", 2, "S/A",
     "The freezers are advertised as holding a steady minus 10 degrees Fahrenheit even in a hot "
     "garage. The company is based in Georgia and has no connection to arctic regions."),
    ("s_velvet", "VELVET", "hand and body lotion", "S", 2, "S/D",
     "The lotion contains shea butter and glycerin but no fabric or textile ingredients. Its ads "
     "promise skin that feels soft and smooth after use."),
    ("s_compass", "COMPASS", "career counseling services for recent graduates", "S", 2, "",
     "Counselors meet clients one on one to help them choose a field and plan a job search. No "
     "navigation instruments are involved."),
    ("s_marathon", "MARATHON", "alkaline AA and AAA batteries", "S", 2, "S/A",
     "The batteries are advertised as outlasting leading brands in high-drain devices like game "
     "controllers. They have no connection to running or athletic events."),
    ("s_falcon", "FALCON", "camera drones for filming sports", "S", 2, "",
     "The quadcopters can chase a skier or cyclist at up to 60 miles per hour while filming. "
     "They have no bird-like design."),
    ("s_sahara", "SAHARA", "home dehumidifiers", "S", 2, "S/A",
     "The units pull moisture out of damp basements and collect up to 50 pints of water a day in "
     "a removable tank."),
    ("s_feather", "FEATHER", "backpacking tents", "S", 3, "S/D",
     "The two-person tent weighs under two pounds and is made of coated nylon; it contains no "
     "feathers or down."),
    ("s_bridge", "BRIDGE", "real-time translation earbuds", "S", 2, "",
     "The earbuds let two people who speak different languages hold a conversation by "
     "translating speech as they talk."),
    ("s_anvil", "ANVIL", "spray-on truck bed liners", "S", 2, "",
     "The polyurea coating is sold to pickup owners who haul gravel, tools, and scrap metal and "
     "want a bed that will not dent or scratch."),
    ("s_hammock", "HAMMOCK", "memory-foam mattress toppers", "S", 2, "S/A",
     "The topper is a three-inch foam layer placed on top of a mattress. Ads say it cradles the "
     "sleeper's body so pressure points relax."),
    ("s_sponge", "SPONGE", "bath mats", "S", 3, "S/D",
     "The rigid mat is made of diatomaceous earth and soaks up water from wet feet within "
     "seconds. It is hard as stone and contains no foam."),
    ("s_magnet", "MAGNET", "online job-advertising services for employers", "S", 1, "",
     "Employers post openings and the service promotes them to qualified candidates on social "
     "media. Its tagline promises to pull the best applicants toward your company."),
    ("s_pillow", "PILLOW", "running shoes", "S", 2, "S/D",
     "The shoes have an unusually thick, soft foam midsole aimed at runners who want a plush ride "
     "on long runs."),
    ("s_granite", "GRANITE", "protective phone cases", "S", 2, "",
     "The cases are made of thick rubber and polycarbonate and are tested to survive drops from "
     "twelve feet; no stone is used."),
    ("s_volt", "VOLT", "caffeinated energy drinks", "S", 2, "",
     "Each can has 200 milligrams of caffeine, and ads show drinkers perking up during "
     "late-night study sessions."),
    ("s_snail", "SNAIL", "electric slow cookers", "S", 2, "S/A",
     "The countertop pots cook stews and roasts at low heat over eight to ten hours."),
    ("s_tortoise", "TORTOISE", "lawn fertilizer", "S", 2, "S/A",
     "The granules release nitrogen gradually over about three months instead of all at once."),
    ("s_chameleon", "CHAMELEON", "nail polish", "S", 1, "",
     "The polish shifts from purple to pink as the temperature of the nails changes."),
    ("s_whisper", "WHISPER", "dishwashers", "S", 3, "S/D",
     "The dishwashers run at 38 decibels, which the company says is quieter than a library."),
    ("s_hearth", "HEARTH", "weekly delivery of prepared home-style dinners", "S", 2, "",
     "Customers get chef-cooked stews, casseroles, and pot roasts to reheat. Nothing is cooked "
     "over an open fire."),
    ("s_origami", "ORIGAMI", "folding reading glasses", "S", 2, "S/D",
     "The frames fold along three hinges into a flat case about the size of a credit card."),
    ("s_umbrella", "UMBRELLA", "parental-control software for home networks", "S", 2, "S/A",
     "The app filters websites and blocks adult content on every device connected to the "
     "family's router."),
    ("s_owl", "OWL", "trail cameras for hunters", "S", 2, "S/A",
     "The cameras use infrared LEDs to record clear images of deer and other animals in total "
     "darkness."),
    ("s_cloudwalk", "CLOUDWALK", "cushioned gel shoe insoles", "S", 2, "S/D",
     "The insoles have a gel layer under the heel and forefoot that cushions each step."),
    ("s_cheetah", "CHEETAH", "phone chargers", "S", 2, "",
     "The wall charger supports 65-watt charging and brings a phone from empty to half full in "
     "15 minutes."),
    ("s_armadillo", "ARMADILLO", "fabric protectant spray", "S", 2, "S/A",
     "The spray leaves a water- and oil-repellent layer on upholstery and carpets so spills bead "
     "up instead of soaking in."),
    ("s_submarine", "SUBMARINE", "waterproof pouches for mobile phones", "S", 2, "",
     "The sealed pouch lets swimmers and snorkelers take photos underwater down to about thirty "
     "feet."),
    ("s_hummingbird", "HUMMINGBIRD", "handheld milk frothers", "S", 3, "S/A",
     "The battery-powered wand spins a tiny whisk at high speed and makes a soft buzzing hum "
     "while it froths milk."),
    ("s_homingpigeon", "HOMING PIGEON", "return-shipping logistics services for online retailers", "S", 2, "",
     "The company collects unwanted purchases from shoppers' doorsteps and routes them back to "
     "the retailers' warehouses."),
    ("s_bloodhound", "BLOODHOUND", "skip-tracing services for debt collectors and process servers", "S", 2, "",
     "The company locates people who have moved without leaving a forwarding address by "
     "searching public records and utility data."),
    ("s_lifeboat", "LIFEBOAT", "emergency savings accounts", "S", 2, "",
     "Credit union members set aside money that they can withdraw instantly when an unexpected "
     "bill or a job loss hits."),
    ("s_nightnest", "NIGHTNEST", "sleeping bags", "S", 3, "S/F",
     "The company made up the word from 'night' and 'nest.' The hooded down bag is shaped to "
     "wrap snugly around the sleeper."),
    ("s_snowdrift", "SNOWDRIFT", "down duvets", "S", 3, "S/A",
     "The duvet is bright white, very lofty, and advertised as billowing over the bed."),
    ("s_chipmunk", "CHIPMUNK", "savings app services", "S", 2, "S/A",
     "The app rounds up each card purchase to the next dollar and tucks the spare change away in "
     "a savings account."),
    ("s_firefly", "FIREFLY", "children's night-lights", "S", 2, "",
     "The plug-in light gives off a soft yellow-green glow and dims automatically as the child "
     "falls asleep."),
    ("s_porcupine", "PORCUPINE", "lawn aerator sandals", "S", 2, "",
     "The strap-on sandals have dozens of two-inch metal spikes that punch holes in the soil as "
     "the homeowner walks across the lawn."),
    ("s_beaver", "BEAVER", "wood chippers", "S", 2, "S/A",
     "The gas-powered machines shred branches up to four inches thick into mulch."),
    ("s_octopus", "OCTOPUS", "power strips", "S", 2, "",
     "Each of the eight outlets sits at the end of its own flexible cord, so bulky plugs do not "
     "block one another."),

    # ---------------- arbitrary ----------------
    ("a_tundra", "TUNDRA", "cloud payroll software for small businesses", "A", 1, "",
     "The founders picked the name after a trip to northern Canada. The software calculates "
     "withholding, files payroll taxes, and issues direct deposits."),
    ("a_lantern", "LANTERN", "frozen dumplings", "A", 2, "",
     "The founder named the company after the diner where she first worked as a cook. The "
     "pork-and-chive dumplings are sold in grocery freezer cases."),
    ("a_velvet", "VELVET", "road-salt spreaders for municipal trucks", "A", 1, "",
     "The spreaders are steel hoppers with a spinning disc that throws rock salt across icy "
     "roads. They are sold to city public-works departments."),
    ("a_compass", "COMPASS", "canned tomatoes and tomato paste", "A", 1, "",
     "The cannery has used the name since it opened in 1987. Labels show a ripe tomato on a "
     "plain white background."),
    ("a_pebble", "PEBBLE", "pet health insurance", "A", 2, "A/S",
     "The insurer covers veterinary bills for dogs and cats. The name comes from the founder's "
     "first cat, which customers learn about only if they read the company history page."),
    ("a_nectar", "NECTAR", "bicycle tires", "A", 1, "",
     "The company makes tubeless road and gravel tires in Taiwan and sells them through bike "
     "shops."),
    ("a_beacon", "BEACON", "all-purpose and bread flour", "A", 1, "",
     "The mill grinds wheat grown in Kansas and sells five-pound bags to grocery stores. The "
     "bags show the mill's grain elevator."),
    ("a_marathon", "MARATHON", "canned soups and broths", "A", 1, "",
     "The soups include chicken noodle, minestrone, and split pea. The company does not sponsor "
     "sporting events or market to athletes."),
    ("a_falcon", "FALCON", "tile grout and grout sealer", "A", 1, "",
     "Contractors use the sanded grout to fill joints between floor tiles; it comes in twelve "
     "colors."),
    ("a_sahara", "SAHARA", "piano tuning and repair services", "A", 2, "A/S",
     "A two-person shop tunes and regulates upright and grand pianos in customers' homes."),
    ("a_bridge", "BRIDGE", "scented soy candles", "A", 1, "",
     "The candles come in fig, cedar, and sea-salt scents and are poured by hand in Portland."),
    ("a_anvil", "ANVIL", "women's perfume", "A", 2, "A/S",
     "The floral fragrance has notes of jasmine and pear and is sold in department stores."),
    ("a_hammock", "HAMMOCK", "tire-pressure gauges", "A", 1, "",
     "The digital gauges read tire pressure in PSI and bar and are sold at auto-parts stores."),
    ("a_magnet", "MAGNET", "bottled roasted barley tea", "A", 1, "",
     "The unsweetened tea is brewed from roasted barley and sold chilled in convenience stores."),
    ("a_cactus", "CACTUS", "wedding dresses", "A", 1, "",
     "The bridal boutique designs and sells lace and satin gowns and does not use desert or "
     "Southwestern themes."),
    ("a_ruby", "RUBY", "brass plumbing fittings", "A", 1, "",
     "The valves and couplings are unpainted brass and are sold to plumbing contractors."),
    ("a_bamboo", "BAMBOO", "guitar strings", "A", 2, "",
     "The strings contain no plant fiber; they are made of nickel-wound steel and nylon."),
    ("a_granite", "GRANITE", "shampoo and conditioner", "A", 1, "",
     "The shampoo is a lightly scented formula for everyday use and contains no stone-derived "
     "ingredients."),
    ("a_volt", "VOLT", "wool knitting yarn", "A", 1, "",
     "The yarn is spun from undyed merino wool and sold in skeins to hand knitters."),
    ("a_zebra", "ZEBRA", "tax preparation services", "A", 1, "",
     "The firm prepares individual income tax returns. Its logo is a plain blue circle."),
    ("a_citrus", "CITRUS", "accounting software for small businesses", "A", 2, "A/S",
     "The software tracks invoices, expenses, and bank reconciliations. The founders liked that "
     "the word sounded fresh."),
    ("a_copper", "COPPER", "children's picture books", "A", 1, "",
     "The publisher releases about twenty illustrated books a year for readers ages three to "
     "seven."),
    ("a_papaya", "PAPAYA", "project-management software", "A", 1, "",
     "Teams use the software to assign tasks, set deadlines, and track progress on shared "
     "boards."),
    ("a_juniper", "JUNIPER", "dog-walking and pet-sitting services", "A", 1, "",
     "Walkers take dogs on hour-long neighborhood walks and visit cats while owners travel."),
    ("a_raven", "RAVEN", "hearing aids", "A", 1, "",
     "The devices sit behind the ear and amplify speech; they come in beige, silver, and gray."),
    ("a_steel", "STEEL", "loose-leaf herbal teas", "A", 1, "",
     "The blends include chamomile, peppermint, and rooibos and are sold in paper pouches."),
    ("a_chameleon", "CHAMELEON", "frozen pizza", "A", 1, "",
     "The pizzas come in pepperoni, margherita, and four-cheese varieties and are sold in "
     "grocery freezers."),
    ("a_whisper", "WHISPER", "canned chickpeas", "A", 1, "",
     "The chickpeas are cooked and packed in salted water in 15-ounce cans."),
    ("a_hearth", "HEARTH", "swim goggles", "A", 1, "",
     "The anti-fog goggles are made for competitive pool swimmers."),
    ("a_origami", "ORIGAMI", "dry dog food", "A", 1, "",
     "The kibble is made with lamb and brown rice and sold in 30-pound bags."),
    ("a_umbrella", "UMBRELLA", "canned sardines", "A", 1, "",
     "The sardines are packed in olive oil in Portugal and sold in flat tins."),
    ("a_quincunx", "QUINCUNX", "wool socks", "A", 3, "A/F",
     "The word is an old English term for an arrangement of five points like the five on a die. "
     "The socks are plain-knit and solid-colored."),
    ("a_snickersnee", "SNICKERSNEE", "cough drops", "A", 3, "A/F",
     "The word is an archaic English term for a large knife used in fighting. The lozenges are "
     "honey-lemon flavored."),
    ("a_pynekone", "PYNEKONE", "home alarm systems", "A", 3, "A/F",
     "The name is pronounced exactly like the word for the seed cone of a pine tree. The system "
     "includes door sensors, a siren, and a keypad."),
    ("a_antarctica", "ANTARCTICA", "fresh bananas", "A", 3, "A/D",
     "The bananas are grown in Ecuador and Costa Rica and sold ripe to grocery chains. No one "
     "grows bananas on the frozen continent the name refers to."),
    ("a_okapi", "OKAPI", "ballpoint pens", "A", 3, "A/F",
     "An okapi is a rare forest animal of central Africa related to the giraffe. The pens are "
     "refillable and made of brushed aluminum."),
    ("a_tarn", "TARN", "leather wallets", "A", 3, "A/F",
     "The word refers to a small mountain lake formed by a glacier. The wallets are bifold and "
     "made of vegetable-tanned leather."),
    ("a_mariposa", "MARIPOSA", "snow chains for car tires", "A", 3, "A/F",
     "The word means 'butterfly' in Spanish. The chains are steel-link sets that strap onto "
     "tires for driving on icy roads."),

    # ---------------- fanciful ----------------
    ("f_zorvanta", "ZORVANTA", "chewable antacid tablets", "F", 1, "",
     "Translation statement: the wording ZORVANTA has no meaning in a foreign language. The "
     "tablets use calcium carbonate to relieve heartburn."),
    ("f_quelmira", "QUELMIRA", "sit-on-top fishing kayaks", "F", 1, "",
     "A naming agency assembled the word from random syllables and confirmed it has no meaning "
     "in any major language."),
    ("f_vaskello", "VASKELLO", "home espresso machines", "F", 2, "F/A",
     "The machine has a 15-bar pump and a steam wand. The brand team wanted a name that sounds "
     "Italian, but it is not a word in Italian or any other language."),
    ("f_trunoviq", "TRUNOVIQ", "mesh Wi-Fi routers", "F", 1, "",
     "The three-unit system covers a house with a single wireless network. The name was produced "
     "by software that combines syllables at random."),
    ("f_brelloque", "BRELLOQUE", "hair clips and barrettes", "F", 2, "F/A",
     "The name looks French, but French dictionaries do not list it and it has no meaning. The "
     "clips are acetate claw clips in several solid colors."),
    ("f_plivex", "PLIVEX", "bathroom tile cleaner", "F", 1, "",
     "The foaming spray removes soap scum and mildew from shower tiles."),
    ("f_korrendel", "KORRENDEL", "interior wall paint", "F", 1, "",
     "The paint company chose the name because the founder liked how it sounded when said "
     "aloud."),
    ("f_zinthara", "ZINTHARA", "sparkling wine", "F", 1, "",
     "The winery produces a dry sparkling white wine from chardonnay grapes. Its labels show the "
     "name in gold script."),
    ("f_dravello", "DRAVELLO", "rain boots", "F", 2, "F/A",
     "The rubber boots are knee-high and come in six colors. The name is not a place, a surname, "
     "or a word in any language the applicant's search turned up."),
    ("f_ulvareth", "ULVARETH", "merino hiking socks", "F", 1, "",
     "The socks have cushioned soles and reinforced heels. The founders built the name by "
     "rearranging letters drawn from a hat."),
    ("f_ozmirell", "OZMIRELL", "laundry detergent", "F", 1, "",
     "The detergent comes in liquid and pod forms and is sold in supermarkets."),
    ("f_fenniquo", "FENNIQUO", "board games", "F", 1, "",
     "The publisher's first game is a tile-placement strategy game for two to four players."),
    ("f_talvorin", "TALVORIN", "cough syrup", "F", 1, "",
     "Translation statement: the wording TALVORIN has no meaning in a foreign language. The "
     "syrup contains dextromethorphan and honey."),
    ("f_kiveldra", "KIVELDRA", "frozen lasagna", "F", 1, "",
     "The lasagna is made with beef ragu and ricotta and sold in family-size trays."),
    ("f_norbaz", "NORBAZ", "cordless drills", "F", 2, "F/S",
     "The 20-volt drills come with two batteries and a charger. The founders say the name sounds "
     "tough and memorable."),
    ("f_melvaniq", "MELVANIQ", "cloud file-storage services", "F", 1, "",
     "Businesses use the service to store and share documents online."),
    ("f_troskella", "TROSKELLA", "ceramic dinnerware", "F", 1, "",
     "The stoneware plates and bowls are glazed in muted earth tones."),
    ("f_bakundro", "BAKUNDRO", "motor scooters", "F", 1, "",
     "The 50cc scooters are sold to city commuters. A trademark search found no dictionary entry "
     "for the word in any language."),
    ("f_lorquin", "LORQUIN", "wristwatches", "F", 1, "",
     "The watches have automatic movements and sapphire crystals and are sold through jewelers."),
    ("f_desmolay", "DESMOLAY", "sunscreen", "F", 1, "",
     "The mineral sunscreen is SPF 50 and water resistant for 80 minutes."),
    ("f_virendel", "VIRENDEL", "veterinary clinic services", "F", 1, "",
     "The clinic offers vaccinations, dental care, and surgery for dogs and cats. The owners made "
     "up the name so no other clinic would have it."),
    ("f_hovrandi", "HOVRANDI", "snowboards", "F", 1, "",
     "The boards have a poplar core and come in freestyle and all-mountain shapes."),
    ("f_eskavor", "ESKAVOR", "sewing machines", "F", 1, "",
     "The computerized machines have 200 built-in stitches. The word does not appear in any "
     "dictionary."),
    ("f_telquora", "TELQUORA", "yoga studio services", "F", 1, "",
     "The studio offers vinyasa and restorative classes in a converted warehouse."),
    ("f_ruxalene", "RUXALENE", "floor wax", "F", 2, "F/S",
     "The liquid wax is applied with a mop and buffs to a high shine on vinyl floors. The ending "
     "was chosen to sound like a chemical, but the word itself means nothing."),
    ("f_kwendari", "KWENDARI", "roasted coffee beans", "F", 3, "F/D",
     "Although it sounds like a coffee-growing region, it is not the name of any place, farm, or "
     "language; the beans come from Colombia and Ethiopia."),
    ("f_izeldro", "IZELDRO", "dental floss", "F", 1, "",
     "The waxed floss comes in a flavored and an unflavored version."),
    ("f_vornisk", "VORNISK", "hockey sticks", "F", 1, "",
     "The composite sticks are sold to youth and adult players."),
    ("f_tamvrique", "TAMVRIQUE", "clumping cat litter", "F", 1, "",
     "The clay litter is unscented and low-dust."),
    ("f_oskelvan", "OSKELVAN", "electric kettles", "F", 1, "",
     "The gooseneck kettles have variable temperature control for pour-over coffee and tea."),
    ("f_blixovar", "BLIXOVAR", "bicycle helmets", "F", 1, "",
     "The helmets have rotational-impact liners and built-in rear lights. The founders picked the "
     "sounds they liked best from a list of made-up words."),
    ("f_dunmarel", "DUNMAREL", "canned cat food", "F", 2, "F/D",
     "The pate-style food comes in salmon and chicken flavors. The name is not a town, an estate, "
     "or a family name."),
    ("f_yorveska", "YORVESKA", "vodka", "F", 2, "F/A",
     "The vodka is distilled from wheat in Idaho. The Slavic-sounding name has no meaning in "
     "Russian, Polish, or any other language."),
    ("f_zelquari", "ZELQUARI", "gardening gloves", "F", 1, "",
     "The nitrile-coated gloves are sold at garden centers."),
    ("f_hevrando", "HEVRANDO", "insurance brokerage services", "F", 1, "",
     "The brokerage places commercial property and liability coverage for small manufacturers."),
    ("f_anlivo", "ANLIVO", "baby strollers", "F", 2, "F/A",
     "The name blends the first syllables of the founders' children, Ana, Liv, and Otto, into a "
     "word that has no meaning of its own."),
    ("f_quorbel_shoes", "QUORBEL", "running shoes", "F", 1, "",
     "The shoes have a knit upper and a responsive foam midsole."),
    ("f_quorbel_sauce", "QUORBEL", "jarred pasta sauces", "F", 1, "",
     "The sauces come in marinara, arrabbiata, and vodka varieties."),
]

# Cross-mark minimal pairs that share one context: grouped together.
PAIR_GROUPS = {
    "d_fastcharge": "pair_charger", "s_cheetah": "pair_charger",
    "d_stainguard": "pair_protectant", "s_armadillo": "pair_protectant",
    "d_softstep": "pair_insole", "s_cloudwalk": "pair_insole",
    "d_nightvision": "pair_trailcam", "s_owl": "pair_trailcam",
}

# yes/no probes on item states: (item key, level asked)
NOUL = [
    ("g_icemelt", G), ("g_umbrella", G), ("g_fromage", G),
    ("g_rashguard", D), ("g_nectar", D), ("g_kidzkloz", F),
    ("d_raven", D), ("d_aquaheat", D), ("d_rapido", D),
    ("d_marathon", S), ("d_tortoise", S), ("d_midtowndental", G),
    ("s_whisper", S), ("s_sponge", S), ("s_hummingbird", S),
    ("s_feather", D), ("s_snowdrift", A), ("s_nightnest", F),
    ("a_quincunx", A), ("a_antarctica", A), ("a_pebble", A),
    ("a_mariposa", F), ("a_anvil", S), ("a_citrus", S),
    ("f_kwendari", F), ("f_vaskello", F), ("f_norbaz", F),
    ("f_anlivo", A), ("f_ruxalene", S), ("f_yorveska", A),
]

TEMPLATES = [
    "Mark: {m}\nGoods/services: {g}\nContext: {c}",
    "Proposed trademark: {m}\nUsed for: {g}\n{c}",
    "Trademark application summary\nMark (standard characters): {m}\n"
    "Identification of goods/services: {g}\nApplicant's notes: {c}",
    "Brand name under review: {m}\nProduct or service: {g}\nBackground: {c}",
    "Client intake memo\nName the client wants to protect: {m}\nWhat it is used on: {g}\nFacts: {c}",
    "Clearance request\nMark: \"{m}\"\nOffered for: {g}\nNotes from the client: {c}",
]

CHOICE_Q = [
    "Where does the mark fall on the distinctiveness spectrum?",
    "Using the definitions provided, how distinctive is this mark for the stated goods or services?",
    "Which category of trademark distinctiveness fits this mark as used here?",
    "Classify the mark on the Abercrombie spectrum of distinctiveness.",
    "An examiner has to place this mark on the distinctiveness spectrum. Which category applies?",
    "For these goods or services, which distinctiveness category does the mark belong to?",
    "How should the mark be classified under the standard trademark distinctiveness categories?",
    "Rate the inherent distinctiveness of this mark for the listed goods or services.",
]

NOUL_Q = [
    "Is the mark {L} as used for these goods or services?",
    "Would this mark be classified as {L} on the distinctiveness spectrum?",
    "Does the mark belong in the {L} category of trademark distinctiveness?",
    "Is {L} the right distinctiveness category for this mark?",
]

LEAK = re.compile(r"generic|descripti|describ|suggest|arbitrar|fanci|distinctive", re.I)


def h(s):
    return int(hashlib.md5(f"{SEED}:{s}".encode()).hexdigest(), 16)


ITEM_OF = {}


def cid(instr, state, options):
    x = hashlib.sha1(json.dumps([instr, state, options], ensure_ascii=False).encode()).hexdigest()
    return "c_" + x[:12]


def card_text(order):
    return "\n".join(f"- {o}: {DEFS[o]}" for o in order)


def neutral_id(key, mark):
    # item id without the gold-coded key prefix, so blind rows do not leak the label
    return re.sub(r"[^a-z0-9]+", "", mark.lower()) + f"_{h('id' + key) % 65536:04x}"


def build():
    keys = [it[0] for it in ITEMS]
    assert len(keys) == len(set(keys)), "duplicate keys"
    mark_count = Counter(it[1] for it in ITEMS)
    items = list(ITEMS)
    random.Random(SEED).shuffle(items)
    rows, n, by_key = [], 0, {}
    for i, (key, mark, goods, code, diff, btag, ctx) in enumerate(items):
        gold = CODE[code]
        if mark_count[mark] > 1:
            fam = mark.lower().replace(" ", "_")
        else:
            fam = PAIR_GROUPS.get(key)
        iid = neutral_id(key, mark)
        gid = f"g:{SRC}:{fam or iid}"
        state = TEMPLATES[h("t" + key) % len(TEMPLATES)].format(m=mark, g=goods, c=ctx)
        order = SCALE[::-1] if h("o" + key) % 3 == 0 else list(SCALE)
        instr = CHOICE_Q[h("q" + key) % len(CHOICE_Q)]
        n += 1
        meta = {"domain": DOMAIN, "difficulty": diff, "boundary": bool(btag), "item": iid}
        if fam:
            meta["family"] = fam
        row = {
            "id": f"r_{SRC}_{n}", "group_id": gid, "call_id": cid(instr, state, order),
            "split": "train", "track": "STD", "source": SRC, "state": state,
            "qtype": "choice", "instructions": instr, "options": order, "gold": gold,
            "role": "choice", "card": card_text(order), "meta": meta,
        }
        rows.append(row)
        by_key[key] = row
        ITEM_OF[iid] = (key, mark, goods, code, diff, btag, ctx)
    for j, (key, lvl) in enumerate(NOUL):
        base = by_key[key]
        instr = NOUL_Q[j % len(NOUL_Q)].format(L=lvl)
        n += 1
        meta = {k: v for k, v in base["meta"].items()}
        meta["base_id"] = base["id"]
        rows.append({
            "id": f"r_{SRC}_{n}", "group_id": base["group_id"],
            "call_id": cid(instr, base["state"], None),
            "split": "train", "track": "STD", "source": SRC, "state": base["state"],
            "qtype": "noul", "instructions": instr, "options": None,
            "gold": 1 if base["gold"] == lvl else 0, "role": "aff",
            "card": card_text(SCALE), "meta": meta,
        })
    return rows


def validate(rows):
    errs = []
    need = {"id", "group_id", "call_id", "split", "track", "source", "state", "qtype",
            "instructions", "options", "gold", "role", "card", "meta"}
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        errs.append("duplicate ids")
    text2cid = {}
    for r in rows:
        k = json.dumps([r["instructions"], r["state"], r["options"]], ensure_ascii=False)
        if k in text2cid:
            errs.append(f"{r['id']}: duplicate text")
        text2cid[k] = r["call_id"]
    if len(set(text2cid.values())) != len(text2cid):
        errs.append("call_id collision")
    item_of = ITEM_OF
    for r in rows:
        rid = r["id"]
        if set(r) != need:
            errs.append(f"{rid}: keys {sorted(set(r) ^ need)}")
        if r["split"] != "train" or r["track"] != "STD" or r["source"] != SRC:
            errs.append(f"{rid}: split/track/source")
        if not re.fullmatch(rf"r_{SRC}_\d+", rid):
            errs.append(f"{rid}: id format")
        it = item_of[r["meta"]["item"]]
        if it[1] not in r["state"]:
            errs.append(f"{rid}: mark missing from state")
        if LEAK.search(r["state"]):
            errs.append(f"{rid}: label word in state: {LEAK.search(r['state']).group(0)}")
        nsent = len(re.findall(r"[.!?](?:'|\")?(?:\s|$)", it[6]))
        if not 1 <= nsent <= 3:
            errs.append(f"{rid}: context sentences {nsent}")
        lines = r["card"].split("\n")
        if any(not ln.startswith("- ") or ": " not in ln for ln in lines):
            errs.append(f"{rid}: card format")
        names = [ln[2:].split(": ", 1)[0] for ln in lines]
        if r["qtype"] == "choice":
            if LEAK.search(r["instructions"]) and "distinctive" not in r["instructions"].lower():
                errs.append(f"{rid}: label word in instructions")
            if any(x in r["instructions"].lower() for x in SCALE):
                errs.append(f"{rid}: label in choice instructions")
            if r["role"] != "choice" or r["gold"] not in r["options"]:
                errs.append(f"{rid}: choice fields")
            if sorted(r["options"]) != sorted(SCALE) or r["options"] not in (SCALE, SCALE[::-1]):
                errs.append(f"{rid}: options")
            if names != r["options"]:
                errs.append(f"{rid}: card/options mismatch")
            if r["gold"] != CODE[it[3]]:
                errs.append(f"{rid}: gold mismatch")
        else:
            if r["options"] is not None or r["gold"] not in (0, 1) or isinstance(r["gold"], bool):
                errs.append(f"{rid}: noul fields")
            if r["role"] != "aff" or names != SCALE:
                errs.append(f"{rid}: noul role/card")
    ch = [r for r in rows if r["qtype"] == "choice"]
    bal = Counter(r["gold"] for r in ch)
    if max(bal.values()) - min(bal.values()) > 2 or set(bal) != set(SCALE):
        errs.append(f"gold imbalance {bal}")
    pos = Counter(r["options"].index(r["gold"]) for r in ch)
    if pos.most_common(1)[0][1] / len(ch) > 0.30:
        errs.append(f"gold position skew {pos}")
    if len({r["instructions"] for r in ch}) < 6:
        errs.append("fewer than 6 choice phrasings")
    nl = [r for r in rows if r["qtype"] == "noul"]
    if nl and not 0.4 <= sum(r["gold"] for r in nl) / len(nl) <= 0.6:
        errs.append("noul yes share")
    # twins: same mark, different goods, same group; golds should differ within a family
    fams = {}
    for r in ch:
        if "family" in r["meta"] and not r["meta"]["family"].startswith("pair_"):
            fams.setdefault(r["meta"]["family"], []).append(r)
    for f, rs in fams.items():
        if len({x["group_id"] for x in rs}) != 1:
            errs.append(f"family {f}: group split")
    # group_id must not be shared across unrelated items
    g2items = {}
    for r in ch:
        g2items.setdefault(r["group_id"], set()).add(r["meta"].get("family") or r["meta"]["item"])
    for g, s in g2items.items():
        if len(s) != 1:
            errs.append(f"group {g} mixes {s}")
    return errs


def report(rows):
    ch = [r for r in rows if r["qtype"] == "choice"]
    nl = [r for r in rows if r["qtype"] == "noul"]
    fams = Counter(r["meta"]["family"] for r in ch
                   if "family" in r["meta"] and not r["meta"]["family"].startswith("pair_"))
    btags = Counter(it[5] for it in ITEMS if it[5])
    return {
        "rows": len(rows), "choice": len(ch), "noul": len(nl),
        "gold": dict(Counter(r["gold"] for r in ch)),
        "gold_position": dict(sorted(Counter(r["options"].index(r["gold"]) for r in ch).items())),
        "reversed_order": sum(r["options"][0] == F for r in ch),
        "noul_yes": sum(r["gold"] for r in nl),
        "difficulty": dict(sorted(Counter(r["meta"]["difficulty"] for r in ch).items())),
        "boundary_items": sum(r["meta"]["boundary"] for r in ch),
        "boundary_tags": dict(btags.most_common()),
        "twin_families": len(fams), "twin_rows": sum(fams.values()),
        "groups": len({r["group_id"] for r in rows}),
        "choice_phrasings": len({r["instructions"] for r in ch}),
        "noul_phrasings": len({r["instructions"] for r in nl}),
        "templates_used": len({r["state"].split("\n")[0].split(":")[0] for r in ch}),
    }


def main():
    rows = build()
    errs = validate(rows)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print("  ", e)
        sys.exit(1)
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{DOMAIN}.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(OUT / f"{DOMAIN}.blind.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k != "gold"}, ensure_ascii=False) + "\n")
    print(json.dumps(report(rows), indent=1))


if __name__ == "__main__":
    main()
