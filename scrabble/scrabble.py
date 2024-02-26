# scrabble.py module, imported by scrabble_words.py
#
# Read sowpods.txt file, which is a list of some 260,000 valid english words 
# for Scrabble game 
#
WORD_LIST = "scrabble/sowpods.txt"

wordlist = open(WORD_LIST).readlines()
# Get rid of newlines
wordlist = set([word.lower().strip() for word in wordlist])

# set up a dictionary of points for each letter, to be used to calculate scores
scores = {"a": 1, "c": 3, "b": 4, "e": 1, "d": 2, "g": 2,
          "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 4,
          "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
          "r": 2, "u": 1, "t": 1, "w": 5, "v": 5, "y": 4,
          "x": 8, "z": 10}
