class Node:
    data: str
    next: "Node"

    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    head: Node

    def __init__(self, head):
        self.head = head

    def bubble_sort(self):
        if not self.head:
            return
        
        end = None
        while end != self.head.next:
            has_made_changes = False
            current = self.head
            while current.next != end:
                next_node = current.next
                if current.data > next_node.data:
                    temp = current.data
                    current.data = next_node.data
                    next_node.data = temp
                    has_made_changes = True
                current = current.next
            end = current

            if not has_made_changes:
                return
            

    def print_structure(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

node5 = Node(10)
node4 = Node(5, node5)
node3 = Node(8, node4)
node2 = Node(3, node3)
node1 = Node(7, node2)

linked_list = LinkedList(node1)

print("Lista antes de ordenar:")
linked_list.print_structure()

linked_list.bubble_sort() 

print("\nLista después de ordenar:")
linked_list.print_structure()
