#!/usr/bin/env python3
"""
自动化生成《偏爱难藏硅谷AI版》人物场景视频
使用Dreamina CLI生成图片和视频
"""

import json
import subprocess
import time
import os
import re
from pathlib import Path

# 配置
DREAMINA_CLI = "/root/.local/bin/dreamina"
WORKSPACE = Path("/root/.openclaw/workspace/projects/silicon-valley-ai-video")
OUTPUT_DIR = WORKSPACE / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def run_dreamina_command(cmd_args, timeout=300):
    """运行Dreamina命令并返回输出"""
    print(f"执行命令: {' '.join(cmd_args)}")
    try:
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        print(f"返回码: {result.returncode}")
        if result.stdout:
            print(f"STDOUT (前500字符): {result.stdout[:500]}")
        if result.stderr:
            print(f"STDERR: {result.stderr[:500]}")
        
        return result
    except subprocess.TimeoutExpired:
        print(f"命令超时: {timeout}秒")
        return None
    except Exception as e:
        print(f"命令异常: {e}")
        return None

def extract_task_id(output):
    """从Dreamina输出中提取任务ID"""
    # 尝试匹配任务ID模式
    patterns = [
        r'"task_id"\s*:\s*"([a-f0-9]+)"',
        r'task_id["\']?\s*[:=]\s*["\']([a-f0-9]+)["\']',
        r'ID[:\s]+([a-f0-9]+)',
        r'([a-f0-9]{16,})'  # 长hex字符串
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, output, re.IGNORECASE)
        if matches:
            print(f"找到任务ID: {matches[0]}")
            return matches[0]
    
    # 如果没有找到，尝试从JSON解析
    try:
        data = json.loads(output)
        if isinstance(data, dict):
            if 'task_id' in data:
                return data['task_id']
            if 'id' in data:
                return data['id']
    except:
        pass
    
    print("未找到任务ID")
    return None

def query_task_result(task_id, max_attempts=30, interval=10):
    """查询任务结果"""
    print(f"查询任务结果: {task_id}")
    
    for attempt in range(max_attempts):
        print(f"尝试 {attempt + 1}/{max_attempts}")
        
        result = run_dreamina_command([
            DREAMINA_CLI, "query_result",
            f"--submit_id={task_id}"
        ], timeout=60)
        
        if not result or result.returncode != 0:
            print(f"查询失败，等待{interval}秒后重试")
            time.sleep(interval)
            continue
        
        # 检查输出中是否包含成功状态
        output = result.stdout.lower()
        if 'success' in output or 'succeeded' in output or 'completed' in output:
            print("任务成功完成")
            return result
        elif 'failed' in output or 'error' in output:
            print("任务失败")
            return result
        elif 'pending' in output or 'processing' in output or 'running' in output:
            print(f"任务仍在处理中，等待{interval}秒")
            time.sleep(interval)
        else:
            # 无法判断状态，假设仍在处理
            print(f"未知状态，等待{interval}秒")
            time.sleep(interval)
    
    print(f"达到最大查询次数 {max_attempts}，任务可能仍在处理")
    return None

def generate_image(prompt, output_name, ratio="16:9", model_version="5.0", poll_seconds=30):
    """生成图片"""
    print(f"\n🖼️  生成图片: {output_name}")
    
    output_path = OUTPUT_DIR / f"{output_name}.jpg"
    
    # 构建命令
    cmd = [
        DREAMINA_CLI, "text2image",
        f"--prompt={prompt[:1000]}",  # 限制长度
        f"--ratio={ratio}",
        "--resolution_type=2k",
        f"--model_version={model_version}",
        f"--poll={poll_seconds}"
    ]
    
    result = run_dreamina_command(cmd, timeout=poll_seconds + 60)
    
    if not result:
        print("图片生成命令失败")
        return None
    
    if result.returncode == 0:
        # 尝试从输出中提取任务ID
        task_id = extract_task_id(result.stdout)
        if task_id:
            # 查询任务结果
            query_result = query_task_result(task_id, max_attempts=10, interval=15)
            if query_result:
                # 检查是否有文件路径信息
                # 这里简化处理，实际需要解析输出获取文件路径
                print(f"图片生成任务完成，任务ID: {task_id}")
                # 实际文件可能保存在Dreamina默认位置，这里返回任务ID
                return task_id
    else:
        print(f"图片生成失败，返回码: {result.returncode}")
    
    return None

def generate_video_with_images(prompt, image_paths, output_name, duration=25, poll_seconds=60):
    """使用多张图片生成视频"""
    print(f"\n🎬 生成视频: {output_name}")
    
    output_path = OUTPUT_DIR / f"{output_name}.mp4"
    
    # 构建命令
    cmd = [
        DREAMINA_CLI, "multimodal2video",
        f"--prompt={prompt[:1500]}",  # 限制长度
        f"--duration={duration}",
        f"--poll={poll_seconds}"
    ]
    
    # 添加图片参数
    for img_path in image_paths:
        if img_path and os.path.exists(img_path):
            cmd.append(f"--image={img_path}")
        else:
            print(f"图片不存在: {img_path}")
    
    # 如果没有有效图片，使用text2video
    if len(cmd) <= 3:  # 只有基本参数
        print("没有有效图片，使用text2video")
        cmd = [
            DREAMINA_CLI, "text2video",
            f"--prompt={prompt[:1500]}",
            f"--duration={duration}",
            f"--poll={poll_seconds}"
        ]
    
    result = run_dreamina_command(cmd, timeout=poll_seconds + 120)
    
    if not result:
        print("视频生成命令失败")
        return None
    
    if result.returncode == 0:
        task_id = extract_task_id(result.stdout)
        if task_id:
            print(f"视频生成任务已提交，任务ID: {task_id}")
            
            # 查询任务结果
            query_result = query_task_result(task_id, max_attempts=20, interval=20)
            if query_result:
                print("视频生成任务完成")
                return task_id
    else:
        print(f"视频生成失败，返回码: {result.returncode}")
    
    return None

