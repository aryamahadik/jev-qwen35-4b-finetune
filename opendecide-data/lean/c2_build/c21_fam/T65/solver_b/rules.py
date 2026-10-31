"""Solver B tables (T65). Everything here is a constant written from the G0-lite sections 2.1 / 5 and the ROW_SCHEMA; nothing is read at run time.

Class ids follow the registry (CWEC-n). The neutraliser table is B's OWN reading of "a step made for that kind of operation" (G0-lite 2.1): a call or edit
is credited to exactly the class it is made for, and to no other.
"""

DYNAMIC = ("CWEC-22", "CWEC-78", "CWEC-79", "CWEC-89", "CWEC-117", "CWEC-601")
STATIC = ("CWEC-295", "CWEC-327", "CWEC-377")
CLASSES = DYNAMIC + STATIC
ALL_NEUT = frozenset(DYNAMIC)          # a value that is one of fixed constants (allow-list) is neutral for every dynamic class

# class words (ROW_SCHEMA section 2) and keyword stems used to read the option text of a CWE head row
CLASS_WORDS = {"CWEC-22": "path traversal", "CWEC-78": "OS command injection", "CWEC-79": "cross-site scripting", "CWEC-89": "SQL injection",
               "CWEC-117": "log injection", "CWEC-601": "open redirect", "CWEC-295": "disabled certificate verification",
               "CWEC-327": "weak password hashing", "CWEC-377": "insecure temporary file"}
# ordered: the first class whose stem list has a hit in the option text (all stems of one entry must be absent from the others)
WORD_STEMS = (("CWEC-22", ("traversal",)), ("CWEC-78", ("command",)), ("CWEC-79", ("cross-site", "scripting", "xss")), ("CWEC-89", ("sql",)),
              ("CWEC-117", ("log injection", "log forging", "log ")), ("CWEC-601", ("redirect",)),
              ("CWEC-295", ("certificate", "tls", "verification")), ("CWEC-327", ("hash",)), ("CWEC-377", ("temporary", "temp file", "tempfile")))

# qualified call name -> class it neutralises (registry SAN-*, one API per class in the standard library)
NEUTRALISER_CALLS = {"os.path.basename": "CWEC-22", "shlex.quote": "CWEC-78", "html.escape": "CWEC-79"}
# str.replace(old, new) pairs that neutralise (the literal arguments are read from the code)
REPLACE_NEUT = {("'", "''"): "CWEC-89", ("\n", " "): "CWEC-117", ("\n", ""): "CWEC-117", ("\r\n", " "): "CWEC-117"}
# string methods that keep the value's state (benign transforms, G0-lite 2.1)
PASS_METHODS = frozenset(["strip", "lstrip", "rstrip", "lower", "upper", "title", "casefold", "capitalize", "encode", "decode", "hex", "hexdigest", "digest",
                          "swapcase", "zfill", "ljust", "rjust", "center", "expandtabs", "removeprefix", "removesuffix", "splitlines", "split", "copy"])
CLEAN_RESULT_METHODS = frozenset(["read", "readlines", "readline", "fetchall", "fetchone", "fetchmany", "close", "commit", "write", "flush", "startswith", "endswith",
                                  "isalnum", "isalpha", "isdigit", "isnumeric", "isascii", "isspace", "isidentifier", "count", "find", "index", "rollback", "seek", "tell"])
# builtins whose result carries no state of the arguments
CLEAN_BUILTINS = frozenset(["len", "bool", "isinstance", "print", "any", "all", "min", "max", "sum", "ord", "chr", "id", "hash", "repr_len"])
PASS_BUILTINS = frozenset(["str", "bytes", "bytearray", "repr", "format", "sorted", "list", "tuple", "set", "reversed"])

SHELL_CALLS = frozenset(["subprocess.run", "subprocess.call", "subprocess.check_call", "subprocess.check_output", "subprocess.Popen", "subprocess.getoutput",
                         "subprocess.getstatusoutput"])
SHELL_STRING_CALLS = frozenset(["os.system", "os.popen"])
FAST_HASHES = frozenset(["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "sha3_224", "sha3_256", "sha3_384", "sha3_512"])
SLOW_HASHES = frozenset(["pbkdf2_hmac", "scrypt"])

PW_NAME_STEMS = ("password", "passwd", "pwd", "passphrase")
LOG_LEVEL_WORDS = ("INFO", "WARN", "WARNING", "ERROR", "DEBUG", "CRITICAL", "NOTICE", "TRACE")
