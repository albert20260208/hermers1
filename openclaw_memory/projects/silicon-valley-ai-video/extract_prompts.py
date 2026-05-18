#!/usr/bin/env python3
import json
import os

script_file = "/root/.openclaw/workspace/projects/silicon-valley-ai-video/outputs/script_analysis.json"
with open(script_file, "r", encoding="utf-8") as f:
    data = json.load(f)

killian_prompt = data["characters"]["killian"]["image_prompt"]
elara_prompt = data["characters"]["elara"]["image_prompt"]
scene_prompt = data["scene"]["scene_prompt"]

# 清理提示词：移除描述性文本，只保留实际提示词
def clean_prompt(prompt):
    # 尝试提取最后一个逗号后的部分
    parts = prompt.split(',')
    if len(parts) > 1:
        # 取最后一部分，通常是具体的描述
        return parts[-1].strip()
    return prompt

killian_clean = clean_prompt(killian_prompt)
elara_clean = clean_prompt(elara_prompt)
scene_clean = clean_prompt(scene_prompt)

print("Killian提示词:", killian_clean[:200])
print("\nElara提示词:", elara_clean[:200])
print("\n场景提示词:", scene_clean[:200])

# 保存到文件
with open("/tmp/killian_prompt.txt", "w") as f:
    f.write(killian_clean)
with open("/tmp/elara_prompt.txt", "w") as f:
    f.write(elara_clean)
with open("/tmp/scene_prompt.txt", "w") as f:
    f.write(scene_clean)

print("\n提示词已保存到 /tmp/")