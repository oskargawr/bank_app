import unittest

from ..KontoFirmowe import KontoFirmowe
from parameterized import parameterized


class TestKredytFirma(unittest.TestCase):
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
        konto = KontoFirmowe("Nazwa firmy", "1234567890")
        konto.history = history
        konto.saldo = saldo
        konto.zaciagnij_kredyt(kwota)
        self.assertEqual(
            konto.udzielony_kredyt,
            oczekiwany_udzielony_kredyt,
            "Kredyt nie został udzielony!",
        )
        self.assertEqual(
            konto.saldo,
            oczekiwane_saldo,
            "Saldo nie zgadza się z oczekiwanym!",
        )
