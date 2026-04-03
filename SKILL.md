---
name: 13f-analysis
description: Use when user asks to analyze institutional 13F holdings, compare fund manager positions, track quarterly portfolio changes, identify long-term core holdings, or research what major investors are buying/selling. Triggers on "13F", "持仓", "holdings", fund manager names, or institutional investment analysis requests.
---

# 13F Institutional Holdings Analysis

## Overview

Analyze SEC 13F filings to track what major institutional investors are buying, selling, and holding. Core capability: fetch raw data from SEC EDGAR, parse holdings, compare across quarters, and produce actionable reports for fund managers.

**13F = quarterly snapshot of long positions for US institutions managing >$100M. Filed within 45 days of quarter-end.**

## When to Use

- User asks about institutional holdings or 13F filings
- User names a fund manager and wants portfolio analysis
- User wants to compare holdings across quarters or across managers
- User asks "what is [manager] buying/selling"
- User wants sector/industry allocation analysis
- User asks about a specific stock's institutional ownership history

## Limitations to Always Disclose

1. **45-day lag** — Q2 data appears by ~Aug 15, reflects June 30 snapshot
2. **Long-only** — no shorts, options, futures, or derivatives visible
3. **Confidential treatment** — active positions may be hidden temporarily
4. **Snapshot only** — high-frequency/quant funds may have turned over positions within the quarter

## Language Detection

Detect the user's language from their input and respond accordingly:
- If user writes in Chinese → respond in Chinese, show Chinese labels in reports
- If user writes in English → respond in English, show English labels in reports
- Default: English
- Reports are always bilingual (English + Chinese labels) regardless of input language

## Onboarding

When the user's input is vague (e.g., just "13F", "holdings", "show me some funds"), **show the Quick Menu from filers-database.md** — a categorized list of popular managers with numbered options.

If user has a watchlist file (`13f_watchlist.md` in the working directory), mention it: "You have X managers in your watchlist. Want to see the latest updates?"

## Input Recognition

User may provide:
- Fund manager name (e.g., "巴菲特", "Buffett", "Druckenmiller")
- Fund/entity name (e.g., "Berkshire Hathaway", "Bridgewater")
- CIK number directly
- A stock ticker for reverse lookup (Mode 3: "谁持有TSLA")
- A number from the Quick Menu (e.g., "1" = 段永平)
- "我的关注列表" / "my watchlist" — load from watchlist file
- "对比 X 和 Y" / "compare X and Y" — Mode 2
- **A description/requirement** — see Discovery Mode below

**First step:** Map input to CIK number. Check filers-database.md for known filers. If not found, try Discovery Mode or search SEC EDGAR.

## Discovery Mode / 帮我找基金经理

When the user doesn't know a specific name but describes what they want, enter Discovery Mode:

**Trigger phrases:**
- "帮我推荐几个值得关注的基金经理"
- "有没有重仓科技股的大佬"
- "谁的风格跟巴菲特像"
- "哪些基金经理最近在买中概股"
- "我想找集中持仓、长期持有的价值投资人"
- "有没有管理规模小但业绩好的"
- Any vague description of a style, sector, or preference

**Flow:**

1. **Parse the requirement** — extract keywords: style (集中/分散, 价值/成长), sector preference (科技/金融/消费), scale (大型/小型), geography (中概/美股), etc.

2. **Search in filers-database.md first** — filter the 20 pre-mapped managers by matching criteria. Present as options:

```
🔍 根据你的要求"集中持仓的价值投资人"，推荐：

  A. 段永平 (Himalaya) — 9 只股票，43.9% 重仓谷歌，极致集中
  B. Bill Ackman (Pershing) — 11 只股票，激进价值+activist
  C. Seth Klarman (Baupost) — 22 只股票，深度价值，低调神秘
  D. Mohnish Pabrai — 3-5 只股票，巴菲特信徒，最极致的集中

想看谁的？可以选多个（比如 "A 和 D"），也可以说 "都加到关注列表"
```

3. **If no match in database** — search SEC EDGAR using EFTS full-text search:
```
GET https://efts.sec.gov/LATEST/search-index?q={keywords}&forms=13F-HR
```
Present discovered filers as options with basic info (entity name, CIK, recent filing date).

4. **User selects** → proceed to Mode 1 (single fund) or add to watchlist

