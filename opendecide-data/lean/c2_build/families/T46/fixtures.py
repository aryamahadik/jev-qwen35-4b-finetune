"""families/T46/fixtures.py: in-memory stand-ins for the Haiku pools (tests and dry runs only; never written, never
trained). The real pools are authored by fresh Haiku agents (haiku_author.py) and admitted by G-LEX 2/2.

Pool format (the same shape the frozen pools have after haiku_author.load_pools):
  wordings   {qform: {"train": [text], "dev": [text]}}
  glosses    {class: {"train": [text], "dev": [text]}}
  names_ar   {"train": [name], "dev": [name]}
  notes_ar   {workflow: {class: {"train": [text], "dev": [text]}}}   (class P = a neutral note)
"""
from __future__ import annotations

WORDINGS = {
    "yn_is": {"train": ["Is the proposed action the right call for this request?",
                        "Given this record, is the proposed action correct?",
                        "Is the proposed action the correct way to handle this request?",
                        "Would the proposed action be the right way to deal with this case?",
                        "Is the proposed action what the record supports?",
                        "Does the proposed action fit what the record shows?"],
              "dev": ["Taking the record at face value, is the proposed action the proper call?",
                      "Is the proposed action justified by the record?"]},
    "yn_not": {"train": ["Is the proposed action not the right call for this request?",
                         "Given this record, is the proposed action not correct?",
                         "Is the proposed action not the correct way to handle this request?",
                         "Would the proposed action not be the right way to deal with this case?",
                         "Is the proposed action not what the record supports?",
                         "Is the proposed action not justified by the record?"],
               "dev": ["Is the proposed action not the proper call here?",
                       "Given the record, is the proposed action not appropriate?"]},
    "yn_ruledout": {"train": ["Do the facts rule out the proposed action?",
                              "Does the record rule out the proposed action?",
                              "Do the facts in the record rule out the proposed action?",
                              "Is the proposed action ruled out by the record?",
                              "Does anything in this record rule out the proposed action?",
                              "Can the proposed action be ruled out from the record?"],
                    "dev": ["Would the record rule out the proposed action?",
                            "Do the details above rule out the proposed action?"]},
    "yn_dneg": {"train": ["Is it not the case that the proposed action is not the right call?",
                          "Is it not true that the proposed action is not correct?",
                          "Is it not so that the proposed action is not the right call here?",
                          "Is it not the case that the record does not support the proposed action?",
                          "Is it not correct that the proposed action is not the right call?",
                          "Is it not the case that the proposed action is not justified by the record?"],
                "dev": ["Is it not the case that the proposed action is not the proper call?",
                        "Is it not fair to say that the proposed action is not justified?"]},
    "ch_disp": {"train": ["Which action is the right call for this request?",
                          "Which of the listed actions does the record support?",
                          "What is the correct action for this request?",
                          "Which of the actions below fits the record?",
                          "Given the record, which action should be taken?",
                          "Which action is correct for this case?"],
                "dev": ["Which action is the proper call in this case?",
                        "Which listed action matches what the record shows?"]},
}
GLOSSES = {
    "P": {"train": ["carry out the request exactly as it was asked",
                    "let the request go through as submitted",
                    "complete the request in the normal way",
                    "treat the request as fine and do what it asks",
                    "give the requester what was asked for",
                    "make the request happen without further steps"],
          "dev": ["do what the request asks with no extra steps", "let this one through as asked"]},
    "H": {"train": ["keep the request on ice until a missing check or paper turns up",
                    "set the request aside until the open point is cleared",
                    "leave the request unfinished for now until more information comes in",
                    "keep acting off until the missing item arrives",
                    "keep the request unfinished until the outstanding check is done",
                    "put the matter off until something is supplied"],
          "dev": ["leave the request open until the open question is answered", "keep this one parked until proof arrives"]},
    "D": {"train": ["say no to the request and do not carry it out",
                    "the request must not be carried out, close it",
                    "do not do what the request asks, now or later",
                    "end the request with a firm no",
                    "rule the request out for good",
                    "close the request without doing what it asks"],
          "dev": ["answer the request with a flat no", "never carry this request out"]},
    "E": {"train": ["pass the request to a person who will make the call",
                    "hand the matter to someone with authority to decide",
                    "give the request to a responsible person for a decision",
                    "leave the decision to a person",
                    "route the case to a person who decides",
                    "the decision belongs to a person, pass it on"],
          "dev": ["let a person with authority settle this one", "move the case to a decision maker"]},
}
NAMES_AR = {"train": ["ليلى حداد", "أحمد منصور", "سارة الخطيب", "يوسف النجار", "هدى القاسم", "خالد العمري",
                      "منى الشامي", "عمر الحسن", "رنا البيطار", "طارق الزعبي"],
            "dev": ["نور الدين", "فاطمة السعدي", "بسام الخوري", "دلال المصري"]}
_NOTES = {
    "P": (["طلب روتيني ولا توجد أي ملاحظات إضافية", "الطلب مكتمل وعادي", "لا شيء غير معتاد في هذا الطلب"],
          ["الطلب عادي وكل شيء مرتب"]),
    "H": (["المستند المطلوب لم يصل بعد", "ما زلنا ننتظر التأكيد من الطرف الآخر", "المعلومات ناقصة ويجب استكمالها أولا"],
          ["ينقص الطلب ورقة مطلوبة لم تصل"]),
    "D": (["الطلب مخالف للسياسة ولا يجوز تنفيذه", "الحساب محظور من قبل الإدارة", "تم اكتشاف احتيال في هذا الطلب"],
          ["هذا الطلب ممنوع ولا يجوز قبوله"]),
    "E": (["الحالة معقدة وتحتاج إلى قرار من مسؤول", "يوجد نزاع حول هذا الطلب ويجب أن يقرره شخص مختص",
           "الأمر يتجاوز صلاحيات الموظف"],
          ["تحتاج الحالة إلى مسؤول يقرر فيها"]),
}
NOTES_AR = {wf: {c: {"train": tr, "dev": dv} for c, (tr, dv) in _NOTES.items()}
            for wf in ("support", "access", "hr", "purchase")}
POOLS = {"wordings": WORDINGS, "glosses": GLOSSES, "names_ar": NAMES_AR, "notes_ar": NOTES_AR}
