"""Claude-written label tables, definitions and keyword cues for build_msha_injury.py (MSHA Part 50 accident data).

Each task maps the MSHA code -> (option text, definition, cue regex or None). A cue of None means the label is shown
only as a distractor (never gold), because its narratives cannot be checked reliably from the text. Cues are a
consistency guard (the human-coded label must be the ONLY label whose cue fires); they never create labels.
All regexes run on the upper-cased narrative.
"""

POSS = r"(?:HIS|HER|THEIR|LEFT|RIGHT|LT|RT|L|R|BOTH|EE S|EES|EMPLOYEE S|EMPLOYEES|MINER S|VICTIM S|INJURED S|IP S|THE)"
INJ = (r"(?:INJUR\w*|LAC\w*|STRAIN\w*|SPRAIN\w*|FRACTUR\w*|PAIN|CUT|CONTUSION\w*|BRUIS\w*|WOUND\w*|ABRASION\w*|"
       r"AMPUTAT\w*|CRUSH\w*|BURN\w*|SWELL\w*|SORE\w*|BROKE\w*)")


def ctx(part):
    """part mentioned as a body part: possessive/side before it, or an injury word right after it."""
    return rf"\b{POSS}\s+(?:\w+\s+){{0,2}}{part}\b|\b{part}\s+{INJ}\b|\b(?:TO|ON|IN) (?:THE |HIS |HER )?{part}\b"


# ---------------------------------------------------------------------------------------------------------------
BODY = {
    "100": ("head (not elsewhere classified)",
            "The head in general, when the narrative only says 'head' and names no more specific part (scalp, "
            "skull, brain, ear, eye or face part).", ctx(r"HEAD")),
    "110": ("brain", "The brain itself, such as a concussion or other brain injury named as such.", None),
    "120": ("ears, internal and external", "Both the inner or middle ear (or hearing) and the outer ear.", None),
    "121": ("ear, external", "The outer ear only (auricle or earlobe), for example a cut, bruise or burn on the ear.",
            r"\bEARS?\b(?=.*\b(CUT|LAC\w*|STITCH\w*|SUTUR\w*|BRUIS\w*|BURN\w*|LOBE|TORN|SCRATCH\w*)\b)"),
    "122": ("ear, internal, or hearing",
            "The inner or middle ear, eardrum or ear canal, or hearing itself (for example hearing loss or "
            "something lodged in the ear canal).",
            r"\bHEARING\b|\bEAR ?DRUMS?\b|\bEAR CANAL\b|\bTINNITUS\b|\bRINGING IN (HIS |HER )?EARS?\b"),
    "130": ("eye(s)", "One or both eyes, including the eyeball, cornea, optic nerve and vision.",
            r"\b(?:" + POSS + r"\s+(?:\w+\s+){0,2})EYES?\b(?! ?BOLT| OF THE| HOOK| LET)|\bCORNEA\w*|\bIN (HIS|HER|THE) EYES?\b"),
    "140": ("face (not elsewhere classified)",
            "A face part with no code of its own (cheek, forehead, eyebrow, temple) or the face in general; not the "
            "eyes, ears, nose, mouth or jaw.", None),
    "141": ("jaw or chin", "The jaw (mandible) or chin.", r"\bJAW\b|\bCHIN\b"),
    "142": ("mouth, lips, teeth, tongue or throat", "The mouth, lips, teeth, tongue, throat or sense of taste.",
            r"\bMOUTH\b|\bLIPS?\b|\bTEETH\b|\bTOOTH\b|\bTONGUE\b|\bTHROAT\b"),
    "143": ("nose, nasal passages or sinuses", "The nose, nasal passages, sinuses or sense of smell.",
            r"\bNOSE\b|\bNASAL\b|\bSINUS\w*"),
    "144": ("face, multiple parts", "Two or more different face parts (for example nose and mouth, or eye and cheek).",
            None),
    "150": ("scalp", "The skin and tissue covering the skull, named as the scalp.", r"\bSCALP\b"),
    "160": ("skull", "The bones of the skull (cranium), for example a skull fracture.", None),
    "170": ("head, multiple parts", "Two or more different parts of the head (for example scalp and face).", None),
    "200": ("neck", "The neck, including the cervical spine and neck muscles, but not the throat.",
            r"\bNECK\b|\bCERVICAL\b"),
    "310": ("arm (not elsewhere classified)",
            "The arm when the narrative does not say which part of it (upper arm, elbow or forearm) was hurt.",
            ctx(r"ARMS?")),
    "311": ("upper arm (humerus)", "The arm between the shoulder and the elbow, including the humerus, biceps and triceps.",
            r"\bUPPER ARMS?\b|\bHUMERUS\b|\bBICEPS?\b|\bTRICEPS?\b"),
    "312": ("elbow", "The elbow joint.", r"\bELBOWS?\b"),
    "313": ("forearm (ulna, radius)", "The arm between the elbow and the wrist, including the ulna and radius.",
            r"\bFORE ?ARMS?\b|\bULNA\b|\bRADIUS\b"),
    "314": ("arm, multiple parts", "Two or more different parts of the same arm (for example forearm and elbow).", None),
    "320": ("wrist", "The wrist joint.", r"\bWRISTS?\b"),
    "330": ("hand (not wrist or fingers)",
            "The hand itself (palm or back of the hand), not the wrist, fingers or thumb.",
            ctx(r"HANDS?") + r"|\bPALM\b"),
    "340": ("finger(s) or thumb", "One or more fingers or the thumb, including fingertips and fingernails.",
            r"\bFINGERS?\b|\bTHUMBS?\b|\bFINGER ?TIPS?\b|\bPINKY\b|\bFINGER ?NAILS?\b"),
    "350": ("upper extremities, multiple parts", "Parts of both arms or hands, or several different arm and hand parts.",
            None),
    "410": ("abdomen or internal organs", "The abdomen, stomach area or internal abdominal organs.", None),
    "420": ("back (muscles, spine, spinal cord, tailbone)",
            "The back, including back muscles, the thoracic and lumbar spine, spinal cord and tailbone; not the neck.",
            r"\b(?:LOWER|UPPER|MID|MIDDLE|LOW|HIS|HER|INJURED|STRAINED|HURT|WRENCHED|TWISTED) BACK\b(?! (OF|TO|INTO|ON|UP|DOWN|OUT|IN|OVER|AGAINST|FROM|AND FORTH))|\bBACK (INJURY|PAIN|STRAIN|MUSCLES?|SPASMS?)\b|\bSPINE\b|\bLUMBAR\b|\bTAILBONE\b|\bCOCCYX\b"),
    "430": ("chest (ribs, breastbone, chest organs)", "The chest, including the ribs, breastbone and chest organs.",
            r"\bCHEST\b|\bRIBS?\b|\bSTERNUM\b|\bBREAST ?BONE\b"),
    "440": ("hips (pelvis, pelvic organs, kidneys, buttocks)",
            "The hips, including the pelvis, pelvic organs, kidneys and buttocks.",
            r"\bHIPS?\b|\bPELVI\w*|\bBUTTOCKS?\b|\bKIDNEYS?\b"),
    "450": ("shoulder (collarbone, shoulder blade)",
            "The shoulder, including the collarbone (clavicle), shoulder blade (scapula) and rotator cuff.",
            ctx(r"SHOULDERS?") + r"|\bCLAVICLE\b|\bCOLLAR ?BONE\b|\bSCAPULA\b|\bROTATOR CUFF\b"),
    "460": ("trunk, multiple parts", "Two or more parts of the trunk (for example back and chest).", None),
    "510": ("leg (not elsewhere classified)",
            "The leg when the narrative does not say which part of it (thigh, knee or lower leg) was hurt.",
            ctx(r"LEGS?")),
    "511": ("thigh (femur)", "The thigh, including the femur and hamstring.", r"\bTHIGHS?\b|\bFEMUR\b|\bHAMSTRING\b"),
    "512": ("knee (kneecap)", "The knee, including the kneecap (patella) and meniscus.",
            r"\bKNEES?\b|\bPATELLA\b|\bKNEE ?CAP\b|\bMENISCUS\b"),
    "513": ("lower leg (shin, calf, tibia, fibula)", "The leg between the knee and the ankle: shin, calf, tibia, fibula.",
            r"\bLOWER LEGS?\b|\bSHINS?\b|\bCALF\b|\bTIBIA\b|\bFIBULA\b"),
    "514": ("leg, multiple parts", "Two or more different parts of the same leg (for example knee and thigh).", None),
    "520": ("ankle", "The ankle joint.", r"\bANKLES?\b"),
    "530": ("foot (not ankle or toes)", "The foot itself (heel, arch, instep, metatarsals), not the ankle or toes.",
            ctx(r"(?:FOOT|FEET)") + r"|\bHEEL\b(?! OF)|\bINSTEP\b|\bMETATARSAL\w*"),
    "540": ("toe(s)", "One or more toes.", r"\bTOES?\b(?! ?(BOARD|CAP|PLATE))"),
    "550": ("lower extremities, multiple parts", "Parts of both legs or feet, or several different leg and foot parts.",
            None),
    "600": ("body systems", "A whole body system rather than one part (for example poisoning, heat illness or a heart "
            "attack).", None),
    "700": ("multiple body parts (more than one major part)",
            "Two or more major body regions (for example head and leg, or arm and back).", None),
}
# words that make the body-part question unclear (several parts, whole body, systemic illness, brain/skull/face)
BODY_BLOCK = (r"\bMULTIPLE\b|\bSEVERAL\b|\bVARIOUS\b|\bALL OVER\b|\bWHOLE BODY\b|\bENTIRE BODY\b|\bBOTH\b|\bBILATERAL|"
              r"\bB L\b|\bSKULL\b|\bBRAIN\b|\bCONCUSS\w*|\bFACE\b|\bFACIAL\b|\bCHEEK\b|\bFOREHEAD\b|\bEYEBROW\b|"
              r"\bTEMPLE\b|\bABDOM\w*|\bSTOMACH\b|\bGROIN\b|\bTORSO\b|\bTRUNK\b|\bHEART\b|\bCARDIAC\b|\bPOISON\w*|"
              r"\bHEAT (STROKE|EXHAUSTION)|\bUNCONSCIOUS|\bPASSED OUT|\bSEIZURE|\bDIZZ\w*|\bNAUSEA|\bFATAL|\bDIED\b|"
              r"\bDEATH\b|\bKILLED\b|\bKNUCKLE|\bINNER EAR|\bHEARING PROTECTION")

