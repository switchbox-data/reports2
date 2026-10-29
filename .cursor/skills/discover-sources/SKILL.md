---
name: discover-sources
description: >-
  Find candidate sources for a topic or project (regulatory filings, studies,
  papers, web pages), download them to a scratch inbox, check them against the
  library, and present a triage table. Use when the user asks to find, search for
  or gather sources, documents or filings on a topic. Never writes to Zotero.
---

# Discover sources

Search, download, de-duplicate and recommend. **Do not write to Zotero, DocumentCloud, Drive or the repo.** Anything the user keeps goes through the `ingest-source` skill afterwards.

## Steps

1. **Pin down the request**: topic, project (see `uv run python -m lib.sources.cli projects`), jurisdictions, years, document types, and **what the sources are for**: the question, testimony, report section or argument they will serve. Ingest needs this for each source's "why it's here" (see `context/code/source_metadata_conventions.md`, Index rows and descriptions), and this is the moment it is known. If the project or the purpose is unclear, ask once.
2. **Search.** Use web search and the source's own sites (commission dockets, agency libraries, Google Scholar, OSTI, SSRN). Prefer the primary document over a summary of it. For Maryland PSC filings use the `mdpuc-documents` skill's fetch recipes.
3. **Download to the scratch inbox**, never into the repo:

   ```text
   ~/.cache/switchbox_sources/inbox/<YYYY-MM-DD>_<topic>/
   ```

   One file per candidate, named after the original, plus two files in the same folder:
   - `candidates.json`: a list of `{file, title, issuer, date, docket, source_url, doi, why_relevant}`. Only record facts you saw on the document or its landing page; leave unknown fields `null`. `why_relevant` says what this candidate could do for the purpose below, specifically.
   - `PURPOSE.md`: the request in the user's own terms: the project, the question or work the sources serve, and who asked. Ingest reads it to write each source's "why it's here", so a later session (or another agent) can ingest these files without this chat.
4. **De-duplicate.** For each candidate run `just sources-dedupe --path-file <file> --url <source_url>` (add `--doi` or `--title` when known). Matches by file hash, URL, DOI or title in the repo or Zotero mean the library already has it; list the existing citation key.
5. **Triage table in chat**, one row per candidate: title, issuer, date, docket, relevance in one line, a recommendation (ingest / skip / already in library as `<citekey>`), and the file path. Put the strongest candidates first. Say what you searched and what you could not reach.
6. **Hand off.** Ask which candidates to ingest. For each approved one, continue with the `ingest-source` skill, passing the downloaded file as `--path-source` and the inbox folder's `PURPOSE.md` and `why_relevant` as the basis for "why it's here".

## Rules

- Do not download paywalled material by working around the paywall; list it with its landing page for the user to fetch.
- A candidate is not a recommendation to cite it. Relevance notes say what the document contains, not what it proves.
- Leave the inbox folder in place; the user cleans it.
