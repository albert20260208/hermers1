#!/usr/bin/env python3
"""
提取《偏爱难藏硅谷AI版》人物场景信息并生成小邱格式提示词
"""

import os
import json
from pathlib import Path

# 配置
WORKSPACE = Path("/root/.openclaw/workspace")
SCRIPT_FILE = WORKSPACE / "skills" / "video" / "projects" / "偏爱难藏-硅谷AI版" / "scripts" / "硅谷AI版-完整人设+80集剧情大纲.md"
OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_section(content, start_marker, end_marker=None):
    """提取两个标记之间的内容"""
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return None
    
    if end_marker:
        end_idx = content.find(end_marker, start_idx + len(start_marker))
        if end_idx == -1:
            return content[start_idx + len(start_marker):]
        return content[start_idx + len(start_marker):end_idx]
    else:
        return content[start_idx + len(start_marker):]

def extract_character_details(content, character_name):
    """提取特定角色的详细描述"""
    # 查找角色标题
    lines = content.split('\n')
    in_character = False
    character_lines = []
    
    for i, line in enumerate(lines):
        if character_name in line and ('##' in line or '###' in line):
            in_character = True
            continue
        
        if in_character:
            if line.strip() == '':
                continue
            if line.startswith('##') and character_name not in line:
                break
            if line.startswith('- **') or line.startswith('  -'):
                character_lines.append(line.strip())
            elif ':' in line and '**' in line:
                character_lines.append(line.strip())
    
    return '\n'.join(character_lines)