# ---------------------------------------------------------------------------------------------------------------
_PART = (r"(BONES?|FINGERS?|TOES?|ARMS?|LEGS?|WRISTS?|ANKLES?|RIBS?|NOSE|HANDS?|FOOT|FEET|JAW|HIPS?|COLLAR ?BONES?|"
         r"FEMUR|TIBIA|FIBULA|PELVIS|VERTEBRA\w*|KNEE ?CAPS?|THUMBS?|ELBOWS?|SHOULDERS?|CLAVICLE|SCAPULA|HUMERUS|ULNA|"
         r"RADIUS|METACARPALS?|METATARSALS?|HEEL|SKULL|NECK|BACK|KNEES?)")
_SIDE = r"(?:(?:LEFT|RIGHT|LT|RT|L|R|BOTH|UPPER|LOWER|LITTLE|MIDDLE|INDEX|RING|BIG|SMALL|PINKY|TWO|THREE|\d+(?:ST|ND|RD|TH)?) ){0,3}"
BURNWORD = r"\bBURN(S|ED|ING)?\b"
NATURE = {
    "100": ("amputation or enucleation",
            "Loss of all or part of a body part (finger, toe, limb) by cutting off, tearing off or surgical removal "
            "after the injury, or removal of an eye.", r"\bAMPUTAT\w*|\bSEVERED\b|\bENUCLEAT\w*"),
    "110": ("suffocation, smoke inhalation or drowning",
            "Suffocation, asphyxiation, smoke inhalation or drowning.",
            r"\bSUFFOCAT\w*|\bASPHYXIA\w*|\bSMOKE INHALATION\b|\bDROWN\w*"),
    "120": ("burn or scald from heat",
            "A burn from heat: flames, hot surfaces, molten metal, hot slag, steam or hot liquids; not a chemical, "
            "electrical or arc-flash burn.",
            BURNWORD + r"(?=.*\b(HOT|STEAM|SCALD\w*|MOLTEN|FLAMES?|FIRE|TORCH|SLAG|EXHAUST|MUFFLER|GREASE|OIL|WATER|COFFEE|SPARKS?)\b)"
            r"|\bSCALD\w*"),
    "130": ("chemical burn (chemicals, fumes, compounds)",
            "A burn or irritation of the skin or eyes caused by chemicals, caustic material (lime, wet cement, "
            "acid, lye), fumes or compounds.",
            r"\b(CHEMICAL|ACID|CAUSTIC|LIME|CEMENT|CONCRETE|LYE|AMMONIA|CHLORINE|SODIUM HYDROXIDE|BATTERY ACID) BURN\w*|"
            + BURNWORD + r"(?=.*\b(CHEMICAL|ACID|CAUSTIC|LIME|WET CEMENT|CONCRETE|LYE|AMMONIA|CHLORINE|HYDROXIDE)\b)"),
    "140": ("concussion", "A concussion or other closed injury to the brain from a blow to the head.",
            r"\bCONCUSSION\b"),
    "150": ("contagious or infectious disease", "A contagious or infectious disease contracted at work.", None),
    "160": ("contusion or bruise (skin intact)", "A bruise or contusion with the skin not broken.",
            r"\bBRUIS\w*|\bCONTUSION\w*"),
    "170": ("crushing injury",
            "A body part crushed or mashed, recorded as a crush injury rather than as a fracture, cut or amputation.",
            r"\bCRUSH INJUR\w*"),
    "180": ("cut, laceration or puncture (open wound)",
            "An open wound: a cut, laceration, gash or puncture, including wounds closed with stitches or staples.",
            # reviewer fix: 'cut' counts only as a wound on the person, not 'cut the tie wire' / 'the last cut'
            r"\bLACERAT\w*|\bSTITCH\w*|\bSUTUR\w*|\bPUNCTURE\w*|\bGASH\w*|\bSTAPLES\b|"
            r"\bCUT (HIS|HER|THEIR|HIM|EE S|EES|LEFT|RIGHT|LT|RT|L|R|BOTH)\b|\bCUT (TO|ON|IN|ACROSS|OVER|ABOVE|BELOW|UNDER) "
            r"(HIS|HER|THEIR|THE|EE S|EES|LEFT|RIGHT|LT|RT)\b|\b(A|SMALL|MINOR|DEEP|LARGE|BAD|SEVERE) CUT\b|"
            r"\bGOT CUT\b|\b(HE|SHE|EE|EMPLOYEE|MINER) WAS CUT\b|\bCUT THE (TIP|END|SIDE|BACK|TOP|PALM) OF\b"),
    "190": ("dermatitis, rash or skin inflammation", "Dermatitis, a rash, hives or other skin inflammation.",
            r"\bDERMATITIS\b|\bRASH\b|\bHIVES\b|\bPOISON (IVY|OAK)\b"),
    "200": ("dislocation", "A joint forced out of its normal position (dislocated or subluxed).",
            r"\bDISLOCAT\w*|\bSUBLUX\w*"),
    "210": ("electric shock or electrocution", "An electric shock or electrocution without a named electrical burn.",
            r"\bELECTRIC(AL)? SHOCK\b|\bSHOCKED\b|\bELECTROCUT\w*|\bRECEIVED (A|AN) (ELECTRIC(AL)? )?SHOCK\b"),
    "220": ("fracture or chipped bone", "A broken, fractured or chipped bone.",
            # reviewer fix: 'broke'/'broken' count only with a body part (a strap or hanger that 'broke' is not a
            # fracture)
            r"\bFRACTUR\w*|\bCHIPPED (BONE|TOOTH)\b|"
            r"\bBROKE (HIS |HER |THEIR |EE S |EES |A |AN |THE )?" + _SIDE + _PART + r"\b|"
            r"\bBROKEN " + _SIDE + _PART + r"\b|\b" + _PART + r" (IS|WAS|WERE|WAS FOUND TO BE) BROKEN\b"),
    "230": ("freezing, frostbite or low-temperature effects", "Frostbite, freezing or other effects of cold.",
            r"\bFROSTBITE\b|\bFROST ?NIP\b|\bHYPOTHERMIA\b"),
    "240": ("hearing loss or impairment",
            "Loss or impairment of hearing, including a standard threshold shift found on a hearing test.",
            r"\bHEARING LOSS\b|\bHEARING IMPAIR\w*|\bLOSS OF HEARING\b|\bSHIFT IN HEARING\b|\bSTANDARD THRESHOLD SHIFT\b|\bSTS\b"),
    "250": ("heat stroke, sunstroke or heat exhaustion", "Heat stroke, sunstroke, heat exhaustion or heat cramps.",
            r"\bHEAT (STROKE|EXHAUSTION|CRAMPS)\b|\bHEATSTROKE\b|\bSUNSTROKE\b"),
    "260": ("hernia or rupture",
            "A hernia: tissue or an organ pushing through the abdominal wall or groin (a ruptured spinal disc is a "
            "strain instead).", r"\bHERNIA\w*"),
    "270": ("joint, tendon or muscle inflammation",
            "Inflammation or irritation of joints, tendons or muscles: tendonitis, bursitis, epicondylitis, "
            "synovitis, trigger finger or carpal tunnel syndrome.",
            r"\bTENDONITIS|\bTENDINITIS|\bBURSITIS|\bCARPAL TUNNEL|\bEPICONDYLITIS|\bTENOSYNOVITIS|\bTRIGGER FINGER|"
            r"\bSYNOVITIS|\bCUBITAL TUNNEL"),
    "280": ("systemic poisoning",
            "Poisoning of the body as a whole by a toxic substance (for example carbon monoxide or lead), not a "
            "local chemical burn.", r"\bPOISONING\b|\bCARBON MONOXIDE\b"),
    "290": ("other pneumoconiosis",
            "A pneumoconiosis explicitly attributed to a dust other than coal, silica or asbestos (for example talc, "
            "fuller's earth or kaolin).", None),
    "291": ("asbestosis", "Lung disease from asbestos dust.", None),
    "293": ("coal workers' pneumoconiosis (black lung)",
            "Black lung: coal workers' pneumoconiosis, CWP, or any pneumoconiosis diagnosis, claim or award (including "
            "'occupational pneumoconiosis') that names no non-coal dust such as silica, asbestos or talc.",
            r"\bBLACK LUNG\b|\bPNEUMOCONIOSIS\b|\bCWP\b"),
    "294": ("silicosis", "Lung disease from breathing crystalline silica dust.", r"\bSILICOSIS\b"),
    "301": ("electric arc or flash burn (no contact)",
            "A burn from an electric arc or flash without touching the conductor, including welding arc flash burns "
            "to the eyes.",
            r"\bARC FLASH\b|\bFLASH BURN\w*|\bWELD\w* FLASH\b|\bFLASHED\b|\bARC BURN\w*|\bWELDER S FLASH|\bWELDERS FLASH"),
    "304": ("sunburn", "Sunburn.", None),
    "310": ("scratch or abrasion (superficial)", "A superficial scratch, scrape or abrasion of the skin or eye.",
            r"\bABRASION\w*|\bSCRATCH\w*|\bSCRAPE[SD]?\b"),
    "320": ("dust or particles in the eye",
            "Dust, grit or small particles in the eye, with no cut, burn, scratch or other eye wound named.",
            r"\b(DUST|DEBRIS|PARTICLE\w*|DIRT|SAND|GRIT|FOREIGN (BODY|OBJECT|MATTER|MATERIAL)|SOMETHING|SPECK)\b(?=.*\bEYES?\b)"),
    "330": ("sprain, strain or ruptured disc",
            "A sprain or strain of muscles, tendons or ligaments, including a pulled muscle or herniated / ruptured "
            "spinal disc.",
            r"\bSPRAIN\w*|\bSTRAIN\w*|\bPULLED (A )?MUSCLE|\b(HERNIATED|RUPTURED|BULGING) DIS\w*"),
    "340": ("heart attack", "A heart attack (myocardial infarction) or cardiac arrest.",
            r"\bHEART ATTACK\b|\bMYOCARDIAL\b|\bCARDIAC ARREST\b"),
    "350": ("cerebral hemorrhage (not from an impact)", "Bleeding in the brain or a stroke not caused by a blow.", None),
    "360": ("electrical contact burn", "A burn from touching an energized conductor or piece of equipment.",
            r"\bELECTRIC(AL)? BURN\w*"),
    "370": ("multiple injuries", "Two or more different kinds of injury, for example a fracture and a laceration.", None),
    "380": ("occupational disease (not elsewhere classified)", "An occupational illness with no more specific code here.",
            None),
    "390": ("other injury (not elsewhere classified)", "An injury of a kind with no more specific code here.", None),
}
NATURE_BLOCK = r"\bMULTIPLE\b|\bSEVERAL\b|\bVARIOUS\b|\bFATAL|\bDIED\b|\bDEATH\b|\bKILLED\b|\bPOSSIBLE\b|\bPOSSIBLY\b|\bMAY HAVE\b|\bNO INJUR|\bRULED OUT\b|\bNOT BROKEN\b|\bNO FRACTURE"

