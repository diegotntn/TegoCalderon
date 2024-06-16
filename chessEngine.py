import chess
import sys
import random

class GameState():
    def __init__ (self):
        self.board = chess.Board()
        self.whiteToMove = True
        self.moveLog = []

    def make_move(self, move):
        if self.board.is_legal(move):
            self.board.push(move)
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove
        else:
            print("Move is not legal")

class Move():
    def __init__(self, startSq, endSq, board):
        self.startSq = startSq
        self.endSq = endSq
        self.pieceMoved = board.piece_at(startSq)
        self.pieceCaptured = board.piece_at(endSq)
    
    def get_chess_notation(self):
        return chess.Board().san(chess.Move(self.startSq, self.endSq))