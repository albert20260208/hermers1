#!/usr/bin/env python3
"""
自动生成《偏爱难藏硅谷AI版》人物场景视频脚本
使用小邱提示词方式，调用Dreamina CLI生成图片和视频
"""

import os
import json
import subprocess
import tempfile
import time
import re
from pathlib import Path

# 配置
WORKSPACE = Path("/root/.openclaw/workspace")
SCRIPT_DIR = Path(__file__).parent
OUTPUT_DIR = SCRIPT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 剧本文件路径
SCRIPT_FILE = WORKSPACE / "skills" / "video" / "projects" / "偏爱难藏-硅谷AI版" / "scripts" / "硅谷AI版-完整人设+80集剧情大纲.md"

# Dreamina CLI路径
DREAMINA_CLI = "/root/.local/bin/dreamina"

def read_script():
    """读取剧本文件，提取人物描述和场景信息"""
    with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取人物描述部分
    # 查找"五、终极完整人设（植入AI核心设定）"部分
    sections = content.split('#')
    characters_section = None
    for i, section in enumerate(sections):
        if '终极完整人设' in section:
            characters_section = '# ' + section
            break
    
    if not characters_section:
        print("未找到人物描述部分")
        return None
    
    # 提取男主描述
    male_character = extract_character(characters_section, '男主', 'Killian Blackwood')
    female_character = extract_character(characters_section, '女主', 'Elara Voss')
    sister_character = extract_character(characters_section, '姐姐', 'Seraphina Voss')
    
    # 提取关键场景 - 选择采访场景（剧本中提到的经典场景）
    interview_scene = extract_interview_scene(content)
    
    return {
        'male_character': male_character,
        'female_character': female_character,
        'sister_character': sister_character,
        'interview_scene': interview_scene
    }

def extract_character(section, role, name):
    """从人物部分提取特定角色描述"""
    lines = section.split('\n')
    character_start = False
    character_lines = []
    
    for line in lines:
        if role in line or name in line:
            character_start = True
        elif character_start and line.strip() and not line.startswith('##'):
            character_lines.append(line.strip())
        elif character_start and line.startswith('##'):
            break
    
    return ' '.join(character_lines[:10])  # 取前10行作为描述

def extract_interview_scene(content):
    """提取采访场景描述"""
    # 查找采访相关描述
    interview_keywords = ['采访', 'interview', '专访', '职场采访未婚夫']
    lines = content.split('\n')
    scene_lines = []
    
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in interview_keywords):
            # 收集后续几行
            for j in range(i, min(i+10, len(lines))):
                scene_lines.append(lines[j])
            break
    
    return '\n'.join(scene_lines[:20])  # 取前20行

