# 13F 机构持仓分析

[English Documentation](README.md)

AI 驱动的 SEC 13F 持仓分析工具——追踪巴菲特、段永平、Ackman 等顶级投资人的买卖动向。生成交互式 HTML 报告，包含组合演变图表、风格分析和大佬共识。

**支持所有主流 AI 编程工具：** Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Aider 等。

## 功能介绍

对 AI 说一个基金经理的名字，自动生成一份完整的 HTML 报告：

- **季度变化** — 新建仓、清仓、加减仓变动
- **全部持仓** — 可排序表格，点击跳转雅虎财经
- **板块分析** — 环形图 + 板块轮动趋势
- **持仓生命周期** — 历史上持有过的每只股票，含生命周期条和分类标签
- **组合演变** — SVG 图表：规模趋势、集中度、持仓构成变化
- **风格分析** — 雷达图 + 量化指标
- **季度浏览器** — 点击任意历史季度查看快照
- **大佬档案** — 背景、投资风格、经典交易

单个 HTML 文件，零依赖，深色/浅色主题切换，离线可用。

## 快速开始

### 安装

```bash
git clone https://github.com/jl3032/13f-analysis.git
cd 13f-analysis && ./setup
```

### 环境要求

- 任意 AI 编程助手（见下方平台配置）
- Python 3.6+
- curl
- 网络连接（SEC EDGAR API，免费，无需 API key）

### 使用方式

用自然语言提问即可：

```
"分析段永平的13F持仓"
"巴菲特最近在买什么？"
"对比段永平和巴菲特的持仓"
"大佬都在买什么"（共识分析）
"谁持有 TSLA"（个股反查）
"帮我找集中持仓的价值投资人"（发现模式）
```

## 平台配置

### Claude Code

```bash
git clone https://github.com/jl3032/13f-analysis.git ~/.claude/skills/13f-analysis
cd ~/.claude/skills/13f-analysis && ./setup
```

输入"13F"、"持仓"或基金经理名字即可自动触发。

### Cursor

在 `.cursor/rules` 或项目规则中添加：

```
Read the file 13f-analysis/SKILL.md and follow its instructions for analyzing SEC 13F institutional holdings.
Reference files: 13f-analysis/edgar-api-reference.md, 13f-analysis/filers-database.md
```

### Windsurf

在项目根目录的 `.windsurfrules` 中添加：

```
For 13F institutional holdings analysis, follow the instructions in 13f-analysis/SKILL.md.
Reference: 13f-analysis/edgar-api-reference.md and 13f-analysis/filers-database.md
```

### GitHub Copilot

在 `.github/copilot-instructions.md` 中添加：

```
When the user asks about 13F filings, institutional holdings, or fund manager portfolios,
follow the instructions in 13f-analysis/SKILL.md to fetch data from SEC EDGAR and generate
interactive HTML reports.
```

### Gemini CLI

在项目的 `GEMINI.md` 中添加：

```
For 13F analysis tasks, read and follow 13f-analysis/SKILL.md.
```

### 通用方式

将 `SKILL.md` 的内容复制到你的 AI 工具的系统提示词或自定义指令中即可。

## 报告功能

### 8 个交互标签页

| 标签页 | 内容 |
|--------|------|
| 季度变化 | 逐季对比：新建仓、清仓、加减仓 |
| 全部持仓 | 可排序表格，搜索过滤，仓位权重条 |
| 板块分析 | CSS 环形图 + 板块轮动表 |
| 持仓生命周期 | 每只股票的完整买入/持有/卖出历史 |
| 组合演变 | SVG 时序图（规模、集中度、持仓构成） |
| 风格分析 | 雷达图 + 量化风格指标 |
| 季度浏览器 | 交互式浏览任意历史季度 |
| 大佬档案 | 背景、风格、经典交易 |

### 核心特性

- **单文件 HTML** — CSS/JS 全部内联，零外部依赖
- **深色/浅色主题** — 一键切换，偏好自动保存
- **纯 SVG 图表** — 无需 Chart.js 或 D3
- **雅虎财经链接** — 每只股票可直接跳转查看行情
- **中英双语** — 标签和内容支持中英文
- **响应式** — 电脑和手机都能用

## 数据来源

所有数据直接来自 [SEC EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch) — 美国证券交易委员会的官方公开数据库。**免费，无需 API key，无需注册。**

## 预置基金经理（20 位）

| 分类 | 基金经理 |
|------|----------|
| 🔥 全网最火 | 大空头 Burry、木头姐 ARK、Ackman |
| 💰 中文投资圈 | 段永平、巴菲特、李录、高瓴/张磊 |
| 🏛️ 价值传奇 | Klarman、Pabrai、Einhorn |
| 📈 宏观 & 成长 | Druckenmiller、Tiger Global、Coatue |
| 🔄 稳健复利 | Gayner/Markel、Terry Smith |

支持分析任何 13F 申报机构——提供名字或 CIK 号码即可。

## 分析模式

| 模式 | 触发方式 | 输出 |
|------|---------|------|
| **单基金深度分析** | "分析段永平" | 完整 8 标签页 HTML 报告 |
| **多基金交叉对比** | "对比段永平和巴菲特" | 共识持仓矩阵 |
| **个股反查** | "谁持有 TSLA" | 哪些大佬持有这只股票 |
| **关注列表共识** | "大佬都在买什么" | 你关注的大佬们的共识方向 |
| **发现模式** | "帮我找重仓科技股的大佬" | AI 根据你的偏好推荐基金经理 |

## 测试

```bash
# 快速冒烟测试（2 个基金，约 30 秒）
python3 tests/test_pipeline.py --quick

# 完整测试（7 个基金，约 2 分钟）
python3 tests/test_pipeline.py
```

已通过 7 个基金经理的端到端验证，数据与 SEC 官方交叉核对。

## 免责声明

**本工具仅供信息参考和学习用途，不构成任何投资建议。**

- 13F 数据有 45 天滞后，不代表基金经理当前持仓
- 历史持仓不预测未来表现
- 作者不是持牌投资顾问
- 投资有风险，决策需谨慎
- 使用风险自担——详见 MIT 许可证 "AS IS" 条款

## 许可证

MIT 许可证。详见 [LICENSE](LICENSE)。

## 致谢

数据来源：[SEC EDGAR](https://www.sec.gov/)（免费公开 API）。股票链接：[Yahoo Finance](https://finance.yahoo.com/)。
