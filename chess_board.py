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

class Bishop(Piece):
    def gen_next_pos(self):
        while True:
            self.delta_col_idx = random.randint(-7, 7)
            self.delta_row_idx = random.choice([-1 * self.delta_col_idx, self.delta_col_idx])
            if 0 <= self.curr_col_idx + self.delta_col_idx <= 7 and 0 <= self.curr_row_idx + self.delta_row_idx <= 7:
                break
        super().gen_next_pos()

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
    'r': '♜', 'nl': '♞', 'nr': '♞', 'bl': '♝', 'br': '♝', 'q': '♛', 'k': '♚', 'p': '♟', # Black Pieces
    'R': '♖', 'NL': '♘', 'NR': '♘', 'BL': '♗', 'BR': '♗', 'Q': '♕', 'K': '♔', 'P': '♙', # White Pieces
    '.': ''                                                      # Empty Square
}

# 5. Your 2D Python Input Array (8x8)
# Lowercase = Black, Uppercase = White, '.' = Empty
### chess_array[row_idx][col_idx] ###
chess_array = [
    ['r', 'nl', 'bl', 'q', 'k', 'br', 'nr', 'r'],  #row 0 black pieces
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'P', '.', '.', '.'],  # E4 Pawn Open example
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', '.', 'P', 'P', 'P'],
    ['R', 'NL', 'BL', 'Q', 'K', 'BR', 'NR', 'R']   #row 7 white pieces
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

def move_next_pos(board_array, piece_obj):
        board_array[piece_obj.curr_row_idx][piece_obj.curr_col_idx] = '.'
        while True:
            piece_obj.gen_next_pos()
            if piece_obj.name.islower(): #Black piece
                if board_array[piece_obj.next_row_idx][piece_obj.next_col_idx] not in ['r', 'nl', 'nr', 'b', 'q', 'k', 'p']:
                    board_array[piece_obj.next_row_idx][piece_obj.next_col_idx] = piece_obj.name
                    break
            else: #White piece
                if board_array[piece_obj.next_row_idx][piece_obj.next_col_idx] not in ['R', 'NL', 'NR', 'B', 'Q', 'K', 'P']:
                    board_array[piece_obj.next_row_idx][piece_obj.next_col_idx] = piece_obj.name
                    break
        piece_obj.curr_col_idx = piece_obj.next_col_idx
        piece_obj.curr_row_idx = piece_obj.next_row_idx

    
clock = pygame.time.Clock()

# 7. Main Game Loop

blkl_kn_obj = Knight('nl', 1, 0)
blkr_kn_obj = Knight('nr', 6, 0)
whtl_kn_obj = Knight('NL', 1, 7)
whtr_kn_obj = Knight('NR', 6, 7)
blkl_bi_obj = Bishop('bl', 2, 0)
blkr_bi_obj = Bishop('br', 5, 0)
whtl_bi_obj = Bishop('BL', 2, 7)
whtr_bi_obj = Bishop('BR', 5, 7)

total_pieces = [blkl_kn_obj, blkr_kn_obj, whtl_kn_obj, whtr_kn_obj, blkl_bi_obj, blkr_bi_obj, whtl_bi_obj, whtr_bi_obj]

running = True
while running:
    for board_obj in total_pieces:

        clock.tick(0.5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
        # Redraw the UI
        draw_board(chess_array)
        pygame.display.flip() #Board is (re)drawn here

        move_next_pos(chess_array, board_obj)

