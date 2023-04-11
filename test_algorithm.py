import unittest
from algorithm import FurnitureArrangement, Figure


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
        
    def test_placing_in_coordinates(self):
        room_width = 5.0
        room_height = 5.0
        
        furniture_width = 1.0
        furniture_height = 1.0
        
        figure = Figure(side_b=furniture_width, side_a=furniture_height, side_c=room_width, side_d=room_height)
        
        initial_coordinates = {
        "Furniture_1": {"corners": {
            "north_west": {"x": 0.0, "y": 0.0},
            "north_east": {"x": 0.0, "y": 1.0},
            "south_west": {"x": 1.0, "y": 0.0},
            "south_east": {"x": 1.0, "y": 1.0}
        }}
    }

    def test_triple_free_space_algorithm(self):
        self.assertEqual(self.calculator.free_space_algorithm(
            [{"south_east": {"x": 2, "y": 0}, "south_west": {"x": 0, "y": 0},
              "north_east": {"x": 2, "y": 3}, "north_west": {"x": 0, "y": 3}},
             {"south_east": {"x": 5, "y": 0}, "south_west": {"x": 3, "y": 0},
              "north_east": {"x": 5, "y": 3}, "north_west": {"x": 3, "y": 3}},
             {"south_east": {"x": 8, "y": 0}, "south_west": {"x": 10, "y": 0},
              "north_east": {"x": 8, "y": 3}, "north_west": {"x": 10, "y": 3}}
             ]),({'North_east': {'x': 8, 'y': 3}}, {'North_west': {'x': 0, 'y': 3}}))

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
