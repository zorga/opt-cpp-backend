##############################################
########### MACROS DEFINITIONS ###############
##############################################

### MACROS FOR THE LINKED_LIST TESTS ###

DEPS_LLISTS = LinkedLists/thesis_LinkedList.h
OBJ_LLISTS = LinkedLists/thesis_LinkedList.o

### MACROS FOR COMPILATION AND VALGRIND ###

VG = /home/nico/coding/opt-cpp-backend/valgrind-3.11.0/inst/bin/valgrind
#VG = ../valgrind-3.11.0/inst/bin/valgrind
CFLAGS = -ggdb -O0 -fno-omit-frame-pointer
CC = @gcc

### MACROS FOR THE SCRIPT ###

PYTHON = python2.7
SCRIPT = ../vg_to_opt_trace.py
SCRIPT_CALL = ../vg_to_opt_trace.py --create_jsvar=trace

##############################################
######### END OF MACROS DEFINITION ###########
##############################################

# This is the target called by default when typing only 'make' :
all-traces: llists 

########### TRACES FOR LINKED_LISTS ##########

llists: LinkedLists/llTests.trace

LinkedLists/llTests.trace: LinkedLists/llTests.vgtrace $(SCRIPT)
	@$(PYTHON) $(SCRIPT_CALL) $(basename $<) > $(basename $<).trace || true

LinkedLists/llTests.vgtrace: LinkedLists/llTests.c $(OBJ_LLISTS)
	$(CC) $(CFLAGS) $< -o $(basename $@).o $(OBJ_LLISTS)
	@$(VG) --tool=memcheck --source-filename=$< --trace-filename=$(basename $<).vgtrace ./$(basename $<).o || true

LinkedLists/thesis_LinkedList.o: LinkedLists/thesis_LinkedList.c $(DEPS_LLISTS)
	$(CC) $(CFLAGS) -c $< -o $(basename $@).o

######### TRACES FOR ALL FILES ###############
# Generate the Valgrind trace files :

%.vgtrace: %.c $(VG)
	$(CC) $(CFLAGS) $< -o $(basename $@).o
	@$(VG) --tool=memcheck --source-filename=$< --trace-filename=$(basename $<).vgtrace ./$(basename $<).o || true

# Generate the final trace files :

%.trace: %.vgtrace $(SCRIPT)
	@$(PYTHON) $(SCRIPT_CALL) $(basename $<) > $(basename $<).trace || true

##############################################

.PHONY: clean

clean:
	rm -f */*.trace */*.vgtrace */*.out */*.o *.o *.trace *.vgtrace *.out

