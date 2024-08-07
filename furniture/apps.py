from django.apps import AppConfig


class FurnitureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'furniture'
    verbose_name = 'Мебель'

    def ready(self):
        """
        Этот метод вызывается автоматически, когда Django приложение готово к работе.
        Здесь происходит импорт схемы, содержащей описание эндпоинтов Djoser для приложения
        пользователей, что необходимо для интеграции с `drf-spectacular`. Данный подход описан
        в документации `drf-spectacular` в разделе `Extensions`.

        Замечание:
            Импорт делается внутри этого метода, чтобы избежать проблем циклического импорта,
            которые могут возникнуть, если бы импорт был выполнен в верхней части файла.
            Пометка `# noqa: E402` используется для указания инструментам статического анализа
            (например, flake8), что данное правило (E402) не должно применяться к этой строке.
        """
        import furniture.schema.schema_furniture  # noqa
        import furniture.schema.schema_room  # noqa
