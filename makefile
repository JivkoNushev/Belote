FILES = client.py network.py server.py
CFLAGS = -Wall -pedantic

all: ${FILES}
	python client.py network.py 

server:
	start python server.py 

clean:
	rm *.o *.out

open:
	code client.py network.py server.py

OPEN:
	gedit client.py network.py server.py

run:
	python client.py network.py server.py