def main():
    print("📚 提取《偏爱难藏硅谷AI版》剧本信息")
    print("=" * 70)
    
    # 读取剧本
    with open(SCRIPT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"剧本文件大小: {len(content)} 字符")
    
    # 提取人物部分（第五部分）
    characters_section = extract_section(content, '# 五、终极完整人设（植入AI核心设定）', '# 五、80集全剧完整剧情')
    if not characters_section:
        characters_section = extract_section(content, '# 五、终极完整人设（植入AI核心设定）', '# 六、')
    
    if characters_section:
        print("\n👥 提取到人物描述部分")
        
        # 提取男主信息
        killian_section = extract_section(characters_section, '## 👨‍💻 男主：Killian Blackwood（基利安·布莱克伍德）', '## 👩‍🎨 女主：')
        if not killian_section:
            killian_section = extract_section(characters_section, '男主：Killian Blackwood', '女主：')
        
        # 提取女主信息
        elara_section = extract_section(characters_section, '## 👩‍🎨 女主：Elara Voss（埃拉拉·沃斯）', '## 👑 姐姐：')
        if not elara_section:
            elara_section = extract_section(characters_section, '女主：Elara Voss', '姐姐：')
        
        # 提取姐姐信息
        seraphina_section = extract_section(characters_section, '## 👑 姐姐：Seraphina Voss（塞拉菲娜·沃斯）', '## 🤝 其他核心配角')
        if not seraphina_section:
            seraphina_section = extract_section(characters_section, '姐姐：Seraphina Voss', '其他核心配角')
        
        print(f"男主描述长度: {len(killian_section) if killian_section else 0} 字符")
        print(f"女主描述长度: {len(elara_section) if elara_section else 0} 字符")
        print(f"姐姐描述长度: {len(seraphina_section) if seraphina_section else 0} 字符")
    else:
        print("⚠️  未找到人物描述部分，使用全文搜索")
        killian_section = extract_character_details(content, "Killian")
        elara_section = extract_character_details(content, "Elara")
        seraphina_section = extract_character_details(content, "Seraphina")
    
    # 提取采访场景
    print("\n🎬 搜索采访场景...")
    interview_keywords = ['采访', 'interview', '专访', '职场采访未婚夫', '采访名场面']
    interview_lines = []
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in interview_keywords):
            # 收集上下文
            start = max(0, i - 3)
            end = min(len(lines), i + 10)
            context = lines[start:end]
            interview_lines.extend(context)
            interview_lines.append("---")  # 分隔符
    
    interview_scene = '\n'.join(interview_lines[:50])  # 限制长度
    
    # 生成人物描述摘要
    def summarize_character(section, name, default_role):
        if not section:
            return default_role
        # 提取关键信息
        lines = section.split('\n')
        key_info = []
        for line in lines[:10]:  # 前10行
            if '**' in line or ':' in line or '-' in line:
                key_info.append(line.strip())
        return ' '.join(key_info[:5])  # 前5条关键信息
    
    killian_desc = summarize_character(killian_section, "Killian", "28岁硅谷AI创业者，斯坦福大学人工智能博士，Blackwood家族继承人，技术极客，专注BlackAI研发")
    elara_desc = summarize_character(elara_section, "Elara", "22岁纽约大学传媒/艺术策展专业学生，沃斯家族小女儿，艺术气质，敏感自卑但温柔坚韧")
    seraphina_desc = summarize_character(seraphina_section, "Seraphina", "24岁沃斯家嫡长女，虚荣势利，精致利己，逃婚后后悔，试图抢婚")
    
    print("\n📋 人物摘要:")
    print(f"  👨 Killian: {killian_desc[:100]}...")
    print(f"  👩 Elara: {elara_desc[:100]}...")
    print(f"  👑 Seraphina: {seraphina_desc[:100]}...")
    print(f"  🎬 采访场景: {len(interview_scene)} 字符")
    
    # 生成小邱格式提示词（采访场景）
    print("\n✍️  生成小邱格式提示词...")
    
    xiaoqiu_prompt = f"""
0-5秒
·动态行为/剧情描述：Killian Blackwood（{killian_desc[:80]}）身穿黑色西装，坐在硅谷科技公司现代会议室，接受专业采访。他神情专注，手指轻轻敲击桌面，表现出技术专家的自信与些许紧张。
·镜头运动：固定机位中景镜头，焦点在Killian面部，背景虚化显示高科技办公室环境，浅景深突出人物。

5-10秒
·动态行为/剧情描述：Elara Voss（{elara_desc[:80]}）作为采访记者，身穿简约白色长裙，手持麦克风专业提问。她眼神充满好奇与专注，微微前倾身体，表现出对AI技术的浓厚兴趣。
·镜头运动：过肩镜头，从Killian肩后拍摄Elara，焦点在Elara面部表情，捕捉她的专业与温柔气质。

10-15秒
·动态行为/剧情描述：Killian回答问题时，目光与Elara相遇，眼神突然变得柔和，嘴角微微上扬，展现出技术男特有的笨拙温柔。Elara微微低头掩饰笑意，形成微妙的情感张力。
·镜头运动：特写镜头，缓慢推近Killian面部，捕捉微表情变化，背景完全虚化，突出情感细节。

15-20秒
·动态行为/剧情描述：两人在采访间隙短暂交流，Killian用技术语言解释AI概念，Elara认真记录并点头理解。镜头展现两人默契的互动，暗示超越采访的情感连接。
·镜头运动：双人镜头，固定机位，缓慢平移捕捉两人互动，环境光线柔和温馨，营造浪漫氛围。

20-25秒
·动态行为/剧情描述：采访结束，Killian起身送Elara离开，在会议室门口短暂停留，两人目光再次交汇，空气中弥漫着未言明的情感。Killian手指无意识地摩挲着西装扣子。
·镜头运动：远景镜头，从会议室内部拍摄门口两人，框架构图，象征两人关系的开始与界限。

音频设计：
·背景音乐：轻柔的现代钢琴曲，略带科技感的电子音效，营造专业又温馨的氛围
·环境音效：办公室轻微键盘声、空调背景音、纸张翻动声
·对话音效：清晰的采访对话，专业录音质量，音量适中
·情感音效：微妙的环境静音时刻，突出情感张力

视觉风格：
·电影质感：Cinematic quality, 35mm film grain, shallow depth of field, anamorphic lens flares
·画面比例：2.35:1 widescreen, 24fps, cinematic aspect ratio
·色调氛围：现代科技冷色调为主（蓝、灰），局部暖光（黄、橙）突出情感时刻
·镜头语言：专业电影镜头语言，情感导向的镜头运动，匹配剪辑转场
·色彩分级：Professional color grading with desaturated tones, highlight warmth, shadow coolness
"""
    
    # 生成图片提示词
    print("\n🎨 生成图片提示词...")
    
    killian_image_prompt = f"Professional portrait of Killian Blackwood, {killian_desc}, 28-year-old Silicon Valley AI entrepreneur, wearing black suit, in modern tech office, cinematic lighting, photorealistic, detailed facial features, confident expression, shallow depth of field, 8k resolution"
    
    elara_image_prompt = f"Professional portrait of Elara Voss, {elara_desc}, 22-year-old art student, wearing elegant white dress, as professional journalist, holding microphone, gentle expression, artistic气质, cinematic lighting, photorealistic, detailed features, soft focus background, 8k resolution"
    
    interview_scene_prompt = f"Modern Silicon Valley tech office interview scene, {killian_desc[:50]} and {elara_desc[:50]} in professional interview setting, cinematic composition, clean modern interior design, large windows with city view, professional lighting, photorealistic, detailed environment, wide shot, 8k resolution"
    
    # 保存所有输出
    output_data = {
        "characters": {
            "killian": {
                "name": "Killian Blackwood",
                "description": killian_desc,
                "image_prompt": killian_image_prompt
            },
            "elara": {
                "name": "Elara Voss",
                "description": elara_desc,
                "image_prompt": elara_image_prompt
            },
            "seraphina": {
                "name": "Seraphina Voss",
                "description": seraphina_desc
            }
        },
        "scene": {
            "interview": interview_scene[:500],
            "xiaoqiu_prompt": xiaoqiu_prompt.strip(),
            "scene_prompt": interview_scene_prompt
        }
    }
    
    # 保存JSON文件
    json_file = OUTPUT_DIR / "script_analysis.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    # 保存小邱提示词文本
    prompt_file = OUTPUT_DIR / "xiaoqiu_interview_prompt.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(xiaoqiu_prompt.strip())
    
    # 保存图片提示词
    image_prompts_file = OUTPUT_DIR / "image_prompts.txt"
    with open(image_prompts_file, 'w', encoding='utf-8') as f:
        f.write("=== Killian Portrait ===\n")
        f.write(killian_image_prompt + "\n\n")
        f.write("=== Elara Portrait ===\n")
        f.write(elara_image_prompt + "\n\n")
        f.write("=== Interview Scene ===\n")
        f.write(interview_scene_prompt + "\n")
    
    print("\n💾 输出文件:")
    print(f"  📄 {json_file}")
    print(f"  📝 {prompt_file}")
    print(f"  🎨 {image_prompts_file}")
    
    print("\n📊 提示词统计:")
    print(f"  小邱提示词: {len(xiaoqiu_prompt)} 字符")
    print(f"  Killian图片提示词: {len(killian_image_prompt)} 字符")
    print(f"  Elara图片提示词: {len(elara_image_prompt)} 字符")
    print(f"  场景图片提示词: {len(interview_scene_prompt)} 字符")
    
    print("\n" + "=" * 70)
    print("✅ 信息提取完成！")
    print("\n下一步:")
    print("1. 使用 dreamina text2image 生成人物和场景图片")
    print("2. 使用 dreamina multimodal2video 生成视频")
    print("3. 或使用 DeerFlow API 调用 image-generation 和 video-generation 技能")
    print("\n已生成完整的提示词文件，可直接使用。")

if __name__ == "__main__":
    main()