**Key principles:**
- Always give **numbered/lettered options**, don't just dump a list
- Include a one-line hook for each option explaining WHY it matches the user's requirement
- Offer to "都加到关注列表" as a quick action
- If user's requirement is about a specific stock ("谁在买 NVDA"), redirect to Mode 3 instead

## Watchlist / 关注列表

Users can maintain a personal watchlist at `13f_watchlist.md` in their working directory.

**Format:**
```markdown
# My 13F Watchlist

- 段永平 / Himalaya Capital (CIK 0001709323)
- 巴菲特 / Berkshire Hathaway (CIK 0001067983)
- Bill Ackman / Pershing Square (CIK 0001336528)
```

**Operations:**
- "加 Druckenmiller 到关注列表" → append to file, confirm
- "从关注列表删除 ARK" → remove from file, confirm
- "我的关注列表" / "看看我关注的基金" → read file, list all
- "关注列表最新动态" / "watchlist update" → for each manager, fetch latest quarter, generate a one-line summary of changes. Output as a summary table:

```
📊 关注列表最新动态 (Q4 2025)

| 基金经理 | 最新操作 | 组合规模 |
|----------|---------|---------|
| 段永平 | 新买 CROCS，清仓 SABLE，其余不动 | $35.7亿 |
| 巴菲特 | 减仓 AAPL，加仓 OXY | $2,664亿 |
| Ackman | 新买 META，清仓 CMG | $155亿 |

想看哪个的详细报告？
```

If the watchlist file doesn't exist and user asks about it, create it with a default template.

- **"共识分析" / "consensus" / "大佬都在买什么"** → Mode 4: Watchlist Consensus Analysis (see below)

## Analysis Modes

```dot
digraph modes {
  rankdir=LR;
  "User Input" [shape=doublecircle];
  "Has Watchlist?" [shape=diamond];
  "Single Fund?" [shape=diamond];
  "Single Stock?" [shape=diamond];
  "Fund Deep Dive" [shape=box];
  "Cross-Fund Compare" [shape=box];
  "Stock Ownership Timeline" [shape=box];
  "Watchlist Consensus" [shape=box];

  "User Input" -> "Has Watchlist?" [label="consensus/共识/大佬都在买什么"];
  "Has Watchlist?" -> "Watchlist Consensus" [label="yes"];
  "Has Watchlist?" -> "Cross-Fund Compare" [label="no, prompt to create"];
  "User Input" -> "Single Fund?" [label="specific name"];
  "Single Fund?" -> "Fund Deep Dive" [label="one fund"];
  "Single Fund?" -> "Single Stock?" [label="multiple or none"];
  "Single Stock?" -> "Stock Ownership Timeline" [label="stock focus"];
  "Single Stock?" -> "Cross-Fund Compare" [label="multi-fund"];
}
```

### Mode 1: Fund Deep Dive (Single Institution)

**Input:** Fund name/manager → CIK
**Data needed:** Latest 2-6 quarters of 13F filings

**Output structure:**

#### 1. Manager Profile
- Background, investment style, AUM, famous trades
- Style classification: long-term concentrated / diversified / quant / activist
- **If high-frequency/quant → warn user: 13F has limited reference value**

#### 2. Current Portfolio Snapshot
- Top 20 holdings by value (name, **Chinese name/简称**, shares, value, % of portfolio)
- **Chinese stock names:** Always include a Chinese name or brief description for each stock, e.g. "EAST WEST BANCORP (华美银行)", "ALPHABET (谷歌)", "PDD HOLDINGS (拼多多)". Use Claude's knowledge to provide accurate Chinese names.
- **Concentration metric:** top 10 holdings as % of total portfolio
- Sector/industry breakdown

#### 3. Quarterly Changes (most important)
Compare latest quarter vs previous quarter:

| Category | Fields |
|----------|--------|
| **New positions** | Stock, shares, value, % of portfolio |
| **Eliminated positions** | Stock, previous shares, previous value |
| **Significant increases** (>25% shares change) | Stock, shares before/after, value change, new % |
| **Significant decreases** (>25% shares change) | Stock, shares before/after, value change, new % |
| **Unchanged core** | Stocks with <5% share change |

