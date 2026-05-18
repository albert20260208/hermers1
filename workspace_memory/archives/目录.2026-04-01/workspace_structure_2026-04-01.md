# Workspace 文件夹结构文档

**创建时间**: 2026-04-01 14:00 UTC  
**文档版本**: v1.0  
**生成工具**: OpenClaw AI Assistant (贾维斯)

---

## 📋 目录总览

### 一、核心目录结构
### 二、主要文件夹用途说明
### 三、关联配置文件
### 四、统计概览
### 五、使用建议

---

## 一、核心目录结构

```
workspace/
├── 📂 .agents/                  # Agent技能存储（包括seedance-prompt-en等技能）
│   └── skills/                  # 所有技能文件
├── 📂 .git/                     # Git版本控制仓库（包含分支、提交记录等）
├── 📂 .openclaw/                # OpenClaw运行时配置与缓存
├── 📂 backup/                   # 系统备份目录（包含会话备份等）
├── 📂 data/                     # 数据存储目录
├── 📂 docs/                     # 文档库（包含Seedance API教程、163邮箱指南等）
├── 📂 downloads/                # 下载文件暂存区
├── 📂 knowledge/                # 知识库（分主题存储）
│   ├── bigquant/                # 量化投资知识
│   ├── human/                   # 人类行为/心理学知识
│   ├── stock/                   # 股票投资知识
│   ├── video-business/          # 视频业务知识
│   └── zhouyi/                  # 周易相关知识
├── 📂 memory/                   # 记忆系统（核心存储）
│   ├── archives/                # 历史存档
│   ├── config/                  # 配置文件
│   ├── evolution/               # 进化记录
│   ├── framework/               # 框架文档
│   ├── human/                   # 用户交互记忆
│   ├── indexes/                 # 索引文件
│   ├── journals/                # 日记/日志
│   ├── learning/                # 学习记录
│   ├── plans/                   # 计划/目标
│   ├── projects/                # 项目记忆
│   ├── skills/                  # 技能记忆
│   └── transcripts/             # 对话转录
├── 📂 projects/                 # 项目工作区
│   ├── deerflow-integration/    # DeerFlow集成项目
│   └── hidden-preference-overseas-merged-20260326/  # 隐藏偏好项目
├── 📂 scripts/                  # 自动化脚本库（20+个Python脚本）
│   └── __pycache__/             # Python缓存目录
├── 📂 skills/                   # 本地技能库（除.agents外的补充技能）
│   ├── agent-browser/           # 无头浏览器自动化技能
│   ├── agents/                  # Agent相关技能
│   ├── audio/                   # 音频处理技能
│   ├── capability-evolver/      # 自我进化引擎技能
│   ├── learning/                # 学习技能
│   ├── legal/                   # 法务技能（2026-03-28新增）
│   ├── stock/                   # 股票技能
│   └── video/                   # 视频技能
├── 📂 stocks/                   # 股票数据相关文件
├── 📂 videos/                   # 视频文件存储
└── 📂 work/                     # 临时工作目录
    ├── seedance/                # Seedance视频生成工作区
    └── 塞班项目/                 # "塞班项目"工作区
```

## 二、主要文件夹用途说明

| 文件夹 | 主要用途 | 重要性 |
|--------|----------|--------|
| **`.agents/skills/`** | **核心技能库** - 包含`seedance-prompt-en`等官方技能 | 🔴 核心 |
| **`scripts/`** | **自动化脚本** - 20+个Python脚本（监控、API调用等） | 🔴 核心 |
| **`memory/`** | **记忆系统** - 完整的记忆分层存储，防止压缩丢失 | 🔴 核心 |
| **`knowledge/`** | **知识库** - 按主题分类的结构化知识 | 🟡 重要 |
| **`skills/`** | **本地技能库** - 用户安装的扩展技能（如`capability-evolver`） | 🟡 重要 |
| **`docs/`** | **文档库** - 教程、指南、配置说明 | 🟢 参考 |
| **`projects/`** | **项目工作区** - 正在进行的项目文件 | 🟡 重要 |
| **`data/`** | **数据存储** - 通用数据文件 | 🟢 参考 |
| **`stocks/`** | **股票数据** - 股票相关文件存储 | 🟢 参考 |
| **`videos/`** | **视频文件** - 生成的视频内容 | 🟢 参考 |
| **`downloads/`** | **下载文件** - 临时下载内容 | 🟢 临时 |

