from .Konto import Konto
from .KontoOsobiste import KontoOsobiste
from pymongo import MongoClient


class RejestrKont:
    client = MongoClient("localhost", 27017)
    db = client["bank_app"]
    collection = db["konta"]
    lista = []

    @classmethod
    def dodaj_konto(cls, konto):
        cls.lista.append(konto)

    @classmethod
    def ile_kont(cls):
        return len(cls.lista)

    @classmethod
    def znajdz_konto(self, pesel):
        for konto in self.lista:
            if konto.pesel == pesel:
                return konto
        return None

    @classmethod
    def usun_konto(self, pesel):
        for konto in self.lista:
            if konto.pesel == pesel:
                self.lista.remove(konto)
                return True
        return False

    @classmethod
    def save(cls):
        cls.collection.delete_many({})
        for konto in cls.lista:
            cls.collection.insert_one(
                {
                    "imie": konto.imie,
                    "nazwisko": konto.nazwisko,
                    "pesel": konto.pesel,
                    "saldo": konto.saldo,
                    "history": konto.history,
                }
            )

    @classmethod
    def load(cls):
        cls.lista = []
        for konto in cls.collection.find():
            acc = KontoOsobiste(konto["imie"], konto["nazwisko"], konto["pesel"])
            acc.saldo = konto["saldo"]
            acc.history = konto["history"]
            cls.lista.append(acc)
