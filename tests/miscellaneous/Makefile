all-traces: thesis_LinkedList.trace

%.vgtrace: %.c ../../valgrind-3.11.0/inst/bin/valgrind
	@gcc -ggdb -O0 -fno-omit-frame-pointer $< -o $(basename $@).o
	@../../valgrind-3.11.0/inst/bin/valgrind --tool=memcheck --source-filename=$< --trace-filename=$(basename $<).vgtrace ./$(basename $<).o || true

%.vgtrace: %.cpp ../valgrind-3.11.0/inst/bin/valgrind
	@g++ -ggdb -O0 -fno-omit-frame-pointer $< -o $(basename $@)
	@../valgrind-3.11.0/inst/bin/valgrind --tool=memcheck --source-filename=$< --trace-filename=$(basename $<).vgtrace ./$(basename $<) || true

%.trace: %.vgtrace ../../vg_to_opt_trace.py
	#python2.7 ../../vg_to_opt_trace.py --create_jsvar=trace $(basename $<) > $(basename $<).trace || true
	python2.7 ../../generate_traces.py $(basename $<) > $(basename $<).trace || true

clean:
	rm -f *.trace *.vgtrace *.out *.o
