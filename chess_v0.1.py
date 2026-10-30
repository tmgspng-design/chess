class Piece: # base class for all chess pieces
    def __init__(self, name, symbol, curr_col_idx, curr_row_idx, chess_array):
        self.name = name      # qr qn qb q k kb kn kr - Black ; QR QN QB Q K KB KN KR - White
        self.symbol = symbol  # r n b q k p - Black ; R N B Q K P - White
        self.curr_col_idx = curr_col_idx  # Current COL position - 0 to 7 from left to right
        self.curr_row_idx = curr_row_idx  # Current ROL position - 0 to 7 from top to bottom
        self.active = True # TRUE if piece in play ; FALSE if piece is taken
        self.chess_array = chess_array # pointer to chess board
        self.attack_pos_list_all = []
        self.attack_pos_list_bound = []
        self.attack_pos_list = [] # all available move positions wrt current position and obstacles

    def gen_attack_space(self): # base method to create available move positions list
        for col, row in self.attack_pos_list_all:
            if 0 <= col <= 7 and 0 <= row <= 7:
                self.attack_pos_list_bound.append([col, row])
                self.attack_pos_list.append([col, row])
        for col, row in self.attack_pos_list_bound: # go thru & remove pos from list if obstacles along its path
            #print (f"col={col} row={row}")
            if self.curr_col_idx < col:
                sgnc = 1 # move RIGHT
            elif self.curr_col_idx > col:
                sgnc = -1 # move LEFT
            else:
                sgnc = 0 # no R/L motion
            if self.curr_row_idx < row:
                sgnr = 1 # move DOWN
            elif self.curr_row_idx > row:
                sgnr = -1 # move UP
            else:
                sgnr = 0 # no D/U motion
            print (f"col={col} row={row} sgnc={sgnc} sgnr={sgnr}")
            if sgnc == 0: # only D/U motion
                for x in range(self.curr_row_idx, row + sgnr, sgnr): # check along vertical path
                    if x == self.curr_row_idx:
                        continue
                    elif self.chess_array[x][self.curr_col_idx] in ['R', 'N', 'B', 'Q', 'K', 'P']:
                        self.attack_pos_list.remove([col, row])
                        break
            elif sgnr == 0: # only R/L motion
                for x in range(self.curr_col_idx, col + sgnc, sgnc): # check along horizontal path
                    if x == self.curr_col_idx:
                        continue
                    elif self.chess_array[self.curr_row_idx][x] in ['R', 'N', 'B', 'Q', 'K', 'P']:
                        self.attack_pos_list.remove([col, row])
                        break
            else: # both R/L and D/U motion
                for x, y in zip(range(self.curr_col_idx, col + sgnc, sgnc), range(self.curr_row_idx, row + sgnr, sgnr)): # check along diag path
                    print (f"x={x} y={y}")
                    if (x, y) == (self.curr_col_idx , self.curr_row_idx ):
                        continue
                    elif self.chess_array[y][x] in ['R', 'N', 'B', 'Q', 'K', 'P']:
                        self.attack_pos_list.remove([col, row])
                        break

# override base method with piece specific move details in extended classes

class Bishop(Piece):
    def gen_attack_space(self):
        for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            for delta_row_idx in [-1 * delta_col_idx, delta_col_idx]:
                self.attack_pos_list_all.append([self.curr_col_idx + delta_col_idx, self.curr_row_idx + delta_row_idx])
        super().gen_attack_space()

class Rook(Piece):
    def gen_attack_space(self):
        for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            self.attack_pos_list_all.append([self.curr_col_idx + delta_col_idx, self.curr_row_idx])
        for delta_row_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            self.attack_pos_list_all.append([self.curr_col_idx, self.curr_row_idx + delta_row_idx])
        super().gen_attack_space()

chess_array = [
#     qr   qn   qb   q    k   kb   kn   kr
    ['.', '.', '.', '.', '.', '.', '.', '.'],  #row 0 black pieces
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'Q', '.', 'B', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'P', '.', 'K', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']   #row 7 white pieces
#     QR   QN   QB   Q    K   KB   KN   KR
] # col 0                              col 7

piece_obj_list = [] #name, symbol, col, row, chess_array

piece_obj_list += [Bishop('QB', 'B', 2, 7, chess_array)]
piece_obj_list += [Rook('KR', 'R', 7, 7, chess_array)]

for obj in piece_obj_list:
    chess_array[obj.curr_row_idx][obj.curr_col_idx] = obj.symbol # place pieces onto chess board

for obj in piece_obj_list:
    obj.gen_attack_space() # create availabe move pos for each piece

for obj in piece_obj_list:
    for col, row in obj.attack_pos_list:
        chess_array[row][col] = 'x' # mark all available pos for all pieces on board (may overlap)
        pass
