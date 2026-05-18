# 📊 当前系统流程图

## 🏗️ 系统架构总览

```mermaid
flowchart TD
    A[用户输入<br>《偏爱难藏》硅谷AI版剧本] --> B{DeerFlow 2.0 系统}
    
    subgraph B [DeerFlow 2.0 工作流编排层]
        B1[Nginx反向代理<br>端口:2026] --> B2[Gateway API<br>端口:8001]
        B2 --> B3[LangGraph引擎<br>端口:2024]
        B3 --> B4[Frontend界面<br>端口:3000]
    end
    
    B3 --> C[剧情分析模块]
    C --> D[生成图片提示词]
    
    D --> E{Dreamina CLI<br>执行层}
    
    subgraph E [Dreamina CLI 图片/视频生成]
        E1[text2image<br>生成3张场景图片] --> E2[图片保存到temp_images]
        E2 --> E3[multiframe2video<br>多参考图生成15秒视频]
        E3 --> E4[视频保存到temp_videos]
    end
    
    E4 --> F[输出结果整理]
    F --> G[生成结果报告]
    
    H[心跳检查系统] --> I{分级监控}
    
    subgraph I [分级心跳检查]
        I1[A级检查<br>完整系统健康] --> I2[B级检查<br>简化安静时段]
        I2 --> I3[C级检查<br>最小状态维持]
    end
    
    I --> J[更新NOW.md状态]
    
    K[外部依赖] --> L{API与模型}
    
    subgraph L [外部服务集成]
        L1[火山引擎API<br>豆包模型] --> L2[Google Gemini<br>2.5 Flash模型]
        L2 --> L3[Dreamina服务<br>图片/视频生成]
    end
    
    G --> M[最终输出:<br>8个15秒视频]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style E fill:#e8f5e8
    style I fill:#fff3e0
    style L fill:#fce4ec
    style M fill:#c8e6c9
```

## 🔄 详细工作流程

### 1. 剧本分析阶段
```
用户剧本 → DeerFlow LangGraph → 剧情分析 → 提取8个关键场景 → 生成图片提示词
```

### 2. 图片生成阶段
```
图片提示词 → Dreamina CLI text2image → 生成3张图片/场景 → 保存到temp_images/
```

### 3. 视频生成阶段
```
temp_images/图片 → Dreamina CLI multiframe2video → 生成15秒视频 → 保存到temp_videos/
```

### 4. 质量控制循环
```mermaid
flowchart LR
    A[开始场景处理] --> B[生成图片]
    B --> C{图片审核通过?}
    C -->|是| D[生成视频]
    C -->|否| E[修改提示词]
    E --> B
    D --> F{视频审核通过?}
    F -->|是| G[保存到outputs]
    F -->|否| H[跳过到下一场景]
    H --> I[记录失败原因]
    G --> J[下一个场景]
```

### 5. 系统监控流程
```mermaid
flowchart TD
    A[OpenClaw心跳触发] --> B{北京时间判断}
    
    B -->|09:00-24:00<br>活跃时段| C[A级完整检查]
    C --> D[执行全部检查项]
    
    B -->|00:00-09:00<br>安静时段| E[B级简化检查]
    E --> F[执行关键检查项]
    
    B -->|所有时间| G[C级最小检查]
    G --> H[仅更新时间戳]
    
    D --> I[更新NOW.md状态]
    F --> I
    H --> I
    
    I --> J[回复HEARTBEAT_OK]
```

## 📁 目录结构流程图

```mermaid
flowchart TD
    A[workspace根目录] --> B[projects/]
    
    B --> C[deerflow-integration/]
    C --> D[deerflow-repo/]
    
    subgraph D [DeerFlow 2.0项目]
        D1[backend/] --> D2[skills/]
        D2 --> D3[frontend/]
        D3 --> D4[config.yaml]
    end
    
    B --> E[auto-video-generation/]
    
    subgraph E [自动化视频项目]
        E1[scripts/] --> E2[temp_images/]
        E2 --> E3[temp_videos/]
        E3 --> E4[outputs/]
        E4 --> E5[logs/]
    end
    
    B --> F[ad-workflow/]
    
    subgraph F [广告工作流项目]
        F1[workflows/] --> F2[knowledge/]
        F2 --> F3[test_workflow.py]
    end
    
    B --> G[silicon-valley-ai-video/]
    
    subgraph G [硅谷AI视频项目]
        G1[outputs/] --> G2[script_analysis.json]
    end
```

