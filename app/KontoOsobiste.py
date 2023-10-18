from .Konto import Konto


class KontoOsobiste(Konto):
    def __init__(self, imie, nazwisko, pesel, promo_code=None):
        self.imie = imie
        self.nazwisko = nazwisko
        self.saldo = 0
        if len(pesel) != 11:
            self.pesel = "Niepoprawny pesel!"
        else:
            self.pesel = pesel

        if self.is_promo_code_correct(promo_code) and self.is_born_after_year_1960():
            self.saldo = 50
        else:
            self.saldo = 0

    def is_promo_code_correct(self, promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
        else:
            return False

    def get_year_from_pesel(self):
        if self.pesel != "Niepoprawny pesel!":
            if self.pesel.startswith("0"):
                return 2000 + int(self.pesel[0:2])
            else:
                return 1900 + int(self.pesel[0:2])
        else:
            return "Niepoprawny pesel!"

    def is_born_after_year_1960(self):
        if self.pesel == "Niepoprawny pesel!":
            return False
        return self.get_year_from_pesel() > 1960
