clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -rf build

test: clean
	pytest

install: clean
	pip install .

install-test: clean
	pip install .[test]

install-dev: clean
	pip install -e ".[test,dev]"