import numpy as np
import rasterio
import matplotlib.pyplot as plt

# Глобальные переменные для хранения выбранных точек
points = []


def get_elevation_profile(raster_file, point1, point2, num_points=100):
    with rasterio.open(raster_file) as src:
        transform = src.transform

        # Генерируем линейные интерполяции между двумя точками
        lons = np.linspace(point1[0], point2[0], num_points)
        lats = np.linspace(point1[1], point2[1], num_points)

        elevations = []
        for lon, lat in zip(lons, lats):
            row, col = ~transform * (lon, lat)
            row = int(row)
            col = int(col)

            # Получаем значение высоты из растрового изображения
            elevation = src.read(1)[row, col]
            elevations.append(elevation)

    return elevations


def onclick(event):
    global points
    if event.xdata is not None and event.ydata is not None:
        points.append((event.xdata, event.ydata))
        plt.plot(event.xdata, event.ydata, 'ro')  # Отметить выбранную точку
        plt.draw()

        # Если выбраны две точки, строим профиль
        if len(points) == 2:
            plt.disconnect(cid)  # Отключаем обработчик кликов
            profile = get_elevation_profile(raster_file, points[0], points[1])
            distance = np.linspace(0, 100, len(profile))  # Пример расстояния в метрах

            # Построение графика профиля местности
            plt.figure(figsize=(10, 5))
            plt.plot(distance, profile)
            plt.title('Профиль местности')
            plt.xlabel('Расстояние (м)')
            plt.ylabel('Высота (м)')
            plt.grid()
            plt.show()


# Путь к файлу с данными высоты
raster_file = 'srtm_46_01/srtm_46_01.tif'  # Укажите путь к файлу с данными высоты

# Отображение карты
with rasterio.open(raster_file) as src:
    data = src.read(1)  # Чтение первого канала (высота)
    plt.imshow(data, cmap='terrain')
    plt.colorbar(label='Высота (м)')

    # Подключаем обработчик кликов мыши
    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)

plt.title('Выберите две точки на карте')
plt.show()