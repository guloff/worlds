import pygame
import random
import time

from colors import Colors

class Config():
    """Класс с системными настройками симуляции."""
    def __init__(self):
        self.clock = pygame.time.Clock()
        # Создание экземпляра класса Colors
        self.color = Colors()
        # Характеристики экрана:
        # Цвет экрана
        self.screen_color = self.color.LAVENDER
        # Ширина и высота/размер экрана
        self.screen_size = self.screen_width, self.screen_height = 1280, 720
        # Частота кадров
        self.FPS = 60

        # Характеристики Точек:
        # Радиус точки
        self.dot_radius = 6
        # Радиус обзора
        self.dot_scan_radius = 120
        # Начальный уровень энергии
        self.dot_energy = 500
        # Скорость
        self.dot_vel = random.randint(1,3)


        # Характеристики Травинок:
        # Цвет Травинки
        self.grass_color = self.color.WHITE
        # Радиус точки
        self.grass_radius = 2
        # Энергатическая ценность
        self.grass_energy = 120
