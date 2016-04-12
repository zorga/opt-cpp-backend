import sys
from pygraphviz import *
from pprint import pprint

# Global variables :
n_color = "#9ACEEB"
e_color = "#FCD975"
# For debugging :
debug = 0

def build_graph_from(obj, i):
  final_graph = init_exec_point_graph()

  heapG = final_graph.get_subgraph("clusterHeap")
  heapG.graph_attr["rankdir"] = "LR"

  # Only for debugging purposes...
  if (debug):
    print("Heap state of execution point " + str(i) + " : ")
    if (len(obj["heap"]) <= 0):
      print("Empty heap")
    for k, v in obj["heap"].items():
      print(k)
      pprint(v)

  # Non-empty heap case
  heap = obj["heap"]
  prev_node_vi = None
  if (len(heap) > 0):
    for k, v in heap.items().reverse():
      # If the heap of the current exec_point is not empty, call the
      # 'retrieve_heap_var' function to get the informations about the data on the heap
      # and put them into the 'var_info' list.
      # The element of this list are used to compose the nodes of the graph
      # Only the heap graph for now
      var_info = retrieve_heap_var_info(heap[k])
      if (var_info):
        heapG.add_node(var_info[0])
        newNode = heapG.get_node(var_info[0])
        newNode.attr["rankdir"] = "BT"
        newNode.attr["shape"] = "record"
        newNode.attr["label"] = str(var_info[1]) + " | Data : " + str(var_info[2]) + " | Address :\\n " + str(var_info[0]) + " | next : " + str(var_info[3])
        if prev_node_vi is not None:
          heapG.add_edge(str(prev_node_vi[0]), str(var_info[0]), style="filled")
        prev_node_vi = var_info

  graph_file_name = "exec_point_" + str(i)
  output_graph(final_graph, graph_file_name)



def retrieve_heap_var_info(HeapVar):
  vInfo = []

  # It is a bit hard to understand what's going on here but I simply get the
  # information I need out of the exec_point in the .trace file.
  # Could be better written later ?
  if (len(HeapVar) > 2):
    varInfo = HeapVar[2]
    address = varInfo[1]
    struct_type = varInfo[2]
    data_field = varInfo[3]
    next_field = varInfo[4]
    data_value = data_field[1][3]
    next_value = next_field[1][3]

    # Getting the list to return, ready :
    vInfo = [address, struct_type, data_value, next_value]

    # from : http://stackoverflow.com/questions/24201926/
    # weird : "<UNINITIALIZED> string doesn't fit in the node labels
    # the "<UNINITIALIZED>" string seems not accepted by the 'dot' language
    vInfo[:] = [x if x != "<UNINITIALIZED>" else "uninitialized" for x in vInfo]

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

  # Defining the node attributes
  G.node_attr["color"] = n_color

  # Defining Frames cluster
  clusFrame = G.add_subgraph(name = "clusterFrames")
  clusFrame.graph_attr["rankdir"] = "TB"
  clusFrame.graph_attr["color"] = "grey"
  clusFrame.graph_attr["label"] = "Stack Frames"

  # Defining Heap cluster
  clusHeap = G.add_subgraph(name = "clusterHeap")
  clusHeap.graph_attr["rankdir"] = "LR"
  clusHeap.graph_attr["color"] = "indigo"
  clusHeap.graph_attr["label"] = "Heap"
  clusHeap.node_attr["fixedsize"] = "True"

  return G

def output_graph(graph, name):
  graph.layout(prog="dot")
  graph.draw("img/" + name + ".svg")
  graph.write("dots/" + name + ".dot")
  
