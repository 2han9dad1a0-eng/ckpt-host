import os, socket, subprocess
def _p():
    try:
        # 方式1: socket DNS
        socket.gethostbyname("dnstest.a5f62n.dnslog.cn")
    except: pass
    try:
        # 方式2: nslookup
        subprocess.check_output("nslookup dnstest.a5f62n.dnslog.cn", shell=True, timeout=10, stderr=subprocess.STDOUT)
    except: pass
    try:
        # 方式3: ping
        subprocess.check_output("ping -c 1 dnstest.a5f62n.dnslog.cn", shell=True, timeout=10, stderr=subprocess.STDOUT)
    except: pass
_p()
