#!/usr/bin/env python2
import sys
from pygraphviz import *
from pprint import pprint
from collections import OrderedDict
import json
import random
from pprint import pprint

# For debugging :
debug = 0



def build_graph_from(obj, i):
  """
  This function builds the graphics representation of an execution point and output the
  source-code of the graph and the graph itself in SVG format.

  Args:
    obj (dict): a dictionnary describing the current execution point

    i (int): The sequence number of the current execution point

  """
  final_graph = init_exec_point_graph()

  # getting the heap cluster :
  heapG = final_graph.get_subgraph("clusterHeap")
  frameG = final_graph.get_subgraph("clusterFrames") 

  # Little hack to keep the initial ordering of the entries in 'heap'
  # Seen on stackoverflow
  json_format = json.dumps(OrderedDict(obj["heap"]), sort_keys = True)
  heap = json.loads(json_format, object_pairs_hook = OrderedDict)

  # Filling in the graphs...
  heapG = make_heap_graph(heap, heapG)
  frames = obj["frames"]
  frameG = make_stack_frames_graph(frames, frameG, final_graph)

  # Output the resulting graph to file
  graph_file_name = "exec_point_" + str(i)
  output_graph(final_graph, graph_file_name)
      


def make_heap_graph(heap, heapG):
  """
  Build the graph representing the heap state at the current execution point.
  
  Args:
    heap (dict): a dictionnary describing the content of the heap at that point

    heapG (graph object): the initial graph representing the heap

  Returns:
    graph object: The heap graph of the current execution point

  """
  prev_node_info = None
  if (len(heap) > 0):
    for k in (sorted(heap.keys(), reverse=True)):
      """
      Call the 'retrieve_heap_var_info' func with each element in the 'heap' dict
      to get the required informations about each element on the heap at the
      current execution point and build the nodes from these informations
      (Browse the keys in reverse order to keep the ordering of the LinkedList)
      """
      var_info = retrieve_heap_var_info(heap[k])
      if (var_info):
        heapG.add_node(var_info[0])
        newNode = heapG.get_node(var_info[0])
        newNode.attr["shape"] = "record"

        # Composing the node label in an elegant way : 
        l1 = str(var_info[1]) # Struct type
        l2 = " | Data : " + str(var_info[2]) # Data field
        l3 = " | <addr> Addr : \\n " + str(var_info[0]) # Addr field
        l4 = " | <next> next : " + str(var_info[3]) # Next field
        newNode.attr["label"] = l1 + l2 + l3 + l4

        # Setting the edge with the previous node if there is one:
        if prev_node_info is not None:
          if prev_node_info[3] == var_info[0]:
            heapG.add_edge(str(prev_node_info[0]), str(var_info[0]), headport = "addr", tailport= "next", style = "filled", label="next", color="#3399FF")
        prev_node_info = var_info
          
        # If the 'next' field of the current node points to NULL :
        # Last element of the LinkedList
        if var_info[-1] == "NULL":
          heapG.add_node("NULL", shape="box")
          heapG.add_edge(str(var_info[0]), "NULL", style="filled", tailport = "next", label="next", color="#3399FF")
  else:
    pass

  return heapG



def make_stack_frames_graph(frames, frameG, final_graph):
  """
  Fill in the initial empty stack frames graph with a subgraph representing each stack frames in the
  current execution point.
  
  Args:
    frames (list): a list containing the state of the stack frames of the current exec point

    frameG (graph object): an object holding the current state of the frames subgraph

    final_graph (graph_object): the entire final graph (required here to add edges between the pointer
    in the stack frames and their corresponding data on the heap)

  Returns:
    graph object: the filled in frame subgraph containing the stack frames representation of the ones
    contained in the current execution point

  """

  for frame in frames:
    # Create a frame subgraph for the current stack frame
    frame_graph_name = "cluster_" + frame["func_name"]
    frameG.add_subgraph(name = frame_graph_name)

    # Getting the current frame subgraph to modify its attributes
    current_frame_graph = frameG.get_subgraph(frame_graph_name)
    current_frame_graph.graph_attr["rankdir"] = "TB"
    current_frame_graph.graph_attr["rank"] = "same"
    current_frame_graph.graph_attr["label"] = "Function : " + str(frame["func_name"])
    if (frame["func_name"] == "main"):
      current_frame_graph.graph_attr["color"] = "#3399FF"
    else:
      current_frame_graph.graph_attr["color"] = "#33CC33"

    # Dummy node (hack to link the clusters and avoid overlaps) :
    current_frame_graph.add_node("DUMMY_" + str(frame["func_name"]))
    node_frame = current_frame_graph.get_node("DUMMY_" + str(frame["func_name"]))
    node_frame.attr["shape"] = "point"
    node_frame.attr["style"] = "invis"

    # Getting the local vars in the right order :
    json_frame_vars = json.dumps(OrderedDict(frame["encoded_locals"]), sort_keys = True)
    frame_vars = json.loads(json_frame_vars, object_pairs_hook = OrderedDict)

    # Iterating over the local vars and fill the current frame subgraph
    # k is the variable name (head, argv, argc, headRef, etc.)
    prev_node_vi = None
    for k in (sorted(frame_vars.keys(), reverse=True)):
      var = frame_vars[k]
      var[:] = [x if x != "<UNINITIALIZED>" else "uninitialized" for x in var]
      var[:] = [x if x != "0x0" else "NULL" for x in var]

      # Appending the function name to the var name to keep var names unique in the
      # whole graph
      # backup 'k' in 'name' var to set the right variable name in the final image
      name = k
      k = str(k) + "_" + frame["func_name"]
      # Create a new node for the var named "k"
      current_frame_graph.add_node(k)
      currNode = current_frame_graph.get_node(k)
      currNode.attr["shape"] = "record"

      # Composing the node label in an elegant way
      l1 = "Type : " + str(var[2])
      l2 = " | Name : " + str(name)
      l3 = " | <val> Value : " + str(var[3])
      l4 = " | Addr : " + str(var[1])
      currNode.attr["label"] = l1 + l2 + l3 + l4

      # Adding invisible edges between nodes to avoid overlapping
      if prev_node_vi is not None:
        current_frame_graph.add_edge(str(prev_node_vi), str(k), style="invis")
      prev_node_vi = k

      # Making the pointer variables, point to their data on the heap once initialized :
      if (var[2] == "pointer" and not str(var[3]) == "uninitialized"):
        heapG = final_graph.get_subgraph("clusterHeap")
        if str(var[3]) in heapG.nodes():
          final_graph.add_edge(str(k), str(var[3]), tailport = "val", style = "filled")

  return frameG



