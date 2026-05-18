# VIDEO 技能目录结构标准（STRUCTURE.md）

**版本**: v2.1 Standard
**创建时间**: 2026-03-28
**最后更新**: 2026-03-28
**状态**: 标准结构（锁定）

---

## 📋 标准目录结构（5大分类）

```
skills/video/
├── README.md                          # 本目录说明
├── STRUCTURE.md                       # 本文件（结构标准）
│
├── 编剧/                              # 编剧技能
│   ├── screenwriting.md               # 编剧基础、故事结构
│   └── dialogue-to-screenplay.md      # 对白转剧本模板
│
├── 导演/                              # 导演技能
│   ├── directing.md                   # 镜头语言、180度法则
│   ├── director-styles.md             # 6位大师风格
│   ├── shots-guide.md                 # 镜头完全指南
│   ├── style-library-director.md      # 导演风格库
│   ├── wuxia-action-guide.md          # 武侠动作指导
│   └── seedance-prompt-en.md          # Seedance英文版提示词指南
│
├── 场景人物道具/                      # 场景一致性、人物设定、道具管理
│   ├── knowledge.md                   # 视频知识核心索引
│   ├── knowledge-room-4wall.md        # 四面墙场景一致性方法
│   ├── scene-consistency-checklist.md # 场景一致性检查清单
│   ├── production-tips.md             # 制作经验贴士
│   ├── video-consistency-study.md     # 视频一致性研究
│   ├── ai-music-copyright.md          # AI音乐版权指南
│   └── north-american-short-drama-market.md  # 北美短剧市场分析
│
├── 工作流程/                          # AI工具使用与工作流
│   ├── call-rules.md                  # 调用规则（本文件）
│   ├── workflow-index.md              # 6阶段视频制作流程
│   ├── seedance-guide.md              # Seedance 2.0使用指南
│   ├── seedream-5.0.md                # Seedream 5.0图像生成API
│   ├── prompt-generation-mustread.md  # 提示词生成必读
│   └── sensitive-words.md             # 敏感词库（审核避坑）
│
├── 其他/                              # 其他相关资源
│   └── ai-tools-overview.md           # AI视频工具全景图
│
├── projects/                          # 实战项目文件夹
│   ├── 偏爱难藏-硅谷AI版/             # 海外改编项目（完整）
│   ├── clara-divorce/                 # 离婚短剧项目
│   ├── 精灵王座/                      # 精灵王座项目
│   ├── 赛博朋克-贾维斯出场/           # 赛博朋克概念项目
│   └── 青山镇恐怖片/                  # 青山镇恐怖片项目
│
├── templates/                         # 模板文件
│   └── qingshanzhen-horror.json       # 青山镇恐怖片JSON模板
│
└── 备份/                              # 备份文件
    ├── knowledge-camera-movement.md.bak
    └── shots-guide.md.bak
```

---

## 🎯 分类原则

### 1️⃣ 编剧/
**用途**: 剧本创作相关技能
**包含内容**: 故事结构、对白技巧、剧本格式
**触发关键词**: 剧本、编剧、台词、三幕、角色弧线、对白、潜台词

### 2️⃣ 导演/
**用途**: 导演技巧与镜头语言
**包含内容**: 镜头技术、导演风格、运镜技巧、动作指导、英文提示词
**触发关键词**: 镜头、运镜、风格、王家卫、希区柯克、诺兰、武侠、动作、打斗、英文提示词、English prompt

### 3️⃣ 场景人物道具/
**用途**: 场景一致性、人物设定、道具管理、制作贴士
**包含内容**: 场景搭建方法、一致性检查、制作经验、市场分析
**触发关键词**: 场景不一致、物理位置、场景一致性、检查清单、服装、换装、视频知识

### 4️⃣ 工作流程/
**用途**: AI工具使用与工作流
**包含内容**: 生成工具指南、提示词规则、敏感词库
**触发关键词**: 视频生成、Seedance、图像生成、Seedream、工作流程、提示词必读、敏感词

### 5️⃣ 其他/
**用途**: 不便分类的其他资源
**包含内容**: 工具概览、参考资料
**触发关键词**: 按需查阅

### 📂 projects/
**用途**: 实战项目文件夹
**包含内容**: 具体项目的完整资料（剧本、人物、研究、制作）
**管理原则**: 每个项目一个子目录，内部结构自定

---

## 📞 调用规则映射表

