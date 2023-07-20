
import bisect
from .corner_markings import corner_markings
from .main_functions import FurnitureArrangement
from .create_picture import create_rectangles
from .offset_finder_convert import MiddlePointAndShift


class Core(FurnitureArrangement, MiddlePointAndShift):
    def algorithm_activation(self, doors_and_windows: list, furniture: list, room_size: dict):
        """Основная функция алгоритма, проходящаяся по всему заданному списку мебели
        и расставляющая каждую единицу внутри помещения

        Args:
            doors_and_windows:
            furniture:
            room_size:
        Returns:

        """

        print(furniture)
        self.data_preprocessing(room_size, doors_and_windows)
        for item, item2 in enumerate(furniture):
            result_free_space = self.free_space_algorithm(self.coordinates)
            result_middle_distance = self.middle_point_finder(result_free_space, self.wall_perimetr, self.walls_length)
            result_wall_definition = self.wall_definition(result_middle_distance)
            result_corner_markings = corner_markings(item2, result_middle_distance, result_wall_definition)
            final_point, figure = self.placing_in_coordinates(result_middle_distance, result_corner_markings, room_size, item2)
            
            # добавляем конечные значения в соответствии их расположением по стенам
            furniture[item]["adjacent_center_point"] = final_point 
            # print(furniture[item])
            bisect.insort(self.sorted_points, final_point)
            self.coordinates.insert(self.sorted_points.index(final_point), figure)
        
        powersocets = []
        # добавление разеток к каждой мебели
        for item in furniture:
            if item['first_power_socket_width'] != 0:
                item['first_power_socket_placement'] = \
                item['adjacent_center_point'] + item['first_power_socket_width']
                print(item['first_power_socket_placement'])
                powersocets.append(self.convert_line_to_coordinates(item['first_power_socket_placement'], self.walls_length, self.wall_perimetr))
                
            if item['second_power_socket_width'] != 0:
                item['second_power_socket_placement'] = \
                item['adjacent_center_point'] + item['second_power_socket_width']
                powersocets.append(self.convert_line_to_coordinates(item['second_power_socket_placement'], self.walls_length, self.wall_perimetr))
        
        # функции для возможности наглядного тестирования результата до отправки на фронт
        # print(self.coordinates)
        create_rectangles(self.coordinates, self.room_coordinates, powersocets)