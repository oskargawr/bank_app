import unittest

from ..KontoFirmowe import KontoFirmowe
from unittest.mock import patch
from unittest.mock import patch


class TestCreateBankAccount(unittest.TestCase):
    name = "JDG"
    nip = "1234567890"

    @patch("requests.get")
    def test_create_bank_account(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 200
        first_account = KontoFirmowe(self.name, self.nip)
        self.assertEqual(
            first_account.nazwa_firmy, self.name, "Nazwa firmy nie jest poprawna!"
        )
        self.assertEqual(first_account.nip, self.nip, "Nip nie jest poprawny!")
        self.assertEqual(first_account.saldo, 0, "Saldo nie jest poprawne!")

    @patch("requests.get")
    def test_check_nip_false(self, mock_requests_get):
        mock_requests_get.return_value.status_code = 404
        with self.assertRaises(Exception) as context:
            KontoFirmowe("Nazwa firmy", "1234567890")
        self.assertTrue("Niepoprawny nip!" in str(context.exception))

    def test_too_short_nip(self):
        konto = KontoFirmowe("Nazwa firmy", "1234569")
        self.assertEqual(konto.nip, "Niepoprawny nip!", "Nip nie jest poprawny!")

    def test_incoming_transfer(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.przelew_przychodzacy(100)
        self.assertEqual(first_account.saldo, 100, "Saldo nie jest równe 100!")

    def test_outgoing_transfer(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 120
        first_account.przelew_wychodzacy(100)
        self.assertEqual(first_account.saldo, 20, "Saldo nie jest poprawne!")

    def test_outgoing_transfer_with_insufficient_funds(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 120
        first_account.przelew_wychodzacy(200)
        self.assertEqual(first_account.saldo, 120, "Saldo nie jest poprawne!")

    def test_incoming_transfer_with_incorrrect_ammount(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 120
        first_account.przelew_przychodzacy(-20)
        self.assertEqual(first_account.saldo, 120, "Saldo nie jest poprawne!")

    def test_outgoing_express_transfer(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 120
        first_account.przelew_ekspresowy(100)
        self.assertEqual(first_account.saldo, 20 - 5, "Saldo nie jest poprawne!")

    def test_outgoing_express_transfer_with_negative_result(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 20
        first_account.przelew_ekspresowy(20)
        self.assertEqual(first_account.saldo, -5, "Saldo nie jest poprawne!")

    def test_outgoing_express_transfer_with_insufficient_funds(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 20
        first_account.przelew_ekspresowy(100)
        self.assertEqual(first_account.saldo, 20, "Saldo nie jest poprawne!")

    def test_outgoing_express_transfer_history(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 120
        first_account.przelew_ekspresowy(100)
        self.assertEqual(
            first_account.history, [-100, -5], "Historia nie jest poprawna!"
        )

    def test_series_of_transfers(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.przelew_przychodzacy(100)
        first_account.przelew_przychodzacy(120)
        first_account.przelew_wychodzacy(50)
        self.assertEqual(first_account.saldo, 170, "Saldo nie jest poprawne!")
        self.assertEqual(
            first_account.history, [100, 120, -50], "Historia nie jest poprawna!"
        )

    def test_outgoing_transfer_insufficient_funds_history(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 20
        first_account.przelew_wychodzacy(100)
        self.assertEqual(first_account.history, [], "Historia nie jest poprawna!")
