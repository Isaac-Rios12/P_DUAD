def bubble_sort(unorder_list):

    if not isinstance(unorder_list, list):
        raise TypeError("El parámetro debe ser una lista")

    for outer_index in range(0, len(unorder_list) - 1):
        has_made_changes = False
        for index in range(0, len(unorder_list) - 1 - outer_index):
            current_number = unorder_list[index]
            next_number    = unorder_list[index + 1]

            if current_number > next_number:
                unorder_list[index] = next_number
                unorder_list[index + 1] = current_number
                has_made_changes = True
        
        if not has_made_changes:
            break
        
    return unorder_list

input_list = "hello"

try: 
    result = bubble_sort(input_list)
    print(result)
except TypeError as e:
    print(f'se produjo un error...{e}')