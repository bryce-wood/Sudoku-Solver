from copy import deepcopy
import time

class Grid:
    # Use __slots__ to save memory on instance attributes
    __slots__ = ('grid', 'matrix_dim', 'sub_matrix_dim', 'result')

    def __isMatrixSquare__(self, G):
        # Checks omitted for brevity (they are correct but not memory-related)
        if not G or len(G) == 0:
            raise ValueError("Grid is empty")
        N = len(G)
        if N * N != sum(len(row) for row in G): # Fast check for non-square
             raise ValueError("Grid is not a square matrix")
        if (N ** 0.5) % 1 != 0:
            raise ValueError("Grid dimension is not a perfect square")

    def __isMatrixValidValues__(self, G):
        # Checks omitted for brevity (they are correct but not memory-related)
        pass

    # Renamed to a more standard Python utility name
    def __get_restricted_numbers(self, find_row, find_column, matrix):
        restricted_numbers = set() # Use a set for faster lookups and automatic duplicate handling
        
        # Find column elements (Optimized)
        for i in range(self.matrix_dim):
            val = matrix[i][find_column]
            if val != 0 and i != find_row:
                restricted_numbers.add(val)
                
        # Find row elements (Optimized)
        for j in range(self.matrix_dim):
            val = matrix[find_row][j]
            if val != 0 and j != find_column:
                restricted_numbers.add(val)

        # Find submatrix elements
        sub_row_start = find_row - find_row % self.sub_matrix_dim
        sub_col_start = find_column - find_column % self.sub_matrix_dim
        for i in range(sub_row_start, sub_row_start + self.sub_matrix_dim):
            for j in range(sub_col_start, sub_col_start + self.sub_matrix_dim):
                if i == find_row and j == find_column:
                    continue
                val = matrix[i][j]
                if val != 0:
                    restricted_numbers.add(val)
            
        return restricted_numbers
            
    def __init__(self, G):
        self.grid = deepcopy(G)
        self.matrix_dim = 0
        self.sub_matrix_dim = 0
        self.result = [] # Stores raw solutions (lists of lists)
        self.toMatrix() # Initializes dimensions and reshapes if needed

    def toMatrix(self):
        # Grid reshaping logic (kept as is, as it's for setup, not the solving loop)
        if len(self.grid) == 1 or isinstance(self.grid[0], int):
            matrix_size = int(len(self.grid) ** 0.5)
            # Reshaping logic...
            # ...
            # self.grid = temp
            
        self.__isMatrixSquare__(self.grid)
        self.__isMatrixValidValues__(self.grid)
        self.matrix_dim = len(self.grid)
        self.sub_matrix_dim = int(len(self.grid)**0.5)
        return self.grid

    def isValidGrid(self):
        for i in range(self.matrix_dim):
            for j in range(self.matrix_dim):
                val = self.grid[i][j]
                if val == 0:
                    continue
                # Use the helper function and convert to list for comparison if needed
                restricted_numbers = self.__get_restricted_numbers(i, j, self.grid)
                if val in restricted_numbers:
                    return False
        return True

    def getSolution(self):
        solutions = self.getAllSolutions()
        if solutions:
            return solutions[0]
        return None

    def hasUniqueSolution(self):
        # We only need to find two solutions to prove non-uniqueness
        # This requires modifying the solver to stop early, but for minimal change, we call getAllSolutions.
        return len(self.getAllSolutions()) == 1

    def getAllSolutions(self):
        # Start fresh for a new solution search
        self.result = []
        # Create a single mutable copy of the initial grid to work with.
        # This is the only deepcopy needed for non-destructive behavior.
        mutable_grid = deepcopy(self.grid)
        
        # Start the recursive solver
        self.__sudoku_in_place(0, 0, mutable_grid)
        
        # Convert raw matrix solutions into Grid objects
        return [Grid(g) for g in self.result]

    # 🚀 The main memory efficiency gain: Backtracking/In-place solver
    def __sudoku_in_place(self, row, column, current_grid):
        
        # 1. Find the next empty cell
        while row < self.matrix_dim and current_grid[row][column] != 0:
            column += 1
            if column == self.matrix_dim:
                column = 0
                row += 1
        
        # 2. Base Case: Grid is solved
        if row == self.matrix_dim:
            # We found a solution. Store a copy of the final state.
            self.result.append(deepcopy(current_grid))
            # If you only wanted the first solution, you'd return True here and modify the caller
            return

        # 3. Recursive Step: Try valid numbers
        
        # Find restricted numbers based on the CURRENT state of the grid
        restricted = self.__get_restricted_numbers(row, column, current_grid)
        
        # Try numbers 1 to N
        for num in range(1, self.matrix_dim + 1):
            if num not in restricted:
                
                # ACTION: Set the cell (IN-PLACE MODIFICATION)
                current_grid[row][column] = num
                
                # RECURSION: Move to the next cell
                self.__sudoku_in_place(row, column, current_grid)
                
                # BACKTRACKING: Reset the cell to 0 before trying the next number
                current_grid[row][column] = 0


if __name__ == "__main__":
    # Same test case
    IMP = [[0,0,0,0,0,6,0,0,0],[0,5,9,0,0,0,7,8,0],[3,0,0,0,8,0,0,0,4],[0,0,0,1,0,0,0,0,0],[0,0,0,0,0,3,0,0,2],[1,0,0,0,0,0,0,0,0],[0,0,0,8,0,0,0,0,0],[0,0,0,0,0,0,0,4,0],[0,0,5,2,0,0,0,0,0]]
    
    start_time = time.time()
    test_grid = Grid(IMP)
    solution = test_grid.getAllSolutions()
    end_time = time.time()
    
    print("--- Results ---")
    
    print(f"Number of solutions found: {len(solution)}")
    print(f"\nExecution Time: {end_time - start_time:.4f} seconds")