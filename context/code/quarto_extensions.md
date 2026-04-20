# Quarto extensions in this repo

## The problem: extensions are project-local

Quarto extensions live in `_extensions/` inside each project directory (where `_quarto.yml` is). There is no supported environment variable, config setting, or global library that lets multiple projects share a single `_extensions/` directory. Symlinks under `_extensions/` are unreliable — Quarto's CLI does not consistently resolve them, and shortcodes in particular fail when loaded via symlink ([quarto-cli#9069](https://github.com/quarto-dev/quarto-cli/issues/9069), confirmed as late as January 2026).

In a monorepo with many report projects, the default approach — `quarto add <extension>` in each project — creates duplicate copies of extension source code that must be kept in sync manually. Any customization has to be propagated to every copy.

## The workaround: project-level `shortcodes:` and `filters:` keys

Quarto extensions are bundles that contribute features to project-level YAML keys that already exist independently. The `_extension.yml` `contributes:` block maps to these keys:

| `_extension.yml` contributes | Equivalent `_quarto.yml` key      | Accepts file paths? |
| ---------------------------- | --------------------------------- | ------------------- |
| `shortcodes:`                | `shortcodes:`                     | Yes                 |
| `filters:`                   | `filters:`                        | Yes (documented)    |
| `formats:` / templates       | `template:`, `template-partials:` | Yes                 |

When you use these keys directly in `_quarto.yml` with a file path (instead of an extension name), Quarto loads the Lua file without going through the `_extensions/` discovery mechanism at all. Paths are resolved relative to the project root — including `../` paths that point outside the project directory.

This was confirmed in [quarto-cli#14283](https://github.com/quarto-dev/quarto-cli/issues/14283) (milestone v1.10):

> shortcodes can be added to a project with minimal boilerplate, namely:
>
> ```yaml
> shortcodes:
>   - shortcodes.lua
> ```
>
> in the same way than custom filters. [...] all an extension does is to contribute features for options already available at the top level (filters, shortcodes, template, template-partials).

### Why CSS and other dependencies resolve correctly

The [Quarto Lua API](https://quarto.org/docs/extensions/lua-api.html) resolves dependency paths **relative to the Lua file calling the function**, not relative to the project root:

- `quarto.doc.add_html_dependency()` — `stylesheets` and `scripts` paths are relative to the calling Lua file
- `quarto.doc.include_file()` — path is relative to the Lua script calling the function
- `quarto.utils.resolve_path()` — computes full path to a file alongside the Lua script

So a shortcode Lua file at `lib/quarto_extensions/glossary/glossary.lua` that references `glossary.css` will find the CSS in the same directory, regardless of which project loaded the Lua file.

### Limitation: `revealjs-plugins`

The `revealjs-plugins` contribution type does not have an equivalent project-level YAML key. Extensions that contribute RevealJS plugins still require per-project `_extensions/` installation. This is not relevant to this repo's Quarto Manuscript reports.

## Our setup: `lib/quarto_extensions/`

Shared Quarto extension files live in `lib/quarto_extensions/`, organized by extension name:

```
lib/quarto_extensions/
└── glossary/
    ├── glossary.lua    # shortcode handlers (glossary, glossary-def)
    └── glossary.css    # hover popup and inline pill styling
```

Each report that uses an extension references it directly in `_quarto.yml`:

```yaml
# reports/<project>/_quarto.yml
shortcodes:
  - ../../lib/quarto_extensions/glossary/glossary.lua
```

Per-report term definitions (`glossary.yml`) stay in each report directory — different reports define different terms. The front matter in `index.qmd` points to this local file:

```yaml
glossary:
  path: glossary.yml
  popup: hover
```

### Adding an extension to a new report

1. Add the `shortcodes:` (or `filters:`) key to the report's `_quarto.yml` with the relative path to the Lua file in `lib/quarto_extensions/`.
2. If the extension needs per-report config (like `glossary.yml`), create that file in the report directory and reference it in the document front matter.

### Adding a new extension to the repo

1. Create a directory under `lib/quarto_extensions/<name>/` with the Lua and CSS/JS files.
2. Reference it from each report's `_quarto.yml` using the appropriate key (`shortcodes:`, `filters:`, etc.).
3. Do **not** use `quarto add` or create per-project `_extensions/` directories.

### Modifying an extension

Edit the files in `lib/quarto_extensions/<name>/`. The change takes effect for all reports on the next render — no sync or copy step needed.
