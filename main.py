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

background = (0, 225, 130)
textcolor = (255, 255, 255)

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


def main():
    global FPS_clock, mainSurface, images, barriers, outside, text, players, currentImage
    pygame.init()
    FPS_clock = pygame.time.Clock()
    sound = pygame.mixer.Sound('music1.wav')
    sound.play()

    mainSurface = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Gold Rush')
    text = pygame.font.Font('arial.ttf', 20)
    tile_size = tile_width, tile_height = 50, 85
    coin_size = coin_width, coin_height = 50, 50

    images = {'goal': pygame.transform.scale(load_image('Bronze_30.png'), coin_size),
              'goal with coin': pygame.transform.scale(load_image('Silver_21.png'), coin_size),
              'coin': pygame.transform.scale(load_image('Silver_21.png'), coin_size),
              'corner': pygame.transform.scale(load_image('Tile_03.png'), tile_size),
              'wall': load_image('crystal_blue2.png'),
              'inside floor': load_image('Plain_Block.png'),
              'outside floor': pygame.transform.scale(load_image('Grass_Block.png'), tile_size),
              'title': load_image('star_title.png'),
              'solved': load_image('star_solved.png'),
              'ghost': load_image('ghost_.png'),
              'boy': load_image('ghost_.png'),
              'girl': load_image('ghost_.png'),
              'cat': load_image('ghost_.png'),
              'pinkgirl': load_image('pinkgirl.png'),
              'rock': load_image('Rock.png'),
              'short tree': pygame.transform.scale(load_image('bush7_3.png'), tile_size),
              'tall tree': pygame.transform.scale(load_image('birch_4.png'), tile_size),
              'ugly tree': pygame.transform.scale(load_image('jungle_tree_5.png'), tile_size)}

    players = [images['ghost'],
                images['boy'],
                images['girl'],
                images['cat'],
                images['pinkgirl']]

    barriers = {'x': images['corner'],
                '#': images['wall'],
                'o': images['inside floor'],
                ' ': images['outside floor']}

    outside = {'1': images['rock'],
                '2': images['short tree'],
                '3': images['tall tree'],
                '4': images['ugly tree']}

    currentImage = 0

    startScreen()

    levels = readLevelsFile('for_play.txt')
    currentLevelIndex = 0


def terminate():
    pygame.quit()
    sys.exit()

