# This is the implementation of the application translating the execution
# trace files to beautiful graphs to be shown to the sinf1252 student on the
# INGInious platform at UCL

import sys
from pygraphviz import *
import json
from pprint import pprint
from llist_graph_utils import *
import argparse

def get_exec_point_info (obj):
  info = {}
  info["heap"] = obj["heap"] 
  info["frame_name"] = obj["func_name"] 
  info["frames"] = obj["stack_to_render"]
  return info



def main():
  # Command line parse to get the filename and to pass some options.
  parser = argparse.ArgumentParser()
  parser.add_argument("trace_filename", help="A path to a .trace file")
  parser.add_argument("-v", "--verbose", help="Explain what is being done",
    action="store_true")
  args = parser.parse_args()
  # print an error to stderr and return if the file is not a .trace file :
  if not args.trace_filename.endswith('.trace'):
    print("Error : need a \".trace\" file !", file = sys.stderr)
    return

  if (args.verbose):
    print("Opening " + args.trace_filename + " file...")
  with open(args.trace_filename) as trace_file:
    trace = json.load(trace_file)
    nTraces = len(trace["trace"])
    if (args.verbose):
      print("Generating graphics of " + str(nTraces) + " execution points...")
    i = 0
    # Get the useful informations from each exec point and put them into
    # the 'infos' list.
    # Then call the 'build_graph_from' function from 'llist_graph_utils' to
    # build the graphs of each exec point.
    for exec_point in trace["trace"]:
      if (args.verbose):
        print ("Processing exec point number " + str(i))
      infos = get_exec_point_info(exec_point)
      # 'i' will serve for the graph image file name
      build_graph_from (infos, i)
      i = i + 1
    # at this points, the graph should be present in the current dir
    trace_file.close

  


if __name__ == '__main__':
    main()


