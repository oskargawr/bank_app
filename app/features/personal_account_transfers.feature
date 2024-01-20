Feature: Personal Account Transfers

    Scenario: Create account
        When I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
        Then Number of accounts in registry equals: "1"
        And Account with pesel "12345678901" exists in registry

    Scenario: Incoming Transfers
        Given Number of accounts in registry equals: "1"
        When I make incoming transfer with pesel: "12345678901", ammount: "100"
        Then Account with pesel "12345678901" has saldo: "100"

    Scenario: Incoming Transfer with incorrect ammount
        Given Number of accounts in registry equals: "1"
        When I make incoming transfer with pesel: "12345678901", ammount: "-100"
        Then Account with pesel "12345678901" has saldo: "100"


    Scenario: Outgoing Transfer
        Given Number of accounts in registry equals: "1"
        When I make incoming transfer with pesel: "12345678901", ammount: "100"
        When I make outgoing transfer with pesel: "12345678901", ammount: "50"
        Then Account with pesel "12345678901" has saldo: "150"

    Scenario: Outgoing Transfer with incorrect ammount
        Given Number of accounts in registry equals: "1"
        When I make outgoing transfer with pesel: "12345678901", ammount: "-50"
        Then Account with pesel "12345678901" has saldo: "150"

    Scenario: Outgoing Transfer with infsufficient saldo
        Given Number of accounts in registry equals: "1"
        When I make outgoing transfer with pesel: "12345678901", ammount: "200"
        Then Account with pesel "12345678901" has saldo: "150"

    Scenario: Series of transfer
        Given Number of accounts in registry equals: "1"
        When I make incoming transfer with pesel: "12345678901", ammount: "100"
        When I make incoming transfer with pesel: "12345678901", ammount: "100"
        When I make outgoing transfer with pesel: "12345678901", ammount: "50"
        When I make outgoing transfer with pesel: "12345678901", ammount: "50"
        Then Account with pesel "12345678901" has history of transfers: "100,100,-50,100,100,-50,-50"

    Scenario: cleanup
        Given Number of accounts in registry equals: "1"
        When I delete account with pesel: "12345678901"
        Then Number of accounts in registry equals: "0"
