
all:
	python weio\__init__.py

install:
	python setup.py install

dep:
	pip install numpy pandas


help:
	echo "Available rules:"
	echo "   all        run the standalone program"
	echo "   install    install the python package in the system" 
	echo "   dep        download the dependencies " 

test:all


