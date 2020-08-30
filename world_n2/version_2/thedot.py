# Класс создания Точки

import pygame
import random
from pygame.sprite import Sprite

from config import Config
from colors import Colors



class Dot(Sprite):
    """Класс создания Точки."""
    def __init__(self):
        # Класс точки наследует от встроенного класса Sprite
        super().__init__()
        # self.name = name
        # Создается экземпляр класса Config, где хранятся все настройки и цветов Colors
        self.config = Config()
        self.color = Colors()
        # Цвет Точки
        if self.config.dot_vel == 1:
            self.dot_color = self.color.BLUE
        elif self.config.dot_vel == 2:
            self.dot_color = self.color.FUCHSIA
        elif self.config.dot_vel == 3:
            self.dot_color = self.color.DARKKHAKI
        # Создаем спрайт Точки. Ширина и высота прямоугольника Точки равны диаметру Точки (два радиуса)
        self.image = pygame.Surface([self.config.dot_radius * 2, self.config.dot_radius * 2])
        self.image.fill(self.color.WHITE)
        # Создаем поверхность для Точек
        self.image.set_colorkey(self.color.WHITE)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.dot_color, (self.rect.x + self.config.dot_radius, self.rect.y + self.config.dot_radius), self.config.dot_radius)

    # Создание методов
    # Метод Update()
    def update(self, target):
        """Движение в сторону целевой координаты."""
        # Изменение координат Точки в сторону введенных координат
        if self.rect.x > target[0]:
            self.rect.x -= self.config.dot_vel
            self.config.dot_energy -= self.config.dot_vel
        elif self.rect.x < target[0]:
            self.rect.x += self.config.dot_vel
            self.config.dot_energy -= self.config.dot_vel
        if self.rect.y > target[1]:
            self.rect.y -= self.config.dot_vel
            self.config.dot_energy -= self.config.dot_vel
        elif self.rect.y < target[1]:
            self.rect.y += self.config.dot_vel
            self.config.dot_energy -= self.config.dot_vel