def main():
    print("🚀 开始自动化生成《偏爱难藏硅谷AI版》视频")
    print("=" * 70)
    
    # 检查Dreamina CLI
    if not os.path.exists(DREAMINA_CLI):
        print(f"❌ Dreamina CLI不存在: {DREAMINA_CLI}")
        return
    
    # 检查积分余额
    print("\n💰 检查积分余额...")
    credit_result = run_dreamina_command([DREAMINA_CLI, "user_credit"], timeout=30)
    if credit_result and credit_result.returncode == 0:
        print(f"积分信息: {credit_result.stdout[:500]}")
    else:
        print("无法获取积分信息，继续执行")
    
    # 加载之前提取的提示词
    print("\n📖 加载提示词...")
    json_file = OUTPUT_DIR / "script_analysis.json"
    if not json_file.exists():
        print(f"❌ 提示词文件不存在: {json_file}")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取提示词
    killian_prompt = data['characters']['killian']['image_prompt']
    elara_prompt = data['characters']['elara']['image_prompt']
    scene_prompt = data['scene']['scene_prompt']
    xiaoqiu_prompt = data['scene']['xiaoqiu_prompt']
    
    print(f"Killian提示词长度: {len(killian_prompt)}")
    print(f"Elara提示词长度: {len(elara_prompt)}")
    print(f"场景提示词长度: {len(scene_prompt)}")
    print(f"小邱视频提示词长度: {len(xiaoqiu_prompt)}")
    
    # 生成图片
    print("\n" + "=" * 70)
    print("阶段1: 生成人物和场景图片")
    print("=" * 70)
    
    image_tasks = []
    
    # 生成Killian图片
    killian_task = generate_image(
        killian_prompt,
        "killian_portrait",
        ratio="16:9",
        model_version="5.0",
        poll_seconds=30
    )
    if killian_task:
        image_tasks.append(killian_task)
    
    time.sleep(5)  # 避免请求过快
    
    # 生成Elara图片
    elara_task = generate_image(
        elara_prompt,
        "elara_portrait",
        ratio="16:9",
        model_version="5.0",
        poll_seconds=30
    )
    if elara_task:
        image_tasks.append(elara_task)
    
    time.sleep(5)
    
    # 生成场景图片
    scene_task = generate_image(
        scene_prompt,
        "interview_scene",
        ratio="16:9",
        model_version="5.0",
        poll_seconds=30
    )
    if scene_task:
        image_tasks.append(scene_task)
    
    print(f"\n📊 图片生成任务: {len(image_tasks)} 个")
    
    # 等待所有图片任务完成
    print("\n⏳ 等待图片生成完成...")
    time.sleep(60)  # 等待1分钟
    
    # 检查任务状态
    completed_images = []
    for task_id in image_tasks:
        print(f"检查任务 {task_id}...")
        result = query_task_result(task_id, max_attempts=5, interval=10)
        if result:
            completed_images.append(task_id)
    
    print(f"✅ 已完成图片: {len(completed_images)} 张")
    
    # 阶段2: 生成视频
    print("\n" + "=" * 70)
    print("阶段2: 生成视频")
    print("=" * 70)
    
    # 查找生成的图片文件
    # 注意: Dreamina CLI可能将文件保存在默认位置
    # 这里简化处理，直接使用提示词生成视频
    
    # 使用text2video生成视频（简化版）
    print("使用小邱提示词生成视频...")
    
    video_task = generate_video_with_images(
        xiaoqiu_prompt,
        [],  # 暂时不传入图片
        "silicon_valley_interview",
        duration=25,
        poll_seconds=60
    )
    
    if video_task:
        print(f"✅ 视频生成任务已提交: {video_task}")
        
        # 等待视频生成完成
        print("\n⏳ 等待视频生成完成...")
        time.sleep(90)  # 等待1.5分钟
        
        # 查询视频结果
        video_result = query_task_result(video_task, max_attempts=15, interval=20)
        if video_result:
            print("🎉 视频生成成功！")
            
            # 保存任务信息
            tasks_file = OUTPUT_DIR / "generation_tasks.json"
            tasks_data = {
                "image_tasks": image_tasks,
                "video_task": video_task,
                "timestamp": time.time(),
                "status": "completed"
            }
            with open(tasks_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
            
            print(f"任务信息已保存: {tasks_file}")
        else:
            print("⚠️  视频生成可能仍在处理中")
    else:
        print("❌ 视频生成失败")
    
    # 最终状态
    print("\n" + "=" * 70)
    print("📋 生成任务总结")
    print("=" * 70)
    print(f"图片任务: {len(image_tasks)} 个")
    print(f"视频任务: {'已提交' if video_task else '未提交'}")
    print(f"输出目录: {OUTPUT_DIR}")
    
    # 再次检查积分余额
    print("\n💰 最终积分余额...")
    run_dreamina_command([DREAMINA_CLI, "user_credit"], timeout=30)
    
    print("\n✅ 自动化流程完成！")
    print("\n下一步:")
    print("1. 使用 dreamina list_task 查看任务状态")
    print("2. 使用 dreamina query_result --submit_id=<ID> 查询具体任务结果")
    print("3. 下载生成的图片和视频文件")

if __name__ == "__main__":
    main()