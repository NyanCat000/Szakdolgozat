import os
import pygame

def image(path):
    img = pygame.image.load("assets/images/" + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def images(path):
    imgs = []
    for img in sorted(os.listdir("assets/images/" + path)):
        imgs.append(image(path + "/" + img))
    return imgs

class Animation:
    def __init__(self, images, duration):
        self.images = images
        self.duration = duration
        self.tick = 0
        self.index = 0
    
    def copy(self):
        return Animation(self.images, self.duration)

    def update(self):
        self.tick += 1
        if self.tick >= self.duration * len(self.images):
            self.tick = 0
    
    def current_image(self):
        self.index = int(self.tick / self.duration)
        return self.images[self.index]