from spellCast.spellCast import *
from spellCast.spellCastChecker import SpellCastChecker
from spellCast.heap import Heap

class SpellCastSolver:
    def __init__(self, matrix=None):
        self.checker = SpellCastChecker()

        self.heap = Heap()
        self.valid_words = set()
        self.terminated = False
        self.best_score = 0

        self.matrix = matrix
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
        self.heap = Heap()
        self.valid_words = set()
        self.terminated = False
        self.best_score = 0
        
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                letter = self.matrix[y][x]
                score = get_letter_score(
                                letter=letter,
                                cords=(y,x),
                                double_letter=self.double_letter,
                                triple_letter=self.triple_letter)
                priority = self._determine_priority(letter, (y, x), set())
                current_backtrack = {
                    "starting_cords": (y,x),
                    "cords": (y,x),
                    "current_word": letter,
                    "visited": set(),
                    "changed": set(),
                    "substitutions": subs,
                    "score": score
                }
                self.heap.push((priority, current_backtrack.copy()))
        
        while self.terminated == False and len(self.heap) > 0:
            self.search_for_best()

        output = list(self.valid_words)
        if len(output) == 0:
            return None
        
        output.sort(key = lambda x: x[4] - len(x[3]), reverse=True)
        return output

    def is_valid_cords(self, cords):
        if cords[0] < 0 or cords[0] >= len(self.matrix) or cords[1] < 0 or cords[1] >= len(self.matrix[cords[0]]): 
            return False
        return True

    def search_for_best(self):
        neighbours = [(-1, 0), (1, 0), (-1, 1), (1, 1), (0, -1), (0, 1), (1,-1), (-1,-1)]
        priority, current_backtrack = self.heap.pop()
        
        '''
            "starting_cords": (y,x),
            "cords": (y,x),
            "current_word": letter,
            "visited": set(),
            "changed": set(),
            "substitutions": subs,
            "score": score
        '''
        starting_cords = current_backtrack["starting_cords"]
        cords = current_backtrack["cords"]
        visited = current_backtrack["visited"]
        substitutions = current_backtrack["substitutions"] 
        current_word = current_backtrack["current_word"] 
        changed = current_backtrack["changed"] 
        score = current_backtrack["score"]
        
        if cords in visited:
            return
        visited.add(cords)

        if substitutions > 0:
                new_visited = visited.copy()
                
                for potential_letter in self.checker.get_possible_letter_subs(current_word):
                    new_current = current_word + potential_letter                    

                    for add_y, add_x in neighbours:
                        new_score = score

                        new_cords = (cords[0]+add_y, cords[1]+add_x)
                        new_changed = changed.copy()
                        new_changed.add(new_cords)

                        new_priority = self._determine_priority(new_current, new_cords, visited)

                        if self.is_valid_cords(new_cords):
                            new_score += get_letter_score(
                                letter=potential_letter,
                                cords=new_cords,
                                double_letter=self.double_letter,
                                triple_letter=self.triple_letter)
                            '''
                            self.search_at_tile(
                                starting_cords=starting_cords, 
                                cords=new_cords, 
                                current_word=new_current, 
                                visited=new_visited.copy(), 
                                substitutions=substitutions-1, 
                                changed=new_changed, 
                                score=new_score)
                            '''
                            new_backtrack = current_backtrack.copy()
                            new_backtrack["score"] = new_score
                            new_backtrack["visited"] = new_visited.copy()
                            new_backtrack["substitutions"] = substitutions-1
                            new_backtrack["changed"] = new_changed.copy()
                            new_backtrack["current_word"] = new_current
                            new_backtrack["cords"] = new_cords

                            self.heap.push((new_priority, new_backtrack.copy()))

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
            
            if (self.checker.is_leaf_word(current_word)):
                if (self._used_double_or_triple(visited) and 
                    self._used_double_word(visited)):
                    self.terminated = True
                
                elif (self._used_double_or_triple(visited) and 
                      not self._used_double_word(visited) and 
                      current_score * 2 <= self.best_score):
                    self.terminated = True

                elif (not self._used_double_or_triple(visited) and
                      self._used_double_word(visited) and 
                      current_score + 20 <= self.best_score):
                    self.terminated = True

                elif (not self._used_double_or_triple(visited) and
                      not self._used_double_word(visited) and 
                      current_score*2 + 20 <= self.best_score):
                    self.terminated = True

            self.best_score = max(self.best_score, current_score)



        for add_y, add_x in neighbours:
            new_cords = (cords[0]+add_y, cords[1]+add_x)

            if self.is_valid_cords(new_cords):
                new_letter = self.matrix[new_cords[0]][new_cords[1]]
                new_current = current_word+new_letter

                new_visited = visited.copy()

                new_score = score
                new_score += get_letter_score(
                    letter=new_letter,
                    cords=new_cords,
                    double_letter=self.double_letter,
                    triple_letter=self.triple_letter)
            
                new_backtrack = current_backtrack.copy()
                new_backtrack["score"] = new_score
                new_backtrack["visited"] = new_visited.copy()
                new_backtrack["substitutions"] = substitutions
                new_backtrack["current_word"] = new_current
                new_backtrack["cords"] = new_cords
                new_backtrack["changed"] = changed.copy()

                new_priority = self._determine_priority(new_current, new_cords, new_visited)

                self.heap.push((new_priority, new_backtrack.copy()))
     
    def get_solutions(self):
        return list(self.valid_words)

    def _used_double_or_triple(self, visited):
        return (self.double_letter in visited or self.triple_letter in visited)
    
    def _used_double_word(self, visited):
        return (self.double_word in visited)
    
    def _determine_priority(self, word, cords, visited):
        double_multiplier = 1 
        if self.double_word in visited or cords == self.double_word:
            double_multiplier = 2
        
        return self.checker.get_priority(word)*double_multiplier
