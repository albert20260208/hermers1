# 🎬 DeerFlow 视频工作流索引

**最后更新**: 2026-04-06 04:08 UTC  
**工作流数量**: 2  
**总积分消耗**: ~200-300积分/项目

---

## 🚀 快速启动

### 方式1: 一键命令（推荐）

```bash
# 半自动广告工作流
cd /root/.openclaw/workspace/projects/ad-workflow
python workflows/ad_creation_workflow.py

# 全自动视频工作流
cd /root/.openclaw/workspace/projects/auto-video-generation
bash start_generation.sh
```

### 方式2: 通过别名（需配置）

```bash
# 添加到 ~/.bashrc
alias workflow-ad='cd /root/.openclaw/workspace/projects/ad-workflow && python workflows/ad_creation_workflow.py'
alias workflow-auto='cd /root/.openclaw/workspace/projects/auto-video-generation && bash start_generation.sh'

# 使用
workflow-ad      # 启动广告工作流
workflow-auto    # 启动自动视频工作流
```

---

## 📊 工作流对比表

| 特性 | 半自动广告工作流 | 全自动视频工作流 |
|------|-----------------|-----------------|
| **路径** | `projects/ad-workflow/` | `projects/auto-video-generation/` |
| **主脚本** | `workflows/ad_creation_workflow.py` | `scripts/fixed_generator.py` |
| **启动命令** | `python workflows/ad_creation_workflow.py` | `bash start_generation.sh` |
| **自动化程度** | ⏸️ 4个人工确认环节 | ⚡ 完全自动化 |
| **输入类型** | 产品信息 + 广告风格 | 完整剧本（scenes.json） |
| **输出数量** | 1个高质量广告视频 | 8个15秒视频 |
| **经验库** | ✅ 图片+视频提示词库 | ⚠️ 剧本场景库 |
| **质量控制** | 人工确认每个环节 | 审核失败自动跳过 |
| **积分控制** | 精确控制（用户确认） | 批量消耗（150-200积分） |
| **适合场景** | 商业广告制作 | 批量视频生成 |
| **执行时间** | 10-20分钟（含确认） | 30-60分钟（全自动） |
| **成功率** | 接近100%（人工把关） | 87.5%（7/8场景） |

---

## 🎯 决策树：选择哪个工作流？

```
┌─────────────────────────────────┐
│   需要生成视频？                 │
└─────────────┬───────────────────┘
              │
              ├─ 是批量生成（>3个视频）？
              │  │
              │  ├─ 是 → 【全自动视频工作流】
              │  │       - 有完整剧本/场景列表
              │  │       - 需要多个场景视频
              │  │       - 可接受部分失败（87.5%成功率）
              │  │       - 积分充足（150-200积分）
              │  │
              │  └─ 否 → 继续判断
              │
              ├─ 需要人工审核/质量把关？
              │  │
              │  ├─ 是 → 【半自动广告工作流】
              │  │       - 商业广告（需精确控制）
              │  │       - 预算有限（精确控制积分）
              │  │       - 单个高质量视频
              │  │       - 需要经验库匹配
              │  │       - 4个确认环节保证质量
              │  │
              │  └─ 否 → 继续判断
              │
              └─ 特殊场景判断
                 │
                 ├─ 内容可能触发审核？
                 │  └─ 是 → 【半自动】（人工确认避免浪费积分）
                 │
                 ├─ 需要经验库匹配？
                 │  └─ 是 → 【半自动】（有图片+视频提示词库）
                 │
                 ├─ 完全无人值守运行？
                 │  └─ 是 → 【全自动】（失败自动跳过）
                 │
                 └─ 不确定？
                    └─ 先用【半自动】测试1个，再决定是否批量
```

### 📋 决策速查表

