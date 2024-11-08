import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Путь к вашему TIFF файлу
tif_path = 'srtm_46_01/srtm_46_01.tif'  # Замените на путь к вашему TIFF файлу

# Открываем TIFF файл
with rasterio.open(tif_path) as src:
    # Читаем данные первого канала (или нужного вам слоя)
    band1 = src.read(1)
    transform = src.transform

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

# Подписываем обработчик клика мыши
cid = plt.gcf().canvas.mpl_connect('button_press_event', on_click)

plt.show()