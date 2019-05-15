# Source, Executable, Includes, Library Defines
SRC    = main.c
OBJ    = $(SRC:.c=.o)
INCL_PATH = $(PWD)/../../src/state
#LIBS   =
EXE    = state_test

# Compiler, Linker Defines
CC      = /usr/bin/gcc
CFLAGS  = -ansi -pedantic -Wall -O2 -I$(INCL_PATH)
LIBPATH = -L.
LDFLAGS = -o $(EXE) $(LIBPATH) $(LIBS)
CFDEBUG = -ansi -pedantic -Wall -g -DDEBUG $(LDFLAGS)

default: $(EXE)

%.o: %.c
	$(CC) -c $(CFLAGS) $*.c

$(EXE): $(OBJ)
	$(CC) $(LDFLAGS) $(OBJ)

$(OBJ): $(INCL)

clean:
	rm $(OBJ) $(EXE)

test: $(EXE)
	./$(EXE)
