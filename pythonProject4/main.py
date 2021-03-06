import pygame
import pygame_gui

maps_d = 'MAPS'
tile_size = 40
WAR_EVENT_TYPE = 30
pygame.init()
size = width, height = 620, 560
screen = pygame.display.set_mode(size)
j = 0

background = pygame.Surface((620, 560))
color = (174, 96, 170)
background.fill(pygame.Color(color))
manager = pygame_gui.UIManager((620, 560))
screen.blit(background, (0, 0))

my_image = pygame.image.load("data/fon5.jpg").convert_alpha()
scaled_image = pygame.transform.scale(my_image, (620, 560))
screen.blit(scaled_image, (0, 0))

my_image = pygame.image.load("data/hero4.png").convert_alpha()
scaled_image = pygame.transform.scale(my_image, (200, 170))
screen.blit(scaled_image, (10, 20))

my_image = pygame.image.load("data/hero4.png").convert_alpha()
scaled_image = pygame.transform.scale(my_image, (120, 120))
screen.blit(scaled_image, (480, 400))

my_image = pygame.image.load("data/war.png").convert_alpha()
scaled_image = pygame.transform.scale(my_image, (80, 100))
screen.blit(scaled_image, (340, 6))

my_image = pygame.image.load("data/war1.png").convert_alpha()
scaled_image = pygame.transform.scale(my_image, (100, 110))
screen.blit(scaled_image, (500, 130))

my_image = pygame.image.load("data/war2.png").convert_alpha()
scaled_image = pygame.transform.scale(my_image, (130, 150))
screen.blit(scaled_image, (30, 370))

start = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((205, 180), (200, 150)),
    text='START',
    manager=manager)
ex = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((260, 400), (100, 60)),
    text='EXIT',
    manager=manager)
ret = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((30, 660), (70, 20)),
    text='return',
    manager=manager)


