from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import InsuredPerson, InsuranceContract, InsuranceType


class InsuredPersonSearchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            username="admin_search_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.admin_user)
        self.insured_user1 = User.objects.create_user(
            username="search_client_user1",
            password="client_password_123",
        )
        self.insured_person1 = InsuredPerson.objects.create(
            user=self.insured_user1,
            first_name="Alice",
            last_name="Nováková",
            age=30,
            address="Praha",
            phone_number="+420 111 222 333",
        )
        self.insured_user2 = User.objects.create_user(
            username="search_client_user2",
            password="client_password_123",
        )
        self.insured_person2 = InsuredPerson.objects.create(
            user=self.insured_user2,
            first_name="Bob",
            last_name="Dvořák",
            age=40,
            address="Brno",
            phone_number="+420 444 555 666",
        )

    def test_admin_can_search_insured_people_by_name(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get("/api/insured-people/?name=Alice")

        self.assertEqual(response.status_code, 200)

        results = response.data.get("results", response.data)
        names = [
            person["first_name"]
            for person in results
        ]

        self.assertIn("Alice", names)
        self.assertNotIn("Lucie", names)

    def test_admin_can_search_insured_people_by_phone_number(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get(
            "/api/insured-people/",
            {"phone_number": "+420 444 555 666"},
        )

        self.assertEqual(response.status_code, 200)

        results = response.data.get("results", response.data)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["first_name"], "Bob")
        self.assertEqual(results[0]["phone_number"], "+420 444 555 666")


class InsuranceContractSearchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="admin_contract_search_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.user)
        self.first_user = User.objects.create_user(
            username="contract_search_first_user",
            password="client_password_123",
        )
        self.second_user = User.objects.create_user(
            username="contract_search_second_user",
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
            first_name="Bob",
            last_name="Druhý",
            age=40,
            address="Brno",
            phone_number="+420 111 222 333",
        )
        self.insurance_type = InsuranceType.objects.create(
            name_en="Vehicle insurance",
            name_cs="Pojištění vozidla",
            default_amount=250000,
        )
        self.first_contract = InsuranceContract.objects.create(
            insured_person=self.first_person,
            insurance_type=self.insurance_type,
            subject="Škoda Octavia",
            amount=120000,
            contract_date="2026-09-16",
            valid_until="2027-09-16",
        )
        self.second_contract = InsuranceContract.objects.create(
            insured_person=self.second_person,
            insurance_type=self.insurance_type,
            subject="Toyota Corolla",
            amount=120000,
            contract_date="2026-09-16",
            valid_until="2027-09-16",
        )

    def test_admin_can_search_insurance_contracts_by_subject(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get(
            "/api/insurance-contracts/",
            {"subject": "Škoda"},
        )

        self.assertEqual(response.status_code, 200)

        results = response.data.get("results", response.data)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["subject"], "Škoda Octavia")

    def test_admin_can_search_insurance_contracts_by_insured_person(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.get(
            "/api/insurance-contracts/",
            {"insured_person": "Bob Druhý"},
        )

        self.assertEqual(response.status_code, 200)

        results = response.data.get("results", response.data)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["insured_person_name"], "Bob Druhý")
        self.assertEqual(results[0]["subject"], "Toyota Corolla")
