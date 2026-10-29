class Piece:
    def __init__(self, name, symbol, curr_col_idx, curr_row_idx, chess_array):
        self.name = name      # Obj name
        self.symbol = symbol  # r n b q k p R N B Q K P
        self.curr_col_idx = curr_col_idx  # Init Col Index
        self.curr_row_idx = curr_row_idx  # Init Row Index
        #self.delta_col_idx = 0
        #self.delta_row_idx = 0
        #self.next_col_idx = 0 # Final Col Index
        #self.next_row_idx = 0 # Final Row Index
        self.active = True # In play
        self.chess_array = chess_array # pointer to chess board
        self.attack_pos_list_all = []
        self.attack_pos_list_bound = []
        self.attack_pos_list = []

    def gen_attack_space(self):
        for col, row in self.attack_pos_list_all:
            if 0 <= col <= 7 and 0 <= row <= 7:
                self.attack_pos_list_bound.append([col, row])
                self.attack_pos_list.append([col, row])
        for col, row in self.attack_pos_list_bound:
            #print (f"col={col} row={row}")
            if self.curr_col_idx < col:
                sgnc = 1 # move RIGHT
            elif self.curr_col_idx > col:
                sgnc = -1 # move LEFT
            else:
                sgnc = 0
            if self.curr_row_idx < row:
                sgnr = 1 # move DOWN
            elif self.curr_row_idx > row:
                sgnr = -1 # move UP
            else:
                sgnr = 0
            print (f"col={col} row={row} sgnc={sgnc} sgnr={sgnr}")
            if sgnc == 0:
                for x in range(self.curr_row_idx, row + sgnr, sgnr):
                    if x == self.curr_row_idx:
                        continue
                    elif self.chess_array[x][self.curr_col_idx] in ['R', 'N', 'B', 'Q', 'K', 'P']: # if any pos along path occupied by ally piece
                        self.attack_pos_list.remove([col, row])
                        break
            elif sgnr == 0:
                for x in range(self.curr_col_idx, col + sgnc, sgnc):
                    if x == self.curr_col_idx:
                        continue
                    elif self.chess_array[self.curr_row_idx][x] in ['R', 'N', 'B', 'Q', 'K', 'P']: # if any pos along path occupied by ally piece
                        self.attack_pos_list.remove([col, row])
                        break
            else:
                for x, y in zip(range(self.curr_col_idx, col + sgnc, sgnc), range(self.curr_row_idx, row + sgnr, sgnr)): # check each spot along path to dest stop
                    print (f"x={x} y={y}")
                    if (x, y) == (self.curr_col_idx , self.curr_row_idx ): # do not check current piece pos
                        continue
                    elif self.chess_array[y][x] in ['R', 'N', 'B', 'Q', 'K', 'P']: # if any pos along path occupied by ally piece
                        self.attack_pos_list.remove([col, row])
                        break
        #return attack_pos_list

class Bishop(Piece):
    def gen_attack_space(self):
        for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            for delta_row_idx in [-1 * delta_col_idx, delta_col_idx]:
                self.attack_pos_list_all.append([self.curr_col_idx + delta_col_idx, self.curr_row_idx + delta_row_idx])
        super().gen_attack_space()

chess_array = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],  #row 0 black pieces
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'Q', '.', 'B', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'P', '.', 'K', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']   #row 7 white pieces
]

bishop_obj = Bishop('BL', 'B', 2, 7, chess_array)

bishop_obj.gen_attack_space()

for col, row in bishop_obj.attack_pos_list:
    chess_array[row][col] = 'x'
    pass
