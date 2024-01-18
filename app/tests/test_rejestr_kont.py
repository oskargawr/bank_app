import requests
import unittest
from unittest.mock import patch, Mock
from app.RejestrKont import RejestrKont
from ..KontoOsobiste import KontoOsobiste


class testRejestrLoadSave(unittest.TestCase):
    @patch("app.RejestrKont.RejestrKont.collection")
    def test_zaladuj_konta_z_bazy_danch(self, mock_collection):
        mock_collection.find.return_value = [
            {
                "imie": "Jan",
                "nazwisko": "Kowalski",
                "pesel": "12345678901",
                "saldo": 0,
                "history": [],
            },
            {
                "imie": "Jan",
                "nazwisko": "Kowalski",
                "pesel": "12345678902",
                "saldo": 0,
                "history": [],
            },
        ]
        RejestrKont.load()
        self.assertEqual(RejestrKont.ile_kont(), 2)
        self.assertEqual(RejestrKont.lista[0].imie, "Jan")
        self.assertEqual(RejestrKont.lista[1].imie, "Jan")

    @patch("app.RejestrKont.RejestrKont.collection")
    def test_zapisz_konta_do_bazy_danych(self, mock_collection):
        mock_collection.find.return_value = [
            {
                "imie": "Jan",
                "nazwisko": "Kowalski",
                "pesel": "12345678901",
                "saldo": 0,
                "history": [],
            },
            {
                "imie": "Jan",
                "nazwisko": "Kowalski",
                "pesel": "12345678902",
                "saldo": 0,
                "history": [],
            },
        ]

        RejestrKont.load()
        self.assertEqual(RejestrKont.ile_kont(), 2)

        RejestrKont.dodaj_konto(KontoOsobiste("Jan", "Kowalski", "12345678903"))
        RejestrKont.save()
        self.assertEqual(mock_collection.insert_one.call_count, 3)
        RejestrKont.load()

    @patch("app.RejestrKont.RejestrKont.collection")
    def test_zapisz_konto_do_bazy_danych(self, mock_collection):
        mock_collection.find.return_value = [
            {
                "imie": "Jan",
                "nazwisko": "Kowalski",
                "pesel": "12345678900",
                "saldo": 0,
                "history": [],
            },
            {
                "imie": "Jan",
                "nazwisko": "Kowalski",
                "pesel": "12345678901",
                "saldo": 0,
                "history": [],
            },
        ]
        RejestrKont.load()
        self.assertEqual(RejestrKont.ile_kont(), 2)
        RejestrKont.dodaj_konto(KontoOsobiste("Jan", "Kowalski", "12345678902"))
        self.assertEqual(RejestrKont.ile_kont(), 3)
        mock_collection.find.return_value.append(
            {
                "imie": "Jan",
                "nazwisko": "Kowalski",
                "pesel": "12345678902",
                "saldo": 0,
                "history": [],
            }
        )
        RejestrKont.save()

        RejestrKont.usun_konto("12345678902")
        mock_collection.find.return_value.pop()
        RejestrKont.load()
        self.assertEqual(RejestrKont.ile_kont(), 2)