#### 4. Long-term Core Holdings & Transaction History
- Positions held 4+ consecutive quarters
- Entry timeline (first appeared, share count progression)
- **Buy price range:** for each buy/add quarter, show that quarter's stock price low ~ high as reference
- **Current price position:** For each stock, show where the current price sits relative to the buy quarter's price range. Use a simple indicator:
  - "在买入区间内" / "Within buy range" — current price is between quarter low and high
  - "高于买入区间 +X%" / "Above buy range +X%" — current price above the high
  - "低于买入区间 -X%" / "Below buy range -X%" — current price below the low (potential opportunity)
- Do NOT estimate cost basis or P&L — just show the price range and current relative position

#### 5. Sector Allocation Trend
- Sector weights per quarter (use CUSIP → sector mapping or issuer name heuristics)
- Highlight sector rotation: increasing/decreasing allocations

#### 6. Position Sizing Analysis
- New position sizes relative to portfolio (conviction indicator)
- Largest single-quarter additions

### Mode 2: Cross-Fund Comparison

**Input:** Multiple fund names/managers (e.g., "对比段永平和巴菲特", "Compare Ackman, Einhorn and Klarman")
**Data needed:** Same quarter(s) for all funds

**Output structure:**

#### 1. Side-by-side Changes
For each fund: new positions, eliminated, major increases/decreases

#### 2. Consensus Holdings / 共识持仓 (HIGHLIGHT THIS)
Stocks held by 2+ of the selected managers — **this is what retail investors care about most**
- Show as a matrix table: rows = stocks, columns = managers, cells = % of portfolio (or "—" if not held)
- Sort by number of managers holding the stock (descending)
- Color-code: green if recently added by multiple managers, red if recently reduced
- Add Chinese stock names

#### 3. Consensus Moves / 共识动作
Stocks that multiple managers bought or sold in the same quarter — **strongest signal**
- "巴菲特和段永平同时加仓 BAC" is a powerful insight for retail investors

#### 4. Sector Comparison
Each manager's sector allocation side by side

#### 5. Style Comparison
Radar charts overlaid or side-by-side showing how managers differ in concentration, turnover, etc.

### Mode 3: Stock Ownership Timeline (个股反查)

**Input:** Stock ticker/name (e.g., "哪些大佬持有TSLA？", "Who owns Apple?")
**Data needed:** Multiple quarters of 13F data for ALL known filers, filtered for target stock (by CUSIP)

This mode answers: **"我看中了这只股票，哪些大佬也在买？"** — a core use case for retail investors.

**Output structure:**

#### 1. Ownership Matrix / 持仓矩阵
Table: rows = managers (from filers-database.md), columns = recent quarters, cells = shares held or "—"
- Highlight: green if recently added, red if recently reduced, bold if top-10 holding for that manager
- Sort by current position size descending

#### 2. Entry/Exit Price Context
For each institution's entry and exit, show the stock's price range during that quarter as reference

#### 3. Conviction Indicator
For each holder, show what % of their portfolio this stock represents — higher % = higher conviction

#### 4. Who Sold Too Early
Institutions that exited before significant price appreciation

### Mode 4: Watchlist Consensus Analysis (大佬共识)

**Input:** "共识分析", "大佬都在买什么", "consensus", "我关注的大佬有什么共同持仓"
**Data needed:** Latest 2 quarters for ALL managers in the user's watchlist
**Prerequisite:** Watchlist file must exist. If not, prompt user to create one first.

This is the **killer feature for retail investors** — "I don't know who to look at specifically, just tell me where the smart money is going."

**Flow:**
1. Read `13f_watchlist.md` in working directory
2. For each manager: fetch latest 2 quarters of 13F data
3. Compute consensus analysis
4. Output as structured text (not HTML report — this is a quick overview)

**Output structure:**

#### 1. Consensus Holdings / 共识持仓
Stocks held by 2+ watchlist managers, sorted by holder count descending:
```
共识持仓 — 被 2 个以上大佬同时持有:

| 股票 (中文名)           | 几人持有 | 谁在持有 (占比)                           |
|------------------------|---------|------------------------------------------|
| ALPHABET (谷歌)         | 4       | 段永平 22%, Ackman 12.5%, Gayner 6.9%... |
| AMAZON (亚马逊)         | 4       | Ackman 14.3%, Klarman 9.3%...            |
| APPLE (苹果)            | 3       | 巴菲特 22.6%, Gayner 2.7%...             |
```

#### 2. Consensus Moves / 本季度共识动作
Stocks where 2+ managers made the same directional move this quarter:
- "Ackman 和 Gayner 同时加仓 Brookfield" → strong buy signal
- "Klarman 和 Burry 同时新建仓 Molina Healthcare" → new idea convergence
If no consensus moves: "本季度各买各的，没有共识方向操作"

