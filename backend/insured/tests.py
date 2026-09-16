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

class InsuredPersonDetailTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(
            username="admin_detail_user",
            password="admin_password_123",
            is_staff = True,
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
            f'/api/insured-people/{self.insured_person.id}/',
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
            is_staff = True,
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
            f'/api/insured-people/{self.insured_person.id}/',
            {
                "last_name": "Krejčířová",
                "age": 36,
                "address": "Ostrava",
                "phone_number": "+420 434 555 666",
            },
            format="json"
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
            is_staff = True,
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
            f'/api/insured-people/{self.insured_person.id}/',
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(InsuredPerson.objects.filter(id=self.insured_person.id).exists())

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
            contract_date='2026-09-13',
            valid_until='2027-09-13',
        )

        self.second_contract = InsuranceContract.objects.create(
            insured_person=self.second_person,
            insurance_type=self.insurance_type,
            subject="Second user contract",
            amount=300000,
            contract_date='2026-09-13',
            valid_until='2027-09-13',
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

class InsuranceTypeCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="admin_type_create_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.user)

    def admin_can_create_insurance_type(self):
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
            format="json"
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
            format="json"
        )

        self.assertEqual(response.status_code, 403) # Forbidden

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
            format="json"
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
        self.assertFalse(InsuranceType.objects.filter(id=self.insurance_type.id).exists())

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
            {"phone_number": "+420 444 555 666"}
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
            {"subject": "Škoda"}
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
            {"insured_person": "Bob Druhý"}
        )

        self.assertEqual(response.status_code, 200)

        results = response.data.get("results", response.data)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["insured_person_name"], "Bob Druhý")
        self.assertEqual(results[0]["subject"], "Toyota Corolla")

class InsuredPersonValidationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="admin_validation_user",
            password="admin_password_123",
            is_staff=True,
        )
        self.token = Token.objects.create(user=self.user)

    def test_cannot_create_insured_person_without_required_field(self):
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
            format="json"
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

    def test_cannot_create_insurance_contract_without_required_field(self):
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
            format="json"
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

    def test_cannot_create_insurance_type_without_required_field(self):
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
            format="json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("name_en", response.data)
        self.assertIn("name_cs", response.data)
        self.assertIn("default_amount", response.data)