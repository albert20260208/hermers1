# DeerFlow 整合项目 - 贾维斯控制层

## 项目概述

**DeerFlow整合项目**是一个基于字节跳动开源的DeerFlow 2.0框架的多模型AI工作流自动化平台。我（贾维斯）作为控制层，负责任务分解、模型调度和结果整合，实现高效的多模型协作工作流。

## 🎯 核心目标

1. **建立控制层架构**：我作为智能调度中心，协调多个AI模型协作
2. **实现工作流自动化**：为《偏爱难藏》等项目提供端到端的视频生成解决方案
3. **优化模型使用**：根据任务类型智能选择最佳模型（DeepSeek/Opus/Minimax/Seedance）
4. **降低成本提高效率**：通过自动化流程减少人工干预，提升内容产出效率

## 🏗️ 系统架构

```
用户指令 → 贾维斯(控制层) → 任务分解 → 模型调度 → 结果整合 → 用户输出
        ↓           ↓           ↓           ↓
   任务理解    子任务分配    API调用管理   质量检查
        ↓           ↓           ↓           ↓
   优先级排序  模型选择策略  错误重试机制  格式标准化
```

### 模型分工

| 模型 | 擅长领域 | 使用场景 |
|------|----------|----------|
| **DeepSeek** | 日常对话、技术咨询、代码编写 | 基础任务、优化工作 |
| **Opus (Claude 3.5)** | 深度分析、复杂推理、逻辑思维 | 剧本分析、战略规划 |
| **Minimax** | 中文创作、对话生成、内容创作 | 对话生成、提示词创作 |
| **Seedance** | 视频生成、图像生成 | 视频内容产出 |

## 📁 项目结构

```
deerflow-integration/
├── src/                    # 源代码
│   ├── controller/        # 控制层核心
│   │   └── deerflow_controller.py
│   ├── models/           # 模型客户端（待实现）
│   ├── tasks/           # 任务定义（待实现）
│   └── utils/           # 工具函数（待实现）
├── config/               # 配置文件
│   ├── project_config.yaml
│   └── deerflow_config.yaml
├── tests/               # 测试代码
│   └── test_controller.py
├── workflows/           # 工作流定义（待实现）
├── docs/               # 文档
├── scripts/            # 脚本
│   └── start_controller.py
├── logs/               # 日志文件
├── data/               # 数据存储
└── deerflow-repo/      # DeerFlow 2.0源代码
```

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 22+ (用于DeerFlow前端)
- pnpm、uv、nginx (用于DeerFlow完整部署)

### 安装步骤

1. **克隆项目** (已完成)
```bash
cd /root/.openclaw/workspace/projects/deerflow-integration
```

2. **安装DeerFlow依赖** (进行中)
```bash
cd deerflow-repo
make install
```

3. **运行控制层测试**
```bash
python scripts/start_controller.py --test
```

4. **运行演示任务**
```bash
python scripts/start_controller.py --demo
```

### 运行单个任务

```bash
# 对话生成任务
python scripts/start_controller.py --task "dialog:生成男女主角对峙对话" --input '{"scene":"订婚宴","emotion":"紧张"}'

# 视频生成任务
python scripts/start_controller.py --task "video:生成算法反转场景视频" --input '{"style":"紧张悬疑"}'

# 提示词生成任务
python scripts/start_controller.py --task "prompt:生成Seedance视频提示词" --input '{"requirements":"不要字幕，电影感"}'
```

## 📋 任务类型

### 1. 对话生成 (dialog_generation)
- **描述**：生成角色对话内容
- **工作流**：情感分析 → 风格设定 → 对话生成 → 对话优化
- **使用模型**：Opus → Minimax → Minimax → DeepSeek
- **适用场景**：《偏爱难藏》角色对话、剧情对话

### 2. 视频生成 (video_generation)
- **描述**：生成视频内容
- **工作流**：场景分析 → 分镜设计 → 提示词生成 → 视频生成
- **使用模型**：Opus → Minimax → Minimax → Seedance
- **适用场景**：短视频制作、剧情片段

### 3. 提示词生成 (prompt_generation)
- **描述**：生成AI视频生成提示词
- **工作流**：场景理解 → 镜头设计 → 提示词生成
- **使用模型**：DeepSeek → Opus → Minimax
- **适用场景**：Seedance、DALL-E等AI视频生成工具

### 4. 文本分析 (text_analysis)
- **描述**：深度文本分析
- **工作流**：单任务处理
- **使用模型**：Opus
- **适用场景**：剧本分析、情感分析、逻辑分析

### 5. 场景设计 (scene_design)
- **描述**：设计场景和镜头
- **工作流**：单任务处理
- **使用模型**：Minimax
- **适用场景**：分镜设计、场景描述

## 🔧 技术实现

### 控制层核心类

