---
name: memory-search-workflow
description: 正确的记忆/历史信息搜索工作流 - 优先使用rag_search，当其不可用时回退到search_files搜索workspace_memory
version: 1.0.0
author: user
license: MIT
metadata:
  hermes:
    tags: [search, memory, rag, workflow]
    homepage: 
prerequisites:
  commands: []
---

# 记忆/历史信息搜索工作流

## 正确流程

1. **优先**: 使用 `rag_search` 搜索历史对话和记忆
2. **回退**: 如果 rag_search 不可用或失败，使用 `search_files` 搜索 `/root/openclaw_memory/workspace_memory/`
3. **备选**: 使用 `session_search` (但用户表示不希望用这个)

## rag_search 已知问题

**问题**: cpu_rag 插件的 rag_search 未注册到 Hermes 工具系统

**修复状态**:
- 已修改 toolsets.py、model_tools.py、创建 tools/rag_tools.py
- 但 Hermes CLI 从未重启，修复未生效

**关键**: 修改 cpu_rag 插件后必须重启 Hermes CLI 才能生效

## 重要经验：Web搜索失败时的回退策略

**场景**: 当需要搜索中国平台（抖音、百度等）时，通常会遇到：
- 抖音: 验证码中间页（安全验证）
- 百度: 滑动验证码（安全验证）
- Google: IP被标记为机器人

**有效策略**: 立即回退到 `rag_search` 搜索历史对话
- 优点: 用户可能之前已经讨论过相同话题
- 实测效果: 抖音高尔夫账号研究在网页搜索失败后，通过 rag_search 找到了2026-04-14的完整对话记录

**操作流程**:
1. 尝试网页搜索 → 遇到验证码/机器人检测
2. 立即调用 `rag_search(query="相关关键词")` 搜索历史
3. 如果找到相关记录，继续使用；找不到再尝试其他方法

## search_files 回退方案

当 rag_search 不可用时，使用:

```bash
search_files(path="/root/openclaw_memory/workspace_memory", pattern="关键词", target="content")
```

常用搜索路径:
- `/root/openclaw_memory/workspace_memory/` - 每日记忆文件
- `/root/openclaw_memory/knowledge/` - 知识库
- `/root/.hermes/skills/` - 技能文件

## 用户偏好

- **不要**用 session_search 进行搜索 (用户明确表示不喜欢)
- 优先使用 rag_search
- 简洁回复，不要过度使用 markdown