#### 3. Sector Consensus / 板块共识
Table showing each manager's sector allocation, with an average column:
```
| 板块       | 段永平 | 巴菲特 | Ackman | ... | 平均  |
|-----------|--------|--------|--------|-----|-------|
| Tech      | 44.7%  | 24.8%  | 39.5%  |     | 27.8% |
| Financials| 37.5%  | 0.0%   | 18.1%  |     | 9.7%  |
```

#### 4. Action Prompt
End with: "想看某个共识股票的详细反查？还是看某个大佬的完整报告？"

**Key principles:**
- This mode outputs TEXT, not HTML — it is a quick scan, not a deep dive
- Always include Chinese stock names
- Sort by "signal strength" (more holders = stronger signal)
- The consensus moves section is the most actionable — highlight it
- If watchlist has < 3 managers, suggest adding more for better consensus signal

## Data Fetching Workflow

**REQUIRED:** See edgar-api-reference.md for complete API details.

### Step-by-step for one filer, one quarter:

```
1. GET https://data.sec.gov/submissions/CIK{padded_cik}.json
   Headers: User-Agent: 13F-Analysis research@example.com
   → Extract filings.recent, filter form=="13F-HR", match reportDate for target quarter
   → Get accessionNumber

2. GET https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dashes}/
   → Find the INFORMATION TABLE XML filename (not primary_doc.xml)

3. GET https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dashes}/{info_table.xml}
   → Parse XML: each <infoTable> entry = one holding
   → Extract: nameOfIssuer, cusip, value, sshPrnamt, sshPrnamtType, putCall
```

### For bulk/historical analysis:

Use SEC quarterly data sets (TSV format, much faster for multi-filer analysis):
```
https://www.sec.gov/files/structureddata/data/form-13f-data-sets/
```
Download the ZIP for each quarter, filter INFOTABLE.tsv by accession numbers.

### Rate limits:
- 10 requests/second max
- **Always include User-Agent header** or you get 403

## Comparing Quarters

To detect changes between Q(n) and Q(n-1):

```python
# Pseudocode - match holdings by CUSIP
for cusip in all_cusips:
    prev = prev_quarter.get(cusip)
    curr = curr_quarter.get(cusip)
    if curr and not prev:        # NEW POSITION
    elif prev and not curr:      # ELIMINATED
    elif abs(curr.shares - prev.shares) / prev.shares > 0.25:  # SIGNIFICANT CHANGE
    else:                        # STABLE
```

**Key:** Match by CUSIP, not by issuer name (names can vary slightly between filings).

## Buy Price Range (Not Cost Estimation)

13F doesn't disclose purchase price. Instead of estimating cost basis:

- For each buy/add quarter, show the stock's **price range (low ~ high)** during that quarter
- This gives users a reference for the likely purchase price range
- Do NOT calculate estimated cost, weighted average cost, or P&L estimates
- Do NOT include "Est. Cost Range", "Est. P&L", or "Confidence" columns
- The transaction timeline table columns should be: Quarter, Action, Shares Change, Total After, Price Range

To get historical stock prices for the quarter range, use WebFetch with Yahoo Finance.

## Stock Links

**Every stock name in the report must link to Yahoo Finance** (`https://finance.yahoo.com/quote/{TICKER}`):
- Use `target="_blank" rel="noopener noreferrer"` to open in new tab (rel required for security)
- Style: inherit text color, no underline by default, blue underline on hover
- Apply to: All Holdings table, Quarterly Changes table, Transaction Timeline headers
- For Berkshire Hathaway CL B, use `BRK-B` (Yahoo format, not `BRK.B`)

## Historical Data Collection (Full History Mode)

When generating a deep analysis report with historical modules, fetch ALL 13F filings for the filer:

1. Use the submissions API to get all filing accession numbers
2. For each filing, find the info table XML via index.json (filename varies: could be InfoTable.xml, 13fq32022.xml, etc.)
3. Parse XML holdings, match by CUSIP across quarters
4. Handle value scale: older filings use value-in-thousands, newer filings (2024+) use full dollars — detect by checking if max single position value > $100B raw
5. For amended filings (13F-HR/A), use the amendment instead of original
6. Note: CIK may change (e.g., Himalaya Capital changed from 1709323 to filing agent 2043585 in 2025, but filings remain under original CIK path)

