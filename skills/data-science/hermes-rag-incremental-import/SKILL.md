---
name: hermes-rag-incremental-import
description: Hermes RAG 向量数据库增量导入脚本 - 基于哈希校验的智能增量导入
---

# Hermes RAG 增量导入脚本

## 功能
每天凌晨 3:00 自动增量导入 Hermes 系统文档到 RAG 向量数据库。

## 核心逻辑

### 增量导入策略（哈希校验）
```python
# 1. 从数据库读取已有文档的哈希
existing_sources = get_existing_sources_with_hash(db_path)

# 2. 计算文件哈希判断是否需要导入
current_hash = compute_file_hash(filepath)
if source not in existing_sources:
    # 新文档 -> 导入
elif current_hash != existing_hash:
    # 内容变化 -> 先删旧记录，再导入新记录
else:
    # 未变化 -> 跳过
```

### 关键发现
- **哈希检测**：用 MD5 哈希检测内容变化，比 mtime 更可靠
- **API 返回格式**：`rag_add_memory` 返回 `{"status": "success"}`，不是 `{"success": true}`
- **向量数据库**：LanceDB 存储在 `/root/.hermes/rag_vector_db/`
- **provider 路径**：`/root/.hermes/hermes-agent/plugins/memory/cpu_rag/`

### 数据库 Schema（必须严格遵循）
**表结构**：`memories` 表有独立列 `id`, `content`, `vector`, `source`, `metadata`, `timestamp`, `access_count`

**metadata 字段结构**：
```json
{
  "type": "memory_file",           // 或 "session_file"
  "filepath": "/root/.hermes/sessions/xxx.json",  // 完整绝对路径
  "filename": "xxx.json",          // 文件名
  "file_hash": "a1b2c3d4...",     // MD5 哈希
  "chunk_index": 0,
  "total_chunks": 1,
  "imported_at": "2026-05-11T03:00:00"
}
```

**⚠️ 容易踩的坑**：
- `source` 列只存**文件名**（如 `2026-03-25.md`），不是完整路径
- `metadata.source` 根本不存在，**必须用 `metadata.filepath`** 获取完整路径来做哈希匹配
- `metadata` 中存的是 `filepath` 不是 `source`（2026-05-11 踩坑记录：脚本原用 `metadata.source` 导致 `已有文档数: 0`，已修复为 `metadata.filepath`）

## 文件位置
- 脚本：`/root/.hermes/scripts/incremental_rag_import.py`
- 定时任务 ID：`8b2ef35fa499`

## 监控目录
- `/root/.hermes/memories/` — 记忆文件（MEMORY.md, USER.md）
- `/root/.hermes/sessions/` — 会话文件（jsonl/json）

## 使用方法
```bash
# 手动运行
cd /root/.hermes/hermes-agent && source venv/bin/activate && python /root/.hermes/scripts/incremental_rag_import.py

# 查看定时任务
hermes cron list

# 查看 RAG 统计
rag_stats
```

## 依赖
- LanceDB
- CPURAGMemoryProvider from plugins.memory.cpu_rag
- hashlib (MD5)
