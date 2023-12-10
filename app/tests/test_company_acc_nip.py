import unittest
from ..KontoFirmowe import KontoFirmowe
from unittest.mock import patch
from datetime import date
from io import StringIO


@patch("sys.stdout", new_callable=StringIO)
@patch("requests.get")
class TestCompanyAccNip(unittest.TestCase):
    def test_check_nip(self, mock_requests_get, mock_stdout):
        mock_requests_get.return_value.status_code = 200
        konto = KontoFirmowe("Nazwa firmy", "8461627563")
        self.assertEqual(konto.check_nip(konto.nip), True)

    def test_check_nip_false(self, mock_requests_get, mock_stdout):
        mock_requests_get.return_value.status_code = 404
        with self.assertRaises(Exception) as context:
            KontoFirmowe("Nazwa firmy", "1234567890")
        self.assertTrue("Niepoprawny nip!" in str(context.exception))

    def test_check_nip_print_false(self, mock_requests_get, mock_stdout):
        mock_requests_get.return_value.status_code = 404
        with self.assertRaises(Exception) as context:
            konto = KontoFirmowe("Nazwa firmy", "1234567890")
        self.assertTrue("Niepoprawny nip!" in str(context.exception))
        self.assertIn("False", mock_stdout.getvalue())
