import pygame
from pygame.locals import *
from functions import load_image
from Classes import Map, Player, Enemy


pygame.init()

# creating pygame window
window = pygame.display.set_mode((1408, 832))

# variables
wall = load_image('blue_brick.png')
gold = load_image('gold.png')
box = load_image('box.png')
door = load_image('door.png')
door_open = load_image('door_open.png')

frame = 2

pygame.display.set_caption("Arsene Lapin")
pygame.display.set_icon(gold)

# creating Map and Player objects
level_01 = Map('map_01.txt', window)
arsene = Player()
cow = Enemy(window)

# main loop
while True:

    pygame.time.Clock().tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        if event.type == KEYDOWN:
            old_pos = arsene.x, arsene.y
            events = event.key
            (arsene.x, arsene.y), frame = arsene.acting(old_pos, level_01, events, frame)

    pygame.Surface.fill(window, (0, 0, 0))
    arsene.collecting_gold(level_01, door_open)
    level_01.filling_the_map(wall, gold, door, box, door_open)
    window.blit(arsene.frames[frame], (arsene.x, arsene.y))
    cow.parsing_the_level(level_01)


    pygame.display.update()
