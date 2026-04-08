all: clean render

clean:
    uv run python -m lib.just.clean

render path_qmd="":
    uv run python -m lib.just.render {{ path_qmd }}

today := `date +%Y%m%d`

draft path_qmd="index.qmd":
    uv run quarto render {{ path_qmd }} --to docx -M fig-dpi:300 --output {{ if path_qmd == "index.qmd" { "report_draft_" + today + ".docx" } else { file_stem(path_qmd) + "_" + today + ".docx" } }}

typeset_name := "report_" + today + ".icml"

typeset:
    uv run quarto render index.qmd --to icml --output {{ typeset_name }}

publish:
    uv run python -m lib.just.publish

diff label="":
    uv run python -m lib.just.diff {{ label }}
