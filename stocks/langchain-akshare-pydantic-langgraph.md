# LangChain + akshare + Pydantic + LangGraph 新闻情感分析

## 一、技能概述

基于 **LangChain/LangGraph + akshare + Pydantic + DeepSeek API**，对 A 股新闻进行自动化情感分析，输出板块级舆情指数和个股事件信号。

**核心特点**：
- ✅ 零 GPU 依赖，纯 API 调用
- ✅ 已验证可运行（verify_v2.py 测试通过）
- ✅ 使用 OpenClaw 配置的 DeepSeek API Key
- ✅ akshare 正确 API：`stock_news_em` / `stock_board_industry_spot_em`

**参考项目**：
- daily_stock_analysis (32k⭐) — 数据源设计
- FinGPT (19.7k⭐) — 金融情感分析方法
- multi-agent-stocks-analysis (LangGraph) — Agent 编排架构

---

## 二、环境配置

### 2.1 虚拟环境位置

```bash
/root/.openclaw/workspace/scripts/test-multi-agent/venv/
```

### 2.2 激活环境

```bash
source /root/.openclaw/workspace/scripts/test-multi-agent/venv/bin/activate
```

### 2.3 已安装依赖

```
langchain==1.3.1
langchain-openai==1.2.1
langchain-community==0.4.1
langchain-core==1.4.0
langgraph==1.2.0
akshare==1.18.60
pydantic==2.13.4
python-dotenv==1.2.2
loguru==0.7.3
```

---

## 三、核心代码（已验证可运行）

### 3.1 API Key 加载

```python
import json, os

# 从 OpenClaw 配置加载 DeepSeek API Key
config_path = "/root/.openclaw/openclaw.json"
with open(config_path) as f:
    cfg = json.load(f)

deepseek_key = cfg["models"]["providers"]["deepseek"]["apiKey"]
deepseek_url = cfg["models"]["providers"]["deepseek"]["baseUrl"]
```

### 3.2 akshare 新闻获取（正确 API）

```python
import akshare as ak

# ✅ 正确：获取个股新闻
def fetch_stock_news(symbol="603296", limit=10):
    """获取个股新闻（东方财富）"""
    try:
        df = ak.stock_news_em(symbol=symbol)
        return df.head(limit)
    except Exception as e:
        print(f"获取新闻失败: {e}")
        return None

# ✅ 正确：获取板块实时行情
def fetch_sector_heatmap():
    """获取板块热度（按涨跌幅排序）"""
    try:
        df = ak.stock_board_industry_spot_em()
        return df.sort_values("涨跌幅", ascending=False)
    except Exception as e:
        print(f"获取板块行情失败: {e}")
        return None
```

**注意**：
- ❌ `ak.stock_board_industry_news_em()` — 此 API 不存在
- ✅ `ak.stock_news_em()` — 正确的个股新闻 API
- ✅ `ak.stock_board_industry_spot_em()` — 板块实时行情

### 3.3 LangChain 情感分析 Pipeline

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# ========== Pydantic 输出结构 ==========
class SentimentScore(BaseModel):
    sentiment: str = Field(description="positive/negative/neutral")
    score: float = Field(description="-1.0~1.0")
    event_type: str = Field(description="事件类型")
    affected_sectors: list = Field(description="影响的板块")
    summary: str = Field(description="一句话总结")

# ========== Prompt 模板 ==========
parser = PydanticOutputParser(pydantic_object=SentimentScore)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个A股金融情感分析师。分析新闻情感。{format_instructions}"),
    ("human", "标题：{title}\n内容：{content}")
])

# ========== LLM 初始化 ==========
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.1,
    api_key=deepseek_key,
    base_url=deepseek_url
)

# ========== Chain 构建 ==========
chain = prompt | llm | parser

# ========== 调用示例 ==========
def analyze_news(title, content):
    """分析单条新闻情感"""
    try:
        result = chain.invoke({
            "title": title,
            "content": content,
            "format_instructions": parser.get_format_instructions()
        })
        return result
    except Exception as e:
        print(f"分析失败: {e}")
        return None
```

### 3.4 批量分析 + 板块汇总

```python
from datetime import datetime
from typing import List

class DailyReport(BaseModel):
    date: str = Field(description="报告日期")
    overall_sentiment: str = Field(description="整体情绪：bullish/bearish/neutral")
    top_positive: List[str] = Field(description="Top 3利好事件")
    top_negative: List[str] = Field(description="Top 3利空事件")
    sector_heatmap: dict = Field(description="板块热度字典")