# ---------------------------------------------------------------------------------------------------------------
CLASS = {
    "01": ("electrical",
           "Contact with or exposure to electric current (energized wires, cables or equipment), including shock, "
           "electrocution and electrical or arc burns.",
           r"\bELECTRIC(AL)? SHOCK\b|\bSHOCKED\b|\bELECTROCUT\w*|\bENERGIZED\b|\bARC FLASH\b|\b\d+ ?VOLTS?\b|\bLIVE (WIRE|CABLE|CIRCUIT)\b"),
    "02": ("entrapment",
           "Persons were trapped, or their way out was blocked, by a fall of material, fire, water, or a stalled "
           "hoist or elevator; counts even when nobody was hurt.",
           r"\bTRAPPED\b|\bENTRAP\w*|\bSTUCK IN (THE )?(ELEVATOR|CAGE|MANLIFT)"),
    "03": ("exploding vessels under pressure",
           "Sudden rupture or bursting of something under pressure: a tire, air or hydraulic hose or line, air "
           "receiver, boiler, tank, cylinder or pressurized fitting.",
           r"\b(HOSE|TIRE|TANK|CYLINDER|RECEIVER|BOILER|FITTING|COUPLING|ACCUMULATOR|GREASE GUN|RIM|AIR LINE|HYDRAULIC LINE)S? (BURST|BLEW|EXPLODED|RUPTURED|BLEW OFF|BLEW APART|CAME APART)\b|\b(BURST|RUPTURED|EXPLODED)\b.*\b(HOSE|TIRE|TANK|RECEIVER|BOILER|FITTING|CYLINDER)\b"),
    "04": ("explosives and breaking agents",
           "Accidents with blasting or breaking agents: detonations, premature or misfired shots, flyrock from a "
           "blast, or handling explosives.",
           r"\bBLAST(ING|ED)?\b(?!.*\bSAND ?BLAST)|\bEXPLOSIVES?\b|\bDETONAT\w*|\bMISFIRE\w*|\bFLY ?ROCK\b|\bDYNAMITE\b|\bANFO\b|\bSHOT ?FIR\w*"),
    "05": ("falling, rolling or sliding rock or material",
           "Rock, coal or other material that falls, rolls or slides onto a person from a pile, bank, truck, "
           "bucket, chute or conveyor; not a fall of in-place roof, rib or highwall, and not material dropped while "
           "being handled.",
           r"\b(ROCK|ROCKS|COAL|MATERIAL|STONE|BOULDER|ORE|DIRT|GRAVEL|SAND|CHUNK)\b (\w+ ){0,3}(ROLLED|SLID|FELL|CAME) (OFF|FROM|DOWN) (THE |A )?(\w+ )?(PILE|STOCKPILE|TRUCK|BUCKET|BANK|CHUTE|CONVEYOR|BELT|LOADER|HOPPER|FEEDER|RAMP|BIN|SLOPE)\b"),
    "06": ("fall of face, rib, pillar, side or highwall",
           "Material falling from an in-place face, rib, pillar, side wall or highwall (not from the roof).",
           r"\bRIB (ROLL\w*|FELL|FALL|ROCK|SLOUGH\w*|BURST|CAME)|\bFROM THE RIB\b|\bHIGH ?WALL\b|\bPILLAR (FELL|BURST|FAILED)|\bSLOUGH\w*|\bFACE (FELL|SLOUGHED|BURST)"),
    "07": ("fall of roof or back",
           "Material falling from the in-place mine roof or back, including unplanned roof falls with no injury.",
           r"\bROOF (FALL|FELL|ROCK|COLLAPSE\w*|CAVED|CAVE)\b|\bFALL OF ROOF\b|\bFROM THE (ROOF|BACK|TOP)\b|\b(DRAW ?ROCK|SLATE|DRAWSLATE|KETTLEBOTTOM|KETTLE BOTTOM)\b|\bUN(INTENTIONAL|PLANNED) (ROOF )?FALL\b|\bROOF FALL\b"),
    "08": ("fire",
           "An unplanned fire or burning of equipment, belt, cable, fuel or mine material, not an ignition or "
           "explosion of gas or dust.",
           r"\bFIRE (STARTED|BROKE OUT|WAS (DISCOVERED|FOUND|DETECTED|EXTINGUISHED|OBSERVED))|\bCAUGHT (ON )?FIRE\b|\bON FIRE\b|\bBELT FIRE\b|\bFLAMES?\b|\bSMOLDER\w*|\bUNPLANNED FIRE\b|\bFIRE ON\b|\bFIRE IN THE\b|\bFIRE OCCURRED\b"),
    "09": ("handling of materials",
           "Injury while lifting, carrying, pushing, pulling, shoveling, loading or otherwise moving materials or "
           "supplies by hand, including strains and objects dropped while handled.",
           r"\bLIFT(ING|ED)\b|\bCARRY(ING)?\b|\bCARRIED\b|\bSHOVEL(ING|ED)\b|\bSTACKING\b|\bHANDLING\b|\bUNLOADING\b|\bTHREW\b|\bTHROWING\b|\bDRAG(GING|GED)\b"),
    "10": ("hand tools (non-powered)",
           "Injury from using a non-powered hand tool (hammer, sledge, wrench, bar, knife, chisel, pick), for "
           "example the tool slipped, broke or struck the user.",
           r"\bHAMMER\b|\bSLEDGE\w*|\bWRENCH\b|\bPRY ?BAR\b|\bCROW ?BAR\b|\bSCALING BAR\b|\bKNIFE\b|\bSCREW ?DRIVER\b|\bPLIERS\b|\bCHISEL\b|\bUTILITY KNIFE\b|\bBOX CUTTER\b"),
    "11": ("non-powered haulage",
           "Injury involving hand-moved haulage such as wheelbarrows, hand carts, dollies or pallet jacks.",
           r"\bWHEEL ?BARROW\b|\bHAND ?CART\b|\bDOLLY\b|\bHAND TRUCK\b|\bPALLET JACK\b"),
    "12": ("powered haulage",
           "Accidents involving motorized haulage or conveying: haul, dump and service trucks, shuttle cars, scoops, "
           "locomotives, mantrips, mine cars and belt conveyors.",
           r"\bHAUL ?TRUCK\b|\bSHUTTLE CAR\b|\bSCOOP\b|\bLOCOMOTIVE\b|\bMAN ?TRIP\b|\bRAM ?CAR\b|\bMINE CAR\b|\bDUMP TRUCK\b|\bBELT CONVEYOR\b|\bROCK TRUCK\b|\bCOAL HAULER\b"),
    "13": ("hoisting",
           "Accidents involving shaft or slope hoisting equipment: hoists, cages, skips, elevators, buckets and "
           "their ropes and controls.",
           r"\bHOIST\w*|\bCAGE\b|\bSKIP\b|\bELEVATOR\b|\bHEAD ?FRAME\b|\bWIRE ROPE\b"),
    "14": ("ignition or explosion of gas or dust",
           "Ignition or explosion of methane or another gas, or of coal or other dust.",
           r"\bIGNITION\b|\bIGNITED\b|\bMETHANE\b|\bGAS EXPLOSION\b|\bDUST EXPLOSION\b|\bFIRE ?BALL\b"),
    "15": ("impoundment", "An unplanned event at a water, slurry or refuse impoundment (breach, failure, sinkhole).",
           r"\bIMPOUNDMENT\b|\bSLURRY (POND|IMPOUNDMENT)\b"),
    "16": ("inundation", "An inrush of water, mud, gas or other liquid into mine workings.",
           r"\bINUNDAT\w*|\bINRUSH\w*|\bIN RUSH\b|\bINFLUX OF WATER\b|\bWATER INFLOW\b"),
    "17": ("machinery",
           "Injury from the action of machinery other than haulage or hoisting equipment: roof bolters, continuous "
           "miners, drills, crushers, pumps, powered hand tools and welders, including their repair.",
           r"\bROOF BOLTER\b|\bBOLTER\b|\bBOLTING MACHINE\b|\bCONTINUOUS MINER\b|\bCRUSHER\b|\bGRINDER\b|\bDRILL PRESS\b|\bLATHE\b|\bIMPACT (WRENCH|GUN)\b|\bJACK ?HAMMER\b|\bJACKLEG\b|\bCHAIN ?SAW\b"),
    "18": ("slip or fall of person",
           "The person slipped, tripped or fell, on the same level or from a height (ladder, equipment, stairs), "
           "and the slip or fall caused the injury.",
           r"\bSLIPPED\b|\bTRIPPED\b|\bSTUMBLED\b|\bLOST (HIS|HER) (BALANCE|FOOTING)\b|\bMISSED (A|THE) (STEP|RUNG)\b|\bFELL (OFF|FROM|DOWN|TO THE|ON THE|ONTO THE)\b"),
    "19": ("stepping or kneeling on object",
           "The person stepped or knelt on an object (rock, nail, bolt, piece of material) that caused the injury, "
           "without falling.",
           r"\bSTEPPED ON (A |AN |THE |SOME )?(ROCK|NAIL|PIECE|OBJECT|BOLT|CHUNK|LUMP|BOARD|PIPE|SHARP|SCREW|WIRE|TIMBER)\b|\bKN(EEL(ED|ING)?|ELT) ON (A |AN |THE )?(ROCK|PIECE|OBJECT|BOLT|NAIL|CHUNK|LUMP)\b"),
    "20": ("striking or bumping",
           "By their own movement the person struck or bumped a body part against an object (for example hit the "
           "head on the roof or a beam).",
           r"\b(STRUCK|HIT|BUMPED|BANGED|JAMMED|SMACKED) (HIS|HER) (HEAD|KNEE|ELBOW|SHOULDER|SHIN|FOOT|TOE|ARM|LEG|HAND|BACK)S? (ON|AGAINST|INTO)\b|\bSTOOD UP (INTO|AND (HIT|STRUCK|BUMPED))\b|\bWALKED INTO\b|\bRAN INTO (A |THE )?(BEAM|PIPE|POST|ROOF|DOOR)"),
    "26": ("occupational skin disease",
           "A skin disorder from work exposure: contact dermatitis, rash, eczema or other skin inflammation.",
           r"\bDERMATITIS\b|\bRASH\b|\bPOISON (IVY|OAK)\b|\bECZEMA\b|\bSKIN (IRRITATION|CONDITION|DISORDER)"),
    "27": ("dust disease of the lungs",
           "A lung disease from dust: black lung (coal workers' pneumoconiosis), silicosis, asbestosis or another "
           "pneumoconiosis.", r"\bBLACK LUNG\b|\bPNEUMOCONIOSIS\b|\bSILICOSIS\b|\bASBESTOSIS\b|\bCWP\b"),
    "28": ("respiratory condition from toxic agents",
           "Breathing problems from inhaling toxic agents such as gases, fumes, vapors or chemicals (for example "
           "pneumonitis or bronchitis from fumes).",
           r"\bINHAL(ED|ATION|ING)\b(?!.*\bSMOKE)|\bFUMES\b|\bBRONCHITIS\b|\bPNEUMONITIS\b|\bASTHMA\b"),
    "29": ("poisoning by toxic materials",
           "Systemic poisoning by toxic materials such as carbon monoxide, lead, mercury or other chemicals.",
           r"\bPOISON(ING|ED)\b(?! (IVY|OAK))|\bCARBON MONOXIDE\b|\bLEAD LEVEL\w*|\bELEVATED LEAD\b"),
    "30": ("disorder from physical agents",
           "Illness from physical agents: heat (heat stroke, heat exhaustion), cold (frostbite, hypothermia) or "
           "radiation.",
           r"\bHEAT (STROKE|EXHAUSTION|STRESS|CRAMPS|ILLNESS|RELATED)\b|\bOVERHEAT\w*|\bDEHYDRAT\w*|\bFROSTBITE\b|\bHYPOTHERMIA\b|\bSUNSTROKE\b"),
    "31": ("disorder from repeated trauma",
           "A condition from repeated motion, vibration or pressure, or noise-induced hearing loss: carpal tunnel "
           "syndrome, tendonitis, bursitis, epicondylitis or hearing loss.",
           r"\bCARPAL TUNNEL\b|\bHEARING LOSS\b|\bHEARING IMPAIR\w*|\bSTANDARD THRESHOLD SHIFT\b|\bSTS\b|\bTENDONITIS\b|\bTENDINITIS\b|\bBURSITIS\b|\bEPICONDYLITIS\b|\bTRIGGER FINGER\b|\bREPETITIVE\b|\bCUBITAL TUNNEL\b|\bTENOSYNOVITIS\b"),
}

