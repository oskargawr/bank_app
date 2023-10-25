import unittest

from ..KontoOsobiste import KontoOsobiste


class TestCreateBankAccount(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "12345678901"

    def test_tworzenie_konta(self):
        pierwsze_KontoOsobiste = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        self.assertEqual(
            pierwsze_KontoOsobiste.imie, self.imie, "Imie nie zostało zapisane!"
        )
        self.assertEqual(
            pierwsze_KontoOsobiste.nazwisko,
            self.nazwisko,
            "Nazwisko nie zostało zapisane!",
        )
        self.assertEqual(pierwsze_KontoOsobiste.saldo, 0, "Saldo nie jest zerowe!")
        self.assertEqual(
            pierwsze_KontoOsobiste.pesel, self.pesel, "Pesel nie zostal zapisany"
        )

    def test_pesel_with_len_10(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "1234567890")
        self.assertEqual(
            Konto.pesel,
            "Niepoprawny pesel!",
            "Za krotki pesel zostal przyjety za prawidlowy",
        )

    def test_pesel_with_len_12(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "123456789000")
        self.assertEqual(
            Konto.pesel,
            "Niepoprawny pesel!",
            "Za krotki pesel zostal przyjety za prawidlowy",
        )

    def test_empty_pesel(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "")
        self.assertEqual(
            Konto.pesel,
            "Niepoprawny pesel!",
            "Za krotki pesel zostal przyjety za prawidlowy",
        )

    def test_promo_wrong_prefix(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel, "prom_123")
        self.assertEqual(Konto.saldo, 0, "Saldo nie jest zerowe!")

    def test_promo_wrong_suffix(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel, "PROM_123sd")
        self.assertEqual(Konto.saldo, 0, "Saldo nie jest zerowe!")

    def test_promo_wrong_len(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel, "PROM_")
        self.assertEqual(Konto.saldo, 0, "Saldo nie jest zerowe!")

    def test_promo_correct(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "65010112345", "PROM_123")
        self.assertEqual(Konto.saldo, 50, "Osoba urodzona po '60, kod poprawny")

    def test_promo_year_59(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "59010101010", "PROM_123")
        self.assertEqual(Konto.saldo, 0, "Osoba urodzona przed '60, kod poprawny")

    def test_promo_year_61(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "61010101010", "PROM_123")
        self.assertEqual(Konto.saldo, 50, "Osoba urodzona po '60, kod poprawny")

    def test_promo_year_60(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "60010101010", "PROM_123")
        self.assertEqual(Konto.saldo, 0, "Osoba urodzona w '60, kod poprawny")

    def test_promo_year_2001(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "01010101010", "PROM_123")
        self.assertEqual(Konto.saldo, 50, "Osoba urodzona w '01, kod poprawny")

    def test_promo_year_2001_wrong_promo_code(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "01010101010", "PROM_1234")
        self.assertEqual(Konto.saldo, 0, "Osoba urodzona w '01, kod niepoprawny")

    def test_promo_year_correct_promo_code_wrong_pesel(self):
        Konto = KontoOsobiste(self.imie, self.nazwisko, "010101010100", "PROM_123")
        self.assertEqual(Konto.pesel, "Niepoprawny pesel!", "Pesel niepoprawny")
        self.assertEqual(Konto.saldo, 0, "Osoba urodzona w '01, pesel niepoprawny")
