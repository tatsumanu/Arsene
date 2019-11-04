from functions import strip_from_sheet, load_image
from pygame.locals import *
from random import randint


class Map:

    def __init__(self, level, window, x=0, y=0, grid=[]):
        self.x = x
        self.y = y
        self.level = level
        self.window = window
        self.wall = []
        self.gold = []
        self.start = []
        self.door = []
        self.box = []
        with open(self.level, 'r') as f:
            leveled = f.read()
        self.grid = [[i for i in j] for j in leveled.split('\n')]
        for n in range(22):
            for m in range(13):
                if self.grid[m][n] == 'X':
                    self.wall.append((n*64, m*64))
                if self.grid[m][n] == 'G':
                    self.gold.append((n*64, m*64))
                if self.grid[m][n] == 'S':
                    self.start.append((n*64, m*64))
                if self.grid[m][n] == 'O':
                    self.door.append((n*64, m*64))

    def filling_the_map(self, wall, gold, door, box, door_open):
        for i in self.wall:
            self.window.blit(wall, i)
        for j in self.gold:
            self.window.blit(gold, j)
        for k in self.door:
            if len(self.gold) > 0:
                self.window.blit(door, k)
            else:
                self.window.blit(door_open, k)
        for l in self.box:
            self.window.blit(box, l)

    def obstacle(self, new_pos):
        x, y = new_pos
        if (x, y) in self.wall or (x, y) in self.box:
            return True
        else:
            return False

    def no_more_ground(self, new_pos):
        x, y = new_pos
        while (x, y+64) not in (self.wall + self.box):
            y += 64
        new_pos = x, y
        return new_pos

    def climb_the_wall(self, new_pos, old_pos):
        x, y = new_pos
        xo, yo = old_pos
        if (x, y-64) not in (self.wall + self.box):
            if (xo, yo-64) not in (self.wall + self.box):
                new_pos = x, y-64
                return new_pos
            else:
                return old_pos
        else:
            return old_pos

    def destroy_the_box(self, old_pos, key):
        x, y = old_pos
        if key == 'up':
            if (x, y-64) in self.box:
                self.box.remove((x, y-64))
            else:
                pass
        elif key == 'down':
            if (x, y+64) in self.box:
                self.box.remove((x, y+64))
            else:
                pass


class Player:

    def __init__(self, x=11, y=7, life=1, frames=[]):
        self.x = x*64
        self.y = y*64
        self.life = life
        sheet = load_image('arsene.png')
        size = sheet.get_size()
        self.frames = strip_from_sheet(sheet, (0, 0), (size[0]/3, size[1]/4), 1, 4)
        self.movement = 64

    def acting(self, old_pos, maps, events, frame):
        self.x, self.y = old_pos
        if events == K_RIGHT:
            frame = 1
            new_pos = self.x + self.movement, self.y
            if maps.obstacle(new_pos):
                pos = maps.climb_the_wall(new_pos, old_pos)
                return pos, frame
            else:
                new_pos = maps.no_more_ground(new_pos)
                return new_pos, frame
        elif events == K_LEFT:
            frame = 3
            new_pos = self.x - self.movement, self.y
            if maps.obstacle(new_pos):
                pos = maps.climb_the_wall(new_pos, old_pos)
                return pos, frame
            else:
                new_pos = maps.no_more_ground(new_pos)
                return new_pos, frame
        elif events == K_TAB:
            if frame == 1:
                new_pos = self.x + self.movement, self.y
            else:
                new_pos = self.x - self.movement, self.y
            if maps.obstacle(new_pos):
                return old_pos, frame
            else:
                if new_pos not in maps.gold:
                    maps.box.append(new_pos)
                return old_pos, frame
        elif events == K_DOWN:
            maps.destroy_the_box(old_pos, key='down')
            new_pos = maps.no_more_ground(old_pos)
            return new_pos, frame
        elif events == K_UP:
            maps.destroy_the_box(old_pos, key='up')
            new_pos = maps.no_more_ground(old_pos)
            return new_pos, frame
        else:
            return old_pos, frame

    def collecting_gold(self, maps, door_open):
        if (self.x, self.y) in maps.gold:
            maps.gold.remove((self.x, self.y))


class Enemy:

    def __init__(self, window, x=10, y=5, mvmt=5):
        self.x = x*64
        self.y = y*64
        self.mvmt = mvmt
        self.window = window
        self.img = load_image('vache.png')
        self.x_action = {1: self.x+self.mvmt, 2: self.x-self.mvmt}
        self.y_action = {1: self.y+self.mvmt, 2: self.y-self.mvmt}

    def parsing_the_level(self, maps):
        self.window.blit(self.img, (self.x, self.y))
        if not maps.obstacle((self.x+self.mvmt, self.y)):
            self.x += self.mvmt
        else:
            self.x -= self.mvmt
