
all: test

install:
	python setup.py install

dep:
	python -m pip install -r requirements.txt


help:
	echo "Available rules:"
	echo "   all        run the standalone program"
	echo "   install    install the python package in the system" 
	echo "   dep        download the dependencies " 

test:
	python -m unittest discover -v


