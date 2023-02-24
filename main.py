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
    text = pygame.font.Font('data/arial.ttf', 20)
    tile_size = tile_width, tile_height = 50, 85
    coin_size = coin_width, coin_height = 50, 50

    images = {'goal': pygame.transform.scale(load_image('Bronze_30.png'), coin_size),
              'goal with coin': pygame.transform.scale(load_image('Silver_21.png'), coin_size),
              'coin': pygame.transform.scale(load_image('Silver_21.png'), coin_size),
              'corner': pygame.transform.scale(load_image('Tile_03.png'), tile_size),
              'wall': load_image('crystal_blue2.png'),
              'inside floor': load_image('Plain_Block.png'),
              'outside floor': pygame.transform.scale(load_image('Grass_Block.png'), tile_size),
              'title': load_image('titlle_image.png'),
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
    levels = readFile('for_play.txt')

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


def running(levels, levelnumber):
    global currentImage
    levelObj = levels[levelnumber]
    mapObj = decorateMap(levelObj['mapObj'], levelObj['startState']['player'])
    gameStateObj = copy.deepcopy(levelObj['startState'])
    mapNeedsRedraw = True
    levelSurf = text.render('Level %s of %s' % (levelnumber + 1, len(levels)), 1, textcolor)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (20, height - 35)
    mapWidth = len(mapObj) * object_width
    mapHeight = (len(mapObj[0]) - 1) * object_floor_height + object_height
    MAX_CAM_X_PAN = abs(half_height - int(mapHeight / 2)) + object_width
    MAX_CAM_Y_PAN = abs(half_width - int(mapWidth / 2)) + object_height

    levelIsComplete = False

    camera_setX = 0
    camera_setY = 0

    cameraUp, cameraDown, cameraLeft, cameraRight = False, False, False, False

    while True:
        playermove = None
        keyPressed = False

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                keyPressed = True
                if event.key == K_LEFT:
                    playermove = LEFT
                elif event.key == K_RIGHT:
                    playermove = RIGHT
                elif event.key == K_UP:
                    playermove = UP
                elif event.key == K_DOWN:
                    playermove = DOWN

                elif event.key == K_a:
                    cameraLeft = True
                elif event.key == K_d:
                    cameraRight = True
                elif event.key == K_w:
                    cameraUp = True
                elif event.key == K_s:
                    cameraDown = True

                elif event.key == K_n:
                    return 'next'
                elif event.key == K_b:
                    return 'back'

                elif event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_BACKSPACE:
                    return 'reset'
                elif event.key == K_p:
                    currentImage += 1
                    if currentImage >= len(players):
                        currentImage = 0
                    mapNeedsRedraw = True

            elif event.type == KEYUP:
                if event.key == K_a:
                    cameraLeft = False
                elif event.key == K_d:
                    cameraRight = False
                elif event.key == K_w:
                    cameraUp = False
                elif event.key == K_s:
                    cameraDown = False

        if playermove != None and not levelIsComplete:
            moved = makeMove(mapObj, gameStateObj, playermove)
            if moved:
                gameStateObj['stepCounter'] += 1
                mapNeedsRedraw = True
            if isLevelFinished(levelObj, gameStateObj):
                levelIsComplete = True
                keyPressed = False

        mainSurface.fill(background)

        if mapNeedsRedraw:
            mapSurf = drawMap(mapObj, gameStateObj, levelObj['goals'])
            mapNeedsRedraw = False

        if cameraUp and camera_setY < MAX_CAM_X_PAN:
            camera_setY += CAM_MOVE_SPEED
        elif cameraDown and camera_setY > -MAX_CAM_X_PAN:
            camera_setY -= CAM_MOVE_SPEED
        if cameraLeft and camera_setX < MAX_CAM_Y_PAN:
            camera_setX += CAM_MOVE_SPEED
        elif cameraRight and camera_setX > -MAX_CAM_Y_PAN:
            camera_setX -= CAM_MOVE_SPEED

        mapSurfRect = mapSurf.get_rect()
        mapSurfRect.center = (half_width + camera_setX, half_height + camera_setY)

        mainSurface.blit(mapSurf, mapSurfRect)

        mainSurface.blit(levelSurf, levelRect)
        stepSurf = text.render('Steps: %s' % (gameStateObj['stepCounter']), 1, textcolor)
        stepRect = stepSurf.get_rect()
        stepRect.bottomleft = (20, height - 10)
        mainSurface.blit(stepSurf, stepRect)

        if levelIsComplete:
            solvedRect = images['solved'].get_rect()
            solvedRect.center = (half_width, half_height)
            mainSurface.blit(images['solved'], solvedRect)

            if keyPressed:
                return 'solved'

        pygame.display.update()
        FPS_clock.tick()


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
                copy_map[x][y] = random.choice(list(outside.keys()))

    return copy_map


def isBlocked(mapObj, state_game, x, y):
    if isWall(mapObj, x, y):
        return True

    elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return True

    elif (x, y) in state_game['coins']:
        return True

    return False


def makeMove(mapObj, state_game, playermove):
    player_x, player_y = state_game['player']
    coins = state_game['coins']
    if playermove == UP:
        xOffset = 0
        yOffset = -1
    elif playermove == RIGHT:
        xOffset = 1
        yOffset = 0
    elif playermove == DOWN:
        xOffset = 0
        yOffset = 1
    elif playermove == LEFT:
        xOffset = -1
        yOffset = 0

    if isWall(mapObj, player_x + xOffset, player_y + yOffset):
        return False
    else:
        if (player_x + xOffset, player_y + yOffset) in coins:
            if not isBlocked(mapObj, state_game, player_x + (xOffset*2), player_y + (yOffset*2)):
                ind = coins.index((player_x + xOffset, player_y + yOffset))
                coins[ind] = (coins[ind][0] + xOffset, coins[ind][1] + yOffset)
            else:
                return False
        state_game['player'] = (player_x + xOffset, player_y + yOffset)
        return True


def startScreen():
    titleRect = images['title'].get_rect()
    topCoord = 50
    titleRect.top = topCoord
    titleRect.centerx = half_width
    topCoord += titleRect.height

    instructionText = ['Передвигайте монеты на необходимые поля.',
                       'Используйте стрелочки для передвижения,',
                       ' W A S D для управления камерой, P для изменения персонажа.',
                       'Backspace для обновления уровня, Esc для выхода из игры.',
                       'N для перехода на следующий уровень, B для возвращения на предыдущий уровень.']

    mainSurface.fill(background)
    mainSurface.blit(images['title'], titleRect)

    for i in range(len(instructionText)):
        instSurf = text.render(instructionText[i], 1, textcolor)
        instRect = instSurf.get_rect()
        topCoord += 10
        instRect.top = topCoord
        instRect.centerx = half_width
        topCoord += instRect.height
        mainSurface.blit(instSurf, instRect)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

        pygame.display.update()
        FPS_clock.tick()


def readFile(filename):
    assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
    mapFile = open(filename, 'r')
    content = mapFile.readlines() + ['\r\n']
    mapFile.close()

    levels = []
    levelnum = 0
    mapTextLines = []
    mapObj = []
    for linenum in range(len(content)):
        line = content[linenum].rstrip('\r\n')

        if line != '':
            mapTextLines.append(line)
        elif line == '' and len(mapTextLines) > 0:
            maxWidth = -1
            for i in range(len(mapTextLines)):
                if len(mapTextLines[i]) > maxWidth:
                    maxWidth = len(mapTextLines[i])
            for i in range(len(mapTextLines)):
                mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))
            for x in range(len(mapTextLines[0])):
                mapObj.append([])
            for y in range(len(mapTextLines)):
                for x in range(maxWidth):
                    mapObj[x].append(mapTextLines[y][x])

            start_x = None
            start_y = None
            goals = []
            coins = []
            for x in range(maxWidth):
                for y in range(len(mapObj[x])):
                    if mapObj[x][y] in ('@', '+'):
                        start_x = x
                        start_y = y
                    if mapObj[x][y] in ('.', '+', '*'):
                        goals.append((x, y))
                    if mapObj[x][y] in ('$', '*'):
                        coins.append((x, y))

            assert start_x != None and start_y != None, 'Level %s (around line %s) in %s is missing a "@" or "+" to mark the start point.' % (
            levelnum + 1, linenum, filename)
            assert len(goals) > 0, 'Level %s (around line %s) in %s must have at least one goal.' % (
            levelnum + 1, linenum, filename)
            assert len(coins) >= len(goals), 'Level %s (around line %s) in %s is impossible to solve. It has %s goals but only %s coins.' % (
            levelnum + 1, linenum, filename, len(goals), len(coins))

            gameStateObj = {'player': (start_x, start_y),
                            'stepCounter': 0,
                            'coins': coins}
            levelObj = {'width': maxWidth,
                        'height': len(mapObj),
                        'mapObj': mapObj,
                        'goals': goals,
                        'startState': gameStateObj}

            levels.append(levelObj)

            mapTextLines = []
            mapObj = []
            gameStateObj = {}
            levelnum += 1
    return levels


