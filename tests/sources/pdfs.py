"""A tiny PDF writer for tests: text pages in Helvetica, with a correct cross-reference table."""

from __future__ import annotations

from pathlib import Path


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_numbered_pdf(pages: list[list[str]], path: Path, footer: list[str] | None = None) -> Path:
    """Pleading-paper pages: each line numbered 1, 2, ... in the left margin, with an optional footer per page."""
    streams = []
    for i, lines in enumerate(pages):
        ops = ["BT", "/F1 11 Tf"]
        for n, line in enumerate(lines, start=1):
            y = 740 - 20 * n
            ops.append(f"1 0 0 1 40 {y} Tm ({n}) Tj")
            ops.append(f"1 0 0 1 80 {y} Tm ({_escape(line)}) Tj")
        if footer:
            ops.append(f"1 0 0 1 300 40 Tm ({_escape(footer[i])}) Tj")
        ops.append("ET")
        streams.append("\n".join(ops))
    return _write(streams, path)


def make_pdf(pages: list[list[str]], path: Path, info: dict[str, str] | None = None) -> Path:
    """Write ``pages`` (each a list of text lines, top to bottom) to ``path``; ``info`` goes in the Info dict."""
    streams = []
    for lines in pages:
        ops = ["BT", "/F1 11 Tf", "14 TL", "50 750 Td"]
        for line in lines:
            ops.append(f"({_escape(line)}) Tj T*")
        ops.append("ET")
        streams.append("\n".join(ops))
    return _write(streams, path, info)


def _write(streams: list[str], path: Path, info: dict[str, str] | None = None) -> Path:
    objects: list[bytes] = []

    def add(body: str | bytes) -> int:
        objects.append(body.encode("latin-1") if isinstance(body, str) else body)
        return len(objects)

    catalog = add("")  # placeholder, filled once the page tree exists
    pages_obj = add("")
    font = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    for stream in streams:
        content = add(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")
        page_ids.append(
            add(
                f"<< /Type /Page /Parent {pages_obj} 0 R /MediaBox [0 0 612 792] "
                f"/Contents {content} 0 R /Resources << /Font << /F1 {font} 0 R >> >> >>"
            )
        )
    objects[catalog - 1] = f"<< /Type /Catalog /Pages {pages_obj} 0 R >>".encode()
    kids = " ".join(f"{i} 0 R" for i in page_ids)
    objects[pages_obj - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>".encode()
    info_ref = ""
    if info:
        entries = " ".join(f"/{k} ({_escape(v)})" for k, v in info.items())
        info_ref = f" /Info {add(f'<< {entries} >>')} 0 R"
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objects) + 1} /Root {catalog} 0 R{info_ref} >>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.write_bytes(bytes(out))
    return path
