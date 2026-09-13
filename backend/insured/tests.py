from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class LoginApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password_123"
        )

    def test_login_returns_token_for_valid_credentials(self):
        response = self.client.post(
            "/api/login/",
            {
                    "username": "test_user",
                    "password": "test_password_123",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

        token_exists = Token.objects.filter(user=self.user).exists()
        self.assertTrue(token_exists)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            "/api/login/",
            {
                "username": "test_user",
                "password": "wrong_password",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertNotIn("token", response.data)

class InsuredPeoplePermissionTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_anonymous_user_cannot_access_insured_people(self):
        response = self.client.get('/api/insured-people/')

        self.assertEqual(response.status_code, 401) # Unauthorized

class InsuredPeopleAdminAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_user",
            password="admin_password_123",
            is_staff = True,
        )
        self.token = Token.objects.create(user=self.admin_user)

    def test_admin_user_can_access_insured_people(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get('/api/insured-people/')

        self.assertEqual(response.status_code, 200)

class InsuredPeopleClientAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_user = User.objects.create_user(
            username="client_user",
            password="client_password_123",
            is_staff = False,
        )
        self.token = Token.objects.create(user=self.client_user)

    def test_client_user_cannot_access_insured_people(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get('/api/insured-people/')

        self.assertEqual(response.status_code, 403) # Forbidden

class InsuredPersonCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_user",
            password="admin_password_123",
            is_staff = True,
        )
        self.token = Token.objects.create(user=self.admin_user)

    def test_admin_can_create_insured_person(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            '/api/insured-people/',
            {
                "first_name": "John",
                "last_name": "Smith",
                "age": 30,
                "address": "Praha 1",
                "phone_number": "+420 123 456 789",
                "username": "john_smith",
                "password": "client_password_123",
            },
        format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Smith")

class InsuredPersonClientCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_user = User.objects.create_user(
            username="client_user",
            password="client_password_123",
            is_staff = False,
        )
        self.token = Token.objects.create(user=self.client_user)

    def test_client_cannot_create_insured_person(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        response = self.client.post(
            '/api/insured-people/',
            {
                    "first_name": "John",
                    "last_name": "Smith",
                    "age": 30,
                    "address": "Praha 1",
                    "phone_number": "+420 123 456 789",
                    "username": "john_smith",
                    "password": "client_password_123",
            },
            format="json"
        )

        self.assertEqual(response.status_code, 403) # Forbidden