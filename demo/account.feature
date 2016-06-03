
@basic @db
Feature: Account system
  users can login and change password

 @happyflow
 Scenario: Normal login
  Given a valid user with username a and password b
  When the user logs in with username a and password b
  Then the user is logged in

 Scenario: Wrong password
  Given a valid user with username a and password b
  When the user logs in with username a and password x
  Then the user is not logged in
