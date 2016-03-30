LLISTS = LinkedLists
DEPS_LLISTS = $(LLISTS)/thesis_LinkedLists.h
VG = ../valgrind-3.11.0/inst/bin/valgrind
CFLAGS = -ggdb -O0 -fno-omit-frame-pointer
CC = @gcc
PYTHON = python2.7
SCRIPT = ../vg_to_opt_trace.py --create_jsvar=trace

all-traces: llists

llists: $(LLISTS)/llTests.trace

others: miscellaneous/thesis_nicolas.trace

%.vgtrace: %.c $(VG)
	$(CC) $(CFLAGS) $< -o $(basename $@).o
	@$(VG) --tool=memcheck --source-filename=$< --trace-filename=$(basename $<).vgtrace ./$(basename $<).o || true

# Generate the final trace files :

%.trace: %.vgtrace ../vg_to_opt_trace.py
	$(PYTHON) $(SCRIPT) $(basename $<) > $(basename $<).trace || true

.PHONY: clean

clean:
	rm -f */*.trace */*.vgtrace */*.out */*.o

