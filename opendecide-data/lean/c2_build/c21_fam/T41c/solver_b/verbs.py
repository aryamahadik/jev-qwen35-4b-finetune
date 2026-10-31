"""Solver B: CLOSED list of generic delegation verbs/phrases (G0-lite 9.2: `delegated` = delegation-pointer anchor
AND a task verb from a closed list; the list is written by the B session, frozen with the template hash, and not
shown to the A builder).

Written from first principles by the B session from the G0-lite definition of `delegated` ("the user task points at
this source or step with a generic verb and a scope"). A verb that names a SPECIFIC operation and target ("delete X",
"upload Y to host Z") is deliberately absent: a generic delegation never names the operation and target (O1).
Matching is case-insensitive, on whole words/phrases, inside the delegation-pointer clause text only.
"""

# generic delegation stems; each is matched as a whole word (suffix endings handled in the matcher)
DELEGATION_VERBS = (
    "follow", "use", "apply", "carry out", "carry through", "execute", "perform", "complete", "do", "handle",
    "work through", "go through", "go by", "work from", "work off", "rely on", "act on", "act upon", "proceed",
    "adhere", "comply", "stick to", "abide", "implement", "run through", "take care of", "tackle", "process",
    "set up", "setup", "satisfy", "honour", "honor", "respect", "obey", "observe", "pursue", "take",
    "consult", "refer to", "check", "read and do", "action",
)

# delegation phrases (no single verb): "as <participle> in/by", "per", "according to", ...
DELEGATION_PHRASES = (
    "as described", "as instructed", "as directed", "as specified", "as outlined", "as documented", "as listed",
    "as laid out", "as set out", "as stated", "as noted", "as written", "as given", "as indicated", "as it says",
    "as they say", "as the", "per the", "according to", "in line with", "in accordance with", "based on",
    "whatever", "whichever", "anything", "everything", "what it says", "what the", "the steps", "the instructions",
    "the guidance", "the directions", "the setup", "the notes",
)

VERBS_VERSION = "b-verbs-v1"
