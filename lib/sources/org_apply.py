"""What the cleanup writes to each Zotero item, and a local preview of the CSL it would produce.

``target_data`` is the item ``data`` the apply step sends: the plan's reviewed metadata, the key
pinned in Extra and Zotero's native ``citationKey`` cleared. It is used by both the dry run and
the apply, so the dry run previews exactly what will be written.

Zotero builds an item's CSL-JSON on the server, so the dry run cannot fetch it for unsaved edits.
``preview_csl`` patches the snapshot's CSL-JSON for the Zotero fields the cleanup changes, with
Zotero's field-to-CSL mapping. It is a preview: after the apply, the bibliography is rebuilt from
the CSL-JSON Zotero returns and the render diff is rerun on it.
"""

from __future__ import annotations

import copy
import re
from collections.abc import Mapping
from typing import Any

from lib.sources import extra

# Zotero field -> CSL variable, for the fields the cleanup can change. Several fields can map to
# one variable; an item type only has one of them.
CSL_VARIABLE = {
    "title": "title",
    "caseName": "title",
    "nameOfAct": "title",
    "subject": "title",
    "date": "issued",
    "dateDecided": "issued",
    "dateEnacted": "issued",
    "issueDate": "issued",
    "publisher": "publisher",
    "institution": "publisher",
    "university": "publisher",
    "company": "publisher",
    "label": "publisher",
    "distributor": "publisher",
    "network": "publisher",
    "studio": "publisher",
    "repository": "publisher",
    "websiteTitle": "container-title",
    "blogTitle": "container-title",
    "forumTitle": "container-title",
    "publicationTitle": "container-title",
    "proceedingsTitle": "container-title",
    "bookTitle": "container-title",
    "programTitle": "container-title",
    "legislativeBody": "authority",
    "court": "authority",
    "authority": "authority",
    "extra": "note",
}

# Zotero creator type -> CSL name variable (Zotero's own mapping; unlisted types are dropped).
CSL_NAME = {
    "author": "author",
    "sponsor": "author",
    "presenter": "author",
    "programmer": "author",
    "inventor": "author",
    "artist": "author",
    "director": "author",
    "podcaster": "author",
    "cartographer": "author",
    "performer": "author",
    "interviewee": "author",
    "contributor": "contributor",
    "editor": "editor",
    "seriesEditor": "collection-editor",
    "translator": "translator",
    "reviewedAuthor": "reviewed-author",
    "recipient": "recipient",
    "interviewer": "interviewer",
    "cosponsor": "contributor",
}

_ISO_RE = re.compile(r"^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$")


def target_data(plan: Mapping[str, Any]) -> dict[str, Any] | None:
    """The ``data`` to write for an ``update`` plan entry; ``None`` for items going to the trash."""
    if plan["action"] != "update":
        return None
    data = copy.deepcopy(plan["after"])
    if plan["key"]:
        data["extra"] = extra.set_field(data.get("extra"), extra.CITATION_KEY, plan["key"])
    if "citationKey" in data:
        data["citationKey"] = ""
    return data


def _csl_name(creator: Mapping[str, Any]) -> dict[str, str]:
    if creator.get("name"):
        return {"literal": creator["name"]}
    name = {"family": creator.get("lastName", "")}
    if creator.get("firstName"):
        name["given"] = creator["firstName"]
    return name


def _csl_date(text: str) -> dict[str, Any]:
    if m := _ISO_RE.match(text.strip()):
        return {"date-parts": [[int(p) for p in m.groups() if p]]}
    return {"raw": text}


def preview_csl(csl: Mapping[str, Any], before: Mapping[str, Any], after: Mapping[str, Any]) -> dict[str, Any]:
    """``csl`` with the variables of every Zotero field that differs between ``before`` and ``after`` redone."""
    out = copy.deepcopy(dict(csl))
    if before.get("creators") != after.get("creators"):
        for var in set(CSL_NAME.values()):
            out.pop(var, None)
        for c in after.get("creators", []):
            if var := CSL_NAME.get(c["creatorType"]):
                out.setdefault(var, []).append(_csl_name(c))
    changed = {f for f in set(before) | set(after) if f in CSL_VARIABLE and before.get(f) != after.get(f)}
    for var in {CSL_VARIABLE[f] for f in changed}:
        value = next((after[f] for f, v in CSL_VARIABLE.items() if v == var and after.get(f)), "")
        if not value:
            out.pop(var, None)
        elif var == "issued":
            out[var] = _csl_date(value)
        else:
            out[var] = value
    return out
