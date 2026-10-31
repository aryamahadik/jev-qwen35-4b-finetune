"""c2_kit/globsem.py: the glob semantics a card states (C2_DATA_SPEC 3.1 T28, 3.2 T35). Parameters only, no matching.

Two matchers implement these semantics independently: glob_a.py (token AST + memoised search; solver-A side) and
glob_b.py (compiled regular expression; solver-B side). A solver B module must never import glob_a (plugin check).

  star_crosses_slash  "*" also matches "/" (T35 robots rules: True; T28 cards state it either way)
  anchored            True: the whole subject must match; False: a prefix match is enough (robots path rules)
  dollar_end          a trailing "$" anchors the end of the subject (robots); elsewhere "$" is a literal
  question_mark       "?" matches one character (never "/" unless star_crosses_slash); False: "?" is a literal
  double_star         "**" matches anything, "/" included, even when "*" does not cross "/"
  case_sensitive      compare characters exactly (True) or ignoring ASCII letter case (patterns and subjects are ASCII)
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GlobSem:
    star_crosses_slash: bool = False
    anchored: bool = True
    dollar_end: bool = False
    question_mark: bool = True
    double_star: bool = False
    case_sensitive: bool = True

    def card_text(self) -> str:
        """One plain sentence per parameter, for the card (every C2 card states its glob semantics)."""
        out = ['"*" matches any run of characters, including "/".' if self.star_crosses_slash
               else '"*" matches any run of characters except "/".']
        if self.double_star and not self.star_crosses_slash:
            out.append('"**" matches any run of characters, including "/".')
        if self.question_mark:
            out.append('"?" matches exactly one character' + ('.' if self.star_crosses_slash else ' other than "/".'))
        out.append("A pattern must match the whole value." if self.anchored
                   else "A pattern matches when it matches the start of the value.")
        if self.dollar_end:
            out.append('A "$" at the end of a pattern means the value must end there.')
        out.append("Letter case matters." if self.case_sensitive else "Letter case is ignored.")
        return " ".join(out)


ROBOTS = GlobSem(star_crosses_slash=True, anchored=False, dollar_end=True, question_mark=False)
