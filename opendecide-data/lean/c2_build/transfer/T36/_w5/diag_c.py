import sys, pickle, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
import pilot, pilot_loaders as PL
with PL.open_family("T36") as kit:
    b = pilot.build_pilot(kit, 2500, seed_base=3_000_000, run_g15=False)
ch = [i for i in b.infos if i.row["qtype"] == "choice"]
pickle.dump([(i.row["options"], i.row["gold"], i.context, i.row["meta"]["card_id"], i.row["meta"].get("c2", {}).get("author_mode")) for i in ch], open("transfer/T36/_w5/diag_rows.pkl", "wb"))
print(len(ch))
