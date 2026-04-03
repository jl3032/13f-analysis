# 13F 基金经理数据库（中文友好版）

这个版本面向中文用户，优先收录中文投资圈更熟悉、讨论度更高的基金经理，同时保留一些全球范围内有代表性的海外机构投资人。

## 快速菜单

当用户输入比较模糊（例如只说“13F”“持仓”“看看有哪些大佬”）时，可以先展示下面的菜单：

```
13F 机构持仓分析：你想看谁？

  中文投资圈高关注
    1. 段永平 / Himalaya Capital
    2. 李录 / Himalaya Capital Partners
    3. 高瓴 / HHLR Advisors
    4. 巴菲特 / Berkshire Hathaway

  海外价值投资
    5. Bill Ackman / Pershing Square
    6. Seth Klarman / Baupost
    7. David Einhorn / Greenlight
    8. Mohnish Pabrai / Pabrai Funds

  宏观 / 事件驱动
    9. Stanley Druckenmiller / Duquesne
    10. David Tepper / Appaloosa
    11. Ray Dalio / Bridgewater
    12. Dan Loeb / Third Point

  成长 / 科技
    13. Cathie Wood / ARK
    14. Chase Coleman / Tiger Global
    15. Philippe Laffont / Coatue
    16. Terry Smith / Fundsmith

  稳健复利 / 特色机构
    17. Tom Gayner / Markel
    18. Michael Burry / Scion
    19. Joel Greenblatt / Gotham
    20. Howard Marks / Oaktree

也可以直接说名字、CIK，或者说“对比段永平和巴菲特”“谁持有TSLA”
```

## 预置基金经理

| # | 基金经理 | 常见别名 | 申报实体 | CIK | 风格 | 13F 参考价值 | 备注 |
|---|---------|----------|----------|-----|------|--------------|------|
| 1 | 段永平 | Duan Yongping, Himalaya, 步步高 | Himalaya Capital Management LLC | 0001709323 | 极致集中、长期价值 | HIGH | 中文投资圈最常被跟踪的 13F 之一 |
| 2 | 李录 | Li Lu, Himalaya Partners | Himalaya Capital Partners LLC | 0001709324 | 集中价值、深度研究 | HIGH | 芒格高度认可，中文用户熟悉度高 |
| 3 | 高瓴 | Hillhouse, HHLR, 张磊, Zhang Lei | HHLR ADVISORS LTD | 0001510455 | 成长 + 中国相关 | MEDIUM | 中文用户关注度高，但换手和结构复杂度更高 |
| 4 | 巴菲特 | Warren Buffett, Berkshire, 伯克希尔 | BERKSHIRE HATHAWAY INC | 0001067983 | 长期价值、集中 | HIGH | 全球认知度最高 |
| 5 | Bill Ackman | Ackman, Pershing, 阿克曼 | Pershing Square Capital Management, L.P. | 0001336528 | 激进投资、集中 | HIGH | 公开表达多，适合散户跟踪 |
| 6 | Seth Klarman | Klarman, Baupost, 克拉曼 | BAUPOST GROUP LLC/MA | 0001061768 | 深度价值、逆向 | HIGH | 神秘低调，持仓变化常有研究价值 |
| 7 | David Einhorn | Einhorn, Greenlight, 艾因霍恩 | GREENLIGHT CAPITAL INC | 0001079114 | 价值 + 事件驱动 | HIGH | 新仓/减仓通常有明确逻辑 |
| 8 | Mohnish Pabrai | Pabrai, 帕布莱 | Pabrai Investment Funds | 0001173334 | 极度集中、深度价值 | HIGH | 持仓数少，信号很强 |
| 9 | Stanley Druckenmiller | Druckenmiller, Duquesne, 德鲁肯米勒 | Duquesne Family Office LLC | 0001536411 | 宏观 + 集中股票 | MEDIUM | 方向感强，但季度波动大 |
| 10 | David Tepper | Tepper, Appaloosa | APPALOOSA MANAGEMENT LP | 0001006438 | 事件驱动、困境反转 | MEDIUM | 风格鲜明，适合看大方向 |
| 11 | Ray Dalio | Dalio, Bridgewater, 桥水 | Bridgewater Associates, LP | 0001350694 | 宏观、系统化 | LOW | 13F 只能看到很有限的一部分 |
| 12 | Dan Loeb | Loeb, Third Point | Third Point LLC | 0001040273 | 激进、事件驱动 | MEDIUM | 常见快速调整 |
| 13 | Cathie Wood | Wood, ARK, 木头姐 | ARK Investment Management LLC | 0001697748 | 成长、创新主题 | LOW | 每日披露比季度 13F 更重要 |
| 14 | Chase Coleman | Coleman, Tiger Global | Tiger Global Management LLC | 0001167483 | 科技成长 | MEDIUM | 更适合看持仓方向而非精确时点 |
| 15 | Philippe Laffont | Laffont, Coatue | Coatue Management LLC | 0001535392 | 科技对冲 | MEDIUM | 技术成长风格明显 |
| 16 | Terry Smith | Smith, Fundsmith | Fundsmith LLP | 0001569205 | 高质量复利 | HIGH | 低换手、长期持有 |
| 17 | Tom Gayner | Gayner, Markel | MARKEL GROUP INC. | 0001096343 | 保险浮存金、长期质量 | HIGH | 常被看作“迷你伯克希尔” |
| 18 | Michael Burry | Burry, Scion, 大空头 | Scion Asset Management, LLC | 0001649339 | 逆向、深度价值 | HIGH | 变动大，但关注度极高 |
| 19 | Joel Greenblatt | Greenblatt, Gotham, 格林布拉特 | Gotham Asset Management, LLC | 0001510387 | 量化价值 | LOW | 信号较弱，更适合背景研究 |
| 20 | Howard Marks | Marks, Oaktree, 霍华德马克斯 | Oaktree Capital Management LP | 0001491956 | 困境债务、特殊机会 | MEDIUM | 股票 13F 不是其全貌 |

