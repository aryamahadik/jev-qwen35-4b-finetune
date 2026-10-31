import ssl,urllib.request,json,hashlib
CTX=ssl.create_default_context(cafile="/etc/ssl/cert.pem")
def get(url,timeout=60):
    req=urllib.request.Request(url,headers={"User-Agent":"c2-di-ts/1.0"})
    return urllib.request.urlopen(req,timeout=timeout,context=CTX).read()
def gj(url): return json.loads(get(url))
def sha(b): return hashlib.sha256(b).hexdigest()