def batch_analyze(news_list: list) -> DailyReport:
    """批量分析新闻并汇总板块舆情"""
    results = []
    
    for news in news_list:
        title = news.get("新闻标题", "")
        content = news.get("新闻内容", "")
        result = analyze_news(title, content)
        if result:
            results.append(result)
    
    # 统计板块热度
    sector_scores = {}
    for r in results:
        for sec in r.affected_sectors:
            s = 1 if r.sentiment == "positive" else \
                -1 if r.sentiment == "negative" else 0
            score = s * r.score
            sector_scores.setdefault(sec, []).append(score)
    
    sector_heatmap = {
        sec: round(sum(scores)/len(scores), 2)
        for sec, scores in sector_scores.items()
    }
    
    # 排序
    sorted_sectors = sorted(sector_heatmap.items(), key=lambda x: x[1], reverse=True)
    
    # Top 正负面
    positives = [r for r in results if r.sentiment == "positive"]
    negatives = [r for r in results if r.sentiment == "negative"]
    positives.sort(key=lambda x: x.score, reverse=True)
    negatives.sort(key=lambda x: x.score)
    
    avg_score = sum(r.score for r in results) / len(results) if results else 0
    overall = "bullish" if avg_score > 0.3 else ("bearish" if avg_score < -0.3 else "neutral")
    
    return DailyReport(
        date=datetime.now().strftime("%Y-%m-%d"),
        overall_sentiment=overall,
        top_positive=[p.summary for p in positives[:3]],
        top_negative=[n.summary for n in negatives[:3]],
        sector_heatmap=dict(sorted_sectors[:10])
    )
```

---

## 四、完整运行示例

### 4.1 测试脚本（已验证通过）

```python
#!/usr/bin/env python3
"""
完整测试：akshare 获取新闻 → LangChain 情感分析 → 输出报告
"""
import json, os
import akshare as ak
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# --- 1. 加载 API Key ---
config_path = "/root/.openclaw/openclaw.json"
with open(config_path) as f:
    cfg = json.load(f)
deepseek_key = cfg["models"]["providers"]["deepseek"]["apiKey"]
deepseek_url = cfg["models"]["providers"]["deepseek"]["baseUrl"]

# --- 2. 获取新闻 ---
df = ak.stock_news_em(symbol="603296")  # 华勤技术
print(f"✅ 获取 {len(df)} 条新闻")

# --- 3. 情感分析 ---
class SentimentScore(BaseModel):
    sentiment: str = Field(description="positive/negative/neutral")
    score: float = Field(description="-1.0~1.0")
    event_type: str = Field(description="事件类型")
    affected_sectors: list = Field(description="影响的板块")
    summary: str = Field(description="一句话总结")

parser = PydanticOutputParser(pydantic_object=SentimentScore)
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是A股金融情感分析师。{format_instructions}"),
    ("human", "标题：{title}\n内容：{content}")
])

llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0.1,
    api_key=deepseek_key,
    base_url=deepseek_url
)

chain = prompt | llm | parser

# --- 4. 分析前3条新闻 ---
for i, (_, row) in enumerate(df.head(3).iterrows(), 1):
    title = row.get("新闻标题", "")
    content = row.get("新闻内容", "")
    
    result = chain.invoke({
        "title": title,
        "content": content,
        "format_instructions": parser.get_format_instructions()
    })
    
    emoji = "🟢" if result.sentiment == "positive" else \
            ("🔴" if result.sentiment == "negative" else "⚪")
    
    print(f"\n[{i}] {emoji} {title[:40]}")
    print(f"    情感={result.sentiment}  得分={result.score}")
    print(f"    事件={result.event_type}")
    print(f"    板块={result.affected_sectors}")
    print(f"    总结={result.summary[:60]}")
```

### 4.2 运行结果（实际输出）

```
✅ 获取 10 条新闻

[1] 🟢 国务院：算力网纳入六张网战略，投资超7万亿
    情感=positive  得分=0.8
    事件=政策利好
    板块=['算力', '基建', '数字经济']
    总结=国务院将算力网纳入六张网战略，发改委宣布今年投资超7万亿，利好算力及基建板块。

[2] 🟢 中芯国际406亿并购落地
    情感=positive  得分=0.85
    事件=并购重组
    板块=['半导体', '芯片', '集成电路']
    总结=中芯国际完成406亿元并购，利好公司利润和先进制程发展，对半导体板块有积极影响。

[3] 🟢 普京5月19日访华
    情感=positive  得分=0.7
    事件=外交事件
    板块=['能源', '贸易', '一带一路']
    总结=普京访华签署合作协议，利好中俄能源与贸易板块
