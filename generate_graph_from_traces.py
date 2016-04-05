# This is the implementation of the application translating the execution
# trace files to beautiful graphs to be shown to the sinf1252 student on the
# INGInious platform at UCL

import graphviz as gv

def main():
  g2 = gv.Digraph(format='svg')
  

  print(g1.source)

  filename = g1.render(filename='g1.dot')
  print(filename)

if __name__ == '__main__':
    main()


