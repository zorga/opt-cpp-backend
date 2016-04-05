import sys
from pygraphviz import *

# Global variables :
n_color = "#9ACEEB"
e_color = "#FCD975"

def build_graph_from(obj, i):
  G = init_exec_point_graph()
  G.layout(prog="dot")
  graph_file_name = "graph " + str(i) + ".svg"
  G.draw(graph_file_name)
  graph_src = "source " + str(i) + ".dot"
  G.write(graph_src)
  
  return 0


def add_node_from_heap_var(heap_graph, var_info):
  heap_graph.add_node(var_info["addr"])
  n = graph.get_node(var_info["addr"])
  n.attr["shape"] = "record"
  n.attr["width"] = 1
  n.attr["height"] = 1

  label = "" + var_info["type"] + " | Data : " + var_info["data"] + " | Address :\\n " + var_info["addr"] + " | next : " + var_info["next"]

  n.attr["label"] = label

  return heap_graph

def init_exec_point_graph():
  # Defining graph attributes :
  G = AGraph(strict=False, directed=True, rankdir="LR")
  G.graph_attr["nodesep"] = 1.5

  # Defining edge attributes :
  G.edge_attr["color"] = e_color
  G.edge_attr["arrowsize"] = 1

  # Defining the node attributes
  G.node_attr["color"] = n_color

  # Defining Frames cluster
  clusFrame = G.add_subgraph(name = "clusterFrames")
  clusFrame.graph_attr["rankdir"] = "TB"
  clusFrame.graph_attr["color"] = "grey"
  clusFrame.graph_attr["label"] = "Stack Frames"
  clusFrame.node_attr["style"] = "filled"

  # Defining Heap cluster
  clusHeap = G.add_subgraph(name = "clusterHeap")
  clusHeap.graph_attr["rankdir"] = "LR"
  clusHeap.graph_attr["color"] = "indigo"
  clusHeap.graph_attr["label"] = "Heap"

  return G
  
