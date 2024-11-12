import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Глобальные переменные для хранения координат точек
points = []


def onclick(event):
    """
    Обработчик клика мыши для выбора точек.
    """
    if event.xdata is not None and event.ydata is not None:
        points.append((event.ydata, event.xdata))  # Сохраняем (row, col)
        print(f"Точка выбрана: {event.ydata}, {event.xdata}")

        # Если выбрано 2 точки, закрываем окно
        if len(points) == 2:
            plt.close()


def seconds_to_meters(arc_seconds, radius=6371000):
    """
    Переводит угловые секунды в метры.

    :param arc_seconds: Количество угловых секунд.
    :param radius: Радиус Земли в метрах (по умолчанию 6371000 м).
    :return: Расстояние в метрах.
    """
    # Переводим угловые секунды в радианы
    radians = arc_seconds * (np.pi / 648000)

    # Вычисляем линейное расстояние
    distance = radius * radians
    return distance

def extract_elevation_profile(tif_file, points):
    """
    Извлекает профиль высоты между двумя точками из растрового файла .tif.

    :param tif_file: Путь к файлу .tif.
    :param points: Список координат двух точек (row, col).
    :return: Профиль высоты.
    """
    with rasterio.open(tif_file) as src:
        elevation_data = src.read(1)  # Чтение первого канала (высоты)

        # Получаем индексы пикселей
        row1, col1 = map(int, points[0])
        row2, col2 = map(int, points[1])

        # Генерируем линейные индексы между двумя точками
        rows = np.linspace(row1, row2, num=100).astype(int)
        cols = np.linspace(col1, col2, num=100).astype(int)

        # Извлекаем высоты по линейным индексам
        elevations = elevation_data[rows, cols]

    return elevations


# Укажите путь к вашему файлу .tif
tif_file_path = 'srtm_46_01/srtm_46_01.tif'

# Отображение карты
with rasterio.open(tif_file_path) as src:
    elevation_data = src.read(1)
    width = src.width  # Ширина в пикселях
    height = src.height  # Высота в пикселях
    crs = src.crs  # Система координат
    transform = src.transform  # Трансформация (Affine)
    resolution = src.res  # Разрешение в угловых секундах

    # Переводим разрешение из угловых секунд в метры
    resolution_meters_x = seconds_to_meters(resolution[0])
    resolution_meters_y = seconds_to_meters(resolution[1])

    plt.figure(figsize=(10, 6))
    plt.imshow(elevation_data, cmap='terrain', interpolation='nearest', aspect='auto')
    plt.colorbar(label='Elevation (meters)')
    plt.title('Выберите две точки на карте для построения профиля местности')

    # Подключаем обработчик кликов
    cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)

    plt.show()

# Проверяем, выбраны ли две точки
if len(points) == 2:
    # Извлечение профиля высоты
    elevation_profile = extract_elevation_profile(tif_file_path, points)

    # Вывод извлеченных параметров
    print(f'Размер карты: {width} пикселей (ширина) x {height} пикселей (высота)')
    print(f'Система координат: {crs}')
    print(f'Трансформация: {transform}')
    print(f'Разрешение: {resolution_meters_x:.6f} м по оси X и {resolution_meters_y:.6f} м по оси Y')

    # Построение графика профиля высоты
    plt.figure(figsize=(10, 6))
    plt.plot(elevation_profile)
    plt.title('Профиль высоты между двумя выбранными точками')
    plt.xlabel('Сегменты расстояния')
    plt.ylabel('Высота (метры)')
    plt.grid()
    plt.show()
else:
    print("Необходимо выбрать две точки.")