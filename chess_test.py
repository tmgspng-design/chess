chess_array_valid = [
    ['a', 'b', '.', '.', '.', '.', 'c', 'd'],  #row 0 black pieces
    ['e', '.', '.', '.', '.', '.', '.', 'f'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['g', '.', '.', '.', '.', '.', '.', 'h'],
    ['i', 'j', '.', '.', '.', '.', 'k', 'l']   #row 7 white pieces
]
chess_array_inplay = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],  #row 0 black pieces
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', 'Q', '.', 'B', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'P', '.', 'K', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']   #row 7 white pieces
]

attack_pos_list = []
attack_pos_list_bound = []
attack_pos_list_all = []
curr_col_idx = 3
curr_row_idx = 4
chess_array_inplay[curr_row_idx][curr_col_idx] = 'R' #start pos of white piece

#for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
    #for delta_row_idx in [-1 * delta_col_idx, delta_col_idx]:
        #attack_pos_list_all.append([curr_col_idx + delta_col_idx, curr_row_idx + delta_row_idx])

for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
        attack_pos_list_all.append([curr_col_idx + delta_col_idx, curr_row_idx])

for delta_row_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
        attack_pos_list_all.append([curr_col_idx, curr_row_idx + delta_row_idx])

for col, row in attack_pos_list_all:
    if 0 <= col <= 7 and 0 <= row <= 7:
        attack_pos_list_bound.append([col, row])
        attack_pos_list.append([col, row])

for col, row in attack_pos_list_bound:
            #print (f"col={col} row={row}")
            if curr_col_idx < col:
                sgnc = 1 # move RIGHT
            elif curr_col_idx > col:
                sgnc = -1 # move LEFT
            else:
                sgnc = 0
            if curr_row_idx < row:
                sgnr = 1 # move DOWN
            elif curr_row_idx > row:
                sgnr = -1 # move UP
            else:
                sgnr = 0
            print (f"col={col} row={row} sgnc={sgnc} sgnr={sgnr}")
            if sgnc == 0:
                for x in range(curr_row_idx, row + sgnr, sgnr):
                    if x == curr_row_idx:
                        continue
                    elif chess_array_inplay[x][curr_col_idx] in ['R', 'N', 'B', 'Q', 'K', 'P']: # if any pos along path occupied by ally piece
                        attack_pos_list.remove([col, row])
                        break
            elif sgnr == 0:
                for x in range(curr_col_idx, col + sgnc, sgnc):
                    if x == curr_col_idx:
                        continue
                    elif chess_array_inplay[curr_row_idx][x] in ['R', 'N', 'B', 'Q', 'K', 'P']: # if any pos along path occupied by ally piece
                        attack_pos_list.remove([col, row])
                        break
            else:
                for x, y in zip(range(curr_col_idx, col + sgnc, sgnc), range(curr_row_idx, row + sgnr, sgnr)): # check each spot along path to dest stop
                    print (f"x={x} y={y}")
                    if (x, y) == (curr_col_idx , curr_row_idx ): # do not check current piece pos
                        continue
                    elif chess_array_inplay[y][x] in ['R', 'N', 'B', 'Q', 'K', 'P']: # if any pos along path occupied by ally piece
                        attack_pos_list.remove([col, row])
                        break

for col, row in attack_pos_list:
    chess_array_valid[row][col] = 'x'
    pass

