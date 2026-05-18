---
name: daily-shortvideo-research
description: 短视频制作优化每日信息采集工作流 - 每天凌晨1点自动运行，采集7大主题（提示词优化、剧本改编、分镜脚本、风格统一、数字知产、图片生成、视频生成），生成简报推送Telegram。
---

# 短视频制作优化 — 每日信息采集工作流

## 功能描述

每天凌晨1点自动运行的全网信息采集Pipeline，采集7大主题（提示词优化、剧本改编、分镜脚本、风格统一、数字知产、图片生成、视频生成），生成简报并推送Telegram。

## 触发条件

- Cron job: `0 1 * * *`
- 任务ID: `cron_aa706cde858f`
- 手动触发: 说"运行每日短视频研究"

## 7大主题（按优先级）

| 优先级 | 主题 | 搜索重点 |
|--------|------|----------|
| 1 | 提示词优化 | AI视频生成prompt工程、调优方法、模板 |
| 2 | 剧本改编 | 小说/短篇转AI短剧剧本的改编方法 |
| 3 | 分镜脚本制作 | AI辅助分镜生成、storyboard工作流 |
| 4 | 风格统一 | 短剧视觉风格一致性控制方法 |
| 5 | 数字知产 | AI生成内容版权、确权、管理 |
| 6 | 图片生成 | 短剧素材AI图片生成技巧 |
| 7 | 视频生成 | AI视频工具工作流、制作效率 |

## 信息源覆盖

**可用来源（已验证）：**
- YouTube（主要来源，搜索功能稳定，内容质量高）
- Bilibili（中文AI短剧教程最大聚集地，内容量大且新）
- AI工具官方博客/更新日志

**受限来源：**
- 知乎（可能无法访问）
- 小红书（可能无法访问）
- 微信公众号（可能无法访问）
- Reddit（可能需要代理）

## 执行流程

### Step 1: 检查是否已执行

```bash
# 检查今天的报告是否已生成
ls /root/.hermes/scripts/daily_report_2026-04-25.md
```

如果报告已存在且内容完整，跳过采集。

### Step 2: 信息采集

每个主题用 YouTube 和 Bilibili 搜索关键词：

**YouTube 搜索（URL格式）：**
- 主题1: `https://www.youtube.com/results?search_query=AI+video+prompt+engineering+Seedance+Runway+2026`
- 主题2: `https://www.youtube.com/results?search_query=AI+short+drama+script+adaptation+novel+2026`
- 主题3: `https://www.youtube.com/results?search_query=AI+storyboard+generation+workflow+short+video`
- 主题4: `https://www.youtube.com/results?search_query=AI+video+style+consistency+character+control+2026`
- 主题5: `https://www.youtube.com/results?search_query=AI+video+copyright+ownership+GenAI+2026`
- 主题6: `https://www.youtube.com/results?search_query=AI+image+generation+short+drama+Stable+Diffusion+Flux`
- 主题7: `https://www.youtube.com/results?search_query=Seedance+2.0+tutorial+workflow+Runway+API`

**Bilibili 搜索（URL格式）：**
- 中文关键词使用URL编码，如：`https://search.bilibili.com/all?keyword=AI%E7%9F%AD%E5%89%A7+%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90+2026`
- 推荐中文搜索词：AI短剧、提示词优化、AI视频生成、Seedance教程、Stable Diffusion等

**搜索方法（按优先级）：**

1. **browser_navigate + browser_snapshot（最可靠）** - 直接访问YouTube和B站搜索结果页面：
   - YouTube: `https://www.youtube.com/results?search_query=关键词`
   - Bilibili: `https://search.bilibili.com/all?keyword=关键词`
   - 可以获取丰富的标题、播放量、频道信息

2. **curl + grep（备选）** - Bing 中文版：
   ```bash
   curl -s -L -A "Mozilla/5.0 ..." "https://cn.bing.com/search?q=关键词" > /tmp/search.html
   grep -o 'b_algo' /tmp/search.html | wc -l  # 确认有结果
   ```
   注意：Bing 会重定向到 `cn.bing.com`，需要用 `-L` 跟随重定向。

3. **Python requests** - 注意：requests.get 会遇到 Object moved 重定向，需要处理。知乎/小红书有反爬，建议用 curl。

4. **DuckDuckGo html 模式** - `https://html.duckduckgo.com/html/?q=关键词&ia=web`，但结果数量不稳定（0-5条）。

5. **BeautifulSoup** - venv 中的 python3 可能没有 bs4，需用 `/root/.hermes/hermes-agent/venv/bin/python3` 或 pip install --break-system-packages。

**已知搜索障碍：**
- Google: 被墙或返回验证码（"unusual traffic"）
- 知乎/小红书: 需要登录/反爬
- Bing requests: 直接 requests.get 会收到 Object moved 页面
- DuckDuckGo: 不稳定，有时返回 0 条

### Step 3: 质量过滤

**过滤掉：**
- 广告/营销内容（"限时优惠"、"加盟代理"、"赚钱"等）
- 标题党（"震惊！"、"必看！"、"不看后悔"等）
- 低信息量内容（摘要少于50字）
- 失效链接

