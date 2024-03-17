from spellCast.solver import SpellCastSolver
from spellCast.spellCastChecker import *
from spellCast.spellCast import *

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()
solver = SpellCastSolver()

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameSettings(BaseModel):
    matrix: list[list[str]]
    double_word: tuple[int, int]|tuple = None
    double_letter: tuple[int, int]|tuple = None
    triple_letter: tuple[int, int]|tuple = None


@app.post("/score/{replacements}", )
async def get_score(replacements : int, settings: GameSettings):
 
    if len(settings.matrix) < 4 or any(len(row) < 4 for row in settings.matrix):
        raise HTTPException(status_code=400, detail="Matrix must be at least 4x4.")

    print(settings.matrix)
    print(settings.double_word)
    print(settings.double_letter)
    print(settings.triple_letter)

    solver.set_game_properties(
        matrix=settings.matrix,
        double_word=settings.double_word,
        double_letter=settings.double_letter,
        triple_letter=settings.triple_letter
    )
    result = solver.search_for_words(replacements)

    if result == None:
        return { "starting_tile" : [] ,"word" : "NONE", "tiles":[], "replaced":[], "score": 0 }
    
    starting_tile, word, tiles, replaced, score = result[0]

    return { "starting_tile": starting_tile, "word" : word, "tiles":tiles, "replaced": replaced, "score": score }
