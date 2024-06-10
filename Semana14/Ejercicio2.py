
class Node:
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = None
        self.prev = None

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def push_left(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def push_right(self, data):
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        #return data

    def pop_left(self):
        if self.head is None:
            raise IndexError('Empty deque')
        data = self.head.data
        self.head = self.head.next
        if self.head is not None:
            self.head.prev = None
        else:
            self.tail = None
        return data
    
    def pop_right(self):
        if self.tail is None:
            raise IndexError('Empty deque')
        data = self.tail.data
        self.tail = self.tail.prev
        if self.tail is not None:
            self.tail.next = None
        else:
            self.head = None
        return data
    
    def print_structure(self):
        current_node = self.head
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next
        print()


deque = Deque()

deque.push_right("Soy el primer nodo")
deque.push_left("Soy el nodo a la izquierda")
deque.push_right("Soy el nodo a la derecha")

print("deque después de las insertar:")
deque.print_structure()

print("Elemento eliminado del frente del deque:")
print(deque.pop_left())

print("Elemento eliminado del final del deque:")
print(deque.pop_right())

print()
print("Deque final.....")
deque.print_structure()