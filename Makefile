.PHONY: test
test:
	python3 -m unittest discover tests -v

.PHONY: loaddb
loaddb:
	python3 -m flashserver.data_loader.loader

.PHONY: run
run:
	python3 -m flashserver.flashserver
