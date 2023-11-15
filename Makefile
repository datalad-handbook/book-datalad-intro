latex: src/sphinx src/handbook/docs
	# get a clean build
	rm -rf src/sphinx/*
	rm -rf src/handbook/docs/_build
	$(MAKE) -C src/handbook latex
	# take anything that sphinx produced verbatim, but not java script
	rm -rf src/handbook/docs/_build/latex/_static
	cp src/handbook/docs/_build/latex/* src/sphinx/
	# but kill any figures/images, we want dedicated variants for all of them
	# and avoid the churn caused by sphinx not creating them reproducibly
	rm src/sphinx/*.pdf src/sphinx/*.png

src/sphinx:
	mkdir -p $@

.PHONY: latex
