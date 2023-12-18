import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from os import mkdir


class Statistical_analysis_of_images:
    def __init__(self, file_name: str):
        if len(file_name.split(sep=".")) == 1:
            self.file_name = f"{file_name}.jpg"
        else:
            self.file_name = file_name

    def read_img(self):
        img = Image.open(f"images/{self.file_name}")
        fig1 = plt.figure()
        plt.imshow(img)
        return img

    def crop_img(self, x1, y1, x2, y2, filename="origin", num=0) -> Image:
        self.check_directory(filename)
        img = self.read_img()
        img2 = img.crop((x1, y1, x2, y2))
        fig2 = plt.figure()
        plt.imshow(img2)
        plt.savefig(f"{filename}/{num}.jpg")
        return img2

    @staticmethod
    def read_answer() -> list:
        plt.show()
        while True:
            answer = input("Введіть координати зони (лівої верхньої та правої нижньої через пробіл):\n")
            if len(answer.split(sep=" ")) == 4:
                try:
                    answer = list(map(int, answer.split(sep=" ")))
                    return answer
                except ValueError:
                    print("Введіть числа, а не текст")
            else:
                print("Введіть 4 значення")

    def check_directory(self, filename):
        try:
            mkdir(filename)
        except FileExistsError:
            pass

    def plot_rgb_hist(self, result, result_hist, filename, histname, m=64):
        self.check_directory(filename)
        for i in range(len(result)):
            fig3 = plt.figure()
            plt.title(histname[i])
            plt.imshow(result[i])
            plt.savefig(f"{filename}/{histname[i]}_image.jpg")
            fig3 = plt.figure()
            plt.hist(result_hist[i], m, color=histname[i], density=True)
            plt.savefig(f"{filename}/{histname[i]}_hist.jpg")
        plt.show()

    def plot_table_correlation(self, correlation_data, color_name, num_file, filename="correlation_table"):
        self.check_directory(filename)

        data_correlation = [
            ['', color_name[0], color_name[1], color_name[2]],
            [color_name[0], correlation_data[0], correlation_data[1], correlation_data[2]],
            [color_name[1], correlation_data[3], correlation_data[4], correlation_data[5]],
            [color_name[2], correlation_data[6], correlation_data[7], correlation_data[8]]
        ]
        table = plt.table(cellText=data_correlation, loc='center', cellLoc='center', colLabels=None)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        for key, cell in table.get_celld().items():
            cell.set_edgecolor('black')
            if key[0] == 0 or key[1] == -1:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor('#1f77b4')
            elif key[1] == 0:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor('#ff7f0e')

        plt.axis('off')
        plt.savefig(f"{filename}/{num_file}.jpg")
        plt.show()

    def plot_table_statistics(self, data, color_name, num_file, filename="statistics"):
        self.check_directory(filename)
        cows = [num_file, "Середнє вибіркове", "СКВ"]
        data_stats = [
            [cows[0], color_name[0], color_name[1], color_name[2]],
            [cows[1], data[0][0], data[1][0], data[2][0]],
            [cows[2], data[0][1], data[1][1], data[2][1]],
        ]
        fit = plt.figure(figsize=(10, 5))
        table = plt.table(cellText=data_stats, loc='center', cellLoc='center', colLabels=None)
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        for key, cell in table.get_celld().items():
            cell.set_edgecolor('black')
            if key[0] == 0 or key[1] == -1:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor('#1f77b4')
            elif key[1] == 0:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor('#ff7f0e')

        plt.axis('off')
        plt.savefig(f"{filename}/{num_file}.jpg")
        plt.show()

    @staticmethod
    def correlation(result, n):
        correlation_data = []
        statistics_value = []
        for i in range(len(result)):
            correlation_data.append([result[i], np.mean(result[i]), np.std(result[i])])
            statistics_value.append([round(float(np.mean(result[i])), 2), round(float(np.std(result[i])), 2)])
        correlation = []
        for first_color in correlation_data:
            for second_color in correlation_data:
                Z = (first_color[0] - first_color[1]) * (second_color[0] - second_color[1])
                result_c = round((sum(Z) / (n - 1)) / (first_color[2] * second_color[2]), 4)
                if result_c > 1:
                    result_c = 1
                correlation.append(result_c)
        return correlation, statistics_value

    def rgb_plot(self, filename, origin_name):
        coord = self.read_answer()
        img2 = self.crop_img(x1=coord[0], x2=coord[2], y1=coord[1], y2=coord[3], num=origin_name)
        r, g, b = img2.split()
        R = np.reshape(np.asarray(r), -1)
        G = np.reshape(np.asarray(g), -1)
        B = np.reshape(np.asarray(b), -1)
        N = R.size
        M = 64
        result_s = [np.asarray(r), np.asarray(g), np.asarray(b)]
        result = [R, G, B]
        colors = ["red", "green", "blue"]
        self.plot_rgb_hist(result_s, result, filename, colors, M)
        correlation_values, statistics_value = self.correlation(result, N)
        self.plot_table_correlation(correlation_values, colors, num_file=origin_name)
        self.plot_table_statistics(data=statistics_value, color_name=colors, num_file=origin_name)


if __name__ == "__main__":
    stat = Statistical_analysis_of_images("07")
    stat.rgb_plot("first", "Море")
    stat.rgb_plot("second", "Ліс")
