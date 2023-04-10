import unittest
from algorithm import FurnitureArrangement


class TestFurnitureArrangement(unittest.TestCase):

    def setUp(self):
        self.calculator = FurnitureArrangement()

    def test_double_free_space_algorithm(self):
        self.assertEqual(self.calculator.free_space_algorithm(
            [{"south_east": {"x": 6, "y": 4}, "south_west": {"x": 8, "y": 4},
              "north_east": {"x": 6, "y": 2}, "north_west": {"x": 8, "y": 2}},
             {"south_east": {"x": 2, "y": 4}, "south_west": {"x": 4, "y": 4},
              "north_east": {"x": 2, "y": 2}, "north_west": {"x": 4, "y": 2}}]),
            ({'left_corner': {'x': 2, 'y': 2}}, {'right_corner': {'x': 8, 'y': 2}}))

    def test_triple_free_space_algorithm(self):
        self.assertEqual(self.calculator.free_space_algorithm(
            [{"south_east": {"x": 6, "y": 4}, "south_west": {"x": 8, "y": 4},
              "north_east": {"x": 6, "y": 2}, "north_west": {"x": 8, "y": 2}},
             {"south_east": {"x": 2, "y": 4}, "south_west": {"x": 4, "y": 4},
              "north_east": {"x": 2, "y": 2}, "north_west": {"x": 4, "y": 2}},
             {"south_east": {"x": 7, "y": 6}, "south_west": {"x": 5, "y": 6},
              "north_east": {"x": 7, "y": 8}, "north_west": {"x": 5, "y": 8}}
             ]),
            ({'left_corner': {'x': 2, 'y': 2}}, {'right_corner': {'x': 5, 'y': 8}}))

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
