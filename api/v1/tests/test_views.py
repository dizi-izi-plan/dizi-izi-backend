from http import HTTPStatus

from test_storage.fixtures import TestUserFixture

from users.tests.factories import PASSWORD


class TestUserView(TestUserFixture):
    def test_user_registration(self):
        pswd = "password_exmpl_123"
        body = {
            "email": "example@example.com",
            "password": pswd,
            "re_password": pswd
        }
        response = self.anon_client.post(
            "/api/v1/auth/users/", data=body, format="json"
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue("email" in response.data)

    def test_login(self):
        body = {"email": self.user_1.email, "password": PASSWORD}
        response = self.anon_client.post(
            "/api/v1/auth/token/login/", data=body, format="json"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue("auth_token" in response.data)

    def test_logout(self):
        response = self.user_1_client.post("/api/v1/auth/token/logout/")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_get_current_user_information(self):
        response = self.user_1_client.get("/api/v1/auth/users/me/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data.get("email", None), self.user_1.email)
