import pygame
import sys
import chess
import chessGui as gui
import minmax

def main():
    pygame.init()
    screen = pygame.display.set_mode((gui.WIDTH + gui.BUTTON_WIDTH + 2 * gui.PADDING, gui.HEIGHT))
    pygame.display.set_caption('Ajedrez')
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("White"))

    gui.load_images()  
    running = True
    sq_selected = ()
    clicks_user = []
    best_move = None  # Variable para almacenar el mejor movimiento

    board = chess.Board()
    move_log = []  # Lista para guardar los movimientos
    player_color = None  # Variable para guardar el color del jugador
    game_over = False  # Variable para indicar si el juego ha terminado

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                if game_over:
                    if gui.is_reset_button_clicked(location):
                        board = chess.Board()
                        move_log = []
                        game_over = False
                        if player_color == chess.BLACK:
                            ai_move = minmax.getBestMove(board, 3)  # El AI hace el primer movimiento si el jugador es negro
                            if ai_move:
                                board.push(ai_move)
                                move_log.append(ai_move)
                elif player_color is None:
                    # Elegir color del jugador
                    if gui.is_button_clicked(location, 'white'):
                        player_color = chess.WHITE
                    elif gui.is_button_clicked(location, 'black'):
                        player_color = chess.BLACK
                    if player_color is not None:
                        board = chess.Board()
                        move_log = []  # Reiniciar el registro de movimientos
                        best_move = None  # Limpiar el mejor movimiento al reiniciar
                        if player_color == chess.BLACK:
                            ai_move = minmax.getBestMove(board, 3)  # El AI hace el primer movimiento si el jugador es negro
                            if ai_move:
                                board.push(ai_move)
                                move_log.append(ai_move)
                else:
                    if location[0] < gui.WIDTH:
                        col = location[0] // gui.SQ_SIZE
                        fila = location[1] // gui.SQ_SIZE
                        if sq_selected == (col, fila):
                            sq_selected = ()
                            clicks_user = []
                        else:
                            sq_selected = (col, fila)
                            clicks_user.append(sq_selected)

                        if len(clicks_user) == 2:
                            start_sq = chess.square(clicks_user[0][0], gui.DIMENSION - clicks_user[0][1] - 1)
                            end_sq = chess.square(clicks_user[1][0], gui.DIMENSION - clicks_user[1][1] - 1)
                            move = chess.Move(start_sq, end_sq)
                            if move in board.legal_moves:
                                board.push(move)
                                move_log.append(move)  # Guardar el movimiento
                                if board.is_checkmate():
                                    game_over = True
                                else:
                                    ai_move = minmax.getBestMove(board, 3)  # Profundidad máxima de 4
                                    if ai_move:
                                        board.push(ai_move)
                                        move_log.append(ai_move)  # Guardar el movimiento del AI
                                        if board.is_checkmate():
                                            game_over = True
                            sq_selected = ()
                            clicks_user = []
                            best_move = None  # Limpiar el mejor movimiento al realizar un movimiento
                    else:
                        button_action = gui.handle_button_click(location, board)
                        if button_action == 'reset':
                            board = chess.Board()
                            move_log = []  # Reiniciar el registro de movimientos
                            best_move = None  # Limpiar el mejor movimiento al reiniciar
                            if player_color == chess.BLACK:
                                ai_move = minmax.getBestMove(board, 3)  # El AI hace el primer movimiento si el jugador es negro
                                if ai_move:
                                    board.push(ai_move)
                                    move_log.append(ai_move)
                        elif button_action == 'help':
                            best_move = minmax.getBestMove(board, 3)  # Obtener el mejor movimiento
                        elif button_action == 'undo':
                            if len(move_log) > 0:
                                board.pop()  # Deshacer el último movimiento
                                move_log.pop()  # Eliminar el último movimiento del registro
                                if len(move_log) > 0:
                                    board.pop()  # Deshacer el movimiento del AI
                                    move_log.pop()  # Eliminar el movimiento del AI del registro
                            best_move = None  # Limpiar el mejor movimiento al deshacer

        if game_over:
            if board.turn == player_color:
                gui.draw_end_screen(screen, "Perdiste lol")
            else:
                gui.draw_end_screen(screen, "Ganaste lol")
        elif player_color is None:
            gui.draw_color_selection(screen)
        else:
            gui.drawGameState(screen, board, sq_selected, best_move)
        
        pygame.display.flip()
        clock.tick(gui.MAX_FPS)

if __name__ == "__main__":
    main()
