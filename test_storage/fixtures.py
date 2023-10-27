from rest_framework.test import APITestCase, APIClient

from users.tests.factories import UserFactory


class TestUserFixture(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = UserFactory()
        cls.user_1_client = APIClient()
        cls.user_1_client.force_authenticate(cls.user_1)

        cls.user_2 = UserFactory()
        cls.user_2_client = APIClient()
        cls.user_2_client.force_authenticate(cls.user_2)

        cls.anon_client = APIClient()
