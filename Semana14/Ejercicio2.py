
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

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
            self.head = new_node

    def push_right(self, data):
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        

    def pop_left(self):
        if self.head is None:
            raise IndexError('Empty deque')
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return data
    
    def pop_right(self):
        if self.tail is None:
            raise IndexError('Empty deque')
        
        #esto en caso de que solo un elemento
        if self.head == self.tail:
            data = self.tail.data
            self.head = self.tail = None
            return data
        
        #aca itero para encontrar el penulti
        current = self.head
        while current.next != self.tail:
            current = current.next

        data = self.tail.data
        self.tail = current
        self.tail.next = None
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