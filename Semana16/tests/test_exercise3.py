from exercises.exercise3 import reverse_word
import pytest 

def test_exercise3_reverse_word_with_small_string():
    
    input_variable = "Hello world"
    result = reverse_word(input_variable)
    assert result == "dlrow olleH"

def test_exercise3_reverse_word_with_big_string():

    input_variable = "Python is a versatile programming language known for its easy-to-read syntax. It's popular in web development, data analysis, AI, and automation, making it a go-to choice for both beginners and professionals."
    result = reverse_word(input_variable)
    assert result == ".slanoisseforp dna srennigeb htob rof eciohc ot-og a ti gnikam ,noitamotua dna ,IA ,sisylana atad ,tnempoleved bew ni ralupop s'tI .xatnys daer-ot-ysae sti rof nwonk egaugnal gnimmargorp elitasrev a si nohtyP"

def test_exercise3_reverse_word_with_non_string():
    with pytest.raises(TypeError):
        reverse_word(123456)

