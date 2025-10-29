import sudoku
from copy import deepcopy

def main():
    n_tests = 0
    n_pass = 0
    n_fail = 0
    
    A = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    n_tests += 1
    passing = runTest("confirming malformed input raises ValueError",
        formatTest, A, ValueError)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    A = [[0,0,0], [0,0,0], [0,0,0]]
    n_tests += 1
    passing = runTest("confirming non-square length raises ValueError",
        formatTest, A, ValueError)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("confirming valid grid is valid",
        validationTest, GRID1, True)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("toMatrix on 4x4 grid",
        toMatrixTest, FOURBYFOUR)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("toMatrix on 9x9 grid",
        toMatrixTest, GRID1)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("toMatrix on 16x16 grid",
        toMatrixTest, BIG)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    A = deepcopy(GRID1)
    A[0][0] = 1
    n_tests += 1
    passing = runTest("confirming grid with invalid row is invalid",
        validationTest, A, False)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    A[0][0] = 2
    n_tests += 1
    passing = runTest("confirming grid with invalid column is invalid",
        validationTest, A, False)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    A[0][0] = 4
    n_tests += 1
    passing = runTest("confirming grid with invalid subsquare is invalid",
        validationTest, A, False)
    if passing:
        n_pass += 1
    else:
        n_fail += 1
    
    n_tests += 1
    passing = runTest("checking fully solved grid has solution",
        hasSolutionTest, GRID1S, True)
    if passing:
        n_pass += 1
    else:
        n_fail += 1
    
    n_tests += 1
    passing = runTest("checking grid with one solution has solution",
        hasSolutionTest, GRID1, True)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("checking grid with two solutions has solution",
        hasSolutionTest, GRID2, True)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("checking grid with no solution has no solution",
        hasSolutionTest, IMP, False)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("checking fully solved grid for unique solution",
        hasUniqueSolutionTest,GRID1S,True)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("checking grid with one solution for unique solution",
        hasUniqueSolutionTest,GRID1,True)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("checking grid with two solutions for unique solution",
        hasUniqueSolutionTest,GRID2,False)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("checking grid with no solution for unique solution",
        hasUniqueSolutionTest,IMP,False)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("solving fully solved grid", correctUniqueSolutionTest,
        GRID1S, GRID1S)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("solving grid with unique solution",
        correctUniqueSolutionTest, GRID1, GRID1S)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("finding both solutions to grid with two solutions",
        countTest,GRID2,2)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("finding 0 solutions to impossible grid",
        countTest,IMP,0)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("finding all solutions to blank 4x4 grid",
        countTest,FOURBYFOUR,288)
    if passing:
        n_pass += 1
    else:
        n_fail += 1

    n_tests += 1
    passing = runTest("solving big grid with unique solution",
        correctUniqueSolutionTest, BIG, BIGS)
    if passing:
        n_pass += 1
    else:
        n_fail += 1
    
    print("\n")
    print("Testing complete.")
    print("\tPASS: %d" % n_pass)
    print("\tFAIL: %d" % n_fail)
    print("\tSKIP: %d" % (n_tests - n_pass - n_fail))

def formatTest(matrix, error):
    passed = False

    try:
        grid = sudoku.Grid(matrix)
    except Exception as e:
        passed = (type(e) is error)

    return passed

def validationTest(matrix, expected):
    grid = sudoku.Grid(matrix)
    return (grid.isValidGrid() == expected)

def hasSolutionTest(matrix, expected):
    grid = sudoku.Grid(matrix)
    return ((grid.getSolution() is not None) == expected)

def toMatrixTest(matrix):
    grid = sudoku.Grid(matrix)
    m = grid.toMatrix()

    n = len(matrix)
    passing = n == len(m)
    for r in range(n):
        for c in range(n):
            if passing:
                passing = passing and (matrix[r][c] == m[r][c])

    return passing

def hasUniqueSolutionTest(matrix, expected):
    grid = sudoku.Grid(matrix)
    return (grid.hasUniqueSolution() == expected)

