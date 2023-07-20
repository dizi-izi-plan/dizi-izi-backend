from PIL import Image, ImageDraw, ImageOps


def create_rectangles(data: list, borders: dict, powersocets: list):
    """Cоздание картинки с визуализированными прямоугольниками по
    координатам."""

    # Создаем холст с размером size (ширина, высота) и цветом фона color
    # (код RGB)

    if borders["north_east"]["x"] < 100:
        centering = 3
        external_border = 1.7
        border_width = 1
    elif borders["north_east"]["x"] < 1000:
        centering = 30
        external_border = 1.4
        border_width = 10
    else:
        centering = 300
        external_border = 1.1
        border_width = 100

    canvas = Image.new("RGB", size=(int(borders["north_east"]["x"]*external_border),
                                    int(borders["north_east"]["y"]*external_border)),
                                    color=(255, 255, 255))



    # Создаем объект кисть для холста
    paint_brush = ImageDraw.Draw(canvas)

    # рисуем границы комнаты для визуального отслеживания пересечений
    paint_brush.line((borders["south_west"]["x"] + centering, borders["south_west"]["y"] + centering,
                      borders["south_east"]["x"] + centering, borders["south_east"]["y"] + centering),
                     fill=(177, 220, 165), width=border_width)
    paint_brush.line((borders["south_east"]["x"] + centering, borders["south_east"]["y"] + centering,
                      borders["north_east"]["x"] + centering, borders["north_east"]["y"] + centering),
                     fill=(177, 220, 165), width=border_width)
    paint_brush.line((borders["north_west"]["x"] + centering, borders["north_west"]["y"] + centering,
                      borders["north_east"]["x"] + centering, borders["north_east"]["y"] + centering),
                     fill=(177, 220, 165), width=border_width)
    paint_brush.line((borders["south_west"]["x"] + centering, borders["south_west"]["y"] + centering,
                      borders["north_west"]["x"] + centering, borders["north_west"]["y"] + centering),
                     fill=(177, 220, 165), width=border_width)


    # проходя через данные отрисовываем каждый прямоугольник цвета fill с шириной width
    # для построения прямоугольника достаточно использовать только две точки по диагонали


    for item in data:
        x_north_west, y_north_west = item['north_west'].values()
        x_north_east, y_north_east = item['north_east'].values()
        x_south_east, y_south_east = item['south_east'].values()
        x_south_west, y_south_west = item['south_west'].values()
        paint_brush.polygon(
            (
                (x_north_west+centering, y_north_west+centering),
                (x_north_east+centering, y_north_east+centering),
                (x_south_east+centering, y_south_east+centering),
                (x_south_west+centering, y_south_west+centering),
            ),
            fill=(222, 184, 200),
            width=10,
        )

    # for item in powersocets:
    for item in powersocets:
        paint_brush.regular_polygon(
            (item['x']+centering, 
             item['y']+centering, 100
            ), n_sides= 4, 
            fill=(0, 100, 0)
        )
    print('hoVNJKSVSNDVS:UIDVNSDVUISDVSDV')
    canvas = canvas.rotate(180)
    canvas = ImageOps.mirror(canvas)
    # сохраняем готовое изображение
    canvas.save('canvas.png')
    # открыть результат
    canvas.show()



