from tariff.models import Tariff, UsersTariffs
from users.models import CustomUser


def initialize_basic_user_tariff(user: CustomUser) -> None:
    """
    Инициализирует базовый тариф для пользователя.

    Эта функция проверяет наличие тарифов в системе и, если они существуют,
    назначает пользователю базовый тариф. Базовым считается тариф, отмеченный
    в системе как тариф по умолчанию (`is_default=True`).

    Параметры:
    - user (CustomUser): Объект пользователя, которому будет назначен базовый тариф.

    Возвращает:
    - None: Функция не возвращает значение.

    Примечания:
    - Если тарифов в системе нет, функция не выполняет никаких действий.
    - Если для пользователя уже установлен базовый тариф, повторное создание
      записи не происходит благодаря использованию метода `get_or_create`,
      который предотвращает дублирование записей.
    """
    if Tariff.objects.exists():
        UsersTariffs.objects.get_or_create(
            user=user,
            tariff=Tariff.objects.get(is_default=True),
        )
