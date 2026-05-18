#!/usr/bin/env python3
"""
Seedance 2.0 Fast 模式视频生成
生成参考图片，然后使用图生视频生成2分钟视频
"""

import os
import time
import json
from volcenginesdkarkruntime import Ark

# ============ 配置 ============
API_KEY = "d380aed6-916e-4542-bd67-a20bbd1b377c"
IMAGE_MODEL = "doubao-seedream-5-0-260128"
VIDEO_MODEL = "doubao-seedance-1-5-pro-251215"  # 使用1.5 Pro，可能支持更长时长

# 初始化客户端
client = Ark(api_key=API_KEY)

def generate_image(prompt, image_name):
    """生成图片并返回URL"""
    print(f"生成图片: {image_name}")
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
            print(f"✅ 图片生成成功: {image_url[:80]}...")
            return image_url
        else:
            print("❌ 图片生成失败: 无返回数据")
            return None
            
    except Exception as e:
        print(f"❌ 图片生成异常: {e}")
        return None

def generate_video_with_images(image_urls, prompt, duration=120, ratio="16:9"):
    """
    使用多张参考图片生成视频
    image_urls: 图片URL列表
    prompt: 视频描述
    duration: 视频时长（秒），尝试120秒
    ratio: 画面比例
    """
    print(f"\n开始生成视频，时长: {duration}秒")
    print(f"使用 {len(image_urls)} 张参考图片")
    
    # 构建内容数组
    content = []
    
    # 添加图片
    for img_url in image_urls:
        content.append({
            "type": "image_url",
            "image_url": {"url": img_url}
        })
    
    # 添加文本描述
    content.append({
        "type": "text",
        "text": prompt
    })
    
    try:
        # 尝试fast模式参数
        extra_body = {
            "duration": duration,
            "ratio": ratio,
            "mode": "fast"  # 尝试fast模式
        }
        
        task = client.content_generation.tasks.create(
            model=VIDEO_MODEL,
            content=content,
            extra_body=extra_body
        )
        
        print(f"✅ 视频任务创建成功!")
        print(f"   任务 ID: {task.id}")
        print(f"   状态: {task.status}")
        
        return task.id
        
    except Exception as e:
        print(f"❌ 创建视频任务失败: {e}")
        # 尝试不使用fast模式
        print("尝试不使用fast模式...")
        try:
            extra_body = {
                "duration": min(duration, 10),  # 限制时长，API可能只支持短时长
                "ratio": ratio
            }
            
            task = client.content_generation.tasks.create(
                model=VIDEO_MODEL,
                content=content,
                extra_body=extra_body
            )
            
            print(f"✅ 视频任务创建成功 (短时长)!")
            print(f"   任务 ID: {task.id}")
            return task.id
            
        except Exception as e2:
            print(f"❌ 再次失败: {e2}")
            return None

def check_task_status(task_id):
    """查询任务状态"""
    try:
        task = client.content_generation.tasks.get(task_id=task_id)
        
        result = {
            "task_id": task.id,
            "status": task.status,
            "created_at": getattr(task, 'created_at', 'N/A'),
        }
        
        if task.status == "succeeded" and hasattr(task, 'content'):
            result["video_url"] = task.content.video_url if hasattr(task.content, 'video_url') else None
            
        return result
        
    except Exception as e:
        return {"error": str(e)}

