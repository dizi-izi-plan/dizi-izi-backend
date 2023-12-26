from datetime import timedelta


class Constants:
    def __setattr__(self, name: str, value: tuple) -> None:
        raise AttributeError(f"Нельзя переопределить '{name}'")

    CHOICES = (
        (timedelta(days=30), "месяц"),
        (timedelta(days=90), "3 месяца"),
        (timedelta(days=180), "6 месяцев"),
        (timedelta(days=270), "9 месяцев"),
        (timedelta(days=365), "год"),
    )
