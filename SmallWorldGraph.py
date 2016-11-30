from RandomGraph import RandomGraph
import numpy as np
from Graph import Vertex
from Graph import Edge
from Graph import Graph
import GraphWorld
import random
from collections import deque

class SmallWorldGraph(RandomGraph):
    """"""
    def __init__(self, n, k):
        vs = [Vertex(i) for i in range(n)]
        RandomGraph.__init__(self, vs, [])
        self.k = k
        self.add_regular_edges(k)

    def rewire(self, p):
        """A method that takes a probability
        p as a parameter and, starting with a 
        regular graph, rewires the graph using 
        Watts and Strogatzs algorithm"""
        original_edges = set(edge for sublist in self.edges() for edge in sublist)
        subset_to_rewire = list()
        for closeness in range(self.k):
            for v in self.vertices():
                if len(original_edges) < 1:
                    break
                # choose neighbour by degree of separation
                # use sort to make sure that list of 
                # vertices is ordered. Not sure if this
                # is neccessary.
                w = sorted(self.out_vertices(v))[closeness]
                e = self.get_edge(v, w)
                if e in original_edges:
                    original_edges.remove(e)
                    replace = random.random() <= p
                    if replace:
                        subset_to_rewire.append(e)
        self.replace(subset_to_rewire)

    def replace(self, subset):
        """Takes a subset of Edges and replaces them randomly."""
        for e in subset:
            v = e[0]
            self.remove_edge(e)
            choices = list(set(self.vertices()) - set([v]))
            new = random.choice(choices)
            self.add_edge(Edge(v, new))
    
    def clustering_coefficient(self):
        """Average Cluster ratio of all vertices.
        Cluster ratio per vertex is actual number
        of neighbours connectivity divided by maximum possible number
        of neighbours connectivity"""
        res = [] # list for storing ratios for each vertex
        edges = set(edge for sublist in self.edges() for edge in sublist)
        for v in self.vertices(): # iterate through all vertices
            out = self.out_vertices(v) # store the out vertices
            k_v = len(out) # len of out vertices is number of neighbours 
            # compute the maximum number of neighbour connectedness:
            most = float(k_v) * (k_v - 1.0) / 2.0 
            actual = 0 # initiate count of actual neighbour connectedness
            # iterate through all possible combinations of vs neighbours:
            for w in out:
                for x in out: 
                    # If the Edge between the neighbour pair exists,
                    # incresae the actual count by 1:
                    if Edge(w, x) in edges or Edge(x, w) in edges:
                        actual += 1
            # calculate vs ratio as actual divided by most:
            ratio = float(actual) / most
            res.append(ratio) # append to list of ratios
        return np.average(res) # use numpy to compute the mean ratio

    def shortest_paths(self, initial):
        """Simplified version of Dijkstras shortest path algorithm.
        Takes an initial node and calculates its distance to all
        other nodes. Assumes distance of 1 for all edges."""
        distances = dict()
        distances[initial] = 0
        others = self.vertices()
        others.remove(initial)
        [distances[each] = None for each in others]
        q = deque()
        q.append(initial)
        while q:
            v = q.pop()
            d = distances[v]
            out = self.out_vertices(v)
            for w in out:
                if distances[w] == None:
                    distances[w] = d + 1.0
            q.extend(out)
        return distances

    def shortest_path_coeff(self):
        """Calculate the shortes path coefficient. It is the average
        of all shortest paths between all vertix pairs."""
        # get all vertix combinations:
        res = deque()
        vs = self.vertices()
        for v in vs:
            sps = self.shortest_paths(v)
            for w in vs:
                if v != w:
                    res.append(sps[w])
        return np.average(res)

        # for all combinations, get the shortest paths
        # store the shortest paths in a list to calculate their average






def plot():
    pass

def main():
    g = SmallWorldGraph(1000, 10)
    g.rewire(0.10)
    print g.clustering_coefficient()
    print g.shortest_path_coeff()

    layout = GraphWorld.CircleLayout(g)

    # draw the graph
    gw = GraphWorld.GraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()

if __name__ == '__main__':
    main()
