# This is the implementation of the application translating the execution
# trace files to beautiful graphs to be shown to the sinf1252 student on the
# INGInious platform at UCL

from pygraphviz import *
import json
from pprint import pprint
from llist_graph_utils import *

def get_exec_point_info (obj):
  info = {}
  info["heap"] = obj["heap"] 
  info["frame_name"] = obj["func_name"] 
  info["frames"] = obj["stack_to_render"]
  
  return info


def main():
  with open("thesis_LinkedList.trace") as trace_file:
    trace = json.load(trace_file)
    i = 1
    for exec_point in trace["trace"]:
      infos = get_exec_point_info(exec_point)
      # 'i' will serve for the graph image file name
      build_graph_from (infos, i)
      i = i + 1
    # at this points, the graph should be present in the current dir
    trace_file.close

print("Hello World !")
  


if __name__ == '__main__':
    main()


