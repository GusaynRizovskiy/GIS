import rasterio
import numpy as np
import matplotlib.pyplot as plt


class ElevationProfile:
    def __init__(self, tif_path):
        self.tif_path = tif_path
        self.points = []
        self.data = None
        self.transform = None

    def load_data(self):
        with rasterio.open(self.tif_path) as src:
            self.transform = src.transform
            self.data = src.read(1)  # Читаем первый слой

    def get_elevation_profile(self):
        if len(self.points) < 2:
            print("Необходимо выбрать две точки.")
            return None

        point1, point2 = self.points
        row1, col1 = ~self.transform * point1
        row2, col2 = ~self.transform * point2

        # Проверка на допустимые индексы.
        rows = np.clip(np.linspace(int(row1), int(row2), num=100).astype(int), 0, self.data.shape[0] - 1)
        cols = np.clip(np.linspace(int(col1), int(col2), num=100).astype(int), 0, self.data.shape[1] - 1)

        elevations = self.data[rows, cols]
        return elevations

    def on_click(self, event):
        if event.inaxes is not None and event.button == 1:  # Обрабатываем только левую кнопку мыши
            x, y = event.xdata, event.ydata
            self.points.append((x, y))
            plt.scatter(x, y, color='red')  # Отметим выбранные точки
            plt.draw()

            if len(self.points) == 2:
                elevations = self.get_elevation_profile()
                if elevations is not None:
                    self.plot_elevation_profile(elevations)

    def plot_elevation_profile(self, elevations):
        plt.figure()
        plt.plot(elevations)
        plt.title('Профиль местности между двумя точками')
        plt.xlabel('Позиция вдоль линии')
        plt.ylabel('Высота (м)')
        plt.grid()
        plt.show()


def main():
    tif_path = 'srtm_46_01/srtm_46_01.tif'  # Замените на ваш путь к TIFF файлу
    profile = ElevationProfile(tif_path)

    # Загружаем данные
    profile.load_data()

    # Отображаем растровое изображение
    plt.imshow(profile.data, cmap='terrain')
    plt.title('Выберите две точки на карте')
    plt.colorbar(label='Высота (м)')

    # Подписываем обработчик клика мыши
    cid = plt.gcf().canvas.mpl_connect('button_press_event', profile.on_click)

    plt.show()


if __name__ == "__main__":
    main()