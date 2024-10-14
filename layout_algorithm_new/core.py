import bisect
from .main_functions import FurnitureArrangement
from .create_picture import create_rectangles
from .offset_finder_convert import MiddlePointAndShift

from .room import Room
from .furniture import Furniture


class Core(MiddlePointAndShift):
    def algorithm_activation(
        self, doors_and_windows: list, furniture: list, room_size: dict,
    ):
        """Основная функция алгоритма, проходящаяся по всему заданному списку
        мебели и расставляющая каждую единицу внутри помещения

        Args:
            doors_and_windows:
            furniture:
            room_size:
        Returns:

        """

        print(furniture)
        room = Room(room_size, doors_and_windows)
        algorithm = FurnitureArrangement(room)

        for item, item2 in enumerate(furniture):
            result_free_space = algorithm.free_space_algorithm(room.room_objects_coordinates)
            result_middle_distance = self.middle_point_finder(
                result_free_space, room.wall_perimetr, room.walls_length,
            )
            result_wall_definition = room.wall_definition(
                result_middle_distance,
            )
            result_corner_markings = Furniture.corner_markings(
                item2, result_middle_distance, result_wall_definition,
            )
            final_point, figure = algorithm.placing_in_coordinates(
                result_middle_distance,
                result_corner_markings,
                room_size,
                item2,
            )

            # добавляем конечные значения в соответствии их расположением по стенам
            furniture[item]["adjacent_center_point"] = final_point
            bisect.insort(room.sorted_points, final_point)
            room.room_objects_coordinates.insert(
                room.sorted_points.index(final_point), figure,
            )

        powersocets = []
        # добавление разеток к каждой мебели
        # for item in furniture:
        #     if item["first_power_socket_width"] != 0:
        #         item["first_power_socket_placement"] = (
        #             item["adjacent_center_point"]
        #             + item["first_power_socket_width"]
        #         )
        #         powersocets.append(
        #             self.convert_line_to_coordinates(
        #                 item["first_power_socket_placement"],
        #                 room.walls_length,
        #                 room.wall_perimetr,
        #             ),
        #         )
        #     if item["second_power_socket_width"] != 0:
        #         item["second_power_socket_placement"] = (
        #             item["adjacent_center_point"]
        #             + item["second_power_socket_width"]
        #         )
        #         powersocets.append(
        #             self.convert_line_to_coordinates(
        #                 item["second_power_socket_placement"],
        #                 room.walls_length,
        #                 room.wall_perimetr,
        #             ),
        #         )

        # функции для возможности наглядного тестирования результата до
        # отправки на фронт
        create_rectangles(room.room_objects_coordinates, room.room_coordinates, powersocets)
