.PHONY: install test test-smoke test-wap test-regression \
        lint mypy ruff-format ruff-check format \
        report clean help

PYTHON     := python
PYTEST     := pytest
SRC_DIRS   := pages utils tests
REPORT_DIR := reports

# ------------------------------------------------------------------------------
# Install
# ------------------------------------------------------------------------------

install:
	pip install -r requirements.txt
	pip install mypy ruff

# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

test:
	$(PYTEST)

report:
	@mkdir -p $(REPORT_DIR)
	$(PYTEST) --html=$(REPORT_DIR)/report.html --self-contained-html
	@echo "Report generated: $(REPORT_DIR)/report.html"

# ------------------------------------------------------------------------------
# Quality checks
# ------------------------------------------------------------------------------

mypy:
	@echo ">>> Running mypy (type checking)..."
	mypy $(SRC_DIRS) \
		--ignore-missing-imports \
		--exclude __pycache__

# ------------------------------------------------------------------------------
# Auto-format
# ------------------------------------------------------------------------------

ruff-format:
	@echo ">>> Formatting with ruff..."
	$(PYTHON) -m ruff format $(SRC_DIRS)

ruff-check:
	@echo ">>> Linting with ruff..."
	$(PYTHON) -m ruff check $(SRC_DIRS) --fix

format: ruff-format ruff-check
	@echo ">>> Code formatted!"

# ------------------------------------------------------------------------------
# Clean
# ------------------------------------------------------------------------------

clean:
	@echo ">>> Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache  -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf $(REPORT_DIR)
	@echo ">>> Clean done!"
# ------------------------------------------------------------------------------
# Help
# ------------------------------------------------------------------------------

help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  install         Install dependencies + dev tools"
	@echo ""
	@echo "  test            Run all tests"
	@echo "  test-smoke      Run smoke tests only"
	@echo "  test-wap        Run WAP tests only"
	@echo "  test-regression Run regression suite"
	@echo "  report          Run all tests + generate HTML report"
	@echo ""
	@echo "  mypy            Type checking"
	@echo "  format          Format + lint with ruff"
	@echo ""
	@echo "  clean           Remove reports, screenshots, caches"
	@echo ""