## 13F 参考价值说明

| 评级 | 含义 | 适合谁 |
|------|------|--------|
| HIGH | 持仓稳定、仓位少、每次变化都值得看 | 段永平、李录、巴菲特、Ackman、Klarman、Pabrai |
| MEDIUM | 有参考价值，但季度内或跨季度变化较大 | 高瓴、Druckenmiller、Tepper、Tiger、Coatue |
| LOW | 13F 只能看到部分信息，或者换手太高 | ARK、Bridgewater、Gotham |

## 中文用户高关注人物简述

### 段永平 / Himalaya Capital
- 风格：极致集中、长期持有、商业理解优先
- 适合看什么：新建仓、清仓、核心持仓是否变化
- 中文用户为什么爱看：讨论热度高，仓位少，信号强

### 李录 / Himalaya Capital Partners
- 风格：集中价值、研究驱动
- 适合看什么：核心持仓的长期变化、和段永平的交集
- 中文用户为什么爱看：芒格加持，风格稳定

### 高瓴 / HHLR
- 风格：成长投资、中国相关、跨市场
- 适合看什么：中概、消费、医药、科技方向变化
- 注意：13F 不能代表高瓴全部持仓结构

### 巴菲特 / Berkshire Hathaway
- 风格：长期价值、超大规模集中配置
- 适合看什么：新进持仓、减持苹果、金融股变化
- 注意：13F 不包含伯克希尔大量非上市或完全控股业务

## 海外代表人物简述

### Bill Ackman / Pershing Square
- 风格：集中持仓、激进投资、公开表达
- 散户价值：持仓少，逻辑通常清楚，容易跟踪

### Seth Klarman / Baupost
- 风格：深度价值、逆向、低调
- 散户价值：新仓和大调整往往很值得研究

### Stanley Druckenmiller / Duquesne
- 风格：宏观框架下的集中股票下注
- 散户价值：更适合看方向，不适合机械跟单

### Cathie Wood / ARK
- 风格：高成长、创新主题、高换手
- 散户价值：更适合结合每日持仓披露一起看，单看 13F 不够

## 未收录人物的查找方式

如果用户提到的人不在这份中文数据库里：

1. 先到 `filers-database.md` 查英文版预置人物
2. 再去 SEC EDGAR 搜索：

```text
https://efts.sec.gov/LATEST/search-index?q={name}&forms=13F-HR
```

3. 或使用公司检索页：

```text
https://www.sec.gov/cgi-bin/browse-edgar?company={name}&CIK=&type=13F&owner=include&count=40&action=getcompany
```

4. 找到后再用 submissions JSON 验证 CIK：

```text
https://data.sec.gov/submissions/CIK{zero_padded_cik}.json
```

