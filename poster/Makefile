TEX = main.tex
PDF = main.pdf
REF_TEX = corpus_references.tex
REF_PDF = corpus_references.pdf

.PHONY: all corpus-references-data clean

all: $(PDF) $(REF_PDF)

$(PDF): $(TEX) corpus-references-data
	latexmk -pdf -interaction=nonstopmode -file-line-error $(TEX)

corpus-references-data:
	python3 scripts/build_corpus_references.py

$(REF_PDF): $(REF_TEX) corpus-references-data
	latexmk -pdf -interaction=nonstopmode -file-line-error $(REF_TEX)

clean:
	latexmk -C $(TEX)
	latexmk -C $(REF_TEX)
