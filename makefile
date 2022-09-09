FILES = client.py network.py server.py

all:
	python client.py

server:
	CMD /C start python server.py

open:
	code ${FILES}

OPEN:
	gedit ${FILES}

run:
	python client.py network.py server.py
