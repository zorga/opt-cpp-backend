#!/bin/python2.7
# Converts a trace created by the Valgrind C backend to a format that
# will be used by the frontend to generate the graphs representing the
# execution of a C program

# Originally created 2015-10-04 by Philip Guo for his Online Python Tutor tool
# Many thanks to him ! Link : http://pgbovine.net/rosetta/c-demo.html

# Hacked by Nicolas Ooghe for his master thesis in Computer Sciences at the
# Universite Catholique de Louvain

# pass in the $basename of a program. assumes that the Valgrind-produced
# trace is $basename.vgtrace and the source file is $basename.{c,cpp}



import json
import os
import pprint
import sys
from optparse import OptionParser

# Global variables definitions :

# This list will contain all the execution points record from the Valgrind trace file
# if it's successfully parsed
all_execution_points = []

# Functions definitions :

def process_record(lines):
  """
  This function should be used as a sub-routine for the .vgtrace files parsing.
  It parses an execution point in the Valgrind trace format and append it, to
  the 'all_execution_points' global variable.
  
  Args:
    lines (list): a list of lines (Strings) from a .vgtrace file corresponding 
    to an execution point record in the Valgrind trace format.

  Returns:
    bool: True if successful, False otherwise.

  """
  if not lines:
    return True # 'nil success case to keep the parser going

  rec = '\n'.join(lines) # groups all the lines and separates them with a line-return
  try:
    obj = json.loads(rec)
  except ValueError:
    print >> sys.stderr, "Ugh, bad record!"
    return False
  x = process_json_obj(obj)
  all_execution_points.append(x)
  return True



def process_json_obj(obj):
  """
  This function transforms a Valgrind execution point object in the final
  trace format.

  Args:
    obj (JSON Python object): An execution point object in the Valgrind trace format
    (Which are themselves encoded in the JSON format)

  Returns:
    dict: A Dictonnary representing a execution point in the final trace format

  """

  assert len(obj['stack']) > 0 # C programs always have a main at least!
  # Here, the assert will throw an exception (error) if the condition after assert is false

  obj['stack'].reverse() # make the stack grow down to follow convention
  top_stack_entry = obj['stack'][-1]

  # create an execution point object
  ret = {}
  heap = {}
  stack = []
  enc_globals = {}

  ret['heap'] = heap
  ret['stack_to_render'] = stack
  ret['globals'] = enc_globals
  ret['ordered_globals'] = obj['ordered_globals']
  ret['line'] = obj['line']
  ret['func_name'] = top_stack_entry['func_name'] # use the 'topmost' entry's name
  ret['event'] = 'step_line'
  ret['stdout'] = '' # TODO: handle this

  for g_var, g_val in obj['globals'].iteritems():
    enc_globals[g_var] = encode_value(g_val, heap)

  for e in obj['stack']:
    stack_obj = {}
    stack.append(stack_obj)

    stack_obj['func_name'] = e['func_name']
    stack_obj['ordered_varnames'] = e['ordered_varnames']
    stack_obj['is_highlighted'] = e is top_stack_entry
    # the stack_obj['is_highlighted'] is set to "True" if e and top_stack_entry
    # are the same variable (address AND value)

    # hacky: does FP (the frame pointer) serve as a unique enough frame ID?
    # sometimes it's set to 0 :/
    stack_obj['frame_id'] = e['FP']
    stack_obj['unique_hash'] = stack_obj['func_name'] + '_' + stack_obj['frame_id']

    # unsupported
    stack_obj['is_parent'] = False
    stack_obj['is_zombie'] = False
    stack_obj['parent_frame_id_list'] = []

    enc_locals = {}
    stack_obj['encoded_locals'] = enc_locals

    for local_var, local_val in e['locals'].iteritems():
      enc_locals[local_var] = encode_value(local_val, heap)

  return ret



