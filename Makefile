#! /usr/bin/make -f

NOSETESTS = nosetests test -v
nosetests_cmd = $(NOSETESTS) ${NOSETESTS_OPTS}

.PHONY: checks
checks:
	PYTHONPATH=. $(PYTHON) checks/compare_pseudo-pkgs_lists.py

.PHONY: tests
tests:
	$(nosetests_cmd)

coverage: NOSETESTS_OPTS += --with-coverage --cover-package=reportbug
coverage:
	$(nosetests_cmd)

codechecks: pep8 pyflakes pylint

pep8:
	pep8 --verbose --repeat --show-source --filename=*.py,reportbug,querybts . --statistics

pyflakes:
	pyflakes . bin/*

pylint:
	pylint --output-format=colorized  bin/* reportbug/ checks/* test/ setup.py