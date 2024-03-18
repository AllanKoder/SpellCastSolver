from spellCast.spellCast import get_final_score, get_letter_score
from spellCast.spellCastChecker import SpellCastChecker

class SpellCastSolver:
    def __init__(self, matrix=None):
        self.checker = SpellCastChecker()

        self.valid_words = set()
        self.matrix = [
            ['e', 'u', 'i', 'r', 't'],
            ['u', 'f', 'j', 'i', 't'],
            ['h', 'n', 'y', 'g', 'u'],
            ['f', 'o', 'd', 'i', 'e'],
            ['a', 'e', 'a', 'o', 'q'],
        ]
        self.double_word = ()
        self.double_letter = ()
        self.triple_letter = ()
        
    def set_game_properties(self, matrix=None, double_word=None, double_letter=None, triple_letter=None):
        if matrix is not None:
            for y in range(len(matrix)):
                for x in range(len(matrix[y])):
                    matrix[y][x] = matrix[y][x].lower()
            self.matrix = matrix
        if double_word is not None:
            self.double_word = double_word
        if double_letter is not None:
            self.double_letter = double_letter
        if triple_letter is not None:
            self.triple_letter = triple_letter

    def search_for_words(self, subs: int = 0):
        self.valid_words = set()
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                letter = self.matrix[y][x]
                score = get_letter_score(
                                letter=letter,
                                cords=(y,x),
                                double_letter=self.double_letter,
                                triple_letter=self.triple_letter)
                self.search_at_tile((y,x), (y,x), letter, set(), subs, score=score)
        
        output = list(self.valid_words)
        if len(output) == 0:
            return None
        
        output.sort(key = lambda x: x[4] - len(x[3]), reverse=True)
        return output

    def is_valid_cords(self, cords):
        if cords[0] < 0 or cords[0] >= len(self.matrix) or cords[1] < 0 or cords[1] >= len(self.matrix[cords[0]]): 
            return False
        return True

    def search_at_tile(self, starting_cords, cords, current_word, visited, substitutions=0, changed=set(), score = 0):
        #return set of (startingCords, word, path to get word, dictionary of cord to the changed letter, score)  
        neighbours = [(-1, 0), (1, 0), (-1, 1), (1, 1), (0, -1), (0, 1), (1,-1), (-1,-1)]
        if cords in visited:
            return
        # deal with repeats
        visited.add(cords)
    
        # deal with substitutions
        if substitutions > 0:
                new_visited = visited.copy()
                
                for potential_letter in self.checker.get_possible_letter_subs(current_word):
                    new_current = current_word + potential_letter                    
                    
                    for add_y, add_x in neighbours:
                        new_score = score

                        new_cords = (cords[0]+add_y, cords[1]+add_x)
                        new_changed = changed.copy()
                        new_changed.add(new_cords)

                        if self.is_valid_cords(new_cords):
                            new_score += get_letter_score(
                                letter=potential_letter,
                                cords=new_cords,
                                double_letter=self.double_letter,
                                triple_letter=self.triple_letter)
                            self.search_at_tile(
                                                starting_cords=starting_cords, 
                                                cords=new_cords, 
                                                current_word=new_current, 
                                                visited=new_visited.copy(), 
                                                substitutions=substitutions-1, 
                                                changed=new_changed, 
                                                score=new_score)
                    

        if self.checker.is_prefix(current_word) == False:
            return
        
        if self.checker.is_word(current_word):
            path_taken = visited.copy()
            current_score = get_final_score(
                score=score,
                traversal=path_taken,
                double_word=self.double_word
                )
            self.valid_words.add((tuple(starting_cords), str(current_word), tuple(path_taken), tuple(changed), int(current_score)))


        for add_y, add_x in neighbours:
            new_cords = (cords[0]+add_y, cords[1]+add_x)

            if self.is_valid_cords(new_cords):
                new_letter = self.matrix[new_cords[0]][new_cords[1]]
                new_current = current_word+new_letter

                another_new_visited = visited.copy()

                new_score = score
                new_score += get_letter_score(
                    letter=new_letter,
                    cords=new_cords,
                    double_letter=self.double_letter,
                    triple_letter=self.triple_letter)

                self.search_at_tile(
                    starting_cords=starting_cords, 
                    cords=new_cords, 
                    current_word=new_current, 
                    visited=another_new_visited.copy(), 
                    substitutions=substitutions, 
                    changed=changed,
                    score=new_score)
                # merge sets

    def get_solutions(self):
        return list(self.valid_words)