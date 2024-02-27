from scrabble.scrabbleChecker import *
from scrabble.scrabble import *

checker = ScrabbleChecker()

matrix = [
    ['t', 'v', 'b', 'o', 'f'],
    ['y', 't', 'a', 'k', 'l'],
    ['i', 'a', 'c', 'n', 'e'],
    ['u', 'o', 'l', 's', 'r'],
    ['i', 'i', 'r', 'r', 'x'],
]

double_word = (2,2)
double_letter = ()
triple_letter = ()

def search_for_words(subs: int = 0):
    all_words = set()
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            all_words.update(search_at_tile((y,x), matrix[y][x], set(), subs))
    output = list(all_words)
    output.sort(key = lambda x: x[2], reverse=True)
    return output

from collections import namedtuple
Word = namedtuple("Word", "word score")

def is_valid_cords(cords):
    if cords[1] < 0 or cords[1] >= len(matrix) or cords[0] < 0 or cords[0] >= len(matrix[cords[1]]): 
        return False
    return True

def search_at_tile(cords, current_word, visited, substitutions=0):
    #return set of (word, path to get word, score)  
    if cords in visited:
        return set()
    visited.add(cords)

    print(current_word)

    # valid words 
    valid_words = set() # list of Words
    if checker.is_prefix(current_word) == False:
        return set()
    
    if checker.is_word(current_word):
        path_taken = visited.copy()
        current_score = get_score(traversal=visited, matrix=matrix, double_word=double_word, double_letter=double_letter, triple_letter=triple_letter)
        valid_words.add((current_word, tuple(path_taken), current_score))

    # deal with substitutions
    if substitutions > 0:
        prefix_word = current_word[0:len(current_word)-1]
        new_visited = visited.copy()
        new_visited.remove(cords)
        
        for potential_letter in checker.get_possible_letter_subs(current_word):
            new_current = prefix_word + potential_letter
            new_words = search_at_tile(cords=cords, current_word=new_current, visited=new_visited.copy(), substitutions=substitutions-1)
            valid_words.update(new_words) 

    neighbours = [(-1, 0), (1, 0), (-1, 1), (1, 1), (0, -1), (0, 1), (1,-1), (-1,-1)]
    for add_x, add_y in neighbours:
        new_cords = (cords[0]+add_y, cords[1]+add_x)
        if is_valid_cords(new_cords):
            new_current = current_word+matrix[new_cords[0]][new_cords[1]]

            another_new_visited = visited.copy()

            new_words = search_at_tile(cords=new_cords, current_word=new_current, visited=another_new_visited.copy(), substitutions=substitutions)
            valid_words.update(new_words)  # Merge sets instead of adding
    return valid_words
    
print(search_for_words(1)[0:10])