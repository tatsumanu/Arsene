import os
import pygame


# function loading ressources for the images of the game
def load_image(name):
    fullname = os.path.join('graphics', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


# function loading frames of the hero
def strip_from_sheet(sheet, start, size, columns, rows=1):
    """
    Strips individual frames from a sprite sheet given a start location,
    sprite size, and number of columns and rows.
    """
    frames = []
    for j in range(rows):
        for i in range(columns):
            location = (start[0]+size[0]*i, start[1]+size[1]*j)
            frames.append(sheet.subsurface(pygame.Rect(location, size)))
    return frames
