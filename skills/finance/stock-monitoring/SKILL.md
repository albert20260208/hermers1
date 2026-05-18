---
name: stock-monitoring
description: A股股票监控方法 - MACD指标监控、价格提醒、成交量异常检测等技术分析监控策略
version: 1.0.0
author: user
license: MIT
metadata:
  hermes:
    tags: [stock, quant, trading, A股, MACD]
    homepage: 
prerequisites:
  commands: []
---

# A股股票监控方法

## 监控指标

### MACD (指数平滑移动平均线)
- **30分钟金叉/死叉** - 中短期趋势判断
- **15分钟金叉/死叉** - 短期趋势判断
- 死叉信号示例：蓝科高新、中金公司、瑞丰银行、西南证券

### 成交量异常
- 成交量放大/萎缩检测
- 与历史平均对比

### 布林带 (Bollinger Bands)
- 价格突破上轨/下轨检测

### 价格提醒
- 设定价格阈值，到达时触发提醒

## 相关脚本

| 脚本 | 功能 | 路径 |
|------|------|------|
| daily_macd_monitor.py | MACD监控 | ~/.openclaw/workspace/scripts/ |
| price_alert_monitor.py | 价格提醒 | ~/.openclaw/workspace/scripts/ |
| news_monitor.py | 新闻监控 | ~/.openclaw/workspace/scripts/ |

## 已知问题

1. **API数据源过期**：2026-03-16 过期，脚本可能使用缓存或模拟数据
2. **高频任务暂停**：MACD、价格提醒等高频监控任务因错误已被暂停
3. **chinese_calendar依赖**：A股监控脚本依赖此库

## cron定时任务配置

参考 `stock-watchlist-reminder` (每月1,15日)、`buy-desay-stock` (每月16日周一)、`buy-aotai-stock` (每周一)

## 注意事项

- 交易时间运行监控
- API数据源需定期更新
- 多个监控任务已暂停，需用户决策是否恢复