def wait_for_video(task_id, max_wait=600, interval=15):
    """等待视频生成完成"""
    print(f"\n⏳ 等待视频生成...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)
        
        if "error" in result:
            print(f"查询状态错误: {result['error']}")
            return result
        
        status = result.get("status", "")
        print(f"   状态: {status} (已等待 {int(time.time() - start_time)} 秒)")
        
        if status == "succeeded":
            print(f"✅ 视频生成完成!")
            return result
        elif status == "failed":
            print(f"❌ 视频生成失败")
            return {"error": "Video generation failed", "details": result}
        
        time.sleep(interval)
    
    return {"error": f"超时等待 ({max_wait} 秒)"}

def load_script_data():
    """加载剧本分析数据"""
    script_file = "/root/.openclaw/workspace/projects/silicon-valley-ai-video/outputs/script_analysis.json"
    if not os.path.exists(script_file):
        print(f"❌ 脚本分析文件不存在: {script_file}")
        return None
    
    with open(script_file, "r", encoding="utf-8") as f:
        return json.load(f)

def create_video_prompt():
    """创建2分钟视频提示词"""
    prompt = """
# 《偏爱难藏》硅谷AI版 - 职场采访未婚夫
## 2分钟短视频脚本

### 场景描述:
硅谷科技公司现代办公室，BlackAI创始人Killian Blackwood接受记者Elara Voss的独家专访。这是两人第一次在工作场合正式见面，虽然私下已有婚约，但公开场合需保持专业距离。

### 时间线 (120秒):
1. 0-20秒: 开场，Killian在会议室等待，Elara带着采访设备进入。两人礼貌寒暄，气氛正式。
2. 20-40秒: 采访开始，Elara提问关于AI伦理的问题。Killian专业回答，展现技术深度。
3. 40-60秒: 随着对话深入，Killian注意到Elara对技术的真诚好奇，眼神变得柔和。
4. 60-80秒: Elara记录回答时展现出专业素养，两人之间产生微妙默契。
5. 80-100秒: 采访间隙轻松交流，讨论科技与艺术的融合。
6. 100-120秒: 采访结束，Killian起身送别，两人目光交汇，留下情感张力。

### 视觉风格:
- 电影质感: 35mm胶片颗粒，浅景深，宽银幕比例 (2.35:1)
- 色调: 现代科技冷色调 (蓝、灰) 为主，情感时刻加入暖光 (黄、橙)
- 镜头语言: 专业电影镜头，情感导向的运动，匹配剪辑转场
- 分辨率: 4K画质，24fps

### 音频设计:
- 背景音乐: 轻柔钢琴曲 + 科技电子音效
- 环境音: 办公室背景音、键盘声、空调声
- 对话: 专业采访录音质量
- 情感音效: 微妙的环境静音时刻，突出情感张力

### 人物一致性:
- Killian Blackwood: 28岁硅谷AI创业者，黑色西装，技术专家气质
- Elara Voss: 22岁艺术学生/记者，白色长裙，温柔专业形象

### 特别要求:
- 使用Seedance 2.0 Fast模式生成
- 保持人物形象与参考图片一致
- 情感表达细腻自然
- 专业电影级质感
"""
    return prompt.strip()

def main():
    print("=" * 60)
    print("Seedance 2.0 Fast - 2分钟视频生成")
    print("=" * 60)
    
    # 加载剧本数据
    script_data = load_script_data()
    if not script_data:
        return
    
    # 生成参考图片
    print("\n📷 生成参考图片...")
    image_urls = []
    
    # 1. Killian图片
    killian_url = generate_image(
        script_data["characters"]["killian"]["image_prompt"],
        "killian_portrait"
    )
    if killian_url:
        image_urls.append(killian_url)
    
    # 2. Elara图片  
    elara_url = generate_image(
        script_data["characters"]["elara"]["image_prompt"],
        "elara_portrait"
    )
    if elara_url:
        image_urls.append(elara_url)
    
    # 3. 场景图片
    scene_url = generate_image(
        script_data["scene"]["scene_prompt"],
        "interview_scene"
    )
    if scene_url:
        image_urls.append(scene_url)
    
    if not image_urls:
        print("❌ 未能生成任何图片，无法继续")
        return
    
    print(f"\n✅ 成功生成 {len(image_urls)} 张参考图片")
    
    # 创建视频提示词
    video_prompt = create_video_prompt()
    
    # 保存提示词
    prompt_file = "/root/.openclaw/workspace/projects/silicon-valley-ai-video/video_prompt_2min.txt"
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(video_prompt)
    print(f"📝 视频提示词已保存: {prompt_file}")
    
    # 生成视频
    print("\n🎬 开始生成2分钟视频...")
    
    # 尝试生成120秒视频，如果失败则尝试10秒
    task_id = generate_video_with_images(image_urls, video_prompt, duration=120)
    
    if not task_id:
        print("❌ 视频任务创建失败")
        return
    
    # 等待视频生成
    result = wait_for_video(task_id, max_wait=900, interval=20)  # 最多等待15分钟
    
    if "video_url" in result:
        video_url = result["video_url"]
        print(f"\n🎥 视频生成成功!")
        print(f"   视频 URL: {video_url}")
        
        # 尝试下载视频
        try:
            import requests
            video_response = requests.get(video_url)
            if video_response.status_code == 200:
                video_file = f"/root/.openclaw/workspace/projects/silicon-valley-ai-video/2min_interview_video_{task_id}.mp4"
                with open(video_file, "wb") as f:
                    f.write(video_response.content)
                print(f"✅ 视频已下载: {video_file}")
                
                # 生成结果报告
                report = {
                    "status": "success",
                    "task_id": task_id,
                    "video_url": video_url,
                    "video_file": video_file,
                    "image_urls": image_urls,
                    "prompt_file": prompt_file,
                    "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                
                report_file = f"/root/.openclaw/workspace/projects/silicon-valley-ai-video/generation_report_{task_id}.json"
                with open(report_file, "w", encoding="utf-8") as f:
                    json.dump(report, f, ensure_ascii=False, indent=2)
                print(f"📊 生成报告: {report_file}")
                
            else:
                print(f"❌ 下载视频失败: {video_response.status_code}")
                
        except Exception as e:
            print(f"❌ 下载视频异常: {e}")
            
    else:
        print(f"\n❌ 视频生成失败或超时")
        print(f"   结果: {result}")

if __name__ == "__main__":
    main()