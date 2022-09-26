<<<<<<< HEAD
FILES = client.py network.py server.py player.py game.py card.py ui.py
=======
FILES = client.py network.py server.py player.py game.py card.py
>>>>>>> 63aadb6c9ceb074bbf7cf3a172d51458f6fc1493

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


