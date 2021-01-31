import pygame
import os
import sys
import random

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('HARVESTING')

all_sprites = pygame.sprite.Group()

A = [25, 125, 225, 325, 425, 525, 625]  # координаты х для фруктов
x_colors = [pygame.Color('grey'), pygame.Color('grey'), pygame.Color('grey')]  # цвета крестиков в углу экрана
tm = pygame.time.Clock()
time = 200
score = 0  # счет
omissions = 0  # промахи


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# функция для обновления счета
def print_score():
    font = pygame.font.Font(None, 25)
    text = font.render(f'''Счёт: {str(score)}''', True, (0, 255, 0))
    text_x, text_y = 5, 5
    screen.blit(text, (text_x, text_y))
    draw_x()


# фунция для отрисовки крестиков в углу экрана
def draw_x():
    pygame.draw.line(screen, x_colors[0], (5, 25), (30, 50), width=8)
    pygame.draw.line(screen, x_colors[0], (5, 50), (30, 25), width=8)

    pygame.draw.line(screen, x_colors[1], (35, 25), (60, 50), width=8)
    pygame.draw.line(screen, x_colors[1], (35, 50), (60, 25), width=8)

    pygame.draw.line(screen, x_colors[2], (65, 25), (90, 50), width=8)
    pygame.draw.line(screen, x_colors[2], (65, 50), (90, 25), width=8)


# начальный экран, заставка
def start_screen():
    intro_text = ["Правила игры", 'Передвигая корзинку при помощи клавиш -> и <-,',
                  'постарайтесь собрать как можно больше фруктов', '', 'Чтобы поставить игру на паузу, нажмите 1',
                  'Чтобы снять игру с паузы, нажмите 1 повторно', '', 'Для начала игры нажмите Enter']
    fon2 = pygame.transform.scale(load_image('fon2.png'), (width, height))
    screen.blit(fon2, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            elif e.type == pygame.KEYDOWN:
                if e.key == 13:
                    return
        pygame.display.flip()


# финальный экран
def finish_screen():
    global score, omissions, x_colors
    intro_text = [f'Ваш результат - {score}',
                  'Нажмите "Enter", чтобы начать новую игру.']
    fon2 = pygame.transform.scale(load_image('fon2.png'), (width, height))
    screen.blit(fon2, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            if e.type == pygame.KEYDOWN:
                if e.key == 13:
                    score = 0
                    omissions = 0
                    x_colors = [pygame.Color('grey'), pygame.Color('grey'), pygame.Color('grey')]
                    draw_x()
                    return
        pygame.display.flip()


# класс корзины
class Basket(pygame.sprite.Sprite):
    image = load_image("box.png", colorkey=-1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Basket.image
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height

    def update(self):
        global f
        if f == 'left' and self.rect.x > 0:
            self.rect = self.rect.move(-100, 0)
        elif f == 'right' and self.rect.x < 600:
            self.rect = self.rect.move(100, 0)


basket = Basket()


# класс фруктов
class Fruit(pygame.sprite.Sprite):
    image1 = load_image('apple.png')
    image2 = load_image('pear.png')
    image3 = load_image('apricot.png')
    image4 = load_image('cherry.png')
    image5 = load_image('orange.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.images = [Fruit.image1, Fruit.image2, Fruit.image3, Fruit.image4, Fruit.image5]
        self.image = random.choice(self.images)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        global score, omissions, time
        if not pygame.sprite.collide_mask(self, basket) and self.rect.colliderect(screen.get_rect()):
            self.rect = self.rect.move(0, 1)
        elif pygame.sprite.collide_mask(self, basket):
            score += 1
            self.kill()
            Fruit((random.choice(A), 0))
            if time < 400:
                time += 3
        else:
            if omissions < 3:
                x_colors[omissions] = pygame.Color('red')
                omissions += 1
            else:
                finish_screen()
            self.kill()
            Fruit((random.choice(A), 0))


start_screen()
fon = pygame.transform.scale(load_image('fon.png'), (width, height))
running = True
pause = False  # для паузы
Fruit((random.choice(A), 0))
while running:
    screen.blit(fon, (0, 0))
    f = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                f = 'left'
            elif event.key == pygame.K_RIGHT:
                f = 'right'
            elif event.key == 1073741913:
                pause = not pause
        else:
            f = None
    if not pause:
        all_sprites.update()
        all_sprites.draw(screen)
        print_score()
        tm.tick(time)
        pygame.display.flip()
terminate()
