
from bdd import Context


ctx = Context()


@ctx.given('a product of {:d} euro')
def step(context, amount):
    context.price = amount


@ctx.when('I add it to the basket')
def step(context):
    if context.price >= 20:
        context.total = context.price + 2
    else:
        context.total = context.price + 5


@ctx.then('the total price should be {:d} euro')
def step(context, total):
    assert total == context.total


FeatureTestCase = ctx.load_feature_as_testcase('demo.feature')
