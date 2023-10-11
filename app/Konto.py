class Konto:
    def __init__(self, imie, nazwisko, pesel, promo_code=None):
        self.imie = imie
        self.nazwisko = nazwisko
        self.saldo = 0
        if len(pesel) != 11:
            self.pesel = "Niepoprawny pesel!"
        else:
            self.pesel = pesel

        if self.is_promo_code_correct(promo_code):
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
