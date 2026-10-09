# File : MyBreak.py
# Authors : King Igwe, Nicholas Osborne
# Date : 2024-06-10
# Class : CMSC 450
# Description : 

from breakthrough import *


class MinimaxPlayer(Player):

    def __init__(self, depthLimit):
        self.limit = depthLimit

    def initialize(self, side, rules):
        self.side = side
        self.rules = rules
        #complete this

    def getMove(self, board):
        #complete this

    def eval(self, board):
        #complete this – this will be your evaluation function.
        #High values should be good for max.