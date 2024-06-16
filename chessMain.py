import pygame
import os
import sys
import chess

# Añadir el directorio que contiene chessEngine y otros módulos a la ruta del sistema
sys.path.append(r'C:/Users/DELL/OneDrive/Documentos/Diego/Fundamentos de IA/proyecto final/TegoCalderon/Ajedrez')

import chessEngine
import minmax

WIDTH = HEIGHT = 600  # Aumentar el tamaño para mejor visualización
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}

# Cargar imágenes de las piezas
def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load(os.path.join("images", piece + ".png")).convert_alpha()
        IMAGES[piece] = pygame.transform.scale(IMAGES[piece], (SQ_SIZE, SQ_SIZE))

def drawBoard(screen):
    colors = [pygame.Color('#EEEED2'), pygame.Color('#769656')]  # Colores más atractivos
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[(i + j) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquare(screen, sqSelected):
    if sqSelected:
        col, fila = sqSelected
        pygame.draw.rect(screen, pygame.Color('blue'), pygame.Rect(col * SQ_SIZE, fila * SQ_SIZE, SQ_SIZE, SQ_SIZE), 4)

def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board.piece_at(chess.square(j, DIMENSION - i - 1))
            if piece:
                piece_str = piece.symbol()
                if piece_str.islower():
                    piece_str = 'b' + piece_str.upper()
                else:
                    piece_str = 'w' + piece_str
                screen.blit(IMAGES[piece_str], pygame.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(screen, ej, sqSelected):
    drawBoard(screen)
    highlightSquare(screen, sqSelected)
    drawPieces(screen, ej.board)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Ajedrez')
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("White"))
    ej = chessEngine.GameState()

    load_images()  
    running = True
    sqSelected = ()
    clicksUser = []
    player_turn = True  # True para las blancas, False para las negras

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_SIZE
                fila = location[1] // SQ_SIZE
                if sqSelected == (col, fila):
                    sqSelected = ()
                    clicksUser = []
                else:
                    sqSelected = (col, fila)
                    clicksUser.append(sqSelected)

                if len(clicksUser) == 2:
                    start_sq = chess.square(clicksUser[0][0], DIMENSION - clicksUser[0][1] - 1)
                    end_sq = chess.square(clicksUser[1][0], DIMENSION - clicksUser[1][1] - 1)
                    move = chess.Move(start_sq, end_sq)
                    if move in ej.board.legal_moves:
                        ej.make_move(move)
                        player_turn = False
                    sqSelected = ()
                    clicksUser = []

        # Turno de las negras (AI)
        if not player_turn:
            ai_move = minmax.getBestMove(ej.board, 4)  
            if ai_move:
                ej.make_move(ai_move)
            player_turn = True

        drawGameState(screen, ej, sqSelected)
        pygame.display.flip()
        clock.tick(MAX_FPS)

if __name__ == "__main__":
    main()
