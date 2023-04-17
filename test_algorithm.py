import unittest
from unittest import TestCase

from algorithm import FurnitureArrangement


class TestFurnitureArrangement(unittest.TestCase):

    def setUp(self):
        self.calculator = FurnitureArrangement()

    def test_double_free_space_algorithm(self):
        self.assertEqual(self.calculator.free_space_algorithm(
            [{"south_east": {"x": 2, "y": 0}, "south_west": {"x": 0, "y": 0},
              "north_east": {"x": 2, "y": 3}, "north_west": {"x": 0, "y": 3},
              "wall_info": {"wall_number": 4, "wall_length": 5}},
             {"south_east": {"x": 5, "y": 0}, "south_west": {"x": 3, "y": 0},
              "north_east": {"x": 5, "y": 3}, "north_west": {"x": 3, "y": 3},
              "wall_info": {"wall_number": 4, "wall_length": 5}}],
            {"walls_length": {"first_wall": 3, "second_wall": 5, "third_wall": 3, "fourth_wall": 5}}),
            ({'left_corner': {'x': 5, 'y': 3}, 'right_corner': {'x': 0, 'y': 3}},
             {"walls_length": {"first_wall": 3, "second_wall": 5, "third_wall": 3, "fourth_wall": 5}}))

    def test_triple_free_space_algorithm(self):
        self.assertEqual(self.calculator.free_space_algorithm(
            [{"south_east": {"x": 6, "y": 4}, "south_west": {"x": 8, "y": 4},
              "north_east": {"x": 6, "y": 2}, "north_west": {"x": 8, "y": 2},
              "wall_info": {"wall_number": 2, "wall_length": 6}},
             {"south_east": {"x": 2, "y": 4}, "south_west": {"x": 4, "y": 4},
              "north_east": {"x": 2, "y": 2}, "north_west": {"x": 4, "y": 2},
              "wall_info": {"wall_number": 2, "wall_length": 6}},
             {"south_east": {"x": 7, "y": 6}, "south_west": {"x": 5, "y": 6},
              "north_east": {"x": 7, "y": 8}, "north_west": {"x": 5, "y": 8},
              "wall_info": {"wall_number": 4, "wall_length": 6}}],
            {"walls_length": {"first_wall": 6, "second_wall": 6, "third_wall": 6, "fourth_wall": 6}}),
            ({'left_corner': {'x': 2, 'y': 2}, 'right_corner': {'x': 5, 'y': 8}},
             {"walls_length": {"first_wall": 6, "second_wall": 6, "third_wall": 6, "fourth_wall": 6}}))

    def test_middle_of_the_distance_on_the_wall(self):
        self.assertEqual(self.calculator.middle_of_the_distance_on_the_wall(
            {'left_corner': {'x': 0, 'y': 4}, 'right_corner': {'x': 10, 'y': 4}},
            {"first_wall": 4, "second_wall": 10, "third_wall": 4, "fourth_wall": 10}), {'x': 5, 'y': 4})
        self.assertEqual(self.calculator.middle_of_the_distance_on_the_wall(
            {'left_corner': {'x': 0, 'y': 4}, 'right_corner': {'x': 8, 'y': 0}},
            {"first_wall": 4, "second_wall": 10, "third_wall": 4, "fourth_wall": 10}), {'x': 8, 'y': 4})
        self.assertEqual(self.calculator.middle_of_the_distance_on_the_wall(
            {'left_corner': {'x': 2, 'y': 0}, 'right_corner': {'x': 0, 'y': 4}},
            {"first_wall": 4, "second_wall": 10, "third_wall": 4, "fourth_wall": 10}), {'x': 0, 'y': 1})
        self.assertEqual(self.calculator.middle_of_the_distance_on_the_wall(
            {'left_corner': {'x': 2, 'y': 0}, 'right_corner': {'x': 4, 'y': 0}},
            {"first_wall": 4, "second_wall": 10, "third_wall": 4, "fourth_wall": 10}), {'x': 7, 'y': 4})

    def test_corner_markings_first_wall(self):
        self.assertEqual(self.calculator.corner_markings({"length": 4, "width": 6}, {"x": 3, "y": 4}, 1),
                         {"north_west": {"x": 3, "y": 1}, "north_east": {"x": 3, "y": 7},
                          "south_west": {"x": 7, "y": 1}, "south_east": {"x": 7, "y": 7}})

    def test_corner_markings_second_wall(self):
        self.assertEqual(self.calculator.corner_markings({"length": 4, "width": 6}, {"x": 5, "y": 6}, 2),
                         {"north_west": {"x": 2, "y": 6}, "north_east": {"x": 8, "y": 6},
                          "south_west": {"x": 2, "y": 2}, "south_east": {"x": 8, "y": 2}})

    def test_corner_markings_third_wall(self):
        self.assertEqual(self.calculator.corner_markings({"length": 4, "width": 6}, {"x": 7, "y": 4}, 3),
                         {"north_west": {"x": 7, "y": 7}, "north_east": {"x": 7, "y": 1},
                          "south_west": {"x": 3, "y": 7}, "south_east": {"x": 3, "y": 1}})

    def test_corner_markings_fourth_wall(self):
        self.assertEqual(self.calculator.corner_markings({"length": 4, "width": 6}, {"x": 5, "y": 2}, 4),
                         {"north_west": {"x": 8, "y": 2}, "north_east": {"x": 2, "y": 2},
                          "south_west": {"x": 8, "y": 6}, "south_east": {"x": 2, "y": 6}})

    def test_placing_in_coordinates(self):
        # middle_point (dict): {"x": 0, "y": 0}
        # figure (dict): координаты для мебели. {"north_west": {"x": 0, "y": 0}, "north_east": {"x": 0, "y": 0},
        #                                        "south_west": {"x": 0, "y": 0}, "south_east": {"x": 0, "y": 0}}
        # walls (dict): стены комнаты начиная от левой {"first_wall": 0, "second_wall": 0,
        #                                               "third_wall": 0, "fourth_wall":0}
        # objects (dict): словарь с координатами других объектов в комнате

        self.assertEqual(self.calculator.placing_in_coordinates({"x": 1.5, "y": 3},
                                                                {"north_west": {"x": 1, "y": 3},
                                                                 "north_east": {"x": 2, "y": 3},
                                                                 "south_west": {"x": 1, "y": 2},
                                                                 "south_east": {"x": 2, "y": 2}},
                                                                {"first_wall": 3, "second_wall": 3,
                                                                 "third_wall": 3, "fourth_wall": 3},
                                                                ({"north_west": {"x": 1, "y": 3},
                                                                  "north_east": {"x": 3, "y": 3},
                                                                  "south_west": {"x": 1, "y": 2},
                                                                  "south_east": {"x": 3, "y": 2}},
                                                                 {"north_west": {"x": 2, "y": 0.5},
                                                                  "north_east": {"x": 3, "y": 0.5},
                                                                  "south_west": {"x": 2, "y": 0},
                                                                  "south_east": {"x": 3, "y": 0}})
                                                                ), True)

        self.assertEqual(self.calculator.placing_in_coordinates({"x": 1.5, "y": 3},
                                                                {"north_west": {"x": 1, "y": 3},
                                                                 "north_east": {"x": 2, "y": 3},
                                                                 "south_west": {"x": 1, "y": 2},
                                                                 "south_east": {"x": 2, "y": 2}},
                                                                {"first_wall": 3, "second_wall": 3,
                                                                 "third_wall": 3, "fourth_wall": 3},
                                                                ({"north_west": {"x": 1, "y": 3},
                                                                  "north_east": {"x": 3, "y": 3},
                                                                  "south_west": {"x": 1, "y": 2},
                                                                  "south_east": {"x": 3, "y": 2}},
                                                                 {"north_west": {"x": 0, "y": 2.5},
                                                                  "north_east": {"x": 3, "y": 2.5},
                                                                  "south_west": {"x": 0, "y": 0},
                                                                  "south_east": {"x": 3, "y": 0}})
                                                                ), False)
