from copy import deepcopy
# Representation of a sudoku grid. For any perfect square n, a sudoku grid is
# an n x n matrix containing the symbols 1,...,n, and possibly an "empty"
# symbol. In a complete solution, each symbol 1,...,n appears exactly once in
# each row, column, and sqrt(n) x sqrt(n) sub-square.
class Grid:
    grid = None  # two dimensional matrix representing the grid
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
            if len(G[i] != sideLen):
                raise ValueError # not a square matrix
            for j in range(sideLen):
                if not (isinstance(G[i][j], int) and (0 <= G[i][j] <= sideLen)):
                    raise ValueError # invalid value
        # If we reach this point, G is valid
        self.grid = deepcopy(G)


    # Returns a two dimensional matrix representing the grid.
    def toMatrix(self):
        raise NotImplementedError

    # Return True if this grid represents a valid partially filled sudoku
    # board, meaning every cell is empty or contains a valid value and
    # no value appears more than once in any row, column, or sub-square
    def isValidGrid(self):
        raise NotImplementedError

    # Returns a new Grid with a complete solution of this grid, if it exists,
    # or None otherwise. This method is non-destructive.
    def getSolution(self):
        raise NotImplementedError

    # Return True if there is exactly one complete solution of this grid. This
    # method is non-destructive.
    def hasUniqueSolution(self):
        raise NotImplementedError

    # Return a (possibly empty) list of Board objects containing all possible
    # solutions of this grid. This method is non-desctructive.
    def getAllSolutions(self):
        raise NotImplementedError
