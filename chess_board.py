import pygame
import sys
import random

class Piece:
    """A class containing both data and a method."""
    def __init__(self, name, curr_col_idx, curr_row_idx):
        self.name = name      # Obj name
        self.curr_col_idx = curr_col_idx  # Init Col Index
        self.curr_row_idx = curr_row_idx  # Init Row Index
        self.delta_col_idx = 0
        self.delta_row_idx = 0
        self.next_col_idx = 0 # Final Col Index
        self.next_row_idx = 0 # Final Row Index

    def display_info(self):
        """Method that utilizes the object's data."""
        return f"Name: {self.name}"

    def gen_next_pos(self):
        print(f"Delta RC {self.name} {self.delta_row_idx}  {self.delta_col_idx}")
        self.next_col_idx = self.curr_col_idx + self.delta_col_idx
        self.next_row_idx = self.curr_row_idx + self.delta_row_idx

class Knight(Piece):
    def gen_next_pos(self):
        while True:
            self.delta_col_idx = random.choice([-2,-1,1,2])
            if self.delta_col_idx in [-2,2]:
                self.delta_row_idx = random.choice([-1,1])
            else: # self.delta_col_idx in [-1,1]
                self.delta_row_idx = random.choice([-2,2])
            if 0 <= self.curr_col_idx + self.delta_col_idx <= 7 and 0 <= self.curr_row_idx + self.delta_row_idx <= 7:
                break
        super().gen_next_pos()
'''
class Bishop(Piece):
    def gen_next_pos(self):
        while True:
            self.delta_col_idx = random.choice([-2,-1,1,2])
            if self.delta_col_idx in [-2,2]:
                self.delta_row_idx = random.choice([-1,1])
            else: # self.delta_col_idx in [-1,1]
                self.delta_row_idx = random.choice([-2,2])
            if 0 <= self.curr_col_idx + self.delta_col_idx <= 7 and 0 <= self.curr_row_idx + self.delta_row_idx <= 7:
                break
        super().gen_next_pos()
'''
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
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'P', '.', '.', '.'],  # E4 Pawn Open example
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', '.', 'P', 'P', 'P'],
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

blk_kn_obj = Knight('n', 1, 0)
chess_array[blk_kn_obj.curr_row_idx][blk_kn_obj.curr_col_idx] = blk_kn_obj.name
wht_kn_obj = Knight('N', 1, 7)
chess_array[wht_kn_obj.curr_row_idx][wht_kn_obj.curr_col_idx] = wht_kn_obj.name

blk_turn = True
running = True
while running:

    clock.tick(0.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
    # Redraw the UI
    draw_board(chess_array)
    pygame.display.flip() #Board is (re)drawn here

    if blk_turn:
        chess_array[blk_kn_obj.curr_row_idx][blk_kn_obj.curr_col_idx] = '.'
        while True:
            blk_kn_obj.gen_next_pos()
            if chess_array[blk_kn_obj.next_row_idx][blk_kn_obj.next_col_idx] != ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', 'p']:
                chess_array[blk_kn_obj.next_row_idx][blk_kn_obj.next_col_idx] = blk_kn_obj.name
                break
        blk_kn_obj.curr_col_idx = blk_kn_obj.next_col_idx
        blk_kn_obj.curr_row_idx = blk_kn_obj.next_row_idx
    else:
        chess_array[wht_kn_obj.curr_row_idx][wht_kn_obj.curr_col_idx] = '.'
        while True:
            wht_kn_obj.gen_next_pos()
            if chess_array[wht_kn_obj.next_row_idx][wht_kn_obj.next_col_idx] != ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r', 'p']:
                chess_array[wht_kn_obj.next_row_idx][wht_kn_obj.next_col_idx] = wht_kn_obj.name
                break
        wht_kn_obj.curr_col_idx = wht_kn_obj.next_col_idx
        wht_kn_obj.curr_row_idx = wht_kn_obj.next_row_idx

    blk_turn = not blk_turn
