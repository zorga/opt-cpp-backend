all: graphs

graphs: 
	python generate_graph_from_traces.py tests/miscellaneous/thesis_LinkedList.trace

.PHONY: clean

clean:
	rm -f img/* dots/*

