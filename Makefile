.PHONY: help run tests coverage coverage-html

.DEFAULT_GOAL := help

help: ## List all the command helps.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

run: ## Run RERWatcher.
	@python rerwatcher

tests: ## Run tests.
	@pytest tests/ -x

coverage: ## Run tests with coverage.
	@pytest tests/ --cov=transilienwatcher

coverage-html: ## Run tests with html format coverage.
	@pytest tests/ --cov=transilienwatcher --cov-report html
