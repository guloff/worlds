import random
from config import Config

class Dot():
    """Класс Точки."""
    # Инициализация основных параметров
    def __init__(self):
        # Уровень энергии
        self.energy = 1000
        # Радиус Точки
        self.dotRad = 6
        # Радиус сканирования
        self.scanRad = 150
        # Состояние сканера (включено)
        self.scanStatusOn = True

        # Начальные координаты
        self.dotX = random.randint(200, 500)
        self.dotY = random.randint(200, 500)
        # Скорость
        self.vel = 1


    def moveTo(self, target):
        """Движение в сторону целевой координаты."""
        # Изменение координат Точки в сторону введенных координат
        if self.dotX > target[0]:
            self.dotX -= self.vel
            self.energy -= 1
        elif self.dotX < target[0]:
            self.dotX += self.vel
            self.energy -= 1
        if self.dotY > target[1]:
            self.dotY -= self.vel
            self.energy -= 1
        elif self.dotY < target[1]:
            self.dotY += self.vel
            self.energy -= 1

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

        # Иначе (если точки нет в списке координат трав):
        # else:
            # # Вывести на экран ("Точки нет, видимо, ее съели до меня.")
            # print(f"Точки {target} нет, видимо, ее съели до меня.")
            # Включить сканирование
            # self.scanStatusOn = True
