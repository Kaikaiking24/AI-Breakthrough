## File : MyBreak.py
## Authors : King Igwe, Nicholas Osborne
## Date : 10/09/2026
## Class : CMSC 450
## Description : Applying minimax with alpha-beta pruning to the game of Breakthrough.

# import Breakthrough
from breakthrough import *

# create a class for the MinimaxPlayer that inherits from the Player class
class MinimaxPlayer(Player):

    # constructor for the MinimaxPlayer class that takes in a depth limit as an argument
    def __init__(self, depthLimit):
        self.limit = depthLimit

    # initialize method for the MinimaxPlayer class that takes in a side and rules as arguments
    def initialize(self, side, rules):
        self.side = side
        self.rules = rules
        self.name = "MinimaxPlayer"

    # method to get the move for the MinimaxPlayer class that takes in a board as an argument
    def getMove(self, board):
        pass


    # method to evaluate the board for the MinimaxPlayer class that takes in a board as an argument
    def eval(self, board):
        pass

if __name__ == "__main__":
    game = Game(6)
    game.playManyGames(1, SimplePlayer(), RandomPlayer(), True)