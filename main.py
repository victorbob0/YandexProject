
#представьте себе код
#он обязательно будет
#прямо здесь
import pygame, sys, os, random, copy
from pygame.locals import *

FPS = 30
width, height = 800, 600
half_width = int(width / 2)
half_height = int(height / 2)
object_width = 50
object_height = 85
object_floor_height = 40

CAM_MOVE_SPEED = 5

outside_decoration = 20

BRIGHTBLUE = (0, 170, 255)
WHITE = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    return image


def terminate():
    pygame.quit()
    sys.exit()

