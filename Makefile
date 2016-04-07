all: graphs

graphs: 
	python generate_graph_from_traces.py

.PHONY: clean

clean:
	rm -f img/* dots/*

