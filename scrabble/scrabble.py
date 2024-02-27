# scrabble.py module, imported by scrabble_words.py
#
# Read sowpods.txt file, which is a list of some 260,000 valid english words 
# for Scrabble game 
#
WORD_LIST = "scrabble/test.txt"
MINIMUM_BETTER_SCORE = 1

# set up a dictionary of points for each letter, to be used to calculate scores
scores = {"a": 1, "c": 5, "b": 4, "e": 1, "d": 3, "g": 3,
          "f": 5, "i": 1, "h": 4, "k": 6, "j": 7, "m": 4,
          "l": 3, "o": 1, "n": 2, "q": 8, "p": 4, "s": 2,
          "r": 2, "u": 4, "t": 2, "w": 5, "v": 5, "y": 4,
          "x": 7, "z": 8}

def get_raw_score(word):
    s = 0 
    for letter in word: s += scores[letter]
    return s 

def get_multiplier(cord: tuple, double_letter: set[tuple], triple_letter: set[tuple]):
    output = 1
    if cord == double_letter:
        output = 2
    if cord == triple_letter:
        output = 3
    return output

def get_score(traversal: set[tuple], matrix: list[list[str]], double_word : tuple, double_letter: tuple, triple_letter: tuple):
    score = 0
    double_multiplier = 1
    if double_word in traversal:
        double_multiplier = 2
    for y,x in traversal:
        letter = matrix[y][x]
        score += scores[letter] * get_multiplier((y,x), double_letter, triple_letter)
    return score*double_multiplier
    

wordlist = open(WORD_LIST).readlines()
# Get rid of newlines
wordlist = set([word.lower().strip() for word in wordlist])
better_wordlist = set([word for word in wordlist if get_raw_score(word) >= MINIMUM_BETTER_SCORE])


