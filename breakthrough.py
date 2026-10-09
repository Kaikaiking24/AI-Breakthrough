"""
File: breakthrough.py
Author: Stephanie Schwartz, adapted from konane.py (Lisa Meeden, Stephanie Schwartz, Chad Hogg)
Classes defined: BreakthroughError, Breakthrough, Player, Game, HumanPlayer,
RandomPlayer, SimplePlayer

Breakthrough holds the rules of the game for a given board size.  Game holds
one game in progress (the current board) and plays games between players.
A player is given the rules at the start of each game, and uses them to
generate moves and look ahead without changing the game in progress.
"""

import abc
import random
from collections.abc import Sequence
from typing import Literal, TypeAlias

# A player's symbol: 'B' for black or 'W' for white.
Side: TypeAlias = Literal['B', 'W']
# A board is a list of rows, each a list of 'B', 'W', or '.'.
Board: TypeAlias = list[list[str]]
# A move is (r1, c1, r2, c2), moving the piece at (r1, c1) to (r2, c2).
Move: TypeAlias = tuple[int, int, int, int]
# What a player may return from getMove: a move, or [] for no move (concede).
# Any sequence of four integers is accepted as a move, so a list also works.
PlayerMove: TypeAlias = Sequence[int]
# A location on the board, as (row, col).
Location: TypeAlias = tuple[int, int]


class BreakthroughError(ValueError):
    """
    This class is used to indicate a problem in the breakthrough game.
    """


