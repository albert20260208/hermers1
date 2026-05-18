# 此目录已迁移

> 技能知识库已迁移到新的技能库结构中

---

## 📍 迁移目的地

原 `memory/skills/` 目录中的内容已按新框架迁移：

### 1. 技能索引 → `skills/README.md`
- 技能分类结构、调用规则等

### 2. 股票技能 → `skills/stock/`
- `indicators.md` - 技术指标知识
- `knowledge-base.md` - 股票量化知识库（13个核心知识点）

### 3. 视频技能 → `skills/video/`
- `seedance/` 目录 - Seedance视频生成全套技能
  - `api.md` - API配置、定价
  - `prompts.md` - 提示词技巧、镜头语言
  - `complete-guide.md` - 完整指南

### 4. 实习生区 → `skills/learning/`
- 正在学习的技能、实验性代码（暂时为空）

---

## 🔄 新技能库架构

### 分层结构
```
skills/
├── learning/          # 实习生区（正在实践）
├── stock/            # 正式股票技能（已掌握）
├── video/            # 正式视频技能（已掌握）
└── README.md         # 技能总览
```

### 技能状态演进
1. **学习资料** (`knowledge/`) → 理论学习
2. **实践阶段** (`skills/learning/`) → 实验验证
3. **掌握阶段** (`skills/`) → 成品技能
4. **核心记忆** (`MEMORY.md`) → 长期经验

---

## 📋 如何使用新结构

### 调用现有技能
- **股票相关任务**：参考 `skills/stock/` 目录
- **视频相关任务**：参考 `skills/video/` 目录
- **学习新技能**：参考 `skills/learning/` + `knowledge/`

### 添加新技能
1. 学习资料放入 `knowledge/` 对应目录
2. 实践代码放入 `skills/learning/` 对应目录
3. 验证有效后，移动到 `skills/` 正式目录
4. 更新 `skills/README.md` 技能清单

### 任务驱动加载
- 采用按需加载策略，优化Token使用
- 不同任务类型加载不同的技能组合
- 详见 `memory/config/` 中的加载策略配置

---

## ⚠️ 重要提示

1. **原路径已失效**：请更新所有对 `memory/skills/` 的引用
2. **新路径生效**：使用 `skills/` 目录结构
3. **外部技能**：`seedance-prompt-en` 软链接保持不变
4. **文档更新**：已更新 `AGENTS.md`、`MEMORY.md` 等核心文档

---

## 📅 迁移记录

- **迁移时间**：2026-02-18 UTC
- **执行者**：贾维斯
- **迁移方案**：技能库独立化，支持晋升路径
- **架构升级**：实习生区与正式区分离，支持任务驱动加载

---

_如需恢复原结构，请查看Git历史记录或联系贾维斯。_