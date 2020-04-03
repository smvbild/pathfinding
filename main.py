import pygame
import sys
import random

pygame.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)


WIDTH = 600
HEIGHT = int(WIDTH * 2/3)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Rect(object):
    def __init__(self, x, y, w, h):
        self.typedict = {
                'empty': {
                        'c': (255,255,255),
                    },
                'target': {
                        'c': (30,144,255),
                    },
                'start': {
                        'c': (124,252,0)
                    },
                'wall': {
                        'c': (0,0,0)
                    }
                }

        self.type = 'empty'
        self.c = self.typedict[self.type]['c']
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self):
        pygame.draw.rect(screen, self.typedict[self.type]['c'], pygame.Rect(self.x,self.y,self.w,self.h))

    def update(self, solving):
        if solving:
            pass
        else:
            self.is_clicked_prep()

    def is_clicked_prep(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if (pos[0] >= self.x and pos[0] <= self.x + self.w 
                and pos[1] >= self.y and pos[1] <= self.y + self.h):
                typedict_keys = list(self.typedict.keys())
                index = typedict_keys.index(self.type) 
                index = (index + 1) % len(typedict_keys)
                self.type = typedict_keys[index]

        if pygame.mouse.get_pressed()[2]:
            pos = pygame.mouse.get_pos()
            if (pos[0] >= self.x and pos[0] <= self.x + self.w 
                and pos[1] >= self.y and pos[1] <= self.y + self.h):
                typedict_keys = list(self.typedict.keys())
                index = typedict_keys.index(self.type) 
                index -= 1
                if index < 0:
                    index = len(typedict_keys) - 1

                self.type = typedict_keys[index]

class Grid(object):
    def __init__(self, width, height, padding=2):
        self.width = int(width)
        self.height = int(height)
        self.end_width = 2/3 * WIDTH
        self.solving = False

        if padding < 1:
            print('Grid __init__: padding too small. Setting padding to 2')
            self.padding = 2
        else:
            self.padding = padding
    
        
        self.effective_width = self.end_width - (self.width + 1) * padding
        self.effective_height = HEIGHT - (self.height + 1) * padding

        self.effective_width_rect = int(self.effective_width / self.width)
        self.effective_height_rect = int(self.effective_height / self.height)

        self.leftover_space_vertical = HEIGHT - (self.height * self.effective_height_rect + padding * (self.height + 1))

        self.start_y = (self.leftover_space_vertical + padding) // 2

        self.rects = []

        for i in range(self.height):
            self.rects.append([])

        for i in range(self.width):
            for j in range(self.height):

                x = i * self.effective_width_rect + self.padding * i + 1
                y = j * self.effective_height_rect + self.padding * j + self.start_y
                w = self.effective_width_rect
                h = self.effective_height_rect

                self.rects[i].append(Rect(x, y, w, h))

    def start_solving():
        targets = []
        starts = []
        
        for i in range(self.width):
            for j in range(self.height):
                if self.rects[i][j].type == 'target':
                    targets += 1
                if self.rects[i][j].type == 'start':
                    starts += 1

        if len(targets) > 1:
            print('Grid start_solving: too many targets, expected 1')
            return
        if len(starts) > 1:
            print('Grid start_solving: too many starts, expected 1')
            return

        self.soving = True
        print('Started the pathfinding process.')

    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                self.rects[i][j].draw()

    def update(self):
        for i in range(self.width):
            for j in range(self.height):
                self.rects[i][j].update(self.solving)


    def clear(self):
        for i in range(self.width):
            for j in range(self.height):
                self.rects[i][j].type = 'empty'


class Button(object):
    def __init__(self, x, y, w, h, function, grid):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.function = function

        def start():
            if not grid.solving:
                grid.start_solving()

        def quit():
            pygame.quit()
            sys.exit()

        def clear():
            grid.clear()
            grid.solving = False

        self.funcdict = {
                'start': start,
                'quit': quit,
                'clear': clear
                }

    def draw(self):
        pygame.draw.rect(screen, (255,255,255), (self.x, self.y, self.w, self.h))
        textsurface = myfont.render(f'{self.function.upper()}', False, (0,0,0))
        screen.blit(textsurface, (self.x - 25 + self.w // 2, self.y + self.h // 2))

    def is_clicked(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if (pos[0] >= self.x and pos[0] <= self.x + self.w 
                and pos[1] >= self.y and pos[1] <= self.y + self.h):
                self.funcdict[self.function]()

class Menu(object):
    def __init__(self, x, grid, padding=2):
        if padding < 1:
            print('Menu __init__: padding too small. Setting padding to 2')
            self.padding = 2
        else:
            self.padding = padding

        self.x = x + self.padding
        self.y = self.padding
        self.width = WIDTH - self.x - self.padding
        self.height = HEIGHT - self.y - self.padding
        
        self.funcdict = {
                0: 'start',
                1: 'clear',
                2: 'quit'
                }

        self.num_buttons = 3
        self.button_height = (self.height - 2 * padding) // self.num_buttons

        print(self.button_height)

        self.buttons = []

        for i in range(self.num_buttons):
            self.buttons.append(Button(self.x, i * self.button_height + self.y + i * self.padding, self.width, self.button_height, self.funcdict[i], grid))

        print(self.buttons)

    def draw(self):
        for button in self.buttons:
            button.draw()

    def update(self):
        for button in self.buttons:
            button.is_clicked()


grid = Grid(7, 7)
menu = Menu(int(grid.end_width), grid, 2)

def draw():
    grid.draw()
    menu.draw()

def update():
    grid.update()
    menu.update()
        
        

def main():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((51,51,51))

        draw()
        update()

        pygame.display.flip()

        clock.tick(8)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
