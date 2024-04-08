from rest_framework.throttling import AnonRateThrottle


class SustainedRateThrottle(AnonRateThrottle):
    """
    Устанавливает более длительное ограничение скорости для анонимных запросов.

    Расширяет `AnonRateThrottle`, применяя лимит 'long_time'. Используйте в `DEFAULT_THROTTLE_RATES`
    REST Framework для задания лимита, например, '3/day'.

    Attributes:
        scope (str): Идентификатор для лимита, по умолчанию 'long_time'.
    """
    scope = 'long_time'
