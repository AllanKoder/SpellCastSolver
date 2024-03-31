import unittest

from spellCast.solver import SpellCastSolver
from spellCast.spellCastChecker import *
from spellCast.spellCast import *

from collections import Counter
from spellCast.spellCast import enough_words

solver = SpellCastSolver()

class TestEnoughCounter(unittest.TestCase):
    def test_enough_words_works(self):
        c1 = Counter("abcds")
        board = Counter("abcd")
        assert (enough_words(c1, board, 1) is True)
        assert (enough_words(Counter("as"), board, 1) is True)
        assert (enough_words(Counter("abcdsae"), board, 1) is False)
        assert (enough_words(Counter("cats"), board, 1) is False)
        assert (enough_words(Counter("act"), board, 1) is True)
        assert (enough_words(Counter("acts"), board, 2) is True)
        assert (enough_words(Counter("acts"), board, 0) is False)


class TestSpellCastSolver(unittest.TestCase):
    @classmethod
    def setUp(self):
        solver.set_game_properties(
            matrix=None,
            double_letter=(),
            triple_letter=(),
            double_word=(),
        )
  
    def test_zero_substituions_chiarezza(self):
        solver.set_game_properties(
            matrix=[
                ["a","c","a","a","a"],
                ["a","h","a","a","a"],
                ["a","i","a","a","a"],
                ["a","a","r","e","z"],
                ["a","a","a","z","a"],
                
            ]
        )
        result = solver.search_for_words()
        starting_tile, word, tiles, replaced, score = result[0]
        
        self.assertEqual(score, 41, "should solve for chiarezza")
        self.assertEqual(word, "chiarezza", "should solve for chiarezza")
      
    def test_zero_substituions_dl_dw_bedfast(self):
        solver.set_game_properties(
            matrix=[['d', 'f', 'd', 's', 's'], ['d', 'z', 'z', 'd', 'e'], ['A', 'a', 'f', 'd', 'w'], ['e', 'f', 's', 'd', 'e'], ['w', 'r', 't', 'b', 'b']],
            double_letter=(3,2),
            double_word=(2,3)
        )
        result = solver.search_for_words()
        starting_tile, word, tiles, replaced, score = result[0]
        
        self.assertEqual(score, 50, "should solve for bedfast")
        self.assertEqual(word, "bedfast", "should solve for bedfast")

    def test_zero_substituions_tl_dw_bedfast(self):
        solver.set_game_properties(
            matrix=[['d', 'f', 'd', 's', 's'], ['d', 'z', 'z', 'd', 'e'], ['A', 'a', 'f', 'd', 'w'], ['e', 'f', 's', 'd', 'e'], ['w', 'r', 't', 'b', 'b']],
            triple_letter=(3,2),
            double_word=(2,3)
        )
        result = solver.search_for_words()
        starting_tile, word, tiles, replaced, score = result[0]
        
        self.assertEqual(score, 54, "should solve for bedfast")
        self.assertEqual(word, "bedfast", "should solve for bedfast")

    # best answer is the same as the bruteforce
    def bruteforce_vs_heap(self, matrix, triple_letter = (), double_letter = (), double_word = (), subs=1):
        solver.set_game_properties(
            matrix=matrix,
            triple_letter=triple_letter,
            double_letter=double_letter,
            double_word=double_word
        )
        expected = solver.search_for_words(subs=subs, BruteForce=True, testingNovel=False)
        _, expected_word, _, _, expected_score = expected[0]

        actual = solver.search_for_words(subs=subs, testingNovel=True, BruteForce=False)
        _, actual_word, _, _, actual_score = actual[0]
        return expected_score,actual_score
        
    def test_one_substituion_same_one(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['d', 'f', 'z', 'u', 'c'], ['d', 'z', 't', 'e', 'h'], ['A', 'a', 't', 'w', 'z'], ['e', 'a', 's', 'd', 'e'], ['w', 'e', 'z', 'z', 'b']],
            triple_letter=(0,2),
            double_word=(0,3)
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_one_substituion_same_two(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['d', 'f', 'z', 'q', 'a'], ['a', 'y', 'u', 'j', 'k'], ['b', 'a', 'q', 'x', 'z'], ['e', 'a', 'p', 'u', 'e'], ['k', 'i', 'a', 'v', 'h']],
            triple_letter=(4,2),
            double_word=(1,3),
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_one_substituion_same_three(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['Q', 'W', 'D', 'S', 'D'], ['G', 'N', 'Z', 'S', 'A'], ['J', 'B', 'E', 'F', 'S'], ['D', 'X', 'L', 'A', 'S'], ['N', 'G', 'N', 'E', 'F']],
            triple_letter=(2,1),
            double_word=(2,3),
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_one_substituion_same_four(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['Q', 'W', 'D', 'S', 'D'], ['Z', 'Z', 'X', 'Z', 'A'], ['A', 'B', 'Y', 'V', 'S'], ['D', 'Z', 'A', 'Z', 'S'], ['N', 'S', 'N', 'E', 'F']],
            triple_letter=(2,1),
            double_word=(2,3),
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_one_substituion_same_five(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['A', 'W', 'D', 'A', 'S'], ['A', 'Z', 'X', 'V', 'X'], ['C', 'V', 'X', 'C', 'B'], ['F', 'D', 'H', 'E', 'T'], ['R', 'H', 'D', 'F', 'H']],
            double_word=(4,0),
            triple_letter=(3,4),
        )

        self.assertEqual(expected_score, actual_score, "should be same score")
  
    def test_two_substituion_same_one(self):
      expected_score, actual_score = self.bruteforce_vs_heap(
          matrix=[['d', 'f', 'z', 'u', 'c'], ['d', 'z', 't', 'e', 'h'], ['A', 'a', 't', 'w', 'z'], ['e', 'a', 's', 'd', 'e'], ['w', 'e', 'z', 'z', 'b']],
          triple_letter=(0,2),
          double_word=(0,3),
          subs=2
      )

      self.assertEqual(expected_score, actual_score, "should be same score")

    def test_two_substituion_same_two(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['d', 'f', 'z', 'q', 'a'], ['a', 'y', 'u', 'j', 'k'], ['b', 'a', 'q', 'x', 'z'], ['e', 'a', 'p', 'u', 'e'], ['k', 'i', 'a', 'v', 'h']],
            triple_letter=(4,2),
            double_word=(1,3),
            subs=2
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_two_substituion_same_three(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['A', 'E', 'A', 'V', 'C'], ['G', 'N', 'Z', 'S', 'A'], ['J', 'B', 'E', 'F', 'S'], ['D', 'X', 'L', 'A', 'S'], ['N', 'G', 'N', 'E', 'F']],
            triple_letter=(2,1),
            double_word=(2,3),
            subs=2
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_two_substituion_same_four(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['Q', 'W', 'D', 'S', 'D'], 
                    ['Z', 'Z', 'X', 'Z', 'A'], 
                    ['A', 'B', 'Y', 'V', 'S'], 
                    ['D', 'Z', 'A', 'Z', 'S'], 
                    ['N', 'S', 'N', 'E', 'F']],
            triple_letter=(2,1),
            double_word=(2,3),
            subs=2
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_two_substituion_same_five(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['A', 'W', 'D', 'A', 'S'], ['A', 'Z', 'X', 'V', 'X'], ['C', 'V', 'X', 'C', 'B'], ['F', 'D', 'H', 'E', 'T'], ['R', 'H', 'D', 'F', 'H']],
            double_word=(4,0),
            triple_letter=(3,4),
            subs=2
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_two_substituion_same_six(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['A', 'S', 'H', 'W', 'B'], ['J', 'A', 'K', 'J', 'D'], ['H', 'F', 'A', 'W', 'B'], ['B', 'E', 'F', 'A', 'G'], ['I', 'J', 'S', 'D', 'Z']],
            double_word=(3,3),
            double_letter=(1,1),
            subs=2
        )

        self.assertEqual(expected_score, actual_score, "should be same score")

    def test_two_substituion_same_seven(self):
        expected_score, actual_score = self.bruteforce_vs_heap(
            matrix=[['c', 'v', 'v', 'i', 'u'], ['s', 'd', 'j', 'l', 'd'], ['H', 'a', 's', 'f', 'g'], ['i', 'h', 'j', 'j', 'G'], ['e', 'r', 'S', 't', 'w']],
            double_word=(4,0),
            double_letter=(1,4),
            subs=2
        )

        self.assertEqual(expected_score, actual_score, "should be same score")


    # def test_three_substituion_same_one(self):
    #     expected_score, actual_score = self.bruteforce_vs_heap(
    #         matrix=[['A', 'S', 'H', 'W', 'B'], ['J', 'A', 'K', 'J', 'D'], ['H', 'F', 'A', 'W', 'B'], ['B', 'E', 'F', 'A', 'G'], ['I', 'J', 'S', 'D', 'Z']],
    #         double_word=(3,3),
    #         double_letter=(1,1),
    #         subs=3
    #     )

    #     self.assertEqual(expected_score, actual_score, "should be same score")

    # def test_three_substituion_same_two(self):
    #     expected_score, actual_score = self.bruteforce_vs_heap(
    #         matrix=[['c', 'v', 'v', 'i', 'u'], ['s', 'd', 'j', 'l', 'd'], ['H', 'a', 's', 'f', 'g'], ['i', 'h', 'j', 'j', 'G'], ['e', 'r', 'S', 't', 'w']],
    #         double_word=(4,0),
    #         double_letter=(1,4),
    #         subs=3
    #     )

    #     self.assertEqual(expected_score, actual_score, "should be same score")



if __name__ == '__main__':
  unittest.main(failfast=False)