class Breakthrough:
    """
    This class implements the rules of Breakthrough, a race game played
    with pawns, on an n by n board.  It does not hold a board itself;
    every method is given the board to work with.

    The board is represented as a two-dimensional list.  Each
    location on the board contains one of the following symbols:
       'B' for a black piece
       'W' for a white piece
       '.' for an empty location
    Black starts on the first two rows (rows 0 and 1) and moves down
    the board, toward row n-1.  White starts on the last two rows and
    moves up the board, toward row 0.  The black player always goes first.

    On each turn a player moves one of their pieces one square forward,
    either straight ahead or diagonally.  A straight move is only allowed
    into an empty location.  A diagonal move may go into an empty location
    or onto a location holding an opponent's piece, which captures (removes)
    that piece.  Pieces never move backward or sideways.

    A move is represented as a tuple (r1, c1, r2, c2), moving the piece at
    (r1, c1) to (r2, c2).

    The game ends when:
       - a player moves a piece onto the opponent's home row (the far side
         of the board), making that player the winner, or
       - a player has no pieces left or no legal moves, making the other
         player the winner.
    Because pieces only move forward, every game ends and there are no draws.
    The board may be any size from 5 by 5 to 8 by 8.
    """
    def __init__(self, n: int) -> None:
        if not 5 <= n <= 8:
            raise ValueError(f"the board size must be from 5 to 8, not {n}")
        self.size = n

    def startBoard(self) -> Board:
        """
        Returns a new board in the starting position.
        """
        board: Board = []
        for i in range(self.size):
            if i < 2:
                board.append(['B'] * self.size)
            elif i >= self.size - 2:
                board.append(['W'] * self.size)
            else:
                board.append(['.'] * self.size)
        return board

    def boardToStr(self, board: Board) -> str:
        """
        Returns a string representation of the breakthrough board.
        """
        header = "  " + "".join(f"{i} " for i in range(self.size)) + "\n"
        rows = "".join(f"{i} " + "".join(f"{cell} " for cell in board[i]) + "\n"
                       for i in range(self.size))
        return header + rows

    def valid(self, row: int, col: int) -> bool:
        """
        Returns true if the given row and col represent a valid location on
        the breakthrough board.
        """
        return 0 <= row < self.size and 0 <= col < self.size

    def contains(self, board: Board, row: int, col: int, symbol: str) -> bool:
        """
        Returns true if the given row and col represent a valid location on
        the breakthrough board and that location contains the given symbol.
        """
        return self.valid(row, col) and board[row][col] == symbol

    def countSymbol(self, board: Board, symbol: str) -> int:
        """
        Returns the number of instances of the symbol on the board.
        """
        return sum(row.count(symbol) for row in board)

    def opponent(self, player: Side) -> Side:
        """
        Given a player symbol, returns the opponent's symbol, 'B' for black,
        or 'W' for white.
        """
        return 'W' if player == 'B' else 'B'

    def direction(self, player: Side) -> int:
        """
        Returns the row delta for a forward move by the given player:
        1 for black (moving down the board), -1 for white (moving up).
        """
        return 1 if player == 'B' else -1

    def goalRow(self, player: Side) -> int:
        """
        Returns the row the given player is trying to reach.
        """
        return self.size - 1 if player == 'B' else 0

    def pieces(self, board: Board, player: Side) -> list[Location]:
        """
        Returns a list of the (row, col) locations of the given player's
        pieces on the board.
        """
        return [(r, c) for r in range(self.size) for c in range(self.size)
                if board[r][c] == player]

    def rowsToGoal(self, player: Side, row: int) -> int:
        """
        Returns how many rows a piece belonging to the given player, located
        in the given row, still has to move to reach its goal row.
        """
        return abs(self.goalRow(player) - row)

    def captureSquares(self, player: Side, row: int, col: int) -> list[Location]:
        """
        Returns a list of the (row, col) locations onto which a piece
        belonging to the given player, located at (row, col), could capture:
        the squares one row forward and one column to either side that are
        on the board.  This does not check what is on those squares.
        """
        r2 = row + self.direction(player)
        return [(r2, c2) for c2 in (col - 1, col + 1) if self.valid(r2, c2)]

    def winner(self, board: Board) -> Side | None:
        """
        Returns 'B' or 'W' if that player has won on the given board, by
        reaching the goal row or by capturing every opposing piece.
        Otherwise returns None.  (A player who has pieces but no legal
        moves also loses; generateMoves returns [] in that case.)
        """
        if 'B' in board[self.goalRow('B')]:
            return 'B'
        if 'W' in board[self.goalRow('W')]:
            return 'W'
        if not any('W' in row for row in board):
            return 'B'
        if not any('B' in row for row in board):
            return 'W'
        return None

    def nextBoard(self, board: Board, player: Side, move: PlayerMove) -> Board:
        """
        Given a move for a particular player from (r1,c1) to (r2,c2) this
        executes the move on a copy of the given board.  It will raise a
        BreakthroughError if the move is invalid.  It returns the copy of
        the board, and does not change the given board.
        """
        if (not isinstance(move, (list, tuple)) or len(move) != 4
                or not all(isinstance(x, int) for x in move)):
            raise BreakthroughError("a move must be four integers (r1, c1, r2, c2)")
        r1, c1, r2, c2 = move
        if not (self.valid(r1, c1) and self.valid(r2, c2)):
            raise BreakthroughError("move is off the board")
        if board[r1][c1] != player:
            raise BreakthroughError("no piece of yours at the starting location")
        if r2 - r1 != self.direction(player):
            raise BreakthroughError("pieces move exactly one row forward")
        if c2 == c1:
            if board[r2][c2] != '.':
                raise BreakthroughError("straight moves must be into an empty location")
        elif abs(c2 - c1) == 1:
            if board[r2][c2] == player:
                raise BreakthroughError("cannot move onto your own piece")
        else:
            raise BreakthroughError("pieces move straight or diagonally forward")
        newBoard = [row[:] for row in board]
        newBoard[r1][c1] = '.'
        newBoard[r2][c2] = player
        return newBoard

    def generateMoves(self, board: Board, player: Side) -> list[Move]:
        """
        Generates and returns all legal moves for the given player on the
        given board.  Returns [] if the game is already over.
        """
        if self.winner(board) is not None:
            return []
        moves: list[Move] = []
        dr = self.direction(player)
        for r in range(self.size):
            for c in range(self.size):
                if board[r][c] == player:
                    r2 = r + dr
                    for c2 in (c - 1, c, c + 1):
                        if not self.valid(r2, c2):
                            continue
                        target = board[r2][c2]
                        if c2 == c and target == '.':
                            moves.append((r, c, r2, c2))
                        elif c2 != c and target != player:
                            moves.append((r, c, r2, c2))
        return moves


class Player(abc.ABC):
    """
    A base class for Breakthrough players.  All players must implement
    the initialize and getMove methods.
    """
    name: str = "Player"
    side: Side
    rules: Breakthrough
    wins: int = 0
    losses: int = 0

    def results(self) -> str:
        return f"{self.name} Wins:{self.wins} Losses:{self.losses} Score: {self.score()}"

    def score(self) -> int:
        return self.wins - self.losses

    def lost(self) -> None:
        self.losses += 1

    def won(self) -> None:
        self.wins += 1

    def reset(self) -> None:
        self.wins = 0
        self.losses = 0

    @abc.abstractmethod
    def initialize(self, side: Side, rules: Breakthrough) -> None:
        """
        Called at the start of each game.  Records the player's side,
        either 'B' for black or 'W' for white, and the rules of the game
        being played (as self.side and self.rules).  Should also set the
        name of the player.
        """
        ...

    @abc.abstractmethod
    def getMove(self, board: Board) -> PlayerMove:
        """
        Given the current board, should return a valid move, such as one
        of the moves from generateMoves, or [] if there is no move to make.
        """
        ...


