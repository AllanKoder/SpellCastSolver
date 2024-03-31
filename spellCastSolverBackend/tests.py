from collections import Counter

from spellCast.spellCast import enough_words


c1 = Counter("abcds")
board = Counter("abcd")
print(enough_words(c1, board, 1) == True)
print(enough_words(Counter("as"), board, 1) == True)
print(enough_words(Counter("abcdsae"), board, 1) == False)
print(enough_words(Counter("cats"), board, 1) == False)
print(enough_words(Counter("act"), board, 1) == True)
print(enough_words(Counter("acts"), board, 2) == True)
print(enough_words(Counter("acts"), board, 0) == False)