| 类别 | 触发关键词 | 调取文件 |
|------|-----------|----------|
| 场景 | 场景不一致、物理位置 | 场景人物道具/knowledge-room-4wall.md |
| 镜头 | 镜头、运镜 | 导演/shots-guide.md |
| 导演 | 风格、王家卫、希区柯克、诺兰、库布里克、斯皮尔伯格 | 导演/director-styles.md |
| 导演方法论 | 多Agent协作、导演技巧 | 导演/directing.md |
| 武侠动作 | 武侠、动作、打斗、对决 | 导演/wuxia-action-guide.md |
| 英文提示词 | 英文提示词、English prompt、Seedance英文 | 导演/seedance-prompt-en.md |
| 编剧 | 剧本、编剧、台词、三幕、角色弧线 | 编剧/screenwriting.md |
| 台词改编 | 对白、潜台词、剧本格式 | 编剧/dialogue-to-screenplay.md |
| 场景检查 | 场景一致性、检查清单 | 场景人物道具/scene-consistency-checklist.md |
| 服装 | 服装、换装、造型 | 场景人物道具/production-tips.md |
| 视频知识 | 视频知识、知识索引、VIDEO知识 | 场景人物道具/knowledge.md |
| 一致性研究 | 一致性研究、视频一致性 | 场景人物道具/video-consistency-study.md |
| 工具-视频 | 视频生成、Seedance | 工作流程/seedance-guide.md |
| 工具-图像 | 图像生成、Seedream | 工作流程/seedream-5.0.md |
| 工作流 | 工作流程、制作流程、6阶段 | 工作流程/workflow-index.md |
| 必读 | 提示词必读、生成必读 | 工作流程/prompt-generation-mustread.md |

---

## 🛡️ 结构保护规则

### 变更审批流程
```
变更请求 → 检查本文件 → 用户确认 → 更新 STRUCTURE.md → 执行变更 → 验证
```

### 禁止操作
1. **禁止** 直接移动5大分类目录下的文件到根目录
2. **禁止** 创建与5大分类同级别的目录（projects/、templates/、备份/ 除外）
3. **禁止** 删除 STRUCTURE.md 文件
4. **禁止** 修改文件位置而不更新 call-rules.md

### 允许操作
1. ✅ 在5大分类内部增删文件
2. ✅ 在 projects/ 下创建新项目
3. ✅ 更新文件内容
4. ✅ 添加新的触发关键词（需更新 call-rules.md）

---

## 🔄 恢复流程

### 如果目录结构混乱
1. **读取本文件**（STRUCTURE.md）确认标准结构
2. **对比当前结构**找出差异
3. **移动文件**到正确位置
4. **更新 call-rules.md** 中的路径
5. **验证**调用规则映射表

### 如果本文件丢失
1. **查看 MEMORY.md** 中 "VIDEO技能目录结构" 部分
2. **查看 call-rules.md** 中的路径映射
3. **参考今天日期（2026-03-28）的 memory 日志**

---

## 🔧 维护指南

### 定期清理（每月执行）
```bash
# 清理超过30天的备份文件
./scripts/cleanup-backups.sh 30

# 或手动清理
find 备份/ -name "*.bak" -mtime +30 -delete
find projects/*/备份/ -type f -mtime +30 -delete
```

### 完整性检查（每季度执行）
1. 检查 call-rules.md 中的文件路径是否有效
2. 检查 knowledge.md 索引是否最新
3. 检查 projects/ 下各项目的README是否完整
4. 运行 Capability Evolver 进行系统审查

### 版本更新流程
1. 更新 STRUCTURE.md 版本号
2. 同步更新 call-rules.md 版本号
3. 更新 knowledge.md 时间戳
4. 记录到 MEMORY.md
5. 创建 memory/YYYY-MM-DD.md 日志

---

## 📊 版本历史

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-03-28 | v2.1 Standard | 创建5大分类标准结构（编剧/导演/场景人物道具/工作流程/其他），本文件创建 |
| 2026-03-28 | v2.3 | call-rules.md新增"提示词制作全流程"，明确提示词制作需调用全部相关文件 |
| 2026-03-27 | v2.0 | 扁平结构（director/knowledge/projects/templates） |
| 2026-03-26 | v1.0 | 完全合并《偏爱难藏》项目 |
| 2026-03-06 | v0.9 | 初始扁平结构 |

---

## 📝 关键记忆锚点

**如果记忆压缩或丢失，以下信息帮助恢复**:

1. **核心分类**: 5个中文分类目录（编剧、导演、场景人物道具、工作流程、其他）
2. **关键文件**: call-rules.md（调用规则）、STRUCTURE.md（本文件）
3. **项目位置**: projects/ 目录下有5个项目（偏爱难藏-硅谷AI版、clara-divorce、精灵王座、赛博朋克-贾维斯出场、青山镇恐怖片）
4. **备份位置**: 备份/ 目录下有2个.bak文件
5. **创建时间**: 2026-03-28 首次创建此结构

---

**本文件是 VIDEO 技能目录结构的唯一标准，任何变更必须同步更新本文件。**

_Last updated: 2026-03-28 (v2.1 Standard)_
