install:
	pip3 install -r requirements.txt
	pip3 install .

run:
	pip3 install -r requirements.txt
	pip3 install .
	musicManager -c

test:
	pip3 install -r requirements.txt
	pip3 install .

	rm -rf ~/.musicManager/
	musicManager -c