PYTHON ?= python

.PHONY: setup test session1 session2 notebook-smoke

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

session1:
	$(PYTHON) scripts/run_session1.py

session2:
	$(PYTHON) scripts/run_session2.py

notebook-smoke:
	$(PYTHON) scripts/notebook_smoke_test.py
