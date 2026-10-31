import sys,json,subprocess
from net import get,sha
def gh(p): return json.loads(subprocess.run(["gh","api",p],capture_output=True,text=True,check=True).stdout)
def info(repo,path=""):
    r=gh(f"repos/{repo}"); br=r["default_branch"]; c=gh(f"repos/{repo}/commits/{br}")
    print(f"## {repo} branch={br} commit={c['sha']} date={c['commit']['committer']['date']} api_license={(r.get('license') or {}).get('spdx_id')}")
    for f in gh(f"repos/{repo}/contents/{path}?ref={c['sha']}"):
        n=f['name']
        if f['type']=='file' and any(k in n.lower() for k in ('licen','copying','readme','notice')):
            b=get(f['download_url']); print(f"  FILE {f['path']} sha256={sha(b)} bytes={len(b)}")
            if 'licen' in n.lower() or 'copying' in n.lower(): print("   ---",b.decode('utf8','replace')[:250].replace('\n',' | '))
        else: print("  ",f['type'],f['path'])
for a in sys.argv[1:]:
    repo,_,p=a.partition(":")
    try: info(repo,p)
    except Exception as e: print(a,"ERR",str(e)[:200])
