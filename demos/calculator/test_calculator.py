from bdd import Environment
from calculator import Calculator

env = Environment()
env.context.calculator = Calculator()


@env.given('the value {:d}')
def step(context, value):
    context.calculator.value = value


@env.when('I add {:d}')
def step(context, value):
    context.calculator.add(value)


@env.when('I substract {:d}')
def step(context, value):
    context.calculator.substract(value)


@env.then('the result is {:d}')
def step(context, value):
    assert context.calculator.value == value


CalculatorTestCase = env.load_feature_as_testcase('calculator.feature')
