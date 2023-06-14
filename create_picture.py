from PIL import Image, ImageDraw, ImageOps


def create_rectangles(data: list):
    """Cоздание картинки с визуализированными прямоугольниками по координатам"""

    # Создаем холст с размером size (ширина, высота) и цветом фона color (код RGB)
    canvas = Image.new("RGB", size=(700, 500), color=(0, 0, 0))

    # Создаем объект кисть для холста
    paint_brush = ImageDraw.Draw(canvas)

    # проходя через данные отрисовываем каждый прямоугольник цвета fill с шириной width
    # для построения прямоугольника достаточно использовать только две точки по диагонали
    paint_brush.rectangle(
        ((0, 0), (700, 500)), fill=(255, 255, 255), width=100
    )

    for item in data:
        x_north_west, y_north_west = item['north_west'].values()
        x_north_east, y_north_east = item['north_east'].values()
        x_south_east, y_south_east = item['south_east'].values()
        x_south_west, y_south_west = item['south_west'].values()
        paint_brush.polygon(
            (
                (x_north_west * 50, y_north_west * 50),
                (x_north_east * 50, y_north_east * 50),
                (x_south_east * 50, y_south_east * 50),
                (x_south_west * 50, y_south_west * 50),
            ),
            fill=(222, 184, 200),
            width=10,
        )

    canvas = canvas.rotate(180)
    canvas = ImageOps.mirror(canvas)
    # сохраняем готовое изображение
    canvas.save('canvas.png')
    # открыть результат
    canvas.show()
    return


# тестовый запуск
# store = ({'north_west': {'x': 100, 'y': 50}, 'south_east': {'x': 250, 'y': 200}},
#         {'north_west': {'x': 100, 'y': 250}, 'south_east': {'x': 250, 'y': 500}},
#         {'north_west': {'x': 100, 'y': 700}, 'south_east': {'x': 250, 'y': 950}})
#
# sample = create_rectangles(store)

# store_2 = [{'north_west': {'x': 4, 'y': 10}, 'north_east': {'x': 7, 'y': 10}, 'south_west': {'x': 4, 'y': 9}, 'south_east': {'x': 7, 'y': 9}},
#            {'north_west': {'x': 14, 'y': 0}, 'north_east': {'x': 12, 'y': 0}, 'south_west': {'x': 14, 'y': 4}, 'south_east': {'x': 12, 'y': 4}},
#            {'north_west': {'x': 0, 'y': 0.0}, 'north_east': {'x': 0, 'y': 2.0}, 'south_west': {'x': 3, 'y': 0.0}, 'south_east': {'x': 3, 'y': 2.0}},
#            {'north_west': {'x': 7.5, 'y': 0}, 'north_east': {'x': 4.5, 'y': 0}, 'south_west': {'x': 7.5, 'y': 1}, 'south_east': {'x': 4.5, 'y': 1}}]
# create_rectangles(store_2)
