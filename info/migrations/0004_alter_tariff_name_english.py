# Generated by Django 4.1.7 on 2023-12-26 11:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("info", "0003_remove_tariff_actions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tariff",
            name="name_english",
            field=models.SlugField(
                unique=True, verbose_name="Наименование тарифа на английском языке"
            ),
        ),
    ]