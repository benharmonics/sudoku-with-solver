"""objects.py - static and nonstatic objects"""

import pygame
from random import choice
from settings import *

def zeroes_loc(puzzle):
    row_col = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            if puzzle[i][j] == 0:
                row_col.append([i, j])
    return row_col

def background():
    background = pygame.Surface((board_width, board_width))
    background.fill(smoke)
    return background

def grid():
    surface = background()
    for i in range(1, 9):
        if i % 3 != 0:
            horizontal = pygame.Surface((board_width, grid_line_width))
            vertical = pygame.Surface((grid_line_width, board_width))
            horizontal.fill(dark_blue)
            vertical.fill(dark_blue)
            surface.blit(horizontal, [0, i * block_size - grid_line_width / 2])
            surface.blit(vertical, [i * block_size - grid_line_width / 2, 0])
        else:
            horizontal = pygame.Surface((board_width, 2 *grid_line_width))
            vertical = pygame.Surface((2 * grid_line_width, board_width))
            horizontal.fill(dark_blue)
            vertical.fill(dark_blue)
            surface.blit(horizontal, [0, i * block_size - grid_line_width])
            surface.blit(vertical, [i * block_size - grid_line_width, 0])
    return surface

def initial_surf(puzzle):
    surface = grid()
    font = pygame.font.Font('freesansbold.ttf', 30)
    for i in range(len(puzzle)):
        for j in range(len(puzzle[0])):
            if puzzle[i][j] != 0:
                text_surf = font.render(str(puzzle[i][j]), True, black, None)
                x_centered = j * block_size + block_size / 2
                y_centered = i * block_size + block_size / 2
                text_rect = text_surf.get_rect()
                text_rect.center = (x_centered, y_centered)
                surface.blit(text_surf, text_rect)
    return surface

def small_pencil(surface, destination):
    image = pygame.image.load('misc/pictures/pencil.png')
    image = pygame.transform.scale(image, (small_pencil_size, small_pencil_size))
    rect = image.get_rect()
    rect.center = destination
    surface.blit(image, rect)

def well_done(surface):
    img = pygame.image.load('misc/pictures/well_done.png')
    centerx, centery = int(surface.get_width()/2), int(surface.get_height()/2)
    xloc = int(centerx - img.get_width()/2)
    yloc = int(centery - img.get_height()/2)
    surface.blit(img, [xloc,yloc])