def correctUniqueSolutionTest(unsolved, solved):
    grid = sudoku.Grid(unsolved)
    sln = grid.getSolution()
    if sln is None:
        return False
    matrix = sln.toMatrix()

    passing = True
    for r in range(len(matrix)):
        for c in range(len(matrix)):
            passing = passing and (matrix[r][c] == solved[r][c])

    return passing

def countTest(matrix,expected):
    grid = sudoku.Grid(matrix)
    slns = grid.getAllSolutions()
    return (len(slns) == expected)

def runTest(name,test,*args):
    passed = True

    print("Testing %s..." % name)
    try:
        passed = test(*args)
    except NotImplementedError:
        print("\tTest failed. Function not implemented.")
        passed = False
    except Exception as e:
        print("\tTest failed. Unexpected error: %s" % e)
        passed = False
    else:
        if passed:
            print("\tPASS")
        else:
            print("\tFAIL")
    
    return passed

GRID1 = []
GRID1.append([0,3,1,2,0,0,0,0,5])
GRID1.append([0,5,0,0,0,0,0,4,0])
GRID1.append([0,0,4,0,5,9,0,8,0])
GRID1.append([0,8,9,5,7,0,4,0,0])
GRID1.append([2,0,0,1,0,6,0,0,9])
GRID1.append([0,0,5,0,9,3,7,1,0])
GRID1.append([0,9,0,7,3,0,5,0,0])
GRID1.append([0,4,0,0,0,0,0,6,0])
GRID1.append([5,0,0,0,0,8,3,9,0])

GRID1S = []
GRID1S.append([6,3,1,2,8,4,9,7,5])
GRID1S.append([9,5,8,6,1,7,2,4,3])
GRID1S.append([7,2,4,3,5,9,6,8,1])
GRID1S.append([1,8,9,5,7,2,4,3,6])
GRID1S.append([2,7,3,1,4,6,8,5,9])
GRID1S.append([4,6,5,8,9,3,7,1,2])
GRID1S.append([8,9,6,7,3,1,5,2,4])
GRID1S.append([3,4,7,9,2,5,1,6,8])
GRID1S.append([5,1,2,4,6,8,3,9,7])

GRID2 = []
GRID2.append([6,3,0,0,8,4,9,7,5])
GRID2.append([9,5,8,6,0,7,0,4,3])
GRID2.append([7,0,4,3,5,9,6,8,0])
GRID2.append([0,8,9,5,7,0,4,3,6])
GRID2.append([0,7,3,0,4,6,8,5,9])
GRID2.append([4,6,5,8,9,3,7,0,0])
GRID2.append([8,9,6,7,3,0,5,0,4])
GRID2.append([3,4,7,9,0,5,0,6,8])
GRID2.append([5,0,0,4,6,8,3,9,7])

IMP = []
IMP.append([0,7,0,0,6,0,0,0,0])
IMP.append([9,0,0,0,0,0,0,4,1])
IMP.append([0,0,8,0,9,0,0,5,0])
IMP.append([0,9,0,0,7,0,0,0,2])
IMP.append([0,0,3,0,0,0,8,0,0])
IMP.append([4,0,0,8,0,0,0,1,0])
IMP.append([0,8,0,3,0,0,9,0,0])
IMP.append([1,6,0,0,0,0,0,0,7])
IMP.append([0,0,0,5,0,0,0,8,0])

FOURBYFOUR = []
FOURBYFOUR.append([0,0,0,0])
FOURBYFOUR.append([0,0,0,0])
FOURBYFOUR.append([0,0,0,0])
FOURBYFOUR.append([0,0,0,0])

