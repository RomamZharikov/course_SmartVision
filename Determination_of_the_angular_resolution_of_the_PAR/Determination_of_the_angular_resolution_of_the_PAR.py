import numpy as np
import matplotlib.pyplot as plt
from numpy import pi, sin, radians
from matplotlib.pyplot import figure, plot, grid


class Determination_of_the_angular_resolution_of_the_PAR:
    def __init__(self, variant: int = 7):
        self.__N = 16 + variant
        self.__objects_dimensions = 2
        self.__Npoint = 200
        self.__g = 0.5
        self.__teta_zero = 0
        self.__dX = 40
        self.__delta = 180 / self.__Npoint

    def __custom_convolution(self, x, D):
        y = np.zeros_like(x)
        for i in range(len(x)):
            for j in range(len(x)):
                if i >= j:
                    y[i] += x[j] * D[i - j]
        return y

    def __N_DC(self):
        t = [-90 + self.__delta * i for i in range(self.__Npoint)]
        E = np.empty(self.__Npoint, dtype=float)
        for i, teta in enumerate(t):
            if teta != 0:
                b = 2 * pi * self.__g * (sin(radians(teta)) - sin(radians(self.__teta_zero)))
                E[i] = abs(sin(0.5 * self.__N * b)/sin(0.5*b))/self.__N
            else:
                E[i] = 1
        t = [self.__delta * i for i in range(self.__Npoint)]
        return t, E

    def signal_one(self, A=20):
        teta, E = self.__N_DC()
        x_signal = np.zeros(self.__Npoint, dtype=float)
        N = int(self.__Npoint + A - self.__objects_dimensions)
        x_signal[A:A + self.__objects_dimensions] = 255
        y_signal = self.__custom_convolution(x_signal, E)
        y_signal_normalized = (y_signal / np.max(y_signal)) * 255
        fig1 = figure()
        plt.title(f"Відбитий сигнал")
        plot(teta, x_signal, color="red")
        grid()
        plt.axhline(0, color="black")
        plt.axvline(0, color="black")
        plot(teta, y_signal_normalized, color="blue")
        plt.show()

    def __signal(self, dX, A=20):
        teta, E = self.__N_DC()
        x_signal = np.zeros(self.__Npoint, dtype=float)
        N = int(self.__Npoint + A + (2 * self.__objects_dimensions) + dX)
        x_signal[A:A+self.__objects_dimensions] = 255
        x_signal[A + dX:A + self.__objects_dimensions + dX] = 255
        y_signal = self.__custom_convolution(x_signal, E)
        y_signal_normalized = (y_signal / np.max(y_signal)) * 255
        return teta, E, x_signal, y_signal_normalized

    def find_dX(self):
        max_avg_sig_past = 0
        x_signal_past = 0
        y_signal_past = 0
        for dX in range(self.__dX, 0, -1):
            teta, E, x_signal, y_signal = self.__signal(dX)
            first_max = int(np.argmax(y_signal))
            second_max = 0
            for j in range(len(y_signal)):
                if j + 1 < len(y_signal) and y_signal[first_max] * 0.98 <= y_signal[j] <= max(y_signal):
                    if y_signal[j - 1] <= y_signal[j] >= y_signal[j + 1] and j != first_max:
                        second_max = j
                        break
            if second_max >= 1 and first_max >= 1:
                avg_sig = y_signal[first_max + 1:second_max - 1] if first_max < second_max else y_signal[
                                                                                                second_max + 1:first_max - 1]
                max_avg_sig = []
                min_avg_sig = []
                for u in range(1, len(avg_sig)):
                    if u + 2 < len(avg_sig):
                        if avg_sig[u - 1] >= avg_sig[u] <= avg_sig[u + 1]:
                            min_avg_sig.append(avg_sig[u])
                        elif avg_sig[u - 1] <= avg_sig[u] >= avg_sig[u + 1]:
                            max_avg_sig.append(avg_sig[u])
                max_avg_sig = float(max(max_avg_sig)) if len(max_avg_sig) >= 1 else float(min(min_avg_sig))
                ratio = max_avg_sig / max(y_signal)
                if ratio >= 0.707:
                    self.__plot_results(dX, teta, max_avg_sig, x_signal, y_signal, max_avg_sig_past, x_signal_past,
                                        y_signal_past, ratio, ratio_past)
                    break
                else:
                    print(f"dX = {dX}, max_avg = {max_avg_sig}; max_avg / max_sign {round(ratio, 3)} <= 0.707 \n")
                    max_avg_sig_past = max_avg_sig
                    ratio_past = ratio
                    x_signal_past = x_signal
                    y_signal_past = y_signal

    def __plot_results(self, dX, teta, max_avg_sig, x_signal, y_signal, max_avg_sig_past, x_signal_past,
                       y_signal_past):
        fig1 = figure()
        plt.title(f"Відстань між точками, dX = {dX}")
        plot(teta, x_signal, color="red")
        grid()
        plt.axhline(0, color="black")
        plt.axvline(0, color="black")
        plot(teta, y_signal, color="blue")
        plt.axhline(max_avg_sig, color="black", linestyle="--")
        print(f"""Для відстані dX = {dX} максимальний сигнал дорівнює {round(max(y_signal), 3)}, а 0.707 від нього дорівнює {round(max(y_signal) * 0.707, 3)}.
Але сигнал між цима точками знаходиться на рівні {max_avg_sig}.

Тому вибираємо відстань dX = {dX + 1} максимальний сигнал дорівнює {round(max(y_signal_past), 3)}, а 0.707 від нього дорівнює {round(max(y_signal_past) * 0.707, 3)}
а сигнал між цима точками знаходиться на рівні {max_avg_sig_past}.
Таким чином роздільна здатність дорівнює {self.__delta * (dX + 1)}°
""")
        fig2 = figure()
        grid()
        plt.axhline(0, color="black")
        plt.axvline(0, color="black")
        plt.title(f"Відстань між точками, dX = {dX + 1}")
        plot(teta, x_signal_past, color="red")
        plot(teta, y_signal_past, color="blue")
        plt.axhline(max_avg_sig_past, color="black", linestyle="--")
        plt.show()


if __name__ == "__main__":
    d = Determination_of_the_angular_resolution_of_the_PAR()
    d.signal_one()
    d.find_dX()
