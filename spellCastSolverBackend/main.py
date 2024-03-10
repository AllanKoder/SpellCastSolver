from spellCast.solver import SpellCastSolver
from spellCast.spellCastChecker import *
from spellCast.spellCast import *

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
solver = SpellCastSolver()

class GameSettings(BaseModel):
    matrix: list[list[str]]
    double_word: tuple[int, int] = None
    double_letter: tuple[int, int] = None
    triple_letter: tuple[int, int] = None



@app.post("/score/{replacements}", )
async def get_score(replacements : int, settings: GameSettings):
 
    if len(settings.matrix) < 4 or any(len(row) < 4 for row in settings.matrix):
        raise HTTPException(status_code=400, detail="Matrix must be at least 4x4.")

    print(settings.matrix)

    solver.set_game_properties(
        matrix=settings.matrix,
        double_word=settings.double_word,
        double_letter=settings.double_letter,
        triple_letter=settings.triple_letter
    )
    return { "solution" : solver.search_for_words(replacements)[0] }
