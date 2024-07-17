.PHONY: all install test clean

lint:
	black -l 120 *.py
