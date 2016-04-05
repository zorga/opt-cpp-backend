import sys
from pygraphviz import *

def main():
  # Useful vars
  n_color = "#9ACEEB"
  e_color = "#FCD975"
  nodelab = "node_t\ndata : "
  data1 = 17
  data2 = 18

  # Defining graph attributes
  G = AGraph()
  G = AGraph(strict=False, directed=True, rankdir="LR")
  G.graph_attr["nodesep"] = 1.5

  # Defining edge attributes
  G.edge_attr["color"] = e_color
  G.edge_attr["arrowsize"] = 1

  # Defining the node attributes
  G.node_attr["color"] = n_color

  # Defining nodes
  G.add_node("head")
  head = G.get_node("head")
  head.attr["shape"] = "record"
  head.attr["width"] = 1
  head.attr["height"] = 1
  head.attr["label"] = " pointer | head | Value : 0x51D7040 | Address : 0xFFF0003E8 "

  G.add_node("0x51D7090")
  n = G.get_node("0x51D7090")
  n.attr["shape"] = "record"
  n.attr["width"] = 1
  n.attr["height"] = 1
  n.attr["label"] = "node_t | Data : 17 | Address :\\n 0x51D7090 | next"
  
  G.add_node("0x51D7040")
  m = G.get_node("0x51D7040")
  m.attr["shape"] = "record"
  m.attr["width"] = 1
  m.attr["height"] = 1
  m.attr["label"] = "node_t | Data : 18 | Address :\\n 0x51D7040 | next"

  G.add_node("letter", shape = "record", label = "char | letter | Value : c | Address : 0x8989899 ")

  # Defining edges
  G.add_edge("head", "0x51D7090")
  G.add_edge("0x51D7090", "0x51D7040")

  # Frames cluster
  clusVar = G.add_subgraph(["head", "letter"], name = "clusterFrames")
  clusVar.graph_attr["rankdir"] = "TB"
  clusVar.graph_attr["color"] = "grey"
  clusVar.node_attr["syle"] = "filled"
  clusVar.graph_attr["label"] = "Stack Frames"
  
  # Heap cluster
  clusHeap = G.add_subgraph(["0x51D7090", "0x51D7040"], name = "clusterHeap")
  clusHeap.graph_attr["rankdir"] = "LR"
  clusHeap.graph_attr["color"] = "indigo"
  clusHeap.graph_attr["label"] = "Heap"
  
  G.layout(prog="dot")
  G.draw("graph.svg")
  # Output graph source code
  G.write("source.dot")

if __name__ == "__main__":
  main()