def floodFill(mapObj, x, y, oldCharacter, newCharacter):
    if mapObj[x][y] == oldCharacter:
        mapObj[x][y] = newCharacter

    if x < len(mapObj) - 1 and mapObj[x + 1][y] == oldCharacter:
        floodFill(mapObj, x + 1, y, oldCharacter, newCharacter)
    if x > 0 and mapObj[x - 1][y] == oldCharacter:
        floodFill(mapObj, x - 1, y, oldCharacter, newCharacter)
    if y < len(mapObj[x]) - 1 and mapObj[x][y + 1] == oldCharacter:
        floodFill(mapObj, x, y + 1, oldCharacter, newCharacter)
    if y > 0 and mapObj[x][y - 1] == oldCharacter:
        floodFill(mapObj, x, y - 1, oldCharacter, newCharacter)

def drawMap(mapObj, game_state, goals):
    map_width = len(mapObj) * object_width
    map_height = (len(mapObj[0]) - 1) * object_floor_height + object_height
    map_surf = pygame.Surface((map_width, map_height))
    map_surf.fill(background)
    for x in range(len(mapObj)):
        for y in range(len(mapObj[x])):
            space_rect = pygame.Rect((x * object_width, y * object_floor_height, object_width, object_height))
            if mapObj[x][y] in barriers:
                base_tile = barriers[mapObj[x][y]]
            elif mapObj[x][y] in outside:
                base_tile = barriers[' ']
            map_surf.blit(base_tile, space_rect)

            if mapObj[x][y] in outside:
                map_surf.blit(outside[mapObj[x][y]], space_rect)
            elif (x, y) in game_state['coins']:
                if (x, y) in goals:
                    map_surf.blit(images['goal with coin'], space_rect)
                map_surf.blit(images['coin'], space_rect)
            elif (x, y) in goals:
                map_surf.blit(images['goal'], space_rect)
            if (x, y) == game_state['player']:
                map_surf.blit(players[currentImage], space_rect)
    return map_surf


def isLevelFinished(level, game_state):
    for goal in level['goals']:
        if goal not in game_state['coins']:
            return False
    return True


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()

