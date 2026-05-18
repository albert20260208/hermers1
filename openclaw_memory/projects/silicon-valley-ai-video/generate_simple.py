#!/usr/bin/env python3
"""
简化版生成脚本 - 只生成Killian图片作为测试
"""

import json
import subprocess
import time
import os
from pathlib import Path

DREAMINA_CLI = "/root/.local/bin/dreamina"
OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def run_cmd(cmd):
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    print(f"返回码: {result.returncode}")
    if result.stdout:
        print(f"输出: {result.stdout[:500]}")
    return result

def main():
    print("简化测试: 生成Killian图片")
    
    # 加载提示词
    json_file = OUTPUT_DIR / "script_analysis.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    prompt = data['characters']['killian']['image_prompt']
    print(f"提示词长度: {len(prompt)}")
    print(f"提示词: {prompt[:200]}...")
    
    # 生成图片
    print("\n提交图片生成任务...")
    cmd = [
        DREAMINA_CLI, "text2image",
        f"--prompt={prompt[:1000]}",
        "--ratio=16:9",
        "--resolution_type=2k",
        "--model_version=5.0",
        "--poll=20"
    ]
    
    result = run_cmd(cmd)
    
    # 提取任务ID
    import re
    output = result.stdout
    task_id = None
    
    # 尝试从输出中提取任务ID
    if '"task_id"' in output:
        match = re.search(r'"task_id"\s*:\s*"([a-f0-9]+)"', output)
        if match:
            task_id = match.group(1)
    
    if not task_id and '"id"' in output:
        match = re.search(r'"id"\s*:\s*"([a-f0-9]+)"', output)
        if match:
            task_id = match.group(1)
    
    if not task_id:
        # 尝试查找长hex字符串
        matches = re.findall(r'([a-f0-9]{16,})', output, re.IGNORECASE)
        if matches:
            task_id = matches[0]
    
    if task_id:
        print(f"任务ID: {task_id}")
        
        # 保存任务ID
        task_file = OUTPUT_DIR / "killian_task_id.txt"
        with open(task_file, 'w') as f:
            f.write(task_id)
        print(f"任务ID已保存: {task_file}")
        
        # 查询任务状态
        print(f"\n等待10秒后查询任务状态...")
        time.sleep(10)
        
        print(f"查询任务结果...")
        query_cmd = [DREAMINA_CLI, "query_result", f"--submit_id={task_id}"]
        query_result = run_cmd(query_cmd)
        
        # 检查状态
        if query_result.returncode == 0:
            output_lower = query_result.stdout.lower()
            if 'success' in output_lower or 'succeeded' in output_lower:
                print("✅ 图片生成成功！")
                
                # 尝试提取图片URL
                import json
                try:
                    data = json.loads(query_result.stdout)
                    if 'result' in data and 'url' in data['result']:
                        url = data['result']['url']
                        print(f"图片URL: {url}")
                except:
                    pass
            elif 'failed' in output_lower or 'error' in output_lower:
                print("❌ 图片生成失败")
            else:
                print("⏳ 图片仍在处理中")
                print("可以使用以下命令查询:")
                print(f"  dreamina query_result --submit_id={task_id}")
        else:
            print("查询失败")
    else:
        print("未找到任务ID")
        print("原始输出:", output[:500])
    
    print("\n测试完成")

if __name__ == "__main__":
    main()