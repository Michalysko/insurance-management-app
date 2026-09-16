from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import InsuredPerson, InsuranceContract, InsuranceType


class InsuranceContractCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_contract_user",
            password="admin_password_123",
            is_staff=True,
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
            "/api/insurance-contracts/",
            {
                "insured_person": self.insured_person.id,
                "insurance_type": self.insurance_type.id,
                "subject": "Škoda Octavia",
                "amount": 250000,
                "contract_date": "2026-09-13",
                "valid_until": "2027-09-13",
            },
            format="json",
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
            contract_date="2026-09-13",
            valid_until="2027-09-13",
        )

    def test_client_can_see_own_contracts(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get("/api/my-contracts/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["subject"], "Life coverage")


class MyContractsPrivacyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.first_user = User.objects.create_user(
            username="first_contract_user",
            password="client_password_123",
        )
        self.first_token = Token.objects.create(user=self.first_user)
        self.second_user = User.objects.create_user(
            username="second_contract_user",
            password="client_password_123",
        )
        self.first_person = InsuredPerson.objects.create(
            user=self.first_user,
            first_name="Anna",
            last_name="První",
            age=35,
            address="Plzeň",
            phone_number="+420 444 555 666",
        )
        self.second_person = InsuredPerson.objects.create(
            user=self.second_user,
            first_name="Lucie",
            last_name="Druhá",
            age=28,
            address="Ostrava",
            phone_number="+420 434 555 666",
        )
        self.insurance_type = InsuranceType.objects.create(
            name_en="Health insurance",
            name_cs="Zdravotní pojištění",
            default_amount=300000,
        )
        self.first_contract = InsuranceContract.objects.create(
            insured_person=self.first_person,
            insurance_type=self.insurance_type,
            subject="First user contract",
            amount=500000,
            contract_date="2026-09-13",
            valid_until="2027-09-13",
        )
        self.second_contract = InsuranceContract.objects.create(
            insured_person=self.second_person,
            insurance_type=self.insurance_type,
            subject="Second user contract",
            amount=300000,
            contract_date="2026-09-13",
            valid_until="2027-09-13",
        )

    def test_client_can_see_only_own_contracts(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.first_token.key}"
        )

        response = self.client.get("/api/my-contracts/")

        self.assertEqual(response.status_code, 200)

        subjects = [
            contract["subject"]
            for contract in response.data
        ]

        self.assertIn("First user contract", subjects)
        self.assertNotIn("Second user contract", subjects)


class MyProfileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="profile_user",
            password="client_password_123",
        )
        self.token = Token.objects.create(user=self.user)
        self.insured_person = InsuredPerson.objects.create(
            user=self.user,
            first_name="Marek",
            last_name="Profil",
            age=28,
            address="Liberec",
            phone_number="+420 444 555 666",
        )

    def test_client_can_see_own_profile(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get("/api/my-profile/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "Marek")
        self.assertEqual(response.data["last_name"], "Profil")
        self.assertEqual(response.data["age"], 28)
        self.assertEqual(response.data["address"], "Liberec")
        self.assertEqual(response.data["phone_number"], "+420 444 555 666")
