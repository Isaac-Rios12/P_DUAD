class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        print(' ' * 4 * level + '->', node.value)
        print_tree(node.left, level + 1)

# Crear el árbol
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)

# Imprimir la estructura del árbol
print_tree(root)