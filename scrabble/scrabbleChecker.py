from scrabble.scrabble import wordlist, scores
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
        self.initialize()

    def initialize(self):
        for word in wordlist:
            self.prefix_tree.add(word)

    def get_score(self, word):
        s = 0 
        for letter in word: s += scores[letter]
        return s 
    
    def is_word(self, word):
        return word in wordlist
    
    def is_prefix(self, prefix):
        #see if string is a valid prefix of a word 
        
        return self.prefix_tree.get(prefix)