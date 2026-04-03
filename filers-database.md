# Known 13F Filers Database

## Quick Menu

When the user's input is vague (just "13F", "holdings", etc.), show this menu and adapt the wording to the user's language.

**Default menu:**

```text
13F Institutional Holdings Analysis

  What would you like to do?

  A) Browse recommended fund managers
  B) Compare two or more managers
  C) Look up a stock (e.g. "Who owns TSLA")
  D) Search by style (e.g. "concentrated value investors")
  E) View or edit my watchlist

  Or just type a fund manager name to get started.
```

When the user picks A, expand the recommended list:

```text
  Trending
    1. Michael Burry (Scion) -- The Big Short contrarian
    2. Cathie Wood (ARK Invest) -- Disruptive innovation
    3. Bill Ackman (Pershing Square) -- Activist, active on X
    4. Warren Buffett (Berkshire Hathaway) -- The Oracle of Omaha

  Value & Deep Value
    5. Duan Yongping (Himalaya Capital) -- Ultra-concentrated, long-term
    6. Seth Klarman (Baupost) -- Ultra-private deep value
    7. Li Lu (Himalaya Capital Partners) -- Munger-backed concentrated investor

  Macro
    8. Stanley Druckenmiller (Duquesne) -- Macro legend
    9. David Tepper (Appaloosa) -- Event-driven

  Growth
    10. Hillhouse / HHLR -- China-related growth investor
    11. Chase Coleman (Tiger Global) -- Tech growth

  Compounders
    12. Tom Gayner (Markel) -- Mini-Berkshire
    13. Terry Smith (Fundsmith) -- Quality growth

  Pick a number, or type any name.
```

## Pre-mapped Filers

| # | Manager | Aliases | Filing Entity | CIK | Style | 13F Value | AUM Est. |
|---|---------|---------|--------------|-----|-------|-----------|----------|
| 1 | Duan Yongping | Yongping, Himalaya | Himalaya Capital Management LLC | 0001709323 | Long-term concentrated value | HIGH | ~$3.5B |
| 2 | Warren Buffett | Buffett, Berkshire Hathaway | BERKSHIRE HATHAWAY INC | 0001067983 | Long-term concentrated value | HIGH | ~$300B+ |
| 3 | Li Lu | Himalaya Partners | Himalaya Capital Partners LLC | 0001709324 | Long-term concentrated value | HIGH | ~$3B |
| 4 | Hillhouse Capital | HHLR, Zhang Lei | HHLR ADVISORS LTD | 0001510455 | Growth + PE crossover | MEDIUM | ~$20B |
| 5 | Bill Ackman | Ackman, Pershing | Pershing Square Capital Management, L.P. | 0001336528 | Activist concentrated | HIGH | ~$15B |
| 6 | Stanley Druckenmiller | Druckenmiller, Duquesne | Duquesne Family Office LLC | 0001536411 | Macro concentrated | MEDIUM | ~$3B |
| 7 | Seth Klarman | Klarman, Baupost | BAUPOST GROUP LLC/MA | 0001061768 | Deep value contrarian | HIGH | ~$25B |
| 8 | David Einhorn | Einhorn, Greenlight | GREENLIGHT CAPITAL INC | 0001079114 | Value + activist | HIGH | ~$3B |
| 9 | Cathie Wood | Wood, ARK | ARK Investment Management LLC | 0001697748 | Growth disruptive innovation | LOW | ~$15B |
| 10 | Chase Coleman | Coleman, Tiger Global | Tiger Global Management LLC | 0001167483 | Tech growth | MEDIUM | ~$30B |
| 11 | Philippe Laffont | Laffont, Coatue | Coatue Management LLC | 0001535392 | Tech hedge | MEDIUM | ~$15B |
| 12 | Tom Gayner | Gayner, Markel | MARKEL GROUP INC. | 0001096343 | Long-term quality | HIGH | ~$12B |
| 13 | Terry Smith | Smith, Fundsmith | Fundsmith LLP | 0001569205 | Long-term quality growth | HIGH | ~$25B |
| 14 | Joel Greenblatt | Greenblatt, Gotham | Gotham Asset Management, LLC | 0001510387 | Quantitative value | LOW | ~$10B |
| 15 | Ray Dalio | Dalio, Bridgewater | Bridgewater Associates, LP | 0001350694 | Macro systematic | LOW | ~$100B+ |
| 16 | David Tepper | Tepper, Appaloosa | APPALOOSA MANAGEMENT LP | 0001006438 | Event-driven distressed | MEDIUM | ~$6B |
| 17 | Michael Burry | Burry, Scion | Scion Asset Management, LLC | 0001649339 | Contrarian value | HIGH | ~$300M |
| 18 | Dan Loeb | Loeb, Third Point | Third Point LLC | 0001040273 | Activist event-driven | MEDIUM | ~$12B |
| 19 | Howard Marks | Marks, Oaktree | Oaktree Capital Management LP | 0001491956 | Distressed debt | MEDIUM | ~$170B |
| 20 | Mohnish Pabrai | Pabrai | Pabrai Investment Funds | 0001173334 | Concentrated deep value | HIGH | ~$500M |

