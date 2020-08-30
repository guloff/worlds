import random
from config import Config
from colors import Colors

class Dot():
    """Класс Точки."""
    # Инициализация основных параметров
    def __init__(self, energy = 500, scanRad = 100):
        self.clr = Colors()
        # Уровень энергии
        self.energy = energy
        # Радиус Точки
        self.dotRad = 6
        # Радиус сканирования
        self.scanRad = scanRad
        # Состояние сканера (включено)
        self.scanStatusOn = True

        # Начальные координаты
        self.dotX = random.randint(0, 720)
        self.dotY = random.randint(0, 720)
        # Скорость
        self.vel = random.randint(1, 3)
        # Цвет Точки
        # self.dotColor = self.clr.allColorsCodesList[random.randrange(len(self.clr.allColorsCodesList))]
        if self.vel == 1:
            self.dotColor = self.clr.BLUE
        elif self.vel == 2:
            self.dotColor = self.clr.FUCHSIA
        elif self.vel == 3:
            self.dotColor = self.clr.DARKKHAKI

    def moveTo(self, target):
        """Движение в сторону целевой координаты."""
        # Изменение координат Точки в сторону введенных координат
        if self.dotX > target[0]:
            self.dotX -= self.vel
            self.energy -= 1 * self.vel
        elif self.dotX < target[0]:
            self.dotX += self.vel
            self.energy -= 1 * self.vel
        if self.dotY > target[1]:
            self.dotY -= self.vel
            self.energy -= 1 * self.vel
        elif self.dotY < target[1]:
            self.dotY += self.vel
            self.energy -= 1 * self.vel

        # Возвращает текущие координаты точки, где её следует нарисовать (шаг в сторону целевой координаты)
        newCoord = (self.dotX, self.dotY)
        return newCoord

    def scanner(self, grassesCoords, width, height):
        # """Для быстроты поиска можно сначала создать список только тех травинок, чьи координаты X и Y меньше или больше координат Точки на величину радиуса сканирования в данный момент. Потом уже после этого просканировать, какие из этих точек входят в площадь круга, чей радиус равен радиусу/дальности сканера Точки."""
        # Просканировать окружающий мир в определенном радиусе
        # Территория сканирования
        # Левый верхний угол квадрата сканирования
        x1 = self.dotX - self.scanRad
        y1 = self.dotY - self.scanRad
        # Правый нижний угол квадрата сканирования
        x2 = self.dotX + self.scanRad
        y2 = self.dotY + self.scanRad
        # Список координат ближайших точек
        closestGrasses = []
        for grass_index in range(len(grassesCoords)):
            if (x1 < grassesCoords[grass_index][0] < x2) and (y1 < grassesCoords[grass_index][1] < y2):
                closestGrasses.append(grassesCoords[grass_index])
        # Список расстояний
        distances = []
        # print(closestGrasses)
        # Если в просканированной площади есть травки:
        if len(closestGrasses) > 0:
            # Если травка одна, то ее координаты указать в качестве целевой
            if len(closestGrasses) == 1:
                target = closestGrasses[0]
            # Иначе составить список расстояний от Точки до травок
            else:
                for grass in closestGrasses:
                    distance = round(((self.dotX - grass[0]) ** 2 + (self.dotY - grass[1]) ** 2) ** 0.5)
                    distances.append(distance)
                # Найти ближайшую травку
                closestGrass = min(distances)
                closestGrassIndex = distances.index(closestGrass)
                # Определить координаты ближайшей тарвки
                closestGrassCoord = closestGrasses[closestGrassIndex]
                # Задать координаты ближайшей точки в качестве целевых координат
                target = (closestGrassCoord[0], closestGrassCoord[1])
        # Иначе (если точек нет)
        else:
            # Задать случайную координату в качестве целевой
            target = (random.randrange(self.dotRad, width - self.dotRad), random.randrange(self.dotRad, height - self.dotRad))
        # Возвращает координаты целевой точки
        return target

    def energyDecr(self, num):
        """Декремент энергии"""
        # На каждом шаге уменьшает энергию на заданную величину декремента
        self.energy -= num
        # Возвращает текущий уровень энергии (после декремента)
        return self.energy

    def eatGrass(self, target, grassesCoords, energyIncr):
        """Съесть траву. Инкремент_энергии"""
        # Если целевая координата есть в списке координат трав и целевая координата находится внутри Точки:
        if target in grassesCoords and ((self.dotX - target[0]) ** 2 + (self.dotY - target[1]) ** 2) < self.dotRad ** 2:
            # Удалить координаты из списка координат
            grassesCoords.remove(target)
            # Увеличить энергию Точки
            self.energy += energyIncr

# if __name__ == "__main__":
#     dot = Dot()
#     print(dot.dotColor)
