PYTHON ?= python3
PIP ?= $(PYTHON) -m pip
AWM ?= $(PYTHON) -m awm

.PHONY: help install test lint validate generate check

help:
	@echo "Targets:"
	@echo "  install   install pinned runtime and test dependencies"
	@echo "  validate  JSON Schema validation of model/"
	@echo "  lint      semantic lint of model/"
	@echo "  generate  write generated/ from model/"
	@echo "  test      run the pytest suite"
	@echo "  check     validate + lint + tests + generated-drift check"

install:
	$(PIP) install -r requirements-dev.txt

validate:
	$(AWM) validate

lint:
	$(AWM) lint

generate:
	$(AWM) generate

test:
	$(PYTHON) -m pytest

check:
	$(AWM) check
	$(PYTHON) -m pytest
