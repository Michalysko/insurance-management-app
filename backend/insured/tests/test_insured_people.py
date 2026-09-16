from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import InsuredPerson


class InsuredPeoplePermissionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_anonymous_user_cannot_access_insured_people(self):
        response = self.client.get("/api/insured-people/")

        self.assertEqual(response.status_code, 401)


class InsuredPeopleAdminAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.admin_user)

    def test_admin_user_can_access_insured_people(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get("/api/insured-people/")

        self.assertEqual(response.status_code, 200)


class InsuredPeopleClientAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_user = User.objects.create_user(
            username="client_user",
            password="client_password_123",
            is_staff=False,
        )
        self.token = Token.objects.create(user=self.client_user)

    def test_client_user_cannot_access_insured_people(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get("/api/insured-people/")

        self.assertEqual(response.status_code, 403)


class InsuredPersonCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_user_create",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.admin_user)

    def test_admin_can_create_insured_person(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            "/api/insured-people/",
            {
                "first_name": "John",
                "last_name": "Smith",
                "age": 30,
                "address": "Praha 1",
                "phone_number": "+420 123 456 789",
                "username": "john_smith",
                "password": "client_password_123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Smith")


class InsuredPersonClientCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_user = User.objects.create_user(
            username="client_user_create",
            password="client_password_123",
            is_staff=False,
        )
        self.token = Token.objects.create(user=self.client_user)

    def test_client_cannot_create_insured_person(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            "/api/insured-people/",
            {
                "first_name": "John",
                "last_name": "Smith",
                "age": 30,
                "address": "Praha 1",
                "phone_number": "+420 123 456 789",
                "username": "john_smith",
                "password": "client_password_123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)


class InsuredPersonDetailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_detail_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.insured_user = User.objects.create_user(
            username="detail_client_user",
            password="client_password_123",
        )
        self.insured_person = InsuredPerson.objects.create(
            user=self.insured_user,
            first_name="Petr",
            last_name="Dvořák",
            age=40,
            address="Ostrava",
            phone_number="+420 555 666 777",
        )

    def test_admin_can_view_insured_person_detail(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get(
            f"/api/insured-people/{self.insured_person.id}/",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Petr")
        self.assertEqual(response.data["last_name"], "Dvořák")


class InsuredPersonUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_update_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.insured_user = User.objects.create_user(
            username="update_client_user",
            password="client_password_123",
        )
        self.insured_person = InsuredPerson.objects.create(
            user=self.insured_user,
            first_name="Eva",
            last_name="Kovářová",
            age=35,
            address="Plzeň",
            phone_number="+420 444 555 666",
        )

    def test_admin_can_update_insured_person(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.patch(
            f"/api/insured-people/{self.insured_person.id}/",
            {
                "last_name": "Krejčířová",
                "age": 36,
                "address": "Ostrava",
                "phone_number": "+420 434 555 666",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["address"], "Ostrava")
        self.assertEqual(response.data["last_name"], "Krejčířová")
        self.assertEqual(response.data["age"], 36)
        self.assertEqual(response.data["phone_number"], "+420 434 555 666")


class InsuredPersonDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_delete_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.insured_user = User.objects.create_user(
            username="delete_client_user",
            password="client_password_123",
        )
        self.insured_person = InsuredPerson.objects.create(
            user=self.insured_user,
            first_name="Marek",
            last_name="Svoboda",
            age=28,
            address="Liberec",
            phone_number="+420 222 333 444",
        )

    def test_admin_can_delete_insured_person(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.delete(
            f"/api/insured-people/{self.insured_person.id}/",
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            InsuredPerson.objects.filter(id=self.insured_person.id).exists()
        )
