from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class InsuredPersonValidationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="admin_validation_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.user)

    def test_cannot_create_insured_person_without_required_fields(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            "/api/insured-people/",
            {
                "first_name": "",
                "last_name": "",
                "age": "",
                "address": "",
                "phone_number": "",
                "username": "",
                "password": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("age", response.data)
        self.assertIn("address", response.data)
        self.assertIn("phone_number", response.data)
        self.assertIn("username", response.data)
        self.assertIn("password", response.data)


class InsuranceContractValidationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="admin_contract_validation_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.user)

    def test_cannot_create_insurance_contract_without_required_fields(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            "/api/insurance-contracts/",
            {
                "insured_person": "",
                "insurance_type": "",
                "subject": "",
                "amount": "",
                "contract_date": "",
                "valid_until": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("insured_person", response.data)
        self.assertIn("insurance_type", response.data)
        self.assertIn("subject", response.data)
        self.assertIn("amount", response.data)
        self.assertIn("contract_date", response.data)
        self.assertIn("valid_until", response.data)


class InsuranceTypeValidationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_type_validation_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.admin_user)

    def test_cannot_create_insurance_type_without_required_fields(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            "/api/insurance-types/",
            {
                "name_en": "",
                "name_cs": "",
                "default_amount": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("name_en", response.data)
        self.assertIn("name_cs", response.data)
        self.assertIn("default_amount", response.data)
