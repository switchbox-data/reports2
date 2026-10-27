# Reconcile organization names (one batch)

You are proposing canonical organization names for one batch of the Zotero library cleanup. **You never write to Zotero.** Your only output is one JSON file. A person reviews every proposal in a Google Sheet before anything changes.

## Inputs

- The batch number `NN` you were given.
- Work folder `W` = `~/.cache/switchbox_sources/org_cleanup/<date>/` (the newest dated folder unless told otherwise).
- `W/extract/batches/batch_NN.json`:
  - `groups`: each is one normalized name string (`norm`) with the raw spellings (`variants`) and how often each appears, which fields it appears in (`roles`: `creator:author`, `field:publisher`, `field:institution`, ..., or `key_author` = the author part of the current citation key on an item with no creator), and the items it appears on.
  - `edges`: automatic hints that two groups may be the same organization (acronym, fuzzy match, a short form on the item, two names in one string, author and publisher on the same item). Hints only; many are wrong.
  - `items`: every item touching these groups, with its title, date, URL, creators, organization fields and current key.
- `W/extract/groups_index.tsv`: every group in the whole library (all batches), so you can spot the same organization in another batch.
- **The policy: `context/code/source_metadata_conventions.md`. Read it first and follow it exactly**: full names, short forms, state prefixes, subsidiaries, renamed organizations, sub-units, several organizations.

## Evidence

Every short form, and every full name that differs from what the library already says, needs evidence: a short quote and where it came from. Look, in this order:

1. The document: `just orgs-evidence <item key> [<item key> ...]` prints the item's metadata and the opening of its PDF's text (cover, letterhead, "submitted by", the definitions paragraph where abbreviations are defined). Quote it with the item's current key and "p. 1" (or the page if visible).
2. The organization's own website (search the web). Quote it with the URL.
3. For subsidiaries, the regulator's usage (a commission order or docket listing), with the URL.

Never invent a short form. If you can't find the organization using one, set `short_form` to null and `short_form_source` to `"none"`. If the policy's subsidiary table says "(verify)", find the evidence or say in `notes` that you couldn't, and set `needs_decision: true`.

## What to decide for each group

Assign **every group in your batch to exactly one cluster**. A cluster is one real-world organization (or one non-organization):

- `kind`:
  - `"organization"`: a real organization. Give `canonical_full_name` per the policy.
  - `"person"`: the string is actually a person (for example "Polly Eldringhoff; Jerry Dickson" stored as one field). Put the people in `notes` and add an `item_overrides` entry with `action: "split"` and `to` = each person as "Family, Given".
  - `"not_an_organization"`: a series, website, program or blog name ("Today in Energy", "Mass Save"), a journal, or junk. Say in `notes` what it is and whether it should be removed from the field.
- `groups`: the group ids in **your** batch that belong to this cluster.
- `same_as_groups`: group ids in **other** batches (from `groups_index.tsv`) that you believe are the same organization. Don't assign them; just list them.
- `short_form`, `short_form_source` (`own_usage`, `common_usage`, `state_prefix_rule` or `none`), `evidence`.
- `confidence`: `high` (clear from the documents and policy), `medium` (likely, some judgment), `low` (guess; needs review).
- `flags`, any of: `SUBSIDIARY`, `PARENT`, `RENAMED`, `SUCCESSOR_NOT_RENAME`, `SHORT_FORM_NOT_OWN_USAGE`, `ABBREVIATION_REPLACED`, `FULL_NAME_CORRECTED`, `MIXED_ORG_AND_PEOPLE`, `MULTIPLE_ORGS`, `PER_ITEM_CHECK`, `DISTINCT_FROM:<name>`.
- `item_overrides`: when one string means different organizations on different items (bare "PSC", "National Grid" meaning a subsidiary, "Eversource" meaning CL&P on CT dockets), check each such item and list it:
  - `action: "assign"`, `role` (for example `creator:author` or `field:publisher`), `to: ["<full name of the right organization>"]`, a `reason` and evidence;
  - `action: "split"` when one string names several organizations ("NYSEG / RG&E") or several people; `to` lists each full name;
  - `action: "remove"` when the field should be emptied (a publisher that is a website name, not an organization).
    Use the cluster's own full name for the items that match it; overrides are only for the exceptions.
- `needs_decision: true` when a person must choose (ambiguous parent versus subsidiary, unverified short form, conflicting evidence), with the question in `notes`.

Be careful with look-alikes the hints suggest: NYSEG is not NYPSC; Nicor Gas is not National Grid; New Jersey Natural Gas is not "NG"; NY PSC and MD PSC are different; NY DPS is not NY PSC; ICC Staff is not ICC; EIA is not DOE.

## Output

Write `W/proposals/batch_NN.json` (create the folder if needed):

```json
{
  "batch": "BNN",
  "clusters": [
    {
      "groups": ["G010", "G014"],
      "same_as_groups": [],
      "kind": "organization",
      "canonical_full_name": "Illinois Commerce Commission",
      "short_form": "ICC",
      "short_form_source": "own_usage",
      "evidence": [{"quote": "Illinois Commerce Commission (\"ICC\" or \"Commission\")", "source": "icc_FutureGasProceeding_2024 p. 1"}],
      "confidence": "high",
      "flags": [],
      "item_overrides": [],
      "needs_decision": false,
      "notes": ""
    }
  ]
}
```

Then validate it: `just orgs-proposals NN`. Fix every problem it reports for your batch (problems about other batches' groups mean you put a foreign group in `groups` instead of `same_as_groups`). Finish with a short summary: clusters proposed, how many need a decision, and anything surprising.
