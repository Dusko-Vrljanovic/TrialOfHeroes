import sys
import os
from collections import Counter

from util import is_palindrome, get_symbol_count, is_palindrome_anagram

if len(sys.argv) > 1:
    try:
        input_string = str(sys.argv[1])
        filtered_characher_list = [c for c in input_string if c not in "\"'.,;:!?-_"]
        filtered_string = "".join(filtered_characher_list)
        word_list = filtered_string.split(" ")

        vowels = "aeiouAEIOU"

        contains_palindrome = False
        first_palindrome = None
        letter_count = 0
        uppercase_count = 0
        lowercase_count = 0
        word_count = 0
        vowel_count = 0
        consonant_count = 0

        for word in word_list:
            if not contains_palindrome:
                if is_palindrome(word):
                    contains_palindrome = True
                    first_palindrome = word

            if is_palindrome_anagram(word):
                print(word, "is palindrome anagram.")
            else:
                print(word, "is not palindrome anagram.")

            letter_count += len(word)

            has_number = False
            for c in word:
                if c.isdigit():
                    has_number = True
                else:
                    if c in vowels:
                        vowel_count += 1
                    else:
                        consonant_count += 1

                    if c.islower():
                        lowercase_count += 1
                    elif c.isupper():
                        uppercase_count += 1
            
            if has_number is False:
                word_count += 1

        if contains_palindrome is True:
            print("Contains a palindrome: true ({})".format(first_palindrome))
        else:
            print("Contains a palindrome: false")

        print("Avg Word Len:", letter_count/len(word_list))
        print("Uppercase/Lowercase len: {}/{}".format(uppercase_count, lowercase_count))
        print("Words:", word_count)
        print("  Vowels:", vowel_count)
        print("  Consonanats:", consonant_count)
        print("Len:", len(input_string))
        print("Reverse:", "".join(reversed(input_string)))
        
        #symbols = Counter(input_string)
        symbols = get_symbol_count(input_string)
        print("Symbol count:")
        for key, value in symbols.items():
            print(" '{}': {}".format(key, value))
        

    except Exception as e:
        print("Something went wrong: ", e)
else:
    print("You should enter string if you want string statistics.")