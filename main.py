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

    current_level_index = 0
    while True:
        result = running(levels, current_level_index)
        if result in ('solved', 'next'):
            current_level_index += 1
            if current_level_index >= len(levels):
                current_level_index = 0
        elif result == 'back':
            # Go to the previous level.
            current_level_index -= 1
            if current_level_index < 0:
                current_level_index = len(levels) - 1
        elif result == 'reset':
            pass


def isWall(mapObj, x, y):
    if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return False
    elif mapObj[x][y] in ('#', 'x'):
        return True
    return False


def decorateMap(mapObj, xy_start):
    x_start, y_start = xy_start
    copy_map = copy.deepcopy(mapObj)
    for x in range(len(copy_map)):
        for y in range(len(copy_map[0])):
            if copy_map[x][y] in ('$', '.', '@', '+', '*'):
                copy_map[x][y] = ' '
    floodFill(copy_map, x_start, y_start, ' ', 'o')
    for x in range(len(copy_map)):
        for y in range(len(copy_map[0])):

            if copy_map[x][y] == '#':
                if (isWall(copy_map, x, y-1) and isWall(copy_map, x+1, y)) or \
                   (isWall(copy_map, x+1, y) and isWall(copy_map, x, y+1)) or \
                   (isWall(copy_map, x, y+1) and isWall(copy_map, x-1, y)) or \
                   (isWall(copy_map, x-1, y) and isWall(copy_map, x, y-1)):
                    copy_map[x][y] = 'x'

            elif copy_map[x][y] == ' ' and random.randint(0, 99) < outside_decoration:
                copy_map[x][y] = random.choice(list(OUTSIDEDECOMAPPING.keys()))

    return copy_map


def isBlocked(mapObj, state_game, x, y):
    if isWall(mapObj, x, y):
        return True

    elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return True

    elif (x, y) in state_game['stars']:
        return True

    return False


def makeMove(mapObj, state_game, playerMoveTo):
    player_x, player_y = state_game['player']
    stars = state_game['stars']
    if playerMoveTo == UP:
        xOffset = 0
        yOffset = -1
    elif playerMoveTo == RIGHT:
        xOffset = 1
        yOffset = 0
    elif playerMoveTo == DOWN:
        xOffset = 0
        yOffset = 1
    elif playerMoveTo == LEFT:
        xOffset = -1
        yOffset = 0

    if isWall(mapObj, player_x + xOffset, player_y + yOffset):
        return False
    else:
        if (player_x + xOffset, player_y + yOffset) in stars:
            if not isBlocked(mapObj, state_game, player_x + (xOffset*2), player_y + (yOffset*2)):
                ind = stars.index((player_x + xOffset, player_y + yOffset))
                stars[ind] = (stars[ind][0] + xOffset, stars[ind][1] + yOffset)
            else:
                return False
        state_game['player'] = (player_x + xOffset, player_y + yOffset)
        return True


def terminate():
    pygame.quit()
    sys.exit()

