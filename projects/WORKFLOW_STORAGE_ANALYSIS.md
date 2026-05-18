# 🎬 视频工作流存储方案分析与建议

**分析时间**: 2026-04-06 03:51 UTC  
**分析对象**: 两个视频生成工作流（半自动广告工作流 + 全自动视频工作流）  
**目标**: 设计最佳存储方案，确保下次选择执行时不会遗忘各个环节

---

## 📊 当前文件位置分析

### 工作流1: 半自动广告工作流（带4个人工确认环节）

**当前位置**: `/root/.openclaw/workspace/projects/ad-workflow/`

**文件结构**:
```
ad-workflow/
├── workflows/
│   └── ad_creation_workflow.py          # 主工作流脚本 (16KB)
├── knowledge/
│   ├── prompts/
│   │   ├── image_prompts.json           # 图片提示词经验库 (3案例+2模板)
│   │   └── video_prompts.json           # 视频提示词经验库 (4案例+2模板)
│   └── history/
│       └── ad_projects/                 # 历史项目记录
├── create_moxibustion_ad.py             # 示例项目：艾灸贴广告 (3.2KB)
├── test_workflow.py                     # 测试脚本 (3.1KB)
├── README.md                            # 完整文档
└── DIRECTORY.md                         # 目录说明
```

**核心特点**:
- ⏸️ 4个人工确认环节（图片提示词、图片、视频提示词、视频）
- 📚 经验库系统（自动匹配历史案例）
- 🎯 适合商业广告制作
- 💰 精确控制积分消耗

---

### 工作流2: 全自动视频工作流（《偏爱难藏》硅谷AI版）

**当前位置**: `/root/.openclaw/workspace/projects/auto-video-generation/`

**文件结构**:
```
auto-video-generation/
├── scripts/
│   ├── fixed_generator.py               # 主执行引擎 (14.7KB)
│   ├── auto_video_generator.py          # 旧版本
│   └── auto_video_generator_v2.py       # V2版本
├── scenes.json                          # 8个场景配置 (7.4KB)
├── start_generation.sh                  # 一键启动脚本 (1KB)
├── temp_images/                         # 生成的图片 (21张)
├── temp_videos/                         # 生成的视频 (7个)
├── outputs/
│   ├── fixed_results.json               # 处理结果汇总
│   └── generation_results_v2.json       # V2结果
└── logs/
    ├── fixed_generator.log              # 详细执行日志
    ├── auto_video_v2.log
    └── test_run.log
```

**核心特点**:
- ⚡ 完全自动化，无人工干预
- 📖 剧本驱动（8个场景）
- 🎨 多参考图技术（每场景3张图片）
- 🔄 智能容错（失败自动跳过）

---

## 🚨 当前存储问题

### 问题1: 分散存储，难以对比
- 两个工作流在不同目录
- 没有统一的入口文档
- 选择时需要记忆两个路径

### 问题2: 缺少快速选择指南
- 没有"何时用哪个工作流"的决策树
- 缺少一键启动命令汇总
- 没有对比表格

### 问题3: 文档分散
- README.md 在各自目录
- 没有统一的工作流索引
- 缺少版本管理

### 问题4: 经验库不共享
- 两个工作流的经验库独立
- 无法互相学习和优化
- 重复积累知识

---

## 💡 推荐存储方案

### 方案A: 统一工作流库（推荐 ⭐⭐⭐⭐⭐）

**核心思想**: 创建一个统一的工作流管理系统，所有工作流作为"模板"存储

**目录结构**:
```
/root/.openclaw/workspace/workflows/
├── README.md                            # 工作流总索引（核心文档）
├── QUICKSTART.md                        # 快速选择指南
├── templates/
│   ├── ad-workflow/                     # 半自动广告工作流
│   │   ├── WORKFLOW.md                  # 工作流说明
│   │   ├── workflow.py                  # 主脚本
│   │   ├── config.json                  # 配置文件
│   │   └── examples/                    # 示例项目
│   └── auto-video-generation/           # 全自动视频工作流
│       ├── WORKFLOW.md                  # 工作流说明
│       ├── generator.py                 # 主脚本
│       ├── scenes.json                  # 场景配置
│       └── examples/                    # 示例项目
├── shared/
│   ├── knowledge/                       # 共享经验库
│   │   ├── image_prompts.json
│   │   └── video_prompts.json
│   └── utils/                           # 共享工具函数
├── active-projects/                     # 当前活跃项目
│   ├── moxibustion-ad/                  # 艾灸贴广告
│   └── silicon-valley-ai/               # 硅谷AI视频
└── archive/                             # 已完成项目归档
```

