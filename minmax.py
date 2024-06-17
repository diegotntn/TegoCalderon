import chess
from posiciones import positionEval

def EvaluateBoard(board):
    if board.is_checkmate():
        if board.turn:
            return -9999  # Blancas pierden
        else:
            return 9999  # Negras pierden
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0  # Tablas
    
    evaluation = 0
    materialValues = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 10,
        chess.KING: 100000
    }

    for piece_type in materialValues:
        evaluation += len(board.pieces(piece_type, chess.WHITE)) * materialValues[piece_type]
        evaluation -= len(board.pieces(piece_type, chess.BLACK)) * materialValues[piece_type]

        for square in board.pieces(piece_type, chess.WHITE):
            evaluation += positionEval[piece_type][0][7 - chess.square_rank(square)][chess.square_file(square)]
        for square in board.pieces(piece_type, chess.BLACK):
            evaluation -= positionEval[piece_type][1][chess.square_rank(square)][chess.square_file(square)]

    return evaluation

def order_moves(board, moves):
    def move_order(move):
        if board.is_capture(move):
            return 10  # Mayor prioridad para capturas
        if board.piece_type_at(move.from_square) == chess.PAWN and (chess.square_rank(move.to_square) == 0 or chess.square_rank(move.to_square) == 7):
            return 8  # Alta prioridad para promociones
        return 1  # Menor prioridad para movimientos normales

    return sorted(moves, key=move_order, reverse=True)

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return EvaluateBoard(board)
    
    legal_moves = list(board.legal_moves)
    ordered_moves = order_moves(board, legal_moves)  # Ordenar movimientos

    if maximizing_player:
        max_eval = -float('inf')
        for move in ordered_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in ordered_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def getBestMove(board, depth):
    bestMove = None
    maxEval = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    legal_moves = list(board.legal_moves)
    ordered_moves = order_moves(board, legal_moves)  # Ordenar movimientos

    for move in ordered_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if eval > maxEval:
            maxEval = eval
            bestMove = move

    return bestMove