# 1. Debe incluir los métodos de `push` (para agregar nodos) y `pop` (para quitar nodos).
# 2. Debe incluir un método para hacer `print` de toda la estructura.
# 3. No se permite el uso de tipos de datos compuestos como `lists`, `dicts` o `tuples` ni módulos como `collections`.

class Node:
    data: str
    next: "Node"

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class Stack:
    top: Node
    
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        data = self.top.data
        self.top = self.top.next
        return data

    def print_stack(self):
        current_node = self.top
        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next


stack = Stack()
stack.push("Soy el primer nodo")
stack.push("Soy el segundo nodo")
stack.push("Soy el tercer nodo")

print("Estructura del stack después de push:")
stack.print_stack()

print("Elemento eliminado del stack: ")
print(stack.pop())

print("Estructura del stack después de pop:")
stack.print_stack()
