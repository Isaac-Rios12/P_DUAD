def bubble_sort(list_to_order):
    for l in range(0, len(list_to_order) - 1):
        has_made_changes = False
        for index in range(0, len(list_to_order) - 1 - l):
            current_number = list_to_order[index]
            next_number = list_to_order[index + 1]
            print(f'-- Iteracion {l}, {index}. Elemento actual: {current_number}, Siguiente elemento: {next_number}')
            if current_number > next_number:
                list_to_order[index] = next_number
                list_to_order[index + 1] = current_number
                has_made_changes = True

    if not has_made_changes:
        return

unorder_list = [10, 3, 9, 8, 14]
bubble_sort(unorder_list)

print(unorder_list)