""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import string
import listsum
import random
import matplotlib.pyplot as pyplot

def etime():
    """See how much user and system time this process has used
    so far and return the sum."""

    user, sys, chuser, chsys, real = os.times()
    return user+sys

# Exercise 3  
# Write a function called bisection that takes a sorted list 
# and a target value and returns the index of the value in the 
# list, if it is there, or None if it is not.
# 
# Or you could read the documentation of the bisect module and use that!

def bisect(sorted_list, target_value):
    lo = 0
    hi = len(sorted_list)
    while lo < hi:
        mid = (lo + hi) / 2
        if target_value == a[mid]:
            return mid
        elif target_value < a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return None

class LinearMap(object):
    """A simple implementation of a map using a list of tuples
    where each tuple is a key-value pair."""

    def __init__(self):
        self.items = []

    def add(self, k, v):
        """Adds a new item that maps from key (k) to value (v).
        Assumes that they keys are unique."""
        self.items.append((k, v))

    def get(self, k):
        """Looks up the key (k) and returns the corresponding value,
        or raises KeyError if the key is not found."""
        for key, val in self.items:
            if key == k:
                return val
        raise KeyError


class BetterMap(object):
    """A faster implementation of a map using a list of LinearMaps
    and the built-in function hash() to determine which LinearMap
    to put each key into."""

    def __init__(self, n=100):
        """Appends (n) LinearMaps onto (self)."""
        self.maps = []
        for i in range(n):
            self.maps.append(LinearMap())

    def __len__(self):
        return len(self.maps)

    def find_map(self, k):
        """Finds the right LinearMap for key (k)."""
        index = hash(k) % len(self)
        return self.maps[index]

    def add(self, k, v):
        """Adds a new item to the appropriate LinearMap for key (k)."""
        m = self.find_map(k)
        m.add(k, v)

    def get(self, k):
        """Finds the right LinearMap for key (k) and looks up (k) in it."""
        m = self.find_map(k)
        return m.get(k)

    def iteritems(self):
        for m in self.maps:
            for k, v in m.items:
                yield k, v


class HashMap(object):
    """An implementation of a hashtable using a BetterMap
    that grows so that the number of items never exceeds the number
    of LinearMaps.

    The amortized cost of add should be O(1) provided that the
    implementation of sum in resize is linear."""

    def __init__(self):
        """Starts with 2 LinearMaps and 0 items."""
        self.maps = BetterMap(2)
        self.num = 0

    def get(self, k):
        """Looks up the key (k) and returns the corresponding value,
        or raises KeyError if the key is not found."""
        return self.maps.get(k)

    def add(self, k, v):
        """Resize the map if necessary and adds the new item."""
        if self.num == len(self.maps):
            self.resize()

        self.maps.add(k, v)
        self.num += 1

    def resize(self):
        """Makes a new map, twice as big, and rehashes the items."""
        new_maps = BetterMap(self.num * 2)
        for k, v in self.maps.iteritems():
            new_maps.add(k, v)
        
        self.maps = new_maps


class TreeMap(object):
    """Implementation of a map interface using a red-black tree."""
    def __init__(self):
        pass

etime = listsum.etime

def test_add(o, n):
    """Test the method add for map object o, with n key value pairs."""
    
    start = etime()
    for i in range(n):
        o.add(str(i), i+1)
    end = etime()
    return end - start

def test_get(o, n):
    """Test the method get for map object o with n key value pairs."""
    for i in range(n):
        o.add(i, i+1)
    # look_up = random.choice(range(n))
    look_up = n - 1

    start = etime()
    v = o.get(look_up)
    end = etime()
    return end - start

def test_loop_add(name):
    """Tests the method add with a range of values for n
    for map object o. 
    
    Returns a list of ns and run times."""
    

    # Use different order of magnitudes for n
    # depending on the object
    d = dict(HashMap=10000,
             BetterMap=10000000,
             LinearMap=100000)
    factor = d[name]
    
    # test add for object o ver a range of 
    # values for (n)
    ns = []
    ts = []
    for i in range(2, 25):
        n = factor * i
        o = eval(name + '()')
        t = test_add(o, n)
        print n, t
        ns.append(n)
        ts.append(t)

    return ns, ts

def test_loop_get(name):
    """Tests the method get with a range of values for n
    for map object o.
    
    Returns a list of ns and run times."""
    d = dict(HashMap=100000,
             BetterMap=100000,
             LinearMap=100000)
    factor = d[name]
    
    # test add for object o ver a range of 
    # values for (n)
    ns = []
    ts = []
    for i in range(2, 25):
        n = factor * i
        o = eval(name + '()')
        t = test_get(o, n)
        print n, t
        ns.append(n)
        ts.append(t)

    return ns, ts


plot = listsum.plot
fit = listsum.fit
save = listsum.save

def make_fig(obs, f, scale='log', exp=1.0, filename=''):
    pyplot.clf()
    pyplot.xscale(scale)
    pyplot.yscale(scale)
    pyplot.title('Compare method ' + f)
    pyplot.xlabel('n')
    pyplot.ylabel('run time (s)')

    colors = ['blue', 'orange', 'green']
    for o, color in zip(obs, colors):
        if f == 'add':
            data = test_loop_add(o)
        elif f == 'get':
            data = test_loop_get(o)
        plot(*data, label=o, color=color, exp=exp)

    pyplot.legend(loc=4)

    if filename:
        save(filename)
    else:
        pyplot.show()

# def main(script):
#     m = HashMap()
#     s = string.ascii_lowercase
# 
#     for k, v in enumerate(s):
#         m.add(k, v)
# 
#     for k in range(len(s)):
#         print k, m.get(k)

def main(script):
    make_fig(['LinearMap', 'BetterMap'], 'get', exp=1.0)
    make_fig(['HashMap'], 'get', exp=0.0)


if __name__ == '__main__':
    import sys
    main(*sys.argv)