def encode_value(obj, heap):
  """
  This function encodes the global and local variables from an execution point in the
  Valgrind trace format into the the final trace format.
  It could also modify the 'heap' dictionnary defined in the 'process_json_obj' calling
  function (i.e. while processing pointers variables that points to valid data)

  Args:
    obj (dict): a dictionnary containing the information about the value of a variable
    from a Vagrind execution point format

    heap (dict): a dictionnary representing the 'heap' of an execution trace. It
    is variable defined in the calling 'process_json_obj' function and could be updated
    accordingly during the 'encode_value' function call

  Returns:
    list: a list containing the information about the variable originally described in
    the 'obj' argument, in the final trace format

  """
  if obj['kind'] == 'base':
    return ['C_DATA', obj['addr'], obj['type'], obj['val']]

  elif obj['kind'] == 'pointer':
    if 'deref_val' in obj:
      encode_value(obj['deref_val'], heap) # update the heap
    return ['C_DATA', obj['addr'], 'pointer', obj['val']]

  elif obj['kind'] == 'struct':
    ret = ['C_STRUCT', obj['addr'], obj['type']]

    # sort struct members by address so that they look ORDERED
    members = obj['val'].items()
    members.sort(key=lambda e: e[1]['addr'])
    for k, v in members:
      entry = [k, encode_value(v, heap)] # TODO: is an infinite loop possible here?
      ret.append(entry)
    return ret

  elif obj['kind'] == 'array':
    ret = ['C_ARRAY', obj['addr']]
    for e in obj['val']:
      ret.append(encode_value(e, heap)) # TODO: is an infinite loop possible here?
    return ret

  elif obj['kind'] == 'typedef':
    # pass on the typedef type name into obj['val'], then recurse
    obj['val']['type'] = obj['type']
    return encode_value(obj['val'], heap)

  elif obj['kind'] == 'heap_block':
    assert obj['addr'] not in heap
    new_elt = ['C_ARRAY', obj['addr']]
    for e in obj['val']:
      new_elt.append(encode_value(e, heap)) # TODO: is an infinite loop possible here?
    heap[obj['addr']] = new_elt

  else:
    assert False



def setEvents(ExecutionPoints, success):
  """
  This function modify the 'event' entries of the dictionnaries representing an
  execution point in the final trace format (i.e. 'call', 'return', 'step_line')
  accordingly.
  
  Args:
    ExecutionPoints (list): a list of execution point in the final trace
    format.

    success (bool): a boolean that represents the success of the Valgrind trace
    file parsing. It's useful to modify the 'event' entry of the last execution point.
    (If the parsing went bad, it means that the Valgrind trace is badly formatted. Thus,
    the corresponding C program crashed during the Valgrind analysis)

  Returns:
    list: a list of execution points in the final trace format with their 'event'
    entries modified accordingly.

  """
  finalExecPoints = []

  if ExecutionPoints:
    finalExecPoints.append(ExecutionPoints[0])

    for prev, cur in zip(ExecutionPoints, ExecutionPoints[1:]):
      prev_frame_ids = [e['frame_id'] for e in prev['stack_to_render']]
      cur_frame_ids = [e['frame_id'] for e in cur['stack_to_render']]

      lenPrev = len(prev_frame_ids)
      lenCur = len(cur_frame_ids)
      
      if prev_frame_ids == cur_frame_ids:
        finalExecPoints.append(cur)
      elif lenPrev < lenCur:
        if prev_frame_ids == cur_frame_ids[:-1]:
          cur['event'] = 'call'
          finalExecPoints.append(cur)
      elif lenPrev > lenCur:
        if cur_frame_ids == prev_frame_ids[:-1]:
          prev['event'] = 'return'
          finalExecPoints.append(cur)

    # If all went well with parsing the entries, until now, we could set the
    # event of the last execution point to 'return'
    # Otherwise, it is an exception (crash case)
    if success:
      finalExecPoints[-1]['event'] = 'return'
    else:
      finalExecPoints[-1]['event'] = 'exception'
      finalExecPoints[-1]['exception_msg'] = 'code crash !'

    # The 'finalExecPoints' list should not have the same size 'ExecutionPoints' list
    assert len(finalExecPoints) <= len(ExecutionPoints)

  return finalExecPoints



