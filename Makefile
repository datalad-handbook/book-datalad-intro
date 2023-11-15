all: figures main.pdf

main.pdf: figures *.tex parts/* src/sphinx/*
	mkdir -p build
	# use TEXINPUTS to locate needed ressource (figures) in this repo,
	# or fall back on the source if needed
	cd build && BOOK_REPO_ROOT=$$(pwd)/.. TEXINPUTS=.:..:../figures//:../src/sphinx//:../src/handbook/artwork//:../src/handbook/docs/artwork//: latexmk -r ../src/sphinx/latexmkrc -pdf main.tex
	mv build/main.pdf main.pdf

book.pdf: cover/cover.svg main.pdf
	$(MAKE) -C cover cover.pdf
	pdftk cover/cover.pdf main.pdf cat output $@

figures:
	$(MAKE) -C figures

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

clean:
	rm -rf build main.pdf
	$(MAKE) -C cover clean
	$(MAKE) -C figures clean

src/sphinx:
	mkdir -p $@

split: code/split_handbook.py src/sphinx/dataladhandbook.tex
	mkdir -p parts
	python $<

# Do the full dance of pulling in an upstream change, through all branches
UPGRAYEDD:
	# we need datalad further down, test here for availability
	datalad --version > /dev/null
	# run scripts need 'python'
	python --version > /dev/null
	git checkout upstream
	git -C src/handbook pull
	git add src/handbook
	git commit -m "Upstream update" || true
	git clean -df
	datalad run -i src/handbook -o src/sphinx make latex
	git checkout upstream-processed
	git merge upstream
	datalad run make split
	git checkout main
	git merge upstream-processed

# This can be used to sync the upstream* branch from origin. It is
# assumed that all potentialy existing local changes are pushed, or
# can be thrown away. One would typically use this (only) after not
# having worked locally for some time.
FORCE-SYNC-ORIGIN:
	git fetch origin
	git checkout upstream
	git reset --hard origin/upstream
	git checkout upstream-processed
	git reset --hard origin/upstream-processed
	git checkout main

.PHONY: all latex split figures clean UPGRAYEDD
