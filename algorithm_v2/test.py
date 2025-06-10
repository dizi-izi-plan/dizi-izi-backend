from core import Core
import tkinter as tk
import time

room_data = {
    'width': 400,
    'length': 500,
    'height': 200,
    'min_passage': 70  # Минимальный проход 70 см
}

openings_data = [
    {
        'id': '1',
        'name': 'дверь',
        'x': 400,
        'y': 250,
        'width': 60,
        'length': 5,
        'height': 200,
        'rotation': 90
    },

    {
        'id': '3',
        'name': 'окно',
        'x': 200,
        'y': 0,
        'width': 120,
        'length': 10,
        'height': 150,
        'rotation': 0
    }
]

floor_objects_data = [
    {
        'id': '1',
        'name': 'Кровать',
        'width': 90,
        'length': 200,
        'height': 50,

    },
    {
        'id': '2',
        'name': 'Шкаф',
        'width': 60,
        'length': 120,
        'height': 200,

    },
    {
        'id': '3',
        'name': 'Стол',
        'width': 60,
        'length': 90,
        'height': 75,

    },
    {
        'id': '4',
        'name': 'Стул',
        'width': 45,
        'length': 45,
        'height': 90,

    },
    {
        'id': '5',
        'name': 'Тумба',
        'width': 50,
        'length': 50,
        'height': 250,

    }
]

wall_objects_data = []
start = time.perf_counter()

alg = Core(room_data, openings_data, floor_objects_data, wall_objects_data)
end = time.perf_counter()
print(f"Время выполнения: {end - start:.6f} секунд")


# Создаем окно
root = tk.Tk()
root.title("Комната с проемами")
canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# Центр холста
center_x = canvas_width / 2
center_y = canvas_height / 2


# Отрисовка комнаты как прямоугольника
def draw_room(room):
    x0 = center_x - room.width / 2
    y0 = center_y - room.length / 2
    x1 = center_x + room.width / 2
    y1 = center_y + room.length / 2
    # Рисуем комнату
    rect_id = canvas.create_rectangle(x0, y0, x1, y1, outline='black', width=2)
    return rect_id


# Функция для отрисовки проема
def draw_opening(opening, room):
    # Размеры
    w = opening.width
    l = opening.length
    # Координаты проема относительно левого верхнего угла комнаты
    x_rel = opening.x
    y_rel = opening.y

    # Отрисовка относительно левого верхнего угла комнаты
    # Координаты центра проема внутри комнаты
    x_center = center_x - room.width / 2 + x_rel + w / 2
    y_center = center_y - room.length / 2 + y_rel + l / 2

    # Вычисление углов
    x0 = x_center - w / 2
    y0 = y_center - l / 2
    x1 = x_center + w / 2
    y1 = y_center + l / 2

    color = 'brown' if opening.name == 'дверь' else 'blue'
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')
    # Можно добавить подписи
    canvas.create_text(x_center, y_center, text=opening.name, font=('Arial', 8))


def draw_object(obj, room):
    # Размеры объекта
    w = obj.width
    l = obj.length
    corners = obj.get_corners()
    x0 = corners[3].x + center_x - room.width / 2
    y0 = corners[3].y + center_y - room.length / 2
    x1 = corners[1].x + center_x - room.width / 2
    y1 = corners[1].y + center_y - room.length / 2
    # Координаты центра объекта внутри комнаты
    x_center = center_x - room.width / 2 + obj.x + w / 2
    y_center = center_y - room.length / 2 + obj.y + l / 2

    # Цвет
    color = 'green' if obj.name == 'Кровать' else 'orange'
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')
    # Подпись
    canvas.create_text(x_center, y_center, text=obj.name, font=('Arial', 8))


# Отрисовка комнаты
draw_room(alg.get_room)

# Отрисовка всех проемов
for opening in alg.get_openings:
    draw_opening(opening, alg.get_room)
# Отрисовка объектов
for obj in alg.get_floor_objects:
    draw_object(obj, alg.get_room)
root.mainloop()
