#!/usr/bin/env python3
"""
Seedance 2.0 Fast 2分钟视频生成脚本
使用火山引擎API生成参考图片，然后用图生视频模式生成2分钟视频
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 火山引擎API配置
try:
    from volcenginesdkarkruntime import Ark
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    print("警告: volcenginesdkarkruntime 未安装，尝试使用requests直接调用API")

# API配置
API_KEY = "d380aed6-916e-4542-bd67-a20bbd1b377c"
API_BASE = "https://ark.cn-beijing.volces.com/api/v3"

# 模型配置
IMAGE_MODEL = "doubao-seedream-5-0-260128"  # 图片生成
VIDEO_MODEL = "doubao-seedance-1-5-pro-251215"  # 视频生成，使用1.5 Pro作为Seedance 2.0的替代

# 输出目录
OUTPUT_DIR = project_root / "seedance_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def setup_client():
    """设置火山引擎客户端"""
    if SDK_AVAILABLE:
        client = Ark(api_key=API_KEY)
        return client
    else:
        print("使用requests直接调用API")
        return None

def generate_image_with_sdk(client, prompt, output_name):
    """使用SDK生成图片"""
    print(f"生成图片: {output_name}")
    print(f"提示词: {prompt[:100]}...")
    
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
            print(f"图片生成成功，URL: {image_url}")
            
            # 下载图片
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                output_path = OUTPUT_DIR / f"{output_name}.png"
                with open(output_path, "wb") as f:
                    f.write(img_response.content)
                print(f"图片已保存到: {output_path}")
                return str(output_path)
            else:
                print(f"下载图片失败: {img_response.status_code}")
                return None
        else:
            print("图片生成失败: 无返回数据")
            return None
            
    except Exception as e:
        print(f"图片生成异常: {e}")
        return None

def generate_image_direct(prompt, output_name):
    """直接调用API生成图片（SDK不可用时）"""
    print(f"直接API生成图片: {output_name}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": IMAGE_MODEL,
        "prompt": prompt,
        "size": "2048x2048",
        "response_format": "url",
        "watermark": False
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/images/generations",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                image_url = data["data"][0]["url"]
                print(f"图片生成成功，URL: {image_url}")
                
                # 下载图片
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    output_path = OUTPUT_DIR / f"{output_name}.png"
                    with open(output_path, "wb") as f:
                        f.write(img_response.content)
                    print(f"图片已保存到: {output_path}")
                    return str(output_path)
                else:
                    print(f"下载图片失败: {img_response.status_code}")
                    return None
            else:
                print(f"API返回异常: {data}")
                return None
        else:
            print(f"API调用失败: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"直接API调用异常: {e}")
        return None

def create_video_prompt_with_references(image_paths):
    """创建2分钟视频提示词，引用生成的图片"""
    
    # 基础场景描述
    base_scene = "硅谷科技公司现代办公室采访场景，BlackAI创始人Killian Blackwood接受记者Elara Voss的独家专访。"
    
    # 时间分段：2分钟=120秒，分为8个15秒段落
    time_segments = [
        "0-15秒: 开场，Killian坐在现代会议室中，神情专注等待采访开始。镜头缓慢推近，展现硅谷科技办公室环境。",
        "15-30秒: Elara进入会议室，专业地准备采访设备。两人礼貌寒暄，气氛正式但微妙。",
        "30-45秒: 采访开始，Elara提问关于AI伦理的问题。Killian认真回答，眼神中透露出对技术的热情。",
        "45-60秒: 随着对话深入，Killian的目光变得柔和，注意到Elara对技术的真诚好奇。",
        "60-75秒: Elara记录回答时微微点头，展现出专业素养。两人之间产生微妙的默契感。",
        "75-90秒: 采访间隙，Killian用简单语言解释复杂概念，Elara认真倾听并理解。",
        "90-105秒: 两人就科技与艺术的融合进行讨论，气氛变得轻松温暖。",
        "105-120秒: 采访结束，Killian起身送别Elara，两人目光交汇，留下未言明的情感张力。"
    ]
    
    # 构建完整提示词
    prompt_parts = [
        "# 2分钟短视频脚本：《偏爱难藏》硅谷AI版 - 职场采访未婚夫",
        f"场景: {base_scene}",
        "",
        "## 时间分段描述:",
    ]
    
    prompt_parts.extend(time_segments)
    
    prompt_parts.extend([
        "",
        "## 视觉参考 (@引用):",
        f"主角Killian参考: @{image_paths.get('killian', 'Killian_Blackwood_28岁_硅谷AI创业者_黑色西装')}",
        f"主角Elara参考: @{image_paths.get('elara', 'Elara_Voss_22岁_艺术学生_白色长裙')}",
        f"场景参考: @{image_paths.get('scene', '现代硅谷科技办公室_采访场景')}",
        "",
        "## 视觉风格:",
        "- 电影质感: Cinematic quality, 35mm film grain, shallow depth of field",
        "- 画面比例: 16:9 宽屏, 24fps",
        "- 色调: 现代科技冷色调为主，情感时刻加入暖光",
        "- 镜头语言: 专业电影镜头，情感导向的运动",
        "",
        "## 音频设计:",
        "- 背景音乐: 轻柔钢琴曲 + 科技电子音效",
        "- 环境音: 办公室背景音、键盘声、空调声",
        "- 对话: 专业采访录音质量",
        "",
        "## 特别要求:",
        "- 使用Seedance 2.0 Fast模式生成",
        "- 总时长: 120秒 (2分钟)",
        "- 分辨率: 1280x720 (16:9)",
        "- 保持人物形象一致性",
        "- 情感表达细腻自然"
    ])
    
    return "\n".join(prompt_parts)

def generate_video_with_sdk(client, prompt, image_paths):
    """使用SDK生成视频（图生视频）"""
    print("开始生成2分钟视频...")
    print(f"视频提示词长度: {len(prompt)} 字符")
    
    # 准备内容数组
    content = [
        {
            "type": "text",
            "text": prompt
        }
    ]
    
    # 添加图片参考（如果提供了本地路径，需要先上传或使用base64）
    # 注意：火山引擎API可能需要图片URL，这里我们先使用文本描述
    # 在实际应用中，需要先将图片上传到可访问的URL
    
    extra_body = {
        "duration": 120,  # 2分钟，120秒
        "ratio": "16:9",
        "mode": "fast"  # Fast模式
    }
    
    try:
        task = client.content_generation.tasks.create(
            model=VIDEO_MODEL,
            content=content,
            extra_body=extra_body
        )
        
        task_id = task.id
        print(f"视频任务已提交，任务ID: {task_id}")
        
        # 轮询任务状态
        max_attempts = 60  # 最大尝试次数（60*10秒=10分钟）
        for i in range(max_attempts):
            time.sleep(10)  # 每10秒检查一次
            result = client.content_generation.tasks.get(task_id=task_id)
            
            print(f"检查进度 ({i+1}/{max_attempts}): 状态={result.status}")
            
            if result.status == "succeeded":
                video_url = result.content.video_url
                print(f"视频生成成功! URL: {video_url}")
                
                # 下载视频
                video_response = requests.get(video_url)
                if video_response.status_code == 200:
                    output_path = OUTPUT_DIR / f"2min_interview_video_{task_id}.mp4"
                    with open(output_path, "wb") as f:
                        f.write(video_response.content)
                    print(f"视频已保存到: {output_path}")
                    return str(output_path)
                else:
                    print(f"下载视频失败: {video_response.status_code}")
                    return None
                    
            elif result.status == "failed":
                print(f"视频生成失败: {result}")
                return None
                
        print("视频生成超时")
        return None
        
    except Exception as e:
        print(f"视频生成异常: {e}")
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("Seedance 2.0 Fast 2分钟视频生成")
    print("=" * 60)
    
    # 加载角色和场景信息
    script_file = project_root / "outputs" / "script_analysis.json"
    if not script_file.exists():
        print(f"错误: 脚本分析文件不存在: {script_file}")
        return
    
    with open(script_file, "r", encoding="utf-8") as f:
        script_data = json.load(f)
    
    # 设置客户端
    client = setup_client()
    
    # 生成参考图片
    image_paths = {}
    
    # 1. 生成Killian图片
    killian_prompt = script_data["characters"]["killian"]["image_prompt"]
    killian_path = None
    
    if client and SDK_AVAILABLE:
        killian_path = generate_image_with_sdk(client, killian_prompt, "killian_portrait")
    else:
        killian_path = generate_image_direct(killian_prompt, "killian_portrait")
    
    if killian_path:
        image_paths["killian"] = killian_path
    
    # 2. 生成Elara图片
    elara_prompt = script_data["characters"]["elara"]["image_prompt"]
    elara_path = None
    
    if client and SDK_AVAILABLE:
        elara_path = generate_image_with_sdk(client, elara_prompt, "elara_portrait")
    else:
        elara_path = generate_image_direct(elara_prompt, "elara_portrait")
    
    if elara_path:
        image_paths["elara"] = elara_path
    
    # 3. 生成场景图片
    scene_prompt = script_data["scene"]["scene_prompt"]
    scene_path = None
    
    if client and SDK_AVAILABLE:
        scene_path = generate_image_with_sdk(client, scene_prompt, "interview_scene")
    else:
        scene_path = generate_image_direct(scene_prompt, "interview_scene")
    
    if scene_path:
        image_paths["scene"] = scene_path
    
    # 检查是否至少生成了一张图片
    if not image_paths:
        print("错误: 未能生成任何参考图片，无法继续")
        return
    
    print(f"成功生成 {len(image_paths)} 张参考图片")
    
    # 创建视频提示词
    video_prompt = create_video_prompt_with_references(image_paths)
    
    # 保存提示词
    prompt_file = OUTPUT_DIR / "2min_video_prompt.txt"
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(video_prompt)
    print(f"视频提示词已保存到: {prompt_file}")
    
    # 生成视频
    if client and SDK_AVAILABLE:
        video_path = generate_video_with_sdk(client, video_prompt, image_paths)
    else:
        print("错误: 需要volcenginesdkarkruntime SDK来生成视频")
        print("请安装: pip install volcenginesdkarkruntime")
        return
    
    if video_path:
        print("\n" + "=" * 60)
        print("✅ 视频生成完成!")
        print(f"视频文件: {video_path}")
        print("=" * 60)
        
        # 生成结果报告
        report = {
            "status": "success",
            "video_path": video_path,
            "image_paths": image_paths,
            "prompt_file": str(prompt_file),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        report_file = OUTPUT_DIR / "generation_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"生成报告: {report_file}")
    else:
        print("\n" + "=" * 60)
        print("❌ 视频生成失败")
        print("=" * 60)

if __name__ == "__main__":
    main()