Feature: Basic math operations
 Test addition

Scenario: add
 Given the value 10
 When adding 7
 Then the result is 17

Scenario: add a negative value
 Given the value 19
 When adding -11
 Then the result is 8
