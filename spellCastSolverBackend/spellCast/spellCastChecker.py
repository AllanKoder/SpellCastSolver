from spellCast.spellCast import *
import graphviz
from functools import lru_cache 

class PrefixNode:
    def __init__(self, value=""):
        self.value = value
        self.best_priority_score = 0
        self.parent = None
        self.pathing = {}
        self.priority = 0

    def get_or_create_child(self, letter : str, score: int):
        if self.pathing.get(letter) == None:
            new_node = PrefixNode(self.value + letter)
            self.pathing[letter] = new_node
            
            new_node.parent = self
            new_node.priority = score

        return self.pathing[letter]
    
    def is_leaf_node(self):
        return len(self.pathing) > 0
    
    def get(self, letter):
        if self.pathing.get(letter) != None:
            return self.pathing[letter]
        return None
    

class PrefixTree:
    def __init__(self):
        self.root = PrefixNode()

    def reprioritize(self, node):
        score = node.priority
        while node != None:
            node.priority = max(score, node.priority)
            node = node.parent

    def add(self, word: str, score : int):
        currentNode = self.root
        for letter in word:
            currentNode = currentNode.get_or_create_child(letter, score)
        self.reprioritize(currentNode)

    @lru_cache(maxsize = 256) 
    def get(self, word: str):
        # either return true or false 
        currentNode = self.root
        createdString = ""
        for letter in word:
            if not currentNode: break
            createdString += letter
            currentNode = currentNode.get(letter)
        return currentNode

    @lru_cache(maxsize = 256) 
    def can_get(self, word: str):
        # either return true or false 
        currentNode = self.get(word)
        if currentNode == None: return False
        return currentNode.value == word
    
    @lru_cache(maxsize = 256) 
    def get_priority(self, word: str):
        # return the priority
        currentNode = self.get(word)
        if currentNode == None: return 0
        return currentNode.priority
    
    def is_leaf(self, word: str):
        # return the priority
        currentNode = self.get(word)
        if currentNode == None: return False
        return len(currentNode.pathing) == 0
    
    @lru_cache(maxsize = 256) 
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
        print(dot.source)

    def _visualize_helper(self, node, dot):
        for letter, child in node.pathing.items():
            dot.node(child.value, label=child.value)
            dot.edge(node.value, child.value, label=(f"{letter}, {child.priority}"))
            self._visualize_helper(child, dot)


class SpellCastChecker:
    def __init__(self):
        self.prefix_tree = PrefixTree()
        self.prefix_used_sub_tree = PrefixTree()
        self.prefix_sub_tree = PrefixTree()
        self.prefix_good_tree = PrefixTree()
        self.initializeRoots()

    def initializeRoots(self):
        for word in wordlist:
            score = get_raw_score(word)
            self.prefix_tree.add(word, score)
        for word in better_wordlist:
            score = get_raw_score(word)
            self.prefix_sub_tree.add(word,score)

    def create_good_tree(self, board : Counter, subs=0):
        self.prefix_good_tree = PrefixTree()
        new_wordlist = get_possible_wordlist(board=board, subs=subs)
        for word in new_wordlist:
            score = get_raw_score(word)
            self.prefix_good_tree.add(word, score)
        self.prefix_used_sub_tree = self.prefix_good_tree
    
    def stick_with_basic_tree(self):
        self.prefix_used_sub_tree = self.prefix_sub_tree
    
    @lru_cache(None) 
    def is_word(self, word):
        return word in wordlist
    
    @lru_cache(None)  
    def is_prefix(self, prefix):
        #see if string is a valid prefix of a word
        return self.prefix_used_sub_tree.can_get(prefix)
    
    def is_leaf_word(self, word):
        return self.prefix_used_sub_tree.is_leaf(word)
    
    @lru_cache(None)
    def get_possible_letter_subs(self, prefix):
        #get the possible letters that can sub in for a valid prefix given a prefix
        return self.prefix_used_sub_tree.get_next_letters(prefix)

    def visualize_sub_tree(self):
        self.prefix_used_sub_tree.visualize()
    
    @lru_cache(None)  
    def get_priority(self, word):
        return self.prefix_used_sub_tree.get_priority(word)
    
    @lru_cache(None)  
    def get(self, word):
      return self.prefix_used_sub_tree.get(word)
    
    def is_leaf_word(self, word):
        return self.prefix_used_sub_tree.is_leaf(word)