# 无头浏览器技能学习研究记录 (Agent Browser)

## 📅 研究日期
- **开始时间**: 2026-03-27 13:35 UTC (21:35 北京时间)
- **结束时间**: 2026-03-27 14:56 UTC (仍在进行中)
- **记录时间**: 2026-03-27 15:20 UTC (23:20 北京时间)

## 🎯 研究背景
用户通过QQ询问GitHub上最近很火的无头浏览器技能（下载量很大），要求查相关信息并引导安装。

## 🔍 搜索结果（核心发现）

### 1. 技能基本信息
| 项目 | 详情 |
|------|------|
| **技能名称** | Agent Browser |
| **开发者** | @TheSethRose |
| **GitHub 仓库** | [openclaw/skills/tree/main/skills/thesethrose/agent-browser](https://github.com/openclaw/skills/tree/main/skills/thesethrose/agent-browser) |
| **下载量** | **约 13.8 万次** (137.7k downloads) |
| **安装量** | 约 2.6k installs |
| **最新版本** | v0.2.0 (2026-01-20) |
| **分类** | 浏览器与自动化 (Browser & Automation) |

### 2. 主要特点

**技术栈优势**
- **Rust 核心**：高性能的无头浏览器自动化 CLI
- **Node.js 回退**：当 Rust 版本不可用时自动切换
- **结构化命令**：专为 AI 代理设计的命令接口

**核心功能**
- **导航**：打开网页、跳转、前进/后退
- **交互**：点击元素、输入文本、提交表单
- **截图**：捕获页面或特定区域的截图
- **DOM 操作**：获取元素信息、执行 JavaScript
- **调试模式**：`--headed` 参数显示浏览器窗口
- **连接 CDP**：通过 Chrome DevTools 协议连接

**易用性设计**
- **稳定的引用**：页面加载后元素引用保持稳定
- **智能填充**：推荐使用 `fill` 而非 `type` 确保清空原有内容
- **快照机制**：导航后自动获取新页面的元素引用

### 3. 安装方式

```bash
# 通过 clawhub 安装（推荐）
npx clawhub@latest install thesethrose/agent-browser

# 或通过 npm 全局安装
npm install -g agent-browser
agent-browser install  # 下载 Chromium

# 在 Linux 上安装系统依赖
agent-browser install --with-deps

# 通过 Homebrew 安装
brew install TheSethRose/tap/agent-browser
```

### 4. 类似技能对比

| 技能名称 | 特点 | 适用场景 |
|----------|------|----------|
| **Agent Browser** | Rust 核心，性能高，AI 代理友好 | AI 代理控制浏览器、网页交互 |
| **lightpanda-io/agent-skill** | 集成 Lightpanda，优化数据提取 | 大规模网页抓取和数据提取 |
| **browser-automation-skill** | 通用浏览器自动化 | 多浏览器支持 |
| **camoufox-tools** | 基于 Firefox 的无头浏览器 | Firefox 特定需求 |

## 🛠️ 安装状态确认

### 当前安装状态
- **安装时间**: 2026-03-27（根据 MEMORY.md 记录）
- **安装路径**: `/root/.openclaw/workspace/skills/agent-browser/`
- **CLI工具**: `agent-browser` v0.22.3
- **浏览器**: Chromium v147.0.7727.24
- **技能文件**: `/root/.openclaw/workspace/skills/agent-browser/SKILL.md`

### 验证安装
```bash
# 检查技能目录
ls -la /root/.openclaw/workspace/skills/agent-browser/

# 检查 agent-browser 命令是否可用
which agent-browser || agent-browser --version
```

## 📚 技能文档摘要

### 核心工作流程
1. **导航**: `agent-browser open <url>`
2. **快照**: `agent-browser snapshot -i`（获取交互元素引用，如 `@e1`, `@e2`）
3. **交互**: 使用快照中的引用进行点击、填写等操作
4. **重新快照**: 导航或 DOM 变化后重新获取引用

### 常用命令速查

| 类别 | 命令示例 | 功能 |
|------|----------|------|
| **导航** | `agent-browser open <url>` | 打开网页 |
| **快照** | `agent-browser snapshot -i` | 获取交互元素引用 |
| **点击** | `agent-browser click @e1` | 点击元素 |
| **填写** | `agent-browser fill @e2 "text"` | 填写表单 |
| **等待** | `agent-browser wait @e1` | 等待元素出现 |
| **截图** | `agent-browser screenshot` | 截取屏幕 |
| **录制** | `agent-browser record start demo.webm` | 录制操作视频 |

### 示例：表单提交
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# 输出显示: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # 检查结果
```

### 调试技巧
- 使用 `--headed` 参数显示浏览器窗口进行调试
- 使用 `agent-browser console` 查看控制台消息
- 使用 `agent-browser highlight @e1` 高亮元素

## 🚀 后续推进建议

### 短期目标（明天可立即开展）
1. **基础测试**: 使用 `agent-browser` 访问简单网页，练习基本命令
2. **表单自动化**: 尝试自动化登录、搜索等常见表单操作
3. **数据提取**: 练习从网页中提取结构化数据

### 中期目标
1. **集成到现有项目**: 将浏览器自动化集成到 A 股数据抓取或其他监控任务
2. **技能组合**: 结合其他技能（如数据解析、API 调用）构建完整工作流
3. **性能优化**: 探索 Rust 版本与 Node.js 版本的性能差异

### 学习资源
1. **官方文档**: `skills/agent-browser/SKILL.md`（已完整复制）
2. **GitHub 仓库**: [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
3. **示例项目**: 查看 OpenClaw 社区中的使用案例

## 📝 今日学习收获
1. **技能发现**: 了解了 Agent Browser 作为目前最流行的无头浏览器技能
2. **技术优势**: Rust 核心带来的性能优势，专为 AI 代理设计的接口
3. **安装完成**: 技能已成功安装并验证
4. **文档齐全**: 拥有完整的命令参考和示例

## 🔗 相关文件
- **MEMORY.md**: 记录了技能安装状态
- **SKILL.md**: `/root/.openclaw/workspace/skills/agent-browser/SKILL.md`（完整文档）
- **对话记录**: `memory/2026-03-27-1404.md`（包含详细搜索和讨论）

## ⏭️ 明天行动步骤
1. 读取此文件恢复上下文
2. 运行 `agent-browser --version` 确认环境
3. 从"后续推进建议"中选择一个短期目标开始测试
4. 记录测试结果和遇到的问题

---
**记录人**: 贾维斯 (Jarvis)  
**记录时间**: 2026-03-27 15:20 UTC  
**下次查看**: 明天开始浏览器自动化任务前