all: clean render

# Delete all caches
clean:
  rm -rf .quarto docs/*_files/ notebooks/*_files/ notebooks/*.html \
         notebooks/*.ipynb notebooks/*.rmarkdown

# Render quarto project
render:
  quarto render .

today := `date +%Y%m%d`
draft_name := "report_draft_" + today + ".docx"
draft:
  quarto render index.qmd --to docx --output {{draft_name}}

typeset_name := "report_" + today + ".icml"
typeset:
  quarto render index.qmd --to icml --output {{typeset_name}}

publish:
  bash -c 'parent_folder=$(basename $(pwd)); pub_path="../../docs/$parent_folder"; \
  rm -rf "$pub_path" && mkdir -p "$pub_path" && cp -r docs/* "$pub_path"'
