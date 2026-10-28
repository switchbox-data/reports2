"""Bibliography tooling: build ``reports/references.yaml`` from Zotero and check citations against it.

Zotero is the single source of truth for bibliographic metadata. Modules:

- ``zotero``: pyzotero wrapper (credentials from ``.env``, collection trees, item fetches).
- ``extra``: parse and edit Zotero's Extra field (``Citation Key:``, ``tex.shortauthor:``).
- ``citekeys``: the canonical citation-key rule.
- ``bib``: build ``reports/references.yaml`` from Zotero items (``just sync-bib``).
- ``checks``: consistency checks on the bibliography's organization names and keys.
- ``citations``: find ``@key`` citations in report sources (``just check-citekeys``).
"""
