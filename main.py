from scrabble.scrabbleChecker import *

checker = ScrabbleChecker()

matrix = [
    ['s', 's', 'e', 'i'],
    ['n', 'p', 's', 'd'],
    ['k', 'r', 'i', 'r'],
    ['n', 'a', 'a', 'a'],
]

def search_for_words():
    all_words = set()
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            all_words.update(search_at_tile((y,x), matrix[y][x], set()))
    return all_words

from collections import namedtuple
Word = namedtuple("Word", "word score")

def is_valid_cords(cords):
    if cords[1] < 0 or cords[1] >= len(matrix) or cords[0] < 0 or cords[0] >= len(matrix[cords[1]]): 
        return False
    return True

def search_at_tile(cords, currentWord, visited):
    if cords in visited:
        return set()
    visited.add(cords)
    # valid words 
    valid_words = set() # list of Words
    if checker.is_prefix(currentWord) == False:
        return set()
    if checker.is_word(currentWord):
        valid_words.add(currentWord)

    neighbours = [(-1, 0), (1, 0), (-1, 1), (1, 1), (0, -1), (0, 1)]
    for add_x, add_y in neighbours:
        new_cords = (cords[0]+add_y, cords[1]+add_x)
        if is_valid_cords(new_cords):
            new_current = currentWord+matrix[new_cords[0]][new_cords[1]]
            new_visited = visited.copy() 

            new_words = search_at_tile(cords=new_cords, currentWord=new_current, visited=new_visited)
            valid_words.update(new_words)  # Merge sets instead of adding
    return valid_words
    

print(search_for_words())

