# 13F Institutional Holdings Analysis

[中文文档 / Chinese Documentation](README_CN.md)

AI-powered analysis of SEC 13F filings -- track what Burry, Cathie Wood, Ackman, Buffett and other top investors are buying and selling. Generates interactive HTML reports with portfolio evolution charts, style analysis, and cross-fund consensus.

**Works with any AI coding tool:** Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Aider, and more.

## What It Does

Ask your AI about a fund manager, and it generates a comprehensive single-file HTML report:

- **Quarterly Changes** -- New positions, eliminations, share count changes
- **All Holdings** -- Sortable table with Yahoo Finance links
- **Sector Analysis** -- Donut chart + sector rotation trends
- **Stock Lifecycle** -- Every stock ever held, with lifecycle bars and classification
- **Portfolio Evolution** -- SVG charts: AUM over time, concentration, composition
- **Style Analysis** -- Radar chart + quantitative metrics
- **Quarter Browser** -- Browse any historical quarter interactively
- **Manager Profile** -- Background, investment style, famous trades

Single self-contained HTML file. No dependencies. Dark/light theme toggle. Works offline.

## Quick Start

### Install

```bash
git clone https://github.com/jl3032/13f-analysis.git
cd 13f-analysis && ./setup
```

### Requirements

- Any AI coding assistant (see Platform Setup below)
- Python 3.6+
- curl
- Internet access (SEC EDGAR API, free, no API key needed)
- A real contact email for SEC `User-Agent` headers (`SEC_USER_AGENT_EMAIL`)

### Usage

Just ask in natural language:

```
"Analyze Buffett's 13F holdings"
"What is Ackman buying this quarter?"
"Compare Buffett and Klarman holdings"
"Who owns TSLA?" (reverse stock lookup)
"Find me concentrated value investors" (discovery mode)
```

### SEC User-Agent Setup

SEC EDGAR requests should include a descriptive `User-Agent` with a real contact email you control.

```bash
export SEC_USER_AGENT_EMAIL="your-real-email@example.com"
```

Do not leave placeholder addresses such as `example.com` in real requests.

## Platform Setup

### Claude Code

```bash
git clone https://github.com/jl3032/13f-analysis.git ~/.claude/skills/13f-analysis
cd ~/.claude/skills/13f-analysis && ./setup
```

The skill auto-triggers on keywords: `13F`, `holdings`, fund manager names.

### Cursor

Add to your `.cursor/rules` or project rules:

```
Read the file 13f-analysis/SKILL.md and follow its instructions for analyzing SEC 13F institutional holdings.
Reference files: 13f-analysis/edgar-api-reference.md, 13f-analysis/filers-database.md
```

### Windsurf (Codeium)

Add to `.windsurfrules` in your project root:

```
For 13F institutional holdings analysis, follow the instructions in 13f-analysis/SKILL.md.
Reference: 13f-analysis/edgar-api-reference.md and 13f-analysis/filers-database.md
```

### GitHub Copilot

Add to `.github/copilot-instructions.md`:

```
When the user asks about 13F filings, institutional holdings, or fund manager portfolios,
follow the instructions in 13f-analysis/SKILL.md to fetch data from SEC EDGAR and generate
interactive HTML reports.
```

### Gemini CLI

Add to `GEMINI.md` in your project:

```
For 13F analysis tasks, read and follow 13f-analysis/SKILL.md.
Data source docs: 13f-analysis/edgar-api-reference.md
Known filers: 13f-analysis/filers-database.md
```

### Aider / Other CLI Tools

Point the AI to the instruction file:

```
Read 13f-analysis/SKILL.md for complete instructions on how to analyze SEC 13F filings.
```

### Generic (Any AI)

The core of this tool is `SKILL.md` -- a detailed instruction document that tells any AI how to:
1. Fetch 13F data from SEC EDGAR (free public API)
2. Parse holdings XML
3. Compare across quarters
4. Generate interactive HTML reports

Copy the contents of `SKILL.md` into your AI tool's system prompt or custom instructions.

