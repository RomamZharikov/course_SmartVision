import matplotlib.pyplot as plt
import numpy as np
from numpy import pi, sin, arcsin, radians, degrees
from matplotlib.pylab import figure, plot, grid
import tkinter as tk


class Scanning:
    def __init__(self, Npoint=1000, gamma=0.5, variant=7, teta=0.0):
        self.current_values_label = None
        self.__ent_gamma = None
        self.__ent_variant = None
        self.root = None
        self.__Npoint = Npoint
        self.__gamma = gamma
        self.__teta = teta
        self.__N = 6 + variant
        self.__delta = 180 / (Npoint - 1)

    # Розрахунок массиву точок діаграми спрямованості
    def __RadPattern(self, teta0=0):
        D = np.empty(self.__Npoint, dtype=float)
        for i in range(self.__Npoint):
            theta = radians(-90 + self.__delta * i)
            beta = 2 * pi * self.__gamma * (sin(theta) - sin(radians(teta0)))
            D[i] = abs(sin(0.5 * self.__N * beta) / sin(0.5 * beta)) / self.__N
        return D

    # Розрахунок массиву точок діаграми спрямованості з урахуванням фазового зсуву
    def __RadScan(self, phase=0):
        S = np.empty(self.__Npoint, dtype=float)
        for i in range(self.__Npoint):
            theta = radians(-90 + self.__delta * i)
            thet0 = arcsin(phase / (2 * pi * self.__gamma))
            beta = 2 * pi * self.__gamma * (sin(theta) - sin(thet0))
            sinBdiv2 = sin(0.5 * beta)
            S[i] = abs(sin(0.5 * self.__N * beta) / sin(0.5 * beta)) / self.__N if sinBdiv2 != 0 else 1
        return S

    # Метод для розрахунку довжини головної пелюстки
    def __WGL(self, D):
        teta_max = np.argmax(D)
        left_right = []
        for i in [-1, 1]:
            D_scan = D[:teta_max] if i == -1 else D[teta_max:]
            D_scan = D_scan[::i]
            for j in range(len(D_scan)):
                if (j + 1) < len(D_scan) and (D_scan[j] < D_scan[j + 1]):
                    left_right.append(j * 180 / (len(D) - 1))
                    break
        return sum(left_right)

    # Розрахунок фазового зсуву
    def __phi(self, degree=30):
        return 2 * pi * self.__gamma * sin(radians(degree))

    # Розрахунок та побудова залежності куту напрямку променя ФАР від фази
    def __angle_dependence_with_linear_phase_change(self):
        phase_degree = range(-180, 180)
        teta = np.empty(len(phase_degree), dtype=float)
        for i in range(len(phase_degree)):
            teta[i] = degrees(-arcsin(radians(phase_degree[i]) / (2 * pi * self.__gamma)))
        fig1 = figure()
        plt.axvline(x=0, color='black', linestyle='-')
        plt.axhline(y=0, color='black', linestyle='-')
        grid(True)
        plot(phase_degree, teta)
        plt.show()

    # Побудова графіка 3 графіків (1 без зсуву, 2 з зсувом у 30 та 40 градусів)
    def __plot_signal(self, degree1=30, degree2=40):
        D = self.__RadPattern()
        S1 = self.__RadScan(phase=self.__phi(degree1))
        S2 = self.__RadScan(phase=self.__phi(degree2))
        teta = np.linspace(-90.0, 90.0, self.__Npoint)
        fig1 = figure()
        plot(teta, D, 'r')
        plot(teta, S1, 'b')
        plot(teta, S2, 'orange')
        grid(True)
        plt.show()

    # Розрахунок та побудова графіка залежності фазового зсуву від довжини головної пелюстки
    def __analysis_scan(self, tscan=range(-40, 45, 5)):
        K = len(tscan)
        ws1 = np.empty(K, dtype=float)
        for k in range(K):
            S1 = self.__RadScan(phase=self.__phi(tscan[k]))
            ws1[k] = self.__WGL(S1)
        fig2 = figure()
        plot(tscan, ws1, "b")
        plt.show()

    # Головне меню
    def main(self):
        self.root = tk.Tk()
        self.root.title("Modeling of the process of electronic scanning with a PAR beam")
        variant_label = tk.Label(text="Обновить вариант:")
        variant_label.grid(row=0, column=0, sticky='w')
        self.__ent_variant = tk.Entry(self.root)
        self.__ent_variant.grid(row=0, column=1)
        update_variant_button = tk.Button(text="Обновить", command=self.__update_variant)
        update_variant_button.grid(row=0, column=2)
        gamma_label = tk.Label(text="Обновить гамму:")
        gamma_label.grid(row=1, column=0, sticky='w')
        self.__ent_gamma = tk.Entry(self.root)
        self.__ent_gamma.grid(row=1, column=1)
        update_gamma_button = tk.Button(text="Обновить", command=self.__update_gamma)
        update_gamma_button.grid(row=1, column=2)
        self.current_values_label = tk.Label(text=f"Текущий вариант: {self.__N - 6}, "
                                                  f"Текущее расстояние между елементами (гамма): {self.__gamma}")
        self.current_values_label.grid(row=2, columnspan=3)
        button_1 = tk.Button(text="Диаграма направленности (пример)", command=self.__plot_signal)
        button_1.grid(row=3, column=0)
        button_2 = tk.Button(text="Зависимость длинны главного лепестка от сдвига", command=self.__analysis_scan)
        button_2.grid(row=3, column=1)
        button_3 = tk.Button(text="Зависимости угла направления луча ФАР",
                             command=self.__angle_dependence_with_linear_phase_change)
        button_3.grid(row=3, column=2)
        self.root.mainloop()

    def __update_variant(self):
        variant_value = self.__ent_variant.get()
        if variant_value:
            try:
                self.__N = int(variant_value) + 6
            except ValueError:
                self.__ent_variant.delete(0, 'end')
                self.__ent_variant.insert(0, "Введите число!")
        else:
            self.__N = 13
        self.__update_current_values_label()

    def __update_gamma(self):
        gamma_value = self.__ent_gamma.get()
        if gamma_value:
            try:
                self.__gamma = float(gamma_value)
            except ValueError:
                self.__ent_gamma.delete(0, 'end')
                self.__ent_gamma.insert(0, "Введите число!")
        else:
            self.__gamma = 0.5
        self.__update_current_values_label()

    def __update_current_values_label(self):
        current_variant = self.__N
        current_gamma = self.__gamma
        text = f"Текущий вариант: {current_variant - 6}, Текущее расстояние между елементами (гамма): {current_gamma}"
        self.current_values_label.config(text=text)


if __name__ == "__main__":
    scan = Scanning()
    scan.main()
