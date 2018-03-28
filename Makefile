.PHONY: help install tests coverage coverage-html

.DEFAULT_GOAL := help

help: ## List all the command helps.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install.
	@echo "Generating settings.ini..."
	@cp -n settings.ini.dist settings.ini

tests: ## Run tests.
	@pytest -c pytest.ini

coverage: ## Run tests with coverage.
	@pytest -c pytest.ini --cov=rerwatcher

coverage-html: ## Run tests with html format coverage.
	@pytest -c pytest.ini --cov=rerwatcher --cov-report html
