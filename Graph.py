
""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""
import random
from operator import contains
from collections import deque

class Vertex(object):
    """A Vertex is a node in a graph."""

    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        """Returns a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Edge(tuple):
    """An Edge is a list of two vertices."""

    def __new__(cls, *vs):
        """The Edge constructor takes two vertices."""
        if len(vs) != 2:
            raise ValueError, 'Edges must connect exactly two vertices.'
        return tuple.__new__(cls, vs)

    def __repr__(self):
        """Return a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Graph(dict):
    """A Graph is a dictionary of dictionaries.  The outer
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.
    
    For vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vs=[], es=[]):
        """Creates a new graph.  
        vs: list of vertices;
        es: list of edges.
        """
        # # old:
        # for v in vs:
        #     self.add_vertex(v)

        # for e in es:
        #     self.add_edge(e)

        # new using list comprehension:
        [self.add_vertex(v) for v in vs]
        [self.add_edge(e) for e in es]

    def add_vertex(self, v):
        """Add a vertex to the graph."""
        self[v] = {}

    def add_edge(self, e):
        """Adds and edge to the graph by adding an entry in both directions.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, v, w):
        """Takes two vertices and returns possible edge
        between them. If no edge present return None."""
        try:
            return self[v][w]
        except:
            return None

    def remove_edge(self, e):
        """Removes all references of the edge from the
        graph."""
        v, w = e
        del self[v][w]
        del self[w][v]

    def vertices(self):
        """Return list of vertices in the graph."""
        return self.keys()

    def edges(self):
        """Return list of edges in the graph."""
        # # old:
        # res = list()
        # for d in self.values():
        #     res.append(d.values())

        # new using list comprehension
        res = [d.values() for d in self.values()]
        return res

    def out_vertices(self, v):
        """Takes a vertex and returns list of adjacent
        vertices."""
        return self[v].keys()

    def out_edges(self, v):
        """Takes a vertex and returns outgoing edges."""
        return self[v].values()

    def add_all_edges(self):
        """Assuming a previously edgless graph, add
        all edges to make it a complete graph."""
        # # old:
        # for v in self.keys():
        #     for w in self.keys():
        #         if v != w:
        #             self.add_edge(Edge(v, w))

        # new using list comprehension:
        [self.add_edge(Edge(v,w)) for v in self.keys() for w in self.keys()
                if v!=w]

    def check_regular_possibility(self, degree):
        """Check given degree number can be used
        for forming a regular graph."""
        n, k = len(self.vertices()), degree
        if not n >= (k + 1):
            m = 'Violated n >= (k+1)'
            raise self.DegreeError(m)

        # check if size possible:
        if (n * k) % 2 != 0:
            m = 'Violated nk being even.'
            raise self.DegreeError(m)

    def add_regular_edges(self, degree):
        """Starts with an edgeless graph. Adds edges
        so that every vertex has the same degree."""
        # check preconditions:
        self.check_regular_possibility(degree)
        vs = self.vertices()
        if degree >= len(vs):
            raise self.DegreeError, ('Cannot build a '+
                    'regular Graph with degree >= number ' +
                    'of vertices.')
        if is_odd(degree):
            if is_odd(len(vs)):
                raise self.DegreeError, ('Cannot build a regular ' +
                'graph with both odd degree and odd number of vertices.')
            self.add_regular_edges_even(degree - 1)
            self.add_regular_edges_odd()
        else:
            self.add_regular_edges_even(degree)

    def add_regular_edges_even(self, k=2):
        """Make regular graph with degree k where
        k must be even."""
        if is_odd(k):
            raise ValueError, 'k must be even.'
        vs = self.vertices()
        double = vs * 2

        for i, v in enumerate(vs):
            for j in range(1, k / 2 + 1):
                w = double[i+j]
                self.add_edge(Edge(v, w))

    def add_regular_edges_odd(self):
        vs = self.vertices()
        n = len(vs)
        reduplicated_list = vs * 2

        for i in range(n/2):
            v = reduplicated_list[i]
            w = reduplicated_list[i+n/2]
            self.add_edge(Edge(v, w))

    def is_connected(self):
        """Returns True if the Graph is
        connected of False otherwise."""
        q = deque()
        marked = set()
        vs = self.vertices()
        q.append(random.choice(vs))
        while len(q) > 0:
            # remove a vertex from q
            v = q.pop()
            # mark it
            marked.add(v)
            # if connected to any unmarked vertices
            connected = self.out_vertices(v)

            # # old:
            # for each in connected:
            # #   insert those into q
            #     if each not in marked:
            #         q.append(each)
            # new:
            q.extend(set(connected) - marked)
        # old:
        if all(map(lambda x: x in marked, vs)):
            return True

        # new using list comprehension:
        # if all([contains(x, marked) for x in vs]):
        #     return True
        else:
            return False


    class DegreeError(Exception):
        """Error class for when too many degrees
        demanded in add_regular_edges."""

        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)
            

def is_odd(x):
    return x % 2



def main(script, *args):
    v = Vertex('v')
    print v
    w = Vertex('w')
    print w
    e = Edge(v, w)
    print e
    g = Graph([v,w], [e])
    print g
    print 'Test get_edge:'
    print g.get_edge(v, w)
    print 'Test remove_edge.'
    g.remove_edge(e)
    print 'Print get_edge again:'
    print g.get_edge(v, w)
    # add some more vertices:
    a,b,c = Vertex('a'), Vertex('b'), Vertex('c')
    g.add_vertex(a)
    g.add_vertex(b)
    g.add_vertex(c)
    print 'After adding some new vertices print vertices:'
    print g.vertices()
    print 'Print edges before adding them:'
    print g.edges()
    # add some edges:
    ab = Edge(a, b)
    ac = Edge(a, c)
    bc = Edge(b, c)
    g.add_edge(ab)
    g.add_edge(ac)
    g.add_edge(bc)
    print 'After adding edges, print again:'
    print g.edges()
    print 'out_vertices for a:'
    print g.out_vertices(a)
    print 'out_edges for a:'
    print g.out_edges(a)
    print 'Add all edges:'
    g.add_all_edges()
    print g.edges() 


if __name__ == '__main__':
    import sys
    main(*sys.argv)
