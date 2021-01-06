import pygame
import os
import sys
import random

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('HARVESTING')

all_sprites = pygame.sprite.Group()

A = [25, 125, 225, 325, 425, 525, 625]
tm = pygame.time.Clock()
time = 200
score = 0
omissions = 0


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


class Fruit(pygame.sprite.Sprite):
    image1 = load_image('apple.png')
    image2 = load_image('pear.png')
    image3 = load_image('apricot.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.images = [(Fruit.image1, (45, 60)), (Fruit.image2, (45, 65)), (Fruit.image3, (50, 48))]
        im = random.choice(self.images)
        self.image = im[0]
        self.image = pygame.transform.scale(self.image, im[1])

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
                time += 2
        else:
            omissions += 1
            self.kill()
            Fruit((random.choice(A), 0))


running = True
Fruit((random.choice(A), 0))
while running:
    screen.fill((0, 0, 0))
    f = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                f = 'left'
            elif event.key == pygame.K_RIGHT:
                f = 'right'
        else:
            f = None
    all_sprites.update()
    all_sprites.draw(screen)
    tm.tick(time)
    pygame.display.flip()
terminate()
