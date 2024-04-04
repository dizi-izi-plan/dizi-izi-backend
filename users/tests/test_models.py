from django.test import TestCase

from users.models import CustomUserManager as UserManager
from users.models import CustomUser as User


class UserManagerTest(TestCase):
    args = {
        "email": "user1test@mail.com",
        "password": "User1test!password"
    }

    def test_create_user(self):
        user = User.objects.create_user(**self.args)
        self.assertEqual(user.email, self.args.get("email"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_invalid_user(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser('super1@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super1@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        admin_user = User.objects.create_superuser(
            email='super2@user.com', password='foo', is_superuser=False)
        self.assertTrue(admin_user.is_superuser)


class UserModelTest(TestCase):
    args = {
        "email": "user1test@mail.com",
        "password": "User1test!password"
    }

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(**cls.args)

    def test_str_representation(self):
        user = User.objects.get(email=self.args.get("email"))
        str_representation = str(user)
        self.assertEqual(str_representation, self.args.get("email"))
