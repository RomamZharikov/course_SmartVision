import random
from PIL import Image, ImageDraw
import numpy as np
import json
from Determination_of_the_angular_resolution_of_the_PAR import Determination_of_the_angular_resolution_of_the_PAR as \
    dX_find


class Test_radar_Image_formation:
    def __init__(self, variant=7):
        self.variant = variant
        load = self.load_data_from_file()
        self.__N = 16 + load["Variant"]
        self.__dX = load["dX"]
        self.__Npoint = load["Npoint"]
        self.__D = np.array(load["D"])
        self.__figures = ["points", "square", "several"]

    def figures(self, figures="points"):
        """
        Частина коду, де виконується моделювання початкового об'єкта, такого як дві точки (points), квадрат (square) або
        декількох об'єктів (several). Для перших двух елементів створили код для випадковості розташування та (для
        квадрата) випадкового розміру. Декілька об'єктів будуємо за допомогою бібліотеки PIL
        :param figures:
        :return:
        """
        M1 = np.full((self.__Npoint, self.__Npoint), 0)
        if figures == "points":
            row = random.choice(range(int(self.__Npoint * 0.1), int(self.__Npoint * 0.9)))
            column = random.choice(range(int(self.__Npoint * 0.1), int(self.__Npoint * 0.9)))
            M1[row, column] = 255
            M1[row, column + self.__dX] = 255
        elif figures == "square":
            while True:
                size = random.randint(int(self.__Npoint * 0.1), int(self.__Npoint * 0.5))
                row = random.randint(0, self.__Npoint - size)
                column = random.randint(0, self.__Npoint - size)
                if (0.1 * self.__Npoint <= row <= 0.9 * self.__Npoint) and (
                        0.1 * self.__Npoint <= column <= 0.9 * self.__Npoint):
                    break
            M1[row:row + size, column:column + size] = 255
        elif figures == "several":
            M1 = Image.new('L', (self.__Npoint, self.__Npoint), 0)
            draw = ImageDraw.Draw(M1)
            draw.ellipse(([25, 20, (65, 50)]), 255)
            draw.rectangle(((100, 100), (150, 130)), 255)
            draw.line([(25, 125), (50, 125), (125, 50), (175, 50)], 255)
            draw.polygon([(25, 175), (50, 150), (75, 175)], 255)

        return np.array(M1, dtype=np.int32)

    def radar_return(self, fig):
        """
        Частина коду, де виконується цифрова згортка сигналу. Перебирається кожний рядок зображення, вибирається лише
        той, який має щось, окрім пустих (нульових) значень. Для кожного рядку після згортки виконуємо нормування, задля
        того, щоб значення не перевищували 255 (максимальне значення)
        :param fig:
        :return:
        """
        fig = self.figures(figures=fig)
        figures = fig.copy()
        for i in range(len(figures)):
            row = figures[i]
            if not np.all(row == 0):
                figures[i] = np.convolve(row, self.__D, mode="same")
                row_max = np.max(figures[i])
                if row_max != 0:
                    figures[i] = figures[i] / row_max * 255
        return fig, figures

    def draw_figure(self):
        """
        Частина коду, яка відповідає за малювання результатів
        :return:
        """
        for i in self.__figures:
            first_fig, second_fig = self.radar_return(i)
            img1 = Image.fromarray(first_fig)
            img1.show()
            img2 = Image.fromarray(second_fig)
            img2.show()

    def load_data_from_file(self):
        """
        Частина коду, яка відповідає за зчитування json файлу, у якому знаходяться значення для варіантів, які
        потребуються, або запускає попередню практику з варіантом, який заданий в умові, для того щоб знайти значення dX
        :return:
        """
        try:
            with open("data.json", "r") as file:
                loaded_data = json.load(file)
                for i in loaded_data:
                    if i["Variant"] == self.variant:
                        return i
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass
        dX_find(variant=self.variant).find_dX()
        return self.load_data_from_file()


if __name__ == "__main__":
    Test_radar_Image_formation(variant=7).draw_figure()
