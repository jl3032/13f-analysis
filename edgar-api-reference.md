# SEC EDGAR API Reference for 13F Analysis

## Authentication

- **No API key required** — all endpoints are public
- **User-Agent header MANDATORY**: `User-Agent: 13F-Analysis research@example.com`
- **Rate limit**: 10 requests/second per IP. Missing User-Agent → 403.

## Core Endpoints

### 1. CIK Lookup

**Bulk company list (recommended for startup):**
```
GET https://www.sec.gov/files/company_tickers.json
```
Returns: `{"0": {"cik_str": 1045810, "ticker": "NVDA", "title": "NVIDIA CORP"}, ...}`

**With exchange:**
```
GET https://www.sec.gov/files/company_tickers_exchange.json
```

### 2. Filer Submissions (Filing List)

```
GET https://data.sec.gov/submissions/CIK{zero-padded-10-digits}.json
```
Example: `https://data.sec.gov/submissions/CIK0001067983.json`

**Response structure:**
```json
{
  "cik": "1067983",
  "entityType": "operating",
  "name": "BERKSHIRE HATHAWAY INC",
  "filings": {
    "recent": {
      "form": ["13F-HR", "10-K", ...],
      "accessionNumber": ["0000950123-24-011775", ...],
      "filingDate": ["2024-11-14", ...],
      "reportDate": ["2024-09-30", ...],
      "primaryDocument": ["xslForm13F_X02/primary_doc.xml", ...]
    },
    "files": [
      {"name": "CIK0001067983-submissions-001.json", ...}
    ]
  }
}
```

**Filter for 13F:** `filings.recent.form[] == "13F-HR"` or `"13F-HR/A"`
**Quarter mapping:** `reportDate` = quarter-end date (e.g., "2024-09-30" = Q3 2024)
**Older filings:** Fetch from `filings.files[].name` URLs

### 3. Filing Index (Find Information Table Filename)

```
GET https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dashes}/
```

The accession number `0000950123-24-011775` becomes path `000095012324011775` (remove dashes).

Look for the document with type `INFORMATION TABLE` — this is the holdings XML file.

**Alternative:** Fetch the index JSON:
```
GET https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dashes}/index.json
```

### 4. Holdings Data (Information Table XML)

```
GET https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no_dashes}/{info_table_filename}.xml
```

**XML namespace:** `http://www.sec.gov/edgar/document/thirteenf/informationtable`

**Each `<infoTable>` entry:**
```xml
<infoTable>
  <nameOfIssuer>APPLE INC</nameOfIssuer>
  <titleOfClass>COM</titleOfClass>
  <cusip>037833100</cusip>
  <value>8090692000</value>
  <shrsOrPrnAmt>
    <sshPrnamt>34724000</sshPrnamt>
    <sshPrnamtType>SH</sshPrnamtType>
  </shrsOrPrnAmt>
  <putCall/>
  <investmentDiscretion>DFND</investmentDiscretion>
  <votingAuthority>
    <Sole>34724000</Sole>
    <Shared>0</Shared>
    <None>0</None>
  </votingAuthority>
</infoTable>
```

### 5. Cover Page (Portfolio Summary)

The `primary_doc.xml` contains summary data:
```xml
<summaryPage>
  <tableEntryTotal>121</tableEntryTotal>
  <tableValueTotal>266378900503</tableValueTotal>
</summaryPage>
```
`tableValueTotal` is in **thousands of USD** in the cover page but `value` in the info table is in **full USD**.

**IMPORTANT:** In some filings, the `<value>` field in the information table is in **thousands** (older format) vs **full dollars** (newer format). Cross-check against `tableValueTotal` from cover page to determine which scale is used.

## Field Reference

| Field | Description | Notes |
|-------|-------------|-------|
| `nameOfIssuer` | Company name | May vary between filings |
| `titleOfClass` | Security class | COM, CL A, CL B, etc. |
| `cusip` | 9-char CUSIP | **Use this as primary key for matching** |
| `value` | Market value | Check if thousands or full dollars |
| `sshPrnamt` | Share count or principal | Number |
| `sshPrnamtType` | SH (shares) or PRN (principal) | |
| `putCall` | PUT, CALL, or empty | Options indicator |
| `investmentDiscretion` | SOLE, DFND, OTR | |
| `Sole/Shared/None` | Voting authority | Share counts |

## Bulk Data Sets (Recommended for Multi-Quarter Analysis)

```
https://www.sec.gov/files/structureddata/data/form-13f-data-sets/
```

Each quarter has a ZIP containing TSV files:

| File | Use |
|------|-----|
| `SUBMISSION.tsv` | Filing metadata, accession numbers |
| `COVERPAGE.tsv` | Filer info, match CIK to accession |
| `INFOTABLE.tsv` | **All holdings for all filers** |
| `SUMMARYPAGE.tsv` | Portfolio totals |

**INFOTABLE.tsv columns:**
`ACCESSION_NUMBER | INFOTABLE_SK | NAMEOFISSUER | TITLEOFCLASS | CUSIP | FIGI | VALUE | SSHPRNAMT | SSHPRNAMTTYPE | PUTCALL | INVESTMENTDISCRETION | OTHERMANAGER | VOTING_AUTH_SOLE | VOTING_AUTH_SHARED | VOTING_AUTH_NONE`

**Workflow for bulk:**
1. Download ZIP for target quarter
2. In COVERPAGE.tsv, find rows where CIK matches target filer → get ACCESSION_NUMBER
3. In INFOTABLE.tsv, filter by that ACCESSION_NUMBER → all holdings

## Quarter Reference

| Quarter | Report Date | Filing Deadline | Data Set Period |
|---------|-------------|-----------------|-----------------|
| Q1 | Mar 31 | May 15 | ~Apr-Jun release |
| Q2 | Jun 30 | Aug 14 | ~Jul-Sep release |
| Q3 | Sep 30 | Nov 14 | ~Oct-Dec release |
| Q4 | Dec 31 | Feb 14 | ~Jan-Mar release |

## Common Pitfalls

1. **Accession number format**: API path uses no dashes (`000095012324011775`), but JSON data includes dashes (`0000950123-24-011775`)
2. **Value scale**: Always verify if values are in thousands or full dollars
3. **Amended filings**: `13F-HR/A` supersedes the original `13F-HR` for the same quarter — always prefer the amendment
4. **Multiple entries per stock**: Same CUSIP may appear multiple times if managed by different sub-advisors. Aggregate by CUSIP for total position.
5. **Rate limiting**: Add 100ms+ delay between requests. Batch with bulk data sets when possible.
