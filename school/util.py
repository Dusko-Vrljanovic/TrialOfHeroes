from collections import Counter

def is_palindrome(input_string):
    reversed_input_string = "".join(reversed(input_string))
    if reversed_input_string == input_string:
        return True
    else:
        return False

def get_symbol_count(input_string):
    symbols = {}
    for c in input_string:
        if c not in symbols:
            symbols[c] = 0
        symbols[c] += 1
    
    return symbols

def is_palindrome_anagram(input_string):
    symbols = get_symbol_count(input_string)
    odd_occurrences = 0
    for count in symbols.values():
        if count % 2 == 1:
            odd_occurrences += 1
        
        if odd_occurrences > 1:
            return False
    
    return True