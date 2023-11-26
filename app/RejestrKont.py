from .Konto import Konto


class RejestrKont:
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
