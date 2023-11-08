import unittest

from ..KontoOsobiste import KontoOsobiste


class TestTransfer(unittest.TestCase):
    personal_data = {
        "name": "Dariusz",
        "surname": "Januszewski",
        "pesel": "96001010101",
    }

    def test_kredyt_warunek_a(self):
        konto = KontoOsobiste(
            self.personal_data["name"],
            self.personal_data["surname"],
            self.personal_data["pesel"],
        )
        konto.history = [100, 100, 100]
        konto.zaciagnij_kredyt(100)
        self.assertEqual(konto.udzielony_kredyt, True, "Kredyt nie został udzielony!")

    def test_kredyt_warunek_b(self):
        konto = KontoOsobiste(
            self.personal_data["name"],
            self.personal_data["surname"],
            self.personal_data["pesel"],
        )
        konto.history = [100, -50, 300, -100, 100]
        konto.zaciagnij_kredyt(100)
        self.assertEqual(konto.udzielony_kredyt, True, "Kredyt nie został udzielony!")

    def test_kredyt_warunek_a_nieudzielono(self):
        konto = KontoOsobiste(
            self.personal_data["name"],
            self.personal_data["surname"],
            self.personal_data["pesel"],
        )
        konto.history = [200, 200]
        konto.zaciagnij_kredyt(100)
        self.assertEqual(konto.udzielony_kredyt, False, "Kredyt został udzielony!")

    def test_kredyt_warunek_b_2(self):
        konto = KontoOsobiste(
            self.personal_data["name"],
            self.personal_data["surname"],
            self.personal_data["pesel"],
        )
        konto.history = [200, -100, -5, 10, 200]
        konto.zaciagnij_kredyt(1000)
        self.assertEqual(konto.udzielony_kredyt, False, "Kredyt nie został udzielony!")

    def test_ujemny_kredyt(self):
        konto = KontoOsobiste(
            self.personal_data["name"],
            self.personal_data["surname"],
            self.personal_data["pesel"],
        )
        konto.history = [200, -100, -5, 10, 200]
        konto.zaciagnij_kredyt(-1000)
        self.assertEqual(konto.udzielony_kredyt, False, "Kredyt został udzielony!")
