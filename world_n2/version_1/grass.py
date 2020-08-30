import random

class Grass():
    def __init__(self):
        # Радиус травки
        self.grassRad = 2
        # Начальное общее число
        self.startQuantity = 1000
        # Минимальное число
        self.minQuantity = 500
        # Список координат
        self.grasses_coords = []
        # Энергетическая ценность съеденной травки
        self.energyIncr = 100 #random.randrange(20, 50)

    def addGrass(self, width, height, num = 1):
        """Добавляет координаты новой травки в список координат трав."""
        # Если число меньше или равно 1:
        if num == 1:
            # Определить случайные координаты для 1 точки
            grass_coord = (random.randrange(width - 240), random.randrange(height))
            # Добавить в список координат
            self.grasses_coords.append(grass_coord)
        # Иначе (или больше 1)
        else:
            # Цикл от 1 до числа (и на каждом шаге):
            for i in range(num):
                # Определить случайные координаты для 1 точки
                grass_coord = (random.randrange(width - 240), random.randrange(height))
                # Добавить в список координат
                self.grasses_coords.append(grass_coord)
        # Возвращает список координат трав
        return self.grasses_coords

    def removeGrass(self, coordinates):
        """Удаление_травки(координаты):"""
        # Если указанные координаты есть в списке:
        if coordinates in self.grasses_coords:
            # Удалить координаты из списка
            self.grasses_coords.remove(coordinates)
        # Иначе (если их нет в списке):
        else:
            # Вывести на экран ("Травки с координатами {координаты} не существует.")
            print(f"Травки с координатами {coordinates} не существует.")
            # И пропустить эту итерацию
            pass
