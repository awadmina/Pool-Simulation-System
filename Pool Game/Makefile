#submittion for A4 code
#written by Mina Awad, 1175348
#Export the shared library using "export LD_LIBRARY_PATH=/path/to/libraries:$LD_LIBRARY_PATH"
#To compile the code please type in "make" as a command line argument in the terminal
#To run the code please type "make" in command line then enter "python3 server.py 55348"


CC = clang
CFLAGS = -Wall -std=c99 -pedantic
PYTHON_INCLUDE = /usr/include/python3.11
PYTHON_LIB = /usr/lib/python3.11
PYTHON_VERSION = 3.11

all:	_phylib.so 

clean:
	rm -f *.o *.so *.exe *.svg phylib_wrap.c phylib.py -r __pycache__ 

phylib.o:  phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -fPIC -o phylib.o

libphylib.so: phylib.o
	$(CC) phylib.o -shared -o libphylib.so

phylib_wrap.c: phylib.i 
	swig -python phylib.i

phylib.py: phylib.i phylib.h phylib.c
	swig -python -o $@ $<

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I$(PYTHON_INCLUDE) -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) phylib_wrap.o libphylib.so -shared -L. -L$(PYTHON_LIB) -lpython$(PYTHON_VERSION) -lphylib -o _phylib.so


