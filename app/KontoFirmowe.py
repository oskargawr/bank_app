from .Konto import Konto


class KontoFirmowe(Konto):
    def __init__(self, nazwa_firmy, nip):
        self.nazwa_firmy = nazwa_firmy
        self.nip = nip
        self.saldo = 0
        self.history = []

        if len(nip) != 10:
            self.nip = "Niepoprawny nip!"
        else:
            self.nip = nip
            self.oplata_za_przelew_ekspresowy = 5
