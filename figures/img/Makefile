all: figures

figures: \
  data_origin_bw.pdf \
  dataset_modules.pdf \
  decentralized_publishing_bw.pdf \
  yoda.pdf

# black&white figures are local
%_bw.pdf: %_bw.svg
	inkscape --export-dpi=300 --export-filename "$@" "$<"

%.pdf: ../../src/handbook/docs/artwork/src/img/%.svg
	inkscape --export-dpi=300 --export-filename "$@" "$<"

clean:
	-rm *.pdf

.PHONY: all figures clean
