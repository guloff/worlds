import sys
import pygame
import pygame.font
import random
import time
from config import Config
from thedot import Dot
from grass import Grass
from colors import Colors
import csv
import matplotlib.pyplot as plt

# Основной класс:
class DotWorld():
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

        # Поверхность для создания графика статистики
        self.statsurf = pygame.Surface((240, 240))

        self.font_legend = pygame.font.SysFont("Roboto", 24)
        self.screen_rect = self.statsurf.get_rect()

        # Поверхность для создания симуляции
        self.simsurf = pygame.Surface((1040, 720))

        self.font_tooltip = pygame.font.SysFont("Roboto", 12)

        pygame.mouse.set_visible(False)

        self.filename = "stat.csv"
        self.frame = 0
        self.data = [["Time", "Population", "Resources", "Slows", "Middles", "Fasts"]]

        # Группы по скорости
        self.slowDots = []
        self.middleDots = []
        self.fastDots = []


        self.time = []
        self.population = []
        self.resources = []
        self.slows = []
        self.middles = []
        self.fasts = []

# Функция запуска мира:
    def run_world(self):
        # Основной цикл
        while True:
            self._check_event()
            # Запуск счетчика + скорость
            for dot in self.dotsList:
                self.step += dot.vel

                if dot.energy >= 1000:
                    newDot = Dot(500)
                    dot.energyDecr(500)
                    self.dotsList.append(newDot)
                    if newDot.dotColor == self.colors.BLUE:
                        self.slowDots.append(newDot)
                    elif newDot.dotColor == self.colors.FUCHSIA:
                        self.middleDots.append(newDot)
                    elif newDot.dotColor == self.colors.DARKKHAKI:
                        self.fastDots.append(newDot)

            # Прорисовка поверхности симуляции
            self.screen.blit(self.simsurf, (240, 0))
            # Заполнение фона
            self.simsurf.fill(self.colors.DARKSLATEGREY)
            # Прорисовка трав
            for grassCoord in self.grassesCoords:
                pygame.draw.circle(self.simsurf, self.colors.LAVENDER, (grassCoord[0], grassCoord[1]), self.grass.grassRad)
            # Прорисовка Точки
            for dot in self.dotsList:
                pygame.draw.circle(self.simsurf, dot.dotColor, (dot.dotX, dot.dotY), dot.dotRad)
                self.showTooltip(str(dot.energy), dot.dotX - 2 * dot.dotRad, dot.dotY + 2 * dot.dotRad)

            # Определение новой целевой координаты Точки (куда она должна идти)
            # Сканирование вокруг Точки, определение целевой координаты
            for dot in self.dotsList:
                target = dot.scanner(self.grassesCoords, self.width, self.height)
                # Изменение координат Точки в сторону целевой (движение)
                dot.moveTo(target)
                # Декремент_энергии
                dot.energyDecr(1)
                # Инкремент энергии, если трава съедена
                dot.eatGrass(target, self.grassesCoords, self.grass.energyIncr)

                # pygame.draw.line(self.screen, self.config.PapayaWhip, (dot.dotX, dot.dotY), target, 3)

            # Восполнение запасов травы
            # Если количество травы меньше минимально установленной
            grassesNum = len(self.grassesCoords)
            if grassesNum < self.grass.minQuantity:
                # Добавить координаты еще одной травы в список координат трав
                # (self.grass.minQuantity - grassesNum)
                self.grass.addGrass(self.width, self.height)

            # Если энергия Точки на нуле, удалить ее и вместо нее добавить 3 травинки
            for dot in self.dotsList:
                if dot.energy <= 0:
                    # self.dotsList.remove(dot)
                    # self.grass.addGrass(self.width, self.height, 3)
                    self.dotsList.remove(dot)
                    if dot.dotColor == self.colors.BLUE:
                        try:
                            self.slowDots.remove(dot)
                            self.grass.addGrass(self.width, self.height, 30)
                        except ValueError:
                            continue
                    elif dot.dotColor == self.colors.FUCHSIA:
                        try:
                            self.middleDots.remove(dot)
                            # self.dotsList.remove(dot)
                            self.grass.addGrass(self.width, self.height, 25)
                        except ValueError:
                            continue
                    elif dot.dotColor == self.colors.DARKKHAKI:
                        try:
                            self.fastDots.remove(dot)
                            # self.dotsList.remove(dot)
                            self.grass.addGrass(self.width, self.height, 10)
                        except ValueError:
                            continue

            # Статистика
            slows = len(self.slowDots)
            middles = len(self.middleDots)
            fasts = len(self.fastDots)

            # Прорисовка статистики
            self.statsurf.fill(self.colors.WHITE)
            self.statsurf.set_alpha(200)

            # Сохранение данных в файле
            dotsNum = len(self.dotsList)
            if self.frame % self.config.FPS == 0:
                data = [f'sec_{int(self.frame // self.config.FPS)}', dotsNum, grassesNum, slows, middles, fasts]
                # data = [f'sec_{int(self.frame // 10)}', dotsNum, grassesNum, slows, middles, fasts]
                self.data.append(data)


            # Вывод Легенды
            self.showLegend("Resources", grassesNum, 10)
            self.showLegend("Population", dotsNum, 30)
            self.showLegend("Slow Dots", slows, 50)
            self.showLegend("Middle Dots", middles, 70)
            self.showLegend("Fast Dots", fasts, 90)
            self.screen.blit(self.statsurf, (0, 0))

            # Если численность на нуле, выйти из симуляции
            if dotsNum == 0:
                self.writeStat(self.filename, self.data)
                self.save_plot(self.data)
                sys.exit()
            pygame.display.flip()
            self.config.clock.tick(self.config.FPS)
            self.frame += 1
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
                    self.filename = f"stat_data/stat_{int(time.time())}.csv"
                    self.writeStat(self.filename, self.data)
                    self.save_plot(self.data)
                    # Выйти из программы
                    sys.exit()

    def showLegend(self, caption, num, vIndent):
        """Показ легенды"""
        legend_str = f" {caption}: {num} "
        legend_image = self.font_legend.render(legend_str, True, self.colors.BLACK)
        legend_rect = legend_image.get_rect()
        legend_rect.left = self.screen_rect.left + 5
        legend_rect.top = vIndent
        # Рендер текстов, показателей, вывод на экран легенды
        self.statsurf.blit(legend_image, legend_rect)

    def showTooltip(self, text, xAxis, yAxis):
        """Показ легенды"""
        tooltip_image = self.font_tooltip.render(text, True, self.colors.BLACK)
        tooltip_rect = tooltip_image.get_rect()
        tooltip_rect.left = xAxis
        tooltip_rect.top = yAxis
        # Рендер текстов, показателей, вывод на экран легенды
        self.simsurf.blit(tooltip_image, tooltip_rect)

    def writeStat(self, filename, data):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow(row)

    def save_plot(self, data):
        for row in data:
            self.time.append(row[0])
            self.population.append(row[1])
            self.resources.append(row[2])
            self.slows.append(row[3])
            self.middles.append(row[4])
            self.fasts.append(row[5])
# pyplot styles
# ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']
        plt.style.use("ggplot")
        fig, ax = plt.subplots()
        ax.plot(self.population[1:])
        ax.plot(self.resources[1:])
        ax.plot(self.slows[1:])
        ax.plot(self.middles[1:])
        ax.plot(self.fasts[1:])
        ax.legend(("Population", "Resources", "Slows", "Middles", "Fasts"))

        # ax.axis([0, int(self.x_values[-1][4:]), 0, 1000])
        plt.savefig(f"stat_fig/stat_fig_{int(time.time())}.png", bbox_inches = "tight")
        # plt.show()
        return True

if __name__ == "__main__":
    dw = DotWorld(1280, 720, "The World of Dots.")
    # time.sleep(5)
    dw.run_world()
