FILES = client.py network.py server.py player.py

all:
	python client.py&

server:
	CMD /C start python server.py

run:
	make
	make
	make
	make

open:
	code ${FILES}

OPEN:
	gedit ${FILES}


