class Piece: # base class for all chess pieces
    def __init__(self, name, symbol, prev_col_idx, prev_row_idx, chess_array):
        self.name = name      # qr qn qb q k kb kn kr - Black ; QR QN QB Q K KB KN KR - White
        self.symbol = symbol  # r n b q k p - Black ; R N B Q K P - White
        self.prev_col_idx = prev_col_idx  # Previous COL position - 0 to 7 from left to right
        self.prev_row_idx = prev_row_idx  # Previous ROW position - 0 to 7 from top to bottom
        self.curr_col_idx = prev_col_idx  # Current COL position - 0 to 7 from left to right
        self.curr_row_idx = prev_row_idx  # Current ROW position - 0 to 7 from top to bottom
        self.active = True # TRUE if piece in play ; FALSE if piece is taken
        self.chess_array = chess_array # pointer to chess board
        self.attack_pos_list_all = []
        self.attack_pos_list_bound = []
        self.attack_pos_list = [] # all available move positions wrt current position and obstacles
        self.move_list = [] # save initial attack_pos_list which is actually avail move list wrt curr pos
        self.move_attack_list = [] # the attack spaces for each avail pos the piece can move to

    def gen_attack_space(self): # base method to create available move/attack positions list
        self.attack_pos_list_bound = []
        self.attack_pos_list = [] # all available move positions wrt current position and obstacles
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
            #print (f"col={col} row={row} sgnc={sgnc} sgnr={sgnr}")
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
                    #print (f"x={x} y={y}")
                    if (x, y) == (self.curr_col_idx , self.curr_row_idx ):
                        continue
                    elif self.chess_array[y][x] in ['R', 'N', 'B', 'Q', 'K', 'P']:
                        self.attack_pos_list.remove([col, row])
                        break

    def gen_move_attack_list(self): # base method to create the attack spaces for each avail pos the piece can move to 
        self.gen_attack_space()
        self.move_list = self.attack_pos_list # save initial attack_pos_list which is actually avail move list wrt curr pos
        for colrow in self.move_list: # check attack space for each move pos
            self.curr_col_idx = colrow[0]
            self.curr_row_idx = colrow[1]
            self.gen_attack_space()
            self.move_attack_list.append([colrow, self.attack_pos_list])

# override base method with piece specific move details in extended classes

class Bishop(Piece):
    def gen_attack_space(self):
        self.attack_pos_list_all = []
        for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            for delta_row_idx in [-1 * delta_col_idx, delta_col_idx]:
                self.attack_pos_list_all.append([self.curr_col_idx + delta_col_idx, self.curr_row_idx + delta_row_idx])
        super().gen_attack_space()

class Rook(Piece):
    def gen_attack_space(self):
        self.attack_pos_list_all = []
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

piece_obj_list += [Bishop('qb', 'b', 3, 4, chess_array)] # black bishop
#piece_obj_list += [Bishop('QB', 'B', 2, 7, chess_array)]
piece_obj_list += [Rook('KR', 'R', 7, 7, chess_array)] # white knight

for obj in piece_obj_list:
    chess_array[obj.curr_row_idx][obj.curr_col_idx] = obj.symbol # place pieces onto chess board

for obj in piece_obj_list:
    obj.gen_move_attack_list() # create availabe move pos for each piece wrt current pos

rook_obj = next((p for p in piece_obj_list if p.name == 'KR'), None) # name rook ptr
bishop_obj = next((p for p in piece_obj_list if p.name == 'qb'), None) # name bishop ptr

for coor, space in rook_obj.move_attack_list:
    for pos in space:
        if bishop_obj.prev_col_idx == pos[0] and bishop_obj.prev_row_idx == pos[1]:
            print (f"move to col={coor[0]} row = {coor[1]}")
    pass

