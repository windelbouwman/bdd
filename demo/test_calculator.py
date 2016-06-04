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


CalculatorTestCase = env.load_feature_as_testcase(rel('calculator.feature'))
