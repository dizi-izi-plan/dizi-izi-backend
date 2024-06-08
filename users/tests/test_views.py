from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.models import CustomUser as User


class UserViewSetTest(APITestCase):
    """
    Тесты для кастомного UserViewSet.
    Проверяется корректность работы API endpoints.
    """

    users = [
        ["admin@gmail.com", True],
        ["destroyer@gmail.com", False],
        ["normal_user@gmail.com", False],
        ["victim@gmail.com", False],
    ]

    @classmethod
    def setUpTestData(cls):
        """Подготовка данных для тестирования: создание пользователей."""
        for email, is_staff in cls.users:
            user = User(email=email, is_staff=is_staff)
            user.set_password("User1test!password")
            user.save()
            Token.objects.create(user=user)

    def test_self_destroy_normal_user(self):
        user = User.objects.get(email="normal_user@gmail.com")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + user.auth_token.key)
        data = {"current_password": "User1test!password"}
        response = self.client.delete(
            "/api/v1/auth/users/me/", data=data, format="json"
        )

        self.assertEqual(response.status_code, 204)
        user.refresh_from_db()
        self.assertFalse(user.is_active)

    def test_normal_user_destroy_another(self):
        destroyer = User.objects.get(email="destroyer@gmail.com")
        victim = User.objects.get(email="victim@gmail.com")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + destroyer.auth_token.key)
        response_without_password = self.client.delete(
            f"/api/v1/auth/users/{victim.id}/"
        )

        self.assertEqual(response_without_password.status_code, 403)

        data = {"current_password": "User1test!password"}

        response_with_password = self.client.delete(
            f"/api/v1/auth/users/{victim.id}/", data=data, format="json"
        )

        self.assertEqual(response_with_password.status_code, 403)

    def test_admin_destroy_normal_user(self):
        admin = User.objects.get(email="admin@gmail.com")
        victim = User.objects.get(email="victim@gmail.com")

        self.client.credentials(HTTP_AUTHORIZATION="Token " + admin.auth_token.key)

        response = self.client.delete(f"/api/v1/auth/users/{victim.id}/")

        self.assertEqual(response.status_code, 204)
        victim.refresh_from_db()
        self.assertFalse(victim.is_active)