## 三、关联配置文件

workspace根目录还有以下重要配置文件：

| 文件 | 用途 | 最后更新 |
|------|------|----------|
| `AGENTS.md` | 工作空间说明、行为准则、响应时间规则 | 2026-03-28 |
| `SOUL.md` | 身份设定 - 贾维斯的性格和行为方式 | 2026-02-10 |
| `USER.md` | 用户信息 - 海哥的基本信息和偏好 | 2026-02-10 |
| `TOOLS.md` | 工具配置 - 火山引擎API密钥、模型ID、常见错误总结 | 2026-03-06 |
| `MEMORY.md` | 长期记忆 - 已安装技能列表和重要事项记录 | 2026-03-28 |
| `HEARTBEAT.md` | 心跳检查配置 - 定期检查和状态保存规则 | 2026-03-30 |
| `NOW.md` | 当前状态 - 持续更新的实时状态记录 | 2026-03-30 |
| `IDENTITY.md` | 身份文件 - 贾维斯的基本信息 | 2026-02-10 |
| `README.md` | 项目说明文档 | 2026-02-18 |

## 四、统计概览

### 📊 整体统计
- **总文件夹数**：约40个（包含嵌套子目录）
- **核心业务目录**：`scripts/`、`memory/`、`knowledge/`、`skills/`
- **技能相关目录**：`.agents/skills/` + `skills/`（共10+个技能）
- **数据存储目录**：`data/`、`stocks/`、`videos/`、`downloads/`
- **项目工作区**：2个正在进行中的项目

### 🛠️ 技能库详情
1. **官方技能** (`/.agents/skills/`)：
   - `seedance-prompt-en` - Seedance 2.0提示词编写技能

2. **本地技能** (`/skills/`)：
   - `agent-browser` - 无头浏览器自动化技能
   - `capability-evolver` - 自我进化引擎技能
   - `legal` - 法务基础技能（2026-03-28新增）
   - `video` - 视频处理技能
   - `stock` - 股票分析技能
   - `audio` - 音频处理技能
   - `learning` - 学习技能
   - `agents` - Agent相关技能

### 📝 脚本库详情
- **监控类脚本**：`moltbook_monitor.py`、`daily_macd_monitor.py`、`news_monitor.py`
- **API类脚本**：`seedance_api.py`、`ocean_video_workflow.py`
- **工具类脚本**：`mail_check.py`、`export_chat.py`、`analyze_future_performance.py`
- **总计**：20+个Python脚本

## 五、使用建议

### 🔧 维护建议
1. **定期备份**：重要数据定期备份到`backup/`目录
2. **记忆维护**：定期检查`memory/`目录，确保记忆系统正常运行
3. **脚本更新**：关注`scripts/`目录下的脚本是否需要更新
4. **知识积累**：在`knowledge/`目录中积累专业知识

### 🚀 开发建议
1. **新技能开发**：放置在`skills/`目录下
2. **项目开发**：使用`projects/`目录进行隔离开发
3. **文档编写**：相关教程放入`docs/`目录
4. **测试环境**：使用`work/`目录进行临时测试

### ⚠️ 注意事项
1. **.git目录**：不要手动修改Git版本控制文件
2. **.openclaw目录**：OpenClaw运行时文件，谨慎操作
3. **__pycache__目录**：Python缓存文件，可定期清理
4. **敏感数据**：API密钥等敏感信息存储在`TOOLS.md`中

---

## 📞 联系方式

如有问题或需要进一步协助，请联系：
- **助理名称**：贾维斯 (Jarvis)
- **运行平台**：OpenClaw
- **工作目录**：`/root/.openclaw/workspace/`

---

*文档生成结束*