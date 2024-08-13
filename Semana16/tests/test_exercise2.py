from exercises.exercise2 import sum_list_elements

def test_exercise1_sum_list_elements_return_result_with_big_numbers():
    input_list = [100, 1250, 3550, 12500, 1450, 2560, 8950, 4560, 2350, 10560, 7890, 1000, 10000, 4565, 7895, 1235]
    result = sum_list_elements(input_list)
    assert result == 80415


def test_exercise1_sum_list_elements_return_result_with_small_numbers():
    input_list = [5, 9, 7]
    result = sum_list_elements(input_list)
    assert result == 21

def test_exercise1_sum_list_elements_return_result_with_float_numbers():
    input_list = [5.5, 9.5, 7.9]
    result = sum_list_elements(input_list)
    assert result == 22.9
    