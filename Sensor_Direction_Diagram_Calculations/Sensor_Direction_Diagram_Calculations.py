import math
import statistics
import numpy as np
from numpy import pi, sin, cos, radians
from matplotlib.pylab import plot, grid, figure, polar, plt


class Calculator:
    def __init__(self, lam=None, L=None, delta=None):
        self.__L = L
        self.__lam = lam
        self.__delta = delta

    def __calculations(self) -> list:
        d = self.__delta * self.__lam
        K = int(self.__L / d + 1)
        N = int(180 * self.__L / self.__lam)
        A = np.empty(N, dtype=float)
        G = np.empty(N, dtype=float)
        teta = np.empty(N, dtype=float)
        for i in range(N):
            teta[i] = -90 + i * self.__lam / self.__L
            t = radians(teta[i])
            s = 0.0
            for k in range(K):
                s += 1.0 * cos(k * 2 * pi * d * np.sin(t) / self.__lam)
            A[i] = s / K
            G[i] = (sin(K * pi * d * sin(t) / self.__lam) / (K * sin(pi * d * sin(t) / self.__lam))) ** 2
        return [teta, A, G, K, N]

    def __calculations2(self) -> list:
        teta, A, G, K, N = self.__calculations()
        logG = 20 * np.log10(G)
        list_log_G = list(logG)[math.floor(len(logG) / 2)::-1]
        three_decibel_value = statistics.mean([i for i in logG if 2.9 < abs(i) < 3.1])
        main_petal = 0
        for i in list_log_G:
            if i > main_petal:
                break
            else:
                main_petal = i
        first_side_petal = main_petal
        for i in list_log_G[list_log_G.index(main_petal)::]:
            if i > first_side_petal:
                first_side_petal = i
        second_side_petal = self.__side_petal(first_side_petal, list_log_G[list_log_G.index(first_side_petal)::])
        third_side_petal = self.__side_petal(second_side_petal, list_log_G[list_log_G.index(second_side_petal)::])
        rmbp = first_side_petal
        zero_delta = abs(teta[np.where(logG == main_petal)][0])
        half_delta = abs(teta[np.where(logG == three_decibel_value)][0])
        dbs_per_octave = abs(third_side_petal - second_side_petal)
        delta_theta = abs(teta[np.where(logG == third_side_petal)][0] - teta[np.where(logG == second_side_petal)][0])
        hsbp = dbs_per_octave / delta_theta
        x_points = [teta[np.where(logG == first_side_petal)][0], teta[np.where(logG == second_side_petal)][0],
                    teta[np.where(logG == third_side_petal)][0]]
        y_points = [first_side_petal, second_side_petal, third_side_petal]
        coefficients = np.polyfit(x_points, y_points, 2)
        x_line_extended = np.linspace(min(x_points) - 5, max(x_points) + 3, 100)
        y_line_extended = np.polyval(coefficients, x_line_extended)
        return [teta, A, G, logG, half_delta, zero_delta, rmbp, hsbp, first_side_petal, second_side_petal,
                third_side_petal, x_line_extended, y_line_extended]

    @staticmethod
    def __side_petal(past, array):
        result = past
        for i in array:
            if i > result:
                for e in array[array.index(result)::]:
                    if e < result:
                        break
                    else:
                        result = e
                break
            else:
                result = i
        return result

    def __plot1(self) -> None:
        name = f"ДС у декартових координатах при λ = {self.__lam} мм, Δ = {self.__delta}, L = {self.__L} мм"
        teta, A, G, K, N = self.__calculations()
        print(f"K = {K}, N = {N}")
        fig1 = figure()
        plot(teta, abs(A))
        plt.title(name)
        plt.axhline(0, color='darkorange', linewidth=1)
        plt.axvline(0, color='darkorange', linewidth=1)
        grid(True)
        plt.savefig(fname=f"./savefig/{name}.jpeg", dpi=500)

    def __plot2(self) -> None:
        name = f"ДС у полярних координатах при λ = {self.__lam} мм, Δ = {self.__delta}, L = {self.__L} мм"
        teta, A, G, K, N = self.__calculations()
        fig2 = figure()
        polar(radians(teta), abs(A))
        plt.title(name)
        plt.savefig(fname=f"./savefig/{name}.jpeg", dpi=500)

    def __plot3(self) -> None:
        name = f"ДС при λ = {self.__lam} мм, Δ = {self.__delta}, L = {self.__L} мм (без додаткових розрахунків)"
        teta, A, G, K, N = self.__calculations()
        fig3 = figure()
        plot(teta, 20 * np.log10(G))
        plt.title(f"ДС при λ = {self.__lam} мм, Δ = {self.__delta}, L = {self.__L} мм")
        grid(True)
        plt.axhline(0, color='darkorange', linewidth=1)
        plt.axvline(0, color='darkorange', linewidth=1)
        plt.savefig(fname=f"./savefig/{name}.jpeg", dpi=500)

    def __plot3_addition(self) -> None:
        name = f"ДС при λ = {self.__lam} мм, Δ = {self.__delta}, L = {self.__L} мм (з розрахунками)"
        teta, A, G, logG, half_delta, zero_delta, rmbp, hsbp, first_side_petal, second_side_petal, third_side_petal, \
            x_line_extended, y_line_extended = self.__calculations2()
        print(f"λ = {self.__lam} мм, Δ = {self.__delta}, L = {self.__L} мм\n"
              f"δθ0.5 = {round(half_delta * 2, 2)}°,\n"
              f"δθ0 = {round(zero_delta * 2, 2)}°, \n"
              f"РМБП = {round(rmbp, 2)} дБ,\n"
              f"ШСБП = {round(hsbp, 2)} дБ/октаву\n",
              "=" * 70)
        plt.axvline(zero_delta, linestyle="--", color='red', linewidth=1)
        plt.axvline(-zero_delta, linestyle="--", color='red', linewidth=1)
        plt.axvline(half_delta, linestyle="--", color='red', linewidth=1)
        plt.axvline(-half_delta, linestyle="--", color='red', linewidth=1)
        plt.axhline(rmbp, linestyle="--", color='red', linewidth=1)
        plt.plot(teta[np.where(logG == first_side_petal)], first_side_petal, 'ro', label='Точка першої бічної пелюстки')
        plt.plot(teta[np.where(logG == second_side_petal)], second_side_petal, 'go',
                 label='Точка другої бічної пелюстки')
        plt.plot(teta[np.where(logG == third_side_petal)], third_side_petal, 'bo',
                 label='Точка третьої бічної пелюстки')
        plt.plot(x_line_extended, y_line_extended, 'k--', label='Лінія апроксимації')
        plt.legend()
        plt.savefig(fname=f"./savefig/{name}.jpeg", dpi=500)

    def main(self) -> None:
        stop_param = True
        while stop_param:
            while True:
                if self.__lam is None:
                    try:
                        self.__lam = float(input("Введіть значення λ: "))
                        break
                    except ValueError:
                        print("Введіть десяткове число!")
                else:
                    break
            while True:
                if self.__L is None:
                    try:
                        self.__L = float(input("Введіть значення L: "))
                        print(self.__L, self.__delta, self.__lam)
                        break
                    except ValueError:
                        print("Введіть десяткове число!")
                else:
                    break
            while True:
                if self.__delta is None:
                    try:
                        self.__delta = float(input("Введіть значення Δ: "))
                        break
                    except ValueError:
                        print("Введіть десяткове число!")
                else:
                    break
            choice = input("Чи потрібно розрахувати основні параметри ДС? (yes/no)\n").lower().strip()
            for i in range(1, 4):
                if i == 3:
                    stop_param = False
                    break
                self.__L *= i
                if choice == "y" or choice == "yes":
                    self.__plot1()
                    self.__plot2()
                    self.__plot3()
                    self.__plot3_addition()
                elif choice == "n" or "no":
                    self.__plot1()
                    self.__plot2()
                    self.__plot3()
                else:
                    print("Введено невірний варіант")


if __name__ == "__main__":
    Calculator(1.1, 7, 0.07).main()
