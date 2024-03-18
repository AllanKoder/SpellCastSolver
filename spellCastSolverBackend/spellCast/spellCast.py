# scrabble.py module, imported by scrabble_words.py
#
# Read sowpods.txt file, which is a list of some 260,000 valid english words 
# for Scrabble game 
#
WORD_LIST = "spellCast/sowpods.txt"
MINIMUM_GOOD_SCORE = 1
MINIMUM_BETTER_SCORE = 1

# set up a dictionary of points for each letter, to be used to calculate scores

scores = {
    "a": 1,
    "b": 4,
    "c": 5,
    "d": 3,
    "e": 1,
    "f": 5,
    "g": 3,
    "h": 4,
    "i": 1,
    "j": 7,
    "k": 3,
    "l": 3,
    "m": 4,
    "n": 2,
    "o": 1,
    "p": 4,
    "q": 8,
    "r": 2,
    "s": 2,
    "t": 2,
    "u": 4,
    "v": 5,
    "w": 5,
    "x": 7,
    "y": 4,
    "z": 8,
}

def get_raw_score(word):
    word = word.lower().strip()
    s = 0 
    for letter in word: s += scores[letter]
    return s 

def get_letter_score(letter : str, cords: tuple[int,int], double_letter: set[tuple], triple_letter: set[tuple]):
    s = scores[letter]
    if cords == double_letter:
        s *= 2
    if cords == triple_letter:
        s *= 3
    return s 

def get_final_score(score: int, traversal: set[tuple], double_word : tuple):
    double_multiplier = 1
    if double_word in traversal:
        double_multiplier = 2
    add_on = (0 if len(traversal) < 6 else 10) 
    final_score = (score*double_multiplier) + add_on 
    print(final_score, add_on, score*double_multiplier, score)
    return final_score
    
wordlist = open(WORD_LIST).readlines()
# Get rid of newlines
wordlist = set([word.lower().strip() for word in wordlist if get_raw_score(word) >= MINIMUM_GOOD_SCORE])
better_wordlist = set([word for word in wordlist if get_raw_score(word) >= MINIMUM_BETTER_SCORE])


