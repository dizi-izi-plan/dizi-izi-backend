from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from factory import Sequence, fuzzy, PostGenerationMethodCall
from factory.django import DjangoModelFactory

CITIES = ['Buenos Aires', 'Cairo', 'Moscow', None]
PASSWORD = 'SoMePaSS_word_123'


class UserFactory(DjangoModelFactory):
    """
    Фабрика для создания экземпляров модели пользователя.
    """

    class Meta:
        model = settings.AUTH_USER_MODEL

    email = Sequence(lambda num: 'user{0}@dizi.izi'.format(num))
    first_name = Sequence(lambda num: 'user_{}'.format(num))
    birthday = fuzzy.FuzzyDate(
        timezone.now() - timedelta(weeks=3380),
        timezone.now() - timedelta(weeks=936)
    )
    password = PostGenerationMethodCall('set_password', PASSWORD)
    city = fuzzy.FuzzyChoice(CITIES)