def removeRedundantLines(ExecutionPoints):
  """
  Removes the redundant execution points. Such execution points all have their 'event'
  entry set to 'step_line'. They have the same 'line' entries and the same 'frame_id'
  entries in their 'stack_to_render' entries (dictionnaries).
  
  Args:
    ExecutionPoints (list): a list of execution points in the final trace format.

  Returns:
    list: a list of execution points in the final trace format with their redundant
    execution points removed.

  """
  tmp = []
  prev_event = None
  prev_line = None
  prev_frame_ids = None

  for elt in ExecutionPoints:
    skip = False
    cur_event = elt['event']
    cur_line = elt['line']
    cur_frame_ids = [e['frame_id'] for e in elt['stack_to_render']]
    if prev_frame_ids:
      if cur_event == prev_event == 'step_line':
        if cur_line == prev_line and cur_frame_ids == prev_frame_ids:
          skip = True

    if not skip:
      tmp.append(elt)

    prev_event = cur_event
    prev_line = cur_line
    prev_frame_ids = cur_frame_ids

  return tmp



def filterExecPoints():
  """
  This function filters the execution points based on heuristics and tracks bogus
  execution points

  This function modifies the 'all_execution_points' global variable. So there are no
  arguments for this function.

  Returns:
    list: a list of execution point in the final trace format if their are no bogus
    ones in the original list.

  TODO : To be improved

  """
  filteredExecPoints = []

  for pt in all_execution_points:
    # any execution point with a 0x0 frame pointer is bogus
    frame_ids = [e['frame_id'] for e in pt['stack_to_render']]
    func_names = [e['func_name'] for e in pt['stack_to_render']]
    if '0x0' in frame_ids:
      continue

    # any point with DUPLICATE frame_ids is bogus, since it means
    # that the frame_id of some frame hasn't yet been updated
    # Myself : the "set()" function removes the duplicates
    if len(set(frame_ids)) < len(frame_ids):
      continue

    # any point with a weird '???' function name is bogus
    # but we shouldn't have any more by now
    assert '???' not in func_names

    filteredExecPoints.append(pt)
  return filteredExecPoints



def main():
  """
  The main function of the script

  """
  parser = OptionParser(usage="Create an OPT trace from a Valgrind trace")
  parser.add_option("--create_jsvar", dest="js_varname", default=None,
                      help="Create a JavaScript variable out of the trace")
  (options, args) = parser.parse_args()
  basename = args[0]
  cur_record_lines = []
  RECORD_SEP = '=== pg_trace_inst ==='
  success = True

  # Parsing the VG trace file
  for line in open(basename + '.vgtrace'):
    line = line.strip()
    if line == RECORD_SEP:
      success = process_record(cur_record_lines)
      if not success:
        break
      cur_record_lines = []
    else:
      cur_record_lines.append(line)
  # Only parse final record if we've been successful so far
  if success:
    success = process_record(cur_record_lines)

  # Processing the execution point list
  filtered_execution_points = filterExecPoints();
  final_execution_points = setEvents(filtered_execution_points, success)
  final_execution_points = removeRedundantLines(final_execution_points)

  # Adding an 'ExecutionPointNumber' entry
  i = 0
  for ep in final_execution_points:
    ep['ExecutionPointNumber'] = i 
    i = i + 1
  
  # Getting the code source of the program in a String variable and adding it in
  # the final trace file
  cod = open(basename + '.c').read()
  final_res = {'code': cod, 'trace': final_execution_points}

  # use sort_keys to get some sensible ordering on object keys
  s = json.dumps(final_res, indent=2, sort_keys=True)

  # Creating a javaScript variable if required by the user
  if options.js_varname:
    print('var ' + options.js_varname + ' = ' + s + ';')
  else:
    print(s)



if __name__ == '__main__':
  main()