```python
class DeerFlowController:
    """控制层核心"""
    async def process_task(self, task_type, description, input_data):
        # 1. 任务分解
        subtasks = self.task_decomposer.decompose(...)
        
        # 2. 执行子任务
        results = []
        for subtask in subtasks:
            result = await self.execute_subtask(subtask)
            results.append(result)
        
        # 3. 结果整合
        final_result = self.result_integrator.integrate(...)
        
        return final_result
```

### 任务分解策略

根据任务类型自动分解为合适的子任务：
- **视频生成**：4个子任务（分析→设计→提示词→生成）
- **对话生成**：4个子任务（情感→风格→生成→优化）
- **提示词生成**：3个子任务（理解→设计→生成）

### 模型选择规则

```python
model_rules = {
    TaskType.TEXT_ANALYSIS: ModelType.OPUS,
    TaskType.DIALOG_GENERATION: ModelType.MINIMAX,
    TaskType.SCENE_DESIGN: ModelType.MINIMAX,
    TaskType.PROMPT_GENERATION: ModelType.MINIMAX,
    TaskType.VIDEO_GENERATION: ModelType.SEEDANCE,
}
```

## 🎬 《偏爱难藏》项目应用

### 项目状态
- ✅ 收到完整大纲文件（80集AI融合剧情）
- ✅ 四面墙场景一致性方法验证成功
- 🔄 等待AI安全知识融入反馈
- 🚀 准备开始视频生成工作流

### 优先工作流

1. **角色对话生成工作流**
   ```
   输入：场景描述 → Opus(情感分析) → Minimax(风格设定) → Minimax(对话生成) → DeepSeek(优化) → 输出：对话脚本
   ```

2. **关键场景视频生成工作流**
   ```
   输入：剧本片段 → Opus(场景分析) → Minimax(分镜设计) → Minimax(提示词生成) → Seedance(视频生成) → 输出：视频文件
   ```

3. **批量内容生产流水线**
   ```
   80集大纲 → 分集处理 → 并行生成 → 质量检查 → 成品输出
   ```

## 📊 性能指标

### 第一阶段目标（2周内）
- ✅ 控制层基础框架完成
- 🔄 DeerFlow环境部署
- ⏳ 《偏爱难藏》首个工作流测试
- ⏳ 性能测试和优化

### 成功指标
- 任务分解准确率 > 90%
- 子任务执行成功率 > 95%
- 平均任务完成时间 < 10分钟（简单任务）
- 视频生成质量达到可接受水平

## 🔄 开发计划

### 第一阶段：基础框架（当前）
- [x] 控制层架构设计
- [x] 任务分解器实现
- [x] 模型选择器实现
- [x] 结果整合器实现
- [x] 基础测试套件
- [ ] DeerFlow环境部署
- [ ] 模型API客户端

### 第二阶段：功能完善（1-2周）
- [ ] 实际模型API集成
- [ ] 《偏爱难藏》工作流实现
- [ ] 错误处理和重试机制
- [ ] 性能监控和日志系统
- [ ] REST API接口

### 第三阶段：生产部署（2-3周）
- [ ] Docker容器化
- [ ] 自动化测试流水线
- [ ] 生产环境配置
- [ ] 监控和告警系统
- [ ] 用户界面（可选）

## 🛠️ 开发和测试

### 运行测试
```bash
# 运行所有测试
python tests/test_controller.py

# 通过脚本运行测试
python scripts/start_controller.py --test
```

### 代码规范
- 使用Python类型提示
- 遵循PEP 8代码风格
- 模块化设计，高内聚低耦合
- 完善的错误处理和日志记录

### 提交规范
- feat: 新功能
- fix: 修复问题
- docs: 文档更新
- test: 测试相关
- refactor: 代码重构
- chore: 构建过程或辅助工具变动

## 📝 配置说明

### 项目配置 (config/project_config.yaml)
包含模型配置、任务类型、工作流定义、性能参数等。

### DeerFlow配置 (deerflow-repo/config.yaml)
DeerFlow框架的配置，包括模型API密钥、服务器设置等。

### 环境变量 (.env)
API密钥等敏感信息通过环境变量管理。

## 🤝 贡献指南

1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开Pull Request

## 📄 许可证

本项目基于MIT许可证开源。

## 🙏 致谢

- **字节跳动**：开源DeerFlow 2.0框架
- **海哥**：项目指导和支持
- **DeepSeek/Opus/Minimax/火山引擎**：提供优秀的AI模型

## 📞 联系和支持

- 项目维护者：贾维斯 (Jarvis)
- 项目发起人：海哥 (@ahaius)
- 创建时间：2026-03-25
- 项目状态：活跃开发中

---

**最后更新**: 2026-03-25  
**版本**: v1.0.0  
**状态**: 🟢 环境部署中