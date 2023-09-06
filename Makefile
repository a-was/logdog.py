export PYTHONPATH := $(CURDIR)

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

test: ## Run tests
	pytest

setup: ## Install tools for building
	pip install -U setuptools build twine

build: ## Build package
	@read -p "Please specify build version (X.Y.Z format): " VERSION && \
	echo $$VERSION > VERSION

	python -m build --sdist --wheel --outdir dist/
	@rm VERSION

publish: ## Publish build
	python -m twine dist/*

.PHONY: test setup build publish
