import unittest
from ..KontoOsobiste import KontoOsobiste
from ..KontoFirmowe import KontoFirmowe
from ..SMTPConnection import SMTPConnection
from unittest.mock import patch, MagicMock
from io import StringIO


class TestWyslijHistorie(unittest.TestCase):
    personal_data = {
        "name": "Dariusz",
        "surname": "Januszewski",
        "pesel": "96001010101",
    }

    def test_was_wyslij_called(self):
        smtp_connection = SMTPConnection()
        smtp_connection.wyslij = MagicMock()
        smtp_connection.wyslij("Temat", "Tresc", "Adresat")
        smtp_connection.wyslij.assert_called_once_with("Temat", "Tresc", "Adresat")

    def test_wyslij_returns_false(self):
        smtp_connection = SMTPConnection()
        smtp_connection.wyslij = MagicMock()
        smtp_connection.wyslij.return_value = False
        self.assertFalse(smtp_connection.wyslij("Temat", "Tresc", "Adresat"))

    def test_wysylanie_maila_z_historia(self):
        konto = KontoOsobiste(
            self.personal_data["name"],
            self.personal_data["surname"],
            self.personal_data["pesel"],
        )
        konto.saldo = 1000
        konto.przelew_wychodzacy(100)
        smtp_connection = SMTPConnection()
        smtp_connection.wyslij = MagicMock(return_value=True)
        status = konto.wyslij_historie_na_maila(smtp_connection, "abc@abc.com")
        self.assertTrue(status)

    @patch("app.KontoFirmowe.KontoFirmowe.check_nip")
    def test_wyslania_maila_z_historia_konto_firmowe(self, mock_check_nip):
        mock_check_nip.return_value = True
        kontoFirmowe = KontoFirmowe("Firma", "1234567890")
        kontoFirmowe.saldo = 1000
        kontoFirmowe.przelew_wychodzacy(100)
        smtp_connection = SMTPConnection()
        smtp_connection.wyslij = MagicMock(return_value=True)
        status = kontoFirmowe.wyslij_historie_na_maila(smtp_connection, "abc@abc.com")
        self.assertTrue(status)

    @patch("app.KontoFirmowe.KontoFirmowe.check_nip")
    def test_wyslania_maila_z_historia_konto_firmowe_zly_nip(self, mock_check_nip):
        mock_check_nip.return_value = False
        kontoFirmowe = KontoFirmowe("Firma", "123456789")
        kontoFirmowe.saldo = 1000
        kontoFirmowe.przelew_wychodzacy(100)
        smtp_connection = SMTPConnection()
        smtp_connection.wyslij = MagicMock(return_value=False)
        status = kontoFirmowe.wyslij_historie_na_maila(smtp_connection, "abc@abc.com")
        self.assertFalse(status)
