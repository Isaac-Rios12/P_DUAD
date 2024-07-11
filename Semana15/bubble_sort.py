def bubble_sort(list_to_order):
    for l in range(0, len(list_to_order) - 1): # 0(n)
        has_made_changes = False   # O(1)
        for index in range(0, len(list_to_order) - 1 - l):  # O(n)
            current_number = list_to_order[index]   # O(1)
            next_number = list_to_order[index + 1]    # O(1)
            print(f'-- Iteracion {l}, {index}. Elemento actual: {current_number}, Siguiente elemento: {next_number}')  # O(1)
            if current_number > next_number:  # O(1)
                list_to_order[index] = next_number  # O(1)
                list_to_order[index + 1] = current_number  # O(1)
                has_made_changes = True  # O(1)

        if not has_made_changes:  # O(1)
            return  # O(1)

unorder_list = [10, 3, 9, 8, 14]  # O(1)
bubble_sort(unorder_list)  # O(n)

print(unorder_list)  # O(1)


# el nivel mas alto que alcanza es O(n)