BIG = []
BIG.append([11, 2, 0, 7, 0, 0, 0,15, 6,14,16, 1, 0, 3, 0,13])
BIG.append([ 0, 4,16, 9,11, 8, 2, 0, 0, 0, 0, 0,15, 1, 0, 6])
BIG.append([ 1,10,15,12, 6, 0, 7, 0, 4, 0, 8, 0, 0, 0,14,16])
BIG.append([ 0, 8, 6, 3, 0, 0, 1, 0, 0, 0,15,12,10, 0, 4, 2])
BIG.append([ 0, 0,14, 0, 0, 0, 0, 0, 1, 6,10, 0, 0, 0, 3,15])
BIG.append([ 3, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0,15, 8, 0, 6,11])
BIG.append([ 0, 0, 0,13, 2, 0, 0, 0, 0,11, 0, 0, 7, 4, 0, 9])
BIG.append([ 0,11, 8, 4,16, 0, 0,13, 7, 0, 9, 3,14, 0, 0, 1])
BIG.append([ 2, 0, 0,15, 3, 7, 0, 4, 5, 0, 0, 9,16,13,12, 8])
BIG.append([ 7, 0,12, 8, 0, 0,10, 0, 0, 0, 0,11, 4, 0, 0, 3])
BIG.append([ 4, 9, 0, 5,14, 0,13, 0, 0, 0, 0, 0, 0, 0, 0,10])
BIG.append([10,13, 0, 0, 0, 6,12, 1, 0, 0, 0, 0, 0, 7, 0, 5])
BIG.append([ 9, 1, 0,14, 7, 4, 0, 0, 0,15, 5, 6, 3, 0,13, 0])
BIG.append([ 8, 3, 7,10, 0, 9, 6, 2, 0, 1, 0, 4, 5, 0,16, 0])
BIG.append([15,16, 4,11, 0, 5, 8,10, 0, 3, 2,13, 1, 6, 9, 7])
BIG.append([ 5, 0,13, 0, 0, 0,15,14, 9, 0, 0, 0, 2, 0,11, 4])

BIGS = []
BIGS.append([11, 2, 5, 7, 4, 10, 9, 15, 6, 14, 16, 1, 12, 3, 8, 13])
BIGS.append([14, 4, 16, 9, 11, 8, 2, 12, 13, 5, 3, 10, 15, 1, 7, 6])
BIGS.append([1, 10, 15, 12, 6, 13, 7, 3, 4, 9, 8, 2, 11, 5, 14, 16])
BIGS.append([13, 8, 6, 3, 5, 14, 1, 16, 11, 7, 15, 12, 10, 9, 4, 2])
BIGS.append([16, 7, 14, 2, 8, 11, 4, 9, 1, 6, 10, 5, 13, 12, 3, 15])
BIGS.append([3, 5, 9, 1, 10, 12, 14, 7, 2, 4, 13, 15, 8, 16, 6, 11])
BIGS.append([12, 15, 10, 13, 2, 1, 3, 6, 8, 11, 14, 16, 7, 4, 5, 9])
BIGS.append([6, 11, 8, 4, 16, 15, 5, 13, 7, 12, 9, 3, 14, 2, 10, 1])
BIGS.append([2, 14, 1, 15, 3, 7, 11, 4, 5, 10, 6, 9, 16, 13, 12, 8])
BIGS.append([7, 6, 12, 8, 9, 2, 10, 5, 16, 13, 1, 11, 4, 14, 15, 3])
BIGS.append([4, 9, 3, 5, 14, 16, 13, 8, 15, 2, 12, 7, 6, 11, 1, 10])
BIGS.append([10, 13, 11, 16, 15, 6, 12, 1, 3, 8, 4, 14, 9, 7, 2, 5])
BIGS.append([9, 1, 2, 14, 7, 4, 16, 11, 10, 15, 5, 6, 3, 8, 13, 12])
BIGS.append([8, 3, 7, 10, 13, 9, 6, 2, 12, 1, 11, 4, 5, 15, 16, 14])
BIGS.append([15, 16, 4, 11, 12, 5, 8, 10, 14, 3, 2, 13, 1, 6, 9, 7])
BIGS.append([5, 12, 13, 6, 1, 3, 15, 14, 9, 16, 7, 8, 2, 10, 11, 4])

if __name__ == '__main__':
    main()
