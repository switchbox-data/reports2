---
name: render-preview
description: >-
  Render a reports2 Quarto document with just render into the gitignored
  docs/ folder, serve it locally, and open it for the user. Use when the
  user asks to render, preview, or show a .qmd, including "just render this
  document and show me the result."
---

# Render and preview a Quarto document

Render with the report's `just render`, confirm the HTML landed in gitignored `docs/`, serve that folder, and open the page through Cursor's port forward.

Do not `just publish`. Publish copies into the committed GitHub Pages tree.

## Render

1. Find the report directory: the nearest ancestor of the `.qmd` that has a `Justfile` with a `render` recipe and a `_quarto.yml`. Run every command from that directory.
2. Pass the `.qmd` path relative to the report directory. A file in a subdirectory stays a subdirectory path.

```bash
unset UV_CACHE_DIR
just render ciec_requests/ciec_request_1.qmd   # one file
just render                                     # whole project
```

`unset UV_CACHE_DIR` is required. A leftover sandbox cache path makes `uv` exit immediately. Run the command outside the sandbox (`required_permissions: ["all"]`).

Renders that read S3 can take several minutes. Start the command in the background and poll its terminal. A quiet first minute is not a failure.

`just render` writes HTML beside the source, then `lib/just/render.py` moves the `.html` and `*_files/` into `docs/`, mirroring the relative path, and inlines SVGs. Example: `ciec_requests/ciec_request_1.qmd` becomes `docs/ciec_requests/ciec_request_1.html`.

## Confirm it will not be committed

Repo `.gitignore` ignores `docs/`, `.quarto/`, and `_freeze`. After the render:

- `git check-ignore -v <report>/docs/<path>.html` matches `docs/`.
- No `.html` or `*_files/` remains next to the source.
- `git status --short` does not list the rendered HTML.

If `docs/` is not ignored, stop and say so. Do not invent another output directory.

## Serve

Serve the report's `docs/` directory, not the report root. Reuse a server already serving that directory.

```bash
python3 -m http.server 8765 --bind 127.0.0.1 \
  --directory <report>/docs
```

Pick another port if 8765 is taken. Bind `127.0.0.1` only. Confirm with `curl` that the page returns 200. The URL path is the path under `docs/`:

`http://127.0.0.1:8765/ciec_requests/ciec_request_1.html`

Leave the server running.

## Show the page

The in-editor browser cannot reach this machine. Do not retry `browser_navigate` against `127.0.0.1` or a private IP.

Open the localhost URL with Cursor's helper so the port is forwarded and Simple Browser opens:

```bash
helper=$(find "$HOME/.cursor-server/bin" -path '*/helpers/browser.sh' -type f | head -1)
"$helper" "http://127.0.0.1:<port>/<path-under-docs>"
```

Then tell the user the localhost URL. If no window appeared, they can open that URL from the Ports panel or Simple Browser.

Say where the HTML file is and that `git status` does not list it.