**保留标准：**
- 有具体方法/步骤/工具介绍
- 有可操作性
- 来源可信（官方文档、技术博客、知名社区）

### Step 4: 查重入库

```python
# 查重调用
rag_search(query="内容摘要或关键词", top_k=5)

# 如果相似度<0.85，入库
rag_add_memory(content="...", source="daily_research")
```

**已知问题：** RAG系统编码错误，`'NoneType' object has no attribute 'encode'`。2026-04-28观察到两个RAG方法完全不可用（rag_search和rag_add_memory都报错）。如果查重失败：
- 标记新内容为"待验证"
- 仍生成简报
- 在备注中说明查重系统故障
- 可尝试用内容指纹比对进行简单去重

**重要：RAG函数不在execute_code的hermes_tools中**
`execute_code` sandbox的`hermes_tools`模块不包含`rag_search`/`rag_add_memory`/`rag_stats`。可用函数只有：
```python
from hermes_tools import terminal, read_file, write_file, patch, search_files, retry, shell_quote, json_parse
```
RAG函数需要用工具调用接口，不能在代码中直接导入。

**已知问题：** 如果`HERMES_TELEGRAM_BOT_TOKEN`未设置或无效（404 Not Found），发送会失败。首先检查：

保存路径: `/root/.hermes/scripts/daily_report_{date}.md`

格式模板：
```markdown
# 短视频制作优化 每日简报
日期: YYYY-MM-DD

## 采集概况
- 采集: X条
- 去噪过滤: Y条
- 查重去重: Z条（如果RAG故障，说明"无法查重"）
- 保留入库: W条

## 重点速递
### 🔴 提示词优化（最高优先级）
[最重要的3条方法和工具]

### 🟡 剧本改编
[最多3条]
...（其他主题）

## 趋势观察
## 备注
```

### Step 6: 推送Telegram

```python
import os, requests

token = os.environ.get("HERMES_TELEGRAM_BOT_TOKEN")
chat_id = "7584677982"
url = f"https://api.telegram.org/bot{token}/sendMessage"

# 发送简报精炼版（<4096字符）
requests.post(url, data={
    "chat_id": chat_id, 
    "text": escaped_text, 
    "parse_mode": "MarkdownV2"
})
```

**已知问题：** 如果`HERMES_TELEGRAM_BOT_TOKEN`未设置或无效（404 Not Found），发送会失败。首先检查：
```python
import os
token = os.environ.get("HERMES_TELEGRAM_BOT_TOKEN")
print(f"Token set: {bool(token)}, first 20 chars: {token[:20] if token else 'N/A'}")
```
如果Token未设置：- 报告仍保存到文件
- 在备注中说明 Telegram 未配置
- cron job 系统会自动投递文件，无需手动推送

## 常见障碍与解决方案

| 障碍 | 解决方案 |
|------|----------|
| delegate_task并发超限 | 最多3个并发任务，超出会报"Too many tasks"，需拆分多次调用 |
| 搜索skill不可用 | 使用浏览器YouTube搜索 |
| Reddit被封锁 | 使用YouTube作为主要来源 |
| curl\|python被安全扫描拦截 | 使用browser_navigate或写脚本文件 |
| RAG编码错误 | 跳过查重，标记内容为待验证 |
| Telegram token无效（404 Not Found） | Token可能未配置在HERMES_TELEGRAM_BOT_TOKEN环境变量，报告仅保存文件 |
| cron任务无声失败 | 检查session消息数量，<20条说明未完成 |

## 验证检查清单

- [ ] 今天的报告已生成
- [ ] 7个主题都有覆盖
- [ ] 低质量内容已过滤
- [ ] 简报已推送Telegram（或说明原因）
- [ ] 报告保存路径正确

## 执行记录

**2026-05-18 发现（新内容）：**
- invideo Agent One新发现：一句话生成完整AI短片，支持一致角色+连贯视觉世界+2K分辨率（Kingsway Collins, 286 views, 2天前）
- GPT Image 2 + Seedance 2.0分镜转视频流水线：12镜头分镜 → 自定义GPT转提示词 → Seedance 2.0生成 → 接片延长（1.2K views, 1天前）
- HeyGen官方Seedance 2.0电影感提示词教程：cinematic lighting/dramatic shadows/shallow depth of field等电影术语成优化关键词（1.7K views, 5天前）
- B站高质量内容：Seedance2.0 AI仙侠短剧全流程(1.6万播放)、ComfyUI+豆包+即梦AI保姆级教程(4.2万播放，04-30)
- 趋势：分镜工作流成为主流；全自动AI短剧工具出现实用化

