# 13F Institutional Holdings Analysis

A Claude Code skill that analyzes SEC 13F filings to track what major institutional investors are buying, selling, and holding. Fetches raw data from SEC EDGAR, parses holdings across all historical quarters, and produces interactive HTML reports with deep analysis.

## What It Does

Tell Claude Code about a fund manager, and it generates a comprehensive single-file HTML report:

- **Quarterly Changes** — New positions, eliminations, share count changes
- **All Holdings** — Sortable table with Yahoo Finance links
- **Sector Analysis** — Donut chart + sector rotation trends
- **Stock Lifecycle** — Every stock ever held, with lifecycle bars, classification (Core/Medium/Short-lived), and transaction timeline
- **Portfolio Evolution** — SVG charts: AUM over time, concentration trends, stacked composition
- **Style Analysis** — Radar chart + quantitative metrics (turnover, holding period, conviction)
- **Quarter Browser** — Browse any historical quarter with diff vs previous
- **Manager Profile** — Background, investment style, famous trades

All in a single self-contained HTML file. No dependencies. Dark theme. Works offline.

## Quick Start

### Install

```bash
git clone https://github.com/jl3032/13f-analysis.git ~/.claude/skills/13f-analysis
cd ~/.claude/skills/13f-analysis && ./setup
```

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- Python 3.6+
- curl
- Internet access (SEC EDGAR API)

### Usage

In Claude Code, just ask:

```
"分析段永平的13F持仓"
"What is Buffett buying this quarter?"
"Compare Ackman and Einhorn holdings"
"Show me Druckenmiller's portfolio evolution"
```

The skill triggers on keywords: `13F`, `持仓`, `holdings`, fund manager names, or institutional investment analysis requests.

## Report Features

### 8 Interactive Tabs

| Tab | Description |
|-----|-------------|
| Quarterly Changes | Q-o-Q diff: new, eliminated, changed positions |
| All Holdings | Sortable table with weight bars, search/filter |
| Sector View | CSS donut chart + sector rotation table |
| Transaction History | Full lifecycle of every stock ever held |
| Portfolio Evolution | SVG time-series charts (AUM, concentration, composition) |
| Style Analysis | Radar chart + quantitative style metrics |
| Quarter Browser | Browse any historical quarter interactively |
| Manager Profile | Background, style, famous trades |

### Key Technical Features

- **Single-file HTML** — all CSS/JS inline, zero external dependencies
- **Dark theme** — professional financial aesthetic
- **Pure SVG charts** — no Chart.js or D3 needed
- **Sortable tables** — click any column header
- **Yahoo Finance links** — every stock name links to its Yahoo Finance page
- **Responsive** — works on desktop and mobile
- **Bilingual** — English + Chinese labels throughout
- **Lazy rendering** — charts only render when their tab is activated

## Data Source

All data comes directly from [SEC EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch), the official source for 13F filings. No third-party data providers needed.

### How 13F Works

- US institutions managing >$100M must file quarterly
- Filed within 45 days of quarter-end (e.g., Q4 data available by mid-February)
- Shows long equity positions only (no shorts, options, futures)
- Subject to confidential treatment requests (some positions may be hidden)

## Pre-configured Fund Managers

| Manager | Entity | CIK | Style |
|---------|--------|-----|-------|
| Warren Buffett | Berkshire Hathaway | 0001067983 | Long-term concentrated value |
| 段永平 (Duan Yongping) | Himalaya Capital | 0001709323 | Ultra-concentrated value |
| Bill Ackman | Pershing Square | 0001336528 | Activist concentrated |
| Ray Dalio | Bridgewater Associates | 0001350694 | Macro diversified |
| Stanley Druckenmiller | Duquesne Family Office | 0001536411 | Macro concentrated |
| Seth Klarman | Baupost Group | 0001061768 | Deep value contrarian |
| David Einhorn | Greenlight Capital | 0001079114 | Value + short-selling |
| Cathie Wood | ARK Invest | 0001697748 | Growth disruptive |
| Tom Gayner | Markel Group | 0001096343 | Long-term quality |
| Terry Smith | Fundsmith | 0001569205 | Long-term quality growth |
| Joel Greenblatt | Gotham Asset | 0001510387 | Quantitative value |
| David Tepper | Appaloosa Management | 0001006438 | Event-driven distressed |

Any 13F filer can be analyzed — just provide the name or CIK number.

## Analysis Modes

### Mode 1: Fund Deep Dive (Single Manager)
Full historical analysis with all 8 tabs. Fetches all available quarters.

### Mode 2: Cross-Fund Comparison
Side-by-side comparison of multiple managers: consensus holdings, consensus moves, sector comparison.

### Mode 3: Stock Ownership Timeline
Track a single stock across multiple institutions over time.

## Testing

Run the test suite to verify the pipeline works end-to-end:

```bash
# Quick smoke test (2 managers, ~30 seconds)
python3 tests/test_pipeline.py --quick

# Full test suite (7 managers, ~2 minutes)
python3 tests/test_pipeline.py
```

The test suite validates:
- SEC EDGAR API connectivity and data fetching
- XML parsing across different filing formats
- Value scale detection (thousands vs full dollars)
- Quarter-to-quarter diff logic
- Cross-reference against SEC cover page totals

Tested against: Himalaya Capital, Pershing Square, Greenlight Capital, Duquesne, Baupost Group, Markel Group, ARK Invest.

## Known Edge Cases

See [SKILL.md](SKILL.md#edge-cases--known-issues) for comprehensive documentation of all edge cases, including:

- Value scale differences (pre-2024 vs post-2024 filings)
- CIK changes when filing agents change
- Missing quarters for some filers
- Large portfolios (100+ positions)
- Stock splits affecting share counts
- XML namespace variations across filings

## File Structure

```
13f-analysis/
  SKILL.md              # Main skill definition (Claude reads this)
  edgar-api-reference.md # SEC EDGAR API documentation
  filers-database.md     # Pre-configured fund managers
  report-template.html   # HTML report template with CSS/JS patterns
  setup                  # Installation script
  LICENSE                # MIT
  README.md              # This file
  tests/
    test_pipeline.py     # End-to-end test suite
  examples/
    (sample reports)
```

## Limitations

1. **45-day lag** — 13F data reflects quarter-end, filed 45 days later
2. **Long positions only** — no shorts, options, futures, or derivatives
3. **Confidential treatment** — some positions may be hidden temporarily
4. **Snapshot only** — high-turnover funds may change positions within the quarter
5. **US equities only** — foreign-only positions may not appear
6. **SEC rate limits** — 10 requests/second; bulk analysis may take time

## License

MIT License. See [LICENSE](LICENSE).

## Credits

Data source: [SEC EDGAR](https://www.sec.gov/). Stock links: [Yahoo Finance](https://finance.yahoo.com/).

Built as a Claude Code skill. Works with Claude Opus, Sonnet, and Haiku.
