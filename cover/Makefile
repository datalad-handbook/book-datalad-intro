all: cover.pdf

%.pdf: %.svg
	inkscape --export-dpi=300 --export-filename "$@" "$<"

clean:
	rm -f *.pdf

.PHONY: all clean
