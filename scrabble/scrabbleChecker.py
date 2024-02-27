from scrabble.scrabble import *
from collections import defaultdict
import graphviz

class PrefixNode:
    def __init__(self, value=""):
        self.value = value
        self.pathing = {}

    def get_or_create_child(self, letter):
        if self.pathing.get(letter) == None:
            self.pathing[letter] = PrefixNode(self.value + letter)
        return self.pathing[letter]
    
    def get(self, letter):
        if self.pathing.get(letter) != None:
            return self.pathing[letter]
        return None
    

class PrefixTree:
    def __init__(self):
        self.root = PrefixNode()

    def add(self, word: str):
        currentNode = self.root
        for letter in word:
            currentNode = currentNode.get_or_create_child(letter)
    
    def get(self, word: str):
        # either return true or false 
        currentNode = self.root
        createdString = ""
        for letter in word:
            if not currentNode: break
            createdString += letter
            currentNode = currentNode.get(letter)

        if currentNode == None: return False
        return currentNode.value == word
    
    def get_next_letters(self, word: str) -> list[str]:
        # return a list of letters
        currentNode = self.root
        createdString = ""
        for letter in word:
            if not currentNode: break
            createdString += letter
            currentNode = currentNode.get(letter)

        if currentNode == None: return []
        return list(currentNode.pathing.keys())

    def visualize(self):
        dot = graphviz.Digraph()
        self._visualize_helper(self.root, dot)
        dot.render('trie_visualization', format='png', cleanup=True)

    def _visualize_helper(self, node, dot):
        for letter, child in node.pathing.items():
            dot.node(child.value, label=child.value)
            dot.edge(node.value, child.value, label=letter)
            self._visualize_helper(child, dot)


class ScrabbleChecker:
    def __init__(self):
        self.prefix_tree = PrefixTree()
        self.prefix_sub_1_tree = PrefixTree()
        self.initializeRoots()

    def initializeRoots(self):
        for word in wordlist:
            self.prefix_tree.add(word)
        for word in better_wordlist:
            self.prefix_sub_1_tree.add(word)
    
    def is_word(self, word):
        return word in wordlist
    
    def is_prefix(self, prefix):
        #see if string is a valid prefix of a word     
        return self.prefix_tree.get(prefix)
    
    def get_possible_letter_subs(self, prefix):
        #get the possible letters that can sub in for a valid prefix given a prefix
        return self.prefix_sub_1_tree.get_next_letters(prefix[0:len(prefix)-1])
