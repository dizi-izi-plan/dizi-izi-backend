from dataclasses import dataclass
import math
import random
from typing import List, Dict, Tuple, Any, Optional

from sandbox import *

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Room:
        width: float
        length: float
        height: float

@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    length: float
    rotation: float = 0  # в градусах
     
@dataclass
class BuildingObject:
    """ Общий класс для объекта комнаты и манипуляции с ним """
    
    id: Optional[str] = None
    name: Optional[str] = None
    width: Optional[float] = None
    length: Optional[float] = None
    height: Optional[float] = None
    x: Optional[float] = None
    y: Optional[float] = None
    rotation: Optional[int] = 0
            
    def create_rectangle(self) -> Rectangle:
        """Создает прямоугольник для данного предмета мебели"""
        
        # Если поворот на 90 или 270 градусов, меняем местами ширину и длину
        if self.rotation in [90, 270]:
            return Rectangle(self.x, self.y, self.length, self.width, self.rotation)
        return Rectangle(self.x, self.y, self.width, self.length, self.rotation)
        
    def get_corners(self) -> List[Point]:
        """Возвращает координаты углов прямоугольника с учетом поворота"""
        
        if self.rotation == 0:
            return [
                Point(self.x, self.y),
                Point(self.x + self.width, self.y),
                Point(self.x + self.width, self.y + self.length),
                Point(self.x, self.y + self.length)
            ]
        else:
            # Преобразуем градусы в радианы
            rad = math.radians(self.rotation)
            cos_val = math.cos(rad)
            sin_val = math.sin(rad)
            
            # Центр прямоугольника
            cx = self.x + self.width / 2
            cy = self.y + self.length / 2
            
            # Координаты углов относительно центра
            half_width = self.width / 2
            half_length = self.length / 2
            
            # Применяем поворот к каждому углу
            corners = []
            for dx, dy in [(-half_width, -half_length), 
                           (half_width, -half_length), 
                           (half_width, half_length), 
                           (-half_width, half_length)]:
                x_rotated = cx + dx * cos_val - dy * sin_val
                y_rotated = cy + dx * sin_val + dy * cos_val
                corners.append(Point(x_rotated, y_rotated))
            return corners    
            
    def get_distance(self, obj) -> float:
        """ Получаем дистанцию между двумя объектами """
        
        corners1 = self.get_corners()
        corners2 = obj.get_corners()
        
        min_distance = float('inf')
        for p1 in corners1:
            for p2 in corners2:
                dist = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
                min_distance = min(min_distance, dist)
                
        return min_distance
            
class OpeningObject(BuildingObject):
    """ Класс проёма """
    
    def generate_door_random_placement(self, room: Room, other_obj=[]):
        """ Генерирует случайное расположение проемов """
        # Сделать проще
        
        room_width = room.width
        room_length = room.length
        
        other_side = list(map(lambda x: x.rotation, other_obj))

        self.rotation = random.choice(list(filter(lambda x: x not in other_side, [0, 90, 180, 270])))
       
        if self.name == 'дверь':
            self.width = 60
            self.length = 10
            self.height = 200
        
            if self.rotation == 0:
                self.x = random.choice([30, room.width - self.width - 30])
                self.y = 0
            elif self.rotation == 90:
                self.x = room.width
                self.y = random.choice([30, room.length - self.length - 30])
            elif self.rotation == 180:
                self.x = random.choice([30, room.width - self.width - 30])
                self.y = room.length 
            elif self.rotation == 270:
                self.x = 0
                self.y = random.choice([30, room.length - self.length - 30])
        
        elif self.name == 'окно':
            self.width = 150
            self.length = 10
            self.height = 100
            
            if self.rotation == 0:
                self.x = room.width*0.5 - self.width*0.5
                self.y = 0
            elif self.rotation == 90:
                self.x = room.width
                self.y = room.length*0.5 - self.length
            elif self.rotation == 180:
                self.x = room.width*0.5 - self.width*0.5
                self.y = room.length 
            elif self.rotation == 270:
                self.x = 0
                self.y = room.length*0.5 - self.length
        
    def uturn(self):
        if self.rotation in [90, 270]:
            self.width, self.length = self.length, self.width
            
class FloorObject(BuildingObject):
    """ Класс объекта на полу """
    
    def generate_random_placement(self, other_obj, room):
        """ Генерирует случайное расположение объектов на полу """
        
        self.x = random.uniform(0, room.width - self.width)
        self.y = random.uniform(0, room.length - self.length)
        self.rotation = random.choice([0, 90, 180, 270])
        min_passage = 60
        
        opening_objects = [obj for obj in other_obj if isinstance(obj, OpeningObject)]
        floor_objeects = [obj for obj in other_obj if isinstance(obj, FloorObject)]
        
        # проверки на валидность положкния
        if not room_crossover_check(self, room):
            return False

        if not openings_intersects_check(self, opening_objects):
            return False
            
        for obj in floor_objeects:
            if not intersects_check(self, obj) or distance_check(self, obj, min_passage) < min_passage:
                return False            

        return self 
        
class WallObject(BuildingObject):
    """ Класс объекта на стене """    
    
    # временные заглушки
    def move_wall_object(self) -> None:
        
        if not checks:
            move_wall_object()
            ...
        
    def run_random_placement(self) -> Point:
        ...