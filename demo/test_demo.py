import os
from bdd import Environment


this_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment()


def relpath(p):
    return os.path.join(this_dir, p)


@env.given('a product of {:d} euro')
def step(context, amount):
    context.price = amount


@env.when('I add it to the basket')
def step(context):
    if context.price >= 20:
        context.total = context.price + 2
    else:
        context.total = context.price + 5


@env.then('the total price should be {:d} euro')
def step(context, total):
    assert total == context.total


@env.given('a valid user with username {} and password {}')
def step(context, username, password):
    context.user = username, password


@env.when('the user logs in with username {} and password {}')
def step(context, username, password):
    context.logged_in = context.user == (username, password)


@env.then('the user is logged in')
def step(context):
    assert context.logged_in


@env.then('the user is not logged in')
def step(context):
    assert not context.logged_in


CartTestCase = env.load_feature_as_testcase(relpath('cart.feature'))
AccountTestCase = env.load_feature_as_testcase(relpath('account.feature'))
