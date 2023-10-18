import unittest

from ..KontoFirmowe import KontoFirmowe


class TestCreateBankAccount(unittest.TestCase):
    name = "JDG"
    nip = "1234567890"

    def test_create_bank_account(self):
        first_account = KontoFirmowe(self.name, self.nip)
        self.assertEqual(first_account.nazwa_firmy, self.name,
                         "Nazwa firmy nie jest poprawna!")
        self.assertEqual(first_account.nip, self.nip, "Nip nie jest poprawny!")
        self.assertEqual(first_account.saldo, 0, "Saldo nie jest poprawne!")

    def test_create_bank_account_with_incorrect_nip(self):
        first_account = KontoFirmowe(self.name, "123456789")
        self.assertEqual(first_account.nip, "Niepoprawny nip!",
                         "Nip nie jest poprawny!")

    def test_incoming_transfer(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.przelew_przychodzacy(100)
        self.assertEqual(first_account.saldo, 100, "Saldo nie jest równe 100!")

    def test_outgoing_transfer(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 120
        first_account.przelew_wychodzacy(100)
        self.assertEqual(first_account.saldo, 20,
                         "Saldo nie jest poprawne!")

    def test_outgoing_transfer_with_insufficient_funds(self):
        first_account = KontoFirmowe(self.name, self.nip)
        first_account.saldo = 120
        first_account.przelew_wychodzacy(200)
        self.assertEqual(first_account.saldo, 120,
                         "Saldo nie jest poprawne!")
