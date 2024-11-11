import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk
from tkinter import filedialog

# Путь к вашему TIFF файлу
tif_path = tif_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

# Открываем TIFF файл
with rasterio.open(tif_path) as src:
    # Читаем данные первого канала (или нужного вам слоя)
    band1 = src.read(1)
    transform = src.transform
    # Получаем разрешение (метры на пиксель)
    resolution_x, resolution_y = src.res  # Получаем разрешение по осям X и Y
    resolution = (resolution_x + resolution_y) / 2  # Среднее разрешение
    print(resolution)

# Список для хранения выбранных точек
points = []

# Функция для преобразования географических координат в индексы пикселей
def coords_to_indices(lat, lon):
    row, col = ~transform * (lon, lat)  # Преобразование
    return int(row), int(col)

# Функция для обработки клика мыши
def on_click(event):
    if event.inaxes is not None and event.button == 1:  # Обрабатываем только левую кнопку мыши
        # Получаем координаты клика
        x, y = event.xdata, event.ydata
        A.append(x)
        A.append(y)
        # Преобразуем пиксельные координаты в географические координаты
        lon, lat = transform * (x, y)

        points.append((lat, lon))  # Сохраняем точку

        plt.scatter(x, y, color='red')  # Отметим выбранную точку на графике
        plt.draw()

        # Если выбраны две точки, извлекаем высоты и строим профиль
        if len(points) == 2:
            row1, col1 = coords_to_indices(*points[0])
            row2, col2 = coords_to_indices(*points[1])

            # Генерация линейных индексов между двумя точками
            rows = np.linspace(row1, row2, num=500).astype(int)
            cols = np.linspace(col1, col2, num=500).astype(int)

            # Ограничение индексов для предотвращения выхода за границы массива
            rows = np.clip(rows, 0, band1.shape[0] - 1)
            cols = np.clip(cols, 0, band1.shape[1] - 1)

            # Извлечение высот между двумя точками
            elevations = band1[rows, cols]

            def calculate_distance(pixel1, pixel2, resolution):
                # Вычисляем расстояние в пикселях
                distance_in_pixels = np.sqrt((pixel2[0] - pixel1[0]) ** 2 + (pixel2[1] - pixel1[1]) ** 2)
                # Преобразуем расстояние в метры
                distance_in_meters = distance_in_pixels * resolution
                return distance_in_meters

            # Вычисляем расстояние между двумя пикселями

            point1 = (A[0],A[1])
            point2 = (A[2],A[3])
            distance = calculate_distance(point1, point2, resolution)
            print(f"Расстояние между точками: {distance:.2f} метров")
            # Построение профиля местности
            plt.figure(figsize=(10, 5))
            plt.plot(elevations)
            plt.title('Профиль местности')
            plt.xlabel('Позиция вдоль линии (пиксели)')
            plt.ylabel('Высота (м)')
            plt.grid()
            plt.show()


# Отображаем данные с помощью matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(band1, cmap='terrain')  # Используем цветовую карту 'terrain'
plt.colorbar(label='Высота (м)')  # Добавляем цветовую шкалу
plt.title('Карта высот')
plt.xlabel('Пиксели по X')
plt.ylabel('Пиксели по Y')

A = []
# Подписываем обработчик клика мыши
cid = plt.gcf().canvas.mpl_connect('button_press_event', on_click)

plt.show()

# Инициализация Tkinter
root = Tk()
root.withdraw()  # Скрыть главное окно
