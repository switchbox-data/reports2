all: clean render

# Delete all caches
clean:
  rm -rf .quarto docs/*_files/ notebooks/*_files/ notebooks/*.html \
         notebooks/*.ipynb notebooks/*.rmarkdown

# Render quarto project
render:
  quarto render .

draft:
  quarto render index.qmd --to docx --output report_draft.docx

typeset:
  quarto render index.qmd --to icml

publish:
  bash -c 'parent_folder=$(basename $(pwd)); pub_path="../../docs/$parent_folder"; \
  rm -rf "$pub_path" && mkdir -p "$pub_path" && cp -r docs/* "$pub_path"'
