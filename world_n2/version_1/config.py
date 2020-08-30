import pygame
import time

class Config():
    """Настройки мира."""
    def __init__(self):
        # Настройка частоты кадров
        self.clock = pygame.time.Clock()
        self.FPS = 60
        # Цвета
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.DARKMINT = (33, 188, 112)
        self.KHAKI = (240, 230, 140)
        self.STEELBLUE = (70, 130, 180)
        self.PapayaWhip = (255, 239, 213)
        # Расширенная версия в файле colors.py
