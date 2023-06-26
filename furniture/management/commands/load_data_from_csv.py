import logging
import sys
from csv import DictReader

# from datetime import datetime
from django.core.management import BaseCommand

from furniture.models import Furniture

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
                ),
            )
        Furniture.objects.bulk_create(furniture)

        logger.info('Загрузка в БД завершена')
