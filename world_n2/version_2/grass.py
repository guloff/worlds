import pygame
from pygame.sprite import Sprite
import random

from config import Config
from colors import Colors


# Класс Травинки
class Grass(Sprite):
    def __init__(self):
        # Класс Травки наследует от встроенного класса Sprite
        super().__init__()
        # Создается экземпляр класса Config, где хранятся все настройки и цветов Colors
        self.config = Config()
        self.color = Colors()
        # # Создаем спрайт Травки. Ширина и высота прямоугольника Точки равны диаметру Точки (два радиуса)
        self.image = pygame.Surface([self.config.grass_radius * 2, self.config.grass_radius * 2])
        self.image.fill(self.color.BLACK)
        # # Создаем поверхность для Точек
        self.image.set_colorkey(self.color.BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.config.grass_color, (self.rect.x + self.config.grass_radius, self.rect.y +self.config.grass_radius), self.config.grass_radius)
