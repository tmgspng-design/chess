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

    def gen_attack_space(self, chess_array):
        attack_pos_list2 = []
        for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
            for delta_row_idx in [-1 * delta_col_idx, delta_col_idx]:
                if 0 <= self.curr_col_idx + delta_col_idx <= 7 and 0 <= self.curr_row_idx + delta_row_idx <= 7:
                    if self.curr_col_idx < self.curr_col_idx + delta_col_idx:
                        sgnc = 1 # move RIGHT
                    else:
                        sgnc = -1 # move LEFT
                    if self.curr_row_idx < self.curr_row_idx + delta_row_idx:
                        sgnr = 1 # move DOWN
                    else:
                        sgnr = -1 # move UP
                    for x, y in zip(range(self.curr_col_idx, self.curr_col_idx + delta_col_idx + sgnc, sgnc), range(self.curr_row_idx, self.curr_row_idx + delta_row_idx + sgnr, sgnr)): # check each spot along path to dest stop
                        if (x, y) == (self.curr_col_idx , self.curr_row_idx ): # do not check current piece pos
                            continue
                        elif chess_array[y][x] in ['R', 'N', 'B', 'Q', 'K', 'P']: # if any pos along path occupied by ally piece
                            break
                        elif (x, y) == (self.curr_col_idx + delta_col_idx, self.curr_row_idx + delta_row_idx): # all path empty so ok to add pos to attack space
                            #attack_pos_list.append([delta_col_idx, delta_row_idx])
                            attack_pos_list2.append([self.curr_col_idx + delta_col_idx, self.curr_row_idx + delta_row_idx])
        return attack_pos_list2
