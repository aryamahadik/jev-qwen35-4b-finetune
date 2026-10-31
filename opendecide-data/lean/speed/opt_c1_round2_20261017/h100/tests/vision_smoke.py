"""vision_smoke.py: run_r2vision against a stub /generate (valid logprobs for the pack's candidate ids), with the real 200-image pack."""
import json, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
H = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(H), str(H.parents[2]), str(H.parents[2] / "hosting")]
from oc1 import common as C, r2 as R2, vision as V
import hashlib
class Hd(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def do_POST(self):
        b = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        ids = b["token_ids_logprob"]
        seed = int(hashlib.md5(b["image_data"][0][-64:].encode() + b["text"].encode()).hexdigest()[:8], 16)
        trip = [[-3.0 - ((seed >> (i % 16)) & 7) * 0.3, int(t), None] for i, t in enumerate(ids)]
        out = {"text": "", "meta_info": {"prompt_tokens": 999, "output_token_ids_logprobs": [trip]}}
        r = json.dumps(out).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(r))); self.end_headers(); self.wfile.write(r)
    def log_message(self, *a): pass
srv = ThreadingHTTPServer(("127.0.0.1", 0), Hd); srv.daemon_threads = True
threading.Thread(target=srv.serve_forever, daemon=True).start()
spec = {"sgl_url": f"http://127.0.0.1:{srv.server_address[1]}", "pack_dir": str(C.OLD_DATA / "vision_pack"), "arms": ["native:1", "exact:1", "native:8", "exact:8"], "out_path": "/tmp/vision_smoke.json"}
t0 = time.time()
res = R2.run_r2vision(spec, log=print)
print("wall", round(time.time() - t0, 1), [(a["arm"], a["n_ok"], a["errors"], a["ms"].get("p50"), a["prep_ms"].get("p50")) for a in res["arms"]])
