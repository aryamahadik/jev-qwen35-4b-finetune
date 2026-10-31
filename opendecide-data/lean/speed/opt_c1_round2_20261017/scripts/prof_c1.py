import sys, os, time, json
sys.modules["fla"] = None
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ["OD_PAD_MULTIPLE"] = "64"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.expanduser("~/lean"))
import torch
torch.set_num_threads(int(sys.argv[1]))
import decoder_io as dio
BASE, REV = "Qwen/Qwen3.5-4B", "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a"; AD = os.path.expanduser("~/lean/models/q35_4b_main500k")
model, tok, info = dio.load(BASE, "cpu", adapter=AD, revision=REV, return_info=True); model = model.merge_and_unload(); model.eval()
opts = [f"label {i} - some description words here" for i in range(18)]
row = {"id": "x", "state": "Customer message:\nwake me up at nine am tomorrow", "instructions": "Which kind of smart-assistant request is this customer message?", "qtype": "choice", "options": opts, "card": None}
with torch.no_grad():
    dio.predict(model, tok, [row], batch_size=1, dev="cpu")
    t = time.time(); dio.predict(model, tok, [row], batch_size=1, dev="cpu"); print("one view", round(time.time() - t, 2), "s", flush=True)
    from torch.profiler import profile, ProfilerActivity
    with profile(activities=[ProfilerActivity.CPU]) as prof:
        dio.predict(model, tok, [row], batch_size=1, dev="cpu")
print(prof.key_averages().table(sort_by="self_cpu_time_total", row_limit=14, max_name_column_width=60))
