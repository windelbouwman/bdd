
import logging
import unittest
import os
from collections import namedtuple, defaultdict
import parse

from .parser import load_feature
from .utils import rel

logger = logging.getLogger(__name__)


StepImpl = namedtuple('StepImpl', ['action', 'pattern', 'func'])


class Environment:
    """ The environment in which features can be run """
    def __init__(self):
        self.step_impls = defaultdict(list)
        self.context = Context()

    def given(self, pattern):
        """ Decorator to register a 'given' implementation """
        return self.make_decorator('given', pattern)

    def when(self, pattern):
        """ Decorator to register a 'when' implementation """
        return self.make_decorator('when', pattern)

    def then(self, pattern):
        """ Decorator to register a 'then' implementation """
        return self.make_decorator('then', pattern)

    def load_feature_as_testcase(self, filename):
        """ Load a feature file and convert it to a testcase.
            If the filename is not absolute, it is assumed to be relative
            to the calling scripts directory.
        """
        if not os.path.isabs(filename):
            filename = rel(filename, back=2)
        feature = load_feature(filename)
        return self.make_test_case(feature)

    def make_decorator(self, typ, pattern):
        """ Create a decorator for a certain step kind """
        def fnx(func):
            self.step_impls[typ].append(StepImpl(typ, pattern, func))
            return func
        return fnx

    def make_test_case(self, feature, name='FeatureTestCase'):
        """ Create a unittest.TestCase subclass from a feature """
        attrs = {}
        for i, scenario in enumerate(feature.scenarios):
            test_name = 'test_scenario_{}'.format(i)
            attrs[test_name] = self.make_scenario_test_function(scenario)
        return type(name, (unittest.TestCase,), attrs)

    def execute_step(self, step):
        """ Execute the step in the current context """
        action = step.action.lower()
        for step_impl in self.step_impls[action]:
            res = parse.parse(step_impl.pattern, step.sentence)
            if res:
                step_impl.func(self.context, *res.fixed)
                break
        else:
            raise Exception('No step impl found for {}'.format(step))

    def make_scenario_test_function(self, scenario):
        """ Create a function for a scenario """
        def test_impl(zelf):
            Runner().run_scenario(scenario, self)
        test_impl.__doc__ = scenario.description
        return test_impl


class Context:
    """ This object will be passed to all the steps and can be used to store
        data """
    pass


class Runner:
    """ Runner for features """
    def run(self, features, env):
        """ Run a set of features in a given environment """
        for feature in features:
            for scenario in feature.scenarios:
                try:
                    self.run_scenario(scenario, env)
                    print('OK')
                except Exception as e:
                    print('ERROR:', e)

    def run_scenario(self, scenario, env):
        """ Run a single scenario """
        print(scenario.description)
        logger.debug('Scenario: "%s"', scenario.description)
        for step in scenario.steps:
            logging.debug('%s %s', step.action, step.sentence)
            env.execute_step(step)