"""mutable objects (sprite classes)"""
class clickableSquare(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.pos_vector = position
        self.row = self.pos_vector[0]
        self.col = self.pos_vector[1]
        self.y = self.row * block_size + board_y + 3
        self.x = self.col * block_size + buffer + 3
        self.width = block_size - 6
        self.hover = False
        self.input_mode = False
        self.pencil_marks = []

        self.image = pygame.Surface((self.width, self.width))
        self.rect = self.image.get_rect()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.main_font = pygame.font.Font('freesansbold.ttf', 30)
        self.small_font = pygame.font.Font('freesansbold.ttf', 14)
        self.num = 0

    def update(self, window, current_puzzle, pencil_mode):
        self.num = current_puzzle[self.row][self.col]   # Ensure sprite & puzzle are synced
        self.pencil_marks = sorted(set(self.pencil_marks))
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + block_size and self.y < pos[1] < self.y + block_size:
            self.hover = True
        else:
            self.hover = False
        if self.hover and not self.input_mode:
            # Hovering over a non-selected square
            self.image.fill(turquoise)
            inner_surf = pygame.Surface((self.width - 2*highlight_width, self.width - 2*highlight_width))
            inner_surf.fill(board_color)
            self.image.blit(inner_surf, [highlight_width, highlight_width])
        elif self.input_mode:
            # Magenta outline on a selected square
            self.image.fill(magenta)
            inner_surf = pygame.Surface((self.width - 2*highlight_width, self.width - 2*highlight_width))
            inner_surf.fill(board_color)
            self.image.blit(inner_surf, [highlight_width, highlight_width])
        else:       # No hover, not in input mode, just colored normally
            self.image.fill(board_color)
        if self.num > 0:    # If a number has been input (not pencil marks)
            if pencil_mode and self.input_mode: # show pencil marks if you're in pencil mode and select square
                for i, mark in enumerate(self.pencil_marks):
                    surf = self.small_font.render(str(mark), True, black, None)
                    rect = surf.get_rect()
                    pos = pencil_position(i)
                    if len(self.pencil_marks) <= 3:
                        pos[1] += 14
                    if 3 < len(self.pencil_marks) <= 6:
                        pos[1] += 7
                    rect.center = (-highlight_width + pos[0], pos[1])
                    self.image.blit(surf, rect)
            else:
                text_surf = self.main_font.render(str(self.num), True, black, None)
                text_rect = text_surf.get_rect()
                text_rect.center = (int(self.width / 2), int(self.width / 2))
                self.image.blit(text_surf, text_rect)
        elif self.num == 0:     # for squares with no current input
            for i, mark in enumerate(self.pencil_marks):
                surf = self.small_font.render(str(mark), True, black, None)
                rect = surf.get_rect()
                pos = pencil_position(i)
                if len(self.pencil_marks) <= 3:
                    pos[1] += 14
                if 3 < len(self.pencil_marks) <= 6:
                    pos[1] += 7
                rect.center = (-highlight_width+pos[0], pos[1])
                self.image.blit(surf, rect)
        window.blit(self.image, self.rect)
        if pencil_mode and self.input_mode:     # draw pencil on the corner of the currently selected square
            small_pencil(window, [self.x+self.width+10, self.y-10])

    def check_hover(self):
        return True if self.hover else False

    def new_input(self, squares_group):
        for obj in squares_group:
            obj.input_mode = False
        self.input_mode = True

    def pencil_mark(self, mark):
        if mark not in self.pencil_marks:
            self.pencil_marks.append(mark)
        else:
            self.pencil_marks.remove(mark)

    def update_to_current(self, puzzle):
        self.num = puzzle[self.row][self.col]

class checkButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = generator_color1
        self.font = pygame.font.Font('freesansbold.ttf', check_button_fontsize)
        self.text_surf = self.font.render(check_button_text, True, white, None)
        self.text_rect = self.text_surf.get_rect()

        self.width = check_button_width
        self.height = check_button_height
        self.button_surf = pygame.Surface((self.width, self.height))
        self.button_surf.fill(self.color)
        self.button_rect = self.button_surf.get_rect()
        self.button_rect.x = check_button_x
        self.button_rect.y = check_button_y
        self.text_rect.center = self.button_rect.center
        self.hover = False

    def update(self, window):
        pos = pygame.mouse.get_pos()
        if self.button_rect.x < pos[0] < self.button_rect.x + self.width and \
                self.button_rect.y < pos[1] < self.button_rect.y + self.height:
            self.hover = True
        else:
            self.hover = False
        if self.hover:
            self.color = check_button_hcolor
        else:
            self.color = check_button_color
        self.button_surf.fill(self.color)
        window.blit(self.button_surf, self.button_rect)
        window.blit(self.text_surf, self.text_rect)

    def check_hover(self):
        return True if self.hover else False

class pencilButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('misc/pictures/pencil.png')
        self.image_scaled = pygame.transform.scale(self.image, (71, 71))
        self.image_flipped = pygame.transform.flip(self.image_scaled, True, False)
        self.rect = self.image_scaled.get_rect()
        self.rect.x = pencil_x
        self.rect.y = pencil_y

        self.width = self.image_scaled.get_width()
        self.height = self.image_scaled.get_height()
        self.hover = False

    def update(self, window, pencil_mode):
        pos = pygame.mouse.get_pos()
        if self.rect.x < pos[0] < self.rect.x + self.width and self.rect.y < pos[1] < self.rect.y + self.height:
            self.hover = True
        else:
            self.hover = False
        if self.hover:
            self.image = self.image_flipped
        else:
            self.image = self.image_scaled
        if pencil_mode:
            img1 = pygame.Surface((self.width, self.height))
            img1.fill(bright_green)
            img2 = pygame.Surface((self.width-2*highlight_width, self.height-2*highlight_width))
            img2.fill(black)
            rect1 = img1.get_rect()
            rect2 = img2.get_rect()
            rect1.x, rect1.y = self.rect.x, self.rect.y
            rect2.x, rect2.y = self.rect.x+highlight_width, self.rect.y+highlight_width
            window.blit(img1, rect1)
            window.blit(img2, rect2)
        window.blit(self.image, self.rect)

    def check_hover(self):
        return True if self.hover else False

class clearButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = clear_button_color
        self.width = clear_button_width
        self.height = clear_button_height

        self.font = pygame.font.Font('freesansbold.ttf', clear_button_fontsize)
        self.textsurf = self.font.render(clear_button_text, True, white, None)
        self.textrect = self.textsurf.get_rect()
        self.buttonsurf = pygame.Surface((self.width, self.height))
        self.buttonrect = self.buttonsurf.get_rect()
        self.buttonrect.x = clear_button_x
        self.buttonrect.y = clear_button_y
        self.textrect.center = self.buttonrect.center
        self.hover = False

    def update(self, window):
        pos = pygame.mouse.get_pos()
        x, y = self.buttonrect.x, self.buttonrect.y
        if x < pos[0] < x + self.width and y < pos[1] < y + self.height:
            self.hover = True
        else:
            self.hover = False
        self.color = clear_button_hcolor if self.hover else clear_button_color
        self.buttonsurf.fill(self.color)
        window.blit(self.buttonsurf, self.buttonrect)
        window.blit(self.textsurf, self.textrect)

    def check_hover(self):
        return True if self.hover else False

class newPuzzleButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = generator_color1
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.text_surf = self.font.render(generator_button_text, True, white, None)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (generator_x_center, generator_y_center)

        self.x = self.text_rect.x - buffer
        self.y = self.text_rect.y - buffer
        self.width = int(self.text_surf.get_width() + 2 * buffer)
        self.height = int(self.text_surf.get_height() + 2 * buffer)
        self.button_surf = pygame.Surface((self.width, self.height))
        self.button_surf.fill(self.color)
        self.button_rect = self.button_surf.get_rect()
        self.button_rect.center = self.text_rect.center
        self.hover = False

    def update(self, window):
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            self.hover = True
        else:
            self.hover = False
        if self.hover:
            self.color = generator_color2
        else:
            self.color = generator_color1
        self.button_surf.fill(self.color)
        window.blit(self.button_surf, self.button_rect)
        window.blit(self.text_surf, self.text_rect)

    def check_hover(self):
        return True if self.hover else False

class difficultyButton(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        pygame.sprite.Sprite.__init__(self)

        self.hover = False
        self.selected = False
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.width = difficulty_button_width
        self.height = difficulty_button_height
        self.difficulty = difficulty
        self.text = difficulty.upper()

        self.button_surf = pygame.Surface((self.width, self.height))
        self.text_surf = self.font.render(self.text, True, white, None)
        self.button_rect = self.button_surf.get_rect()
        self.text_rect = self.text_surf.get_rect()

        self.text_rect.center = (int(self.width/2), int(self.height/2))
        if difficulty == 'easy':
            self.selected = True
            self.button_rect.x = easy_button_x
        elif difficulty == 'med':
            self.button_rect.x = med_button_x
        elif difficulty == 'hard':
            self.button_rect.x = hard_button_x
        self.button_rect.y = difficulty_button_y

    def update(self, window):
        pos = pygame.mouse.get_pos()
        x = self.button_rect.x; y = self.button_rect.y
        if x < pos[0] < x + self.width and y < pos[1] < y + self.height:
            self.hover = True
        else:
            self.hover = False

        if self.hover and self.selected:
            self.button_surf.fill(difficulty_color2)
        if not self.hover and self.selected:
            self.button_surf.fill(difficulty_color1)
        if self.hover and not self.selected:
            self.button_surf.fill(generator_color2)
        if not (self.hover or self.selected):
            self.button_surf.fill(generator_color1)
        self.button_surf.blit(self.text_surf, self.text_rect)
        window.blit(self.button_surf, self.button_rect)

    def new_selection(self, button_group):
        for button in button_group:
            button.selected = False
        self.selected = True

    def check_hover(self):
        return True if self.hover else False

class helpButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = '?'
        self.color = help_button_color
        self.colorh = help_button_hcolor
        self.font = pygame.font.Font('freesansbold.ttf', help_button_text_size)

        self.button_img = pygame.Surface((help_button_width, help_button_height))
        self.button_rect = self.button_img.get_rect()
        self.button_rect.x = help_button_x
        self.button_rect.y = help_button_y

        self.text_img = self.font.render(self.text, True, self.color, None)
        self.render = self.text_img
        self.renderh = self.font.render(self.text, True, self.colorh, None)
        self.text_rect = self.text_img.get_rect()
        self.text_rect.center = (help_button_width/2, help_button_height/2)

        self.hover = False

    def update(self, window):
        pos = pygame.mouse.get_pos()
        self.hover = False
        x, y = self.button_rect.x, self.button_rect.y
        if x < pos[0] < x + help_button_width and y < pos[1] < y + help_button_height:
            self.hover = True
        self.text_img = self.renderh if self.hover else self.render
        self.button_img.blit(self.text_img, self.text_rect)
        window.blit(self.button_img, self.button_rect)

    def check_hover(self):
        return True if self.hover else False

class helpMenu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = help_text
        self.font1 = pygame.font.Font('freesansbold.ttf', help_text_size)
        self.font2 = pygame.font.Font('freesansbold.ttf', 2*help_text_size)
        self.color = generator_color1
        self.hover = False

        self.body_img = pygame.Surface((help_menu_width, help_menu_height))
        self.body_img.fill(self.color)
        self.body_rect = self.body_img.get_rect()
        self.body_rect.x, self.body_rect.y = help_menu_x, help_menu_y

        self.text_img = self.font1.render(help_text[0], True, white, None)
        self.text_height = self.text_img.get_height()
        self.text_rect = self.text_img.get_rect()
        self.text_rect.center = (help_menu_width/2, help_menu_height/2)

        self.close_bkg = pygame.Surface((help_close_width, help_close_width))
        self.close_bkg.fill(generator_color2)
        self.close_bkgrect = self.close_bkg.get_rect()
        self.close_bkgrect.x, self.close_bkgrect.y = help_close_x, help_close_y

        self.close_img = self.font2.render('X', True, white, None)
        self.close_rect = self.close_img.get_rect()
        self.close_rect.center = (help_close_width/2, help_close_width/2)

    def update(self, window):
        self.hover = False
        pos = pygame.mouse.get_pos()
        x, y = self.close_bkgrect.x, self.close_bkgrect.y
        if x < pos[0] < x + self.close_bkg.get_width() and y < pos[1] < y + self.close_bkg.get_width():
            self.hover = True
        if self.hover:
            self.close_bkg.fill(generator_color2)
        else:
            self.close_bkg.fill(generator_color1)
        for i, line in enumerate(help_text):
            img = self.font1.render(line, True, white, None)
            rect = img.get_rect()
            rect.x = 10
            rect.y = 10 + i*self.text_height
            self.body_img.blit(img, rect)
        window.blit(self.body_img, self.body_rect)
        self.close_bkg.blit(self.close_img, self.close_rect)
        window.blit(self.close_bkg, self.close_bkgrect)

    def check_hover(self):
        return True if self.hover else False

class failMessage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.genesis = pygame.time.get_ticks()
        self.font = pygame.font.Font('freesansbold.ttf', 60)
        self.text = choice(fail_messages)
        self.text_image = self.font.render(self.text, True, red, None)
        self.text_rect = self.text_image.get_rect()
        self.centerx = fail_message_centerx
        self.text_rect.x = self.centerx - self.text_image.get_width() / 2 + board_width
        self.text_rect.y = fail_message_y

    def update(self, window):
        if pygame.time.get_ticks() - self.genesis > 2000:
            self.kill()
        window.blit(self.text_image, self.text_rect)

    def check_hover(self):
        return False

class solveButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.hover = False
        self.button_surf = pygame.Surface((solve_button_width, solve_button_height))
        self.button_rect = self.button_surf.get_rect()
        self.button_rect.x = solve_button_x
        self.button_rect.y = solve_button_y
        self.text = solve_button_text

        self.font = pygame.font.Font('freesansbold.ttf', solve_button_fontsize)
        self.text_surf = self.font.render(self.text, True, white, None)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (solve_button_width/2, solve_button_height/2)

    def update(self, window):
        pos = pygame.mouse.get_pos()
        x, y = self.button_rect.x, self.button_rect.y
        if x < pos[0] < x + solve_button_width and y < pos[1] < y + solve_button_height:
            self.hover = True
        else:
            self.hover = False
        if self.hover:
            self.button_surf.fill(solve_button_hcolor)
        else:
            self.button_surf.fill(solve_button_color)
        self.button_surf.blit(self.text_surf, self.text_rect)
        window.blit(self.button_surf, self.button_rect)

    def check_hover(self):
        return True if self.hover else False