Embed all data as inline `HISTORICAL_DATA` JSON in the HTML report.

## HISTORICAL_DATA JSON Schema

Top-level keys:

- **`meta`**: cik, entity, manager, quarters array, generatedDate
- **`quarters`**: per-quarter snapshots — reportDate, totalValue, positionCount, holdings array with cusip/name/ticker/sector/shares/value/pctOfPortfolio
- **`stocks`**: per-stock lifecycle keyed by CUSIP — name, ticker, sector, firstQuarter, lastQuarter, totalQuartersHeld, isCurrentlyHeld, classification (Core 8+Q / Medium-term 4-7Q / Short-lived 1-3Q), transactions array
- **`evolution`**: time series for charts — quarters, totalAum, positionCount, top3Pct, top5Pct, stockShares per CUSIP
- **`styleMetrics`**: avgPositionCount, avgHoldingPeriodQuarters, turnoverRate, newPositionFrequency, exitFrequency, sectorConcentrationHHI, topSectorPct, avgNewPositionSizePct, radar (6 axes 0-100)

## Extended Report Modules

- **Portfolio Evolution (Module A)**: SVG time series charts — AUM, concentration, stacked composition. Lazy rendering.
- **Stock Lifecycle (Module B)**: Enhanced transaction history with lifecycle bars, classification badges, filter buttons. All stocks ever held including exited.
- **Style Analysis (Module C)**: Radar chart + metrics table + auto-generated bilingual style summary + **historical win rate** (新建仓后持有 4 季度的胜率，即 4 季度后该股票仍在组合中且市值上涨的比例).
- **Quarter Browser (Module D)**: Interactive quarter selector, dynamic holdings table + diff rendering.

## SVG Chart Guidelines

- All charts pure SVG, generated by inline JS from `HISTORICAL_DATA`
- Use `document.createElementNS('http://www.w3.org/2000/svg', ...)` for element creation
- Standard viewBox: `0 0 900 300` for line charts, `0 0 900 400` for stacked area, `0 0 400 400` for radar
- Color palette: same as donut chart colors
- Responsive: SVG `viewBox` + container `width: 100%`
- Lazy rendering: only init when tab first activated
- Hover tooltips via absolute-positioned divs

## Output: Interactive HTML Report

**ALWAYS output as a self-contained HTML file** saved to the project directory (e.g., `13f_report_{manager}_{date}.html`).

### Dark/Light Theme Toggle
The HTML report must include a theme toggle button in the header area. Implementation:

**CSS:** Define both themes using CSS variables on `:root` (dark, default) and `[data-theme="light"]`:
```css
:root { /* Dark theme - default */
  --bg: #0f172a; --surface: #1e293b; --surface-2: #273548;
  --border: #334155; --text: #e2e8f0; --text-muted: #94a3b8; --text-dim: #64748b;
}
[data-theme="light"] {
  --bg: #f8fafc; --surface: #ffffff; --surface-2: #f1f5f9;
  --border: #e2e8f0; --text: #1e293b; --text-muted: #64748b; --text-dim: #94a3b8;
}
```
- Green/red/blue/amber accent colors stay the same in both themes
- SVG chart text color uses `var(--text-muted)`, adapts automatically

**HTML:** A toggle button in the header, right side:
```html
<button onclick="toggleTheme()" class="theme-toggle" title="Switch theme">🌓</button>
```

**JS:**
```javascript
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('13f-theme', next);
}
// Restore preference on load
const saved = localStorage.getItem('13f-theme');
if (saved) document.documentElement.setAttribute('data-theme', saved);
```

**Style for the toggle button:**
```css
.theme-toggle {
  background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
  padding: 6px 12px; cursor: pointer; font-size: 18px; color: var(--text);
  transition: all 0.2s;
}
.theme-toggle:hover { border-color: var(--blue); }
```

User preference persists via localStorage across page reloads.

