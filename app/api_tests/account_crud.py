import requests
import unittest
from app.RejestrKont import RejestrKont


class TestAccountCrud(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:5000"
        self.konto = requests.post(
            self.url + "/api/accounts",
            json={"imie": "Jan", "nazwisko": "Kowalski", "pesel": "12345678901"},
        )

    def test_1_create_account(self):
        self.assertEqual(self.konto.status_code, 201)

    def test_2_find_by_pesel(self):
        response = requests.get(self.url + "/api/accounts/12345678901")
        self.assertEqual(response.status_code, 200)

    def test_3_find_by_pesel(self):
        response = requests.get(self.url + "/api/accounts/12345678902")
        self.assertEqual(response.status_code, 404)

    def test_4_update_account(self):
        requests.post(
            self.url + "/api/accounts",
            json={"imie": "Jan", "nazwisko": "Kowalski", "pesel": "11111111111"},
        )
        response = requests.patch(
            self.url + "/api/accounts/update/11111111111",
            json={"imie": "Asia", "nazwisko": "Kowalski", "pesel": "12345678901"},
        )
        self.assertEqual(response.status_code, 200)

    def test_5_update_account(self):
        response = requests.patch(
            self.url + "/api/accounts/update/12345678902",
            json={"imie": "Jan", "nazwisko": "Kowalski", "pesel": "12345678901"},
        )
        self.assertEqual(response.status_code, 404)

    def test_6_delete_account(self):
        requests.post(
            self.url + "/api/accounts",
            json={"imie": "Jan", "nazwisko": "Kowalski", "pesel": "12345678901"},
        )
        response = requests.delete(self.url + "/api/accounts/delete/12345678901")
        self.assertEqual(response.status_code, 200)

    def test_7_delete_non_existing_account(self):
        response = requests.delete(self.url + "/api/accounts/delete/12345678902")
        self.assertEqual(response.status_code, 404)

    def test_8_update_only_1_parameter(self):
        requests.post(
            self.url + "/api/accounts",
            json={"imie": "Jan", "nazwisko": "Kowalski", "pesel": "12345678901"},
        )
        response = requests.patch(
            self.url + "/api/accounts/update/12345678901", json={"imie": "Asia"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["konto"]["imie"], "Asia")
        self.assertEqual(response.json()["konto"]["nazwisko"], "Kowalski")

    def test_9_add_already_existing_acc(self):
        response = requests.post(
            self.url + "/api/accounts",
            json={"imie": "Jan", "nazwisko": "Kowalski", "pesel": "12345678901"},
        )
        self.assertEqual(response.status_code, 409)

    def test_10_incoming_transfer(self):
        response = requests.post(
            self.url + "/api/accounts/12345678901/transfer",
            json={"amount": 100, "type": "incoming"},
        )
        self.assertEqual(response.status_code, 200)

    def test_11_outgoing_transfer(self):
        response = requests.post(
            self.url + "/api/accounts/12345678901/transfer",
            json={"amount": 100, "type": "outgoing"},
        )
        saldo = requests.get(self.url + "/api/accounts/12345678901").json()["konto"][
            "saldo"
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(saldo, 0)

    def tearDown(self):
        RejestrKont.lista = []
        requests.delete(self.url + "/api/accounts/delete/12345678901")
