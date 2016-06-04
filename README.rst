
Introduction
============

Library to convert BDD_ features into Python unittest.TestCase classes. Run the
tests with your favorite test runner, like pytest, unittest or nose.
See the demo folder for an example.

Example
=======

Let's take a calculator as an example.
Create a plain text file called calculator.feature containing the BDD_-style
feature description:

.. code::

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

This is the text you can discuss with the customer and agree on.
Next write a backing file called test_calculator.py containing the code to
run this feature:

.. code::

    import os
    from bdd import Environment
    from calculator import Calculator

    env = Environment()
    env.context.calculator = Calculator()

    @env.given('the value {:d}')
    def step(context, value):
        context.calculator.value = value

    @env.when('adding {:d}')
    def step(context, value):
        context.calculator.add(value)

    @env.then('the result is {:d}')
    def step(context, value):
        assert context.calculator.value == value

    def rel(p):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(this_dir, p)

    CalculatorTestCase = env.load_feature_as_testcase('calculator.feature')

Finally, write the actual production code to implement the calculator, in
a file called calculator.py:

.. code::

    class Calculator:
        def __init__(self):
            self.value = 0

        def add(self, value):
            self.value += value

Now run the tests with, for example, pytest:

.. code::

    $ python -m pytest test_calculator.py -v
    =========== test session starts ===========================
    platform linux -- Python 3.5.1, pytest-2.9.1
    collected 2 items 

    test_calculator.py::CalculatorTestCase::test_scenario_0 <- bdd.py PASSED
    test_calculator.py::CalculatorTestCase::test_scenario_1 <- bdd.py PASSED



.. _BDD: https://en.wikipedia.org/wiki/Behavior-driven_development



References
==========

A really good python bdd library is behave_.

.. _behave: http://pythonhosted.org/behave/


Changelog
=========

**0.2**

- Add tag support

**0.1 (Jun 2, 2016)**

- Initial release

.. image:: https://travis-ci.org/windelbouwman/bdd.svg?branch=master
   :target: https://travis-ci.org/windelbouwman/bdd

.. image:: https://codecov.io/gh/windelbouwman/bdd/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/windelbouwman/bdd

