from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User


class AuthTests(TestCase):

    def setUp(self):

        self.client = APIClient()

    def test_register_user(self):

        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "john",
                "email": "john@test.com",
                "password": "Pass1234!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            User.objects.filter(username="john").exists()
        )
        self.assertEqual(
            User.objects.get(username="john").role,
            User.CUSTOMER
        )

    def test_login_user(self):

        User.objects.create_user(
            username="john",
            email="john@test.com",
            password="Pass1234!",
            role=User.CUSTOMER
        )

        response = self.client.post(
            "/api/auth/login/",
            {
                "username": "john",
                "password": "Pass1234!",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