def generate_character_image(character_desc, character_name, output_path):
    """生成人物图片"""
    # 构建图片提示词
    prompt = f"Professional portrait of {character_name}, {character_desc}, cinematic lighting, 8k resolution, photorealistic, detailed facial features, studio portrait, high quality"
    
    print(f"生成人物图片: {character_name}")
    print(f"提示词: {prompt[:100]}...")
    
    # 调用Dreamina CLI生成图片
    cmd = [
        DREAMINA_CLI, "text2image",
        f"--prompt={prompt}",
        "--ratio=16:9",
        "--resolution_type=2k",
        f"--output={output_path}"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print("STDOUT:", result.stdout[:500])
        if result.stderr:
            print("STDERR:", result.stderr[:500])
        
        if result.returncode != 0:
            print(f"生成图片失败: {result.returncode}")
            return None
        
        # 解析输出，获取任务ID
        # Dreamina CLI输出可能包含任务ID
        # 这里简化处理，假设图片已保存到output_path
        return output_path
    except subprocess.TimeoutExpired:
        print("生成图片超时")
        return None
    except Exception as e:
        print(f"生成图片异常: {e}")
        return None

def generate_scene_image(scene_desc, scene_name, output_path):
    """生成场景图片"""
    # 构建场景提示词
    prompt = f"Professional cinematic scene: {scene_desc}, interview setting, Silicon Valley tech office, modern interior design, cinematic lighting, 8k resolution, photorealistic, wide shot, detailed environment"
    
    print(f"生成场景图片: {scene_name}")
    print(f"提示词: {prompt[:100]}...")
    
    cmd = [
        DREAMINA_CLI, "text2image",
        f"--prompt={prompt}",
        "--ratio=16:9",
        "--resolution_type=2k",
        f"--output={output_path}"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        print("STDOUT:", result.stdout[:500])
        if result.stderr:
            print("STDERR:", result.stderr[:500])
        
        if result.returncode != 0:
            print(f"生成场景图片失败: {result.returncode}")
            return None
        
        return output_path
    except subprocess.TimeoutExpired:
        print("生成场景图片超时")
        return None
    except Exception as e:
        print(f"生成场景图片异常: {e}")
        return None

def create_xiaoqiu_prompt(scene_info, male_image_path, female_image_path, scene_image_path):
    """创建小邱格式的时间分段提示词"""
    # 基于采访场景创建小邱提示词
    prompt = """0-5秒
·动态行为/剧情描述：Killian Blackwood身穿黑色西装，坐在硅谷科技公司会议室，面对摄像机采访，神情专注而略带紧张，调整领带，准备回答问题。
·镜头运动：固定机位中景镜头，焦点在Killian面部，背景虚化显示现代办公室环境。

5-10秒
·动态行为/剧情描述：Elara Voss作为采访记者，手持麦克风，专注地提问，眼神充满专业与好奇，微微前倾身体，表现出对技术的兴趣。
·镜头运动：过肩镜头，从Killian肩后拍摄Elara，焦点在Elara面部，浅景深突出情感表达。

10-15秒
·动态行为/剧情描述：Killian回答问题时，眼神突然变得温柔，看向Elara的方向，嘴角微微上扬，展现出技术男特有的笨拙温柔。
·镜头运动：特写镜头，缓慢推近Killian面部，捕捉微表情变化，背景完全虚化。

15-20秒
·动态行为/剧情描述：两人目光交汇，Elara微微低头掩饰笑意，Killian继续讲解AI技术，但注意力明显在Elara身上，形成微妙的情感张力。
·镜头运动：双人镜头，固定机位，捕捉两人互动关系，环境光线柔和温馨。

音频设计：
·背景音乐：轻柔的钢琴曲，营造温馨专业氛围
·环境音效：办公室轻微键盘声、空调背景音
·对话音效：清晰的采访对话，专业录音质量

视觉风格：
·电影质感：Cinematic quality, film grain, shallow depth of field
·画面比例：16:9 widescreen, 24fps
·色调氛围：现代科技感，冷色调为主，局部暖光突出情感
·镜头语言：专业电影镜头语言，情感导向的镜头运动"""
    
    return prompt

def generate_video(xiaoqiu_prompt, image_paths, output_path):
    """使用多张图片生成视频"""
    # 使用multimodal2video命令，结合图片和提示词
    print("生成视频...")
    print(f"使用图片: {image_paths}")
    
    # 构建命令
    cmd = [
        DREAMINA_CLI, "multimodal2video",
        f"--prompt={xiaoqiu_prompt}",
        f"--output={output_path}",
        "--duration=20"
    ]
    
    # 添加图片参数
    for img_path in image_paths:
        cmd.append(f"--image={img_path}")
    
    print(f"执行命令: {' '.join(cmd[:5])}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        print("STDOUT:", result.stdout[:1000])
        if result.stderr:
            print("STDERR:", result.stderr[:500])
        
        if result.returncode != 0:
            print(f"生成视频失败: {result.returncode}")
            return None
        
        # 解析输出，获取视频任务ID
        # 简化处理，假设视频已生成
        return output_path
    except subprocess.TimeoutExpired:
        print("生成视频超时")
        return None
    except Exception as e:
        print(f"生成视频异常: {e}")
        return None

def main():
    print("开始自动生成《偏爱难藏硅谷AI版》视频")
    print("=" * 60)
    
    # 1. 读取剧本
    print("\n1. 读取剧本文件...")
    script_data = read_script()
    if not script_data:
        print("读取剧本失败")
        return
    
    print(f"男主描述: {script_data['male_character'][:100]}...")
    print(f"女主描述: {script_data['female_character'][:100]}...")
    print(f"采访场景: {script_data['interview_scene'][:100]}...")
    
    # 2. 生成人物图片
    print("\n2. 生成人物图片...")
    male_image = OUTPUT_DIR / "killian_portrait.jpg"
    female_image = OUTPUT_DIR / "elara_portrait.jpg"
    
    male_image_path = generate_character_image(
        script_data['male_character'],
        "Killian Blackwood (28岁硅谷AI创业者，技术极客，黑色西装)",
        str(male_image)
    )
    
    female_image_path = generate_character_image(
        script_data['female_character'],
        "Elara Voss (22岁艺术策展专业学生，优雅知性，简约白色长裙)",
        str(female_image)
    )
    
    if not male_image_path or not female_image_path:
        print("生成人物图片失败，使用备用图片")
        # 可以跳过或使用默认图片
    
    # 3. 生成场景图片
    print("\n3. 生成场景图片...")
    scene_image = OUTPUT_DIR / "interview_scene.jpg"
    scene_image_path = generate_scene_image(
        script_data['interview_scene'],
        "硅谷科技公司采访场景",
        str(scene_image)
    )
    
    # 4. 创建小邱格式提示词
    print("\n4. 创建小邱格式提示词...")
    image_paths = []
    if male_image_path and os.path.exists(male_image_path):
        image_paths.append(male_image_path)
    if female_image_path and os.path.exists(female_image_path):
        image_paths.append(female_image_path)
    if scene_image_path and os.path.exists(scene_image_path):
        image_paths.append(scene_image_path)
    
    xiaoqiu_prompt = create_xiaoqiu_prompt(
        script_data['interview_scene'],
        male_image_path,
        female_image_path,
        scene_image_path
    )
    
    print(f"小邱提示词长度: {len(xiaoqiu_prompt)} 字符")
    print("提示词预览:")
    print(xiaoqiu_prompt[:500])
    
    # 保存提示词
    prompt_file = OUTPUT_DIR / "xiaoqiu_prompt.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(xiaoqiu_prompt)
    print(f"提示词已保存: {prompt_file}")
    
    # 5. 生成视频
    print("\n5. 生成视频...")
    video_output = OUTPUT_DIR / "silicon_valley_interview_video.mp4"
    
    video_path = generate_video(xiaoqiu_prompt, image_paths, str(video_output))
    
    if video_path and os.path.exists(video_path):
        print(f"\n✅ 视频生成成功: {video_path}")
        print(f"文件大小: {os.path.getsize(video_path) / 1024 / 1024:.2f} MB")
        
        # 显示积分余额
        print("\n检查积分余额...")
        subprocess.run([DREAMINA_CLI, "user_credit"], timeout=30)
    else:
        print("\n❌ 视频生成失败")
        
        # 尝试使用text2video作为备选
        print("尝试使用text2video备选方案...")
        alt_cmd = [
            DREAMINA_CLI, "text2video",
            f"--prompt={xiaoqiu_prompt[:500]}",  # 截断提示词
            "--duration=20",
            f"--output={video_output}"
        ]
        try:
            result = subprocess.run(alt_cmd, capture_output=True, text=True, timeout=600)
            print("备选方案STDOUT:", result.stdout[:1000])
            if os.path.exists(video_output):
                print(f"✅ 备选方案视频生成成功: {video_output}")
        except Exception as e:
            print(f"备选方案失败: {e}")
    
    print("\n" + "=" * 60)
    print("自动生成流程完成")
    print(f"输出目录: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()