from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import extend_schema_view, extend_schema
from djoser.conf import settings as djoser_settings


class BaseExtension(OpenApiViewExtension):
    """
    Базовый класс для генерации документации Swagger через drf-spectacular для эндпоинтов,
    предоставляемых стандартными библиотеками.

    Attributes:
        target_class (class): Класс представления, для которого будет добавлена документация.
        endpoints_doc (dict): Словарь, ключи которого соответствуют методам эндпоинтов,
                              а значения — настройкам drf-spectacular для каждого из этих методов.
        djoser_serializers: Сериализаторы из настроек Djoser, используемые для добавления
                            документации к запросам и ответам в соответствующих эндпоинтах.

    """
    target_class = None  # Будет определен в подклассах
    endpoints_doc: dict[str, extend_schema] = {}  # Документация для эндпоинтов, определенная в подклассах
    djoser_serializers = djoser_settings.SERIALIZERS

    def view_replacement(self):
        """
        Этот метод добавляет документацию, используя инструменты drf_spectacular.
        """
        @extend_schema_view(**self.endpoints_doc)
        class Fixed(self.target_class):
            pass
        return Fixed
