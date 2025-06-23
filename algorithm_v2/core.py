import itertools

from copy import deepcopy
import random
from typing import List

from sandbox import intersects_check
from objects import (
    Room,
    FloorObject,
    OpeningObject,
    PierGlassZone,
    SleepZone,
    WardrobeZone,
)


class Core:
    """Основной алгоритм"""

    def __init__(self, room_data, openings_data, floor_objects_data):

        self.room_data = room_data
        self.openings_data = openings_data
        self.floor_objects_data = floor_objects_data

        self.min_passage = 60
        self.population_size = 50
        self.generations = 50
        self.mutation_rate = 0.1
        self.max_attemps = 100

        self.floor_objects_data.sort(
            key=lambda x: x["width"] * x["length"], reverse=True
        )

        self.get_room = self.get_room()
        self.get_openings = self.get_openings()
        self.get_floor_objects = self.get_floor_objects()
        self.get_zones = self.get_zones()

    def get_room(self):
        """Создаем объект комнаты"""

        room = Room(
            self.room_data["width"],
            self.room_data["length"],
            self.room_data["height"],
        )
        self.room = room

        return room

    def get_openings(self) -> List[OpeningObject]:
        """Создаем список объектов (проёмов)"""

        openings = []

        names_list = list(map(lambda x: x["name"], self.openings_data))

        # Создаем объекты переданных проёмов если они есть
        for obj in self.openings_data:
            new_obj = OpeningObject(**obj)
            new_obj.get_rotation(self.room)
            openings.append(new_obj)

        # Создаем дверь если её не передали
        if "дверь" not in names_list:
            random_door = OpeningObject(name="дверь")
            random_door.generate_door_random_placement(self.room, openings)
            random_door.uturn()
            openings.append(random_door)

        # Создаем окно если ее не передали
        if "окно" not in names_list:
            random_window = OpeningObject(name="окно")
            random_window.generate_door_random_placement(self.room, openings)
            random_window.uturn()
            openings.append(random_window)

        return openings

    def get_floor_objects(self) -> List[FloorObject]:
        """Создаем объекты на полу"""
        floor_objects = []

        for obj in self.floor_objects_data:
            floor_objects.append(FloorObject(**obj))

        return floor_objects

    def get_zones(self):
        """Создаем зоны комнаты"""

        # создаем списки элементов по уровню
        lvl_1 = list(filter(lambda x: x.lvl == "1", self.get_floor_objects))
        lvl_2 = list(filter(lambda x: x.lvl == "2", self.get_floor_objects))
        # получаем варианты распределения объектов 2 уровня по зонам
        distribution_variants = self.generate_distributions(len(lvl_1), lvl_2)
        # Выбираем случайное распределение
        random_comb = random.choice(distribution_variants)

        zones = []

        for obj in lvl_1:
            if obj.tag == "pz":
                zones.append(PierGlassZone(name="трюмо", main_object=obj))

            elif obj.tag == "sz":
                zones.append(SleepZone(name="спальное место", main_object=obj))

            elif obj.tag == "wz":
                zones.append(WardrobeZone(name="гардеробная", main_object=obj))
        placement_zones = []

        for i in range(len(zones)):
            zones[i].second_objects = random_comb[i]
            attempts = 0
            while attempts < 50:

                zone_copy = deepcopy(zones[i])
                zone_copy.generate_zone()
                zone_copy.placement_zone(self.get_room)

                valid_zone = True
                for obj in placement_zones:
                    if not intersects_check(obj, zone_copy):
                        valid_zone = False
                        attempts += 1
                        break

                for opening in self.get_openings:
                    if not intersects_check(opening, zone_copy):
                        valid_zone = False
                        attempts += 1
                        break

                if valid_zone:
                    placement_zones.append(zone_copy)
                    break

        return placement_zones

    def generate_distributions(self, zones_count, objects):
        """Комбинирует варианты распределения
        второстепенных объектов по количеству зон"""
        results = []

        def recursive_distribute(
            remaining_objects,
            zones_left,
            current_distribution
        ):
            if zones_left == 1:
                # Остальные объекты идут в последнюю зону,
                # если не превышают лимит
                if len(remaining_objects) <= 4:
                    current_distribution.append(remaining_objects)
                    yield current_distribution
                return
            else:
                max_objects_in_zone = min(4, len(remaining_objects))
                # Для первой зоны выбираем возможные количества объектов
                for count in range(1, max_objects_in_zone + 1):
                    # Генерируем все комбинации из remaining_objects по count
                    for combo in itertools.combinations(
                        remaining_objects,
                        count
                    ):
                        remaining = list(remaining_objects)
                        for obj in combo:
                            remaining.remove(obj)
                        # Рекурсия для оставшихся зон
                        for dist in recursive_distribute(
                            remaining,
                            zones_left - 1,
                            current_distribution + [list(combo)],
                        ):
                            yield dist

        # Запускаем рекурсию
        for distribution in recursive_distribute(objects, zones_count, []):
            results.append(distribution)

        return results

    def run_algorithm(self):
        """Основной алгоритм"""

        zones = self.get_zones

        return zones
