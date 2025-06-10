import math
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float


def room_crossover_check(obj, room) -> bool:
    corners = obj.get_corners()
    for corner in corners:
        if corner.x < 0 or corner.x > room.width or corner.y < 0 or corner.y > room.length:
            return False
    return True


def intersects_check(obj, other_obj) -> bool:
    """Проверяет пересечение с другим прямоугольником"""
    # Используем алгоритм разделяющей оси (Separating Axis Theorem)
    # для проверки пересечения двух произвольно повернутых прямоугольников

    corners1 = obj.get_corners()
    corners2 = other_obj.get_corners()
    # Проверяем все возможные оси проекции
    edges = []
    for i in range(4):
        edges.append((corners1[i], corners1[(i + 1) % 4]))
        edges.append((corners2[i], corners2[(i + 1) % 4]))

    for edge in edges:
        # Вектор, перпендикулярный ребру
        normal = Point(-(edge[1].y - edge[0].y), edge[1].x - edge[0].x)

        # Проецируем все углы на нормаль
        min1 = max1 = None
        min2 = max2 = None

        for corner in corners1:
            projection = corner.x * normal.x + corner.y * normal.y
            if min1 is None or projection < min1:
                min1 = projection
            if max1 is None or projection > max1:
                max1 = projection

        for corner in corners2:
            projection = corner.x * normal.x + corner.y * normal.y
            if min2 is None or projection < min2:
                min2 = projection
            if max2 is None or projection > max2:
                max2 = projection

        # Если проекции не пересекаются, прямоугольники не пересекаются
        if max1 < min2 or max2 < min1:
            return True

    return False


def distance_check(obj1, obj2, distance):
    """Вычисляет минимальное расстояние между прямоугольниками"""
        
    # Находим ближайшие точки между прямоугольниками
    corners1 = obj1.get_corners()
    corners2 = obj2.get_corners()
    
    min_distance = float('inf')
    for p1 in corners1:
        for p2 in corners2:
            dist = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
            min_distance = min(min_distance, dist)
    
    return min_distance - distance 


def openings_intersects_check(obj, openings):
    min_distance = 60
    for opening in openings:
        if not intersects_check(obj, opening) or distance_check(obj, opening, min_distance) < 0:
            return False
    return True
