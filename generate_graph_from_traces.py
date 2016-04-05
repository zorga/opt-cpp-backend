# This is the implementation of the application translating the execution
# trace files to beautiful graphs to be shown to the sinf1252 student on the
# INGInious platform at UCL

import graphviz as gv
import json
from pprint import pprint

def get_exec_point_info (path):
  pass
  

def main():
  with open("thesis_LinkedList.trace") as trace_file:
    trace = json.load(trace_file)
    for exec_points in trace:
      pprint(exec_points)

print("Hello World !")
  


if __name__ == '__main__':
    main()


