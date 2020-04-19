import math

class Node:
    def __init__(self, state, score, moves):
        self.state = state
        self.score = score
        self.moves = moves
        self.parent = None
        self.child = None
        self.left = None
        self.right = None
        self.degree = 0
        

class Graph:
    def __init__(self):
        self.root_list = None
        self.min_node = None
        self.total_nodes = 0


    def iterate(self, start):
        #print('iterate')
        node = start
        stop = start
        flag = False

        while True:
            if node == stop and flag is True:
                break

            elif node == stop:
                flag = True

            yield node
            node = node.right


    def root_list_remove(self, node):
        #print('root_list_remove')
        if node == self.root_list:
            self.root_list = node.right

        node.left.right = node.right
        node.right.left = node.left


    def child_list_merge(self, parent, child):
        #print('child_list_merge')
        if parent.child is None:
            parent.child = child

        else:
            child.right = parent.child.right
            child.left = parent.child
            parent.child.right.left = child
            parent.child.right = child


    def root_list_merge(self, node):
        #print('root_list_merge')
        if self.root_list is None:
            self.root_list = node

        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node


    def link(self, node_B, node_A):
        #print('link')
        self.root_list_remove(node_B)
        node_B.left = node_B
        node_B.right = node_B
        self.child_list_merge(node_A, node_B)
        node_A.degree += 1
        node_B.parent = node_A


    def cleanup(self):
        #print('cleanup')
        slots = [None] * int(math.log(self.total_nodes) * 2)
        nodes = [n for n in self.iterate(self.root_list)]

        for node_A in nodes:
            d = node_A.degree

            while slots[d] != None:
                node_B = slots[d]
                if node_A.score > node_B.score:
                    #print('swap')
                    temp_node = node_A
                    node_A, node_B = node_B, temp_node

                self.link(node_B, node_A)
                slots[d] = None
                d += 1

            slots[d] = node_A
            for slot in slots:
                if slot is not None:
                    if slot.score <= self.min_node.score:
                        self.min_node = slot


    def find_min(self):
        #print('find_min')
        return self.min_node


    def extract_min(self):
        #print('extract_min')
        node = self.find_min()
        if node is not None:
            if node.child is not None:
                children = [x for x in self.iterate(node.child)]
                for child in children:
                    child.parent = None
                    child.left = None
                    child.right = None
                    self.root_list_merge(child)

            self.root_list_remove(node)
            if node == node.right:
                self.min_node = None
                self.root_list = None

            else:
                self.min_node = node.right
                self.cleanup()

            self.total_nodes -= 1

            return node


    def add_node(self, state, score, moves):
        #print('add_node')
        n = Node(state, score, moves)
        n.right = n
        n.left = n
        self.root_list_merge(n)
        if self.min_node is None or n.score < self.min_node.score:
            self.min_node = n

        self.total_nodes += 1

        return n