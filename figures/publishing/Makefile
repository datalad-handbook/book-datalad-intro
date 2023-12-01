all: figures

figures: \
  publishing_network_publishparts2_bw.pdf \
  startingpoint_bw.pdf

# black&white figures are local
%_bw.pdf: %_bw.svg
	inkscape --export-dpi=300 --export-filename "$@" "$<"

%.pdf: ../../src/handbook/docs/artwork/src/publishing/%.svg
	inkscape --export-dpi=300 --export-filename "$@" "$<"

clean:
	-rm *.pdf

.PHONY: all figures clean
