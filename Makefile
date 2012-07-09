.PHONY: all clean

all:
	python setup.py build_ext --inplace

clean:
	rm -rf build
	rm -rf examples/test_*
	find . -name "*.pyc" | xargs rm -f

