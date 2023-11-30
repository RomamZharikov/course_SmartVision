import numpy as np
from numpy.random import random
from matplotlib.pyplot import subplots, show


class Simulation_of_random_noise_with_a_given_distribution:
    def __init__(self, N, M, Ng):
        """
        :param N: об'єм вибірки
        :param M: кількість стовбців гістограми
        :param Ng: кількість точок для графіку щільності розподілу
        """
        self.__N = N
        self.__M = M
        self.__Ng = Ng

    @staticmethod
    def __Function():
        """
        Обернена функція
        :return:
        """
        return (7 * random() + 1) ** (2/3)

    def __function(self, x):
        """
        Функція щільності розподілу
        :param x:
        :return:
        """
        return 3/14*np.sqrt(x)

    def plot(self):
        """
        Метод для генерації вибірки та побудова цієї вибірки на графіку. Також розрахунок та побудова гістограми з
        щільністю розподілу.
        :return:
        """
        x = [self.__Function() for _ in range(self.__N)]
        w = np.linspace(min(x), max(x), self.__Ng)
        y = [self.__function(i) for i in w]
        fig, ax = subplots(2, 1)
        ax[0].scatter(np.linspace(0, self.__N - 1, self.__N), y=x, color="red", edgecolor="black", s=10)
        ax[1].hist(x, self.__M, edgecolor="k", density=True)
        ax[1].plot(w, y, color="black")
        show()


if __name__ == "__main__":
    s = Simulation_of_random_noise_with_a_given_distribution(5000, 15, 100)
    s.plot()




