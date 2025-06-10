import random
from copy import deepcopy
from dataclasses import dataclass
from typing import List

from objects import FloorObject, OpeningObject, Room, WallObject
from sandbox import (intersects_check, openings_intersects_check,
                     room_crossover_check)


class Core:
    """Основной алгоритм"""

    def __init__(self, room_data, openings_data, floor_objects_data, wall_objects_data):
        self.room_data = room_data
        self.openings_data = openings_data
        self.floor_objects_data = floor_objects_data
        self.wall_objects_data = wall_objects_data

        self.min_passage = 60
        self.population_size = 50
        self.generations = 50
        self.mutation_rate = 0.1
        self.max_attemps = 100

        self.floor_objects_data.sort(key=lambda x: x['width'] * x['length'], reverse=True)

        self.get_room = self.get_room()
        self.get_openings = self.get_openings()
        self.get_floor_objects = self.run_genetic_algorithm()

    def get_room(self):
        """Создаем объект комнаты"""
        room = Room(
            self.room_data['width'],
            self.room_data['length'],
            self.room_data['height'],
        )
        self.room = room
        return room

    def get_openings(self) -> List[OpeningObject]:
        """Создаем список объектов (проёмов)"""
        openings = []

        names_list = list(map(lambda x: x['name'], self.openings_data))

        # Создаем объекты переданных проёмов, если они есть
        for obj in self.openings_data:
            new_obj = OpeningObject(**obj)
            new_obj.uturn()
            openings.append(new_obj)

        # Создаем дверь, если её не передали
        if 'дверь' not in names_list:
            random_door = OpeningObject(name='дверь')
            random_door.generate_door_random_placement(self.room, openings)
            random_door.uturn()
            openings.append(random_door)

        # Создаем окно, если его не передали
        if 'окно' not in names_list:
            random_window = OpeningObject(name='окно')
            random_window.generate_door_random_placement(self.room, openings)
            random_window.uturn()
            openings.append(random_window)

        return openings

    def get_floor_objects(self) -> List[FloorObject]:
        """Создаем объекты на полу"""
        floor_objects = []

        for obj in self.floor_objects_data:
            for _ in range(self.max_attemps):
                new_obj = FloorObject(**obj)
                new_obj_placement = new_obj.generate_random_placement(self.get_openings() + floor_objects, self.room)
                if new_obj_placement:
                    floor_objects.append(new_obj_placement)
                    break

        return floor_objects

    def get_wall_objects(self) -> List[WallObject]:
        """Создаем объекты на стене"""
        wall_objects = []
        for obj in self.wall_objects_data:
            new_obj = WallObject(**obj)
            new_obj_placement = new_obj.run_random_placement(self.get_openings(), self.room)
            wall_objects.append(new_obj_placement)

        return wall_objects

    def evaluate_placement(self, placement) -> float:
        """Оценивает качество размещения мебели"""
        if len(placement) < len(self.floor_objects_data):
            # Штраф за неразмещённые предметы
            return -1000 * (len(self.floor_objects_data) - len(placement))

        score = 0
        # Оцениваем расстояние между предметами (больше — лучше, но не слишком)
        for i in range(len(placement)):
            for j in range(i + 1, len(placement)):
                distance = placement[i].get_distance(placement[j])
                if distance < 60:
                    score -= 100  # Штраф за слишком близкое расположение
                else:
                    # Оптимальное расстояние — около 80-100 см
                    optimal_distance = 90
                    score -= abs(distance - optimal_distance) * 0.5

        return score

    def crossover(self, parent1, parent2):
        """Скрещивает два размещения мебели для создания нового"""
        # Создаем словарь для быстрого доступа к предметам по ID
        parent1_dict = {item.id: item for item in parent1}
        parent2_dict = {item.id: item for item in parent2}
        child = []

        # Для каждого предмета мебели
        for item in self.floor_objects_data:
            # Выбираем размещение из одного из родителей
            if item['id'] in parent1_dict and item['id'] in parent2_dict:
                # Если предмет есть у обоих родителей, выбираем случайно
                source = parent1_dict if random.random() < 0.5 else parent2_dict
                placement = deepcopy(source[item['id']])
            elif item['id'] in parent1_dict:
                placement = deepcopy(parent1_dict[item['id']])
            elif item['id'] in parent2_dict:
                placement = deepcopy(parent2_dict[item['id']])
            else:
                # Если предмета нет ни у одного из родителей, пропускаем
                continue

            # Проверяем, что мебель не пересекается с уже размещенной мебелью
            valid_placement = True
            for obj in child:
                if not intersects_check(obj, placement) or obj.get_distance(placement) < self.min_passage:
                    valid_placement = False
                    break

            if valid_placement:
                child.append(placement)

        return child

    def mutate(self, placement):
        """Мутирует размещение мебели"""
        if not placement:
            return placement
        # Создаем копию размещения
        mutated = [deepcopy(item) for item in placement]
        # Выбираем случайный предмет для мутации
        item_index = random.randint(0, len(mutated) - 1)
        item = mutated[item_index]
        # Определяем тип мутации
        mutation_type = random.choice(['position', 'rotation'])

        if mutation_type == 'position':
            # Изменяем позицию предмета
            max_shift = min(50, self.room.width * 0.1, self.room.length * 0.1)
            dx = random.uniform(-max_shift, max_shift)
            dy = random.uniform(-max_shift, max_shift)

            item.x = max(0, min(self.room.width - item.width, item.x + dx))
            item.y = max(0, min(self.room.length - item.height, item.y + dy))

        elif mutation_type == 'rotation':
            # Изменяем поворот предмета
            new_rotation = random.choice([0, 90, 180, 270])

            # Если поворот изменился на 90 или 270 градусов, меняем местами ширину и высоту
            if (item.rotation in [0, 180] and new_rotation in [90, 270]) or \
                    (item.rotation in [90, 270] and new_rotation in [0, 180]):
                item.width, item.height = item.height, item.width

            item.rotation = new_rotation

            # Убеждаемся, что предмет остается внутри комнаты
            item.x = max(0, min(self.room.width - item.width, item.x))
            item.y = max(0, min(self.room.length - item.height, item.y))

        # Проверяем, что после мутации размещение остается валидным
        valid_placement = True

        # Проверяем пересечения с дверями, окнами и фиксированными элементами
        if not openings_intersects_check(item, self.get_openings):
            valid_placement = False

        # Проверяем пересечения с другими предметами мебели
        if valid_placement:
            for obj in mutated:
                if obj.id == str(item_index):
                    continue
                if not intersects_check(obj, item) or obj.get_distance(item) < self.min_passage:
                    valid_placement = False
                    break

        # Если мутация привела к невалидному размещению, возвращаем исходное
        if not valid_placement:
            return placement

        return mutated

    def greedy_placement(self, placement):
        """Жадный алгоритм размещения мебели (запасной вариант)"""
        items_id = map(lambda x: x.id, placement)  # Получаем id объектов в популяции
        missing_objects = []

        # Ищем отсутствующие объекты и создаем их
        for obj in self.floor_objects_data:
            if obj['id'] not in list(items_id):
                missing_objects.append(FloorObject(**obj))

        # Создаем сетку возможных позиций
        grid_step = 10  # шаг сетки в см
        possible_positions = []

        for x in range(0, int(self.room.width), grid_step):
            for y in range(0, int(self.room.length), grid_step):
                possible_positions.append((x, y))

        # Для каждого отсутствующего предмета мебели
        for obj in missing_objects:
            # Перебираем все возможные позиции и повороты
            for x, y in possible_positions:
                for rotation in [0, 90, 180, 270]:
                    obj.x = x
                    obj.y = y

                    # Проверяем, что объект в границах комнаты
                    if not room_crossover_check(obj, self.room):
                        continue

                    # Проверяем, что объект не пересекается с уже размещенной мебелью
                    valid_placement = True
                    for placed_obj in placement:
                        if not intersects_check(obj, placed_obj) or obj.get_distance(placed_obj) < self.min_passage:
                            valid_placement = False
                            break

                    if not valid_placement:
                        continue

            if valid_placement:
                placement.append(obj)

        return placement

    def run_genetic_algorithm(self):
        population = []

        for _ in range(self.population_size):
            floor_obj_placement = self.get_floor_objects()
            population.append(floor_obj_placement)

        best_placement = None
        best_score = float('-inf')

        # Основной цикл генетического алгоритма
        for generation in range(self.generations):
            # Оцениваем каждое размещение
            scores = [self.evaluate_placement(placement) for placement in population]

            # Находим лучшее размещение
            max_score_index = scores.index(max(scores))
            current_best = population[max_score_index]
            current_best_score = scores[max_score_index]

            if current_best_score > best_score:
                best_placement = current_best
                best_score = current_best_score

            # Выбираем родителей для следующего поколения (турнирный отбор)
            new_population = [current_best]  # Элитизм — сохраняем лучшее решение

            while len(new_population) < self.population_size:
                # Выбираем двух родителей
                tournament_size = 3
                parent1_idx = max(
                    random.sample(range(len(population)), tournament_size),
                    key=lambda i: scores[i]
                )
                parent2_idx = max(
                    random.sample(range(len(population)), tournament_size),
                    key=lambda i: scores[i]
                )

                parent1 = population[parent1_idx]
                parent2 = population[parent2_idx]

                # Скрещиваем родителей
                child = self.crossover(parent1, parent2)

                # Применяем мутацию с определенной вероятностью
                if random.random() < self.mutation_rate:
                    child = self.mutate(child)

                new_population.append(child)

            # Заменяем старую популяцию новой
            population = new_population

        return best_placement
