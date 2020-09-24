"""main.py - main file for the sudoku game. run in conjunction with objects.py, puzzles.py, settings.py,
check.py, as well as the misc folder containing solution.py, data.txt, and a pictures folder"""

import pygame
import objects
import puzzles
import importlib
from random import choice
from check import check, solve
from settings import *
import misc.solution

pygame.init()

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Sudoku')
clock = pygame.time.Clock()

current_puzzle = None  # Puzzle stored as an array (list)
starting_board = None  # Will be GUI object built by objects.py
currently_selected_square = None    # Selected/highlighted blank square on the puzzle
difficulty = 'easy'
pencil_mode = True      # Pencil mark entry mode (enter multiple numbers)
solving_mode = False    # Used when player clicks solve button
solution_found = False  # Used to save resources
display_index = 0       # displays indexed puzzle from misc/solution.py
win_state = False       # True when puzzle is filled and check button is pressed

# Sprite groups
buttons = pygame.sprite.Group()
difficulty_buttons = pygame.sprite.Group()      # Group is necessary for a function in the object
interactive_squares = pygame.sprite.Group()     # Clickable squares in puzzle are manipulated as a group sometimes
popups = pygame.sprite.Group()

# Create sprite objects and add to group (not interactive squares yet until we have a puzzle)
new_puzzle_button = objects.newPuzzleButton()
check_button = objects.checkButton()
solve_button = objects.solveButton()
easy_button = objects.difficultyButton('easy')
med_button = objects.difficultyButton('med')
hard_button = objects.difficultyButton('hard')
help_button = objects.helpButton()
clear_button = objects.clearButton()
pencil_button = objects.pencilButton()  # requires unique update information and is not added to the buttons group
buttons.add(new_puzzle_button)
buttons.add(check_button)
buttons.add(solve_button)
buttons.add(easy_button)
buttons.add(med_button)
buttons.add(hard_button)
buttons.add(help_button)
buttons.add(clear_button)
difficulty_buttons.add(easy_button)
difficulty_buttons.add(med_button)
difficulty_buttons.add(hard_button)

