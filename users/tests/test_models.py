from django.test import TestCase
from django.contrib.auth import get_user_model

from .factories import UserFactory

User = get_user_model()


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = UserFactory(i_am_designer=True)
        cls.user_2 = UserFactory()

    def test_correct_object_names(self):
        users = User.objects.all()
        for user in users:
            with self.subTest(user=user):
                self.assertEqual(str(user), user.email)

    def test_model_fields_default_values(self):
        field_default_value = {
            'i_am_designer': False,
            'is_active': True,
            'is_admin': False,
            'is_staff': False,
            'is_superuser': False,
        }
        for field, default_value in field_default_value.items():
            with self.subTest(field=field):
                self.assertEqual(
                    getattr(self.user_2, field), default_value
                )
