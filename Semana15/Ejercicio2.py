
def inverted_bubble_sort(list_to_oder):
    for outer_index in range(len(list_to_oder) - 1, 0, -1): 
        has_made_changes = False
        for index in range(len(list_to_oder) - 1, len(list_to_oder) - 1 - outer_index, -1):
            current_number = list_to_oder[index]
            next_number = list_to_oder[index - 1]

            print(f'-- Iteracion {outer_index}, {index}. Elemento actual: {current_number}, Siguiente elemento: {next_number}')

            if current_number < next_number:
                list_to_oder[index] = next_number
                list_to_oder[index - 1] = current_number
                has_made_changes = True

        if not has_made_changes:
            return
        

unorder_list = [10, 3, 9, 8, 14]
inverted_bubble_sort(unorder_list)

print(unorder_list)