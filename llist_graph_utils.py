import sys
from pygraphviz import *
from pprint import pprint

# Global variables :
n_color = "#9ACEEB"
e_color = "#FCD975"
# For debugging :
debug = 1

def build_graph_from(obj, i):
  # "obj" is a dict
  final_graph = init_exec_point_graph()

  heapG = final_graph.get_subgraph("clusterHeap")
  if (debug):
    print("Heap state of execution point " + str(i) + " : ")
    if (len(obj["heap"]) <= 0):
      print("Empty heap")
    for k, v in obj["heap"].items():
      print(k)
      pprint(v)

  # Non-empty heap case
  heap = obj["heap"]
  if (len(heap) > 0):
    for k, v in heap.items():
      var_info = retrieve_heap_var_info(heap[k])
      if (var_info):
        heapG.add_node(var_info[0])
        newNode = heapG.get_node(var_info[0])
        newNode.attr["shape"] = "record"
        newNode.attr["width"] = 1
        newNode.attr["height"] = 1
        newNode.attr["label"] = ""

  graph_file_name = "graph" + str(i)
  output_graph(final_graph, graph_file_name)



def retrieve_heap_var_info(HeapVar):
  vInfo = []

  if (len(HeapVar) > 2):
    varInfo = HeapVar[2]
    address = varInfo[1]
    struct_type = varInfo[2]
    data_field = varInfo[3]
    next_field = varInfo[4]
    data_value = data_field[1][3]
    next_value = next_field[1][3]

    vInfo = [address, struct_type, data_value, next_value]

  else:
    # TODO : handle this case
    if (debug):
      print("HEAP VAR FREED")

  return vInfo



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

def output_graph(graph, name):
  graph.layout(prog="dot")
  #graph.draw("img/" + name + ".svg")
  graph.write("dots/" + name + ".dot")
  