### CRITICAL: JS String Safety Rules
When generating HTML reports with inline JS:
- **Use backtick template literals** (\`...\`) for all HTML content strings, NOT single quotes
- **Use \${variable} interpolation** instead of string concatenation (' + var + ')
- **NEVER use apostrophes** in English text inside JS strings. Write "does not" not "doesn't", "Gayner is" not "Gayner's"
- **For onclick in template literals**, use: \`onclick="fn('arg')"\`
- Violation of these rules causes silent JS failures where all tabs render as empty

### HTML Design Principles
- **Single-file, zero dependencies** — all CSS/JS inline, opens in any browser
- **Dark theme** with professional financial aesthetic (dark navy/charcoal bg, accent colors for up/down)
- **Color coding:** green (#22c55e) for increases/new positions, red (#ef4444) for decreases/eliminated, neutral gray for unchanged
- **Interactive features:**
  - Sortable tables (click column headers)
  - Expandable sections (click to toggle details)
  - Hover tooltips on data points
  - Filter/search box for holdings
  - Tab navigation between analysis sections
  - Responsive — works on desktop and mobile

### HTML Structure Template

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>13F Analysis — {Manager Name}</title>
  <style>
    /* Dark financial theme */
    :root {
      --bg: #0f172a; --surface: #1e293b; --border: #334155;
      --text: #e2e8f0; --text-muted: #94a3b8;
      --green: #22c55e; --red: #ef4444; --blue: #3b82f6; --amber: #f59e0b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, 'SF Pro', 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }
    /* ... full styles inline ... */
  </style>
</head>
<body>
  <!-- Header with manager name, AUM, style badge -->
  <!-- Tab navigation: Quarterly Changes | All Holdings | Sector View | Transaction History | Portfolio Evolution | Style Analysis | Quarter Browser | Manager Profile -->
  <!-- Each tab = one analysis section -->
  <!-- Sortable tables with JS -->
  <!-- Charts using inline SVG or CSS bar charts (no external libs) -->
  <script>
    // Sortable tables, tab switching, search/filter, expand/collapse
  </script>
</body>
</html>
```

### Visual Components to Include

1. **One-line summary / 一句话摘要** — At the very top of the report (in the insight box before tabs), write a 2-3 sentence Chinese summary of the key takeaway. Example: "段永平Q4 2025对所有持仓零交易。唯一操作是新建仓CROCS（试探性仓位）和清仓SABLE OFFSHORE。" This helps casual users get the gist without reading the full report.
2. **Summary cards** at top — AUM, # positions, top holding, concentration %, quarter
2. **Holdings table** — sortable by name/value/shares/change%, with inline bar for portfolio weight
3. **Changes table** — new/eliminated/increased/decreased with color-coded badges
4. **Sector donut chart** — pure CSS/SVG, no Chart.js needed
5. **Timeline sparklines** — for core holdings showing share count over quarters (SVG)
6. **Comparison matrix** — for cross-fund mode, heat-map style grid

### Report Footer Disclaimer
Every generated HTML report MUST include this disclaimer in the footer:
```
Data source: SEC EDGAR 13F-HR filings · Values as of {REPORT_DATE}
13F data has 45-day lag. Long positions only. No shorts, options, or derivatives.
本报告仅供信息参考，不构成投资建议。投资有风险，决策需谨慎。
For informational purposes only. Not investment advice.
```

### Formatting Rules
- $ values: `$1,234,567,890` with commas
- Percentages: 1 decimal place with +/- prefix for changes
- Large numbers: abbreviate in cards (e.g., $266.4B) but full in tables
- Sort by value descending by default
- Chinese + English bilingual labels where appropriate

## Playbook: Full Institutional Report

When user requests a comprehensive report, follow this sequence:

1. **机构画像** — Manager profile, historical returns, famous trades, AUM, style
2. **投资风格分析** — Known quotes, philosophy, concentration vs diversification
3. **核心底仓** — Stock lifecycle with classification, lifecycle bars, and transaction timeline (Module B)
4. **近期新建仓** — New positions in past 2-4 quarters with context (company events, price range, PE, earnings)
5. **近期清仓** — Eliminated positions with retrospective analysis
6. **大幅加减仓** — Significant changes with conviction analysis
7. **板块配置变化** — Sector rotation trends, cross-manager comparison
8. **热门股票追踪** — Single-stock institutional ownership timeline (optional)
9. **组合演变** — Portfolio evolution charts: AUM, concentration, composition (Module A)
10. **风格量化** — Style analysis: radar chart, metrics, bilingual summary (Module C)

## Edge Cases & Known Issues

### 1. Value Scale: Thousands vs Full Dollars
- Older 13F filings (pre-2024) report `value` in thousands of USD
- Newer filings (2024+) may report `value` in full dollars
- **Detection:** Compare sum of all holdings' `value` against `tableValueTotal` from the cover page (primary_doc.xml). If ratio is ~1000x, one is in thousands.
- **Handling:** Always fetch the cover page total and calibrate. If `raw_total / cover_total ≈ 1.0`, same scale. If ratio ≈ 1000, adjust accordingly.

### 2. CIK Changes (Filing Agent)
- Some filers change their filing agent, resulting in a new CIK prefix in accession numbers
- Example: Himalaya Capital — original CIK 1709323, but 2025 filings have accession numbers starting with 0002043585
- The filings are still stored under the ORIGINAL CIK path on EDGAR
- **Detection:** When index.json returns 404 under the accession prefix CIK, try the original CIK
- **Handling:** Always try the entity's CIK from submissions JSON first, then fall back to accession prefix CIK

### 3. Missing Quarters
- Not all filers file every quarter. Some may skip quarters (especially smaller/newer filers)
- Example: Himalaya Capital has no filings for 2018Q4, 2019Q1-Q3
- **Handling:** Don't assume consecutive quarters. Use actual reportDate values. In evolution charts, show gaps or interpolate.

### 4. Amended Filings (13F-HR/A)
- Amendments supersede original filings for the same reportDate
- A filer may file 13F-HR on Feb 17, then 13F-HR/A on Feb 19
- **Handling:** When multiple filings share the same reportDate, always prefer 13F-HR/A (the amendment)

### 5. Large Portfolios (100+ positions)
- Filers like Markel (128 positions), ARK Invest (196 positions) generate large info tables
- The HTML report with full HISTORICAL_DATA JSON can exceed 200KB
- **Handling:** For stacked area charts, group stocks with <3% average portfolio share into "Other". Consider pagination for the holdings table. Lazy-render charts.

### 6. CUSIP Aggregation
- The same CUSIP may appear multiple times in a single filing (different sub-advisors or voting authority splits)
- **Handling:** Always aggregate by CUSIP — sum shares and value for duplicate entries

### 7. XML Namespace Variations
- The 13F info table XML uses namespace `http://www.sec.gov/edgar/document/thirteenf/informationtable`
- But the prefix varies: some files use `ns1:`, others use the default namespace
- **Handling:** Always use the full namespace URI in ElementTree queries: `{http://www.sec.gov/edgar/document/thirteenf/informationtable}infoTable`

### 8. Info Table Filename Variations
- The holdings XML file is NOT always named `InfoTable.xml` or `infotable.xml`
- Real examples: `13fq32022.xml`, `13fhciq425v2.xml`, `infotable.xml`
- **Handling:** Use `index.json` to discover the filename. Pick the XML file that is NOT `primary_doc.xml` and NOT an index file.

### 9. Stock Splits
- A stock split causes share count to jump (e.g., 4:1 split = 4x shares) without any actual buying
- This can be misinterpreted as a "MAJOR ADD" in the transaction timeline
- **Detection:** If shares increased by exactly 2x, 3x, 4x, 5x, 10x, or 20x between quarters, check if a split occurred
- **Handling:** Note potential splits in the analysis. Cross-reference with Yahoo Finance historical data if available.

### 10. Confidential Treatment
- Filers can request confidential treatment to hide specific positions temporarily
- These positions appear in later amendments but not in the original filing
- **Handling:** Note in the report that 13F data may be incomplete due to confidential treatment. Prefer amended filings.

### 11. SEC EDGAR Rate Limiting
- 10 requests/second maximum per IP
- Missing User-Agent header → 403 Forbidden
- Large submissions JSON (filers with 100+ quarterly filings) may timeout
- **Handling:** Always include User-Agent header. Add 150-200ms delay between requests. Use curl for large JSON (more reliable than urllib for large responses). Implement retry with backoff.

### 12. Issuer Name Inconsistency
- The same company may have different `nameOfIssuer` values across filings
- Example: "BK OF AMERICA CORP" vs "BANK OF AMERICA CORP"
- **Handling:** Always match by CUSIP, never by name. Use a canonical name mapping for display.

## Common Mistakes

- **Comparing by name not CUSIP** — issuer names vary between filings, CUSIP is the stable key
- **Ignoring share class** — same company may have CL A and CL B as separate entries
- **Not accounting for stock splits** — share count jumps without actual buying
- **Treating value changes as trades** — value changes from price movement, only share changes indicate trading
- **Assuming current quarter = latest filing** — check reportDate, not filingDate
