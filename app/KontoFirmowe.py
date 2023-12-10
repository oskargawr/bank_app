from .Konto import Konto
import requests
from datetime import date
import os


class KontoFirmowe(Konto):
    def __init__(self, nazwa_firmy, nip):
        self.nazwa_firmy = nazwa_firmy

        self.saldo = 0
        self.history = []
        self.udzielony_kredyt = False

        if len(nip) != 10:
            self.nip = "Niepoprawny nip!"
        else:
            if self.check_nip(nip):
                self.nip = nip
            else:
                raise Exception("Niepoprawny nip!")
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

    def check_nip(self, nip):
        gov_url = os.getenv(
            "BANK_APP_MF_URL", "https://wl-api.mf.gov.pl/api/search/nip/"
        )
        todays_date = date.strftime(date.today(), "%Y-%m-%d")
        response = requests.get(str(gov_url) + nip + "?date=" + str(todays_date))
        if response.status_code == 200:
            print(True)
            return True
        else:
            print(False)
            return False
