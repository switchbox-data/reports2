# MDPUC document fetch — reference

Detailed HTTP workflow for Maryland PSC DMS MailLog search and PSC flat uploads.
Read when the helper script fails or you need to debug a fetch.

## Endpoints

| Purpose        | URL                                                                      |
| -------------- | ------------------------------------------------------------------------ |
| MailLog search | `https://webpscxb.pscmaryland.com/DMS/maillogsearch`                     |
| MailLog viewer | `https://webpscxb.pscmaryland.com/DMS/maillogpdfview/MailLog/0/0/{ML}/0` |
| Case jacket    | `https://webpscxb.pscmaryland.com/DMS/case/{case_no}`                    |
| PSC uploads    | `https://psc.maryland.gov/wp-content/uploads/`                           |

## Technique 1: MailLog search (step by step)

### Why two hops?

The DMS exposes multiple path namespaces:

- **Filing index paths** like `pdfview/Public/PC44/101/0/0/218934_D0121712~pdf` —
  often **0 bytes** when fetched directly.
- **MailLog-resolved paths** like
  `/DMS/pdfview/%60%60wportal%60Documents%60DMS%6021%608934%60/218934_D0051941~pdf`
  — the real PDF (backtick characters URL-encoded as `%60`).

MailLog search → viewer → `btnOpenPdfFile` performs this resolution.

### ASP.NET form fields

The search page is ASP.NET WebForms. Required POST fields:

- `__VIEWSTATE` (required)
- `__VIEWSTATEGENERATOR` (required)
- `__EVENTVALIDATION` (may be absent on current site — omit if not in HTML)
- `ctl00$ContentPlaceHolder1$txtSearch` = ML number
- `ctl00$ContentPlaceHolder1$btnSearch` = `Search`

### HTML parsing pitfalls

1. **`data-pdf` uses single quotes** on search results (`class='btnOpenPdf'`) and
   viewer page (`btnOpenPdfFile`). Match both quote styles:

   ```python
   r'data-pdf="([^"]+)"'   # double quotes
   r"data-pdf='([^']+)'"   # single quotes
   ```

2. **Search results may not use `data-pdf` on the first match** — the ML button
   wraps `data-pdf='/DMS/maillogpdfview/MailLog/0/0/218934/0'`. Fallback: regex
   for `/DMS/maillogpdfview/MailLog/0/0/{ML}/\d+`.

3. **Viewer page** exposes the real PDF on `btnOpenPdfFile`:

   ```html
   data-pdf='/DMS/pdfview/%60%60wportal%60Documents%60DMS%6021%608934%60/218934_D0051941~pdf'
   ```

### Python example (manual)

```python
import re
from pathlib import Path
from urllib.parse import urljoin

import requests

BASE = "https://webpscxb.pscmaryland.com"
ML = "218934"
OUT = Path("context/sources/md_hp_rates/mdpuc_218934_pc44_rate_design_final_report.pdf")

def data_pdf(html: str) -> str | None:
    for pat in (r'data-pdf="([^"]+)"', r"data-pdf='([^']+)'"):
        m = re.search(pat, html)
        if m:
            return m.group(1)
    return None

def hidden_fields(html: str) -> dict[str, str]:
    out = {}
    for name in ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"):
        m = re.search(rf'name="{name}"[^>]*value="([^"]*)"', html)
        if m:
            out[name] = m.group(1)
    return out

with requests.Session() as s:
    s.headers["User-Agent"] = "Mozilla/5.0 (compatible; Switchbox/1.0)"
    page = s.get(f"{BASE}/DMS/maillogsearch", timeout=60)
    page.raise_for_status()

    payload = hidden_fields(page.text)
    payload["ctl00$ContentPlaceHolder1$txtSearch"] = ML
    payload["ctl00$ContentPlaceHolder1$btnSearch"] = "Search"
    results = s.post(f"{BASE}/DMS/maillogsearch", data=payload, timeout=60)
    results.raise_for_status()

    viewer = data_pdf(results.text) or f"/DMS/maillogpdfview/MailLog/0/0/{ML}/0"
    viewer_page = s.get(urljoin(BASE, viewer), timeout=60)
    viewer_page.raise_for_status()

    pdf_path = data_pdf(viewer_page.text)
    assert pdf_path, "no data-pdf on viewer page"

    pdf = s.get(urljoin(BASE, pdf_path), timeout=120)
    pdf.raise_for_status()
    assert pdf.content[:4] == b"%PDF", "not a PDF"
    assert len(pdf.content) > 1000, f"suspiciously small: {len(pdf.content)} bytes"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(pdf.content)
    print(f"wrote {OUT} ({len(pdf.content):,} bytes)")
```

### curl sketch (search only — viewer still needs HTML parse)

```bash
# Step 1: save search page, extract __VIEWSTATE manually or with a script
curl -sS -c /tmp/psc_cookies.txt \
  'https://webpscxb.pscmaryland.com/DMS/maillogsearch' \
  -o /tmp/maillogsearch.html

# Step 2: POST search (substitute VIEWSTATE values from step 1)
curl -sS -b /tmp/psc_cookies.txt -c /tmp/psc_cookies.txt \
  -X POST 'https://webpscxb.pscmaryland.com/DMS/maillogsearch' \
  --data-urlencode 'ctl00$ContentPlaceHolder1$txtSearch=218934' \
  --data-urlencode 'ctl00$ContentPlaceHolder1$btnSearch=Search' \
  --data-urlencode '__VIEWSTATE=PASTE_HERE' \
  --data-urlencode '__VIEWSTATEGENERATOR=PASTE_HERE' \
  -o /tmp/maillog_results.html

# Step 3+: parse data-pdf from results → GET viewer → parse btnOpenPdfFile → GET PDF
# Prefer the Python helper script instead of curl for steps 3–5.
```

### Validation

After every download:

```bash
file downloaded.pdf          # should say "PDF document"
wc -c downloaded.pdf         # expect ≫ 1 KB (ML 218934 ≈ 368 KB)
head -c 5 downloaded.pdf     # should print %PDF-
```

## Technique 2: PSC flat uploads

Direct fetch when you have a public URL:

```bash
curl -fsSL -o context/sources/md_hp_rates/mdpuc_9761_order_91917_drive_act_implementation.pdf \
  "https://psc.maryland.gov/wp-content/uploads/Order-91917_ML-323522-9761-1.pdf"
```

Discovery tips:

- Google: `site:psc.maryland.gov/wp-content/uploads PC44 rate design`
- Order PDFs often embed ML and case: `Order-{order_no}_ML-{ml}-{case}-1.pdf`
- Straw proposals and workshop materials may live under year/month paths

## Case jacket (fallback)

`https://webpscxb.pscmaryland.com/DMS/case/9761`

- Lists filings with ML numbers, dates, and descriptions
- PDF links in the jacket UI do not map reliably to headless-downloadable URLs
- Use the jacket to **find ML numbers**, then fetch via Technique 1

## Extraction notes (fetch companion)

See `SKILL.md` Phase 2 and
`rate-design-platform/.cursor/commands/extract-pdf-to-markdown.md`.

**PyMuPDF footnote pitfall:** In dict/text mode, footnote superscripts often
appear as a small-font span appended to the last word of the sentence
(`AMI).6` where `6` is 6.5pt and the rest is 10pt). Fix by reading the PDF
visually and placing `[^6]` after the correct clause.

**Letterhead blocks** repeat on every page — strip after first occurrence.

**Table reconstruction:** When `get_text` scatters cells, open the PDF side by
side and build markdown tables manually; verify row/column counts against the
source.
