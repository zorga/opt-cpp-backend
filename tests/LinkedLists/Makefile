### MACROS FOR THE LINKED_LIST TESTS ###

DEPS_LLISTS = thesis_LinkedList.h
OBJ_LLISTS = thesis_LinkedList.o

### MACROS FOR COMPILATION AND VALGRIND ###

VG = ../../valgrind-3.11.0/inst/bin/valgrind --tool=memcheck
CFLAGS = -ggdb -O0 -fno-omit-frame-pointer
CC = @gcc

### MACROS FOR THE SCRIPT ###

PYTHON = python2.7
SCRIPT = ../../vg_to_opt_trace.py
SCRIPT_CALL = $(SCRIPT) --create_jsvar=trace

llists: llTests.trace

llTests.trace: llTests.vgtrace $(SCRIPT)
	$(PYTHON) $(SCRIPT_CALL) $(basename $<) > $(basename $<).trace || true

llTests.vgtrace: llTests.c $(OBJ_LLISTS)
	$(CC) $(CFLAGS) $< -o $(basename $@).o $(OBJ_LLISTS)
	@$(VG) --source-filename=$< --trace-filename=$(basename $<).vgtrace ./$(basename $<).o || true

thesis_LinkedList.o: thesis_LinkedList.c $(DEPS_LLISTS)
	$(CC) $(CFLAGS) -c $< -o $(basename $@).o

.PHONY: clean

clean:
	rm -f *.o *.trace *.vgtrace *.out

