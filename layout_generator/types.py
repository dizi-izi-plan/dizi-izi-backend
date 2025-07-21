from typing import Literal

from pydantic import BaseModel


class _Door(BaseModel):
    width: int
    wall: Literal[0, 1, 2, 3]
    x_center: int
    open_direction: Literal["inside_left", "inside_right", "outside_left", "outside_right"]


class _Window(BaseModel):
    width: int
    height: int
    wall: Literal[0, 1, 2, 3]
    x_center: int


class _Balcony(BaseModel):
    width: int
    wall: Literal[0, 1, 2, 3]
    x_center: int


class _RoomDescription(BaseModel):
    type_id: str
    length: int
    width: int
    doors: list[_Door]
    windows: list[_Window]
    balconies: list[_Balcony]


class GenerateLayoutRequest(BaseModel):
    """Describes the input format for the generate_layout method.

    Example:
    ```
    {
        "room_description": {
            "type_id": "bedroom",
            "length": 100,
            "width": 200,
            "doors": [
                {
                    "width": 10,
                    "wall": 0,
                    "x_center": 50,
                    "open_direction": "inside_left"
                }
            ],
            "windows": [
                {
                    "width": 10,
                    "height": 10,
                    "wall": 2,
                    "x_center": 2
                }
            ],
            "balconies": [
                {
                    "width": 20,
                    "wall": 2,
                    "x_center": 2
                }
            ]
        },
        "furniture_item_ids": ["bed_01", "desk_02", "chair_03"]
    }
    ```
    """
    room_description: _RoomDescription
    furniture_item_ids: list[str]


TaskStatus = Literal["PENDING", "IN_PROGRESS", "FAILURE", "SUCCESS"]


class _FurniturePlacement(BaseModel):
    furniture_item_id: str
    x_center: int
    y_center: int
    rotation_degree: int


class GenerateLayoutResult(BaseModel):
    """
    Describes the output format for the get_task_results method.

    Example::

        {
            "id": "task_123",
            "furniture_placements": [
                {
                    "furniture_item_id": "bed_01",
                    "x_center": 2,
                    "y_center": 3,
                    "rotation_degree": 90
                },
                {
                    "furniture_item_id": "desk_02",
                    "x_center": 4,
                    "y_center": 1,
                    "rotation_degree": 0
                }
            ]
        }
    """

    id: str
    furniture_placements: list[_FurniturePlacement]


# TODO: add ErrorCodes enum
