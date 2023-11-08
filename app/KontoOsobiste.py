from .Konto import Konto


class KontoOsobiste(Konto):
    def __init__(self, imie, nazwisko, pesel, promo_code=None):
        self.imie = imie
        self.nazwisko = nazwisko
        self.saldo = 0
        self.oplata_za_przelew_ekspresowy = 1
        self.history = []
        self.udzielony_kredyt = False

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

    def is_born_after_year_1960(self):
        if self.pesel == "Niepoprawny pesel!":
            return False
        return self.get_year_from_pesel() > 1960

    def kredyt_warunek_a(self):
        last_three_elements = self.history[-3:]
        if len(self.history) < 3:
            return False
        elif all(element > 0 for element in last_three_elements):
            return True
        else:
            return False

    def kredyt_warunek_b(self):
        last_five_elements = self.history[-5:]
        return sum(last_five_elements)

    def zaciagnij_kredyt(self, kwota):
        if kwota < 0:
            return False
        elif self.kredyt_warunek_a():
            self.saldo += kwota
            self.udzielony_kredyt = True
            return True
        elif self.kredyt_warunek_b() > kwota and (len(self.history) >= 5):
            self.saldo += kwota
            self.udzielony_kredyt = True
            return True
        else:
            return False
