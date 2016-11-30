class DoublyLinkedNode(object):
    """Node of a doubly linked list.
    Contains a value, a link to previous node
    and a link to following node."""

    def __init__(self, v=None, prev=None, foll=None):
        self.v = v
        self.prev = prev
        self.foll = foll

class DoublyLinkedList(object):
    """Doubly linked list. Consists of nodes
    that are linked to each other."""
    def __init__(self, nodes=[]):
        self.first_node = None
        self.last_node = None

        for each in nodes:
            self.append(each)

    def __str__(self):
        current = self.first_node
        res = ''
        while current:
            res += str(current.v) + ' '
            current = current.foll
        return res

    def append(self, value):
        """Append a value as node to the list."""
        prev = self.last_node
        n = DoublyLinkedNode(value, prev, None)
        if prev == None:
            self.first_node = n
        else:
            prev.foll = n
        self.last_node = n

    def pop(self):
        """Remove the first node."""
        self.first_node = self.first_node.foll
        self.first_node.prev = None

def main():
    dl = DoublyLinkedList([1, 5 , 'a', 3])
    print dl
    dl.append(5)
    print dl
    dl.pop()
    print dl

if __name__ == '__main__':
    main()

