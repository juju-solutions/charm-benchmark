PY := venv/bin/python
# If the bin version does not exist look in venv/local/bin
ifeq ($(wildcard venv/bin/pip),)
  PIP = venv/local/bin/pip
else
  PIP = venv/bin/pip
endif
# If the bin version does not exist look in venv/local/bin
ifeq ($(wildcard venv/bin/nosetests),)
  NOSE = venv/local/bin/nosetests
else
  NOSE = venv/bin/nosetests
endif

PROJECT=charmbenchmark

# ###########
# Build
# ###########

.PHONY: install
install: venv develop

venv: $(PY)
$(PY):
	virtualenv venv

.PHONY: clean_all
clean_all: clean clean_venv

.PHONY: clean_venv
clean_venv:
	rm -rf venv

.PHONY: clean
clean:
	rm -rf MANIFEST dist/* $(PROJECT).egg-info .coverage
	find . -name '*.pyc' -delete
	rm -rf venv

develop: lib/python*/site-packages/$(PROJECT).egg-link
lib/python*/site-packages/$(PROJECT).egg-link:
	$(PY) setup.py develop

.PHONY: sysdeps
sysdeps:
	sudo apt-get $(shell tty -s || echo -y) install python-dev juju-core bzr python-setuptools

docs:
	- [ -z "`dpkg -l | grep python-sphinx`" ] && sudo apt-get install python-sphinx -y
	- [ -z "`dpkg -l | grep python-pip`" ] && sudo apt-get install python-pip -y
	- [ -z "`pip list | grep -i sphinx-pypi-upload`" ] && sudo pip install sphinx-pypi-upload
	cd docs && make html && cd -
.PHONY: docs

release: docs
	python setup.py sdist upload upload_sphinx

# ###########
# Develop
# ###########

$(NOSE): $(PY)
	$(PIP) install -r test-requires.txt

.PHONY: test
test: $(NOSE)
	make py3test

.PHONY: unit_test
unit_test: $(NOSE)
	make ARGS="-e functional" py3test

.PHONY: functional_test
functional_test: $(NOSE)
	make ARGS="tests/functional" py3test

# This is a private target used to get around finding nose in different paths.
# Do not call this manually, just use make test.
.PHONY: py3test
py3test:
	@echo Testing Python 3...
	@$(NOSE) --nologcapture $(ARGS)

.PHONY: coverage
coverage: $(NOSE)
	@echo Testing with coverage...
	@$(NOSE) --nologcapture --with-coverage --cover-package=$(PROJECT) --cover-package=$(PROJECT).cli

.PHONY: lint
lint:
	@find $(sources) -type f \( -iname '*.py' ! -iname '__init__.py' ! -iwholename '*venv/*' \) -print0 | xargs -r0 flake8

.PHONY: check
check: test lint

.PHONY: all
all: clean venv coverage lint
