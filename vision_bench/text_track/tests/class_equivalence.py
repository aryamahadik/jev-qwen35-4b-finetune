"""Scratch: does AutoModelForCausalLM load the real Qwen3.5-4B snapshot without missing keys, and does a text-only forward
through the text-only class (native adapter) equal the multimodal class (renamed adapter)? CPU, bf16."""
import os, sys, json, time, glob, gc
os.environ["HF_HUB_OFFLINE"]="1"; os.environ["TRANSFORMERS_OFFLINE"]="1"
sys.path.insert(0,"/Users/aryamahadik/Documents/jev/vision_bench/harness"); sys.path.insert(0,"/Users/aryamahadik/Documents/jev/vision_bench/harness/vendor")
import torch
torch.set_num_threads(8)
import vb_core as vb
from vb_core import dio
SNAP=glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/*"))[0]
AD="/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"
mode=sys.argv[1]
info=dio.resolve_prompt([AD],"Qwen/Qwen3.5-4B","schema_branch_mark","cygnet",vb.REVISION)
dio.LAYOUT,dio.STYLE=info["layout"],info["style"]
tok=dio.load_tokenizer("Qwen/Qwen3.5-4B",adapter=AD,revision=vb.REVISION)
ro=dio.Readout(tok)
rows=[]
rows.append({"state":'{\n "review": "A gorgeous, witty, seductive movie."\n}',"instructions":"Does `review` express a positive opinion of the movie?","qtype":"noul","options":None})
rows.append({"state":'{\n "article": "Wall St. Bears Claw Back Into the Black"\n}',"instructions":"What is the topic of `article`?","qtype":"choice","options":["world","sports","business","sci_tech"],"card":"- world: world news\n- sports: sports\n- business: business, markets\n- sci_tech: science and technology"})
rows.append({"state":'{\n "review": "meh, not terrible"\n}',"instructions":"How positive is the sentiment of `review`?","qtype":"choice","options":["0: very negative review","1: negative review","2: neutral or mixed review","3: positive review","4: very positive review"]})
out={}
t0=time.time()
if mode=="text":
    from transformers import AutoModelForCausalLM
    from peft import PeftModel
    m,li=AutoModelForCausalLM.from_pretrained(SNAP,dtype=torch.bfloat16,attn_implementation="sdpa",output_loading_info=True)
    print("class",type(m).__name__,"loading_info",{k:(len(v) if hasattr(v,'__len__') else v) for k,v in li.items()},flush=True)
    print("missing sample",list(li.get("missing_keys",[]))[:5],"unexpected sample",list(li.get("unexpected_keys",[]))[:5],flush=True)
    pm=PeftModel.from_pretrained(m,AD)
    sd=__import__("safetensors.torch",fromlist=["load_file"]).load_file(AD+"/adapter_model.safetensors")
    chk=vb.verify_adapter_loaded(pm,sd,496,248); print("adapter check (native keys)",chk,flush=True)
    base=pm.get_base_model(); body,head=base.model,base.lm_head
else:
    from transformers import AutoModelForImageTextToText
    m=AutoModelForImageTextToText.from_pretrained(SNAP,dtype=torch.bfloat16,attn_implementation="sdpa")
    pm,chk=vb.attach_c1_adapter(m,AD,"/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/34eb204a-5e87-45ca-91e0-3859655d8ad7/scratchpad/renamed",496,248); print("adapter check (renamed)",chk,flush=True)
    base=pm.get_base_model(); body,head=base.model,base.lm_head
print("load s",time.time()-t0,flush=True)
pm.eval()
res=[]
with torch.no_grad():
    for r in rows:
        for perm in vb.views_for(r) if False else [None]:
            txt=dio.prompt_texts(ro,[r],[perm])[0]
            ids=tok([txt],add_special_tokens=False,return_tensors="pt")
            hs=body(input_ids=ids["input_ids"],attention_mask=ids["attention_mask"]).last_hidden_state
            h=hs[0,-1]; groups=ro.cand(r); flat=[t for g in groups for t in g]
            lg=h.float()@head.weight[flat].float().T
            parts=[];k=0
            for g in groups: parts.append(torch.logsumexp(lg[k:k+len(g)],0)); k+=len(g)
            res.append(torch.stack(parts).tolist()); print(r["qtype"],len(ids["input_ids"][0]),res[-1],flush=True)
json.dump(res,open(f"/private/tmp/claude-501/-Users-aryamahadik-Documents-jev/34eb204a-5e87-45ca-91e0-3859655d8ad7/scratchpad/cls_{mode}.json","w"))
print("done",time.time()-t0)
