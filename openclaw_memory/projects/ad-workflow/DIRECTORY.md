# 📁 广告制作工作流 - 文件目录说明

## 🗂️ 完整目录结构

```
/root/.openclaw/workspace/projects/ad-workflow/
│
├── workflows/                                    # 工作流脚本目录
│   └── ad_creation_workflow.py                  # 主工作流脚本（16KB）
│                                                 # 包含完整的9个节点函数
│
├── knowledge/                                    # 知识库目录
│   ├── prompts/                                 # 提示词经验库
│   │   ├── image_prompts.json                   # 图片提示词库（1.8KB）
│   │   │                                        # 包含3个历史案例 + 2个模板
│   │   └── video_prompts.json                   # 视频提示词库（2.3KB）
│   │                                            # 包含4个历史案例 + 2个模板
│   └── history/                                 # 历史项目记录
│       └── ad_projects/                         # 广告项目存档
│           └── (自动生成的项目文件)
│
├── test_workflow.py                             # 测试脚本（3.1KB）
│                                                # 用于非交互式测试
│
└── README.md                                    # 使用文档（3.4KB）
                                                 # 包含快速开始、技术细节、故障排查
```

## 📄 核心文件说明

### 1. workflows/ad_creation_workflow.py
**路径**: `/root/.openclaw/workspace/projects/ad-workflow/workflows/ad_creation_workflow.py`

**功能**: 主工作流脚本

**包含的函数**:
- `search_similar_prompts()` - 节点1: 经验检索
- `generate_image_prompt_with_experience()` - 节点2: 图片提示词生成
- `show_image_prompt_options()` - 节点3: 图片提示词确认
- `generate_image()` - 节点4: 图片生成
- `wait_image_approval()` - 节点5: 图片确认
- `generate_video_prompt_with_experience()` - 节点6: 视频提示词生成
- `show_video_prompt_options()` - 节点7: 视频提示词确认
- `generate_video()` - 节点8: 视频生成
- `wait_video_approval()` - 节点9: 视频确认和评分
- `save_image_to_experience()` - 保存图片经验
- `save_video_to_experience()` - 保存视频经验
- `run_workflow()` - 主流程入口

**运行方式**:
```bash
cd /root/.openclaw/workspace/projects/ad-workflow
python workflows/ad_creation_workflow.py
```

---

### 2. knowledge/prompts/image_prompts.json
**路径**: `/root/.openclaw/workspace/projects/ad-workflow/knowledge/prompts/image_prompts.json`

**功能**: 图片提示词经验库

**数据结构**:
```json
{
  "prompts": [
    {
      "id": "ip_001",
      "category": "product_showcase",
      "product_type": "智能手表",
      "prompt": "提示词内容",
      "quality_score": 9.2,
      "used_count": 5,
      "created_at": "2026-04-01T10:00:00",
      "tags": ["科技感", "产品特写"],
      "dreamina_params": {...},
      "result_notes": "效果备注"
    }
  ],
  "templates": [...]
}
```

**初始数据**: 3个历史案例（智能手表、运动产品、智能手机）

---

### 3. knowledge/prompts/video_prompts.json
**路径**: `/root/.openclaw/workspace/projects/ad-workflow/knowledge/prompts/video_prompts.json`

**功能**: 视频提示词经验库

**数据结构**: 同 image_prompts.json

**初始数据**: 4个历史案例（产品展示、生活方式、过渡镜头）

---

### 4. test_workflow.py
**路径**: `/root/.openclaw/workspace/projects/ad-workflow/test_workflow.py`

**功能**: 非交互式测试脚本

**测试内容**:
- 经验检索功能
- 提示词生成功能
- 经验库加载功能

**运行方式**:
```bash
cd /root/.openclaw/workspace/projects/ad-workflow
python test_workflow.py
```

---

### 5. README.md
**路径**: `/root/.openclaw/workspace/projects/ad-workflow/README.md`

**功能**: 完整使用文档

**包含内容**:
- 快速开始指南
- 交互流程说明
- 经验库说明
- 技术细节
- 故障排查
- 使用示例

---

## 🔄 工作流执行流程

```
用户输入产品信息
    ↓
[节点1] 搜索相似提示词
    ↓
[节点2] 生成图片提示词 (AI + 经验库)
    ↓
[节点3] 展示选项，等待用户确认 ⏸️
    ↓
[节点4] 调用 Dreamina CLI 生成图片
    ↓
[节点5] 展示图片，等待用户确认 ⏸️
    ↓ (评分≥7自动保存到经验库)
[节点6] 生成视频提示词 (AI + 经验库)
    ↓
[节点7] 展示选项，等待用户确认 ⏸️
    ↓
[节点8] 调用 Dreamina CLI 生成视频
    ↓
[节点9] 展示视频，等待用户评分 ⏸️
    ↓ (评分≥7自动保存到经验库)
完成 🎉
```

## 🎯 关键特性

### 1. 经验库自动匹配
- 根据产品类型和风格标签自动搜索
- 按质量评分排序
- 展示Top 3历史案例

### 2. 多种确认方式
- 使用AI生成
- 选择历史案例
- 手动编辑
- 重新生成

### 3. 自动保存机制
- 评分≥7自动保存到经验库
- 记录使用次数
- 保存效果备注

### 4. Dreamina CLI 集成
- 图片生成: `dreamina image`
- 视频生成: `dreamina video`
- 支持基于图片生成视频

## 📊 测试结果

✅ **经验检索**: 成功匹配智能手表相关案例
✅ **提示词生成**: AI生成符合预期
✅ **经验库加载**: 3个图片案例 + 4个视频案例
✅ **数据结构**: JSON格式正确

## 🚀 下一步集成

### 集成到 DeerFlow
将此工作流集成到 DeerFlow 的 LangGraph 系统：

1. **创建 LangGraph 图**
   ```python
   from langgraph.graph import StateGraph
   
   workflow = StateGraph(AdState)
   workflow.add_node("search", search_similar_prompts)
   workflow.add_node("gen_img_prompt", generate_image_prompt_with_experience)
   # ... 添加其他节点
   ```

2. **添加 interrupt 机制**
   ```python
   def wait_approval(state):
       return interrupt("等待用户确认")
   ```

3. **创建 API 端点**
   ```python
   @app.post("/api/workflows/ad/start")
   async def start_ad_workflow(product_info: str):
       # 启动工作流
   ```

4. **Telegram Bot 集成**
   - 发送提示词选项（带按钮）
   - 接收用户选择
   - 发送生成的图片/视频

## 📞 快速访问

```bash
# 进入项目目录
cd /root/.openclaw/workspace/projects/ad-workflow

# 查看文件列表
ls -lh

# 运行测试
python test_workflow.py

# 查看经验库
cat knowledge/prompts/image_prompts.json | jq
cat knowledge/prompts/video_prompts.json | jq

# 查看文档
cat README.md
```

---

**创建时间**: 2026-04-05 17:57 UTC  
**版本**: v1.0  
**状态**: ✅ 测试通过，可以使用
