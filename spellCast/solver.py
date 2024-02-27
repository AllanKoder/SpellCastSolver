from spellCast.spellCast import get_score
from spellCast.spellCastChecker import SpellCastChecker

class SpellCastSolver:
    def __init__(self, matrix=None):
        self.checker = SpellCastChecker()

        self.valid_words = set()
        self.matrix = [
            ['a', 'a', 'a', 'o', 'f'],
            ['a', 'a', 'a', 'a', 'a'],
            ['a', 'a', 'c', 'k', 'e'],
            ['a', 'a', 'l', 's', 'r'],
            ['a', 'a', 'a', 'a', 'a'],
        ]
        self.double_word = (2,2)
        self.double_letter = ()
        self.triple_letter = ()
    '''
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
    '''
    def search_for_words(self, subs: int = 0):
        self.valid_words = set()
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                letter = self.matrix[y][x]
                results = self.search_at_tile((y,x), letter, set(), subs)
        output = list(self.valid_words)
        output.sort(key = lambda x: x[3] - len(x[2]), reverse=True)
        return output

    def is_valid_cords(self, cords):
        if cords[0] < 0 or cords[0] >= len(self.matrix) or cords[1] < 0 or cords[1] >= len(self.matrix[cords[0]]): 
            return False
        return True

    def search_at_tile(self, cords, current_word, visited, substitutions=0, changed=set()):
        #return set of (word, path to get word, dictionary of cord to the changed letter, score)  
        if cords in visited:
            return
        visited.add(cords)
    

        # deal with substitutions
        if substitutions > 0:
            prefix_word = current_word[0:len(current_word)-1]
            new_visited = visited.copy()
            new_visited.remove(cords)
            
            for potential_letter in self.checker.get_possible_letter_subs(current_word):
                new_current = prefix_word + potential_letter
                new_changed = changed.copy()
                new_changed.add(cords)
                new_words = self.search_at_tile(cords=cords, current_word=new_current, visited=new_visited.copy(), substitutions=substitutions-1, changed=new_changed)
                
        if self.checker.is_prefix(current_word) == False:
            return
        
        if self.checker.is_word(current_word):
            path_taken = visited.copy()
            current_score = get_score(traversal=visited, matrix=self.matrix, double_word=self.double_word, double_letter=self.double_letter, triple_letter=self.triple_letter)
            self.valid_words.add((str(current_word), tuple(path_taken), tuple(changed), int(current_score)))


        neighbours = [(-1, 0), (1, 0), (-1, 1), (1, 1), (0, -1), (0, 1), (1,-1), (-1,-1)]
        for add_y, add_x in neighbours:
            new_cords = (cords[0]+add_y, cords[1]+add_x)

            if self.is_valid_cords(new_cords):
                new_current = current_word+self.matrix[new_cords[0]][new_cords[1]]

                another_new_visited = visited.copy()

                new_words = self.search_at_tile(cords=new_cords, current_word=new_current, visited=another_new_visited.copy(), substitutions=substitutions)
                # merge sets

    def get_solutions(self):
        return self.valid_words