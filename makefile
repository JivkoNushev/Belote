FILES = client.py network.py server.py player.py game.py card.py ui.py

all:
	python client.py&

l:
	python3 client.py&

server:
	CMD /C start python server.py

serverl:
	python3 server.py&

run:
	make
	make
	make
	make

runl:
	make l
	make l
	make l
	make l

open:
	code ${FILES}

OPEN:
	gedit ${FILES}


