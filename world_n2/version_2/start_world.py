import sys
import pygame
import pygame.font
import random
import time

from config import Config
from colors import Colors
from thedot import Dot
from grass import Grass

# Основной класс симуляции
class DotWorld():
    """Главный класс симуляции."""
    def __init__(self, caption):
        """Инициализация основных параметров."""
        self.caption = caption
        self.config = Config()
        self.color = Colors()
        # Заголовок экрана
        pygame.display.set_caption(self.caption)
        # Экран с заданным размером
        self.screen = pygame.display.set_mode(self.config.screen_size)
        # Создается группа Точек/список спрайтов
        self.dot_list = pygame.sprite.Group()
        # Создается группа Травинок/список спрайтов
        self.grass_list = pygame.sprite.Group()
        # Создается группа всех спрайтов
        self.all_sprites_list = pygame.sprite.Group()

        for i in range(10):
            # Создание Точки
            self.dot = Dot()
            # Выбор случайных координат размещения Точки
            self.dot.rect.x = random.randrange(self.config.screen_width)
            self.dot.rect.y = random.randrange(self.config.screen_height)
            # Добавить точки в список точек
            self.dot_list.add(self.dot)
            self.all_sprites_list.add(self.dot)

        for i in range(100):
            # Создание травинки
            self.grass = Grass()
            # Выбор случайных координат размещения травинки
            self.grass.rect.x = random.randrange(self.config.screen_width)
            self.grass.rect.y = random.randrange(self.config.screen_height)
            # Добавить травинку в список травинок
            self.grass_list.add(self.grass)
            self.all_sprites_list.add(self.grass)


    # Метод запуска симуляции
    def run_world(self):
        # Основной цикл
        while True:
            # Проверка возникновения событий
            self._check_event()
            # Прорисовка поверхности симуляции
            self.screen.fill(self.color.DARKSLATEGREY)
            # for grass in self.grass_list:
            #     # print((grass.rect.x, grass.rect.y))
            #     pygame.draw.circle(self.screen, self.config.grass_color, (grass.rect.x, grass.rect.y), self.config.grass_radius)

            self.all_sprites_list.draw(self.screen)

            for dot in self.dot_list:
                hit_list = pygame.sprite.spritecollide(dot, self.grass_list, True)
                dot.config.dot_energy += self.config.grass_energy * len(hit_list)
                print(dot.config.dot_energy)
                for grass in self.grass_list:
                    if (dot.rect.x - dot.config.dot_scan_radius < grass.rect.x < dot.rect.x + dot.config.dot_scan_radius) and (dot.rect.y - dot.config.dot_scan_radius < grass.rect.y < dot.rect.y + dot.config.dot_scan_radius):
                        target = [grass.rect.x, grass.rect.y]
                    else:
                        target = [random.randint(0, self.config.screen_width), random.randint(0, self.config.screen_height)]

                dot.update(target)
                dot_hits = pygame.sprite.spritecollide(dot, self.dot_list, False)
                if len(dot_hits) > 0:
                    dot.rect.x * -1
                    dot.rect.y * -1

            # self.dot_list.update(target)


            self.config.clock.tick(self.config.FPS)
            pygame.display.flip()
        pygame.quit()


# Инициализация необходимых методов:
    def _check_event(self):
        """Проверка событий"""
        for event in pygame.event.get():
            # Если закрыто окно Pygame:
            if event.type == pygame.QUIT:
                # Выйти из программы
                sys.exit()


if __name__ == "__main__":
    dw = DotWorld("The World of Dots.")
    dw.run_world()
