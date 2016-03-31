# Convert a trace created by the Valgrind OPT C backend to a format that
# the OPT frontend can digest

# Created 2015-10-04 by Philip Guo
# Hacked by Nicolas Ooghe

# pass in the $basename of a program. assumes that the Valgrind-produced
# trace is $basename.vgtrace and the source file is $basename.{c,cpp}


# this is pretty brittle and dependent on the user's gcc version and
# such because it generates code to conform to certain calling
# conventions, frame pointer settings, etc., eeek
#
# we're assuming that the user has compiled with:
# gcc -ggdb -O0 -fno-omit-frame-pointer
#
# on a platform like:
'''
$ gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/lib/gcc/x86_64-linux-gnu/4.8/lto-wrapper
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 4.8.4-2ubuntu1~14.04' --with-bugurl=file:///usr/share/doc/gcc-4.8/README.Bugs --enable-languages=c,c++,java,go,d,fortran,objc,obj-c++ --prefix=/usr --program-suffix=-4.8 --enable-shared --enable-linker-build-id --libexecdir=/usr/lib --without-included-gettext --enable-threads=posix --with-gxx-include-dir=/usr/include/c++/4.8 --libdir=/usr/lib --enable-nls --with-sysroot=/ --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --enable-gnu-unique-object --disable-libmudflap --enable-plugin --with-system-zlib --disable-browser-plugin --enable-java-awt=gtk --enable-gtk-cairo --with-java-home=/usr/lib/jvm/java-1.5.0-gcj-4.8-amd64/jre --enable-java-home --with-jvm-root-dir=/usr/lib/jvm/java-1.5.0-gcj-4.8-amd64 --with-jvm-jar-dir=/usr/lib/jvm-exports/java-1.5.0-gcj-4.8-amd64 --with-arch-directory=amd64 --with-ecj-jar=/usr/share/java/eclipse-ecj.jar --enable-objc-gc --enable-multiarch --disable-werror --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --with-tune=generic --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu
Thread model: posix
gcc version 4.8.4 (Ubuntu 4.8.4-2ubuntu1~14.04)
'''

import json
import os
import pprint
import sys
from optparse import OptionParser

pp = pprint.PrettyPrinter(indent=2)

RECORD_SEP = '=== pg_trace_inst ==='

ONLY_ONE_REC_PER_LINE = True

all_execution_points = []

def process_record(lines):
  """
  This function returns True if the parse is successful
  False otherwise
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
  This function is used to make the executions points for the final trace
  """
  #print '---'
  #pp.pprint(obj)
  #print

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
    # the stack_obj['is_highlighted'] is set to "True" if e and top_stack_entry are the same variable (address AND value)

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

  #pp.pprint(ret)
  #print [(e['func_name'], e['frame_id']) for e in ret['stack_to_render']]

  return ret

def encode_value(obj, heap):
  """
  the function used to encode the different types of variables of the programs, in the
  right trace (OPT) format.
  This is also used to update the heap in case of dynamically allocated variables
  (with malloc : heap_blocks)
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
    # TODO: what about heap-to-heap pointers?
    # TODO: what about the unions ?
    # TODO: what about the void type ?

  else:
    assert False

def setEvents(filtered_execution_points):
  """
  Make sure that each successive entry in the filtered_execution_points list
  has a identical, bigger, of smaller 'stack_to_render' list than the
  previous one. These cases represent a 'step_line' event (nothing to do),
  a function call, or a a function return, respectively.
  returns a finalExecPoints list with the right 'event' entry for all
  execution points of the trace
  """
  finalExecPoints = []

  if filtered_execution_points:
    finalExecPoints.append(filtered_execution_points[0])

    for prev, cur in zip(filtered_execution_points, filtered_execution_points[1:]):
      prev_frame_ids = [e['frame_id'] for e in prev['stack_to_render']]
      cur_frame_ids = [e['frame_id'] for e in cur['stack_to_render']]

      lenPrev = len(prev['stack_to_render'])
      lenCur = len(prev['stack_to_render'])
      
      if lenPrev == lenCur:
        finalExecPoints.append(cur)
      elif lenPrev < lenCur:
        cur['event'] = 'call'
        finalExecPoints.append(cur)
      elif lenPrev > lenCur:
        prev['event'] = 'return'
        finalExecPoints.append(cur)

    # If all went well with parsing the entries, until now, we could set the
    # event of the last execution point to 'return'
    # Otherwise, it is an exception (crash case)
    if success:
      final_execution_points[-1]['event'] = 'return'
    else:
      final_execution_points[-1]['event'] = 'exception'
      final_execution_points[-1]['exception_msg'] = 'code crash !'

  return final_execution_points

###############################################################################

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

  success = True

  for line in open(basename + '.vgtrace'):
    line = line.strip()
    if line == RECORD_SEP:
      success = process_record(cur_record_lines)
      if not success:
        break
      cur_record_lines = []
    else:
      cur_record_lines.append(line)

  # only parse final record if we've been successful so far; i.e., die
  # on the first failed parse
  if success:
    success = process_record(cur_record_lines)

  # now do some filtering action based on heuristics
  filtered_execution_points = []

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

    #print func_names, frame_ids
    filtered_execution_points.append(pt)

  # Setting the 'event' entries of the executions points for the final trace
  final_execution_points = setEvents(filtered_execution_points)
  
  # only keep the FIRST 'step_line' event for any given line, to match what
  # a line-level debugger would do
  if ONLY_ONE_REC_PER_LINE:
    tmp = []
    prev_event = None
    prev_line = None
    prev_frame_ids = None

    for elt in final_execution_points:
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

  final_execution_points = tmp # the ole' switcheroo


  '''
  for elt in final_execution_points:
  skip = False
  cur_event = elt['event']
  cur_line = elt['line']
  cur_frame_ids = [e['frame_id'] for e in elt['stack_to_render']]
  print cur_event, cur_line, cur_frame_ids
  '''

  if os.path.isfile(basename + '.c'):
    cod = open(basename + '.c').read()
    else:
      cod = open(basename + '.cpp').read()

# produce the final trace, voila!
      final_res = {'code': cod, 'trace': final_execution_points}

# use sort_keys to get some sensible ordering on object keys
s = json.dumps(final_res, indent=2, sort_keys=True)
  if options.js_varname:
  print('var ' + options.js_varname + ' = ' + s + ';')
  else:
print(s)

  if __name__ == '__main__':
main()

