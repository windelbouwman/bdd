
Feature: Shopping system
  delivery above 20 euro is 2
  delivery below 20 euro 5 euro

 Scenario: Small basket
  Given a product of 15 euro
  When I add it to the basket
  Then the total price should be 20 euro

 Scenario: Large basket
  Given a product of 22 euro
  When I add it to the basket
  Then the total price should be 24 euro

 Scenario: Edge basket
  Given a product of 20 euro
  When I add it to the basket
  Then the total price should be 22 euro
