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



'''def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)'''

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('стол.png'), size)
    screen.blit((fon), (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '+'), level_map))


tile_images = {
    'empty': pygame.transform.scale(load_image('grass.png'), (100, 100)),
    'wall': pygame.transform.scale(load_image('wall.png'), (100, 100)),
    'bush': pygame.transform.scale(load_image('bush.png'), (100, 100)),
    'closet': pygame.transform.scale(load_image('closet.png'), (100, 100)),
    'toy': pygame.transform.scale(load_image('toy.png'), (100, 100)),
    'chair': pygame.transform.scale(load_image('chair.png'), (100, 100)),
    'spruce': pygame.transform.scale(load_image('spruce.png'), (100, 100)),
    'ppl': pygame.transform.scale(load_image('chelik.png'), (100, 100)), #нужно заменить спрайт
    'sofa': pygame.transform.scale(load_image('sofa.png'), (100, 100)),
    'cooler': pygame.transform.scale(load_image('cooler.png'), (100, 100)),
    'bed': pygame.transform.scale(load_image('bed.png'), (100, 100)),
    'bench': pygame.transform.scale(load_image('bench.png'), (100, 100)),
    'kitstuff': pygame.transform.scale(load_image('closet.png'), (100, 100)), #нужно заменить спрайт
    'helper': pygame.transform.scale(load_image('chelik.png'), (100, 100)), #нужно заменить спрайт
    'wayout': pygame.transform.scale(load_image('grass.png'), (100, 100)), #нужно заменить спрайт
    'fridge': pygame.transform.scale(load_image('fridge.png'), (100, 100)),
    'cooker': pygame.transform.scale(load_image('cooker.png'), (100, 100))
}
player_image = load_image('chelik.png')

tile_width = tile_height = 50
player = None


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()




class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '+':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'K':
                Tile('bush', x, y)
            elif level[y][x] == '%':
                Tile('closet', x, y)
            elif level[y][x] == 'C':
                Tile('chair', x, y)
            elif level[y][x] == 'E':
                Tile('spruce', x, y)
            elif level[y][x] == 'D':
                Tile('sofa', x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
            elif level[y][x] == 'V':
                Tile('cooler', x, y)
            elif level[y][x] == '$':
                Tile('bed', x, y)
            elif level[y][x] == 'H':
                Tile('bench', x, y)
            elif level[y][x] == 'Y':
                Tile('kitstuff', x, y)
            elif level[y][x] == '6':
                Tile('helper', x, y)
            elif level[y][x] == '5':
                Tile('wayout', x, y)
            elif level[y][x] == 'X':
                Tile('fridge', x, y)
            elif level[y][x] == 'P':
                Tile('cooker', x, y)
            elif level[y][x] == '>':
                Tile('toy', x, y)
            elif level[y][x] == '^':
                Tile('empty', x, y)
            elif level[y][x] == 'G':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y



class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target, width, height):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)



camera = Camera()





if __name__ == '__main__':
    pygame.init()
    start_screen()
    size = WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode(size)
    player, level_x, level_y = generate_level(load_level('data/game228.txt'))
    camera.update(player, WIDTH, HEIGHT)
    running = True
    x_pos = 0
    clock = pygame.time.Clock()
    pygame.display.flip()
    #start_screen()
    for sprite in all_sprites:
        camera.apply(sprite)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        pygame.display.update()


