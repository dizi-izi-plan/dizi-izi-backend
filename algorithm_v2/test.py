from core import Core
import tkinter as tk
import time

room_data = {
    'width': 400,
    'length': 500,
    'height': 200,
    'min_passage': 70  # Минимальный проход 70 см
}

doors_data = [
        {
            'id': '1',
            'name': 'дверь',
            'x': 400,
            'y': 250,
            'width': 60,
            'length': 5,
            'height': 200,
        }
]
windows_data = [
        {
            'id': '3',
            'name': 'окно',
            'x': 200,
            'y': 0,
            'width': 180,
            'length': 10,
            'height': 120,
        }
]

floor_objects_data = [
    {
        'id': '1',
        'name': 'Кровать',
        'tag': 'sz', # sleep zone
        'dimension': 'large_furniture',
        'width': 180,
        'length': 200,
        'height': 40,
    },
    {
        'id': '2',
        'name': 'Шкаф',
        'tag': 'wz', # wardrobe zone
        'dimension': 'large_furniture',
        'width': 120,
        'length': 60,
        'height': 200,
    },
    {
        'id': '3',
        'name': 'Стол',
        'tag': 'pz', # pier glass zone
        'dimension': 'large_furniture',
        'width': 90,
        'length': 60,
        'height': 60,
    },
    {
        'id': '4',
        'name': 'Стул',
        'tag': 'sz', # sleep zone
        'dimension': 'medium_furniture',
        'width': 60,
        'length': 40,
        'height': 30,
    },
    {
        'id': '5',
        'name': 'Тумба',
        'tag': 'sz', # sleep zone
        'dimension': 'medium_furniture',
        'width': 100,
        'length': 50,
        'height': 40,
    },
    {
        'id': '6',
        'name': 'Тумба',
        'tag': 'sz', # sleep zone
        'dimension': 'medium_furniture',
        'width': 100,
        'length': 50,
        'height': 40,
    }
]

start = time.perf_counter()

alg = Core(room_data, doors_data, windows_data, floor_objects_data)

end = time.perf_counter()
print(f"Время выполнения: {end - start:.6f} секунд")

import tkinter as tk

def draw_room(canvas, room, canvas_width, canvas_height, margin):

    # Рисуем комнату как прямоугольник
    x0 = margin
    y0 = margin
    x1 = room.width + margin
    y1 = room.length + margin

    canvas.create_rectangle(x0, y0, x1, y1, outline='black', fill='lightgray')

def draw_openings(canvas, openings, canvas_width, canvas_height, margin):
    for opening in openings:
        rect = opening.create_rectangle()
        x0 = opening.x + margin
        y0 = opening.y + margin
        x1 = opening.x + rect.width + margin
        y1 = opening.y + rect.length + margin
        canvas.create_rectangle(x0, y0, x1, y1, outline='blue', fill='lightblue', width=2)


def draw_zones(canvas, zones, canvas_width, canvas_height, margin):
    # Отрисовка зон
    for zone in zones:
        rect = zone.create_rectangle()
        x0 = zone.x + margin
        y0 = zone.y + margin
        x1 = zone.x + rect.width + margin
        y1 = zone.y + rect.length + margin
        # Рисуем многоугольник по углам зоны
        canvas.create_rectangle(x0, y0, x1, y1, outline='', fill='lightblue', width=2)
        
        t_x = x0 + rect.width/2
        t_y = y0 + rect.length/2
        
        canvas.create_text(t_x, t_y, text = zone.name, fill = 'black')

def draw_objects(canvas, objects, canvas_width, canvas_height):
    
    for obj in objects:
        
        if obj.dimension == 'large_furniture':
            color = 'lightgreen'
        else:
            color = 'lightyellow'
            
        if obj.name == 'розетка':
            color = 'red'
            
        obj_r = obj.create_rectangle()
        obj_x0 = obj_r.x + margin
        obj_y0 = obj_r.y + margin
        obj_x1 = obj_r.x + obj_r.width + margin
        obj_y1 = obj_r.y + obj_r.length + margin
        
        canvas.create_rectangle(obj_x0, obj_y0, obj_x1, obj_y1, outline='black', fill=color, width=1)
        
        center = obj.center
        x = center.x + margin
        y = center.y + margin
        r = 2
        canvas.create_oval(x - r, y - r, x + r, y + r, fill='blue')

# Создаем окно и холст
room = alg.room
openings = alg.get_openings
margin = 50
root = tk.Tk()
canvas_width = room.width + margin*2
canvas_height = room.length + margin*2
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# Предполагается, что у вас есть переменные `room` и `zones`
# Например:
zones = alg.run_algorithm()

# Отрисовка комнаты
draw_room(canvas, room, canvas_width, canvas_height, margin)
objects = room.furnitures + room.electricity_points
# Отрисовка зон
draw_zones(canvas, zones, canvas_width, canvas_height, margin)
draw_objects(canvas, objects, canvas_width, canvas_height)
draw_openings(canvas, openings, canvas_width, canvas_height, margin)
root.mainloop()