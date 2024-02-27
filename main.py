from spellCast.solver import SpellCastSolver
from spellCast.spellCastChecker import *
from spellCast.spellCast import *

checker = SpellCastChecker()

matrix = [
    ['a', 'a', 'a', 'o', 'f'],
    ['a', 'a', 'a', 'a', 'a'],
    ['a', 'a', 'c', 'k', 'e'],
    ['a', 'a', 'l', 's', 'r'],
    ['a', 'a', 'a', 'a', 'a'],
]

double_word = (2,2)
double_letter = ()
triple_letter = ()

def search_for_words(subs: int = 0):
    all_words = set()
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            letter = matrix[y][x]
            results = search_at_tile((y,x), letter, set(), subs)
            all_words.update(results)
    output = list(all_words)
    output.sort(key = lambda x: x[3] - len(x[2]), reverse=True)
    return output

def is_valid_cords(cords):
    if cords[0] < 0 or cords[0] >= len(matrix) or cords[1] < 0 or cords[1] >= len(matrix[cords[0]]): 
        return False
    return True

def search_at_tile(cords, current_word, visited, substitutions=0, changed=set()):
    #return set of (word, path to get word, dictionary of cord to the changed letter, score)  
    if cords in visited:
        return set()
    visited.add(cords)
 
    # valid words 
    valid_words = set() # list of Words

    # deal with substitutions
    if substitutions > 0:
        prefix_word = current_word[0:len(current_word)-1]
        new_visited = visited.copy()
        new_visited.remove(cords)
        
        for potential_letter in checker.get_possible_letter_subs(current_word):
            new_current = prefix_word + potential_letter
            new_changed = changed.copy()
            new_changed.add(cords)
            new_words = search_at_tile(cords=cords, current_word=new_current, visited=new_visited.copy(), substitutions=substitutions-1, changed=new_changed)
            valid_words.update(new_words)

    if checker.is_prefix(current_word) == False:
        return set()
    
    if checker.is_word(current_word):
        print(current_word)
        path_taken = visited.copy()
        current_score = get_score(traversal=visited, matrix=matrix, double_word=double_word, double_letter=double_letter, triple_letter=triple_letter)
        valid_words.add((str(current_word), tuple(path_taken), tuple(changed), int(current_score)))


    neighbours = [(-1, 0), (1, 0), (-1, 1), (1, 1), (0, -1), (0, 1), (1,-1), (-1,-1)]
    for add_y, add_x in neighbours:
        new_cords = (cords[0]+add_y, cords[1]+add_x)

        if is_valid_cords(new_cords):
            new_current = current_word+matrix[new_cords[0]][new_cords[1]]

            another_new_visited = visited.copy()

            new_words = search_at_tile(cords=new_cords, current_word=new_current, visited=another_new_visited.copy(), substitutions=substitutions)
            # merge sets
            valid_words.update(new_words)
            
    return valid_words

#checker.visualize_sub_tree()
#print(search_for_words(1)[0:10])
#print(checker.get_possible_letter_subs("fort"))
#print(checker.is_prefix("f"))

#print(search_at_tile((0,4), 'f', set(), 1))

solver = SpellCastSolver()
print(solver.search_for_words(1))
