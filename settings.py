# colors
black = (0, 0, 0)
white = (255, 255, 255)
smoke = (230, 230, 230)
turquoise = (41, 217, 230)
dark_blue = (0, 48, 78)
tangerine = (236, 125, 16)
mikado_yellow = (255, 188, 10)
bright_green = (147, 255, 39)
north_texas_green = (5, 144, 51)
dollar_bill = (147, 203, 86)
lime_green = (50, 205, 50)
magenta = (255, 39, 147)
red = (255, 0, 0)
ue_red = (191, 0, 0)

# window and spacing settings
grid_line_width = 2
window_width = 1000
window_height = int(window_width * 3/5)
buffer = int(window_height / 30)

# for solve function
fps = 60

# block settings
block_size = 60
board_y = int((window_height - block_size * 9) / 2)
board_width = block_size * 9
board_color = smoke

# button settings
sidebar_width = window_width - (buffer + board_width + buffer)

winstate_background_width = 5
highlight_width = 2

generator_button_text = 'NEW PUZZLE'
generator_color1 = dark_blue
generator_color2 = turquoise
generator_xmin = buffer * 2 + block_size * 9
generator_xmax = window_width - buffer
generator_x_center = int(generator_xmin + (generator_xmax - generator_xmin)/2)
generator_y_center = int(window_height * 4/5 - 9)

check_button_text = 'CHECK'
check_button_fontsize = 60
check_button_x = 662
check_button_y = 242
check_button_width = 236
check_button_height = 80
check_button_color = north_texas_green
check_button_hcolor = lime_green

difficulty_button_width = 65
difficulty_button_height = 43
easy_button_x = 662
med_button_x = easy_button_x + difficulty_button_width
hard_button_x = med_button_x + difficulty_button_width
difficulty_button_y = 527
difficulty_color1 = tangerine
difficulty_color2 = mikado_yellow

solve_button_text = 'SOLVE'
solve_button_y = 140
solve_button_x = 662
solve_button_width = 236
solve_button_height = 80
solve_button_fontsize = 60
solve_button_hcolor = lime_green
solve_button_color = north_texas_green

help_button_width = 898 - (hard_button_x + difficulty_button_width)
help_button_height = difficulty_button_height
help_button_x = hard_button_x + difficulty_button_width
help_button_y = difficulty_button_y
help_button_hcolor = bright_green
help_button_color = white
help_button_text_size = 30

help_menu_color = smoke
help_menu_x = 100
help_menu_y = 90
help_menu_width = window_width - 2*help_menu_x
help_menu_height = window_height - 2*help_menu_y
help_text_size = 20
help_text = ['', 'HOW TO PLAY', '', 'The digits 1-9 must be placed in the puzzle such that each digit does not repeat',
             'within any row, column, or any of the 3x3 squares indicated by the thicker',
             'grid lines separating them.', '',
             "Click on the pencil button or press 'p' to enter or exit pencil marking mode,",
             'in which you will be able to make note of which digits are possible in a selected',
             'square. A pencil icon will appear on the upper corner of squares when you',
             'select them by clicking on the square while in pencil marking mode.',
             'Enter the digits which you think might be possible in an empty square,',
             'or press the digit again to remove the digit from the pencil markings.', '',
             'When pencil marking mode is turned off, select a square by clicking on it',
             'and enter a number to place that number in the puzzle. Press backspace to',
             'delete your entry.', '', 'Click the CHECK button to check your solution.']
help_close_x = 840
help_close_y = help_menu_y
help_close_width = 60

pencil_width = 71
pencil_y = 345
pencil_x = 662
pencil_spacing = 56 / 4 # space in a highlighted box to place numbers equidistantly
small_pencil_size = 40  # small pencil in the corner of boxes during pencil mode

clear_button_width = 125
clear_button_height = pencil_width - 20
clear_button_x = pencil_x + pencil_width + 20
clear_button_y = pencil_y + 10
clear_button_text = 'CLEAR'
clear_button_fontsize = 30
clear_button_color = ue_red
clear_button_hcolor = red

def pencil_position(i):
    # Defines pencil position in clickable square. There's probably a better way to do this
    if i == 0: return [14, 14]
    if i == 1: return [28, 14]
    if i == 2: return [42, 14]
    if i == 3: return [14, 28]
    if i == 4: return [28, 28]
    if i == 5: return [42, 28]
    if i == 6: return [14, 42]
    if i == 7: return [28, 42]
    if i == 8: return [42, 42]

# fail state messages (pop up briefly on failed check)
fail_messages = ['Not quite!', 'Try again', 'Hmmm...', 'Sorry!', 'Careful...', 'Nah', 'Not so sure...']
fail_message_y = board_y + buffer
fail_message_centerx = (window_width - board_width + buffer) / 2