from spellCast.solver import SpellCastSolver
from spellCast.spellCastChecker import *
from spellCast.spellCast import *


solver = SpellCastSolver()

solver.set_game_properties(
        matrix=[["q","u","e","a","a"],
                ["e","a","a","a","a"],
                ["h","a","a","a","a"],
                ["c","a","a","a","a"],
                ["a","a","a","a","a"]]
        )

solver.search_for_words(0)
results = solver.get_solutions()
for result in results:
        print(results[1], results[4])
