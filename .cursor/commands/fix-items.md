# Fix items missing an author, date or title (one batch)

You are researching authors, dates and titles for one batch of the Zotero library cleanup. **You never write to Zotero.** Your only output is one JSON file. A person reviews every suggestion in a Google Sheet before anything changes.

Run every command from the repo checkout you were given (the `zotero-org-cleanup` branch).

## Inputs

- The batch number `NN` you were given.
- Work folder `W` = `~/.cache/switchbox_sources/org_cleanup/<date>/` (the newest dated folder unless told otherwise).
- `W/item_fixes/inputs/batch_NN.json`:
  - `items`: each item's key, what it `needs` (`author`, `date`, `title`), the keys reports cite it as (`cited_as`) and its `current` metadata after the organization cleanup.
  - `organizations`: every organization's reviewed full name and short form. Use these exact full names.
- **The policy: `context/code/source_metadata_conventions.md`. Read it first.** The author is the entity that issued the document (the operating company that filed it, not its parent; NY DPS Staff, not the NY PSC, for Staff testimony).

## Evidence

Look, in this order, and quote what you find (a short quote and its source):

1. The document: `just orgs-evidence <item key> [<item key> ...]` prints the item's metadata, notes, attachments and the opening of its PDF's text (cover, letterhead, signature block, filing date).
2. The URL in the item (fetch it), or the docket listing it came from.
3. A web search for the title.

## What to decide for each item

One entry per item in your batch:

- `organizations`: author full names in order, from the `organizations` list when the organization is there; otherwise its full name per the policy (say so in `notes`).
- `people`: person authors as `{"first": ..., "last": ...}`, after organizations. For testimony, the witnesses.
- `date`: the document's own date (filing, publication or "last updated"), as `YYYY`, `YYYY-MM` or `YYYY-MM-DD`. Not the access date. A tariff or rate summary is dated by its effective date.
- `title`: only when the current title is missing or a file name / URL slug. Use the title on the document ("Summary of Gas Adjustment Factors"), not a description.
- Leave a field out when the item doesn't need it and you found nothing wrong.
- `action`: `"fix"` (default); `"delete"` for an empty or junk item; `"duplicate_of"` with `duplicate_of: "<item key>"` when another item in the library is the same document (keep the one reports cite, else the more complete one).
- `evidence` (at least one), `confidence` (`high`, `medium`, `low`) and `notes`.

## Output

Write `W/item_fixes/batch_NN.json`:

```json
{
  "batch": "FNN",
  "fixes": [
    {
      "item": "NDVHDWRY",
      "organizations": ["National Grid Massachusetts Gas"],
      "date": "2025-03-01",
      "title": "Gas Adjustment Factors",
      "evidence": [{"quote": "Boston Gas Company d/b/a National Grid ... Effective March 1, 2025", "source": "NDVHDWRY p. 1"}],
      "confidence": "high",
      "notes": ""
    }
  ]
}
```

Then validate it: `just orgs-fixes NN`, and fix every problem it reports. Finish with a short summary: items fixed, how many are low confidence, and anything surprising.
