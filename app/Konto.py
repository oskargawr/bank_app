from datetime import datetime


class Konto:
    def __init__(self):
        self.saldo = 0

    def przelew_przychodzacy(self, kwota):
        if kwota > 0:
            self.saldo += kwota
            self.history += [kwota]

    def przelew_wychodzacy(self, kwota):
        if (self.saldo - kwota) >= 0 and kwota > 0:
            self.saldo -= kwota
            self.history += [-kwota]

    def przelew_ekspresowy(self, kwota):
        if (self.saldo - kwota) >= 0 and kwota > 0:
            self.saldo -= kwota + self.oplata_za_przelew_ekspresowy
            self.history += [-kwota]
            self.history += [-self.oplata_za_przelew_ekspresowy]

    def wyslij_historie_na_maila(self, SMTPConnection, adresat):
        temat = f"Wyciag z dnia {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if hasattr(self, "nip"):
            tresc = "Historia konta twojej firmy: " + str(self.history)
            return SMTPConnection.wyslij(temat, tresc, adresat)
        else:
            tresc = "Historia konta: " + str(self.history)
            return SMTPConnection.wyslij(temat, tresc, adresat)
