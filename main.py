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
    global FPS_clock, mainSurface, images, TILEMAPPING, OUTSIDEDECOMAPPING, text, PLAYERIMAGES, currentImage
    pygame.init()
    FPS_clock = pygame.time.Clock()
    sound = pygame.mixer.Sound('music1.wav')
    sound.play()

    mainSurface = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Gold Rush')
    text = pygame.font.Font('arial.ttf', 20)

    def main():
        global FPS_clock, mainSurface, images, barriers, outside, text, players, currentImage
        pygame.init()
        FPS_clock = pygame.time.Clock()
        sound = pygame.mixer.Sound('music1.wav')
        sound.play()

        mainSurface = pygame.display.set_mode((width, height))

        pygame.display.set_caption('Gold Rush')
        text = pygame.font.Font('arial.ttf', 20)

        images = {'goal': pygame.image.load('.png'),
                  'goal with coin': pygame.image.load('.png'),
                  'coin': pygame.image.load('.png'),
                  'corner': pygame.image.load('.png'),
                  'wall': pygame.image.load('.png'),
                  'inside floor': pygame.image.load('.png'),
                  'outside floor': pygame.image.load('.png'),
                  'title': pygame.image.load('.png'),
                  'solved': pygame.image.load('.png'),
                  'girl': pygame.image.load('.png'),
                  'boy': pygame.image.load('.png'),
                  'ghost': pygame.image.load('.png'),
                  'cat': pygame.image.load(''),
                  'pinkgirl': pygame.image.load(''),
                  'rock': pygame.image.load('.png'),
                  'short tree': pygame.image.load('.png'),
                  'tall tree': pygame.image.load('.png'),
                  'ugly tree': pygame.image.load('.png')}

        players = [images['girl'],
                   images['boy'],
                   images['ghost'],
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

