from flask import Flask, request, jsonify
from app.RejestrKont import RejestrKont
from app.KontoOsobiste import KontoOsobiste

app = Flask(__name__)


@app.route("/api/accounts", methods=["POST"])
def stworz_konto():
    dane = request.get_json()
    if RejestrKont.znajdz_konto(dane["pesel"]) is not None:
        return jsonify({"message": "Konto o podanym peselu juz istnieje"}), 409
    print(f"Otrzymano dane: {dane}")
    konto = KontoOsobiste(dane["imie"], dane["nazwisko"], dane["pesel"])
    RejestrKont.dodaj_konto(konto)
    return jsonify({"message": "Konto stworzone"}), 201


@app.route("/api/accounts/count", methods=["GET"])
def ile_kont():
    return jsonify({"count": RejestrKont.ile_kont()}), 200


@app.route("/api/accounts/<pesel>", methods=["GET"])
def wyszukaj_konto_z_peselem(pesel):
    konto = RejestrKont.znajdz_konto(pesel)
    if konto is None:
        return jsonify({"message": "Nie znaleziono konta o podanym peselu"}), 404
    else:
        return jsonify({"message": "Znaleziono konto", "konto": konto.__dict__}), 200


@app.route("/api/accounts/update/<pesel>", methods=["PATCH"])
def update_data(pesel):
    konto = RejestrKont.znajdz_konto(pesel)
    if konto is None:
        return jsonify({"message": "Nie znaleziono konta o podanym peselu"}), 404
    else:
        dane = request.get_json()
        if "imie" in dane:
            konto.imie = dane["imie"]
        if "nazwisko" in dane:
            konto.nazwisko = dane["nazwisko"]
        if "pesel" in dane:
            konto.pesel = dane["pesel"]
        return jsonify({"message": "Zmieniono dane", "konto": konto.__dict__}), 200


@app.route("/api/accounts/delete/<pesel>", methods=["DELETE"])
def usun_konto(pesel):
    konto = RejestrKont.znajdz_konto(pesel)
    if konto is None:
        return jsonify({"message": "Nie znaleziono konta o podanym peselu"}), 404
    else:
        RejestrKont.usun_konto(pesel)
        return jsonify({"message": "Usunieto konto"}), 200


@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def transfer(pesel):
    konto = RejestrKont.znajdz_konto(pesel)
    if konto is None:
        return jsonify({"message": "Nie znaleziono konta o podanym peselu"}), 404
    else:
        dane = request.get_json()
        if ("amount" and "type") in dane:
            if dane["type"] == "incoming":
                konto.przelew_przychodzacy(int(dane["amount"]))
                return jsonify({"message": "Przelew zostal wykonany"}), 200
            if dane["type"] == "outgoing":
                konto.przelew_wychodzacy(int(dane["amount"]))
                return jsonify({"message": "Przelew zostal wykonany"}), 200

        return jsonify({"message": "Zlecenie przyjeto do realizacji"}), 200


@app.route("/api/accounts/save", methods=["PATCH"])
def save():
    RejestrKont.save()
    ilosc_kont = RejestrKont.ile_kont()
    return jsonify({"message": "Zapisano konta", "ilosc_kont": ilosc_kont}), 200


@app.route("/api/accounts/load", methods=["PATCH"])
def load():
    RejestrKont.load()
    ilosc_kont = RejestrKont.ile_kont()
    return jsonify({"message": "Zaladowano konta", "ilosc_kont": ilosc_kont}), 200
