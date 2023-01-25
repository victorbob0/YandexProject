import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()

tile_image = {
    'empty': pygame.transform.scale(load_image('grass.png'), (100, 100)),
    'wall': pygame.transform.scale(load_image('wall.png'), (100, 100)),
    'bush': pygame.transform.scale(load_image('bush.png'), (100, 100)),
    'closet': pygame.transform.scale(load_image('closet.png'), (50, 70)),
    'toy': pygame.transform.scale(load_image('toy.png'), (100, 100)),
    'chair': pygame.transform.scale(load_image('chair.png'), (100, 100)),
    'spruce': pygame.transform.scale(load_image('spruce.png'), (100, 100)),
    'ppl': pygame.transform.scale(load_image('chelik.png'), (40, 40)), #нужно заменить спрайт
    'sofa': pygame.transform.scale(load_image('sofa.png'), (100, 100)),
    'cooler': pygame.transform.scale(load_image('cooler.png'), (100, 100)),
    'bed': pygame.transform.scale(load_image('bed.png'), (100, 100)),
    'bench': pygame.transform.scale(load_image('bench.png'), (100, 100)),
    'kitstuff': pygame.transform.scale(load_image('closet.png'), (100, 100)), #нужно заменить спрайт
    'helper': pygame.transform.scale(load_image('chelik.png'), (50, 50)), #нужно заменить спрайт --поправила
    'wayout': pygame.transform.scale(load_image('grass.png'), (100, 100)), #нужно заменить спрайт
    'fridge': pygame.transform.scale(load_image('fridge.png'), (100, 100)),
    'cooker': pygame.transform.scale(load_image('cooker.png'), (100, 100))
}
player_image = load_image('chelik.png')

tile_width = tile_height = 50


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 1000, 1000)


class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for inet in self:
            inet.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_image[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(tile_width * self.pos[0] + 15,
                                               tile_height * self.pos[1] + 5)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Перемещение героя", '',
                  "Герой двигается",
                  "Карта на месте"]
    fon = pygame.transform.scale(load_image('fon.jpg'), size)
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
    filename = 'data/' + filename
    with open(filename, 'r') as mapFile:
         level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '+')), level_map))


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


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up':
        if y > 0 and level_map[y - 1][x] == '+':
            hero.move(x, y - 1)
    elif movement == 'down':
        if y < max_y - 1 and level_map[y + 1][x] == '+':
            hero.move(x, y + 1)
    elif movement == 'left':
        if x > 0 and level_map[y][x - 1] == '+':
            hero.move(x - 1, y)
    elif movement == 'right':
        if x < max_x - 1 and level_map[y][x + 1] == '+':
            hero.move(x + 1, y)


if __name__ == '__main__':
    SIZE = 1000, 1000
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Марио')
    player = None
    ranning = True
    start_screen()
    level_map = load_level('game228.txt')
    hero, max_x, max_y = generate_level(level_map)
    while ranning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ranning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(hero, 'up')
                if event.key == pygame.K_DOWN:
                    move(hero, 'down')
                if event.key == pygame.K_RIGHT:
                    move(hero, 'right')
                if event.key == pygame.K_LEFT:
                    move(hero, 'left')
        screen.fill(pygame.Color('black'))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        pygame.display.flip()
    pygame.quit()