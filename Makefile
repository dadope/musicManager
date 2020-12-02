#just to have a makefile
install:
	pip3 install -r requirements.txt
	pip3 install .

run:
	pip3 install -r requirements.txt
	pip3 install .
	musicManager -c