from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .models import InsuredPerson, InsuranceType, InsuranceContract

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

class InsuranceContractCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_user",
            password="admin_password_123",
            is_staff = True,
        )
        self.token = Token.objects.create(user=self.admin_user)

        self.insured_user = User.objects.create_user(
            username="insured_contract_user",
            password="client_password_123",
        )

        self.insured_person = InsuredPerson.objects.create(
            user=self.insured_user,
            first_name="John",
            last_name="Smith",
            age=30,
            address="Praha 1",
            phone_number="+420 123 456 789",
        )

        self.insurance_type = InsuranceType.objects.create(
            name_en="Vehicle insurance",
            name_cs="Pojištění vozidla",
            default_amount=250000,
        )

    def test_admin_can_create_insurance_contract(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            '/api/insurance-contracts/',
            {
                    "insured_person": self.insured_person.id,
                    "insurance_type": self.insurance_type.id,
                    "subject": "Škoda Octavia",
                    "amount": 250000,
                    "contract_date": '2026-09-13',
                    "valid_until": '2027-09-13',
            },
            format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["subject"], "Škoda Octavia")
        self.assertEqual(response.data["insurance_type"], self.insurance_type.id)
        self.assertEqual(response.data["amount"], "250000.00")

class MyContractsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.insured_user = User.objects.create_user(
            username="my_contracts_user",
            password="client_password_123",
        )
        self.token = Token.objects.create(user=self.insured_user)

        self.insured_person = InsuredPerson.objects.create(
            user=self.insured_user,
            first_name="Lucie",
            last_name="Nováková",
            age=31,
            address="Brno",
            phone_number="+420 987 654 321",
        )

        self.insurance_type = InsuranceType.objects.create(
            name_en="Life insurance",
            name_cs="Životní pojištění",
            default_amount=500000,
        )

        self.contract = InsuranceContract.objects.create(
            insured_person=self.insured_person,
            insurance_type=self.insurance_type,
            subject="Life coverage",
            amount=500000,
            contract_date='2026-09-13',
            valid_until='2027-09-13',
        )

    def test_client_can_see_own_contracts(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )
        response = self.client.get("/api/my-contracts/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["subject"], "Life coverage")