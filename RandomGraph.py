from Graph import Edge, Vertex, Graph
import random
import string

class RandomGraph(Graph):
    def __init__(self, vs=[], es=[]):
        Graph.__init__(self, vs, es)

    def add_random_edges(self, p):
        """Erdos-Renyi G(n, p) model.
        n is given by number of vertices in the graph.
        Pass p to add edges randomly until there is 
        a probability of p that there is an edge between
        any two graphs."""
        vs = self.vertices()
        while vs:
            v = vs.pop()
            for w in vs:
                if random.random() <= p:
                    self.add_edge(Edge(v, w))

def alphabet_cycle():
    while True:
        for c in string.lowercase:
            yield c

def number_cycle():
    n = 0
    while True:
        n +=1
        yield n

def alpha_number_cycle():
    while True:
        for n in number_cycle():
            for c in alphabet_cycle():
                yield c + str(n)

