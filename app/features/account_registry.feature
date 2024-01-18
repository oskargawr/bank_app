Feature: Account registry


 Scenario: User is able to create a new account
   Given Number of accounts in registry equals: "0"
   When I create an account using name: "kurt", last name: "cobain", pesel: "17594942759"
   Then Number of accounts in registry equals: "1"
   And Account with pesel "17594942759" exists in registry


 Scenario: User is able to create a second account
   Given Number of accounts in registry equals: "1"
   When I create an account using name: "john", last name: "lennon", pesel: "84100581195"
   Then Number of accounts in registry equals: "2"


 Scenario: Admin user is able to save the account registry
   When I save the account registry
   Then Number of accounts in registry equals: "2"


 Scenario: User is able to delete already created account
   Given Account with pesel "17594942759" exists in registry
   When I delete account with pesel: "17594942759"
   Then Account with pesel "17594942759" does not exists in registry


 Scenario: User is able to update first name saved in account
   Given Account with pesel "84100581195" exists in registry
   When I update first name in account with pesel "84100581195" to "janek"
   Then First name in account with pesel "84100581195" is "janek"


 Scenario: User is able to load account registry
   Given Number of accounts in registry equals: "1"
   When I load the account registry
   Then Number of accounts in registry equals: "2"
   And Account with pesel "17594942759" exists in registry
   And Account with pesel "84100581195" exists in registry


 Scenario: User is able to delete both accounts
   Given Account with pesel "17594942759" exists in registry
    And Account with pesel "84100581195" exists in registry
    When I delete account with pesel: "17594942759"
    And I delete account with pesel: "84100581195"
    Then Account with pesel "17594942759" does not exists in registry
    And Account with pesel "84100581195" does not exists in registry

  Scenario: cleanup
    Given Number of accounts in registry equals: "0"
    When I save the account registry
    Then Number of accounts in registry equals: "0"