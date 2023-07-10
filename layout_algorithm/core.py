from algorithm import *
from corner_markings import corner_markings
from layout_algorithm import create_picture


class Core(FurnitureArrangement):
    def algorithm_activation(self, doors_and_windows: list, furniture: list, room_size: dict):
        """Основная функция алгоритма, проходящаяся по всему заданному списку мебели
        и расставляющая каждую единицу внутри помещения

        Args:
            doors_and_windows:
            furniture:
            room_size:
        Returns:

        """

        self.data_preprocessing(room_size, doors_and_windows)
        for item in furniture:
            result_free_space = self.free_space_algorithm(self.coordinates)
            result_middle_distance = self.middle_and_shift(result_free_space)
            result_wall_definition = self.wall_definition(result_middle_distance)
            result_corner_markings = corner_markings(item, result_middle_distance, result_wall_definition)
            self.placing_in_coordinates(result_middle_distance, result_corner_markings, room_size, item)

        # функции для возможности наглядного тестирования результата до отправки на фронт
        create_picture.create_rectangles(self.coordinates, self.room_coordinates)
        print(self.coordinates)
