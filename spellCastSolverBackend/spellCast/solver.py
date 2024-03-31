from typing import Self
from spellCast.spellCast import *
from spellCast.spellCastChecker import SpellCastChecker
from spellCast.heap import Heap
import time
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
        self.replacement_bonus = 24
        self.total_subs = 0

        self.max_scores = []
        self.actual_scores = []
        self.game_board_counter = Counter([])

    def set_game_properties(self, matrix=None, double_word=(), double_letter=(), triple_letter=()):
        board_string = ""
        if matrix is not None:
            for y in range(len(matrix)):
                for x in range(len(matrix[y])):
                    letter = matrix[y][x].lower()
                    matrix[y][x] = letter
                    board_string += letter
            self.game_board_counter = Counter(board_string)
            self.matrix = matrix
        if double_word is not None:
            self.double_word = double_word
        if double_letter is not None:
            self.double_letter = double_letter
            self.replacement_bonus = 24
        if triple_letter is not None:
            self.triple_letter = triple_letter
            self.replacement_bonus = 40

    def search_for_words(self, subs: int = 0, testingNovel = False, BruteForce = False):
        t0 = time.time()

        self.heap = Heap()
        self.valid_words = set()
        self.terminated = False

        if (subs >= 1):
            self.checker.create_good_tree(self.game_board_counter, subs)
        else:
            self.checker.stick_with_basic_tree()

        self.max_scores = []
        self.actual_scores = []
        self.total_subs = subs
        self.best_score = 0


        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                letter = self.matrix[y][x]
                score = get_letter_score(
                                letter=letter,
                                cords=(y,x),
                                double_letter=self.double_letter,
                                triple_letter=self.triple_letter)

                if (subs >= 1 and not BruteForce) or testingNovel:
                    add_on = self._get_add_on((y,x), letter)
                    priority, bonus = self._determine_priority(letter, (y, x), set(), add_on)
                    current_backtrack = {
                        "starting_cords": (y,x),
                        "add_on": add_on,
                        "cords": (y,x),
                        "current_word": letter,
                        "visited": set(),
                        "changed": set(),
                        "substitutions": subs,
                        "score": score
                    }
                    self.heap.push((priority, bonus, current_backtrack.copy()))
                    if (subs > 0):         
                        for potential_letter in self.checker.get_possible_letter_subs(""):
                            new_score = get_letter_score(
                                letter=potential_letter,
                                cords=(y,x),
                                double_letter=self.double_letter,
                                triple_letter=self.triple_letter)
                            add_on = self._get_add_on((y,x), potential_letter)
                            priority, bonus = self._determine_priority(potential_letter, (y, x), set(), add_on)
                            current_backtrack = {
                                "starting_cords": (y,x),
                                "add_on": add_on,
                                "cords": (y,x),
                                "current_word": potential_letter,
                                "visited": set(),
                                "changed": set([(y,x)]),
                                "substitutions": subs-1,
                                "score": new_score
                            }
                            self.heap.push((priority, bonus, current_backtrack.copy()))
        
                else:
                    self._search_at_tile((y,x), (y,x), letter, set(), subs, score=score)
                    if (subs > 0):
                        for potential_letter in self.checker.get_possible_letter_subs(""):
                            new_score = get_letter_score(
                                letter=potential_letter,
                                cords=(y,x),
                                double_letter=self.double_letter,
                                triple_letter=self.triple_letter)
                            self._search_at_tile((y,x), (y,x), potential_letter, set(), subs-1, set([(y,x)]), score=new_score)


        while not self.terminated and len(self.heap) > 0:
            self._search_for_best()

        output = list(self.valid_words)
        if len(output) == 0:
            return None

        output.sort(key = lambda x: x[4] - len(x[3]), reverse=True)
        t1 = time.time()

        print("duration for solving:", t1-t0, "seconds")

        f = open("maxscores.txt", "w")
        f.write(str(self.max_scores))
        f.close()
        f = open("actualscores.txt", "w")
        f.write(str(self.actual_scores))
        
        return output

    def is_valid_cords(self, cords):
        if cords[0] < 0 or cords[0] >= len(self.matrix) or cords[1] < 0 or cords[1] >= len(self.matrix[cords[0]]):
            return False
        return True

    def _search_at_tile(self, starting_cords, cords, current_word, visited, substitutions=0, changed=set(), score = 0):
          #self, starting_cords, cords, current_word, visited, substitutions=0, changed=set(), score = 0

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
                              self._search_at_tile(
                                                  starting_cords=starting_cords,
                                                  cords=new_cords,
                                                  current_word=new_current,
                                                  visited=new_visited.copy(),
                                                  substitutions=substitutions-1,
                                                  changed=new_changed.copy(),
                                                  score=new_score)


          if not self.checker.is_prefix(current_word):
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

                  self._search_at_tile(
                      starting_cords=starting_cords,
                      cords=new_cords,
                      current_word=new_current,
                      visited=another_new_visited.copy(),
                      substitutions=substitutions,
                      changed=changed.copy(),
                      score=new_score)
                  # merge sets

    def _search_for_best(self):
        neighbours = [(-1, 0), (1, 0), (-1, 1), (1, 1), (0, -1), (0, 1), (1,-1), (-1,-1)]
        priority, bonus, current_backtrack = self.heap.pop()

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
        add_on = current_backtrack["add_on"]

        if cords in visited:
            return
        visited.add(cords)

        # have we reached the best?
        self._should_terminate(visited, priority, bonus, current_word)

        if substitutions > 0:
            for potential_letter in self.checker.get_possible_letter_subs(current_word):
                new_current = current_word + potential_letter

                if self.checker.is_prefix(current_word) == False:
                    continue

                for add_y, add_x in neighbours:
                    new_visited = type(visited)(visited)

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

                        new_addon = add_on
                        if (add_on == (0,1)):
                            new_addon = self._get_add_on(new_cords, potential_letter)

                        new_priority, new_bonus = self._determine_priority(new_current, new_cords, visited, new_addon)

                        new_backtrack = {}
                        new_backtrack["score"] = new_score
                        new_backtrack["add_on"] = new_addon
                        new_backtrack["starting_cords"] = starting_cords
                        new_backtrack["visited"] = new_visited
                        new_backtrack["substitutions"] = substitutions-1
                        new_backtrack["changed"] = new_changed.copy()
                        new_backtrack["current_word"] = new_current
                        new_backtrack["cords"] = new_cords

                        self.heap.push((new_priority, new_bonus, new_backtrack.copy()))

        if not self.checker.is_prefix(current_word):
            return

        if self.checker.is_word(current_word):
            path_taken = visited
            current_score = get_final_score(
                score=score,
                traversal=path_taken,
                double_word=self.double_word
                )

            self.valid_words.add((tuple(starting_cords), str(current_word), tuple(path_taken), tuple(changed), int(current_score)))

            #if (self.checker.is_leaf_word(current_word)):
            self.best_score = max(self.best_score, current_score)
            '''
                if (self._used_double_or_triple(visited) and
                        self._used_double_word(visited)):
                    self.terminated = True
            '''

        # check the next step Moore neighborhood
        for add_y, add_x in neighbours:
            new_cords = (cords[0]+add_y, cords[1]+add_x)

            if self.is_valid_cords(new_cords):
                new_letter = self.matrix[new_cords[0]][new_cords[1]]
                new_current = current_word+new_letter

                if not self.checker.is_prefix(current_word):
                    continue

                new_score = score
                new_score += get_letter_score(
                    letter=new_letter,
                    cords=new_cords,
                    double_letter=self.double_letter,
                    triple_letter=self.triple_letter)

                new_visited = type(visited)(visited)

                new_addon = add_on
                if (add_on == (0,1)):
                    new_addon = self._get_add_on(new_cords, new_letter)

                new_backtrack = {}
                new_backtrack["starting_cords"] = starting_cords
                new_backtrack["score"] = new_score
                new_backtrack["add_on"] = new_addon
                new_backtrack["visited"] = new_visited
                new_backtrack["substitutions"] = substitutions
                new_backtrack["current_word"] = new_current
                new_backtrack["cords"] = new_cords
                new_backtrack["changed"] = changed.copy()

                new_priority, new_bonus = self._determine_priority(new_current, new_cords, new_visited, new_addon)

                self.heap.push((new_priority, new_bonus, new_backtrack.copy()))

    def _should_terminate(self, visited, expected_score, expected_length, word):
        bonus_length_score = 10 if expected_length >= 6 else 0
        expected_score_without_bonus = expected_score - bonus_length_score
        self.actual_scores.append(expected_score)
        self.max_scores.append(self.best_score)

        if (not self._used_double_or_triple(visited) and
                      self._used_double_word(visited) and
                      expected_score + self.replacement_bonus + 24 + bonus_length_score <= self.best_score):
            # this constant can change
            print("top")
            print(visited)
            print(word)
            print(self.best_score)
            print("gains", expected_score + self.replacement_bonus )
            self.terminated = True

        if ((expected_score_without_bonus)*2 + bonus_length_score + self.replacement_bonus <= self.best_score):
            print("bottom")
            print(visited)
            print(word)
            self.terminated = True

    def get_solutions(self):
        return list(self.valid_words)

    def _used_double_or_triple(self, visited):
        return (self.double_letter in visited or self.triple_letter in visited)

    def _used_double_word(self, visited):
        return (self.double_word in visited)

    def _get_add_on(self, cords, letter):
        if cords == self.double_letter:
            return (get_raw_score(letter), 2)
        if cords == self.triple_letter:
            return (get_raw_score(letter), 3)
        return (0,1)

    def _determine_priority(self, word, cords, visited, addon = (0,1)):
        addition, multiplier = addon
        double_multiplier = 1
        if cords == self.double_word or self.double_word in visited:
            double_multiplier = 2
        node = self.checker.get(word)
        priority = 0
        bonus = 0
        if node != None:
          priority = node.priority
          bonus = 10 if len(node.value) >= 6 else 0
        return ((priority + (addition * multiplier)) * double_multiplier - addition + bonus, bonus)
