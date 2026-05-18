# 📁 DeerFlow + Dreamina 目录和文件汇总

> ⚠️ **重要**: 下次调用 DeerFlow 制作视频时，第一时间阅读此文档！
> 
> 📋 **工作流索引**: 查看 [deerflow_WORKFLOWS_INDEX.md](./deerflow_WORKFLOWS_INDEX.md) 选择合适的工作流
> 
> 本文档包含 DeerFlow 2.0 和 Dreamina CLI 的完整目录结构、配置位置、使用命令。

**创建时间**: 2026-04-05  
**最后更新**: 2026-04-06 04:08 UTC

## 🦌 DeerFlow 2.0 部署目录

### 主项目目录
```
/root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo/
```

### 核心子目录
```
deerflow-repo/
├── backend/                              # 后端服务
│   ├── app/                              # 应用代码
│   │   ├── channels/                     # LangGraph 通道
│   │   └── gateway/                      # Gateway API
│   ├── .venv/                            # Python 虚拟环境
│   ├── pyproject.toml                    # 依赖配置
│   └── uv.lock                           # 锁定文件
│
├── frontend/                             # 前端服务
│   ├── src/                              # React 源码
│   └── node_modules/                     # Node 依赖
│
├── skills/                               # 技能库
│   └── public/                           # 公开技能
│       ├── claude-to-deerflow/           # Claude集成技能
│       ├── image-generation/             # 图像生成技能
│       ├── video-generation/             # 视频生成技能
│       ├── web-search/                   # 网页搜索技能
│       ├── code-execution/               # 代码执行技能
│       └── ... (共16个技能)
│
├── config.yaml                           # 主配置文件
├── .env                                  # 环境变量
├── logs/                                 # 日志目录
├── docker/                               # Docker 配置
├── scripts/                              # 脚本工具
└── README.md                             # 项目文档
```

### 服务端口
- **LangGraph**: http://localhost:2024
- **Gateway API**: http://localhost:8001
- **Frontend**: http://localhost:3000
- **Nginx反向代理**: http://localhost:2026 (主入口)

### 关键配置文件
- **模型配置**: `config.yaml` (豆包 + Gemini 2.5 Flash)
- **环境变量**: `.env` (API密钥)
- **技能配置**: `skills/public/*/SKILL.md`

---

## 🎨 Dreamina CLI 目录

### 安装位置
```
/root/.local/bin/dreamina                 # 可执行文件
```

### 配置和缓存
```
/root/.dreamina_cli/                      # Dreamina CLI 主目录
├── dreamina/
│   ├── SKILL.md                          # 技能文档
│   └── credentials/                      # 登录凭证
└── cache/                                # 缓存文件
```

### 登录信息
- **UID**: 2226944428480220
- **VIP等级**: maestro
- **剩余积分**: 15,341 (截至今天)

---

## 🎬 广告制作工作流目录

### 项目主目录
```
/root/.openclaw/workspace/projects/ad-workflow/
```

### 完整结构
```
ad-workflow/
├── workflows/                            # 工作流脚本
│   └── ad_creation_workflow.py           # 主工作流 (16KB)
│                                         # 包含9个节点函数
│
├── knowledge/                            # 知识库
│   ├── prompts/                          # 提示词经验库
│   │   ├── image_prompts.json            # 图片提示词库
│   │   │                                 # 3个历史案例 + 2个模板
│   │   └── video_prompts.json            # 视频提示词库
│   │                                     # 4个历史案例 + 2个模板
│   └── history/                          # 历史项目
│       └── ad_projects/                  # 广告项目存档
│
├── test_workflow.py                      # 测试脚本 (3.1KB)
├── create_moxibustion_ad.py              # 艾灸贴广告脚本 (3.2KB)
├── README.md                             # 使用文档 (3.4KB)
└── DIRECTORY.md                          # 目录说明 (4.8KB)
```

### 工作流特性
- ✅ 经验库自动匹配
- ✅ 4个人工确认环节
- ✅ 自动保存高分案例
- ✅ Dreamina CLI 集成

---

## 📦 今天生成的文件

### 艾灸贴广告素材
```
/tmp/moxibustion_ad_image.png             # 产品图片
  - 尺寸: 5404x3040 (16:9)
  - 消耗积分: 4
  - 任务ID: 296bf5e653d6e752

/tmp/moxibustion_ad_video.mp4             # 广告视频
  - 分辨率: 1280x720 (720p)
  - 时长: 5.042秒
  - 帧率: 24fps
  - 消耗积分: 10
  - 任务ID: 44017a1be6495b86
```

