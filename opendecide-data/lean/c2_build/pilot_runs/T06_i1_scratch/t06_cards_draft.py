import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from c2_kit import cards as CD

H = lambda s: (s, s, s)
STYLES = {
"act": [
 H("Consumer Sales Act of {JURIS} (excerpt)"),
 ("Section I (counting days). A right is used on the day the buyer asks for it. A period in this Act or in a store notice runs in calendar days from an event: the event's day is day zero, the next day is day one, and the period includes its last day.",
  "Section I (counting days). A right is used on the day the buyer asks for it. Periods in this Act or in a store notice run in calendar days from an event: the event's day is day zero, and the last day counts.",
  "I. A right is used on the day the buyer asks for it. Periods in this Act or in a store notice are calendar days from an event: the event's day is day zero, the last day counts."),
 ("Section II (faulty goods). A buyer may reject faulty goods and get a full refund within {N_REJ} from the delivery date.",
  "Section II (faulty goods). A buyer may reject faulty goods and get a full refund within {N_REJ} of delivery.",
  "II. A buyer may reject faulty goods for a full refund within {N_REJ} of delivery."),
 ("Section III (withdrawal). A buyer may withdraw from a purchase for any reason and get a full refund within {N_WD} from the day the buyer took possession of the goods. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.",
  "Section III (withdrawal). A buyer may withdraw for any reason and get a full refund within {N_WD} from the day the buyer took possession. Section III does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit Section II.",
  "III. A buyer may withdraw for any reason for a full refund within {N_WD} of taking possession. It does not cover goods made to the buyer's specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions do not limit II."),
 ("Section IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.",
  "Section IV (store notices). A store notice cannot remove or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.",
  "IV. A store notice cannot remove or shorten these rights. A store may promise more; a full refund its posted notice promises is owed."),
],
"code": [
 H("Civil Code of {JURIS}, consumer sales, Article K (extract)"),
 ("(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the next day is day one, and the final day of the limit still counts.",
  "(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, and the final day still counts.",
  "(a) A right is exercised on the day the buyer requests it. A time limit here or in a seller's notice counts calendar days from an event: the event's day is day zero, the final day still counts."),
 ("(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts {N_REJ}, counted from the date of delivery.",
  "(b) A buyer of faulty goods may reject them and be refunded in full; this right lasts {N_REJ} from the date of delivery.",
  "(b) A buyer may reject faulty goods and be refunded in full; the right lasts {N_REJ} from delivery."),
 ("(c) A buyer may withdraw from a purchase for any reason and be refunded in full; this right lasts {N_WD}, counted from the date the buyer took possession of the goods.",
  "(c) A buyer may withdraw for any reason and be refunded in full; this right lasts {N_WD} from the date the buyer took possession.",
  "(c) A buyer may withdraw for any reason and be refunded in full; the right lasts {N_WD} from taking possession."),
 ("(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.",
  "(d) Paragraph (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. Paragraph (b) has no exclusions.",
  "(d) (c) excludes goods made to the buyer's specification, perishable goods, and sealed hygiene goods whose seal was broken after delivery. (b) has no exclusions."),
 ("(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.",
  "(e) A seller's notice cannot remove or shorten these rights. A seller may promise more, and a full refund its posted notice promises is owed.",
  "(e) A seller's notice cannot remove or shorten these rights. A seller may promise more; a full refund its posted notice promises is owed."),
],
"charter": [
 H("Buyer's Rights Charter of {JURIS} (summary every store must display)"),
 ("- Counting days: you use a right on the day you ask for it. Periods count calendar days: a period's event day is day zero, the next day is day one, and the last day of the period still counts. Store notices count days the same way.",
  "- Counting days: you use a right on the day you ask for it. Periods count calendar days: a period's event day is day zero, and the last day still counts. Store notices count days the same way.",
  "- Counting: you use a right on the day you ask for it. Periods are calendar days: the event day is day zero, the last day still counts. Store notices count the same way."),
 ("- Faulty-goods rule: you can reject faulty goods and get a full refund within {N_REJ} from the day they were delivered.",
  "- Faulty-goods rule: you can reject faulty goods and get a full refund within {N_REJ} from the day they were delivered.",
  "- Faulty-goods rule: you can reject faulty goods for a full refund within {N_REJ} of delivery."),
 ("- Cooling-off rule: for any reason, you can withdraw from a purchase and get a full refund within {N_WD} from the day you took possession of the goods. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery. These exclusions never limit the faulty-goods rule.",
  "- Cooling-off rule: for any reason, you can withdraw and get a full refund within {N_WD} from the day you took possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery. These exclusions never limit the faulty-goods rule.",
  "- Cooling-off rule: for any reason, you can withdraw for a full refund within {N_WD} of taking possession. It does not cover goods made to your specification, perishable goods, or sealed hygiene goods whose seal was broken after delivery; these exclusions never limit the faulty-goods rule."),
 ("- Store notices: a store notice cannot take away or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.",
  "- Store notices: a store notice cannot take away or shorten these rights. A store may promise more, and a full refund its posted notice promises is owed.",
  "- Store notices: a store notice cannot take away or shorten these rights. A store may promise more; a full refund its posted notice promises is owed."),
],
}
tok = CD._tokenizer()[1]
def n(s): return len(tok.encode(s, add_special_tokens=False).ids)
tot = {0:0,1:0,2:0}
for sname, items in STYLES.items():
    row = []
    for idx, name in ((0,'full'),(1,'compact'),(2,'short')):
        txt = "\n".join(it[idx] for it in items)
        row.append(n(txt)); tot[idx]+=n(txt)
    print(sname, row)
    for it in items[1:]:
        for j in (1,2):
            pr = CD.variant_problems(it[0], it[j])
            if pr: print(sname, j, it[j][:40], pr)
print({k: v/3 for k,v in tot.items()})
