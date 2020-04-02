import pygame
import random

pygame.init()

WIDTH = 400
HEIGHT = 400

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

    def is_clicked(self):
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if (pos[0] >= self.x and pos[0] <= self.x + self.w 
                and pos[1] >= self.y and pos[1] <= self.y + self.h):
                typedict_keys = list(self.typedict.keys())
                index = typedict_keys.index(self.type) 
                index = (index + 1) % len(typedict_keys)
                self.type = typedict_keys[index]
                return True
            else:
                return False

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
                return True
            else:
                return False

class Grid(object):
    def __init__(self, width, height, padding):
        self.width = int(width)
        self.height = int(height)

        if padding < 1:
            print('Grid __init__: padding too small. Setting padding to 1')
            self.padding = 1
        else:
            self.padding = padding

        effective_width = WIDTH - (self.width + 1) * padding
        effective_height = HEIGHT - (self.height + 1) * padding

        effective_width_rect = int(effective_width / self.width)
        effective_height_rect = int(effective_height / self.height)

        leftover_space_horizontal = WIDTH - (self.width * effective_width_rect + padding * (self.width + 1))
        leftover_space_vertical = HEIGHT - (self.height * effective_height_rect + padding * (self.height + 1))

        start_x = (leftover_space_horizontal + padding) // 2
        start_y = (leftover_space_vertical + padding) // 2

        self.rects = []

        for i in range(self.height):
            self.rects.append([])

        for i in range(self.width):
            for j in range(self.height):

                x = i * effective_width_rect + padding * i + start_x
                y = j * effective_height_rect + padding * j + start_y
                w = effective_width_rect
                h = effective_height_rect

                self.rects[i].append(Rect(x, y, w, h))
        
    def draw(self):
        for i in range(self.width):
            for j in range(self.height):
                self.rects[i][j].draw()

    def update(self):
        for i in range(self.width):
            for j in range(self.height):
                if(self.rects[i][j].is_clicked()):
                    print(i, j)

        

def main():
    grid = Grid(7, 7, 2)

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill((51,51,51))

        grid.update()
        grid.draw()

        pygame.display.flip()

        clock.tick(8)

    pygame.quit()

if __name__ == '__main__':
    main()