**核心文件: README.md**
```markdown
# 🎬 视频工作流管理系统

## 快速选择

| 需求 | 推荐工作流 | 启动命令 |
|------|-----------|---------|
| 商业广告制作 | ad-workflow | `workflow run ad` |
| 批量视频生成 | auto-video | `workflow run auto` |
| 剧本场景视频 | auto-video | `workflow run auto --scenes scenes.json` |

## 工作流对比

| 特性 | ad-workflow | auto-video |
|------|------------|-----------|
| 自动化程度 | ⏸️ 4个确认环节 | ⚡ 完全自动 |
| 输入 | 产品信息+风格 | 完整剧本 |
| 输出 | 1个高质量广告 | 8个15秒视频 |
| 经验库 | ✅ 图片+视频 | ⚠️ 剧本场景 |
| 适合场景 | 商业广告 | 批量生成 |
```

**优势**:
- ✅ 统一入口，一目了然
- ✅ 快速选择指南
- ✅ 共享经验库
- ✅ 版本管理清晰
- ✅ 易于扩展新工作流

**实施步骤**:
1. 创建 `/root/.openclaw/workspace/workflows/` 目录
2. 移动现有工作流到 `templates/`
3. 创建统一的 README.md 和 QUICKSTART.md
4. 合并经验库到 `shared/knowledge/`
5. 创建 `workflow` CLI 工具（可选）

---

### 方案B: 保持现状 + 增强索引（次选 ⭐⭐⭐⭐）

**核心思想**: 保持现有目录结构，但创建统一的索引文档

**新增文件**:
```
/root/.openclaw/workspace/projects/
├── WORKFLOWS_INDEX.md                   # 工作流总索引（新增）
├── ad-workflow/                         # 保持不变
└── auto-video-generation/               # 保持不变
```

**核心文件: WORKFLOWS_INDEX.md**
```markdown
# 🎬 视频工作流索引

## 快速导航

### 工作流1: 半自动广告工作流
- **路径**: `/root/.openclaw/workspace/projects/ad-workflow/`
- **启动**: `cd ad-workflow && python workflows/ad_creation_workflow.py`
- **适合**: 商业广告制作，需要人工确认质量
- **文档**: [README.md](./ad-workflow/README.md)

### 工作流2: 全自动视频工作流
- **路径**: `/root/.openclaw/workspace/projects/auto-video-generation/`
- **启动**: `cd auto-video-generation && bash start_generation.sh`
- **适合**: 批量视频生成，剧本驱动
- **文档**: [README.md](./auto-video-generation/README.md)

## 决策树

```
需要生成视频？
├─ 是商业广告？
│  ├─ 是 → 使用 ad-workflow（半自动，4个确认环节）
│  └─ 否 → 继续判断
└─ 是批量生成？
   ├─ 是 → 使用 auto-video（全自动，8个场景）
   └─ 否 → 根据具体需求选择
```
```

**优势**:
- ✅ 不破坏现有结构
- ✅ 快速实施
- ✅ 统一入口文档
- ⚠️ 经验库仍然分散

**实施步骤**:
1. 创建 `WORKFLOWS_INDEX.md`
2. 在 `deerflow+dreamina_DIRECTORIES.md` 中添加链接
3. 更新 `VIDEO_WORKFLOW_REMINDER.md`

---

### 方案C: 技能化封装（未来方向 ⭐⭐⭐）

**核心思想**: 将两个工作流封装成 OpenClaw 技能

**目录结构**:
```
/root/.openclaw/workspace/skills/
├── video-ad-workflow/                   # 技能1
│   ├── SKILL.md
│   ├── workflow.py
│   └── knowledge/
└── video-auto-generation/               # 技能2
    ├── SKILL.md
    ├── generator.py
    └── scenes/
```

**优势**:
- ✅ 符合 OpenClaw 技能体系
- ✅ 可以通过 `agents_list` 调用
- ✅ 易于分享和复用
- ⚠️ 需要重构代码

**实施步骤**:
1. 创建技能目录结构
2. 编写 SKILL.md
3. 重构代码为技能格式
4. 测试技能调用

---

## 🎯 最终推荐

### 立即实施: 方案B（保持现状 + 增强索引）

**原因**:
1. **最小改动**: 不破坏现有结构，风险低
2. **快速见效**: 10分钟内完成
3. **解决核心问题**: 提供统一入口和快速选择指南

