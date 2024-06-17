import pygame
import chess
import os
import math

WIDTH = HEIGHT = 600  # Tamaño del tablero
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
PADDING = 20
COLORS = {
    'Rojo': pygame.Color('red'),
    'Verde': pygame.Color('green'),
    'Azul': pygame.Color('blue'),
    'Amarillo': pygame.Color('yellow')
}
selected_color = pygame.Color('red')  # Color seleccionado por defecto

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

def drawGameState(screen, board, sqSelected, best_move=None):
    drawBoard(screen)
    highlightSquare(screen, sqSelected)
    drawPieces(screen, board)
    draw_buttons(screen)
    if best_move:
        draw_arrow(screen, best_move)

def draw_buttons(screen):
    # Posiciones de los botones
    reset_button = pygame.Rect(WIDTH + PADDING, PADDING, BUTTON_WIDTH, BUTTON_HEIGHT)
    help_button = pygame.Rect(WIDTH + PADDING, 2 * PADDING + BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
    undo_button = pygame.Rect(WIDTH + PADDING, 3 * PADDING + 2 * BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    pygame.draw.rect(screen, pygame.Color('lightgray'), reset_button)
    pygame.draw.rect(screen, pygame.Color('lightgray'), help_button)
    pygame.draw.rect(screen, pygame.Color('lightgray'), undo_button)

    font = pygame.font.SysFont(None, 24)
    reset_text = font.render('Reiniciar Juego', True, pygame.Color('black'))
    help_text = font.render('Ayuda', True, pygame.Color('black'))
    undo_text = font.render('Regresar una jugada', True, pygame.Color('black'))

    screen.blit(reset_text, (WIDTH + PADDING + (BUTTON_WIDTH - reset_text.get_width()) // 2, PADDING + (BUTTON_HEIGHT - reset_text.get_height()) // 2))
    screen.blit(help_text, (WIDTH + PADDING + (BUTTON_WIDTH - help_text.get_width()) // 2, 2 * PADDING + BUTTON_HEIGHT + (BUTTON_HEIGHT - help_text.get_height()) // 2))
    screen.blit(undo_text, (WIDTH + PADDING + (BUTTON_WIDTH - undo_text.get_width()) // 2, 3 * PADDING + 2 * BUTTON_HEIGHT + (BUTTON_HEIGHT - undo_text.get_height()) // 2))

def handle_button_click(location, board):
    if WIDTH + PADDING <= location[0] <= WIDTH + PADDING + BUTTON_WIDTH:
        if PADDING <= location[1] <= PADDING + BUTTON_HEIGHT:
            return 'reset'
        elif 2 * PADDING + BUTTON_HEIGHT <= location[1] <= 2 * PADDING + 2 * BUTTON_HEIGHT:
            return 'help'
        elif 3 * PADDING + 2 * BUTTON_HEIGHT <= location[1] <= 3 * PADDING + 3 * BUTTON_HEIGHT:
            return 'undo'
    return None

def draw_arrow(screen, move):
    start_pos = (chess.square_file(move.from_square) * SQ_SIZE + SQ_SIZE // 2, (7 - chess.square_rank(move.from_square)) * SQ_SIZE + SQ_SIZE // 2)
    end_pos = (chess.square_file(move.to_square) * SQ_SIZE + SQ_SIZE // 2, (7 - chess.square_rank(move.to_square)) * SQ_SIZE + SQ_SIZE // 2)
    pygame.draw.line(screen, selected_color, start_pos, end_pos, 5)
    draw_arrowhead(screen, start_pos, end_pos)

def draw_arrowhead(screen, start, end):
    rotation = (math.atan2(start[1] - end[1], start[0] - end[0]) + math.pi) % (2 * math.pi)
    pygame.draw.polygon(screen, selected_color, ((end[0] + 15 * math.sin(rotation - math.pi / 6), end[1] + 15 * math.cos(rotation - math.pi / 6)),
                                                (end[0] + 15 * math.sin(rotation + math.pi / 6), end[1] + 15 * math.cos(rotation + math.pi / 6)),
                                                end))

def draw_color_selection(screen):
    screen.fill(pygame.Color("White"))
    font = pygame.font.SysFont(None, 48)
    title_font = pygame.font.SysFont(None, 72, bold=True)
    button_font = pygame.font.SysFont(None, 36)

    title_text = title_font.render('Ajedrez', True, pygame.Color('black'))
    select_text = font.render('Seleccione su color:', True, pygame.Color('black'))
    
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, screen.get_height() // 2 - 200))
    screen.blit(select_text, (screen.get_width() // 2 - select_text.get_width() // 2, screen.get_height() // 2 - 100))
    
    white_button = pygame.Rect(screen.get_width() // 2 - BUTTON_WIDTH // 2, screen.get_height() // 2 - 25, BUTTON_WIDTH, BUTTON_HEIGHT)
    black_button = pygame.Rect(screen.get_width() // 2 - BUTTON_WIDTH // 2, screen.get_height() // 2 + PADDING + 25, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    pygame.draw.rect(screen, pygame.Color('white'), white_button)
    pygame.draw.rect(screen, pygame.Color('black'), black_button)
    pygame.draw.rect(screen, pygame.Color('black'), white_button, 3)  # Bordes
    pygame.draw.rect(screen, pygame.Color('white'), black_button, 3)  # Bordes
    
    white_text = button_font.render('Blancas', True, pygame.Color('black'))
    black_text = button_font.render('Negras', True, pygame.Color('white'))
    
    screen.blit(white_text, (screen.get_width() // 2 - white_text.get_width() // 2, screen.get_height() // 2 - 25 + (BUTTON_HEIGHT - white_text.get_height()) // 2))
    screen.blit(black_text, (screen.get_width() // 2 - black_text.get_width() // 2, screen.get_height() // 2 + PADDING + 25 + (BUTTON_HEIGHT - black_text.get_height()) // 2))

def is_button_clicked(location, color):
    screen_center_x = pygame.display.get_surface().get_width() // 2
    screen_center_y = pygame.display.get_surface().get_height() // 2
    if color == 'white':
        return screen_center_x - BUTTON_WIDTH // 2 <= location[0] <= screen_center_x + BUTTON_WIDTH // 2 and screen_center_y - 25 <= location[1] <= screen_center_y + 25
    elif color == 'black':
        return screen_center_x - BUTTON_WIDTH // 2 <= location[0] <= screen_center_x + BUTTON_WIDTH // 2 and screen_center_y + PADDING + 25 <= location[1] <= screen_center_y + PADDING + 25 + BUTTON_HEIGHT
    return False

def draw_end_screen(screen, message):
    screen.fill(pygame.Color("White"))
    font = pygame.font.SysFont(None, 72, bold=True)
    button_font = pygame.font.SysFont(None, 36)

    message_text = font.render(message, True, pygame.Color('black'))
    screen.blit(message_text, (screen.get_width() // 2 - message_text.get_width() // 2, screen.get_height() // 2 - 100))

    reset_button = pygame.Rect(screen.get_width() // 2 - BUTTON_WIDTH // 2, screen.get_height() // 2 + 25, BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, pygame.Color('lightgray'), reset_button)
    pygame.draw.rect(screen, pygame.Color('black'), reset_button, 3)  # Bordes

    reset_text = button_font.render('Reiniciar Juego', True, pygame.Color('black'))
    screen.blit(reset_text, (screen.get_width() // 2 - reset_text.get_width() // 2, screen.get_height() // 2 + 25 + (BUTTON_HEIGHT - reset_text.get_height()) // 2))

def is_reset_button_clicked(location):
    screen_center_x = pygame.display.get_surface().get_width() // 2
    screen_center_y = pygame.display.get_surface().get_height() // 2
    return screen_center_x - BUTTON_WIDTH // 2 <= location[0] <= screen_center_x + BUTTON_WIDTH // 2 and screen_center_y + 25 <= location[1] <= screen_center_y + 25 + BUTTON_HEIGHT

def draw_promotion_options(screen, promotion_square):
    screen_center_x = pygame.display.get_surface().get_width() // 2
    screen_center_y = pygame.display.get_surface().get_height() // 2
    options = ['q', 'r', 'b', 'n']
    labels = ['Reina', 'Torre', 'Alfil', 'Caballo']
    font = pygame.font.SysFont(None, 36)
    
    for i, option in enumerate(options):
        button = pygame.Rect(screen_center_x - BUTTON_WIDTH // 2, screen_center_y - 75 + i * (BUTTON_HEIGHT + PADDING), BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, pygame.Color('lightgray'), button)
        pygame.draw.rect(screen, pygame.Color('black'), button, 3)  # Bordes
        
        label = font.render(labels[i], True, pygame.Color('black'))
        screen.blit(label, (screen_center_x - label.get_width() // 2, screen_center_y - 75 + i * (BUTTON_HEIGHT + PADDING) + (BUTTON_HEIGHT - label.get_height()) // 2))

def handle_promotion_click(location, promotion_square):
    screen_center_x = pygame.display.get_surface().get_width() // 2
    screen_center_y = pygame.display.get_surface().get_height() // 2
    options = ['q', 'r', 'b', 'n']
    
    for i, option in enumerate(options):
        if screen_center_x - BUTTON_WIDTH // 2 <= location[0] <= screen_center_x + BUTTON_WIDTH // 2 and screen_center_y - 75 + i * (BUTTON_HEIGHT + PADDING) <= location[1] <= screen_center_y - 75 + (i + 1) * (BUTTON_HEIGHT + PADDING):
            return option
    return None
