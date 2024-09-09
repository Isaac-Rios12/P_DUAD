import random 
import pytest

from exercises.exercise1 import bubble_sort

def test_exercise1_bubble_sort_works_with_small_lists():

    input_list = [10, 9, 8, 7]
    result = bubble_sort(input_list)
    assert result == [7, 8, 9, 10]


def test_excercise1_bubble_sort_works_with_large_list():
    input_list = list(range(1, 101))
    random.shuffle(input_list)

    print(f'lista desordenada...{input_list}')

    result = bubble_sort(input_list)
    print(f'lista ordenada en el bubble sort...{result}')
    assert result == list(range(1,101))

def test_excercise1_bubble_sort_works_with_empty_list():
    
    input_list = []
    result = bubble_sort(input_list)
    assert result == []

def test_excercise1_bubble_sort_doesnt_works_with_parameters_other_than_lists():
    
    input_list = "HULK"
    with pytest.raises(TypeError):
        bubble_sort(input_list)