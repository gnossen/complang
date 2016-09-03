.PHONY: test
test:
	PYTHONPATH=src py.test test --cov=src --cov-report term-missing
