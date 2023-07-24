import csv
import logging
import sys
from csv import DictReader

# from datetime import datetime
from django.core.management import BaseCommand

from furniture.models import Furniture, TypeOfRoom

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s, [%(levelname)s] %(message)s')
handler.setFormatter(formatter)


class Command(BaseCommand):
    help = 'Загрузка данных в БД'

    def handle(self, *args, **options):
        logger.info('Удаление данных о мебели в БД')
        Furniture.objects.all().delete()

        logger.info('Загрузка таблицы комнат')
        type_of_rooms = (
            (1, 'спальня', 'bedroom'),
            (2, 'кухня', 'kitchen'),
        )
        result = []
        try:
            with open('data/rooms.csv', encoding='utf-8') as csvfile:
                reader_obj = csv.reader(csvfile)
                for type_of_rooms in reader_obj:
                    result.append(type_of_rooms)
        except Exception as error:
            print(f'Ошибка {error}')
        try:
            if result:
                type_of_rooms = result
            for id_room, name, slug in type_of_rooms:
                data, status = TypeOfRoom.objects.get_or_create(
                    id=id_room,
                    name=name,
                    slug=slug,

                )
            logger.info('типы комнат загружены')
        except Exception as error:
            raise ImportError(
                f'При импорте произошла ошибка {error}')

        logger.info('Загрузка мебели в БД')
        furniture = []
        for row in DictReader(
                open('furniture/data/furniture.csv', encoding='utf-8'),
        ):
            furniture.append(
                Furniture(
                    name=row['name'],
                    name_english=row['name_eng'],
                    length=row['length'],
                    width=row['width'],
                    length_access=row['length_access'],
                    width_access=row['width_access'],
                    power_socket_type=row['power_socket_type'],
                    first_power_socket_height=row['first_power_socket_height'],
                    first_power_socket_width=row['first_power_socket_width'],
                    second_power_socket_height=row['second_power_socket_height'],
                    second_power_socket_width=row['second_power_socket_width'],
                    type_of_rooms=TypeOfRoom.objects.get(
                        id=row['type_of_rooms'],
                    )
                ),
            )
        Furniture.objects.bulk_create(furniture)

        logger.info('Загрузка в БД завершена')
