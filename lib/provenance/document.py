"""Write the provenance rows as markdown, a landscape Word document and CSVs."""

from __future__ import annotations

import csv
import subprocess
import zipfile
from pathlib import Path

from lib.provenance.config import ProvenanceConfig
from lib.provenance.rows import Row, format_locations
from lib.provenance.text import md_escape


def used_notebooks(rows: list[Row]) -> set[str]:
    return {r.link.notebook for r in rows if r.link and r.link.notebook}


def write_markdown(cfg: ProvenanceConfig, rows: list[Row], path_md: Path) -> None:
    used = used_notebooks(rows)
    out = [
        "---",
        f"title: {_yaml_str(cfg.title)}",
        f"subtitle: {_yaml_str(cfg.subtitle)}",
        "---",
        "",
        cfg.intro,
        "## Where the work happens",
        "",
        "The table links to these notebooks:",
        "",
    ]
    order = [*cfg.namespaces.values(), cfg.testimony_key]
    order += sorted(used - set(order))
    for name in order:
        if name not in used:
            continue
        if name not in cfg.notebook_blurbs:
            raise KeyError(f"no entry for notebook {name!r} in notebook_blurbs")
        title, blurb = cfg.notebook_blurbs[name]
        out.append(f"- **{title}** ([{name}.qmd]({cfg.notebook_url(name)})): {blurb}")
    out.append("")
    if cfg.platform_links:
        out += [cfg.platform_intro, "", *[f"- {s}" for s in cfg.platform_links], ""]
    for heading, row_type, what in (
        ("Figures", "Figure", "Figure"),
        ("Tables", "Table", "Table"),
        ("Numbers", "Number", "Quote (number in bold)"),
    ):
        if not any(r.type == row_type for r in rows):
            continue
        out += [
            f"## {heading}",
            "",
            f"| Location | {what} | Where it's generated |",
            "|------------------|--------------------------------------------------|------------------------------|",
        ]
        for r in rows:
            if r.type != row_type:
                continue
            link = f"[{md_escape(r.link.text)}]({r.link.url})" if r.link else ""
            out.append(f"| {format_locations(r.locations)} | {r.what} | {link} |")
        out.append("")
    path_md.write_text("\n".join(out))


def _yaml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def landscape_reference(path_ref: Path) -> Path:
    data = subprocess.run(
        ["quarto", "pandoc", "--print-default-data-file", "reference.docx"], check=True, capture_output=True
    ).stdout
    path_ref.write_bytes(data)
    tmp = path_ref.with_suffix(".tmp.docx")
    with zipfile.ZipFile(path_ref) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            buf = zin.read(item.filename)
            if item.filename == "word/document.xml":
                page = (
                    '<w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/>'
                    '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" '
                    'w:header="720" w:footer="720" w:gutter="0"/>'
                )
                buf = buf.decode().replace("<w:sectPr>", "<w:sectPr>" + page, 1).encode()
            elif item.filename == "word/styles.xml":
                xml = buf.decode()
                compact = xml.find('w:styleId="Compact"')
                end = xml.find("</w:style>", compact)
                xml = xml[:end] + '<w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>' + xml[end:]
                buf = xml.encode()
            zout.writestr(item, buf)
    tmp.replace(path_ref)
    return path_ref


def write_docx(path_md: Path, path_docx: Path) -> None:
    ref = landscape_reference(path_md.parent / ".reference_landscape.docx")
    subprocess.run(
        ["quarto", "pandoc", str(path_md), "-o", str(path_docx), f"--reference-doc={ref}", "--columns=200"],
        check=True,
    )
    ref.unlink()


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def rows_for_csv(rows: list[Row]) -> list[dict[str, str]]:
    return [
        {
            "type": r.type,
            "location": format_locations(r.locations),
            "what_it_is": r.what_plain,
            "link_text": r.link.text if r.link else "",
            "url": r.link.url if r.link else "",
        }
        for r in rows
    ]
