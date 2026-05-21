# MEETING SEARCH - 高影响力经济会议监控技能

## 技能概述

**目标**: 监控全球高影响力经济会议/峰会，捕捉可能影响市场的重大政策信号

**核心价值**: 
- 央行会议、GDP/CPI发布等直接影响市场流动性和预期
- 顶级商业峰会（达沃斯级别）释放全球经济风向标信号
- 提前布局，在市场反应前建仓或规避风险

**监控原则**: **只抓高影响力事件**，避免信息过载

## 核心数据源

### 1. Trading Economics API ⭐⭐⭐
**用途**: 央行会议、GDP/CPI发布、利率决议等硬数据事件

**API文档**: https://tradingeconomics.com/analytics/api.aspx

**关键端点**:
```python
# 经济日历（未来事件）
GET /calendar/country/{country}/indicator/{indicator}

# 央行会议
GET /calendar/country/all/indicator/central-bank-meeting

# GDP/CPI发布
GET /calendar/country/all/indicator/gdp-growth-rate
GET /calendar/country/all/indicator/inflation-rate

# 利率决议
GET /calendar/country/all/indicator/interest-rate-decision
```

**重点监控国家**:
- 美国（Fed会议、非农数据、CPI）
- 欧元区（ECB会议、欧元区GDP）
- 中国（央行MLF/LPR、GDP、CPI/PPI）
- 日本（BOJ会议）
- 英国（BOE会议）

**影响力评级**:
- ⭐⭐⭐ 高影响: Fed利率决议、美国非农、中国GDP
- ⭐⭐ 中影响: 欧元区CPI、日本央行会议
- ⭐ 低影响: 小国央行会议、次要指标

### 2. Bloomberg Live 爬虫 ⭐⭐⭐
**用途**: 全球顶级商业峰会（达沃斯级别）

**目标网站**: https://www.bloomberg.com/live/conferences

**抓取策略**:
```python
import requests
from bs4 import BeautifulSoup

def scrape_bloomberg_events():
    """
    抓取Bloomberg Live上的顶级峰会
    """
    url = "https://www.bloomberg.com/live/conferences"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取会议信息
    events = []
    for event in soup.find_all('div', class_='conference-card'):
        title = event.find('h3').text.strip()
        date = event.find('time').text.strip()
        location = event.find('span', class_='location').text.strip()
        
        # 只保留顶级峰会
        if is_top_tier_event(title):
            events.append({
                'title': title,
                'date': date,
                'location': location,
                'source': 'Bloomberg Live'
            })
    
    return events

def is_top_tier_event(title):
    """
    判断是否为顶级峰会
    """
    keywords = [
        'World Economic Forum',  # 达沃斯
        'G20', 'G7',
        'IMF', 'World Bank',
        'APEC',
        'Davos',
        'Jackson Hole',  # 美联储年度研讨会
        'Bloomberg New Economy'
    ]
    return any(kw.lower() in title.lower() for kw in keywords)
```

**重点峰会**:
- 达沃斯世界经济论坛（1月）
- Jackson Hole央行年会（8月）
- IMF/世界银行年会（10月）
- G20峰会
- APEC峰会
- Bloomberg New Economy Forum

### 3. 活动行爬虫（可选）⭐⭐
**用途**: 中国高级别峰会

**目标网站**: https://www.huodongxing.com/

**筛选条件**:
- 参会人数 > 500
- 关键词: 金融峰会、经济论坛、投资峰会、央行、监管
- 主办方: 政府机构、顶级券商、知名财经媒体

**抓取策略**:
```python
def scrape_huodongxing():
    """
    抓取活动行上的高级别经济峰会
    """
    url = "https://www.huodongxing.com/search"
    params = {
        'keyword': '金融峰会 OR 经济论坛',
        'city': '全国',
        'orderby': 'participants'  # 按参会人数排序
    }
    
    # 实现抓取逻辑
    # 过滤条件: participants > 500
    pass
```

**重点峰会**:
- 中国发展高层论坛（3月）
- 陆家嘴论坛（6月）
- 金融街论坛（10月）
- 外滩金融峰会
- 各省市政府主办的投资峰会

## 监控脚本实现

