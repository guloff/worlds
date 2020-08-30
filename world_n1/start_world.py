import sys
import pygame
import pygame.font
import random
import time
from config import Config
from thedot import Dot
from grass import Grass
from colors import Colors

# Основной класс:
class DotWorld():
    """Мир состоит только из одного существа, которое ходит и ищет пищу в пределах видимости."""
    # Инициализация основных параметров
    def __init__(self, width, height, caption):
        pygame.init()
        # Размеры окна и заголовок
        self.width = width
        self.height = height
        self.size = (self.width, self.height)
        self.caption = caption
        pygame.display.set_caption(self.caption)
        # Экран с заданным размеров
        self.screen = pygame.display.set_mode(self.size)
        # Полноэкранный режим
        # self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        # Инициализация настроек
        self.config = Config()
        # Инициализация набора цветов
        self.colors = Colors()
        # Инициализация счетчика шагов
        self.step = 0
        # Инициализация списков объектов (Точки и трав)
        self.dotsList = []
        # Инициализация первой точки и добавление в список Точек
        self.firstDot = Dot()
        self.dotsList.append(self.firstDot)
        # Список координат трав
        self.grass = Grass()
        self.grassesCoords = self.grass.addGrass(self.width, self.height, self.grass.startQuantity)

        self.font = pygame.font.SysFont(None, 16)
        self.screen_rect = self.screen.get_rect()

        pygame.mouse.set_visible(False)

# Функция запуска мира:
    def run_world(self):
        # Основной цикл
        while True:
            self._check_event()
            # Запуск счетчика + скорость
            self.step += self.firstDot.vel
            # Заполнение фона
            self.screen.fill(self.colors.DARKSLATEGREY)
            # Прорисовка трав
            for grassCoord in self.grassesCoords:
                pygame.draw.circle(self.screen, self.colors.LAVENDER, (grassCoord[0], grassCoord[1]), self.grass.grassRad)
            # Прорисовка Точки
            pygame.draw.circle(self.screen, self.config.STEELBLUE, (self.firstDot.dotX, self.firstDot.dotY), self.firstDot.dotRad)
            # Прорисовка окружности - границ сканера
            pygame.draw.circle(self.screen, self.config.PapayaWhip, (self.firstDot.dotX, self.firstDot.dotY), self.firstDot.scanRad, 1)


            # Определение новой целевой координаты Точки (куда она должна идти)
            # Сканирование вокруг Точки, определение целевой координаты
            target = self.firstDot.scanner(self.grassesCoords, self.width, self.height)
            # Изменение координат Точки в сторону целевой (движение)
            self.firstDot.moveTo(target)
            # Декремент_энергии
            self.firstDot.energyDecr(1)
            # Инкремент энергии, если трава съедена
            self.firstDot.eatGrass(target, self.grassesCoords, self.grass.energyIncr)

            pygame.draw.line(self.screen, self.config.PapayaWhip, (self.firstDot.dotX, self.firstDot.dotY), target, 3)
            # Восполнение запасов травы
            # Если количество травы меньше минимально установленной
            if len(self.grassesCoords) < self.grass.minQuantity:
                # Добавить координаты еще одной травы в список координат трав
                self.grass.addGrass(self.width, self.height)

            # Если энергия Точки на нуле, выйти из симуляции
            if self.firstDot.energy <= 0:
                sys.exit()

            # Вывод Легенды
            self.showLegend(" Energy", self.firstDot.energy, 5)
            self.showLegend(" En. of 1 dot", self.grass.energyIncr, 20)
            self.showLegend(" Target", target, 35)
            self.showLegend(" Current Coord.", (self.firstDot.dotX, self.firstDot.dotY), 50)

            pygame.display.flip()
            self.config.clock.tick(self.config.FPS)
        pygame.quit()

# Инициализация необходимых методов:
    def _check_event(self):
        """Проверка событий"""
        for event in pygame.event.get():
            # Если закрыто окно Pygame:
            if event.type == pygame.QUIT:
                # Выйти из программы
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Если нажата кнопка q:
                if event.key == pygame.K_q:
                    # Выйти из программы
                    sys.exit()

    def showLegend(self, caption, num, vIndent):
        """Показ легенды"""
        legend_str = f" {caption}: {num} "
        legend_image = self.font.render(legend_str, True, self.colors.GRAY)
        legend_rect = legend_image.get_rect()
        legend_rect.left = self.screen_rect.left + 5
        legend_rect.top = vIndent
        # Рендер текстов, показателей, вывод на экран легенды
        self.screen.blit(legend_image, legend_rect)

if __name__ == "__main__":
    dw = DotWorld(1280, 720, "The World of Lonely Dot.")
    # time.sleep(2)
    dw.run_world()
