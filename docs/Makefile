default: diagrams

dotfiles=$(shell ls *.dot | cut -d "." -f 1)

%.pdf: %.dot
	dot $< -Tpdf > $@

diagrams: $(dotfiles).pdf
