---
name: daily-web-research-workflow
description: Multi-topic daily web research and report generation workflow. Use when the search skill is unavailable, as a fallback using delegate_task with web/browser tools.
---

# Daily Web Research Workflow

## Trigger
When asked to do multi-topic web research, information gathering across multiple themes, or daily news/monitoring tasks.

## Approach

### 1. Use `delegate_task` with parallel subagents
When the `search` skill is unavailable, use `delegate_task` with the `web` and `browser` toolsets as the search workaround. Run multiple subagents in parallel, one per topic (or pair topics into single subagents to stay within concurrency limits).

```python
delegate_task(
    goal="[specific research goal with keywords]",
    context="[specific search terms and platforms to try]",
    max_iterations=20,
    toolsets=["web", "browser"],
    tasks=[
        {"goal": "search Chinese sources", "toolsets": ["web", "browser"], "context": "..."},
        {"goal": "search English sources", "toolsets": ["web", "browser"], "context": "..."},
    ]
)
```

### 2. Platform accessibility patterns (discovered empirically)
| Platform | Status | Notes |
|----------|--------|-------|
| Bilibili/YouTube | ✅ Accessible | Rich video content, accessible |
| Zhihu | ❌ 403/blocked | Login/CAPTCHA required, also for search results |
| Xiaohongshu | ❌ IP risk warning | Blocked for automation |
| Baidu/Sogou | ❌ CAPTCHA | Chinese search engines blocked |
| Google | ❌ CAPTCHA/bot detection | Most Google searches blocked |
| Bing (CN) | ⚠️ Irrelevant results | Returns general AI questions, not video-specific content. Use direct navigation instead. |
| Reddit | ❌ Blocked | Network security blocks |

**Strategy for AI video tools research via YouTube**: YouTube search via `browser_navigate` returns highly relevant results for AI video generation topics. Use this approach:
1. Navigate to `https://www.youtube.com/results?search_query=[keywords]` with relevant English terms
2. Use `browser_snapshot` with `full=true` to read video titles and descriptions
3. Click into relevant videos for detailed chapter/section info
4. Collect video URLs and timestamps for the report

**Best YouTube channels for AI video content** (discovered 2026-04-30):
- Tao Prompts — Runway Gen-3 prompt tutorials, cinematic techniques
- Venice — AI micro drama workflow, 4-step production pipeline
- Dan Kieft — Seedance 2.0 anime character consistency
- AI Filmmaking Academy — Pippit AI, short drama production
- Code And Create — Seedance 2.0 PromptGPT workflows
- Olivio Sarikas — Seedance 2.0 AI filmmaking

**Known Bing search pattern**: Bing CN with English keywords (e.g. "AI video prompt engineering Seedance Runway") DOES return relevant YouTube results — it redirects to `cn.bing.com` but still surfaces video content. Chinese keyword searches on Bing tend to return irrelevant general AI questions.

**Fallback strategy**: If YouTube search also fails, navigate **directly** to official tool pages:
- Seedance: `https://seed.bytedance.com/zh/seedance2_0`
- Runway: `https://runwayml.com` → check Research/Blog section
- Pika: `https://pika.art/blog`
- 可灵 (Kling): `https://klingai.com`

### 3. Information quality filtering
- Discard: ads ("限时优惠", "加盟代理"), clickbait ("震惊！", "必看！"), content with <50 chars summary
- Keep: specific methods/steps/tool names, actionable techniques, official documentation

### 4. Save findings
- Use `rag_add_memory` with `source="daily_research"` for each valuable finding
- If RAG fails (encoding error), fall back to writing to `/root/.hermes/scripts/daily_report_{date}.md`

### 5. Generate structured report
Save to `/root/.hermes/scripts/daily_report_{date}.md` with sections for each topic, trend observations, and notes.

## Known Issues
- `rag_add_memory` can fail with `'NoneType' object has no attribute 'encode'` — fallback to file storage
- Telegram bot token may not be configured — `HERMES_TELEGRAM_BOT_TOKEN` env var missing → Telegram API returns 404 "Not Found". Verify token exists before calling send_message/Telegram API.
