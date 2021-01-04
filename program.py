import pygame
import os
import sys

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption('HARVESTING')

all_sprites = pygame.sprite.Group()


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

running = True
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
    pygame.display.flip()
terminate()
