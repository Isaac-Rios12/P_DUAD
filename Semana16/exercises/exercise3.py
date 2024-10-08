

def reverse_word(vari):
    if not isinstance(vari, str):
        raise TypeError("Input must be a string")
    
    result = ''
    for i in reversed(vari):
        result += i
    
    return result
