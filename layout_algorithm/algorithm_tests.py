import unittest

from core import Core


class TestFurnitureArrangement(unittest.TestCase):
    def setUp(self):
        self.calculator = Core()



    def test_algorithm_activation_1(self):
        self.calculator.algorithm_activation(
            [
                {
                    "north_west": {"x": 4, "y": 10},
                    "north_east": {"x": 7, "y": 10},
                    "south_west": {"x": 4, "y": 9},
                    "south_east": {"x": 7, "y": 9},
                },
                {
                    "north_west": {"x": 14, "y": 0},
                    "north_east": {"x": 12, "y": 0},
                    "south_west": {"x": 14, "y": 4},
                    "south_east": {"x": 12, "y": 4},
                },
            ],
            [{"width": 2, "length": 3},
             {"width": 3, "length": 1}],
            {
                "first_wall": 10,
                "second_wall": 14,
                "third_wall": 10,
                "fourth_wall": 14,
            },
        )

    def test_algorithm_activation_2(self):
        self.calculator.algorithm_activation(
            [
                {
                    "north_west": {"x": 4, "y": 10},
                    "north_east": {"x": 7, "y": 10},
                    "south_west": {"x": 4, "y": 9},
                    "south_east": {"x": 7, "y": 9},
                },
                {
                    "north_west": {"x": 14, "y": 0},
                    "north_east": {"x": 12, "y": 0},
                    "south_west": {"x": 14, "y": 4},
                    "south_east": {"x": 12, "y": 4},
                },
            ],
            [{"width": 4, "length": 6},
             {"width": 3, "length": 2}],
            {
                "first_wall": 10,
                "second_wall": 14,
                "third_wall": 10,
                "fourth_wall": 14,
            },
        )

    def test_algorithm_activation_3(self):
        self.calculator.algorithm_activation(
            [
                {
                    "north_west": {"x": 4, "y": 10},
                    "north_east": {"x": 7, "y": 10},
                    "south_west": {"x": 4, "y": 9},
                    "south_east": {"x": 7, "y": 9},
                },
                {
                    "north_west": {"x": 14, "y": 0},
                    "north_east": {"x": 12, "y": 0},
                    "south_west": {"x": 14, "y": 4},
                    "south_east": {"x": 12, "y": 4},
                },
            ],
            [
                {"width": 1, "length": 1},
                {"width": 2, "length": 1},
                {"width": 1, "length": 1},
                {"width": 3, "length": 1},
            ],
            {
                "first_wall": 10,
                "second_wall": 14,
                "third_wall": 10,
                "fourth_wall": 14,
            },
        )

    def test_algorithm_activation_4(self):
        self.calculator.algorithm_activation(
            [
                {
                    "north_west": {"x": 4, "y": 10},
                    "north_east": {"x": 7, "y": 10},
                    "south_west": {"x": 4, "y": 9},
                    "south_east": {"x": 7, "y": 9},
                },
                {
                    "north_west": {"x": 14, "y": 0},
                    "north_east": {"x": 12, "y": 0},
                    "south_west": {"x": 14, "y": 4},
                    "south_east": {"x": 12, "y": 4},
                },
            ],
            [
                {"width": 4, "length": 1},
                {"width": 1, "length": 6},
                {"width": 3, "length": 3},
                {"width": 1, "length": 1},
            ],
            {
                "first_wall": 10,
                "second_wall": 14,
                "third_wall": 10,
                "fourth_wall": 14,
            },
        )

    def test_algorithm_activation_5(self):
        self.calculator.algorithm_activation(
            [
                {
                    "north_west": {"x": 4, "y": 10},
                    "north_east": {"x": 7, "y": 10},
                    "south_west": {"x": 4, "y": 9},
                    "south_east": {"x": 7, "y": 9},
                },
                {
                    "north_west": {"x": 14, "y": 0},
                    "north_east": {"x": 12, "y": 0},
                    "south_west": {"x": 14, "y": 4},
                    "south_east": {"x": 12, "y": 4},
                },
            ],
            [{"width": 5, "length": 1}],
            {
                "first_wall": 10,
                "second_wall": 14,
                "third_wall": 10,
                "fourth_wall": 14,
            },
        )

    def test_algorithm_activation_6(self):
        self.calculator.algorithm_activation(
            [
                {
                    "north_west": {"x": 0, "y": 250},
                    "north_east": {"x": 0, "y": 750},
                    "south_west": {"x": 500, "y": 250},
                    "south_east": {"x": 500, "y": 750},
                },

            ],
            [{"width": 1800, "length": 2000},
             {"width": 1200, "length": 1200}
             ],
            {
                "first_wall": 10000,
                "second_wall": 12000,
                "third_wall": 10000,
                "fourth_wall": 12000,
            },
        )
