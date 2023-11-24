import matplotlib.pyplot as plt
from PIL.Image import fromarray
from numpy.fft import rfft2, irfft2
from Test_radar_Image_formation import Test_radar_Image_formation as figure_creator
import numpy as np


class Simulation_of_the_radar_image_spectral_method:
    def __init__(self, variant=7):
        # Ініціалізація об'єкта з варіантом та отримання необхідних даних для моделі
        five_practice = figure_creator(variant)
        self.variant = variant
        load = five_practice.load_data_from_file()

        # Збереження властивостей моделі та параметрів
        self.__N = 16 + load["Variant"]
        self.__Npoint = load["Npoint"]
        self.__ax = np.array(load["D"])
        self.__deg = []
        self.__figures = five_practice.figures("several")
        self.__a = [11, 11, 10, 10, 9, 9, 8, 8, 7, 6][variant - 1]
        self.__b = [2, 3, 3, 2, 2, 3, 3, 2, 3, 2][variant - 1]

    def generate_impulse_response(self, x):
        # Генерація імпульсної відповіді для заданого вхідного сигналу x
        return 1 / (1 + (x / self.__a) ** (2 * self.__b))

    def generate_ay_array(self):
        # Генерація масиву ay для обчислень
        y = np.arange(self.__Npoint, dtype=float)
        ay = np.array([self.generate_impulse_response(y[i]) for i in range(self.__Npoint)])
        ay[self.__Npoint // 2:] = ay[:self.__Npoint // 2][::-1]
        return ay

    def generate_image(self):
        # Генерація обробленого зображення
        ay = self.generate_ay_array()
        signal = self.__figures
        target_response = np.outer(self.__ax, ay)

        signal_spectrum = rfft2(signal)
        target_spectrum = rfft2(target_response)
        output_spectrum = signal_spectrum * target_spectrum
        output_signal = irfft2(output_spectrum)

        # Нормалізація та конвертація відображення в зображення
        normalized_output = (output_signal - np.min(output_signal)) * 255 / (
                np.max(output_signal) - np.min(output_signal))
        image = fromarray(normalized_output.astype(np.uint8))
        return image

    def plot_images(self):
        # Побудова та відображення оригінального та обробленого зображення
        original_image = fromarray(self.__figures)
        processed_image = self.generate_image()

        fig, ax = plt.subplots(2, 1)
        fig.suptitle(f"Варіант {self.variant}")

        # Побудова графіка оригінального зображення
        ax[0].imshow(original_image, cmap="gray")
        ax[0].set_title("Оригінальне зображення")
        ax[0].set_xticks([])
        ax[0].set_yticks([])

        # Побудова графіка обробленого зображення
        ax[1].imshow(processed_image, cmap="gray")
        ax[1].set_title("Оброблене зображення")
        ax[1].set_xticks([])
        ax[1].set_yticks([])

        plt.show()


if __name__ == "__main__":
    # Запуск та відображення зображень для різних варіантів
    for i in range(1, 10):
        s = Simulation_of_the_radar_image_spectral_method(i)
        s.plot_images()
