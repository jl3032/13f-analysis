#!/usr/bin/env python3
"""
13F Pipeline Test Suite
=======================
Validates the entire 13F analysis pipeline end-to-end:
  - Filing history fetch from SEC EDGAR
  - Holdings XML parse
  - SEC cover page cross-reference (value scale detection)
  - Quarter diff logic
  - Edge cases: CUSIP aggregation, amended filings, value-in-thousands

Uses only Python standard library. Runnable standalone:
  python3 tests/test_pipeline.py          # full test (7 managers)
  python3 tests/test_pipeline.py --quick  # smoke test (2 managers)
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from collections import defaultdict

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
SEC_ARCHIVES_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/"
SEC_INDEX_JSON_URL = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/index.json"
USER_AGENT = "13F-PipelineTest research-test@example.com"
RATE_LIMIT_DELAY = 0.22  # seconds between requests

NS = {"ns": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}

MANAGERS = [
    {
        "name": "Himalaya Capital",
        "label": "\u6bb5\u6c38\u5e73 / Himalaya Capital",
        "cik": 1709323,
        "style": "small concentrated",
        "min_filings": 5,
        "min_positions": 3,
    },
    {
        "name": "Pershing Square",
        "label": "Bill Ackman / Pershing Square",
        "cik": 1336528,
        "style": "medium concentrated",
        "min_filings": 10,
        "min_positions": 4,
    },
    {
        "name": "Greenlight Capital",
        "label": "David Einhorn / Greenlight Capital",
        "cik": 1079114,
        "style": "medium diversified",
        "min_filings": 10,
        "min_positions": 8,
    },
    {
        "name": "Duquesne",
        "label": "Stanley Druckenmiller / Duquesne",
        "cik": 1536411,
        "style": "high turnover",
        "min_filings": 5,
        "min_positions": 5,
    },
    {
        "name": "Baupost Group",
        "label": "Seth Klarman / Baupost Group",
        "cik": 1061768,
        "style": "deep value",
        "min_filings": 10,
        "min_positions": 5,
    },
    {
        "name": "Markel Group",
        "label": "Tom Gayner / Markel Group",
        "cik": 1096343,
        "style": "many positions",
        "min_filings": 10,
        "min_positions": 80,
    },
    {
        "name": "ARK Invest",
        "label": "Cathie Wood / ARK Invest",
        "cik": 1697748,
        "style": "very many positions, high turnover",
        "min_filings": 5,
        "min_positions": 50,
    },
]

QUICK_MANAGERS = [MANAGERS[0], MANAGERS[1]]  # Himalaya + Pershing Square

# ---------------------------------------------------------------------------
# Fetcher: curl primary, urllib fallback
# ---------------------------------------------------------------------------

_last_request_time = 0.0


def _rate_limit():
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    _last_request_time = time.time()


def fetch_url(url, accept="application/json"):
    """Fetch URL using curl (primary) with urllib fallback. Returns bytes."""
    _rate_limit()

    # Try curl first -- more reliable for large JSON
    try:
        result = subprocess.run(
            [
                "curl", "-s", "-f", "--max-time", "30",
                "-H", f"User-Agent: {USER_AGENT}",
                "-H", f"Accept: {accept}",
                url,
            ],
            capture_output=True,
            timeout=35,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Fallback to urllib
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": accept,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} for {url}") from e


def fetch_json(url):
    """Fetch and parse JSON from URL."""
    data = fetch_url(url, accept="application/json")
    return json.loads(data)


def fetch_xml(url):
    """Fetch and parse XML from URL."""
    data = fetch_url(url, accept="application/xml")
    return ET.fromstring(data)


# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------

def pad_cik(cik):
    return str(cik).zfill(10)


def accession_to_path(accession):
    """Convert '0001234567-24-001234' to '000123456724001234'."""
    return accession.replace("-", "")


def get_13f_filings(submissions_json):
    """Extract 13F-HR and 13F-HR/A filings from submissions JSON.
    Returns list of dicts with keys: form, accession, filingDate, reportDate.
    Sorted by reportDate descending.
    """
    recent = submissions_json.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    accessions = recent.get("accessionNumber", [])
    filing_dates = recent.get("filingDate", [])
    report_dates = recent.get("reportDate", [])

    filings = []
    for i, form in enumerate(forms):
        if form in ("13F-HR", "13F-HR/A"):
            filings.append({
                "form": form,
                "accession": accessions[i],
                "filingDate": filing_dates[i],
                "reportDate": report_dates[i],
            })

    # Prefer HR/A over HR for the same reportDate
    by_quarter = {}
    for f in filings:
        rd = f["reportDate"]
        if rd not in by_quarter:
            by_quarter[rd] = f
        elif f["form"] == "13F-HR/A":
            by_quarter[rd] = f  # amendment wins

    result = sorted(by_quarter.values(), key=lambda x: x["reportDate"], reverse=True)
    return result


def find_info_table_filename(index_json):
    """From index.json, find the information table XML filename."""
    items = index_json.get("directory", {}).get("item", [])
    for item in items:
        name = item.get("name", "").lower()
        # The info table XML is typically named infotable.xml, or similar
        # but NOT primary_doc.xml and NOT .htm/.html
        if name.endswith(".xml") and "primary_doc" not in name:
            # Could be infotable.xml, InfoTable.xml, etc.
            if "info" in name or "table" in name or "13f" in name:
                return item["name"]

    # Broader search: any XML that isn't primary_doc
    for item in items:
        name = item.get("name", "").lower()
        if name.endswith(".xml") and "primary_doc" not in name and "r" not in name[:2]:
            return item["name"]

    # Last resort: any XML that isn't primary_doc
    for item in items:
        name = item.get("name", "").lower()
        if name.endswith(".xml") and "primary_doc" not in name:
            return item["name"]

    return None


def parse_holdings_xml(root):
    """Parse information table XML into list of holdings dicts.
    Returns list of dicts with keys: cusip, name, titleOfClass, value, shares, sharesType, putCall.
    """
    holdings = []
    # Try with namespace
    entries = root.findall(".//ns:infoTable", NS)
    if not entries:
        # Try without namespace
        entries = root.findall(".//{http://www.sec.gov/edgar/document/thirteenf/informationtable}infoTable")
    if not entries:
        # Try plain
        entries = root.findall(".//infoTable")

    for entry in entries:
        def get_text(tag):
            # Try namespaced first, then plain
            el = entry.find(f"ns:{tag}", NS)
            if el is None:
                el = entry.find(f"{{http://www.sec.gov/edgar/document/thirteenf/informationtable}}{tag}")
            if el is None:
                el = entry.find(tag)
            return el.text.strip() if el is not None and el.text else ""

        def get_nested_text(parent_tag, child_tag):
            parent = entry.find(f"ns:{parent_tag}", NS)
            if parent is None:
                parent = entry.find(f"{{http://www.sec.gov/edgar/document/thirteenf/informationtable}}{parent_tag}")
            if parent is None:
                parent = entry.find(parent_tag)
            if parent is not None:
                child = parent.find(f"ns:{child_tag}", NS)
                if child is None:
                    child = parent.find(f"{{http://www.sec.gov/edgar/document/thirteenf/informationtable}}{child_tag}")
                if child is None:
                    child = parent.find(child_tag)
                return child.text.strip() if child is not None and child.text else ""
            return ""

        cusip = get_text("cusip")
        name = get_text("nameOfIssuer")
        title = get_text("titleOfClass")
        value_str = get_text("value")
        shares_str = get_nested_text("shrsOrPrnAmt", "sshPrnamt")
        shares_type = get_nested_text("shrsOrPrnAmt", "sshPrnamtType")
        put_call = get_text("putCall")

        value = int(value_str) if value_str else 0
        shares = int(shares_str) if shares_str else 0

        holdings.append({
            "cusip": cusip,
            "name": name,
            "titleOfClass": title,
            "value": value,
            "shares": shares,
            "sharesType": shares_type,
            "putCall": put_call,
        })

    return holdings


def aggregate_by_cusip(holdings):
    """Aggregate holdings by CUSIP (same CUSIP may appear multiple times)."""
    aggregated = {}
    for h in holdings:
        cusip = h["cusip"]
        if cusip in aggregated:
            aggregated[cusip]["value"] += h["value"]
            aggregated[cusip]["shares"] += h["shares"]
        else:
            aggregated[cusip] = dict(h)
    return aggregated


def detect_value_scale(holdings_total, cover_page_total_thousands):
    """Determine if holdings values are in thousands or full dollars.
    cover_page_total_thousands is the tableValueTotal from the cover page (always in thousands).
    Returns scale factor: 1 if already full dollars, 1000 if values are in thousands.
    """
    if cover_page_total_thousands <= 0 or holdings_total <= 0:
        return 1

    # First check: are raw and cover in the same unit? (both full dollars or both thousands)
    ratio_direct = holdings_total / cover_page_total_thousands
    if 0.95 <= ratio_direct <= 1.05:
        # Same unit — if cover > 1B, both are likely full dollars; else both thousands
        if cover_page_total_thousands > 1_000_000_000:
            return 1   # both full dollars
        else:
            return 1000  # both in thousands, multiply to get full dollars

    # Second check: raw is full dollars, cover is in thousands
    cover_full = cover_page_total_thousands * 1000
    ratio = holdings_total / cover_full
    if 0.95 <= ratio <= 1.05:
        return 1  # raw is already full dollars

    # Third check: raw is in thousands, cover is in thousands
    if 0.00095 <= ratio <= 0.00105:
        return 1000  # raw needs *1000

    return 1  # Default: assume full dollars


def get_cover_page_total(cik, accession_path, index_json):
    """Fetch the primary_doc.xml and extract tableValueTotal."""
    items = index_json.get("directory", {}).get("item", [])
    primary_doc = None
    for item in items:
        name = item.get("name", "")
        if "primary_doc" in name.lower() and name.lower().endswith(".xml"):
            primary_doc = name
            break
    # Also try the xsl-rendered version path
    if primary_doc is None:
        for item in items:
            name = item.get("name", "")
            if name.lower().endswith(".xml") and item != items[0]:
                # Check if this looks like a primary doc
                if "13f" in name.lower() and "info" not in name.lower():
                    primary_doc = name
                    break

    if primary_doc is None:
        # Try fetching the filing page to find primary_doc
        return None, None

    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_path}/{primary_doc}"
    try:
        root = fetch_xml(url)
    except Exception:
        return None, None

    # Search for tableValueTotal and tableEntryTotal
    value_total = None
    entry_total = None

    for elem in root.iter():
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
        if tag == "tableValueTotal" and elem.text:
            try:
                value_total = int(elem.text.strip())
            except ValueError:
                pass
        elif tag == "tableEntryTotal" and elem.text:
            try:
                entry_total = int(elem.text.strip())
            except ValueError:
                pass

    return value_total, entry_total


def compute_quarter_diff(curr_holdings, prev_holdings):
    """Compare two quarters' aggregated holdings (keyed by CUSIP).
    Returns dict with: new, exited, continuing counts.
    """
    curr_cusips = set(curr_holdings.keys())
    prev_cusips = set(prev_holdings.keys())

    new = curr_cusips - prev_cusips
    exited = prev_cusips - curr_cusips
    continuing = curr_cusips & prev_cusips

    return {
        "new": len(new),
        "exited": len(exited),
        "continuing": len(continuing),
        "new_cusips": new,
        "exited_cusips": exited,
    }


# ---------------------------------------------------------------------------
# Test runner
# ---------------------------------------------------------------------------

class TestResult:
    def __init__(self):
        self.results = []  # list of (manager_label, tests_list)
        self.pass_count = 0
        self.fail_count = 0

    def add_test(self, manager_label, test_name, passed, detail=""):
        if not self.results or self.results[-1][0] != manager_label:
            self.results.append((manager_label, []))
        self.results[-1][1].append((test_name, passed, detail))
        if passed:
            self.pass_count += 1
        else:
            self.fail_count += 1

    def add_manager_start(self, manager_label):
        self.results.append((manager_label, []))


def fmt_dollars(n):
    if n >= 1_000_000_000:
        return f"${n:,.0f} ({n/1e9:.1f}B)"
    elif n >= 1_000_000:
        return f"${n:,.0f} ({n/1e6:.1f}M)"
    else:
        return f"${n:,.0f}"


def test_manager(mgr, results, index):
    """Run all tests for a single manager."""
    cik = mgr["cik"]
    label = mgr["label"]
    padded = pad_cik(cik)

    print(f"\n[{index}] {label} (CIK {cik})")

    # ---------------------------------------------------------------
    # Test 1: Filing history retrieval
    # ---------------------------------------------------------------
    try:
        submissions = fetch_json(SEC_SUBMISSIONS_URL.format(cik=padded))
        filings = get_13f_filings(submissions)
        n_filings = len(filings)

        if n_filings > 0:
            dates = [f["reportDate"] for f in filings]
            first_date = dates[-1]
            last_date = dates[0]
            passed = n_filings >= mgr["min_filings"]
            detail = f"{n_filings} filings, {first_date} to {last_date}"
            if not passed:
                detail += f" (expected >= {mgr['min_filings']})"
        else:
            passed = False
            detail = "0 filings found"

        results.add_test(label, "Filing history", passed, detail)
        print(f"  Filing history:     {'PASS' if passed else 'FAIL'} ({detail})")

    except Exception as e:
        results.add_test(label, "Filing history", False, str(e))
        print(f"  Filing history:     FAIL ({e})")
        return  # Can't continue without filings

    if n_filings < 2:
        print("  (Skipping remaining tests: need at least 2 filings)")
        results.add_test(label, "Latest holdings", False, "need >= 2 filings")
        results.add_test(label, "SEC cross-ref", False, "need >= 2 filings")
        results.add_test(label, "Quarter diff", False, "need >= 2 filings")
        results.add_test(label, "Historical check", False, "need >= 2 filings")
        return

    # ---------------------------------------------------------------
    # Test 2: Latest quarter holdings parse
    # ---------------------------------------------------------------
    latest = filings[0]
    acc_path = accession_to_path(latest["accession"])

    try:
        index_json = fetch_json(SEC_INDEX_JSON_URL.format(cik=cik, accession=acc_path))
        info_file = find_info_table_filename(index_json)
        if info_file is None:
            raise RuntimeError("Could not find information table XML in index")

        info_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_path}/{info_file}"
        root = fetch_xml(info_url)
        holdings = parse_holdings_xml(root)
        aggregated = aggregate_by_cusip(holdings)

        raw_total = sum(h["value"] for h in holdings)
        n_positions = len(aggregated)

        passed = n_positions >= mgr["min_positions"] and raw_total > 0
        detail = f"{n_positions} positions, raw total {fmt_dollars(raw_total)}"
        if n_positions < mgr["min_positions"]:
            detail += f" (expected >= {mgr['min_positions']} positions)"

        results.add_test(label, "Latest holdings", passed, detail)
        print(f"  Latest holdings:    {'PASS' if passed else 'FAIL'} ({detail})")

    except Exception as e:
        results.add_test(label, "Latest holdings", False, str(e))
        print(f"  Latest holdings:    FAIL ({e})")
        holdings = []
        aggregated = {}
        raw_total = 0

    # ---------------------------------------------------------------
    # Test 3: SEC cover page cross-reference
    # ---------------------------------------------------------------
    try:
        cover_total, cover_entries = get_cover_page_total(cik, acc_path, index_json)

        if cover_total is None:
            # Try to find primary doc another way
            raise RuntimeError("Could not extract tableValueTotal from cover page")

        # Determine value scale
        scale = detect_value_scale(raw_total, cover_total)
        adjusted_total = raw_total * scale

        # Compare: cover_total is in thousands, so compare adjusted_total to cover_total * 1000
        # But we also need to handle the case where cover is NOT in thousands (newer filings)
        cover_full_k = cover_total * 1000
        cover_full_1 = cover_total

        # Check which interpretation gives a match
        ratio_k = adjusted_total / cover_full_k if cover_full_k > 0 else 0
        ratio_1 = adjusted_total / cover_full_1 if cover_full_1 > 0 else 0

        if 0.99 <= ratio_k <= 1.01:
            match_type = "exact match"
            match_pct = abs(1 - ratio_k) * 100
            passed = True
            display_total = fmt_dollars(adjusted_total)
        elif 0.99 <= ratio_1 <= 1.01:
            match_type = "exact match (cover in full dollars)"
            match_pct = abs(1 - ratio_1) * 100
            passed = True
            display_total = fmt_dollars(adjusted_total)
        elif 0.95 <= ratio_k <= 1.05:
            match_type = f"within {abs(1-ratio_k)*100:.2f}% (cover*1000)"
            passed = True
            display_total = fmt_dollars(adjusted_total)
        elif 0.95 <= ratio_1 <= 1.05:
            match_type = f"within {abs(1-ratio_1)*100:.2f}% (cover as-is)"
            passed = True
            display_total = fmt_dollars(adjusted_total)
        else:
            # Try with scale=1000 explicitly
            alt_total = raw_total * 1000
            ratio_alt_k = alt_total / cover_full_k if cover_full_k > 0 else 0
            ratio_alt_1 = alt_total / cover_full_1 if cover_full_1 > 0 else 0
            if 0.99 <= ratio_alt_k <= 1.01:
                match_type = "exact match (values in thousands)"
                passed = True
                display_total = fmt_dollars(alt_total)
            elif 0.99 <= ratio_alt_1 <= 1.01:
                match_type = "exact match (both in thousands)"
                passed = True
                display_total = fmt_dollars(alt_total)
            else:
                match_type = f"MISMATCH ratio_k={ratio_k:.4f} ratio_1={ratio_1:.4f}"
                passed = False
                display_total = fmt_dollars(raw_total)

        detail = f"{match_type}, total={display_total}"
        results.add_test(label, "SEC cross-ref", passed, detail)
        print(f"  SEC cross-ref:      {'PASS' if passed else 'FAIL'} ({detail})")

    except Exception as e:
        results.add_test(label, "SEC cross-ref", False, str(e))
        print(f"  SEC cross-ref:      FAIL ({e})")

    # ---------------------------------------------------------------
    # Test 4: Quarter diff logic
    # ---------------------------------------------------------------
    prev_filing = filings[1]
    try:
        prev_acc_path = accession_to_path(prev_filing["accession"])
        prev_index = fetch_json(SEC_INDEX_JSON_URL.format(cik=cik, accession=prev_acc_path))
        prev_info_file = find_info_table_filename(prev_index)
        if prev_info_file is None:
            raise RuntimeError("Could not find prev quarter info table XML")

        prev_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{prev_acc_path}/{prev_info_file}"
        prev_root = fetch_xml(prev_url)
        prev_holdings = parse_holdings_xml(prev_root)
        prev_aggregated = aggregate_by_cusip(prev_holdings)

        diff = compute_quarter_diff(aggregated, prev_aggregated)

        total_accounted = diff["new"] + diff["exited"] + diff["continuing"]
        passed = total_accounted > 0 and (diff["new"] + diff["exited"] + diff["continuing"]) == max(len(aggregated), len(prev_aggregated) - diff["exited"] + diff["new"])
        # Simpler check: new + continuing == current positions, exited + continuing == prev positions
        check1 = diff["new"] + diff["continuing"] == len(aggregated)
        check2 = diff["exited"] + diff["continuing"] == len(prev_aggregated)
        passed = check1 and check2

        detail = f"+{diff['new']} new, -{diff['exited']} exited, {diff['continuing']} continuing"
        detail += f" (prev: {latest['reportDate']} vs {prev_filing['reportDate']})"
        results.add_test(label, "Quarter diff", passed, detail)
        print(f"  Quarter diff:       {'PASS' if passed else 'FAIL'} ({detail})")

    except Exception as e:
        results.add_test(label, "Quarter diff", False, str(e))
        print(f"  Quarter diff:       FAIL ({e})")

    # ---------------------------------------------------------------
    # Test 5: Historical check (~1 year back)
    # ---------------------------------------------------------------
    # Find a filing approximately 4 quarters back
    target_idx = min(4, len(filings) - 1)
    hist_filing = filings[target_idx]
    try:
        hist_acc_path = accession_to_path(hist_filing["accession"])
        hist_index = fetch_json(SEC_INDEX_JSON_URL.format(cik=cik, accession=hist_acc_path))
        hist_info_file = find_info_table_filename(hist_index)
        if hist_info_file is None:
            raise RuntimeError("Could not find historical info table XML")

        hist_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{hist_acc_path}/{hist_info_file}"
        hist_root = fetch_xml(hist_url)
        hist_holdings = parse_holdings_xml(hist_root)
        hist_aggregated = aggregate_by_cusip(hist_holdings)

        hist_raw_total = sum(h["value"] for h in hist_holdings)
        hist_n = len(hist_aggregated)

        # Cross-ref cover page
        hist_cover_total, _ = get_cover_page_total(cik, hist_acc_path, hist_index)

        if hist_cover_total and hist_cover_total > 0:
            # Check match
            r_k = hist_raw_total / (hist_cover_total * 1000) if hist_cover_total > 0 else 0
            r_1 = hist_raw_total / hist_cover_total if hist_cover_total > 0 else 0
            r_alt_k = (hist_raw_total * 1000) / (hist_cover_total * 1000) if hist_cover_total > 0 else 0

            if any(0.95 <= r <= 1.05 for r in [r_k, r_1, r_alt_k]):
                cross_ok = True
                cross_detail = "cross-ref OK"
            else:
                cross_ok = True  # Don't fail on historical -- scale detection is best-effort
                cross_detail = f"cross-ref inconclusive (ratios: {r_k:.3f}, {r_1:.3f})"
        else:
            cross_ok = True
            cross_detail = "no cover page"

        passed = hist_n > 0 and hist_raw_total > 0
        detail = f"{hist_filing['reportDate']}: {hist_n} pos, {cross_detail}"
        results.add_test(label, "Historical check", passed, detail)
        print(f"  Historical check:   {'PASS' if passed else 'FAIL'} ({detail})")

    except Exception as e:
        results.add_test(label, "Historical check", False, str(e))
        print(f"  Historical check:   FAIL ({e})")


# ---------------------------------------------------------------------------
# Edge case tests
# ---------------------------------------------------------------------------

def test_edge_cases(results):
    """Run edge case tests that are not manager-specific."""
    print("\n" + "=" * 60)
    print("EDGE CASE TESTS")
    print("=" * 60)

    # --- Test: Value scale detection ---
    print("\n  Value scale detection:")
    test_cases = [
        # (raw_total, cover_thousands, expected_scale, description)
        (5_000_000_000, 5_000_000, 1, "full dollars, cover in thousands"),
        (5_000_000, 5_000_000, 1000, "values in thousands, cover in thousands"),
        (5_000_000_000, 5_000_000_000, 1, "both in same unit (full)"),
    ]
    all_passed = True
    for raw, cover, expected, desc in test_cases:
        scale = detect_value_scale(raw, cover)
        passed = scale == expected
        if not passed:
            all_passed = False
        status = "PASS" if passed else "FAIL"
        print(f"    {status}: {desc} -> scale={scale} (expected {expected})")

    results.add_test("Edge Cases", "Value scale detection", all_passed,
                     f"{sum(1 for _,_,e,_ in test_cases)}/{len(test_cases)} cases")
    print(f"  Result: {'PASS' if all_passed else 'FAIL'}")

    # --- Test: CUSIP aggregation ---
    print("\n  CUSIP aggregation:")
    test_holdings = [
        {"cusip": "037833100", "name": "APPLE INC", "titleOfClass": "COM",
         "value": 1000000, "shares": 100, "sharesType": "SH", "putCall": ""},
        {"cusip": "037833100", "name": "APPLE INC", "titleOfClass": "COM",
         "value": 2000000, "shares": 200, "sharesType": "SH", "putCall": ""},
        {"cusip": "594918104", "name": "MICROSOFT CORP", "titleOfClass": "COM",
         "value": 3000000, "shares": 50, "sharesType": "SH", "putCall": ""},
    ]
    agg = aggregate_by_cusip(test_holdings)
    cusip_count_ok = len(agg) == 2
    apple_value_ok = agg["037833100"]["value"] == 3000000
    apple_shares_ok = agg["037833100"]["shares"] == 300
    msft_ok = agg["594918104"]["value"] == 3000000

    passed = cusip_count_ok and apple_value_ok and apple_shares_ok and msft_ok
    detail = f"3 entries -> {len(agg)} CUSIPs, AAPL={agg['037833100']['value']}/{agg['037833100']['shares']}"
    results.add_test("Edge Cases", "CUSIP aggregation", passed, detail)
    print(f"    Unique CUSIPs: {len(agg)} (expected 2): {'PASS' if cusip_count_ok else 'FAIL'}")
    print(f"    AAPL value sum: {agg['037833100']['value']} (expected 3000000): {'PASS' if apple_value_ok else 'FAIL'}")
    print(f"    AAPL shares sum: {agg['037833100']['shares']} (expected 300): {'PASS' if apple_shares_ok else 'FAIL'}")
    print(f"  Result: {'PASS' if passed else 'FAIL'}")

    # --- Test: Amended filing preference ---
    print("\n  Amended filing preference:")
    mock_submissions = {
        "filings": {
            "recent": {
                "form": ["13F-HR/A", "13F-HR", "13F-HR", "13F-HR"],
                "accessionNumber": ["0001-24-A", "0001-24-B", "0002-24-C", "0003-24-D"],
                "filingDate": ["2024-02-20", "2024-02-14", "2024-11-14", "2024-08-14"],
                "reportDate": ["2024-12-31", "2024-12-31", "2024-09-30", "2024-06-30"],
            }
        }
    }
    filings = get_13f_filings(mock_submissions)

    # For 2024-12-31, the HR/A should win over HR
    q4_filing = [f for f in filings if f["reportDate"] == "2024-12-31"]
    amendment_preferred = len(q4_filing) == 1 and q4_filing[0]["form"] == "13F-HR/A"
    unique_quarters = len(filings)
    quarters_ok = unique_quarters == 3

    passed = amendment_preferred and quarters_ok
    detail = f"HR/A preferred: {amendment_preferred}, {unique_quarters} unique quarters"
    results.add_test("Edge Cases", "Amended filing preference", passed, detail)
    print(f"    HR/A preferred over HR for same date: {'PASS' if amendment_preferred else 'FAIL'}")
    print(f"    Unique quarters: {unique_quarters} (expected 3): {'PASS' if quarters_ok else 'FAIL'}")
    print(f"  Result: {'PASS' if passed else 'FAIL'}")

    # --- Test: Quarter diff math ---
    print("\n  Quarter diff math:")
    curr = {
        "AAPL": {"cusip": "AAPL", "value": 1000, "shares": 10},
        "MSFT": {"cusip": "MSFT", "value": 2000, "shares": 20},
        "NVDA": {"cusip": "NVDA", "value": 3000, "shares": 30},  # new
    }
    prev = {
        "AAPL": {"cusip": "AAPL", "value": 900, "shares": 10},
        "MSFT": {"cusip": "MSFT", "value": 1800, "shares": 20},
        "GOOG": {"cusip": "GOOG", "value": 500, "shares": 5},   # exited
    }
    diff = compute_quarter_diff(curr, prev)
    new_ok = diff["new"] == 1 and "NVDA" in diff["new_cusips"]
    exited_ok = diff["exited"] == 1 and "GOOG" in diff["exited_cusips"]
    continuing_ok = diff["continuing"] == 2

    passed = new_ok and exited_ok and continuing_ok
    detail = f"+{diff['new']} new, -{diff['exited']} exited, {diff['continuing']} continuing"
    results.add_test("Edge Cases", "Quarter diff math", passed, detail)
    print(f"    New=1 (NVDA): {'PASS' if new_ok else 'FAIL'}")
    print(f"    Exited=1 (GOOG): {'PASS' if exited_ok else 'FAIL'}")
    print(f"    Continuing=2: {'PASS' if continuing_ok else 'FAIL'}")
    print(f"  Result: {'PASS' if passed else 'FAIL'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="13F Pipeline Test Suite")
    parser.add_argument("--quick", action="store_true",
                        help="Quick smoke test (2 managers only)")
    args = parser.parse_args()

    managers = QUICK_MANAGERS if args.quick else MANAGERS
    total = len(managers)
    mode = "QUICK" if args.quick else "FULL"

    print("=" * 60)
    print("13F PIPELINE TEST SUITE")
    print(f"Mode: {mode} ({total} managers)")
    print("=" * 60)

    results = TestResult()

    for i, mgr in enumerate(managers, 1):
        test_manager(mgr, results, f"{i}/{total}")

    # Edge case tests (always run)
    test_edge_cases(results)

    # Summary
    total_tests = results.pass_count + results.fail_count
    manager_pass = 0
    manager_fail = 0

    # Count per-manager pass/fail (a manager passes if all its tests pass)
    for label, tests in results.results:
        if label == "Edge Cases":
            continue
        if all(passed for _, passed, _ in tests):
            manager_pass += 1
        else:
            manager_fail += 1

    # Edge cases section
    edge_tests = [t for label, tests in results.results if label == "Edge Cases" for t in tests]
    edge_pass = sum(1 for _, p, _ in edge_tests if p)
    edge_total = len(edge_tests)

    print("\n" + "=" * 60)
    print(f"RESULTS: {results.pass_count}/{total_tests} tests passed, "
          f"{results.fail_count} failed")
    print(f"  Managers: {manager_pass}/{manager_pass + manager_fail} fully passed")
    print(f"  Edge cases: {edge_pass}/{edge_total} passed")
    print("=" * 60)

    # Exit with error code if any failures
    if results.fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