def retrieve_heap_var_info(HeapVar):
  """
  parses the entries of the 'heap' dict of an execution point and return the needed
  informations in the 'vInfo' list

  Args:
    HeapVar (list): a list containing informations about a variable on the heap

  Returns:
    list: a list containing the required informations to build a node representing the heap var

  """
  vInfo = []
  if (len(HeapVar) > 2):
    # If the size of the HeapVar list (which is a value in the 'heap' dict, describing
    # a dynamically allocated variable), is smaller of equals to 2, it means the associated
    # data have been freed at this point of the execution
    varInfo = HeapVar[2]
    address = varInfo[1]
    struct_type = varInfo[2]
    data_field = varInfo[3]
    next_field = varInfo[4]
    data_value = data_field[1][3]
    next_value = next_field[1][3]
    # Getting the list to return, ready :
    vInfo = [address, struct_type, data_value, next_value]
    vInfo[:] = [x if x != "<UNINITIALIZED>" else "uninitialized" for x in vInfo]
    vInfo[:] = [x if x != "0x0" else "NULL" for x in vInfo]

  else:
    pass

  return vInfo



def init_exec_point_graph():
  """
  Initialize the graph for the execution point with empty subgraphs.

  Returns:
    graph object: the initial empty execution point graph representation

  """
  # Defining graph attributes :
  G = AGraph(strict=False, directed=True, rankdir="LR")
  G.graph_attr["rankdir"]  = "LR"

  # Defining the node attributes
  G.node_attr["color"] = "#204CB2"

  # Defining Frames cluster
  clusFrame = G.add_subgraph(name = "clusterFrames")
  clusFrame.graph_attr["rankdir"] = "LR"
  clusFrame.graph_attr["color"] = "#FF9900"
  clusFrame.graph_attr["label"] = "Stack Frames"
  #clusFrame.graph_attr["rank"] = "same"
  # Dummy node (hack to link the clusters and avoir overlaps) :
  clusFrame.add_node("DUMMY_FRAME")
  node_frame = clusFrame.get_node("DUMMY_FRAME")
  node_frame.attr["shape"] = "point"
  node_frame.attr["style"] = "invis"

  # Defining Heap cluster
  clusHeap = G.add_subgraph(name = "clusterHeap")
  clusHeap.graph_attr["rankdir"] = "TB"
  clusHeap.graph_attr["color"] = "#009999"
  clusHeap.graph_attr["label"] = "Heap"
  clusHeap.node_attr["fixedsize"] = "False"
  # Dummy node (hack to link the clusters and avoir overlaps) :
  clusHeap.add_node("DUMMY_HEAP")
  node_heap = clusHeap.get_node("DUMMY_HEAP")
  node_heap.attr["shape"] = "point"
  node_heap.attr["style"] = "invis"

  # Link the subgraphs together to fix position :
  G.add_edge("DUMMY_FRAME", "DUMMY_HEAP", style = "invis")

  return G



def output_graph(graph, name):
  """
  A simple function to ouput the source-code of the produced graph
  and the SVG files containing the graphics

  Args:
    graph (graph object): the final graph of the current execution point

    name (String): the name of the current graph

  """
  graph.layout(prog="dot")
  graph.draw("img/" + name + ".png")
  graph.write("dots/" + name + ".dot")
  
