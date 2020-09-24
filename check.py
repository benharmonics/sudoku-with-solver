from numpy import array

def check(matrix):
    try:
        correct = True
        if not check_sum(matrix):
            correct = False
        if correct and not check_rows(matrix):
            correct = False
        if correct and not check_columns(matrix):
            correct = False
        if correct and not check_squares(matrix):
            correct = False
        return True if correct else False
    except:
        print('check function error')
        return False

def check_sum(matrix):
    try:
        correct = True
        sum = 0
        for row in matrix:
            for number in row:
                if number < 1 or number > 9 or number != int(number):
                    correct = False
                sum += number
        if sum != 405:
            correct = False
        return True if correct else False
    except:
        print('checksum error')
        return False

def check_rows(matrix):
    correct = True
    for row in matrix:
        if sorted(set(row)) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            correct = False
    return True if correct else False

def check_columns(matrix):
    correct = True
    matrix_array = array(matrix)
    for i in range(9):
        column = matrix_array[:, i]
        if sorted(set(column)) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            correct = False
    return True if correct else False

def check_squares(matrix):
    """using arrays to collect information from each 3x3 subarray, then appending
    all the numbers from the subarray into a list to compare to our check"""
    correct = True
    matrix_array = array(matrix)
    for i in range(3):      # iterable for rows
        for j in range(3):  # iterable for columns
            square_list = []
            square_array = matrix_array[3*i : 3*i+3, 3*j : 3*j+3]
            for row in square_array:
                for number in row:
                    square_list.append(number)
            if sorted(set(square_list)) != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                correct = False
    return True if correct else False

def possibility_check(puzzle, row, col, num):
    """Checks a puzzle to see if a given number will work at a given row, column space in the array"""
    for i in range(9):
        if puzzle[row][i] == num:       # row check
            return False
        if puzzle[i][col] == num:       # col check
            return False
    row0 = (row//3)*3                   # resolves to (0, 1, or 2) * 3 = 0, 3, or 6
    col0 = (col//3)*3                   # 0, 3, or 6. Used for starting (upper left) square of inner squares.
    for i in range(3):
        for j in range(3):              # Checking inner squares with double loop of length 3
            if puzzle[row0+i][col0+j] == num:
                return False
    return True

def solve(puzzle, spaces, cached_puzzles, count):
    """Solves a puzzle using backtracking"""
    if check(puzzle):
        cached_puzzles[count] = array(puzzle)
        count += 1
        log_solutions(cached_puzzles, count)
    for i, space in enumerate(spaces):
        if puzzle[space[0]][space[1]] == 0:
            for num in range(1, 10):
                if possibility_check(puzzle, space[0], space[1], num):
                    cached_puzzles[count] = array(puzzle)
                    count +=1
                    puzzle[space[0]][space[1]] = num
                    solve(puzzle, spaces, cached_puzzles, count)
                    if not check(puzzle):
                        cached_puzzles[count] = array(puzzle)
                        count += 1
                        puzzle[space[0]][space[1]] = 0
            return

def log_solutions(cached_puzzles, count):
    with open('misc/solution.py', 'w+') as f:
        f.write('')         # clear solution
    with open('misc/solution.py', 'w') as f:
        f.write('\ncache = [\n')
        for i in range(count):
            f.write('    [')
            for j, row in enumerate(cached_puzzles[i]):
                if j > 0:
                    f.write('    ')
                f.write(str(list(row)))
                f.write(',\n')
            f.write('    ],\n')
        f.write(']\n')