class Game:
    """
    One game of Breakthrough in progress on an n by n board, and methods
    for playing games between players.
    """
    def __init__(self, n: int) -> None:
        self.rules = Breakthrough(n)
        self.size = n
        self.reset()

    def reset(self) -> None:
        """
        Resets the board to the starting position.
        """
        self.board: Board = self.rules.startBoard()

    def __str__(self) -> str:
        return self.rules.boardToStr(self.board)

    def makeMove(self, player: Side, move: PlayerMove) -> None:
        """
        Updates the current board with the next board created by the given
        move.  Raises a BreakthroughError if the move is invalid.
        """
        self.board = self.rules.nextBoard(self.board, player, move)

    def playOneGame(self, p1: Player, p2: Player, show: bool) -> Side:
        """
        Given two instances of players, will play out a game
        between them.  Returns 'B' if black wins, or 'W' if
        white wins. When show is true, it will display each move
        in the game.
        """
        self.reset()
        p1.initialize('B', self.rules)
        p2.initialize('W', self.rules)
        print(f"{p1.name} vs {p2.name}")
        players: dict[Side, Player] = {'B': p1, 'W': p2}
        side: Side = 'B'
        while True:
            player = players[side]
            if show:
                print(self)
                print(f"player {side}'s turn")
            # Any error raised by a player's own code is deliberately caught,
            # so that a buggy player forfeits the game instead of stopping a
            # whole series of games or a tournament.
            try:
                move = player.getMove([row[:] for row in self.board])
            except Exception as e:
                print(f"player {side} is forfeiting because of error: {e}")
                move = []
            if move is None or move == [] or move == ():
                result = self.rules.opponent(side)
                break
            try:
                self.makeMove(side, move)
            except BreakthroughError as e:
                print(f"ERROR: invalid move {move} by {player.name}: {e}")
                result = self.rules.opponent(side)
                break
            if show:
                print(move)
                print()
            if self.rules.winner(self.board) == side:
                result = side
                break
            side = self.rules.opponent(side)
        if show:
            print(self)
            print("Game over")
        return result

    def playManyGames(self, n: int, p1: Player, p2: Player, show: bool) -> None:
        """
        Will play out n games between player p1 and player p2.
        The players alternate going first.  Prints the winner of
        each game.
        """
        first, second = p1, p2
        for i in range(n):
            print(f"Game {i}")
            winner = self.playOneGame(first, second, show)
            if winner == 'B':
                first.won()
                second.lost()
                print(f"{first.name} wins")
            else:
                first.lost()
                second.won()
                print(f"{second.name} wins")
            first, second = second, first


class HumanPlayer(Player):
    """
    Prompts a human player for a move.
    """
    def initialize(self, side: Side, rules: Breakthrough) -> None:
        self.side = side
        self.rules = rules
        self.name = "Human"

    def getMove(self, board: Board) -> PlayerMove:
        while True:
            text = input("Enter r1 c1 r2 c2 (or -1 to concede): ")
            try:
                values = [int(x) for x in text.replace(",", " ").split()]
            except ValueError:
                print("Please enter four integers.")
                continue
            if values and values[0] == -1:
                return []
            if len(values) == 4:
                return tuple(values)
            print("Please enter four integers.")


class RandomPlayer(Player):
    """
    Chooses a random move from the set of possible moves.
    """
    def initialize(self, side: Side, rules: Breakthrough) -> None:
        self.side = side
        self.rules = rules
        self.name = "RandomPlayer"

    def getMove(self, board: Board) -> PlayerMove:
        moves = self.rules.generateMoves(board, self.side)
        if not moves:
            return []
        return random.choice(moves)


class SimplePlayer(Player):
    """
    Always chooses the first move from the set of possible moves.
    """
    def initialize(self, side: Side, rules: Breakthrough) -> None:
        self.side = side
        self.rules = rules
        self.name = "SimplePlayer"

    def getMove(self, board: Board) -> PlayerMove:
        moves = self.rules.generateMoves(board, self.side)
        if not moves:
            return []
        return moves[0]


if __name__ == "__main__":
    game = Game(6)
    game.playManyGames(1, SimplePlayer(), RandomPlayer(), True)
