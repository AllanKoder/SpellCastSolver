from spellCast.solver import SpellCastSolver
from spellCast.spellCastChecker import *
from spellCast.spellCast import *


solver = SpellCastSolver()

solver.set_game_properties(
        matrix=[["b","a","b","a","a"],
                ["a","a","a","a","a"],
                ["a","a","a","a","a"],
                ["a","a","a","a","a"],
                ["a","a","a","a","a"]]
        )

solver.search_for_words(1)
results = solver.get_solutions()
print(results)