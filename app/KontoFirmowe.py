from .Konto import Konto


class KontoFirmowe(Konto):
    def __init__(self, nazwa_firmy, nip):
        self.nazwa_firmy = nazwa_firmy
        self.nip = nip
        self.saldo = 0
        self.history = []
        self.udzielony_kredyt = False

        if len(nip) != 10:
            self.nip = "Niepoprawny nip!"
        else:
            self.nip = nip
            self.oplata_za_przelew_ekspresowy = 5

    def czy_jest_przelew_do_zus(self):
        if -1775 in self.history:
            return True

    def zaciagnij_kredyt(self, kwota):
        if kwota < 0:
            return False
        elif self.czy_jest_przelew_do_zus() and (self.saldo >= kwota * 2):
            self.udzielony_kredyt = True
            self.saldo += kwota
            return True
        else:
            return False
