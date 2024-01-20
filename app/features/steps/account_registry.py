from behave import *
from selenium.webdriver.common.keys import Keys
import requests
from unittest_assertions import AssertEqual

assert_equal = AssertEqual()
URL = "http://127.0.0.1:5000"


@when(
    'I create an account using name: "{name}", last name: "{surname}", pesel: "{pesel}"'
)
def create_account(context, name, surname, pesel):
    json_body = {"imie": f"{name}", "nazwisko": f"{surname}", "pesel": f"{pesel}"}
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert_equal(create_resp.status_code, 201)


@step('Number of accounts in registry equals: "{count}"')
def count_accounts_number_in_account_register(context, count):
    how_many_accounts = requests.get(URL + f"/api/accounts/count")
    assert_equal(how_many_accounts.json()["count"], int(count))


@step('Account with pesel "{pesel}" exists in registry')
def check_if_account_with_pesel_exists(context, pesel):
    account = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(account.status_code, 200)


@step('Account with pesel "{pesel}" does not exists in registry')
def check_if_account_with_pesel_does_not_exists(context, pesel):
    account = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(account.status_code, 404)


@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    resp = requests.delete(URL + f"/api/accounts/delete/{pesel}")
    assert_equal(resp.status_code, 200)
    assert_equal(resp.json()["message"], "Usunieto konto")


@when("I save the account registry")
def save_account(context):
    resp = requests.patch(URL + f"/api/accounts/save")
    assert_equal(resp.status_code, 200)


@when("I load the account registry")
def load_account_register(context):
    resp = requests.patch(URL + f"/api/accounts/load")
    assert_equal(resp.status_code, 200)


@when('I update first name in account with pesel "{pesel}" to "{name}"')
def update_surname(context, pesel, name):
    json_body = {"imie": f"{name}"}
    resp = requests.patch(URL + f"/api/accounts/update/{pesel}", json=json_body)
    assert_equal(resp.status_code, 200)


@then('First name in account with pesel "{pesel}" is "{name}"')
def check_surname(context, pesel, name):
    account = requests.get(URL + f"/api/accounts/{pesel}")
    print("konto: ", account.json())
    assert_equal(account.status_code, 200)
    assert_equal(account.json()["konto"]["imie"], name)


@step('Account with pesel "{pesel}" has saldo: "{saldo}"')
def check_if_account_with_pesel_exists(context, pesel, saldo):
    account = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(account.json()["konto"]["saldo"], int(saldo))


@step('Account with pesel "{pesel}" has history of transfers: "{history}"')
def check_if_account_with_pesel_exists(context, pesel, history):
    historia = [int(x) for x in history.split(",")]
    print("--------------------historia: ", historia)
    account = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(account.json()["konto"]["history"], historia)


@step('I make outgoing transfer with pesel: "{pesel}", ammount: "{ammount}"')
def make_outgoing_transfer(context, pesel, ammount):
    json_body = {"type": "outgoing", "amount": f"{ammount}"}
    resp = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert_equal(resp.status_code, 200)
    assert_equal(resp.json()["message"], "Przelew zostal wykonany")


@when('I make incoming transfer with pesel: "{pesel}", ammount: "{ammount}"')
def make_incoming_transfer(context, pesel, ammount):
    json_body = {"type": "incoming", "amount": f"{ammount}"}
    resp = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert_equal(resp.status_code, 200)
    assert_equal(resp.json()["message"], "Przelew zostal wykonany")
