import pygame
import sys
import random

random.seed(42)

class Piece:
    """A class containing both data and a method."""
    def __init__(self, name, symbol, curr_col_idx, curr_row_idx):
        self.name = name      # Obj name
        self.symbol = symbol  # r n b q k p R N B Q K P
        self.curr_col_idx = curr_col_idx  # Init Col Index
        self.curr_row_idx = curr_row_idx  # Init Row Index
        self.delta_col_idx = 0
        self.delta_row_idx = 0
        self.next_col_idx = 0 # Final Col Index
        self.next_row_idx = 0 # Final Row Index
        self.active = True # In play

    def display_info(self):
        """Method that utilizes the object's data."""
        return f"Name: {self.name}"

    def gen_next_pos(self, board_array):
        print(f"Delta RC after {self.name} {self.delta_row_idx}  {self.delta_col_idx}")
        self.next_col_idx = self.curr_col_idx + self.delta_col_idx
        self.next_row_idx = self.curr_row_idx + self.delta_row_idx

    def set_active(self, active):
        self.active = active

    def is_active(self):
        return self.active

    # checks for smashing into own guy; updates current position
    def move_next_pos(self, board_array):
        while True:
            self.gen_next_pos(board_array)
            if self.name.islower(): #Black piece
                if board_array[self.next_row_idx][self.next_col_idx] not in ['r', 'n', 'b', 'q', 'k', 'p']:
                    board_array[self.next_row_idx][self.next_col_idx] = self.symbol
                    break
                else: #placeholder if smash into own guy
                    return
            else: #White piece
                if board_array[self.next_row_idx][self.next_col_idx] not in ['R', 'N', 'B', 'Q', 'K', 'P']:
                    board_array[self.next_row_idx][self.next_col_idx] = self.symbol
                    break
                else:
                    return
        board_array[self.curr_row_idx][self.curr_col_idx] = '.'
        self.curr_col_idx = self.next_col_idx
        self.curr_row_idx = self.next_row_idx

class Knight(Piece):
    def gen_next_pos(self, board_array):
        while True:
            self.delta_col_idx = random.choice([-2,-1,1,2])
            if self.delta_col_idx in [-2,2]:
                self.delta_row_idx = random.choice([-1,1])
            else: # self.delta_col_idx in [-1,1]
                self.delta_row_idx = random.choice([-2,2])
            # check for board boundary
            if 0 <= self.curr_col_idx + self.delta_col_idx <= 7 and 0 <= self.curr_row_idx + self.delta_row_idx <= 7:
                break
        super().gen_next_pos(board_array)

class Bishop(Piece):
    def gen_next_pos(self, board_array):
        while True:
            self.delta_col_idx = random.choice([-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7])
            self.delta_row_idx = random.choice([-1 * self.delta_col_idx, self.delta_col_idx])
            # check for board boundary
            if 0 <= self.curr_col_idx + self.delta_col_idx <= 7 and 0 <= self.curr_row_idx + self.delta_row_idx <= 7:
                break
        super().gen_next_pos(board_array)

class Rook(Piece):
    def gen_next_pos(self, board_array):
        move_across = random.choice([True, False])
        while True:
            if move_across:
                self.delta_col_idx = random.choice([-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7])
                self.delta_row_idx = 0
                print(f"Delta RC across random try {self.name} {self.delta_row_idx}  {self.delta_col_idx}")
                if 0 <= self.curr_col_idx + self.delta_col_idx <= 7: # in board boundary
                    # check for obstacle piece(s) in move path
                    if self.curr_col_idx < self.curr_col_idx + self.delta_col_idx: # move RIGHT
                        count = 0 # number of occupied spaces in vector
                        for x in range(self.curr_col_idx + 1, self.curr_col_idx + self.delta_col_idx): # do not check current and dest pos
                            if board_array[self.curr_row_idx][x] != ".": # if position is already taken
                                count += 1
                        if count == 0: # no positions taken (all empty)
                            break # no obstacles so go ahead and move to next_col_idx (end of while loop)
                    elif self.curr_col_idx > self.curr_col_idx + self.delta_col_idx: # move LEFT
                        count = 0 # number of occupied spaces in vector
                        for x in range(self.curr_col_idx + self.delta_col_idx + 1, self.curr_col_idx):
                            if board_array[self.curr_row_idx][x] != ".":
                                count += 1
                        if count == 0:
                            break
                else: # not in board boundary (regen while loop move)
                    continue
            else: # move up/dn
                self.delta_row_idx = random.choice([-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7])
                self.delta_col_idx = 0
                print(f"Delta RC up/dn random try {self.name} {self.delta_row_idx}  {self.delta_col_idx}")
                if 0 <= self.curr_row_idx + self.delta_row_idx <= 7:
                    # check for obstacle piece(s) in move path
                    if self.curr_row_idx < self.curr_row_idx + self.delta_row_idx: # move DOWN
                        count = 0 # number of occupied spaces in vector
                        for x in range(self.curr_row_idx + 1, self.curr_row_idx + self.delta_row_idx): # do not check current and dest pos
                            if board_array[x][self.curr_col_idx] != ".":
                                count += 1
                        if count == 0:
                            break # no obstacles so go ahead and move to next_row_idx
                    elif self.curr_row_idx > self.curr_row_idx + self.delta_row_idx: # move UP
                        count = 0 # number of occupied spaces in vector
                        for x in range(self.curr_row_idx + self.delta_row_idx + 1, self.curr_row_idx):
                            if board_array[x][self.curr_col_idx] != ".":
                                count += 1
                        if count == 0:
                            break
                else: # not in board boundary (regen move)
                    continue
        super().gen_next_pos(board_array)

