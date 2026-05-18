# 广告制作工作流系统

## 📁 目录结构

```
/root/.openclaw/workspace/projects/ad-workflow/
├── workflows/
│   └── ad_creation_workflow.py          # 主工作流脚本
├── knowledge/
│   ├── prompts/
│   │   ├── image_prompts.json           # 图片提示词经验库
│   │   └── video_prompts.json           # 视频提示词经验库
│   └── history/
│       └── ad_projects/                 # 历史项目记录
└── README.md                            # 本文件
```

## 🚀 快速开始

### 1. 运行工作流

```bash
cd /root/.openclaw/workspace/projects/ad-workflow
python workflows/ad_creation_workflow.py
```

### 2. 交互流程

工作流会依次引导你完成以下步骤：

#### 阶段0: 输入产品信息
```
产品名称: 智能手表X1
产品类型: 智能手表
广告风格: 科技感
```

#### 阶段1: 图片提示词确认
- 系统会展示AI生成的提示词
- 同时展示历史高分案例（Top 3）
- 你可以选择：
  - `0` - 使用AI生成
  - `1-3` - 使用历史案例
  - `e` - 手动编辑
  - `r` - 重新生成

#### 阶段2: 图片生成确认
- 系统调用 Dreamina CLI 生成图片
- 你可以选择：
  - `y` - 满意，继续
  - `n` - 重新生成
  - `e` - 调整提示词

#### 阶段3: 视频提示词确认
- 系统基于图片生成视频提示词
- 同时展示历史高分案例
- 操作同阶段1

#### 阶段4: 视频生成确认
- 系统调用 Dreamina CLI 生成视频
- 你需要评分（1-10分）
- 评分≥7会自动保存到经验库

## 📚 经验库说明

### 图片提示词库 (image_prompts.json)

包含历史成功的图片提示词，每条记录包括：
- `prompt`: 提示词内容
- `quality_score`: 质量评分（1-10）
- `used_count`: 使用次数
- `tags`: 标签（用于搜索匹配）
- `result_notes`: 效果备注

### 视频提示词库 (video_prompts.json)

包含历史成功的视频提示词，结构同上。

### 自动匹配逻辑

系统会根据以下条件匹配历史案例：
1. **产品类型匹配** (+10分)
2. **风格标签匹配** (+5分)
3. **按质量评分排序**

最终展示评分最高的Top 3案例。

## 🔧 技术细节

### Dreamina CLI 调用

#### 图片生成
```bash
dreamina image \
  --prompt "提示词" \
  --aspect-ratio "16:9" \
  --output "/tmp/ad_image.jpg"
```

#### 视频生成（基于图片）
```bash
dreamina video \
  --image "/tmp/ad_image.jpg" \
  --prompt "视频提示词" \
  --duration "5" \
  --output "/tmp/ad_video.mp4"
```

### 经验库保存条件

- **图片**: 用户主动评分≥7时保存
- **视频**: 评分≥7时自动保存

保存的信息包括：
- 提示词内容
- 质量评分
- 产品类型
- 风格标签
- Dreamina参数
- 效果备注

## 📊 工作流状态

工作流使用字典管理状态，主要字段：

```python
{
    "product_info": "智能手表X1",
    "product_type": "智能手表",
    "style": "科技感",
    
    "similar_image_prompts": [...],  # 匹配的历史图片提示词
    "similar_video_prompts": [...],  # 匹配的历史视频提示词
    
    "image_prompt": "...",           # 当前图片提示词
    "image_prompt_approved": True,   # 是否已确认
    "image_file": "/tmp/xxx.jpg",    # 生成的图片路径
    "image_approved": True,          # 图片是否满意
    
    "video_prompt": "...",           # 当前视频提示词
    "video_prompt_approved": True,   # 是否已确认
    "video_file": "/tmp/xxx.mp4",    # 生成的视频路径
    "video_approved": True,          # 视频是否满意
    "video_quality_score": 8.5       # 视频评分
}
```

## 🎯 下一步优化

### 1. 集成到 DeerFlow
将工作流集成到 DeerFlow 的 LangGraph 系统中，实现：
- Web UI 交互
- Telegram Bot 交互
- 状态持久化

### 2. LLM 集成
当前提示词生成是基于模板的，可以集成：
- 豆包模型（文案生成）
- Gemini 2.5 Flash（质量审核）

### 3. 批量处理
支持一次性生成多个场景的图片和视频。

### 4. 模板系统
基于经验库自动提取最佳实践模板。

## 🐛 故障排查

### Dreamina CLI 未找到
```bash
# 检查安装
which dreamina

# 重新安装
curl -s https://jimeng.jianying.com/cli | bash
```

### 登录态过期
```bash
# 重新登录
dreamina login

# 或导入登录态
dreamina import_login_response --file login.json
```

### 经验库损坏
```bash
# 备份当前数据
cp knowledge/prompts/*.json knowledge/prompts/backup/

# 重新初始化（会丢失数据）
rm knowledge/prompts/*.json
# 重新运行工作流会自动创建空库
```

## 📝 使用示例

### 示例1: 智能手表广告

**输入**:
- 产品: 智能手表X1
- 类型: 智能手表
- 风格: 科技感

**输出**:
- 图片: 黑色背景下的手表特写，蓝色光效
- 视频: 镜头推进，屏幕数据动态变化
- 评分: 9.0/10

### 示例2: 运动鞋广告

**输入**:
- 产品: 跑步鞋Pro
- 类型: 运动产品
- 风格: 生活方式

**输出**:
- 图片: 户外场景，自然光线
- 视频: 慢动作跑步镜头
- 评分: 8.5/10

## 📞 支持

如有问题，请查看：
- Dreamina CLI 文档: `/root/.dreamina_cli/dreamina/SKILL.md`
- DeerFlow 文档: `/root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo/README.md`
