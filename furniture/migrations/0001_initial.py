# Generated by Django 5.0.7 on 2025-03-14 20:02

import django.contrib.gis.db.models.fields
import django.db.models.deletion
import furniture.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Наименование мебели')),
                ('name_eng', models.CharField(max_length=128, verbose_name='Наименование мебели на английском языке')),
                ('depth', models.PositiveIntegerField(help_text='Глубина в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Глубина мебели')),
                ('width', models.PositiveIntegerField(help_text='Ширина в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Ширина мебели')),
                ('depth_with_access_zone', models.PositiveIntegerField(help_text='Глубина c зоной подхода в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Глубина мебели c зоной подхода')),
                ('width_with_access_zone', models.PositiveIntegerField(help_text='Ширина c зоной подхода в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Ширина мебели c зоной подхода')),
                ('image', models.ImageField(blank=True, null=True, upload_to='furniture/', verbose_name='Изображение мебели')),
            ],
            options={
                'verbose_name': 'Мебель',
                'verbose_name_plural': 'Мебель',
            },
        ),
        migrations.CreateModel(
            name='PowerSocket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('socket_type', models.CharField(max_length=128, verbose_name='Тип электроточки')),
                ('height', models.PositiveIntegerField(default=0, verbose_name='Высота электроточки')),
                ('width', models.PositiveIntegerField(default=0, verbose_name='Ширина электроточки')),
                ('power_socket_image', models.ImageField(blank=True, null=True, upload_to='power_sockets/', verbose_name='Изображение электроточки')),
            ],
            options={
                'verbose_name': 'Электроточка',
                'verbose_name_plural': 'Электроточки',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Наименование комнаты')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название комнаты')),
                ('width', models.PositiveIntegerField(help_text='Ширина комнаты в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Ширина комнаты')),
                ('length', models.PositiveIntegerField(help_text='Длина комнаты в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Длина комнаты')),
                ('boundary', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=0, verbose_name='Границы комнаты')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комната',
                'verbose_name_plural': 'Комнаты',
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='DoorPlacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shape', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=0, verbose_name='Координаты объекта')),
                ('width', models.PositiveIntegerField(help_text='Ширина в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Ширина двери')),
                ('height', models.PositiveIntegerField(help_text='Высота в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Высота двери')),
                ('open_direction', models.CharField(choices=[('inside_left', 'Внутрь влево'), ('inside_right', 'Внутрь вправо'), ('outside_left', 'Наружу влево'), ('outside_right', 'Наружу вправо')], help_text='Как открывается дверь', verbose_name='Направление открытия двери')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='furniture.room', verbose_name='Комната')),
            ],
            options={
                'verbose_name': 'Дверь в помещении',
                'verbose_name_plural': 'Двери в помещении',
            },
        ),
        migrations.CreateModel(
            name='RoomLayout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название планировки')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата и время создания')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='layouts', to='furniture.room', verbose_name='Комната')),
            ],
            options={
                'verbose_name': 'Планировка',
                'verbose_name_plural': 'Планировки',
            },
        ),
        migrations.CreateModel(
            name='PowerSocketPlacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shape', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=0, verbose_name='Координаты объекта')),
                ('room_layout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='furniture.roomlayout', verbose_name='Планировка')),
            ],
            options={
                'verbose_name': 'Розетка в помещении',
                'verbose_name_plural': 'Розетки в помещении',
            },
        ),
        migrations.CreateModel(
            name='FurniturePlacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shape', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=0, verbose_name='Координаты объекта')),
                ('furniture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='placements', to='furniture.furniture', verbose_name='Мебель')),
                ('room_layout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='furniture.roomlayout', verbose_name='Планировка')),
            ],
            options={
                'verbose_name': 'Размещение мебели в помещении',
                'verbose_name_plural': 'Размещение мебели в помещении',
            },
        ),
        migrations.AddField(
            model_name='furniture',
            name='type_of_rooms',
            field=models.ManyToManyField(related_name='furniture', to='furniture.roomtype', verbose_name='Комнаты'),
        ),
        migrations.CreateModel(
            name='WindowPlacement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shape', django.contrib.gis.db.models.fields.PolygonField(null=True, srid=0, verbose_name='Координаты объекта')),
                ('height', models.PositiveIntegerField(help_text='Высота в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Высота окна')),
                ('width', models.PositiveIntegerField(help_text='Ширина в мм', validators=[furniture.validators.minimum_len_width_validator], verbose_name='Ширина окна')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)ss', to='furniture.room', verbose_name='Комната')),
            ],
            options={
                'verbose_name': 'Окно в помещении',
                'verbose_name_plural': 'Окна в помещении',
            },
        ),
        migrations.CreateModel(
            name='PowerSocketPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='ID объекта (мебель или дверь)')),
                ('offset_width', models.IntegerField(default=0, verbose_name='Смещение электроточки по ширине относительно центра объекта')),
                ('offset_height', models.IntegerField(default=0, verbose_name='Высота электроточки от пола')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socket_connections', to='contenttypes.contenttype', verbose_name='Тип объекта (мебель или дверь)')),
                ('power_socket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_connections', to='furniture.powersocket', verbose_name='Электроточка')),
            ],
            options={
                'verbose_name': 'Расположение электроточки',
                'verbose_name_plural': 'Расположения электроточек',
                'unique_together': {('content_type', 'object_id', 'power_socket')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='furniture',
            unique_together={('name', 'depth', 'width')},
        ),
    ]
