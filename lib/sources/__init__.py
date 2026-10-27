"""Source metadata tooling shared by the bibliography generator, source ingest and library upkeep.

Zotero is the single source of truth for bibliographic metadata. Modules:

- ``zotero``: pyzotero wrapper (credentials from ``.env``, collection trees, item fetches).
- ``extra``: parse and edit Zotero's Extra field (``Citation Key:``, ``tex.shortauthor:``).
- ``citekeys``: the canonical citation-key rule.
- ``docket_titles``, ``title_case``: title conventions (``Docket <number>: ...``, no ALL CAPS).
- ``bib``: build ``reports/references.yaml`` from Zotero items (``just sync-bib``).
- ``checks``: consistency checks on the bibliography's organization names and keys.
- ``citations``: find ``@key`` citations in report sources (``just check-citekeys``).
- ``rekey``: rename cited keys in report sources (``just rekey-refs``).
- ``make_csl``: the Switchbox CSL style (``just make-csl``).
- ``snapshot``, ``zotero_write``: whole-library backup, and versioned, logged, reversible bulk writes.
"""
