Feature: Basic math operations
 Test addition, substraction and multiplication

Scenario: add
 Given the value 10
 When I add 7
 Then the result is 17

Scenario: add a negative value
 Given the value 19
 When I add -11
 Then the result is 8

Scenario: mixed
 Given the value 10
 When I add 7
 And I add 7
 And I substract 11
 Then the result is 13
