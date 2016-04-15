import sys
from pygraphviz import *
from pprint import pprint
from collections import OrderedDict
import json
from pprint import pprint

# Global variables :
n_color = "#9ACEEB"
e_color = "#FCD975"
# For debugging :
debug = 0

def build_graph_from(obj, i):
  final_graph = init_exec_point_graph()

  # Heap cluster :
  heapG = final_graph.get_subgraph("clusterHeap")

  # Little hack to keep the initial ordering of the entries in 'heap'
  json_format = json.dumps(OrderedDict(obj["heap"]), sort_keys = True)
  heap = json.loads(json_format, object_pairs_hook = OrderedDict)

  # Non-empty heap case
  prev_node_vi = None
  if (len(heap) > 0):
    # Browse the keys in reverse order to keep the ordering of the llist
    for k in (sorted(heap.keys(), reverse=True)):
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
        # Setting the edge with the previous node :
        if prev_node_vi is not None:
          heapG.add_edge(str(prev_node_vi[0]), str(var_info[0]), style="filled")
        prev_node_vi = var_info
        # If the 'next' field of the current node points to NULL :
        # Last element of the LinkedList
        if var_info[-1] == "NULL":
          heapG.add_edge(str(var_info[0]), "NULL", style="filled")


  # Frames cluster :
  frameG = final_graph.get_subgraph("clusterFrames") 
  frames = obj["frames"]

  for frame in frames:
    # Create a frame subgraph for each stack frames
    frame_graph_name = "cluster_" + frame["func_name"]
    frameG.add_subgraph(name = frame_graph_name)
    # Getting the current frame subgraph
    current_frame_graph = frameG.get_subgraph(frame_graph_name)
    current_frame_graph.graph_attr["rankdir"] = "TB"
    current_frame_graph.graph_attr["label"] = str(frame["func_name"]) + " Function"
    # Dummy node (hack to link the cluster and avoir overlaps) :
    current_frame_graph.add_node("DUMMY_" + str(i))
    node_frame = current_frame_graph.get_node("DUMMY_" + str(i))
    node_frame.attr["shape"] = "point"
    node_frame.attr["style"] = "invis"
    # Getting the local vars in the right order :
    json_frame_vars = json.dumps(OrderedDict(frame["encoded_locals"]), sort_keys = True)
    frame_vars = json.loads(json_frame_vars, object_pairs_hook = OrderedDict)
    # Iterating over the local vars and fill the current frame sub graph
    prev_node_vi = None
    for k in (sorted(frame_vars.keys(), reverse=True)):
      var = frame_vars[k]
      var[:] = [x if x != "<UNINITIALIZED>" else "uninitialized" for x in var]
      var[:] = [x if x != "0x0" else "NULL" for x in var]
      # Create a new node for the var named "k"
      current_frame_graph.add_node(k)
      currNode = current_frame_graph.get_node(k)
      currNode.attr["rankdir"] = "BT"
      currNode.attr["shape"] = "record"
      currNode.attr["label"] = "Type : " + str(var[2]) + " | Name : " + str(k) + " | Value : " + str(var[3]) + " | Address : " + str(var[1])

      if prev_node_vi is not None:
        current_frame_graph.add_edge(str(prev_node_vi), str(k), style="invis")
      prev_node_vi = k
      # Making the pointer variables, point to their data on the heap :
      if (k == "head" and not str(var[3]) == "uninitialized"):
        final_graph.add_edge(str(k), str(var[3]), style = "filled")

  graph_file_name = "exec_point_" + str(i)
  output_graph(final_graph, graph_file_name)
  #gen_GIF()
      


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
    vInfo[:] = [x if x != "0x0" else "NULL" for x in vInfo]

  else:
    # TODO : handle this case
    if (debug):
      print("HEAP VAR FREED")

  return vInfo



def init_exec_point_graph():
  # Defining graph attributes :
  G = AGraph(strict=False, directed=True, rankdir="LR")
  #G.graph_attr["nodesep"] = 1.5
  G.graph_attr["rankdir"]  = "LR"
  G.graph_attr["rank"] = "same"

  # Defining the node attributes
  G.node_attr["color"] = n_color

  # Defining Frames cluster
  clusFrame = G.add_subgraph(name = "clusterFrames")
  clusFrame.graph_attr["rankdir"] = "TB"
  clusFrame.graph_attr["color"] = "grey"
  clusFrame.graph_attr["label"] = "Stack Frames"
  clusFrame.graph_attr["rank"] = "same"
  # Dummy node (hack to link the cluster and avoir overlaps) :
  clusFrame.add_node("DUMMY_FRAME")
  node_frame = clusFrame.get_node("DUMMY_FRAME")
  node_frame.attr["shape"] = "point"
  node_frame.attr["style"] = "invis"

  # Defining Heap cluster
  clusHeap = G.add_subgraph(name = "clusterHeap")
  clusHeap.graph_attr["rankdir"] = "LR"
  clusHeap.graph_attr["color"] = "indigo"
  clusHeap.graph_attr["label"] = "Heap"
  clusHeap.graph_attr["rank"] = "same"
  clusHeap.node_attr["fixedsize"] = "False"
  # Dummy node (hack to link the cluster and avoir overlaps) :
  clusHeap.add_node("DUMMY_HEAP")
  node_heap = clusHeap.get_node("DUMMY_HEAP")
  node_heap.attr["shape"] = "point"
  node_heap.attr["style"] = "invis"

  # Link the subgraphs together to fix position :
  G.add_edge("DUMMY_FRAME", "DUMMY_HEAP", style = "invis")

  return G

"""
def gen_GIF():
  file_names = sorted((fn for fn in os.listdir("img") if fn.endswith(".svg")))
  images = [Image.open(fn) for fn in file_names]
  size = (500, 500)
  for im in images:
    im.thumbnail(size, Image.ANTIALIAS)
  print(writeGif.__doc__)
  filename = "my_gif.GIF"
  writeGif(filename, images, duration=0.2)
"""

def output_graph(graph, name):
  graph.layout(prog="dot")
  graph.draw("img/" + name + ".svg")
  graph.write("dots/" + name + ".dot")
  