| 场景 | 批量生成？ | 需要审核？ | 推荐工作流 | 原因 |
|------|-----------|-----------|-----------|------|
| **商业广告（单个）** | ❌ | ✅ | 半自动 | 质量优先，精确控制积分 |
| **商业广告（批量）** | ✅ | ✅ | 半自动 | 虽然批量，但质量要求高 |
| **剧集视频（8集）** | ✅ | ❌ | 全自动 | 批量生成，可接受部分失败 |
| **测试/实验视频** | ❌ | ❌ | 半自动 | 先测试，确认效果后再批量 |
| **敏感内容视频** | ✅/❌ | ✅ | 半自动 | 避免审核失败浪费积分 |
| **产品展示（单个）** | ❌ | ✅ | 半自动 | 需要经验库匹配 |
| **短视频矩阵（>10个）** | ✅ | ❌ | 全自动 | 大批量，效率优先 |

---

## 📁 工作流详细信息

### 工作流1: 半自动广告工作流

**路径**: `/root/.openclaw/workspace/projects/ad-workflow/`

**核心文件**:
- `workflows/ad_creation_workflow.py` - 主工作流脚本（16KB）
- `knowledge/prompts/image_prompts.json` - 图片提示词经验库（3案例+2模板）
- `knowledge/prompts/video_prompts.json` - 视频提示词经验库（4案例+2模板）
- `create_moxibustion_ad.py` - 示例项目：艾灸贴广告

**工作流程**:
```
1. 输入产品信息（名称、类型、风格）
   ↓
2. 生成图片提示词 → ⏸️ 用户确认
   ↓
3. Dreamina生成图片 → ⏸️ 用户确认
   ↓
4. 生成视频提示词 → ⏸️ 用户确认
   ↓
5. Dreamina生成视频 → ⏸️ 用户确认 + 评分
   ↓
6. 评分≥7 → 自动保存到经验库
```

**启动命令**:
```bash
cd /root/.openclaw/workspace/projects/ad-workflow
python workflows/ad_creation_workflow.py
```

**示例项目**:
- **艾灸贴广告**:
  - 图片: 5404x3040分辨率（消耗4积分）
  - 视频: 1280x720分辨率，5.042秒（消耗10积分）
  - 评分: 9.0/10

**文档**:
- [README.md](./ad-workflow/README.md) - 完整使用文档
- [DIRECTORY.md](./ad-workflow/DIRECTORY.md) - 目录说明

---

### 工作流2: 全自动视频工作流

**路径**: `/root/.openclaw/workspace/projects/auto-video-generation/`

**核心文件**:
- `scripts/fixed_generator.py` - 主执行引擎（14.7KB）
- `scenes.json` - 8个场景配置（7.4KB）
- `start_generation.sh` - 一键启动脚本（1KB）

**工作流程**:
```
1. 加载 scenes.json（8个场景）
   ↓
2. 检查 Dreamina 积分余额
   ↓
3. 按顺序处理每个场景：
   ├─ 生成3张图片（人物肖像+场景）
   ├─ 使用3张图片生成15秒视频
   └─ 记录结果和日志
   ↓
4. 失败场景自动跳过
   ↓
5. 保存结果到 outputs/fixed_results.json
```

**启动命令**:
```bash
# 方式1: 一键启动（后台运行）
cd /root/.openclaw/workspace/projects/auto-video-generation
bash start_generation.sh

# 方式2: 前台运行（查看实时输出）
python3 scripts/fixed_generator.py --start-scene 1

# 方式3: 从指定场景继续
python3 scripts/fixed_generator.py --start-scene 5
```

**实际结果**:
- ✅ 7/8场景成功（场景1-6, 8）
- ❌ 1/8场景失败（场景7 - "隐私数据矛盾"审核不通过）
- 📊 资源消耗: 约150-200积分

**生成的文件**:
- `temp_images/` - 21张图片（7个场景 × 3张）
- `temp_videos/` - 7个视频（15秒/个）
- `outputs/fixed_results.json` - 处理结果汇总
- `logs/fixed_generator.log` - 详细执行日志

