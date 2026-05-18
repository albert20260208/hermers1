#!/usr/bin/env python3
"""仅生成参考图片"""

import json
import time
import requests
from volcenginesdkarkruntime import Ark

client = Ark(api_key="d380aed6-916e-4542-bd67-a20bbd1b377c")

# 加载提示词
script_file = "/root/.openclaw/workspace/projects/silicon-valley-ai-video/outputs/script_analysis.json"
with open(script_file, "r", encoding="utf-8") as f:
    data = json.load(f)

prompts = {
    "killian": data["characters"]["killian"]["image_prompt"],
    "elara": data["characters"]["elara"]["image_prompt"],
    "scene": data["scene"]["scene_prompt"]
}

output_dir = "/root/.openclaw/workspace/projects/silicon-valley-ai-video/15s_video_output"
import os
os.makedirs(output_dir, exist_ok=True)

for name, prompt in prompts.items():
    print(f"生成{name}图片...")
    try:
        response = client.images.generate(
            model="doubao-seedream-5-0-260128",
            prompt=prompt,
            size="2048x2048",
            response_format="url",
            watermark=False
        )
        
        if response.data:
            url = response.data[0].url
            print(f"  成功，下载中...")
            img_resp = requests.get(url)
            if img_resp.status_code == 200:
                filename = f"{output_dir}/{name}_portrait.png"
                with open(filename, "wb") as f:
                    f.write(img_resp.content)
                print(f"  已保存: {filename}")
            else:
                print(f"  下载失败: {img_resp.status_code}")
        else:
            print(f"  生成失败")
    except Exception as e:
        print(f"  异常: {e}")
    
    time.sleep(1)

print("图片生成完成！")