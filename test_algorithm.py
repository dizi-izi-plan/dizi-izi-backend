import unittest
from algorithm import FurnitureArrangement


class TestFurnitureArrangement(unittest.TestCase):

    def setUp(self):
        self.calculator = FurnitureArrangement()

    def test_double_free_space_algorithm(self):
        self.assertEqual(self.calculator.free_space_algorithm(
            [{"south_east": {"x": 2, "y": 0}, "south_west": {"x": 0, "y": 0},
            "north_east": {"x": 2, "y": 3}, "north_west": {"x": 0, "y": 3}},
            {"south_east": {"x": 5, "y": 0}, "south_west": {"x": 3, "y": 0},
            "north_east": {"x": 5, "y": 3}, "north_west": {"x": 3, "y": 3}},]),
            ({'North_east': {'x': 5, 'y': 3}}, {'North_west': {'x': 0, 'y': 3}}))

    def test_triple_free_space_algorithm(self):
        self.assertEqual(self.calculator.free_space_algorithm(
            [{"south_east": {"x": 2, "y": 0}, "south_west": {"x": 0, "y": 0},
              "north_east": {"x": 2, "y": 3}, "north_west": {"x": 0, "y": 3}},
             {"south_east": {"x": 5, "y": 0}, "south_west": {"x": 3, "y": 0},
              "north_east": {"x": 5, "y": 3}, "north_west": {"x": 3, "y": 3}},
             {"south_east": {"x": 8, "y": 0}, "south_west": {"x": 10, "y": 0},
              "north_east": {"x": 8, "y": 3}, "north_west": {"x": 10, "y": 3}}
             ]),({'North_east': {'x': 8, 'y': 3}}, {'North_west': {'x': 0, 'y': 3}}))
