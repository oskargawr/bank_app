class Konto:
    def __init__(self):
        self.saldo = 0

    def przelew_przychodzacy(self, kwota):
        if kwota > 0:
            self.saldo += kwota

    def przelew_wychodzacy(self, kwota):
        if (self.saldo - kwota) >= 0 and kwota > 0:
            self.saldo -= kwota
