import rasterio
import matplotlib.pyplot as plt
import numpy as np
import mplcursors

# Путь к вашему файлу TIFF.
tif_path = 'srtm_46_01/srtm_46_01.tif'

# Открываем растровый файл
with rasterio.open(tif_path) as src:
    # Читаем данные в виде массива
    data = src.read(1)  # Читаем первый канал
    transform = src.transform  # Получаем трансформацию для конвертации координат

# Отображаем данные
plt.figure(figsize=(10, 10))
plt.imshow(data, cmap='terrain')
plt.colorbar(label='Высота (м)')
plt.title('Цифровая модель рельефа')
plt.xlabel('Пиксели по X')
plt.ylabel('Пиксели по Y')


# Функция для получения высоты по координатам клика
def get_height(event):
    # Получаем координаты клика
    x = int(event.xdata)
    y = int(event.ydata)

    # Проверяем, что координаты находятся в пределах массива данных
    if 0 <= x < data.shape[1] and 0 <= y < data.shape[0]:
        height_value = data[y, x]
        # Преобразуем пиксели в географические координаты
        lon, lat = transform * (x, y)
        print(f"Координаты: ({lon:.2f}, {lat:.2f}), Высота: {height_value:.2f} м")


# Подключаем обработчик кликов на графике
cid = plt.gcf().canvas.mpl_connect('button_press_event', get_height)

plt.show()