### 提示词记录
**图片提示词**:
```
温馨的居家场景，年轻女性坐在沙发上，
将艾灸贴轻松贴在肩颈部位，
脸上露出舒适放松的表情，
暖色调光线，温馨氛围，
生活方式摄影风格，自然光线
```

**视频提示词**:
```
镜头从产品包装特写开始，
女性手部撕开艾灸贴包装，
轻松贴在肩颈部位，
脸部表情从疲惫到舒适放松的转变，
温暖的光效从贴敷处扩散，
最后展示产品包装和品牌名称，
温馨暖色调，生活方式广告风格
```

---

## 🔧 配置文件位置

### DeerFlow 配置
```
/root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo/config.yaml
/root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo/.env
```

### 关键环境变量
```bash
# 火山引擎豆包模型
VOLCENGINE_API_KEY=d380aed6-916e-4542-bd67-a20bbd1b377c

# Google Gemini 模型
GEMINI_API_KEY=AIzaSyAADWZNNr-IN2wvXm2QSG1MKp0JEyrR4Iw
```

### 模型配置
- **豆包**: `doubao-1-5-pro-32k-250115`
- **Gemini**: `gemini-2.5-flash-preview-04-17` (支持思考推理)

---

## 📚 文档位置

### DeerFlow 文档
```
/root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo/README.md
/root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo/backend/README.md
/root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo/backend/CLAUDE.md
```

### Dreamina 文档
```
/root/.dreamina_cli/dreamina/SKILL.md
```

### 工作流文档
```
/root/.openclaw/workspace/projects/ad-workflow/README.md
/root/.openclaw/workspace/projects/ad-workflow/DIRECTORY.md
```

---

## 🎯 快速访问命令

### 目录导航
```bash
# 进入 DeerFlow 目录
cd /root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo

# 进入广告工作流目录
cd /root/.openclaw/workspace/projects/ad-workflow

# 查看生成的素材
ls -lh /tmp/moxibustion_ad_*
```

### Dreamina CLI 命令
```bash
# 查看帮助
dreamina --help

# 查看用户积分
dreamina user_credit

# 查看任务列表
dreamina list_task

# 查询任务结果
dreamina query_result --submit_id=<任务ID>

# 生成图片
dreamina text2image --prompt "提示词" --ratio 16:9

# 生成视频
dreamina text2video --prompt "提示词"
```

### DeerFlow 服务管理
```bash
# 查看服务状态
cd /root/.openclaw/workspace/projects/deerflow-integration/deerflow-repo
make status

# 启动服务
make up

# 停止服务
make down

# 查看日志
make logs
```

---

## 📊 今天的成果总结

### ✅ 完成的工作

1. **DeerFlow 2.0 部署**
   - 4个服务正常运行
   - 16个技能可用
   - 双模型集成（豆包 + Gemini）

2. **Dreamina CLI 集成**
   - 成功登录（maestro VIP）
   - 掌握所有生成命令
   - 完成首个广告案例

3. **广告工作流系统**
   - 完整的9节点工作流
   - 经验库系统（图片+视频）
   - 自动化脚本

4. **艾灸贴广告**
   - 产品图片（5K分辨率）
   - 广告视频（5秒720p）
   - 配套文案

### 📈 资源消耗
- **积分消耗**: 14积分（图片4 + 视频10）
- **剩余积分**: 15,341
- **生成时间**: 图片~40秒，视频~3分钟

### 🎯 下一步计划
1. 集成工作流到 DeerFlow 的 LangGraph
2. 添加 Telegram Bot 交互
3. 实现批量生成功能
4. 优化提示词生成（接入豆包模型）

---

**创建时间**: 2026-04-05  
**最后更新**: 2026-04-05 18:30 UTC  
**文档版本**: v1.1  
**维护者**: 贾维斯

---

## 🚀 快速开始指南

### 制作视频的完整流程

1. **阅读本文档** - 了解目录结构和命令
2. **检查服务状态** - 确保 DeerFlow 服务运行
3. **确认积分余额** - `dreamina user_credit`
4. **运行工作流** - 使用 `ad_creation_workflow.py` 或自定义脚本
5. **查询任务结果** - `dreamina query_result --submit_id=<任务ID>`

---
