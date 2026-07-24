all: clean render

clean:
    uv run python -m lib.just.clean

render path_qmd="":
    uv run python -m lib.just.render {{ path_qmd }}

draft path_qmd="index.qmd":
    uv run python -m lib.just.draft {{ path_qmd }}

typeset path_qmd="":
    uv run python -m lib.just.typeset {{ path_qmd }}

publish:
    uv run python -m lib.just.publish

diff label="":
    uv run python -m lib.just.diff {{ label }}