## 13F Reference Value Guide

| 13F Value | Meaning | Who |
|-----------|---------|-----|
| **HIGH** | Stable holdings, concentrated portfolios, changes usually matter | Duan Yongping, Buffett, Ackman, Klarman, Burry |
| **MEDIUM** | Useful directionally, but turnover is higher | Druckenmiller, Tiger, Tepper, Hillhouse |
| **LOW** | Quarterly 13F snapshot has limited value | ARK, Bridgewater, Gotham |

## Manager Profiles (Brief)

### Duan Yongping — Himalaya Capital
- **Background:** Chinese entrepreneur turned long-term concentrated investor
- **Famous trades:** Apple, NetEase, Google / Alphabet
- **Style:** Ultra-concentrated, business-quality-first value investing
- **13F note:** Very few positions, high conviction, any change is significant

### Warren Buffett — Berkshire Hathaway
- **Background:** The best-known long-term value investor globally
- **Famous trades:** Coca-Cola, Apple, Bank of America
- **Style:** Buy-and-hold, concentrated at very large scale
- **13F note:** Very stable portfolio; new positions are usually major news

### Li Lu — Himalaya Capital Partners
- **Background:** Munger-backed investor known for concentrated research-driven investing
- **Style:** Deep research, concentrated value, cross-border perspective
- **13F note:** Small number of positions; overlap with Duan Yongping is often worth tracking

### Michael Burry — Scion Asset Management
- **Background:** Best known for the 2008 subprime short
- **Famous trades:** The Big Short, GameStop-related positioning, contrarian sector calls
- **Style:** Contrarian deep value, often high turnover
- **13F note:** Changes frequently, but new positions can still be highly informative

### Bill Ackman — Pershing Square
- **Famous trades:** Chipotle turnaround, Herbalife short, Netflix, Universal Music
- **Style:** Concentrated activist, 8-12 positions
- **13F note:** Very few positions, each one matters, public about theses

### Cathie Wood — ARK Invest
- **Famous trades:** Tesla early conviction, Coinbase, genomics
- **Style:** Disruptive innovation, high growth, high turnover
- **13F note:** Daily ARK disclosures are usually more useful than quarterly 13F data

### Stanley Druckenmiller — Duquesne
- **Famous trades:** Soros-era pound short, concentrated tech and macro calls
- **Style:** Macro framework with concentrated equity bets
- **13F note:** Portfolio can change dramatically quarter to quarter

### Seth Klarman — Baupost
- **Famous trades:** Distressed debt, contrarian equity positions
- **Style:** Deep value, highly selective, very private
- **13F note:** New positions are often especially worth studying

### David Einhorn — Greenlight Capital
- **Famous trades:** Lehman short, Allied Capital, gold-related theses
- **Style:** Value plus event-driven and short-selling background
- **13F note:** New positions often come with a strong underlying thesis

### Tom Gayner — Markel
- **Style:** Long-term quality businesses, insurance-float investor, patient allocator
- **13F note:** Very stable; changes are deliberate and meaningful

### Mohnish Pabrai — Pabrai Investment Funds
- **Background:** Highly concentrated value investor influenced by Buffett and Munger
- **Style:** Extremely concentrated deep value
- **13F note:** Very small number of positions, so changes are strong signals

## CIK Lookup for Unknown Filers

If the user provides a name not in this database:

```text
1. Search: https://efts.sec.gov/LATEST/search-index?q={name}&forms=13F-HR
2. Or: https://www.sec.gov/cgi-bin/browse-edgar?company={name}&CIK=&type=13F&owner=include&count=40&action=getcompany
3. Verify CIK by fetching submissions: https://data.sec.gov/submissions/CIK{padded_cik}.json
```
