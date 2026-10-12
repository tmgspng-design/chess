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
    ['.', '.', 'Q', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', 'R', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'K', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.']   #row 7 white pieces
]

attack_pos_list = []
attack_pos_list2 = []
curr_col_idx = 3
curr_row_idx = 4
#chess_array_inplay[curr_col_idx][curr_row_idx] = 'B' #start pos of white piece
chess_array_inplay[curr_row_idx][curr_col_idx] = 'B' #start pos of white piece

#def find_attack_space():
for delta_col_idx in [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]:
    for delta_row_idx in [-1 * delta_col_idx, delta_col_idx]:
        #attack_pos_list += (delta_col_idx, delta_row_idx)
        if 0 <= curr_col_idx + delta_col_idx <= 7 and 0 <= curr_row_idx + delta_row_idx <= 7:
            if curr_col_idx < curr_col_idx + delta_col_idx:
                sgnc = 1 # move RIGHT
            else:
                sgnc = -1 # move LEFT
            if curr_row_idx < curr_row_idx + delta_row_idx:
                sgnr = 1 # move DOWN
            else:
                sgnr = -1 # move UP
            count = 0 # number of occupied spaces in vector
            for x, y in zip(range(curr_col_idx, curr_col_idx + delta_col_idx + sgnc, sgnc), range(curr_row_idx, curr_row_idx + delta_row_idx + sgnr, sgnr)): # check each spot along path to dest stop
                if chess_array_inplay[y][x] != ".": # if position is already taken by piece (first/orig spot will always be take by orig piece pos)
                    count += 1
                if (x, y) == (curr_col_idx + delta_col_idx, curr_row_idx + delta_row_idx): # arrive here means spot not empty so need to check if ally
                    if chess_array_inplay[y][x] in ['R', 'N', 'B', 'Q', 'K', 'P']: # the checked spot already has a white piece
                        count -= 1
            if count == 1: # no positions taken (all empty)
                attack_pos_list.append([delta_col_idx, delta_row_idx])
                attack_pos_list2.append([curr_col_idx + delta_col_idx, curr_row_idx + delta_row_idx])

#find_attack_space()

for dcol, drow in attack_pos_list:
    #chess_array_valid[curr_col_idx + dcol][curr_row_idx + drow] = 'x'
    chess_array_valid[curr_row_idx + dcol][curr_col_idx + drow] = 'x'
    pass
    #breakpoint()

# end of program
