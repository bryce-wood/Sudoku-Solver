from copy import deepcopy
# Representation of a sudoku grid. For any perfect square n, a sudoku grid is
# an n x n matrix containing the symbols 1,...,n, and possibly an "empty"
# symbol. In a complete solution, each symbol 1,...,n appears exactly once in
# each row, column, and sqrt(n) x sqrt(n) sub-square.
class Grid:
    # Construct a new grid from two dimensional matrix G.
    # Raises ValueError if G is not an n x n square matrix with integer values,
    # or if n is not a perfect square.
    def __init__(self,G):
        columns = len(G)
        rows = len(G[0])
        if columns != rows:
            raise ValueError # not a square matrix
        if int(columns ** 0.5) ** 2 != columns:
            raise ValueError # n is not a perfect square
        sideLen = columns
        
        for i in range(sideLen):
            if len(G[i]) != sideLen:
                raise ValueError # not a square matrix
            for j in range(sideLen):
                if not (isinstance(G[i][j], int) and (0 <= G[i][j] <= sideLen)):
                    raise ValueError # invalid value
        # If we reach this point, G is valid
        self.grid = deepcopy(G)


    # Returns a two dimensional matrix representing the grid.
    def toMatrix(self):
        return deepcopy(self.grid)

    # Return True if this grid represents a valid partially filled sudoku
    # board, meaning every cell is empty or contains a valid value and
    # no value appears more than once in any row, column, or sub-square
    def isValidGrid(self):
        grid = self.grid
        sideLen = len(grid)
        subSquareLen = int(sideLen ** 0.5)
        # check rows and columns
        for i in range(sideLen):
            col_nums = set() # we use a set instead of a list, bc sets have O(1) lookup time
            row_nums = set()
            for j in range(sideLen):
                col_num = grid[i][j]
                if col_num != 0:
                    if col_num in col_nums:
                        return False
                    else: 
                        col_nums.add(col_num)
                row_num = grid[j][i]
                if row_num != 0:
                    if row_num in row_nums:
                        return False
                    else:
                        row_nums.add(row_num)
        # check sub-squares
        for sub_i in range(subSquareLen):
            for sub_j in range(subSquareLen):
                nums = set()
                for i in range(subSquareLen):
                    for j in range(subSquareLen):
                        num = grid[sub_i * subSquareLen + i][sub_j * subSquareLen + j]
                        if num != 0:
                            if num in nums:
                                return False
                            else:
                                nums.add(num)
        return True

    # Returns a new Grid with a complete solution of this grid, if it exists,
    # or None otherwise. This method is non-destructive.
    def getSolution(self):
        # slow since it finds all solutions instead of stopping at the first one, but works
        # TODO: stop at first solution found
        solutions = self._allSolutionsHelper(self.grid, set())
        if len(solutions) == 0:
            return None
        else:
            return Grid(solutions.pop())

    # Return True if there is exactly one complete solution of this grid. This
    # method is non-destructive.
    def hasUniqueSolution(self):
        solutions = self._allSolutionsHelper(self.grid, set())
        return len(solutions) == 1

    # Return a (possibly empty) list of Board objects containing all possible
    # solutions of this grid. This method is non-desctructive.
    def getAllSolutions(self):
        solutions = self._allSolutionsHelper(self.grid, set())
        # solutions is a set of tuples, convert to list before returning
        return [Grid([list(row) for row in solution]) for solution in solutions]
    
    # uses recursion with pruning to find all solutions (a set) of the grid
    def _allSolutionsHelper(self, grid, solutions):
        self.grid = grid
        # if invalid, return complete
        if self.isValidGrid() == False:
            return solutions
        sideLen = len(grid)
        empty_found = False
        # recursively try "next" 0 with all possible values (e.g. 1-9)
        for i in range(sideLen):
            for j in range(sideLen):
                if grid[i][j] == 0:
                    empty_found = True
                    for num in range(1, sideLen + 1):
                        new_grid = deepcopy(grid)
                        new_grid[i][j] = num
                        solutions = self._allSolutionsHelper(new_grid, solutions)
                    break
            if empty_found:
                break
        # if solved, add to complete and return
        if not empty_found:
            solutions.add(tuple(tuple(row) for row in grid))
            return solutions
        # return all unique complete solutions
        return solutions