```

---

## 五、LangGraph 多 Agent 编排（可选）

对于需要实时监控的场景（盘中每30分钟），可使用 LangGraph 构建 Agent 工作流：

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class SentimentState(TypedDict):
    sectors: list
    news: list
    sentiment_results: list
    report: dict
    alerts: list

# 定义节点
def fetch_news(state: SentimentState) -> SentimentState:
    """为每个板块获取最新新闻"""
    all_news = []
    for sector in state["sectors"]:
        # 这里需要根据板块名映射到具体股票代码
        # 暂时用板块行情代替
        pass
    return {**state, "news": all_news}

def analyze_sentiment(state: SentimentState) -> SentimentState:
    """批量情感分析"""
    results = []
    for news in state["news"]:
        result = analyze_news(news["title"], news["content"])
        if result:
            results.append(result)
    return {**state, "sentiment_results": results}

def check_alerts(state: SentimentState) -> SentimentState:
    """检查触发异动预警"""
    alerts = []
    for r in state["sentiment_results"]:
        if abs(r.score) > 0.8:  # 强烈情感信号
            alerts.append(
                f"⚠️ {r.summary[:30]}... | {r.sentiment} 得分={r.score:.2f}"
            )
    return {**state, "alerts": alerts}

def generate_report(state: SentimentState) -> SentimentState:
    """生成汇总报告"""
    # 调用 batch_analyze 生成报告
    return {**state, "report": {}}

# 构建图
workflow = StateGraph(SentimentState)
workflow.add_node("fetch", fetch_news)
workflow.add_node("analyze", analyze_sentiment)
workflow.add_node("alert", check_alerts)
workflow.add_node("report", generate_report)

workflow.set_entry_point("fetch")
workflow.add_edge("fetch", "analyze")
workflow.add_edge("analyze", "alert")
workflow.add_edge("alert", "report")
workflow.add_edge("report", END)

app = workflow.compile()
```

---

## 六、部署接入方案

### 6.1 与现有监控系统集成

```python
# 在 stock_monitor.py 中加入舆情评分
def get_sector_sentiment_score(sector_name):
    """获取指定板块的舆情情绪得分，返回 -1~1"""
    # 激活 venv
    import subprocess
    venv_path = "/root/.openclaw/workspace/scripts/test-multi-agent/venv/bin/python3"
    
    # 调用情感分析脚本
    result = subprocess.run([
        venv_path,
        "/root/.openclaw/workspace/scripts/test-multi-agent/analyze_sector.py",
        sector_name
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        return float(result.stdout.strip())
    return 0.0
```

### 6.2 定时任务配置

```bash
# 盘前舆情报告：交易日 8:30 生成
30 8 * * 1-5 cd /root/.openclaw/workspace/scripts/test-multi-agent && source venv/bin/activate && python3 daily_sentiment_report.py

# 盘中监控（与MACD监控同步）
5,35 9-15 * * 1-5 cd /root/.openclaw/workspace/scripts/test-multi-agent && source venv/bin/activate && python3 intraday_sentiment_monitor.py
```

---

## 七、常见问题

### Q1: akshare API 名称错误怎么办？

**错误示例**：
```python
ak.stock_board_industry_news_em()  # ❌ 此 API 不存在
```

**正确用法**：
```python
ak.stock_news_em(symbol="600519")              # ✅ 个股新闻
ak.stock_board_industry_spot_em()              # ✅ 板块行情
```

### Q2: API Key 加载失败？

确保 `/root/.openclaw/openclaw.json` 存在且包含 DeepSeek 配置：

```json
{
  "models": {
    "providers": {
      "deepseek": {
        "apiKey": "sk-xxx",
        "baseUrl": "https://api.deepseek.com/v1"
      }
    }
  }
}
```

### Q3: LangChain 版本不兼容？

确保使用新版 import 路径：

```python
# ❌ 旧版（已废弃）
from langchain.chains import LLMChain

# ✅ 新版
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
```

---

## 八、项目调研总结

| 特性 | daily_stock_analysis | FinGPT | multi-agent | 本方案 |
|------|---------------------|--------|-------------|--------|
| A股支持 | ✅ 完整 | ❌ 美股为主 | ❌ 美股10只 | ✅ 专注A股 |
| LangChain | ⚪ 部分 | ❌ | ✅ LangGraph | ✅ 核心 |
| 情感分析 | ⚪ LLM直出 | ✅ FinBERT微调 | ✅ FinBERT | ✅ LLM直出 |
| GPU 依赖 | ❌ | ✅ 需要 | ✅ 需要 | ❌ 纯API |
| 部署难度 | 低 | 高 | 中 | **低** |
| 已验证 | - | - | - | ✅ verify_v2.py |

**选择理由**：
1. **零 GPU 成本** — 纯 API 调用
2. **中文金融文本适配度** — DeepSeek 中文能力远超 FinBERT
3. **灵活性** — Prompt 可随时调整
4. **可嵌入性** — 直接接入现有监控管道

---

## 版本记录

| 版本 | 日期 | 内容 |
|------|------|------|
| v1.0 | 2026-05-17 | 初版创建，基于 GitHub Top 4 项目调研 |
| v2.0 | 2026-05-17 | 整合 verify_v2.py 验证通过代码，修正 akshare API 错误 |

_最后更新: 2026-05-17 23:15_