**监控命令**:
```bash
# 实时查看日志
tail -f /root/.openclaw/workspace/projects/auto-video-generation/logs/fixed_generator.log

# 查看结果
cat /root/.openclaw/workspace/projects/auto-video-generation/outputs/fixed_results.json

# 检查生成的视频
ls -la /root/.openclaw/workspace/projects/auto-video-generation/temp_videos/
```

---

## 🔧 常用操作

### 检查 Dreamina 积分
```bash
/root/.local/bin/dreamina user_credit
```

### 查看工作流状态
```bash
# 半自动工作流（无后台进程）
ps aux | grep ad_creation_workflow

# 全自动工作流
ps aux | grep fixed_generator
```

### 清理临时文件
```bash
# 半自动工作流（无临时文件）

# 全自动工作流
rm -rf /root/.openclaw/workspace/projects/auto-video-generation/temp_images/*
rm -rf /root/.openclaw/workspace/projects/auto-video-generation/temp_videos/*
```

---

## 📚 相关文档

### 核心文档
- [deerflow+dreamina_DIRECTORIES.md](./deerflow+dreamina_DIRECTORIES.md) - DeerFlow和Dreamina完整目录
- [VIDEO_WORKFLOW_REMINDER.md](./VIDEO_WORKFLOW_REMINDER.md) - 视频制作流程提醒
- [WORKFLOW_STORAGE_ANALYSIS.md](./WORKFLOW_STORAGE_ANALYSIS.md) - 工作流存储方案分析

### 技能文档
- [Dreamina CLI SKILL.md](/root/.dreamina_cli/dreamina/SKILL.md) - Dreamina CLI使用文档
- [DeerFlow README.md](./deerflow-integration/deerflow-repo/README.md) - DeerFlow系统文档

### 经验库
- [ad-workflow/knowledge/prompts/image_prompts.json](./ad-workflow/knowledge/prompts/image_prompts.json) - 图片提示词库
- [ad-workflow/knowledge/prompts/video_prompts.json](./ad-workflow/knowledge/prompts/video_prompts.json) - 视频提示词库

---

## ⚠️ 注意事项

### 积分管理
- **半自动工作流**: 每个广告约消耗10-20积分（可精确控制）
- **全自动工作流**: 每个场景约消耗15-30积分，总计150-200积分
- **建议**: 启动前确保积分余额>1000

### 审核风险
- **敏感内容**: 如"隐私数据矛盾"可能被审核拒绝
- **全自动工作流**: 失败场景会自动跳过，不影响其他场景
- **半自动工作流**: 人工确认可避免审核问题

### 网络依赖
- 两个工作流都需要稳定的网络连接
- 图片/视频下载可能超时
- 建议在网络稳定时运行

### 磁盘空间
- **全自动工作流**: 每个视频约10-20MB，8个场景约100-200MB
- **半自动工作流**: 单个广告约20-30MB
- 建议定期清理临时文件

---

## 🔮 未来扩展

### 计划中的工作流
1. **短视频批量生成工作流** - 基于热点话题自动生成短视频
2. **产品展示工作流** - 专门用于电商产品展示视频
3. **教程视频工作流** - 自动生成教程类视频

### 技术优化
1. **共享经验库** - 合并两个工作流的经验库
2. **智能推荐** - 根据历史数据推荐最佳工作流
3. **质量预测** - 预测生成质量，提前调整参数
4. **成本优化** - 自动选择最经济的生成策略

---

## 📞 支持

如有问题，请查看：
- [ad-workflow/README.md](./ad-workflow/README.md) - 半自动工作流文档
- [Dreamina CLI SKILL.md](/root/.dreamina_cli/dreamina/SKILL.md) - Dreamina CLI文档

---

**维护者**: 贾维斯  
**创建时间**: 2026-04-06 04:08 UTC  
**最后更新**: 2026-04-06 04:08 UTC  
**版本**: v1.0
