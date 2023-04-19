from PIL import Image, ImageDraw
from typing import Tuple, Dict


def create_rectangles(data: list[Dict[str, Dict[str, int]]]):
    """Cоздание картинки с визуализированными прямоугольниками по координатам"""

    # Создаем холст с размером size (ширина, высота) и цветом фона color (код RGB)
    canvas = Image.new("RGB", size=(1000, 1000), color=(0, 0, 0))

    # Создаем объект кисть для холста
    paint_brush = ImageDraw.Draw(canvas)

    # проходя через данные отрисовываем каждый прямоугольник цвета fill с шириной width
    # для построения прямоугольника достаточно использовать только две точки по диагонали
    paint_brush.rectangle(((10, 10), (990, 990)), fill=(255, 255, 255), width=100)

    for i in data:
        x_north_west, y_north_west = i['north_west'].values()
        x_south_east, y_south_east = i['south_east'].values()
        paint_brush.rectangle(((x_north_west, y_north_west), (x_south_east, y_south_east)), fill=(222, 184, 200),
                              width=10)

    # сохраняем готовое изображение
    canvas.save('canvas.png')
    # открыть результат
    canvas.show()
    return


# тестовый запуск
# store = ({'north_west': {'x': 100, 'y': 50}, 'south_east': {'x': 250, 'y': 200}},
#         {'north_west': {'x': 100, 'y': 250}, 'south_east': {'x': 250, 'y': 500}},
#         {'north_west': {'x': 100, 'y': 700}, 'south_east': {'x': 250, 'y': 950}})

# sample = create_rectangles(store)