## Report Features

### 8 Interactive Tabs

| Tab | Description |
|-----|-------------|
| Quarterly Changes | Quarter-over-quarter diff: new, eliminated, changed positions |
| All Holdings | Sortable table with weight bars, search/filter |
| Sector View | CSS donut chart + sector rotation table |
| Transaction History | Full lifecycle of every stock ever held |
| Portfolio Evolution | SVG time-series charts (AUM, concentration, composition) |
| Style Analysis | Radar chart + quantitative style metrics |
| Quarter Browser | Browse any historical quarter interactively |
| Manager Profile | Background, style, famous trades |

### Key Features

- **Single-file HTML** -- all CSS/JS inline, zero external dependencies
- **Dark/light theme** -- toggle button, preference saved via localStorage
- **Pure SVG charts** -- no Chart.js or D3 needed
- **Yahoo Finance links** -- every stock links to its quote page
- **Bilingual** -- English + Chinese labels throughout
- **Responsive** -- works on desktop and mobile

## Data Source

All data from [SEC EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch) -- the official, free, public source for 13F filings. **No API key needed.** No third-party data providers.

## Pre-configured Fund Managers (20)

| Category | Managers |
|----------|----------|
| Trending | Michael Burry, Cathie Wood/ARK, Bill Ackman |
| Deep Value | Warren Buffett, Seth Klarman, Mohnish Pabrai, David Einhorn |
| Macro | Stanley Druckenmiller, David Tepper |
| Growth | Chase Coleman/Tiger Global, Philippe Laffont/Coatue |
| Compounders | Tom Gayner/Markel, Terry Smith/Fundsmith |

Any 13F filer can be analyzed -- just provide the name or CIK number.

## Analysis Modes

| Mode | Trigger | Output |
|------|---------|--------|
| **Fund Deep Dive** | "Analyze Buffett" | Full 8-tab HTML report |
| **Cross-Fund Compare** | "Compare Buffett and Ackman" | Consensus holdings matrix |
| **Stock Reverse Lookup** | "Who owns TSLA" | Which managers hold a stock |
| **Watchlist Consensus** | "What are the top picks" | Consensus across your watchlist |
| **Discovery** | "Find tech-heavy managers" | AI recommends managers by criteria |

## Testing

```bash
# Quick smoke test (2 managers, ~30 seconds)
python3 tests/test_pipeline.py --quick

# Full test suite (7 managers, ~2 minutes)
python3 tests/test_pipeline.py
```

Validates: EDGAR API fetch, XML parse, value scale detection, quarter diff logic, SEC cover page cross-reference. Tested against 7 fund managers.

## File Structure

```
13f-analysis/
  SKILL.md                 # Core instructions (works with any AI)
  edgar-api-reference.md   # SEC EDGAR API documentation
  filers-database.md       # 20 pre-configured fund managers
  report-template.html     # HTML report template
  setup                    # Installation script
  LICENSE                  # MIT
  README.md                # English documentation
  README_CN.md             # Chinese documentation
  tests/
    test_pipeline.py       # End-to-end test suite
```

## Disclaimer

**This tool is for informational and educational purposes only. It is NOT investment advice.**

- 13F data is backward-looking (45-day lag) and may not reflect current positions
- Past holdings do not predict future performance
- The authors are not licensed financial advisors
- Always do your own research before making investment decisions
- Use at your own risk -- see MIT License "AS IS" clause

## Limitations

1. **45-day lag** -- 13F reflects quarter-end, filed ~45 days later
2. **Long positions only** -- no shorts, options, futures, derivatives
3. **Confidential treatment** -- some positions may be temporarily hidden
4. **Snapshot only** -- high-turnover funds may change within the quarter
5. **US equities focus** -- foreign-only positions may not appear

## License

MIT License. See [LICENSE](LICENSE).

## Credits

Data: [SEC EDGAR](https://www.sec.gov/) (free public API). Stock links: [Yahoo Finance](https://finance.yahoo.com/).
