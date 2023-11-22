import unittest

from ..KontoOsobiste import KontoOsobiste
from parameterized import parameterized


class TestKredytOsobiste(unittest.TestCase):
    personal_data = {
        "name": "Dariusz",
        "surname": "Januszewski",
        "pesel": "96001010101",
    }

    @parameterized.expand(
        [  # [[history], kwota, oczekiwany_udzielony_kredyt, oczekiwane saldo]
            [[100, 100, 100], 100, True, 100],
            [[100, -50, 300, -100, 100], 100, True, 100],
            [[200, 200], 100, False, 0],
            [[200, -100, -5, 10, 200], 1000, False, 0],
            [[200, -100, -5, 10, 200], -1000, False, 0],
        ]
    )
    def test_kredyt_konto_osobiste(
        self, history, kwota, oczekiwany_udzielony_kredyt, oczekiwane_saldo
    ):
        konto = KontoOsobiste(
            self.personal_data["name"],
            self.personal_data["surname"],
            self.personal_data["pesel"],
        )
        konto.history = history
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
