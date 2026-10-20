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
        # get the list of possible moves for the current player
        moveList = self.rules.generateMoves(board, self.side)
    
        # if there are no possible moves, return nothing
        if not moveList:
            return []

        # set the best move from the list of possible moves
        bestMove = moveList[0]

        # initialize the best move and best value to negative infinity
        bestValue = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Apply the minimax algorithm to each move in the list of possible moves
        for move in moveList:
            # make a copy of the board and apply the move to it
            newBoard = self.rules.nextBoard(board, self.side, move)

            # get the value of the new board using the minimax algorithm
            value = self.minimax(newBoard, self.rules.opponent(self.side), self.limit - 1, alpha, beta)

            # if the value is greater than the best value, update the best value and best move
            if value > bestValue:
                bestValue = value
                bestMove = move

            # update alpha for alpha-beta pruning and cut beta
            alpha = max(alpha, bestValue)
            if alpha >= beta:
                break

        return bestMove

    def minimax(self, board, side, depth, alpha, beta):
        # Check wheather the game has a winner or if the depth limit is reached.
        winner = self.rules.winner(board)

        if winner == self.side:
            return float('inf')
        elif winner == self.rules.opponent(self.side):
            return float('-inf')
        elif depth == 0:
            return 0

        # get the list of possible moves for the current player
        moveList = self.rules.generateMoves(board, side)

        # if there are no possible moves, the player looses
        if not moveList:
            if side == self.side:
                return float('-inf')
            else:
                return float('inf')

        # if the current player is maximizing
        if side == self.side:
            bestValue = float('-inf')

            for move in moveList:
                newBoard = self.rules.nextBoard(board, side, move)

                value = self.minimax(newBoard, self.rules.opponent(side), depth - 1, alpha, beta)

                bestValue = max(bestValue, value)
                alpha = max(alpha, bestValue)

                # Prune if we cant improve.
                if alpha >= beta:
                    break

            return bestValue

        # if the current player is minimizing
        else:
            bestValue = float('inf')

            for move in moveList:
                newBoard = self.rules.nextBoard(board, side, move)

                value = self.minimax(newBoard, self.rules.opponent(side), depth - 1, alpha, beta)

                bestValue = min(bestValue, value)
                beta = min(beta, bestValue)

                # Prune if we can not improve.
                if alpha >= beta:
                    break

            return bestValue

    # method to evaluate the board for the MinimaxPlayer class that takes in a board as an argument
    def eval(self, board):
        return 0

if __name__ == "__main__":
    game = Game(7)
    game.playManyGames(2, MinimaxPlayer(4), RandomPlayer(), False)