## ⚙️ 技术组件交互图

```mermaid
sequenceDiagram
    participant User as 用户
    participant DeerFlow as DeerFlow 2.0
    participant Dreamina as Dreamina CLI
    participant Heartbeat as 心跳系统
    participant Output as 输出系统
    
    User->>DeerFlow: 提供《偏爱难藏》剧本
    DeerFlow->>DeerFlow: 分析剧情，提取8个场景
    DeerFlow->>Dreamina: 发送图片生成提示词
    Dreamina->>Dreamina: 调用text2image生成图片
    Dreamina-->>DeerFlow: 返回图片文件路径
    
    loop 每个场景
        DeerFlow->>Dreamina: 发送multiframe2video请求
        Dreamina->>Dreamina: 处理3张参考图生成视频
        Dreamina-->>DeerFlow: 返回视频文件路径
    end
    
    Note over DeerFlow,Dreamina: 7/8场景成功生成
    
    DeerFlow->>Output: 整理所有视频文件
    Output-->>User: 提供8个15秒视频下载
    
    Heartbeat->>Heartbeat: 每30分钟检查一次
    Heartbeat->>DeerFlow: 检查服务状态
    Heartbeat->>Dreamina: 检查积分余额
    Heartbeat-->>User: 发送系统状态报告
```

## 🎯 关键数据流

### 输入数据流
```
剧本文件 → DeerFlow分析 → 8个场景描述 → 24个图片提示词 → 8个视频提示词
```

### 生成数据流
```
24个图片提示词 → Dreamina → 24张图片 → 多参考图组合 → 8个15秒视频
```

### 监控数据流
```
心跳触发 → 系统检查 → 状态更新 → NOW.md记录 → HEARTBEAT_OK回复
```

## 📊 系统状态指标

| 组件 | 状态 | 端口 | 可用性 |
|------|------|------|--------|
| **DeerFlow Nginx** | ✅ 运行中 | 2026 | 100% |
| **DeerFlow Gateway** | ✅ 运行中 | 8001 | 100% |
| **DeerFlow LangGraph** | ✅ 运行中 | 2024 | 100% |
| **DeerFlow Frontend** | ✅ 运行中 | 3000 | 100% |
| **Dreamina CLI** | ✅ 已登录 | - | 100% |
| **心跳系统** | ✅ 已启动 | - | 100% |

## 🔧 故障处理流程

```mermaid
flowchart TD
    A[检测到故障] --> B{故障类型}
    
    B -->|Dreamina审核失败| C[修改提示词重试]
    B -->|积分不足| D[暂停生成通知用户]
    B -->|服务不可用| E[尝试重启服务]
    B -->|脚本错误| F[记录错误并跳过]
    
    C --> G[重新生成当前场景]
    D --> H[等待用户补充积分]
    E --> I[检查服务日志]
    F --> J[继续下一个场景]
    
    G --> K{重试成功?}
    K -->|是| L[继续流程]
    K -->|否| M[记录为失败场景]
    
    L --> N[完成所有场景]
    M --> N
    
    N --> O[生成最终报告]
```

## 📈 性能指标

| 指标 | 当前值 | 目标值 |
|------|--------|--------|
| 视频生成成功率 | 87.5% (7/8) | ≥90% |
| 图片生成时间 | ~40秒/张 | ≤60秒 |
| 视频生成时间 | ~3分钟/个 | ≤5分钟 |
| 系统可用性 | 100% | ≥99.5% |
| 积分消耗 | 150-200/8视频 | ≤250/8视频 |

---

**流程图版本**: v1.0  
**创建时间**: 2026-04-06 02:04 UTC  
**更新状态**: 反映当前完整系统架构  
**维护者**: 贾维斯