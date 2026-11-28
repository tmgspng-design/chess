import pygame
import sys
import random
import chess_lib

# 2D Python Input Array (8x8)
# Lowercase = Black, Uppercase = White, '.' = Empty
# chess_array[row_idx][col_idx] = symbol
chess_array = [
#     qr   qn   qb   q    k   kb   kn   kr
    ['.', '.', '.', '.', '.', '.', '.', '.'],  #row 0 black pieces
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']   #row 7 white pieces
#     QR   QN   QB   Q    K   KB   KN   KR
] # col 0                              col 7

# Initialize Pygame
pygame.init()

piece_obj_list = [] #name, symbol, col, row, chess_array

piece_obj_list += [chess_lib.Bishop('qb', 'b', 3, 4, chess_array)] # black bishop
#piece_obj_list += [chess_lib.Bishop('QB', 'B', 2, 7, chess_array)]
piece_obj_list += [chess_lib.Rook('KR', 'R', 7, 7, chess_array)] # white knight

rook_obj = next((p for p in piece_obj_list if p.name == 'KR'), None) # name rook ptr
bishop_obj = next((p for p in piece_obj_list if p.name == 'qb'), None) # name bishop ptr

for obj in piece_obj_list:
    chess_array[obj.prev_row_idx][obj.prev_col_idx] = obj.symbol # place pieces onto chess board

clock = pygame.time.Clock()

running = True
while running:

    clock.tick(0.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
    chess_lib.draw_board(chess_array)
    pygame.display.flip() #Board is (re)drawn here

    rook_obj.gen_move_attack_list() # create availabe move pos for each piece wrt current pos

    chess_array[rook_obj.prev_row_idx][rook_obj.prev_col_idx] = '.' # move pieces on chess board

    target_move_list = []
    for coor, space in rook_obj.move_attack_list:
        for pos in space:
            if bishop_obj.prev_col_idx == pos[0] and bishop_obj.prev_row_idx == pos[1]:
                target_move_list.append(coor)
    rook_obj.prev_col_idx, rook_obj.prev_row_idx = random.choice(target_move_list)

    chess_array[rook_obj.prev_row_idx][rook_obj.prev_col_idx] = rook_obj.symbol # move pieces on chess board
            
    chess_lib.draw_board(chess_array)
    pygame.display.flip() #Board is (re)drawn here

    bishop_obj.gen_move_attack_list() # create availabe move pos for each piece wrt current pos

    chess_array[bishop_obj.prev_row_idx][bishop_obj.prev_col_idx] = '.' # move pieces on chess board

    bishop_obj.prev_col_idx, bishop_obj.prev_row_idx = random.choice(bishop_obj.move_list)

    chess_array[bishop_obj.prev_row_idx][bishop_obj.prev_col_idx] = bishop_obj.symbol # move pieces on chess board
            
        # Redraw the UI
        #for obj in piece_obj_list: # Update/remove taken pieces from board/play
            #if chess_array[obj.prev_row_idx][obj.prev_col_idx] != obj.symbol: # I've been taken
                ##obj.active = False
                #obj.set_active(False)

        #if board_obj.is_active():
            #board_obj.move_next_pos(chess_array)



for obj in piece_obj_list:
    obj.gen_move_attack_list() # create availabe move pos for each piece wrt current pos

for coor, space in rook_obj.move_attack_list:
    for pos in space:
        if bishop_obj.prev_col_idx == pos[0] and bishop_obj.prev_row_idx == pos[1]:
            print (f"move to col={coor[0]} row = {coor[1]}")
    pass

