import sys
from pygraphviz import *
from pprint import pprint

# Global variables :
n_color = "#9ACEEB"
e_color = "#FCD975"

def build_graph_from(obj, i):
  final_graph = init_exec_point_graph()

  heapG = final_graph.get_subgraph("clusterHeap")
  if (len(obj["heap"]) > 0):
    for k in obj["heap"]:
      heapG = add_node_from_heap_var(heapG, obj["heap"][k])
  final_graph.add_subgraph(heapG)

  graph_file_name = "graph" + str(i)
  output_graph(final_graph, graph_file_name)



def output_graph(graph, name):
  graph.layout(prog="dot")
  graph.draw("img/" + name + ".svg")
  graph.write("dots/" + name + ".dot")
  
  

def add_node_from_heap_var(heap_graph, var):
  if (len(var) > 2):
    varInfo = var[2]
    address = varInfo[1]
    struct_type = varInfo[2]
    data_field = varInfo[3]
    next_field = varInfo[4]
    data_value = data_field[1][3]
    next_value = next_field[1][3]

    heap_graph.add_node(address) 
    n = heap_graph.get_node(address)
    n.attr["shape"] = "record"
    n.attr["width"] = 1
    n.attr["height"] = 1
    label = struct_type + " | Data : " + str(data_value) + " | Address :\\n " + address
    label = label + " | next : " + str(next_value)
    n.attr["label"] = label

  else:
    pass

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
  
