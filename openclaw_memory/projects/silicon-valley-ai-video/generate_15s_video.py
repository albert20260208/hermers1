#!/usr/bin/env python3
"""
生成15秒视频脚本
1. 使用火山引擎API生成3张参考图片
2. 使用Dreamina CLI multimodal2video生成15秒视频
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from volcenginesdkarkruntime import Ark

# 配置
API_KEY = "d380aed6-916e-4542-bd67-a20bbd1b377c"
IMAGE_MODEL = "doubao-seedream-5-0-260128"

# 目录
project_root = Path(__file__).parent
output_dir = project_root / "15s_video_output"
output_dir.mkdir(exist_ok=True)

# 初始化客户端
client = Ark(api_key=API_KEY)

def generate_image_and_save(prompt, filename):
    """使用火山引擎生成图片并保存到本地"""
    print(f"生成图片: {filename}")
    
    try:
        response = client.images.generate(
            model=IMAGE_MODEL,
            prompt=prompt,
            size="2048x2048",
            response_format="url",
            watermark=False
        )
        
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            print(f"  图片URL: {image_url[:80]}...")
            
            # 下载图片
            import requests
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                filepath = output_dir / filename
                with open(filepath, "wb") as f:
                    f.write(img_response.content)
                print(f"  图片已保存: {filepath}")
                return str(filepath)
            else:
                print(f"  下载失败: {img_response.status_code}")
                return None
        else:
            print("  生成失败: 无返回数据")
            return None
            
    except Exception as e:
        print(f"  异常: {e}")
        return None

def load_prompts():
    """加载图片提示词"""
    script_file = project_root / "outputs" / "script_analysis.json"
    with open(script_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    prompts = {
        "killian": data["characters"]["killian"]["image_prompt"],
        "elara": data["characters"]["elara"]["image_prompt"],
        "scene": data["scene"]["scene_prompt"]
    }
    
    # 简化提示词
    simplified = {}
    for key, prompt in prompts.items():
        # 提取关键部分
        parts = prompt.split(',')
        if len(parts) > 5:
            simplified[key] = ','.join(parts[-5:])  # 取最后5个部分
        else:
            simplified[key] = prompt
    
    return simplified

def create_video_prompt():
    """创建15秒视频提示词（小邱格式）"""
    prompt = """
# 《偏爱难藏》硅谷AI版 - 职场采访未婚夫
## 15秒短视频脚本

### 时间分段:
0-5秒: Killian坐在现代会议室等待采访，神情专注。镜头缓慢推近，展现硅谷科技办公室环境。
5-10秒: Elara进入会议室准备采访，两人礼貌寒暄，气氛正式但微妙。
10-15秒: 采访开始，Elara提问，Killian回答，两人目光交流中透露出微妙情感。

### 视觉风格:
- 电影质感: 35mm胶片颗粒，浅景深，宽银幕比例 (2.35:1)
- 色调: 现代科技冷色调为主，情感时刻加入暖光
- 镜头语言: 专业电影镜头，情感导向的运动

### 音频设计:
- 背景音乐: 轻柔钢琴曲 + 科技电子音效
- 环境音: 办公室背景音
- 对话: 专业采访录音质量

### 人物一致性:
- 参考生成的Killian和Elara肖像图片
- 保持人物形象与参考图片一致
"""
    return prompt.strip()

def run_dreamina_video(image_paths, prompt):
    """运行Dreamina CLI生成视频"""
    print("\n🎬 使用Dreamina生成15秒视频...")
    
    # 构建命令
    cmd = [
        "dreamina", "multimodal2video",
        "--model_version=seedance2.0fast",
        "--duration=15",
        "--ratio=16:9",
        f"--prompt={prompt}",
        "--poll=60"
    ]
    
    # 添加图片参数
    for img_path in image_paths:
        cmd.append(f"--image={img_path}")
    
    print(f"执行命令: {' '.join(cmd[:6])}...")
    
    try:
        # 执行命令
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
            encoding="utf-8"
        )
        
        print("Dreamina输出:")
        print(result.stdout)
        
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        if result.returncode == 0:
            # 尝试从输出中提取submit_id
            import re
            match = re.search(r'"submit_id"\s*:\s*"([^"]+)"', result.stdout)
            if match:
                submit_id = match.group(1)
                print(f"✅ 视频任务提交成功! submit_id: {submit_id}")
                return submit_id
            else:
                print("⚠️ 未找到submit_id，但命令执行成功")
                return "unknown"
        else:
            print(f"❌ Dreamina命令失败，返回码: {result.returncode}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Dreamina命令超时")
        return None
    except Exception as e:
        print(f"❌ 执行Dreamina命令异常: {e}")
        return None

def query_dreamina_result(submit_id):
    """查询Dreamina任务结果"""
    print(f"\n⏳ 查询任务结果: {submit_id}")
    
    cmd = ["dreamina", "query_result", f"--submit_id={submit_id}"]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8"
        )
        
        print("查询结果:")
        print(result.stdout)
        
        if result.stderr:
            print("错误:")
            print(result.stderr)
        
        # 尝试解析JSON
        try:
            data = json.loads(result.stdout)
            if data.get("gen_status") == "success":
                print("✅ 视频生成成功!")
                # 提取视频URL或文件路径
                # 注意: Dreamina可能返回文件路径或URL
                return data
            else:
                print(f"状态: {data.get('gen_status')}")
                return data
        except:
            return {"raw_output": result.stdout}
            
    except Exception as e:
        print(f"查询异常: {e}")
        return None

def main():
    print("=" * 60)
    print("15秒视频生成流程")
    print("=" * 60)
    
    # 加载提示词
    print("\n📝 加载提示词...")
    prompts = load_prompts()
    
    # 生成图片
    print("\n📷 生成参考图片...")
    image_files = []
    
    # Killian图片
    killian_path = generate_image_and_save(
        prompts["killian"],
        "killian_portrait.png"
    )
    if killian_path:
        image_files.append(killian_path)
        time.sleep(1)  # 短暂间隔
    
    # Elara图片
    elara_path = generate_image_and_save(
        prompts["elara"],
        "elara_portrait.png"
    )
    if elara_path:
        image_files.append(elara_path)
        time.sleep(1)
    
    # 场景图片
    scene_path = generate_image_and_save(
        prompts["scene"],
        "interview_scene.png"
    )
    if scene_path:
        image_files.append(scene_path)
    
    if len(image_files) < 2:
        print("❌ 图片生成不足，无法继续")
        return
    
    print(f"\n✅ 生成 {len(image_files)} 张参考图片")
    
    # 创建视频提示词
    video_prompt = create_video_prompt()
    prompt_file = output_dir / "video_prompt.txt"
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(video_prompt)
    print(f"📝 视频提示词已保存: {prompt_file}")
    
    # 生成视频
    submit_id = run_dreamina_video(image_files, video_prompt)
    
    if submit_id and submit_id != "unknown":
        # 查询结果
        time.sleep(10)  # 等待一段时间
        result = query_dreamina_result(submit_id)
        
        # 保存结果
        result_file = output_dir / f"result_{submit_id}.json"
        with open(result_file, "w", encoding="utf-8") as f:
            json.dump({
                "submit_id": submit_id,
                "image_files": image_files,
                "prompt_file": str(prompt_file),
                "query_result": result,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }, f, ensure_ascii=False, indent=2)
        print(f"📊 结果已保存: {result_file}")
    
    print("\n" + "=" * 60)
    print("流程完成")
    print("=" * 60)

if __name__ == "__main__":
    main()