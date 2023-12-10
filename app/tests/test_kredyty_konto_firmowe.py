import unittest

from ..KontoFirmowe import KontoFirmowe
from parameterized import parameterized
from unittest.mock import patch


class TestKredytFirma(unittest.TestCase):
    name = "JDG"
    nip = "1234567890"

    @patch("app.KontoFirmowe.KontoFirmowe.check_nip")
    def setUp(self, mock_check_nip):
        mock_check_nip.return_value = True
        self.konto = KontoFirmowe(self.name, self.nip)

    @parameterized.expand(
        [  # [[history], kwota, saldo, oczekiwany_udzielony_kredyt, oczekiwane saldo]
            [[-1775, 100, 100], 100, 200, True, 300],
            [[-1775, 100, 100], 100, 150, False, 150],
            [[100, 100, 100], 200, 1000, False, 1000],
            [[100, 100, 100], 100, 100, False, 100],
            [[-1775, 100, 100], -100, 100, False, 100],
        ]
    )
    def test_kredyt_konto_firmowe(
        self, history, kwota, saldo, oczekiwany_udzielony_kredyt, oczekiwane_saldo
    ):
        self.konto.history = history
        self.konto.saldo = saldo
        self.konto.zaciagnij_kredyt(kwota)
        self.assertEqual(
            self.konto.udzielony_kredyt,
            oczekiwany_udzielony_kredyt,
            "Kredyt nie został udzielony!",
        )
        self.assertEqual(
            self.konto.saldo,
            oczekiwane_saldo,
            "Saldo nie jest równe oczekiwanemu!",
        )
