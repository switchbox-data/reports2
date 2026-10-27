# Find docket numbers for proceeding documents (one batch)

You are finding the docket numbers of utility-commission proceeding documents for one batch of the Zotero library cleanup, so their titles can take the form `Docket <number>: <title>`. **You never write to Zotero.** Your only output is one JSON file. A person reviews every change before anything is written.

Run every command from the repo checkout you were given (the `zotero-org-cleanup` branch).

## Inputs

- The batch number `NN` you were given.
- Work folder `W` = `~/.cache/switchbox_sources/org_cleanup/<date>/` (the newest dated folder unless told otherwise).
- `W/docket_titles/inputs/batch_NN.json`: each item's key, type, the keys reports cite it as (`cited_as`) and its `current` metadata.
- The policy: the "Titles" section of `context/code/source_metadata_conventions.md`. Read it first.

## Evidence

Look, in this order, and quote what you find (a short quote and its source):

1. The document: `just orgs-evidence <item key> [<item key> ...]` prints the item's metadata, notes, attachments and the opening of its PDF's text. Docket numbers are usually on the cover page, in the caption or in the header ("Case 22-E-0317", "D.P.U. 25-08", "Docket No. 26-05-10", "Case No. 9648", "Docket 4770").
2. Fields such as `callNumber`, `extra`, `archiveLocation` and the URL (commission document links often carry the docket).
3. The URL itself (fetch it), or a web search for the title plus the commission's name.

## What to decide for each item

- Is it a **document filed in, or issued in, a utility-commission proceeding** (testimony, exhibits, orders, petitions, applications, comments, briefs, data responses, joint proposals, compliance filings, staff reports, notices, workpapers)? If not (10-Ks, executive orders, agency plans, web pages, tariff sheets, annual reports), set `docket` to `null` and say why in `notes`.
- `docket`: the commission's own number, **without** "Case", "D.P.U.", "Docket" or "No." (`22-E-0317`, `25-08`, `26-05-10`, `9648`, `4770`, `25-45-GE`, `CI-23-117`). A document filed in several dockets: the **first** one listed on the document.
- `title`: the document's title **without** the docket reference and without "Docket …:" (the cleanup adds the prefix). Use the title on the document; keep the current title unless it is wrong, all caps, or contains the docket number. Write it in title case.
- `evidence` (at least one, for any non-null docket), `confidence` (`high`, `medium`, `low`) and `notes`.

## Output

Write `W/docket_titles/batch_NN.json`:

```json
{
  "batch": "DNN",
  "items": [
    {
      "item": "K5DMIHRX",
      "docket": "18-M-0084",
      "title": "Order Directing Energy Efficiency and Building Electrification Proposals",
      "evidence": [{"quote": "CASE 18-M-0084 - In the Matter of a Comprehensive Energy Efficiency Initiative", "source": "K5DMIHRX p. 1"}],
      "confidence": "high",
      "notes": ""
    },
    {"item": "5JS5FZ2W", "docket": null, "evidence": [], "confidence": "high", "notes": "SEC 10-K, not a commission filing"}
  ]
}
```

Finish with a short summary: how many dockets found, how many `null`, how many low confidence, and anything surprising.