run = True  # this bool controls the game loop
"""Main Game Loop"""
while run:
    """Part 1 - Controls and player inputs (the longest part but not the important part)"""
    for event in pygame.event.get():
        """Part 1A - Events - check collision when clicked etc"""
        # quit if you press the close button
        if event.type == pygame.QUIT:
            run = False
        # All clickable buttons updated under MOUSEBUTTONDOWN section
        if event.type == pygame.MOUSEBUTTONDOWN:
            solving_mode = False    # exits solving mode by clicking away
            if win_state:
                win_state = False   # Conveniently deletes the 'Well Done!' message just by clicking away
            if currently_selected_square:  # Clears selected before checking collision
                currently_selected_square.input_mode = False
                currently_selected_square = None
            if new_puzzle_button.check_hover() and not popups:  # Puzzle generator button (New Puzzle)
                starting_board = None
            if check_button.check_hover():      # Check puzzle button
                if check(current_puzzle):       # Solve-check passed
                    win_state = True               # creates a popup message
                elif not popups:                # Solve-check failed
                    message = objects.failMessage()
                    popups.add(message)
            if pencil_button.check_hover():     # Pencil mode button
                pencil_mode = False if pencil_mode else True  # Turns mode off if on / on if off when clicked
            if help_button.check_hover():       # Help button - pulls up help menu on how to play
                help = objects.helpMenu()
                popups.add(help)
            if clear_button.check_hover():
                for s in interactive_squares:
                    row, col = s.pos_vector
                    current_puzzle[row][col] = 0
                    s.pencil_marks = []
            if solve_button.check_hover():      # Solve button
                if not solution_found:          # expensive function if puzzle needs to be solved
                    for s in interactive_squares:   # Clear puzzle
                        row, col = s.pos_vector
                        current_puzzle[row][col] = 0
                    solve(current_puzzle, objects.zeroes_loc(current_puzzle), {}, 0)    # logs to misc.solution
                    solution_found = True       # no need to call solve() func again if we already have solution
                    fps_index = 0               # at 60 fps we change display every 10 frames
                for s in interactive_squares:       # Clear puzzle again after solving & logging solution
                    row, col = s.pos_vector         # and/or before entering solving_mode
                    current_puzzle[row][col] = 0
                importlib.reload(misc.solution)     # reload file cause we updated it, old version still in memory
                display_index = 0                   # Index of the first thing we load from misc.solution
                solving_mode = True                 # See below for Part 3
            for object in buttons:
                if object.check_hover() and isinstance(object, objects.difficultyButton):   # Difficulty buttons
                    object.new_selection(difficulty_buttons)    # Color change
                    if difficulty != object.difficulty:         # Change board if new difficulty is selected
                        starting_board = None
                    difficulty = object.difficulty
            for object in popups:
                if object.check_hover() and isinstance(object, objects.helpMenu):   # Help popup menu / close button
                    object.kill()
            for object in interactive_squares:  # Squares in puzzle
                if object.check_hover():
                    object.new_input(interactive_squares)
                    currently_selected_square = object
        """Part 1B - Input keys"""
        if pencil_mode:     # Stores up to 9 digits in a square at once as pencil marks; press key again to remove
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_1:
                currently_selected_square.pencil_mark(1)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_2:
                currently_selected_square.pencil_mark(2)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_3:
                currently_selected_square.pencil_mark(3)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_4:
                currently_selected_square.pencil_mark(4)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_5:
                currently_selected_square.pencil_mark(5)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_6:
                currently_selected_square.pencil_mark(6)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_7:
                currently_selected_square.pencil_mark(7)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_8:
                currently_selected_square.pencil_mark(8)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_9:
                currently_selected_square.pencil_mark(9)
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_BACKSPACE:
                currently_selected_square.pencil_marks = []
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pencil_mode = False
        else:       # Updates the actual puzzle
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_1:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 1
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_2:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 2
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_3:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 3
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_4:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 4
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_5:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 5
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_6:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 6
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_7:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 7
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_8:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 8
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_9:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 9
            if event.type == pygame.KEYDOWN and currently_selected_square and event.key == pygame.K_BACKSPACE:
                row, col = currently_selected_square.pos_vector
                current_puzzle[row][col] = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pencil_mode = True

    """Part 2 - Setting up board if it has been cleared by generator button, solving mode stuff"""
    if not starting_board:  # starting_board is the pygame Surface set up with fixed digits (initial board)
        win_state = False
        solving_mode = False
        solution_found = False
        for sprite in interactive_squares:
            sprite.kill()
        if difficulty == 'easy':
            current_puzzle = choice(puzzles.easy)
        if difficulty == 'med':
            current_puzzle = choice(puzzles.medium)
        if difficulty == 'hard':
            current_puzzle = choice(puzzles.hard)
        starting_board = objects.initial_surf(current_puzzle)   # the 'frame' of the board without interactivity
        spaces = objects.zeroes_loc(current_puzzle)     # Location of clickable squares [row, col] vector
        for space in spaces:                            # Clickable squares are sprite objects
            square = objects.clickableSquare(space)
            interactive_squares.add(square)

    """Part 3 - Solving mode stuff"""
    if solving_mode:
        if display_index < len(misc.solution.cache) and fps_index%15 == 0:  # only change every 15 frames
            current_puzzle = misc.solution.cache[display_index]     # display_index is initiated to 0 in sec
            display_index += 1
        if check(current_puzzle):
            solving_mode = False
        fps_index += 1      # ticks up once per frame, display is changed every 15 ticks (at 60 fps)

    """Part 4 - Draw stuff to the screen"""
    window.fill(black)
    window.blit(starting_board, [buffer, board_y])  # the non-interactive 'frame' of the interactive stuff
    buttons.update(window)  # general parameters
    pencil_button.update(window, pencil_mode)   # unique parameters
    interactive_squares.update(window, current_puzzle, pencil_mode) # unique parameters
    popups.update(window)   # popups gotta be drawn last
    if win_state:
        objects.well_done(window)
    pygame.display.flip()   # refresh display
    clock.tick(fps)         # tick such that we get 60 fps
pygame.quit()