class Piece:
    """A class containing both data and a method."""
    def __init__(self, name):
        self.name = name      # Data

    def display_info(self):
        """Method that utilizes the object's data."""
        return f"Name: {self.name}"

# Configuration for 64 objects (e.g., an 8x8 2D array)
rows, cols = 8, 8
grid_2d = [[0 for _ in range(cols)] for _ in range(rows)]

# 1. Populate the 2D array with 32 Piece instances
obj_name = f"_Knight_"
grid_2d[0][1] = Piece(obj_name)

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