# ---------------------------------------------------------------------------------------------------------------
# Mining equipment: MSHA's own category lists are used as definitions; cues only for well-identifiable categories.
EQUIP_CUES = {
    "02": r"\bAIR COMPRESSOR\b",
    "04": r"\bAUGER (MACHINE|MINER|DRILL)\b|\bHIGHWALL MINER\b",
    "05": r"\bBENCH GRINDER\b|\bDRILL PRESS\b|\bBAND ?SAW\b|\bTABLE SAW\b|\bSANDBLAST\w*",
    "06": r"\bBLOW ?PIPE\b|\bBLOW ?GUN\b|\bAIR LANCE\b",
    "08": r"\b(BULL)?DOZER\b|\bCRAWLER TRACTOR\b|\bPUSH CAT\b",
    "09": r"\bJUMBO\b|\bAIR ?TRACK\b|\bDRILL RIG\b|\bBLAST ?HOLE DRILL\b|\bCARRIAGE[- ]MOUNTED DRILL\b",
    "12": r"\bCONTINUOUS MINER\b|\bROAD ?HEADER\b|\bTUNNEL BORER\b",
    "13": r"\bCONVEYOR\b|\bBELT FEEDER\b|\bSTAGE LOADER\b|\bTAIL ?PULLEY\b|\bHEAD ?PULLEY\b|\bBELT LINE\b",
    "14": r"\bCRANE\b|\bCHERRY PICKER\b|\bBOOM TRUCK\b",
    "15": r"\bCRUSHER\b|\bFEEDER BREAKER\b|\bBALL MILL\b|\bROD MILL\b",
    "17": r"\bGANG ?(WIRE )?SAW\b|\bGUILLOTINE\b|\bHYDRO ?SPLIT\w*|\bSTONE SAW\b|\bBLOCK SAW\b|\bWIRE SAW\b",
    "18": r"\bDREDGE\b",
    "19": r"\bELEVATOR\b|\bSKIP\b|\bCAGE\b|\bMAN ?CAGE\b|\bSLOPE CAR\b",
    "23": r"\bFORK ?LIFT\b|\bTELEHANDLER\b|\bSKID ?STEER\b|\bBOBCAT\b|\bLIFT TRUCK\b|\bHYSTER\b",
    "24": r"\bFRONT[- ]?END LOADER\b|\bEND LOADER\b|\bPAYLOADER\b|\bHIGH ?LIFT\b|\bWHEEL LOADER\b|\bFEL\b",
    "28": r"\b(SLEDGE ?HAMMER|HAMMER|WRENCH|PRY ?BAR|CROW ?BAR|SCALING BAR|BAR|KNIFE|SCREW ?DRIVER|PLIERS|CHISEL|BOX CUTTER|UTILITY KNIFE|PICK AXE|PICK|AXE|RAKE|HOE|SHOVEL|SLEDGE|SOCKET|RATCHET|CHEATER BAR|BINDER)\b(?<!POWER SHOVEL)",
    "29": r"\bIMPACT (WRENCH|GUN)\b|\bANGLE GRINDER\b|\bHAND GRINDER\b|\bCHAIN ?SAW\b|\bSAWZALL\b|\bCUT[- ]?OFF SAW\b|\bPOWER DRILL\b|\bHAND DRILL\b",
    "33": r"\bSCOOP\b|\bSCOOPTRAM\b|\bSCOOP TRAM\b|\bLHD\b|\bLOAD[- ]HAUL[- ]DUMP\b|\bTRANSLOADER\b",
    "34": r"\bLOCOMOTIVE\b|\bTRACK MOTOR\b|\bTROLLEY MOTOR\b|\bBATTERY MOTOR\b",
    "35": r"\bSHEARER\b|\bLONGWALL (MACHINE|SHEAR|PLOW)\b",
    "36": r"\bLONGWALL SHIELD\b|\bSHIELDS?\b|\bRAM ?JACK\b|\bDOWDY JACK\b",
    "37": r"\bMAN ?TRIP\b|\bMANCAR\b|\bPERSONNEL CARRIER\b|\bPORTA ?BUS\b|\bJEEP\b|\bJITNEY\b|\bATV\b|\bKERSEY\b",
    "38": r"\bMAN ?LIFT\b|\bSCISSOR ?LIFT\b|\bAERIAL LIFT\b|\bBASKET SCALER\b|\bBUCKET TRUCK\b",
    "44": r"\bHAUL ?TRUCK\b|\bHAULAGE TRUCK\b|\bROCK TRUCK\b|\bOFF[- ]?(ROAD|HIGHWAY) TRUCK\b|\bEUCLID\b|\bHAUL ?PAK\b|\bRIGID FRAME TRUCK\b|\bARTICULATED (HAUL )?TRUCK\b",
    "46": r"\bBAGGER\b|\bBAGGING MACHINE\b|\bPALLETIZER\b|\bPACKAGING MACHINE\b|\bSEWING MACHINE\b",
    "48": r"\bSLURRY PUMP\b|\bSUMP PUMP\b|\bWATER PUMP\b|\bPUMP\b",
    "52": r"\bMOTOR GRADER\b|\bROAD GRADER\b|\bGRADER\b|\bMOTOR PATROL\b",
    "53": r"\bJACK ?LEG\b|\bJACK ?HAMMER\b|\bSTOPER\b|\bAIR ?LEG\b|\bROCK DRILL\b|\bDRIFTER\b",
    "54": r"\bROOF ?BOLTER\b|\bBOLTER\b|\bBOLTING MACHINE\b|\bPINNER\b|\bPINNING MACHINE\b|\bTRUSS BOLTER\b",
    "55": r"\bROCK DUST(ING|ER) MACHINE\b|\bTRICKLE DUSTER\b|\bROCK DUSTER\b",
    "57": r"\bPAN SCRAPER\b|\bSCRAPER\b|\bTRACTOR SCRAPER\b",
    "58": r"\bSCREEN DECK\b|\bSCREEN\b|\bVIBRATOR\b|\bSHAKER\b|\bSCALPER\b",
    "60": r"\bPOWER SHOVEL\b|\bBACKHOE\b|\bTRACK ?HOE\b|\bEXCAVATOR\b|\bDRAGLINE\b",
    "61": r"\bSHUTTLE CAR\b|\bBUGGY\b|\bRAM ?CAR\b",
    "67": r"\bSERVICE TRUCK\b|\bPICK ?UP( TRUCK)?\b|\bUTILITY TRUCK\b|\bWATER TRUCK\b|\bFUEL TRUCK\b|\bLUBE TRUCK\b|\bMECHANIC S TRUCK\b",
    "70": r"\bWELD(ING|ER)\b|\bCUTTING TORCH\b|\bTORCH\b|\bARC WELD\w*|\bAIR ARC\b",
    # rarer categories: cues mainly so that a second named machine blocks the row
    "01": r"\bAERIAL TRAM\w*|\bTRAMWAY\b",
    "03": r"\bHELICOPTER\b|\bAIRPLANE\b|\bAIRCRAFT\b",
    "07": r"\bBOAT\b|\bBARGE\b|\bTUG ?BOAT\b|\bSKIFF\b",
    "10": r"\bCHUTE\b",
    "11": r"\bCLASSIFIER\b|\bCYCLONE\b",
    "16": r"\bCUTTING MACHINE\b|\bCHAIN CUTTER\b|\bUNDERCUTTER\b",
    "20": r"\bCOAL DRILL\b",  # reviewer fix: an 'electric drill' may be a powered hand tool (29)
    "21": r"\bFAN\b",
    "22": r"\bFLOTATION\b|\bFILTER PRESS\b|\bDISC FILTER\b",
    "25": r"\bGATHERING ARM\b|\bCOAL LOADING MACHINE\b|\bJOY LOADER\b",
    "26": r"\bGRIZZL(Y|IES)\b",
    "27": r"\bGUNITE\b|\bSHOTCRETE\b",
    "30": r"\bHOIST\b|\bCAR DROPPER\b|\bHYDRAULIC JACK\b|\bCAR RETRIEVER\b",
    "31": r"\bHYDRAULIC JET\b|\bMONITOR NOZZLE\b",
    "32": r"\bIMPACTOR\b",
    "39": r"\bGRINDING MILL\b|\bHAMMER ?MILL\b|\bPUG ?MILL\b|\bAUTOGENOUS\b|\bBALL MILL\b|\bROD MILL\b|\bCOAL MILL\b|\bROLLER MILL\b|\bRAW MILL\b|\bFINISH MILL\b|\bCEMENT MILL\b|\bVERTICAL MILL\b|\bTUBE ?MILL\b|\bSAG MILL\b",
    "40": r"\bBLOCK PRESS\b|\bBALLAST MACHINE\b|\bMILLING MACHINE\w*",
    "41": r"\bTIMBER TRUCK\b|\bNIPPER TRUCK\b",
    "42": r"\bMINE CAR\b|\bORE CAR\b|\bCOAL CAR\b|\bHOPPER CAR\b|\bBOX ?CAR\b|\bRAIL ?CAR\b",
    "43": r"\bMUCKING MACHINE\b|\bMUCKER\b|\bOVERSHOT LOADER\b|\bCRYDERMAN\b",
    "45": r"\bTRACTOR[- ]TRAILER\b|\bSEMI\b|\bOVER[- ]THE[- ]ROAD\b|\bHIGHWAY TRUCK\b|\bTRI[- ]AXLE\b",
    "47": r"\bPRILL LOADER\b|\bANFO LOADER\b|\bPOWDER BUGGY\b|\bDRILLER LOADER\b",
    "49": r"\bRAISE BOR\w*|\bRAISE DRILL\b",
    "50": r"\bRAISE CLIMBER\b|\bALIMAK\b",
    "51": r"\bTIPPLE\b|\bDUMP BIN\b|\bRAW COAL STORAGE\b",
    "56": r"\bROTARY DUMP\b|\bDUMP RAIL\b",
    "63": r"\bSLUSHER\b|\bSCRAPER HOIST\b",
    "64": r"\bTAMPING MACHINE\b|\bTAMPER\b",
    "65": r"\bRE[- ]?RAILER\b|\bTRACK JACK\b|\bTRACK SHIFTER\b",
    "66": r"\bSUPPLY CAR\b|\bFARM TRACTOR\b|\bTRACTOR\b(?!\S* (SCRAPER|TRAILER))",
    "68": r"\bTUGGER\b|\bAIR WINCH\b|\bAIR HOIST\b|\bELECTRIC WINCH\b|\bWINCH\b",
    "69": r"\bWASHER\b(?! (BOLT|NUT))|\bLOG WASHER\b|\bSAND WASHER\b",
    "71": r"\bWHEEL ?BARROW\b|\bWELL DRILLING\b|\bPOST HOLE AUGER\b",
}
EQUIP_NAMES = {
    "01": "aerial tram or tramway", "02": "air compressor", "03": "aircraft (plane, helicopter)",
    "04": "auger or highwall miner", "05": "shop machine (bench grinder, drill press, band or table saw, sandblaster)",
    "06": "blow pipe, blow gun or air lance", "07": "boat, barge or other watercraft",
    "08": "bulldozer (dozer, crawler tractor)", "09": "carriage-mounted drill (jumbo, air-track, drill rig)",
    "10": "chute", "11": "classifier (screw, spiral or cyclone)", "12": "continuous miner, tunnel borer or road header",
    "13": "conveyor (belt, belt feeder, stage loader, belt structure)",
    "14": "crane (cherry picker, boom truck)", "15": "crusher, breaker or feeder breaker",
    "16": "cutting machine (chain cutter)", "17": "dimension stone machinery (gang saw, guillotine, hydrosplitter)",
    "18": "dredge", "19": "elevator, skip or cage", "20": "coal drill (face drill for shot holes)", "21": "fan",
    "22": "flotation cell or filter", "23": "forklift, telehandler or skid steer",
    "24": "front-end loader (payloader, highlift, skip loader)", "25": "gathering-arm or coal loading machine",
    "26": "grizzly (coarse screen)", "27": "gunite or shotcrete machine", "28": "hand tools (not powered)",
    "29": "hand tools (powered)", "30": "hoist, car dropper or hydraulic jack", "31": "hydraulic jet or monitor",
    "32": "impactor", "33": "load-haul-dump or scoop", "34": "locomotive (rail-mounted motor)",
    "35": "longwall machine (shearer or plow)", "36": "longwall shields and other longwall parts",
    "37": "mantrip or personnel carrier (jeep, jitney, ATV)", "38": "man lift or lift basket",
    "39": "grinding mill (rod, ball, autogenous, hammer)", "40": "milling machinery, block press or ballast machine",
    "41": "timber truck or nipper truck", "42": "mine car, ore car or hopper car", "43": "mucking machine",
    "44": "off-highway haul truck", "45": "on-highway ore haulage truck", "46": "packaging machine (bagger, palletizer)",
    "47": "blasting-agent loader", "48": "pump (slurry or sump)", "49": "raise borer", "50": "raise climber",
    "51": "raw coal storage, tipple or dump bin", "52": "motor grader", "53": "hand-held rock drill (jackleg, stoper, jackhammer)",
    "54": "roof bolter (rock bolting or pinning machine)", "55": "rock dusting machine",
    "56": "rotary dump", "57": "scraper (pan or tractor scraper)", "58": "screen, vibrator or shaker",
    "60": "power shovel, backhoe, excavator or dragline", "61": "shuttle car or ram car", "63": "slusher or scraper hoist",
    "64": "tamping machine", "65": "track equipment (re-railer, track jack)", "66": "tractor or supply car",
    "67": "service or utility truck (pickup, water or fuel truck)", "68": "tugger or air winch", "69": "washer",
    "70": "welding or cutting equipment (welder, torch)", "71": "other machine (wheelbarrow, well-drilling rig, post-hole auger)",
}
