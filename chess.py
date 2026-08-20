import random

class Piece:
    """A class containing both data and a method."""
    def __init__(self, name):
        self.name = name      # Data
        self.curr_pos_x = 1   # Init Row Pos
        self.curr_pos_y = 0   # Init Col Pos
        self.next_pos_x = 0   # Next Row Pos
        self.next_pos_y = 0   # Next Col Pos

    def display_info(self):
        """Method that utilizes the object's data."""
        return f"Name: {self.name}"

    def gen_next_pos(self):
        local_delta_x = random.choice([-2,-1,1,2])
        if local_delta_x in [-2,2]:
            local_delta_y = random.choice([-1,1])
        else: # local_delta_x in [-1,1]
            local_delta_y = random.choice([-2,2])
        print(f"local X: {local_delta_x}")
        print(f"local Y: {local_delta_y}")
        self.curr_pos_x = self.curr_pos_x + local_delta_x
        self.curr_pos_y = self.curr_pos_y + local_delta_y

# Configuration for 64 objects (e.g., an 8x8 2D array)
rows, cols = 8, 8
grid_2d = [[0 for _ in range(cols)] for _ in range(rows)]

# 1. Populate the 2D array with 32 Piece instances
obj_name = f"_Knight_"
knight_obj = Piece(obj_name)
grid_2d[knight_obj.curr_pos_y][knight_obj.curr_pos_x] = knight_obj

# 2. Access and test the method on one of the 32 objects
# Let's target the object at row 1, column 2 (index [0][1])
target_object = grid_2d[0][1]
print("Testing the method on a single object:")
print(target_object.display_info())
print("-" * 35)

# 3. Iterate through all 64 objects in the 2D array and call their method
print("Executing the method across all 32 objects in the 2D array:")
for row_idx in range(rows):
    for col_idx in range(cols):
        current_obj = grid_2d[row_idx][col_idx]
        if current_obj != 0:
            print(f"Position [{row_idx}][{col_idx}] -> {current_obj.display_info()}")
        else:
            print(f"Position [{row_idx}][{col_idx}] -> *Position Empty*")

grid_2d[knight_obj.curr_pos_y][knight_obj.curr_pos_x] = 0
knight_obj.gen_next_pos()
grid_2d[knight_obj.curr_pos_y][knight_obj.curr_pos_x] = knight_obj

for row_idx in range(rows):
    for col_idx in range(cols):
        current_obj = grid_2d[row_idx][col_idx]
        if current_obj != 0:
            print(f"Position [{row_idx}][{col_idx}] -> {current_obj.display_info()}")
        else:
            print(f"Position [{row_idx}][{col_idx}] -> *Position Empty*")