**2026-05-13 发现（新内容）：**
- delegate_task的web搜索子任务返回的内容不包含实际搜索结果，只列出工具调用记录（"Tool trace: []"）
- 解决：必须用 browser_navigate 直接访问YouTube搜索结果页，手动提取标题和摘要
- arXiv搜索有效：https://arxiv.org/search/?searchtype=all&query=AI+video+generation 返回1503+篇论文
- RAG编码错误仍然存在：`'NoneType' object has no attribute 'encode'`
- Telegram Bot Token未配置（HERMES_TELEGRAM_BOT_TOKEN环境变量不存在），发送返回404 Not Found
- YouTube是唯一可靠的内容来源，发现Seedance 2.0高质量教程：
  - HeyGen: "Stop the Generic AI Look" (808 views, 16小时前)
  - Dan Kieft: "Seedance 2.0 is CRAZY for AI Filmmaking" (89K views, 2周前)
  - CyberJungle: "Create Long Cinematic AI Films in Claude + Seedance 2.0" (3K views, 1天前)
  - Creating with Conor: "Stop Wasting Credits on Seedance 2.0" (34K views, 2周前)
- 趋势：提示词工程向电影术语进化（cinematic lighting, dramatic shadows, shallow depth of field）

**2026-05-11 发现（新内容）：**
- 网络限制严重：B站搜索、Google、Twitter、Reddit、Bing 均无法访问
- 任务配置的 skill 列表中 "search" 和 "memory" 技能未找到并跳过
- Telegram Bot 仍返回 404（token 未配置或无效）
- 报告仍成功保存到文件：`/root/.hermes/scripts/daily_report_2026-05-11.md`
- 建议：使用 browser_navigate 直接访问 YouTube 搜索结果页获取内容

**2026-05-10 发现（新内容）：**
- `execute_code` sandbox的`hermes_tools`模块不包含`rag_search`/`rag_add_memory`——这些RAG函数根本不在可导入列表中
- `hermes_tools`可用函数：terminal, read_file, write_file, patch, search_files, retry, shell_quote, json_parse
- RAG工具（rag_search/rag_stats）调用失败原因确认：`'NoneType' object has no attribute 'encode'` — 函数接口本身损坏
- delegate_task的web搜索返回摘要而非实际内容，需要用browser_navigate直接访问YouTube/Bing结果页
- Telegram Bot Token仍未配置，HERMES_TELEGRAM_BOT_TOKEN环境变量不存在
- 新发现热门内容：
  - Seedance 2.0多镜头提示词+角色参考表（33K views，13天前）：multi-shot prompts + character reference sheets + video-to-video references
  - Topview Agent V2（4.9K views，8天前）：一键提示词→完整长视频的完整pipeline
  - 停止写提示词用AI文档构建GPT（285K views）：从Hailuo/Kling/Luma/Runway/Veo/Vidu官方文档构建Prompt Sidekick
  - Storyboarder.ai（90秒从想法到分镜，13K views）
  - LTX Studio混合工作流（74K views）
  - PlotDot Horizon 2.0: 头脑风暴→角色创建→AI剧本→Veo-3场景生成
- 趋势：Seedance 2.0继续主导；AI Storyboard概念兴起（GPT Image 2被整合进视频前端）

**2026-05-09 发现（新内容）：**
- RAG问题持续：`'NoneType' object has no attribute 'encode'` 错误仍然存在
- Telegram Bot Token未配置（环境变量HERMES_TELEGRAM_BOT_TOKEN不存在），发送返回404
- delegate_task最多3个并发任务，4个会报错"Too many tasks"
- 新发现高质量内容：
  - Seedance2.0故事板法：放弃传统提示词，用故事板规划视频（全网独家方法）
  - LTX2.3 PromptReplay：一键出分镜，不会写提示词也能做短剧
  - 白菜AI短剧V1.4：开放API对接Seedance和Kling，深度优化LTX2.3工作流
  - 即梦AI4.0电影分镜教程、ComfyUI人物一致性解决方案
  - GPT Image 2 + Seedance 2.0无缝AI电影创作
- 趋势：API化工作流加速、故事板法成为新热点、多工具组合（openclaw+即梦+Seedance）成主流

**2026-05-08 发现：**
- RAG编码错误仍然存在（持续10天未修复）
- Telegram Bot Token仍未配置，报告仅保存文件不推送
- 浏览器导航(browser_navigate)对YouTube和Bilibili均有效，成为唯一可靠搜索方式
- 新发现热门内容：豆包+即梦+剪映AI短剧教程(49.7万播放)、Seedance 2.0仙侠/游戏CG全流程课程
- Seedance 2.0继续主导AI视频领域，角色一致性和JSON Prompt是关键特性

**2026-04-28 发现：**
- Bilibili是中文AI短剧教程最大聚集地，内容量远超预期
- YouTube高质量内容：Dan Kieft的Seedance 2.0 filmmaking教程(51K views)、AI Video School的Prompt Sidekick(280K views)
- RAG搜索和入库服务今日完全不可用（rag_search和rag_add_memory都报错）
- Telegram Bot Token未配置（HERMES_TELEGRAM_BOT_TOKEN未设置）
- 浏览器导航比curl更可靠，推荐用browser_navigate访问YouTube和B站搜索结果页

## 相关文件

- 脚本: `/root/.hermes/scripts/daily_shortvideo_research.py`
- 研究索引: `/root/.hermes/scripts/daily_shortvideo_research.md`
- 历史报告: `/root/.hermes/scripts/daily_report_YYYY-MM-DD.md`