class Lab:
    def __init__(self, filename, free_t, finish_t):
        self.map = []
        with open(f"{maps_d}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.h = len(self.map)
        self.w = len(self.map[0])
        self.tile_size = tile_size
        self.free_t = free_t
        self.finish_t = finish_t

    def render(self, screen):
        colors = {0: (174, 96, 170), 1: (255, 0, 0), 2: (0, 0, 0), 3: (153, 153, 153)}
        for y in range(self.h):
            for x in range(self.w):
                if self.get_tile_id((x, y)) == 1:
                    a, b = tile_size, tile_size
                    pygame.draw.rect(screen, (123, 47, 139), (x * tile_size, y * tile_size, a, b))
                    for i in range(4, a + 2, 8):
                        for j in range(4, b + 2, 8):
                            pygame.draw.rect(screen, (14, 9, 15), (x * tile_size + a - i, y * tile_size + b - j, 4, 4))
                    for i in range(4, a + 2, 12):
                        for j in range(4, b + 2, 12):
                            pygame.draw.rect(screen, (201, 0, 190), (x * tile_size + a - i, y * tile_size + b - j, 4, 4))
                    for i in range(4, a + 2, 10):
                        for j in range(4, b + 2, 10):
                            pygame.draw.rect(screen, (153, 153, 153), (x * tile_size + a - i, y * tile_size + b - j, 4, 4))
                else:
                    rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    screen.fill(colors[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_t

    def find_step(self, start, target):
        INF = 1000
        x, y = start
        distance = [[INF] * self.w for i in range(self.h)]
        distance[y][x] = 0
        prev = [[None] * self.w for i in range(self.h)]
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx, dy in (1, 0), (0, 1), (-1, 0), (0, -1):
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.w and 0 < next_y < self.h and \
                        self.is_free((next_x, next_y)) and distance[next_y][next_x] == INF:
                    distance[next_y][next_x] = distance[y][x] + 1
                    prev[next_y][next_x] = (x, y)
                    queue.append((next_x, next_y))
        x, y = target
        if distance[y][x] == INF or start == target:
            return start
        while prev[y][x] != start:
            x, y = prev[y][x]
        return x, y


class Hero:
    def __init__(self, position, filename):
        self.x, self.y = position
        self.map = []
        with open(f"{maps_d}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.h = len(self.map)
        self.w = len(self.map[0])
        self.tile_size = tile_size

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        if self.map[self.x - 1][self.y - 1] == 1:
            my_image = pygame.image.load("data/hero4.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x + 1][self.y + 1] == 1:
            my_image = pygame.image.load("data/hero4.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x][self.y + 1] == 1:
            my_image = pygame.image.load("data/hero4.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x + 1][self.y] == 1:
            my_image = pygame.image.load("data/hero4.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)


class Hero_2:
    def __init__(self, position, filename):
        self.x, self.y = position
        self.map = []
        with open(f"{maps_d}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.h = len(self.map)
        self.w = len(self.map[0])
        self.tile_size = tile_size

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        if self.map[self.x - 1][self.y - 1] == 1:
            my_image = pygame.image.load("data/hero.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x + 1][self.y + 1] == 1:
            my_image = pygame.image.load("data/hero.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x][self.y + 1] == 1:
            my_image = pygame.image.load("data/hero.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x + 1][self.y] == 1:
            my_image = pygame.image.load("data/hero.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)


class War:
    def __init__(self, position, filename):
        self.x, self.y = position
        self.map = []
        with open(f"{maps_d}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.h = len(self.map)
        self.w = len(self.map[0])
        self.tile_size = tile_size
        self.delay = 100
        WAR_EVENT_TYPE = 30
        # pygame.time.set_timer(WAR_EVENT_TYPE, 100, 1)


    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        if self.map[self.x - 1][self.y - 1] == 1:
            my_image = pygame.image.load("data/war1.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x + 1][self.y + 1] == 1:
            my_image = pygame.image.load("data/war1.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x][self.y + 1] == 1:
            my_image = pygame.image.load("data/war1.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)
        elif self.map[self.x + 1][self.y] == 1:
            my_image = pygame.image.load("data/war1.png").convert_alpha()
            scaled_image = pygame.transform.scale(my_image, (tile_size, tile_size))
            screen.blit(scaled_image, (self.x * tile_size, self.y * tile_size))
            # center = self.x * tile_size + tile_size // 2, self.y * tile_size + tile_size // 2
            # ter = 5
            # pygame.draw.circle(screen, (200, 200, 200), center, ter)


class Game:
    def __init__(self, lab, hero, war):
        self.lab = lab
        self.hero = hero
        self.war = war

    def render(self, screen):
        self.lab.render(screen)
        self.hero.render(screen)
        self.war.render(screen)

    def update_hero(self):
        n_x, n_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            n_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            n_x += 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            n_y += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            n_y -= 1
        if self.lab.is_free((n_x, n_y)):
            self.hero.set_position((n_x, n_y))

    def move_war(self, z):
        if z % 7 == 0:
            next_position = self.lab.find_step(self.war.get_position(), self.hero.get_position())
            self.war.set_position(next_position)

    def check_win(self):
        return self.get_tile_id(self.hero.get_position()) == self.lab.finish_tile

    def check_lose(self):
        return self.hero.get_position() == self.war.get_position()


def show(screen, massage):
    font = pygame.font.Font(None, 50)
    text = font.render(massage, 1, (201, 0, 190))
    text_x = 810 // 2 - text.get_width() // 2
    text_y = 880 // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (153, 153, 153), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


class Game_2:
    def __init__(self, lab, hero, hero_2):
        self.lab = lab
        self.hero = hero
        self.hero_2 = hero_2

    def render(self, screen):
        self.lab.render(screen)
        self.hero.render(screen)
        self.hero_2.render(screen)

    def update_hero(self):
        n_x, n_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            n_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            n_x += 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            n_y += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            n_y -= 1
        if self.lab.is_free((n_x, n_y)):
            self.hero.set_position((n_x, n_y))

    def update_hero_2(self):
        n_x, n_y = self.hero_2.get_position()
        if pygame.key.get_pressed()[pygame.K_a]:
            n_x -= 1
        if pygame.key.get_pressed()[pygame.K_d]:
            n_x += 1
        if pygame.key.get_pressed()[pygame.K_s]:
            n_y += 1
        if pygame.key.get_pressed()[pygame.K_w]:
            n_y -= 1
        if self.lab.is_free((n_x, n_y)):
            self.hero_2.set_position((n_x, n_y))

    def check_win(self):
        return self.get_tile_id(self.hero.get_position()) == self.lab.finish_tile

    def check_lose(self):
        return self.hero.get_position() == self.war.get_position()


z = 1
d = 0
music = pygame.mixer.Sound("voice/re.wav")
music.play(0)
clock = pygame.time.Clock()
running = True
game_over = False
schet = 0
t = 0

while running:
    g = 1
    time_de = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_START_PRESS:
                if event.ui_element == ex:
                    running = False
                    continue
                if event.ui_element == start or event.ui_element == ret:
                    if schet != 1:
                        pygame.display.set_caption('THE BEST LAB')
                        size = width, height = 810, 880
                        screen1 = pygame.display.set_mode(size)

                        run = True
                        x_pos = 0
                        v = 20  # пикселей в секунду
                        clock = pygame.time.Clock()
                        my_image = pygame.image.load("data/hero4.png").convert_alpha()
                        j = 0
                        k = 10
                        t = 0
                        g = 0
                        p = 0
                        while run:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    run = False
                            screen1.fill((82, 0, 135))
                            if int(x_pos) <= 380:
                                screen1.blit(my_image, (int(x_pos), 100))
                                x_pos += v * clock.tick() / 50  # v * t в секундах
                            else:
                                screen1.blit(my_image, (380, 300))
                                j = 1
                            if j == 1:
                                pygame.draw.rect(screen1, (82, 0, 135), (0, 0, 810, 880))
                                if 380 - k > 150:
                                    scaled_image = pygame.transform.scale(my_image, (380 - k, 400 - k))
                                    k += 10
                                    screen1.blit(scaled_image, (380, 100 - t))
                                    t -= 10
                                else:
                                    screen1.blit(scaled_image, (380, 100 - t))
                                    g = 1
                            if g == 1:
                                print(k)
                                war_image = pygame.image.load("data/war.png").convert_alpha()
                                war_image = pygame.transform.scale(war_image, (220 - 70, 310 - 70))
                                war1_image = pygame.image.load("data/war1.png").convert_alpha()
                                war1_image = pygame.transform.scale(war1_image, (262 - 70, 310 - 70))
                                war2_image = pygame.image.load("data/war2.png").convert_alpha()
                                war2_image = pygame.transform.scale(war2_image, (232 - 70, 330 - 70))
                                war3_image = pygame.image.load("data/hero3.png").convert_alpha()
                                war3_image = pygame.transform.scale(war3_image, (262 - 70, 320 - 70))
                                screen1.blit(war_image, (90, 50))
                                screen1.blit(war1_image, (480, 60))
                                screen1.blit(war2_image, (110, 510))
                                screen1.blit(war3_image, (550, 500))
                                p = 1
                            if p == 1:
                                pygame.draw.rect(screen1, (82, 0, 135), (0, 0, 1910, 1070))
                                war_image = pygame.image.load("data/war.png").convert_alpha()
                                war_image = pygame.transform.scale(war_image, (220 - 70, 310 - 70))
                                war1_image = pygame.image.load("data/war1.png").convert_alpha()
                                war1_image = pygame.transform.scale(war1_image, (262 - 70, 310 - 70))
                                war2_image = pygame.image.load("data/war2.png").convert_alpha()
                                war2_image = pygame.transform.scale(war2_image, (232 - 70, 330 - 70))
                                war3_image = pygame.image.load("data/hero3.png").convert_alpha()
                                war3_image = pygame.transform.scale(war3_image, (262 - 70, 320 - 70))
                                screen1.blit(war_image, (90, 50))
                                screen1.blit(war1_image, (480, 60))
                                screen1.blit(war2_image, (110, 510))
                                screen1.blit(war3_image, (550, 500))
                                screen1.blit(scaled_image, (int(x_pos), 100 - t))
                                x_pos += v * clock.tick() / 50  # v * t в секундах

                            pygame.display.flip()
                            schet = 1

                    size = width, height = 650 + 200, 600
                    screen = pygame.display.set_mode(size)

                    background = pygame.Surface((650 + 200, 700))
                    background.fill(pygame.Color(color))
                    manager = pygame_gui.UIManager((650 + 200, 700))
                    switch = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((10 + 200, 10), (100, 50)),
                        text='1',
                        manager=manager)
                    switch1 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((110 + 200, 10), (100, 50)),
                        text='2',
                        manager=manager)
                    switch2 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((210 + 200, 10), (100, 50)),
                        text='3',
                        manager=manager)
                    switch3 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((310 + 200, 10), (100, 50)),
                        text='4',
                        manager=manager)
                    switch4 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((410 + 200, 10), (100, 50)),
                        text='5',
                        manager=manager)
                    switch5 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((510 + 200, 10), (100, 50)),
                        text='6',
                        manager=manager)
                    switch6 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((10 + 200, 100), (100, 50)),
                        text='7',
                        manager=manager)
                    switch7 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((110 + 200, 100), (100, 50)),
                        text='8',
                        manager=manager)
                    switch8 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((210 + 200, 100), (100, 50)),
                        text='9',
                        manager=manager)
                    switch9 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((310 + 200, 100), (100, 50)),
                        text='10',
                        manager=manager)
                    switch10 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((410 + 200, 100), (100, 50)),
                        text='11',
                        manager=manager)
                    switch11 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((510 + 200, 100), (100, 50)),
                        text='12',
                        manager=manager)
                    switch12 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((10 + 200, 200), (100, 50)),
                        text='13',
                        manager=manager)
                    switch13 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((110 + 200, 200), (100, 50)),
                        text='14',
                        manager=manager)
                    switch14 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((210 + 200, 200), (100, 50)),
                        text='15',
                        manager=manager)
                    switch15 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((310 + 200, 200), (100, 50)),
                        text='16',
                        manager=manager)
                    switch16 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((410 + 200, 200), (100, 50)),
                        text='17',
                        manager=manager)
                    switch17 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((510 + 200, 200), (100, 50)),
                        text='18',
                        manager=manager)
                    switch18 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((10 + 200, 300), (100, 50)),
                        text='1',
                        manager=manager)
                    switch19 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((110 + 200, 300), (100, 50)),
                        text='2',
                        manager=manager)
                    switch20 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((210 + 200, 300), (100, 50)),
                        text='3',
                        manager=manager)
                    switch21 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((310 + 200, 300), (100, 50)),
                        text='4',
                        manager=manager)
                    switch22 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((410 + 200, 300), (100, 50)),
                        text='5',
                        manager=manager)
                    switch23 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((510 + 200, 300), (100, 50)),
                        text='6',
                        manager=manager)
                    switch24 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((10 + 200, 400), (100, 50)),
                        text='7',
                        manager=manager)
                    switch25 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((110 + 200, 400), (100, 50)),
                        text='8',
                        manager=manager)
                    switch26 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((210 + 200, 400), (100, 50)),
                        text='9',
                        manager=manager)
                    switch27 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((310 + 200, 400), (100, 50)),
                        text='10',
                        manager=manager)
                    switch28 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((410 + 200, 400), (100, 50)),
                        text='11',
                        manager=manager)
                    switch29 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((510 + 200, 400), (100, 50)),
                        text='12',
                        manager=manager)
                    switch30 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((10 + 200, 500), (100, 50)),
                        text='13',
                        manager=manager)
                    switch31 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((110 + 200, 500), (100, 50)),
                        text='14',
                        manager=manager)
                    switch32 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((210 + 200, 500), (100, 50)),
                        text='15',
                        manager=manager)
                    switch33 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((310 + 200, 500), (100, 50)),
                        text='16',
                        manager=manager)
                    switch34 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((410 + 200, 500), (100, 50)),
                        text='17',
                        manager=manager)
                    switch35 = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((510 + 200, 500), (100, 50)),
                        text='18',
                        manager=manager)
                    ex = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect((300 + 100, 560), (70, 20)),
                        text='EXIT',
                        manager=manager)

                    pygame.display.update()
                    manager.process_events(event)
                    manager.update(time_de)
                    my_image = pygame.image.load("data/fon6.jpg").convert_alpha()
                    scaled_image = pygame.transform.scale(my_image, (650 + 200, 700))
                    screen.blit(scaled_image, (0, 0))

                    font = pygame.font.Font(None, 50)
                    text = font.render('1 PLAYER', 1, (255, 255, 255))
                    text_x = 200 // 2 - text.get_width() // 2
                    text_y = 200 // 2 - text.get_height() // 2
                    text_w = text.get_width()
                    text_h = text.get_height()
                    screen.blit(text, (text_x, text_y + 20))

                    font = pygame.font.Font(None, 50)
                    text = font.render('2 PLAYERS', 1, (255, 255, 255))
                    text_x = 200 // 2 - text.get_width() // 2
                    text_y = 200 // 2 - text.get_height() // 2
                    screen.blit(text, (text_x + 5, text_y + 320))

                    pygame.draw.line(screen, (58, 0, 211), (0, 280), (1000, 280), 4)

                    manager.draw_ui(screen)
                    pygame.display.update()
                    clock.tick(15)
                    d = 0
                    music.stop()
                    continue
                if event.ui_element == switch:
                    k = 'uo.txt'
                    position = (5, 5)
                    w_position = (15, 13)
                    fihish_id = (19, 9)
                    t = 0
                if event.ui_element == switch2:
                    k = 'map'
                    position = (2, 15)
                    w_position = (15, 12)
                    fihish_id = (6, 3)
                    t = 0
                if event.ui_element == switch4:
                    k = 'map1'
                    position = (18, 16)
                    w_position = (5, 5)
                    fihish_id = (4, 3)
                    t = 0
                if event.ui_element == switch3:
                    k = 'map2'
                    position = (14, 17)
                    w_position = (5, 5)
                    fihish_id = (17, 1)
                    t = 0
                if event.ui_element == switch1:
                    k = 'map3'
                    position = (2, 10)
                    w_position = (5, 5)
                    fihish_id = (12, 7)
                    t = 0
                if event.ui_element == switch17:
                    k = 'map4'
                    position = (1, 1)
                    w_position = (9, 4)
                    fihish_id = (13, 11)
                    t = 0
                if event.ui_element == switch5:
                    k = 'map5'
                    position = (18, 19)
                    w_position = (5, 5)
                    fihish_id = (1, 7)
                    t = 0
                if event.ui_element == switch6:
                    k = 'map6'
                    position = (19, 1)
                    w_position = (1, 19)
                    fihish_id = (9, 7)
                    t = 0
                if event.ui_element == switch7:
                    k = 'map7'
                    position = (1, 1)
                    w_position = (13, 18)
                    fihish_id = (19, 10)
                    t = 0
                if event.ui_element == switch8:
                    k = 'map8'
                    position = (1, 1)
                    w_position = (4, 4)
                    fihish_id = (13, 16)
                    t = 0
                if event.ui_element == switch9:
                    k = 'map9'
                    position = (5, 19)
                    w_position = (13, 12)
                    fihish_id = (18, 19)
                    t = 0
                if event.ui_element == switch10:
                    k = 'map10'
                    position = (6, 19)
                    w_position = (19, 3)
                    fihish_id = (13, 3)
                    t = 0
                if event.ui_element == switch11:
                    k = 'map11'
                    position = (2, 1)
                    w_position = (8, 10)
                    fihish_id = (16, 17)
                    t = 0
                if event.ui_element == switch12:
                    k = 'map12'
                    position = (3, 1)
                    w_position = (18, 1)
                    fihish_id = (17, 10)
                    t = 0
                if event.ui_element == switch13:
                    k = 'map13'
                    position = (19, 4)
                    w_position = (14, 7)
                    fihish_id = (17, 18)
                    t = 0
                if event.ui_element == switch14:
                    k = 'map14'
                    position = (1, 19)
                    w_position = (1, 1)
                    fihish_id = (19, 19)
                    t = 0
                if event.ui_element == switch15:
                    k = 'map15'
                    position = (17, 2)
                    w_position = (1, 3)
                    fihish_id = (18, 19)
                    t = 0
                if event.ui_element == switch16:
                    k = 'map16'
                    position = (3, 19)
                    w_position = (6, 15)
                    fihish_id = (9, 1)
                    t = 0
                if event.ui_element == switch18:
                    k = 'uo.txt'
                    position = (5, 5)
                    w_position = (5, 13)
                    fihish_id = (19, 9)
                    t = 1
                if event.ui_element == switch19:
                    k = 'map'
                    position = (2, 15)
                    w_position = (15, 12)
                    fihish_id = (6, 3)
                    t = 1
                if event.ui_element == switch20:
                    k = 'map1'
                    position = (18, 16)
                    w_position = (18, 13)
                    fihish_id = (4, 3)
                    t = 1
                if event.ui_element == switch21:
                    k = 'map2'
                    position = (5, 17)
                    w_position = (2, 12)
                    fihish_id = (17, 1)
                    t = 1
                if event.ui_element == switch22:
                    k = 'map3'
                    position = (2, 10)
                    w_position = (5, 13)
                    fihish_id = (12, 7)
                    t = 1
                if event.ui_element == switch23:
                    k = 'map4'
                    position = (1, 1)
                    w_position = (1, 1)
                    fihish_id = (13, 11)
                    t = 1
                if event.ui_element == switch24:
                    k = 'map5'
                    position = (18, 19)
                    w_position = (8, 19)
                    fihish_id = (1, 7)
                    t = 1
                if event.ui_element == switch25:
                    k = 'map6'
                    position = (19, 1)
                    w_position = (16, 2)
                    fihish_id = (9, 7)
                    t = 1
                if event.ui_element == switch26:
                    k = 'map7'
                    position = (1, 1)
                    w_position = (2, 10)
                    fihish_id = (19, 10)
                    t = 1
                if event.ui_element == switch27:
                    k = 'map8'
                    position = (1, 1)
                    w_position = (4, 4)
                    fihish_id = (13, 16)
                    t = 1
                if event.ui_element == switch28:
                    k = 'map9'
                    position = (5, 17)
                    w_position = (1, 1)
                    fihish_id = (18, 19)
                    t = 1
                if event.ui_element == switch29:
                    k = 'map10'
                    position = (6, 19)
                    w_position = (3, 7)
                    fihish_id = (13, 3)
                    t = 1
                if event.ui_element == switch30:
                    k = 'map11'
                    position = (2, 1)
                    w_position = (15, 6)
                    fihish_id = (16, 17)
                    t = 1
                if event.ui_element == switch31:
                    k = 'map12'
                    position = (2, 15)
                    w_position = (1, 13)
                    fihish_id = (17, 10)
                    t = 1
                if event.ui_element == switch32:
                    k = 'map13'
                    position = (19, 4)
                    w_position = (14, 7)
                    fihish_id = (17, 18)
                    t = 1
                if event.ui_element == switch33:
                    k = 'map14'
                    position = (1, 19)
                    w_position = (1, 1)
                    fihish_id = (19, 19)
                    t = 1
                if event.ui_element == switch34:
                    k = 'map15'
                    position = (17, 2)
                    w_position = (1, 3)
                    fihish_id = (18, 19)
                    t = 1
                if event.ui_element == switch35:
                    k = 'map16'
                    position = (3, 19)
                    w_position = (6, 15)
                    fihish_id = (9, 1)
                    t = 1
                size = width, height = 810, 880
                screen1 = pygame.display.set_mode(size)

                manager = pygame_gui.UIManager((810, 880))
                ret = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((30, 847), (70, 20)),
                    text='return',
                    manager=manager)
                j = 1
                d = 1
        manager.process_events(event)
    if j == 1 and d == 1:
        if t != 1:
            hero = Hero(position, k)
            war = War(w_position, k)
            lab = Lab(k, [0, 3], 3)
            game = Game(lab, hero, war)
            game.update_hero()
            position = hero.get_position()
            game.move_war(z)
            z += 1
            w_position = war.get_position()
            game.render(screen1)
            if position == fihish_id:
                music = pygame.mixer.Sound("voice/Win (online-audio-converter.com).wav")
                music.play(0)
                font = pygame.font.Font(None, 50)
                text = font.render('WON!:)', 1, (201, 0, 190))
                text_x = 810 // 2 - text.get_width() // 2
                text_y = 880 // 2 - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()
                pygame.draw.rect(screen, (153, 153, 153), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
                screen.blit(text, (text_x, text_y))
                d = 0
            if position == w_position:
                music = pygame.mixer.Sound("voice/Lost (online-audio-converter.com).wav")
                music.play(0)
                font = pygame.font.Font(None, 50)
                text = font.render('LOST!:( TRY AGAIN', 1, (201, 0, 190))
                text_x = 810 // 2 - text.get_width() // 2
                text_y = 880 // 2 - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()
                pygame.draw.rect(screen, (153, 153, 153), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
                screen.blit(text, (text_x, text_y))
                d = 0
        else:
            hero = Hero(position, k)
            hero_2 = Hero_2(w_position, k)
            lab = Lab(k, [0, 3], 3)
            game_2 = Game_2(lab, hero, hero_2)
            game_2.update_hero()
            position = hero.get_position()
            game_2.update_hero_2()
            z += 1
            w_position = hero_2.get_position()
            game_2.render(screen1)
            if position == fihish_id:
                if fihish_id == w_position:
                    music = pygame.mixer.Sound("voice/Win (online-audio-converter.com).wav")
                    music.play(0)
                    font = pygame.font.Font(None, 50)
                    text = font.render('BOTH WON!:)', 1, (201, 0, 190))
                    text_x = 810 // 2 - text.get_width() // 2
                    text_y = 880 // 2 - text.get_height() // 2
                    text_w = text.get_width()
                    text_h = text.get_height()
                    pygame.draw.rect(screen, (153, 153, 153), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
                    screen.blit(text, (text_x, text_y))
                    d = 0
                else:
                    music = pygame.mixer.Sound("voice/Win (online-audio-converter.com).wav")
                    music.play(0)
                    font = pygame.font.Font(None, 50)
                    text = font.render('1 WON!:)', 1, (201, 0, 190))
                    text_x = 810 // 2 - text.get_width() // 2
                    text_y = 880 // 2 - text.get_height() // 2
                    text_w = text.get_width()
                    text_h = text.get_height()
                    pygame.draw.rect(screen, (153, 153, 153), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
                    screen.blit(text, (text_x, text_y))
                    d = 0
            elif fihish_id == w_position:
                music = pygame.mixer.Sound("voice/Win (online-audio-converter.com).wav")
                music.play(0)
                font = pygame.font.Font(None, 50)
                text = font.render('2 WON!:)', 1, (201, 0, 190))
                text_x = 810 // 2 - text.get_width() // 2
                text_y = 880 // 2 - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()
                pygame.draw.rect(screen, (153, 153, 153), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
                screen.blit(text, (text_x, text_y))
                d = 0
    manager.update(time_de)
    manager.draw_ui(screen)
    pygame.display.update()
    clock.tick(15)
pygame.quit()