### 完整监控脚本
```python
import requests
from datetime import datetime, timedelta
import json

class MeetingMonitor:
    def __init__(self):
        self.trading_economics_key = "YOUR_API_KEY"
        
    def get_central_bank_meetings(self, days_ahead=30):
        """
        获取未来30天的央行会议
        """
        url = f"https://api.tradingeconomics.com/calendar/country/all/indicator/central-bank-meeting"
        params = {
            'c': self.trading_economics_key,
            'd1': datetime.now().strftime('%Y-%m-%d'),
            'd2': (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        }
        
        response = requests.get(url, params=params)
        events = response.json()
        
        # 过滤高影响力国家
        high_impact_countries = ['United States', 'China', 'Euro Area', 'Japan', 'United Kingdom']
        return [e for e in events if e['Country'] in high_impact_countries]
    
    def get_gdp_cpi_releases(self, days_ahead=30):
        """
        获取GDP/CPI发布日期
        """
        indicators = ['gdp-growth-rate', 'inflation-rate']
        all_events = []
        
        for indicator in indicators:
            url = f"https://api.tradingeconomics.com/calendar/country/all/indicator/{indicator}"
            params = {
                'c': self.trading_economics_key,
                'd1': datetime.now().strftime('%Y-%m-%d'),
                'd2': (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            }
            
            response = requests.get(url, params=params)
            all_events.extend(response.json())
        
        return all_events
    
    def get_top_tier_summits(self):
        """
        获取顶级峰会（Bloomberg + 活动行）
        """
        bloomberg_events = scrape_bloomberg_events()
        huodongxing_events = scrape_huodongxing()
        
        return bloomberg_events + huodongxing_events
    
    def generate_report(self):
        """
        生成监控报告
        """
        report = {
            'central_bank_meetings': self.get_central_bank_meetings(),
            'gdp_cpi_releases': self.get_gdp_cpi_releases(),
            'top_tier_summits': self.get_top_tier_summits(),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def send_alert(self, event):
        """
        发送高影响力事件提醒
        """
        # 通过Telegram发送提醒
        message = f"""
🚨 高影响力经济事件提醒

事件: {event['title']}
时间: {event['date']}
国家: {event['country']}
影响力: {event['impact']}

详情: {event['url']}
        """
        # 调用Telegram API发送
        pass

# 使用示例
monitor = MeetingMonitor()
report = monitor.generate_report()
print(json.dumps(report, indent=2, ensure_ascii=False))
```

### 定时监控Cron
```bash
# 每天早上8点检查未来30天的高影响力事件
0 8 * * * cd /root/.openclaw/workspace && python3 scripts/meeting_monitor.py
```

## 事件影响力评级

### ⭐⭐⭐ 极高影响（必须关注）
- 美联储FOMC会议 + 利率决议
- 美国非农就业数据
- 中国GDP季度数据
- 达沃斯世界经济论坛
- Jackson Hole央行年会

### ⭐⭐ 高影响（重点关注）
- 欧央行/日央行/英央行利率决议
- 美国CPI/PPI数据
- 中国CPI/PPI数据
- G20/G7峰会
- IMF/世界银行年会

### ⭐ 中影响（选择性关注）
- 其他发达国家央行会议
- 区域性经济数据
- 行业性峰会（金融科技、新能源等）

## 实战策略

### 1. 提前布局
- **Fed会议前**: 关注利率期货市场预期，提前1周布局
- **非农数据前**: 周四ADP数据作为预判，周五开盘前调整仓位
- **中国GDP前**: 关注先行指标（PMI、工业增加值），提前2-3天布局

### 2. 事件驱动交易
- **利率决议**: 关注点阵图和会后声明措辞变化
- **通胀数据**: 超预期→加息预期→债券下跌/美元上涨
- **峰会**: 关注政策信号（财政刺激、监管政策）

### 3. 风险规避
- **高波动期**: 会议/数据发布前减仓或对冲
- **黑天鹅**: 意外政策转向时快速止损

## 注意事项

1. **时区转换**: Trading Economics API返回UTC时间，需转换为北京时间
2. **数据延迟**: 免费API可能有15分钟延迟，付费版实时
3. **爬虫合规**: Bloomberg/活动行爬虫需遵守robots.txt，避免频繁请求
4. **信息过载**: 只关注⭐⭐⭐和⭐⭐级别事件，避免噪音

## 与其他技能协同

- **新闻事件驱动**: 会议结果出来后，结合新闻监控捕捉市场反应
- **资金流向分析**: 会议前后观察资金流向，验证市场预期
- **MACD监控**: 会议后观察技术面信号，确认趋势

## 学习资源

- Trading Economics官方文档: https://tradingeconomics.com/analytics/api.aspx
- 美联储官网: https://www.federalreserve.gov/
- 中国人民银行: http://www.pbc.gov.cn/
- Bloomberg Live: https://www.bloomberg.com/live
- 活动行: https://www.huodongxing.com/

---

**最后更新**: 2025-05-18  
**适用场景**: 宏观交易、事件驱动策略、风险管理  
**技能等级**: 高级（需要宏观经济和市场敏感度）
