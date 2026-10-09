# File : MyBreak.py
# Authors : King Igwe, Nicholas Osborne
# Date : 2024-06-10
# Class : CMSC 450
# Description : Applying minimax with alpha-beta pruning to the game of Breakthrough.

from breakthrough import *


class MinimaxPlayer(Player):

    def __init__(self, depthLimit):
        self.limit = depthLimit

    def initialize(self, side, rules):
        self.side = side
        self.rules = rules
        #complete this

    def getMove(self, board):
        pass

    def eval(self, board):
        pass