**实施清单**:
- [ ] 创建 `/root/.openclaw/workspace/projects/WORKFLOWS_INDEX.md`
- [ ] 添加决策树和快速启动命令
- [ ] 在 `deerflow+dreamina_DIRECTORIES.md` 中添加链接
- [ ] 更新 `VIDEO_WORKFLOW_REMINDER.md`

---

### 中期优化: 方案A（统一工作流库）

**时机**: 当有第3个工作流时

**原因**:
1. **可扩展性**: 易于添加新工作流
2. **共享经验库**: 避免重复积累知识
3. **版本管理**: 清晰的模板和项目分离

**实施清单**:
- [ ] 创建 `/root/.openclaw/workspace/workflows/` 目录
- [ ] 迁移现有工作流到 `templates/`
- [ ] 合并经验库到 `shared/knowledge/`
- [ ] 创建统一的 CLI 工具

---

### 长期规划: 方案C（技能化封装）

**时机**: 当工作流稳定且需要分享时

**原因**:
1. **标准化**: 符合 OpenClaw 技能体系
2. **可复用**: 易于分享给其他用户
3. **集成性**: 可以与其他技能组合

---

## 📋 增强索引文档模板

### WORKFLOWS_INDEX.md 完整内容

```markdown
# 🎬 视频工作流索引

**最后更新**: 2026-04-06 03:51 UTC  
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
              ├─ 是商业广告？
              │  ├─ 是 → 【半自动广告工作流】
              │  │       - 需要精确控制质量
              │  │       - 预算有限（精确控制积分）
              │  │       - 单个高质量视频
              │  │
              │  └─ 否 → 继续判断
              │
              ├─ 是批量生成？
              │  ├─ 是 → 【全自动视频工作流】
              │  │       - 有完整剧本
              │  │       - 需要多个场景视频
              │  │       - 可接受部分失败
              │  │
              │  └─ 否 → 根据具体需求选择
              │
              └─ 特殊需求？
                 ├─ 需要经验库匹配 → 【半自动】
                 ├─ 需要完全自动化 → 【全自动】
                 └─ 不确定 → 先用【半自动】测试
```

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
- [auto-video-generation/README.md](./auto-video-generation/README.md) - 全自动工作流文档（待创建）
- [Dreamina CLI SKILL.md](/root/.dreamina_cli/dreamina/SKILL.md) - Dreamina CLI文档

---

**维护者**: 贾维斯  
**创建时间**: 2026-04-06 03:51 UTC  
**最后更新**: 2026-04-06 03:51 UTC
```

---

## 🎯 立即行动清单

### 第1步: 创建索引文档（5分钟）
```bash
# 创建 WORKFLOWS_INDEX.md
cat > /root/.openclaw/workspace/projects/WORKFLOWS_INDEX.md << 'EOF'
[上面的完整内容]
EOF
```

### 第2步: 更新提醒文档（2分钟）
在 `VIDEO_WORKFLOW_REMINDER.md` 开头添加：
```markdown
⚠️ 重要: 选择工作流前，先阅读 [WORKFLOWS_INDEX.md](./WORKFLOWS_INDEX.md)
```

### 第3步: 更新目录文档（2分钟）
在 `deerflow+dreamina_DIRECTORIES.md` 中添加：
```markdown
## 🎬 视频工作流索引
详见: [WORKFLOWS_INDEX.md](./WORKFLOWS_INDEX.md)
```

### 第4步: 创建快速别名（1分钟）
```bash
# 添加到 ~/.bashrc
echo "alias workflow-ad='cd /root/.openclaw/workspace/projects/ad-workflow && python workflows/ad_creation_workflow.py'" >> ~/.bashrc
echo "alias workflow-auto='cd /root/.openclaw/workspace/projects/auto-video-generation && bash start_generation.sh'" >> ~/.bashrc
source ~/.bashrc
```

---

## 📊 方案对比总结

| 方案 | 实施难度 | 实施时间 | 可扩展性 | 推荐度 |
|------|---------|---------|---------|--------|
| **方案A: 统一工作流库** | 中 | 2-3小时 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **方案B: 增强索引** | 低 | 10分钟 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **方案C: 技能化封装** | 高 | 1-2天 | ⭐⭐⭐⭐ | ⭐⭐⭐ |

**最终建议**: 
1. **立即实施方案B**（10分钟解决当前问题）
2. **中期迁移到方案A**（当有第3个工作流时）
3. **长期考虑方案C**（当工作流稳定且需要分享时）

---

**分析完成时间**: 2026-04-06 03:51 UTC  
**下一步**: 等待用户确认方案，立即实施
