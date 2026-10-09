## File : MyBreak.py
## Authors : King Igwe, Nicholas Osborne
## Date : 10/09/2026
## Class : CMSC 450
## Description : Applying minimax with alpha-beta pruning to the game of Breakthrough.

# import Breakthrough
from breakthrough import *

# 
class MinimaxPlayer(Player):

    def __init__(self, depthLimit):
        self.limit = depthLimit

    def initialize(self, side, rules):
        self.side = side
        self.rules = rules
        self.name = "MinimaxPlayer"

    def getMove(self, board):
        pass

    def eval(self, board):
        pass