import pygame

class Piece: # base class for all chess pieces
    def __init__(self, name, symbol, prev_col_idx, prev_row_idx, chess_array):
        self.name = name      # qr qn qb q k kb kn kr - Black ; QR QN QB Q K KB KN KR - White
        self.symbol = symbol  # r n b q k p - Black ; R N B Q K P - White
        self.prev_col_idx = prev_col_idx  # Previous COL position - 0 to 7 from left to right
        self.prev_row_idx = prev_row_idx  # Previous ROW position - 0 to 7 from top to bottom
        self.active = True # TRUE if piece in play ; FALSE if piece is taken
        self.chess_array = chess_array # pointer to chess board
        self.move_list = [] # save initial attack_pos_list which is actually avail move list wrt curr pos
        self.move_attack_list = [] # the attack spaces for each avail pos the piece can move to

    def set_active(self, active): # True if piece has not been taken; False if piece has been taken
        self.active = active

    def is_active(self): # True if piece has not been taken; False if piece has been taken
        return self.active

    def gen_attack_space(self, attack_pos_list_all, curr_col_idx, curr_row_idx): # base method to create available move/attack positions list
        attack_pos_list_bound = []
        attack_pos_list = [] # all available move positions wrt current position and obstacles
        for col, row in attack_pos_list_all:
            if 0 <= col <= 7 and 0 <= row <= 7:
                attack_pos_list_bound.append([col, row])
                attack_pos_list.append([col, row])
        for col, row in attack_pos_list_bound: # go thru & remove pos from list if obstacles along its path
            #print (f"col={col} row={row}")
            if curr_col_idx < col:
                sgnc = 1 # move RIGHT
            elif curr_col_idx > col:
                sgnc = -1 # move LEFT
            else:
                sgnc = 0 # no R/L motion
            if curr_row_idx < row:
                sgnr = 1 # move DOWN
            elif curr_row_idx > row:
                sgnr = -1 # move UP
            else:
                sgnr = 0 # no D/U motion
            #print (f"col={col} row={row} sgnc={sgnc} sgnr={sgnr}")
            if sgnc == 0: # only D/U motion
                for x in range(curr_row_idx, row + sgnr, sgnr): # check along vertical path
                    if x == curr_row_idx:
                        continue
                    elif self.chess_array[x][curr_col_idx] in ['R', 'N', 'B', 'Q', 'K', 'P']:
                        attack_pos_list.remove([col, row])
                        break
            elif sgnr == 0: # only R/L motion
                for x in range(curr_col_idx, col + sgnc, sgnc): # check along horizontal path
                    if x == curr_col_idx:
                        continue
                    elif self.chess_array[curr_row_idx][x] in ['R', 'N', 'B', 'Q', 'K', 'P']:
                        attack_pos_list.remove([col, row])
                        break
            else: # both R/L and D/U motion
                for x, y in zip(range(curr_col_idx, col + sgnc, sgnc), range(curr_row_idx, row + sgnr, sgnr)): # check along diag path
                    #print (f"x={x} y={y}")
                    if (x, y) == (curr_col_idx , curr_row_idx ):
                        continue
                    elif self.chess_array[y][x] in ['R', 'N', 'B', 'Q', 'K', 'P']:
                        attack_pos_list.remove([col, row])
                        break
        return attack_pos_list

    def gen_move_attack_list(self): # base method to create the attack spaces for each avail pos the piece can move to 
        self.move_list = self.gen_attack_space(self.prev_col_idx, self.prev_row_idx) # save initial attack_pos_list which is actually avail move list wrt curr pos
        for colrow in self.move_list: # check attack space for each move pos
            self.move_attack_list.append([colrow, self.gen_attack_space(colrow[0], colrow[1])])

# override base method with piece specific move details in extended classes
class Bishop(Piece):
    def gen_attack_space(self, curr_col_idx, curr_row_idx):
        attack_pos_list_all = []
        for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            for delta_row_idx in [-1 * delta_col_idx, delta_col_idx]:
                attack_pos_list_all.append([curr_col_idx + delta_col_idx, curr_row_idx + delta_row_idx])
        return super().gen_attack_space(attack_pos_list_all, curr_col_idx, curr_row_idx)

class Rook(Piece):
    def gen_attack_space(self, curr_col_idx, curr_row_idx):
        attack_pos_list_all = []
        for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            attack_pos_list_all.append([curr_col_idx + delta_col_idx, curr_row_idx])
        for delta_row_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            attack_pos_list_all.append([curr_col_idx, curr_row_idx + delta_row_idx])
        return super().gen_attack_space(attack_pos_list_all, curr_col_idx, curr_row_idx)

# function to translate python array to graphical chess board
def draw_board(board_array):
    # Setup Board Dimensions
    WIDTH, HEIGHT = 600, 600
    SQUARE_SIZE = WIDTH // 8
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Python Array to Chess Board")

    # Define Colors (RGB)
    LIGHT_SQUARE = (240, 217, 181)  # Cream
    DARK_SQUARE = (181, 136, 99)    # Brown
    TEXT_COLOR = (0, 0, 0)          # Black for pieces

    # Map Characters/Pieces to Unicode Chess Symbols
    PIECE_SYMBOLS = {
        'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟', # Black Pieces
        'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙', # White Pieces
        '.': ''                                                      # Empty Square
    }

    # Initialize Font for Pieces (Make sure it supports Unicode)
    font = pygame.font.SysFont("arialunicode", int(SQUARE_SIZE * 0.8))

    # Iterates through the 2D array and renders the GUI
    for row in range(8):
        for col in range(8):
            # Determine background tile color (alternating checkerboard pattern)
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            
            # Draw the background square
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            
            # Get piece code from array and convert to Unicode
            piece = board_array[row][col]
            symbol = PIECE_SYMBOLS.get(piece, '')
            
            if symbol:
                # Render text and center it inside the square
                text_surface = font.render(symbol, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

