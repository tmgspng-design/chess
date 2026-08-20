import random

class Piece:
    """A class containing both data and a method."""
    def __init__(self, name):
        self.name = name      # Obj name
        self.curr_col_idx = 1   # Init Col Index
        self.curr_row_idx = 0   # Init Row Index

    def display_info(self):
        """Method that utilizes the object's data."""
        return f"Name: {self.name}"

    def gen_next_pos(self):
        delta_col_idx = 0
        while True:
            delta_col_idx = random.choice([-2,-1,1,2])
            if delta_col_idx in [-2,2]:
                delta_row_idx = random.choice([-1,1])
            else: # delta_col_idx in [-1,1]
                delta_row_idx = random.choice([-2,2])
            if self.curr_col_idx + delta_col_idx >= 0 and self.curr_row_idx + delta_row_idx >= 0:
                break
        print(f"Delta RC  {delta_row_idx}  {delta_col_idx}")
        self.curr_col_idx = self.curr_col_idx + delta_col_idx
        self.curr_row_idx = self.curr_row_idx + delta_row_idx

# Configuration for 64 objects (e.g., an 8x8 2D array)
rows, cols = 8, 8
grid_2d = [[0 for _ in range(cols)] for _ in range(rows)]

# 1. Populate the 2D array with 32 Piece instances
obj_name = f"_Knight_"
knight_obj = Piece(obj_name)
grid_2d[knight_obj.curr_row_idx][knight_obj.curr_col_idx] = knight_obj

# 2. Access and test the method on one of the 32 objects
# Let's target the object at row 1, column 2 (index [0][1])
target_object = grid_2d[0][1]
print("Testing the method on a single object:")
print(target_object.display_info())
print("-" * 35)

# 3. Iterate through all 64 objects in the 2D array and call their method
print("Executing the method across all 64 objects in the 2D array:")

for _ in range(5):

    print(f"          R  C")
    print(f"          O  O")
    print(f"          W  L")
    for row_idx in range(rows):
        for col_idx in range(cols):
            current_obj = grid_2d[row_idx][col_idx]
            if current_obj != 0:
                print(f"Position [{row_idx}][{col_idx}] -> {current_obj.display_info()}")
            else:
                print(f"Position [{row_idx}][{col_idx}] -> *Position Empty*")

    grid_2d[knight_obj.curr_row_idx][knight_obj.curr_col_idx] = 0
    knight_obj.gen_next_pos()
    grid_2d[knight_obj.curr_row_idx][knight_obj.curr_col_idx] = knight_obj