class Pawn(Piece):
    def gen_next_pos(self, board_array):
        while True:
            self.delta_col_idx = 0
            if self.name.islower(): #Black piece
                self.delta_row_idx = 1
            else: #White piece
                self.delta_row_idx = -1
            if 0 <= self.curr_col_idx + self.delta_col_idx <= 7 and 0 <= self.curr_row_idx + self.delta_row_idx <= 7:
                break
        super().gen_next_pos(board_array)

# 1. Initialize Pygame
pygame.init()

# 2. Setup Board Dimensions
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Array to Chess Board")

# 3. Define Colors (RGB)
LIGHT_SQUARE = (240, 217, 181)  # Cream
DARK_SQUARE = (181, 136, 99)    # Brown
TEXT_COLOR = (0, 0, 0)          # Black for pieces

# 4. Map Characters/Pieces to Unicode Chess Symbols
PIECE_SYMBOLS = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟', # Black Pieces
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙', # White Pieces
    '.': ''                                                      # Empty Square
}

# 5. Your 2D Python Input Array (8x8)
# Lowercase = Black, Uppercase = White, '.' = Empty
### chess_array[row_idx][col_idx] ###
chess_array = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],  #row 0 black pieces
    #['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    #['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    #['.', '.', '.', '.', '.', '.', '.', '.']
    #['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']   #row 7 white pieces
]
   #col0                                col7

# 6. Initialize Font for Pieces (Make sure it supports Unicode)
# 'segoeuihistoric' or 'arial' usually contain chess symbols by default

try:
    font = pygame.font.SysFont("arialunicode", int(SQUARE_SIZE * 0.8))
except:
    print("arialunicode font needed to render chess images but not found!")

def draw_board(board_array):
    """Iterates through the 2D array and renders the GUI."""
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

clock = pygame.time.Clock()

# 7. Main Game Loop

piece_obj_list = [] #name, symbol, col, row
piece_obj_list += [Rook('rl', 'r', 0, 0)]
piece_obj_list += [Rook('rr', 'r', 7, 0)]
piece_obj_list += [Rook('RL', 'R', 0, 7)]
piece_obj_list += [Rook('RR', 'R', 7, 7)]
#piece_obj_list += [Pawn('PNR', 'P', 6, 6)]
#piece_obj_list += [Pawn('pnr', 'p', 6, 1)]
#piece_obj_list += [Pawn('PBR', 'P', 5, 6)]
#piece_obj_list += [Pawn('pbr', 'p', 5, 1)]
#piece_obj_list += [Pawn('PNL', 'P', 1, 6)]
#piece_obj_list += [Pawn('pnl', 'p', 1, 1)]
#piece_obj_list += [Pawn('PBL', 'P', 2, 6)]
#piece_obj_list += [Pawn('pbl', 'p', 2, 1)]
piece_obj_list += [Knight('nl', 'n', 1, 0)]
piece_obj_list += [Knight('nr', 'n', 6, 0)]
piece_obj_list += [Knight('NL', 'N', 1, 7)]
piece_obj_list += [Knight('NR', 'N', 6, 7)]
#piece_obj_list += [Bishop('bl', 'b', 2, 0)]
#piece_obj_list += [Bishop('br', 'b', 5, 0)]
#piece_obj_list += [Bishop('BL', 'B', 2, 7)]
#piece_obj_list += [Bishop('BR', 'B', 5, 7)]

for obj in piece_obj_list:
    chess_array[obj.curr_row_idx][obj.curr_col_idx] = obj.symbol

running = True
while running:
    for board_obj in piece_obj_list:

        clock.tick(0.5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
        # Redraw the UI
        for obj in piece_obj_list: # Update/remove taken pieces from board/play
            if chess_array[obj.curr_row_idx][obj.curr_col_idx] != obj.symbol: # I've been taken
                #obj.active = False
                obj.set_active(False)

        draw_board(chess_array)
        pygame.display.flip() #Board is (re)drawn here

        if board_obj.is_active():
            board_obj.move_next_pos(chess_array)

