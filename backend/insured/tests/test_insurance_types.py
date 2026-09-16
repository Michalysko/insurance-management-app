from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import InsuranceType


class InsuranceTypeCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="admin_type_create_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.user)

    def test_admin_can_create_insurance_type(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            "/api/insurance-types/",
            {
                "name_en": "Travel insurance",
                "name_cs": "Cestovní pojištění",
                "default_amount": 100000,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name_en"], "Travel insurance")
        self.assertEqual(response.data["name_cs"], "Cestovní pojištění")
        self.assertEqual(response.data["default_amount"], "100000.00")


class InsuranceTypeClientCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="client_type_create_user",
            password="client_password_123",
            is_staff=False,
        )
        self.token = Token.objects.create(user=self.user)

    def test_client_cannot_create_insurance_type(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            "/api/insurance-types/",
            {
                "name_en": "Travel insurance",
                "name_cs": "Cestovní pojištění",
                "default_amount": 100000,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)


class InsuranceTypeUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="admin_type_update_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.user)
        self.insurance_type = InsuranceType.objects.create(
            name_en="Old insurance name",
            name_cs="Starý název pojištění",
            default_amount=80000,
        )

    def test_admin_can_update_insurance_type(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.patch(
            f"/api/insurance-types/{self.insurance_type.id}/",
            {
                "name_en": "Updated insurance name",
                "name_cs": "Upravený název pojištění",
                "default_amount": 120000,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name_en"], "Updated insurance name")
        self.assertEqual(response.data["name_cs"], "Upravený název pojištění")
        self.assertEqual(response.data["default_amount"], "120000.00")


class InsuranceTypeDeleteTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="admin_type_delete_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.user)
        self.insurance_type = InsuranceType.objects.create(
            name_en="Temporary insurance",
            name_cs="Dočasné pojištění",
            default_amount=60000,
        )

    def test_admin_can_delete_insurance_type(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.delete(
            f"/api/insurance-types/{self.insurance_type.id}/",
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            InsuranceType.objects.filter(id=self.insurance_type.id).exists()
        )
