import unittest

from ..KontoOsobiste import KontoOsobiste
from ..RejestrKont import RejestrKont


class TestRejestr(unittest.TestCase):
    imie = "darek"
    nazwisko = "Januszewski"
    pesel = "12345678901"

    @classmethod
    def setUpClass(cls):
        cls.konto = KontoOsobiste(cls.imie, cls.nazwisko, cls.pesel)
        RejestrKont.dodaj_konto(cls.konto)

    def test_dodaj_konto(self):
        konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        konto1 = KontoOsobiste(self.imie + "ddd", self.nazwisko, self.pesel)
        RejestrKont.dodaj_konto(konto)
        RejestrKont.dodaj_konto(konto1)
        self.assertEqual(RejestrKont.ile_kont(), 3, "Niepoprawna ilosc kont!")

    def test_znajdz_konto(self):
        konto = RejestrKont.znajdz_konto(self.pesel)
        self.assertEqual(konto, self.konto, "Nie znaleziono konta!")

    def test_znajdz_konto_with_incorrect_pesel(self):
        konto = RejestrKont.znajdz_konto("12345678900")
        self.assertEqual(konto, None, "Znaleziono nieistniejace konto!")

    def test_usun_konto(self):
        konto = KontoOsobiste(self.imie, self.nazwisko, "10101010101")
        RejestrKont.dodaj_konto(konto)
        RejestrKont.usun_konto(konto.pesel)
        self.assertEqual(RejestrKont.ile_kont(), 3, "Nie usunieto konta!")

    def test_usun_nieistniejace_konto(self):
        RejestrKont.usun_konto("10101010101")
        self.assertEqual(RejestrKont.ile_kont(), 3, "Usunieto nieistniejace konto!")

    @classmethod
    def tearDownClass(cls):
        RejestrKont.lista = []
