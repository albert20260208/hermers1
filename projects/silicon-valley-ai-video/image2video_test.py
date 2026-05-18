#!/usr/bin/env python3
"""最小图生视频测试"""

import time
import requests
from volcenginesdkarkruntime import Ark

client = Ark(api_key="d380aed6-916e-4542-bd67-a20bbd1b377c")

# 生成场景图片
print("生成场景图片...")
scene_prompt = "Modern Silicon Valley tech office interview scene, cinematic composition, clean modern interior design, professional lighting"
try:
    img_resp = client.images.generate(
        model="doubao-seedream-5-0-260128",
        prompt=scene_prompt,
        size="2048x2048",
        response_format="url",
        watermark=False
    )
    
    if img_resp.data:
        img_url = img_resp.data[0].url
        print(f"图片生成成功: {img_url[:80]}...")
        
        # 下载图片（可选）
        img_data = requests.get(img_url).content
        with open("/tmp/scene_test.png", "wb") as f:
            f.write(img_data)
        print("图片已保存到 /tmp/scene_test.png")
        
        # 图生视频
        print("\n生成5秒视频...")
        video_task = client.content_generation.tasks.create(
            model="doubao-seedance-1-5-pro-251215",
            content=[
                {
                    "type": "image_url",
                    "image_url": {"url": img_url}
                },
                {
                    "type": "text",
                    "text": "Silicon Valley tech office interview scene, cinematic camera movement, professional lighting, modern interior"
                }
            ],
            extra_body={
                "duration": 5,
                "ratio": "16:9"
            }
        )
        
        task_id = video_task.id
        print(f"视频任务ID: {task_id}")
        
        # 等待完成
        for i in range(30):
            time.sleep(5)
            task = client.content_generation.tasks.get(task_id=task_id)
            print(f"状态检查 {i+1}: {task.status}")
            
            if task.status == "succeeded":
                video_url = task.content.video_url
                print(f"视频生成成功! URL: {video_url}")
                
                # 下载视频
                video_data = requests.get(video_url).content
                video_path = "/tmp/image2video_test.mp4"
                with open(video_path, "wb") as f:
                    f.write(video_data)
                print(f"视频已保存: {video_path}")
                break
            elif task.status == "failed":
                print("视频生成失败")
                break
        else:
            print("超时")
            
    else:
        print("图片生成失败")
        
except Exception as e:
    print(f"错误: {e}")