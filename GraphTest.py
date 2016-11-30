import string
from Graph import Vertex
from Graph import Edge
from Graph import Graph
from RandomGraph import RandomGraph
import GraphWorld

def main(script, n='1000', *args):

#     # create n Vertices
#     n = int(n)
#     labels = string.ascii_lowercase + string.ascii_uppercase
#     vs = [Vertex(c) for c in labels[:n]]
# 
#     # create a graph and a layout
#     g = RandomGraph(vs)
#     g.add_random_edges(0.015)
#     print g.is_connected()
#     layout = GraphWorld.CircleLayout(g)
# 
#     # draw the graph
#     gw = GraphWorld.GraphWorld()
#     gw.show_graph(g, layout)
#     gw.mainloop()
    for n in range(100, 10000, 1000):
        for p in range(1, 100):
            p = p / 100.0
            success = 0
            for each in range(1000):
                vs = [Vertex(str(c)) for c in range(n)]
                g = RandomGraph(vs)
                g.add_random_edges(p)
                success += g.is_connected()
            pct = float(success) / 1000
            print 'N: %s\t\tp: %s\t\t pct connected: %s' % (n, p, pct)

if __name__ == '__main__':
    import sys
    main(*sys.argv)

