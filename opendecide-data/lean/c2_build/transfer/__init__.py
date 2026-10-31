"""c2_build/transfer: the four transfer-dev families (C2_DATA_SPEC 2.2, 3.20; PREREG A37 d). Code only before A38.

T36 dependency version-range satisfaction, T19 compliance checklist with scope exclusions and evidence expiry, T21
contract cross-references and carve-outs, T20 incident severity with override precedence and timed escalation.
Each is a C2Plugin of tier transfer_dev with its own registers and skins (never used in training), a frozen G0-lite
spec and an independent solver B. Every row they make is dev-only (meta.dev_only = true): 300 items per family,
frozen with sha256 before training, never trained. Nothing here writes a file (A37 f).
"""
