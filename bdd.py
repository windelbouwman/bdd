"""
    A library to load BDD features as unittest.TestCase classes.
"""

import logging
import unittest
from collections import namedtuple, defaultdict
import parse


__version__ = '0.1'


logger = logging.getLogger(__name__)
StepImpl = namedtuple('StepImpl', ['action', 'pattern', 'func'])


class Context:
    def __init__(self):
        self.stepmap = defaultdict(list)

    def deco(self, typ, pattern):
        def fnx(func):
            self.stepmap[typ].append(StepImpl(typ, pattern, func))
            return func
        return fnx

    def given(self, pattern):
        return self.deco('given', pattern)

    def when(self, pattern):
        return self.deco('when', pattern)

    def then(self, pattern):
        return self.deco('then', pattern)

    def load_feature_as_testcase(self, filename):
        """ Load a feature file and convert it to a testcase """
        feature = parse_feature('demo.feature')
        return self.make_test_case(feature)

    def make_test_case(self, feature):
        """ Create a unittest.TestCase subclass from a feature """
        name = 'FeatureTestCase'
        attrs = {}
        for i, scenario in enumerate(feature):
            test_name = 'test_scenario_{}'.format(i)
            attrs[test_name] = self.make_scenario_test_function(scenario)
        return type(name, (unittest.TestCase,), attrs)

    def exe_step(self, step):
        """ Execute the step in the current context """
        action = step.action.lower()
        for x in self.stepmap[action]:
            res = parse.parse(x.pattern, step.sentence)
            if res:
                x.func(self, *res.fixed)
                break
        else:
            raise Exception('No step impl found for {}'.format(step))

    def make_scenario_test_function(ctx, scenario):
        """ Create a function for a scenario """
        def test_impl(zelf):
            logger.debug('Scenario: "%s"', scenario.description)
            for step in scenario.steps:
                logging.debug('Step: "%s"', step.action + ' ' + step.sentence)
                ctx.exe_step(step)
        test_impl.__doc__ = scenario.description
        return test_impl


class Feature:
    def __init__(self, description, scenarios):
        self.description = description
        self.scenarios = scenarios

    def __iter__(self):
        return iter(self.scenarios)


Scenario = namedtuple('Scenario', ['description', 'steps'])
Step = namedtuple('Step', ['action', 'sentence'])


class Parser:
    """ Parses a feature file """
    def __init__(self):
        self._cl = ''
        self.at_end = False

    def parse(self, lines):
        self.prepare(lines)
        feature = self.parse_feature()
        if not self.at_end:
            self.error('No more text expected')
        return feature

    def parse_feature(self):
        """ Parse a single feature """
        line = self.consume('Feature:')
        description = line.split(':', 1)[1].strip()
        while not self.peak.startswith('Scenario:'):
            self.consume()
        scenarios = self.parse_scenarios()
        return Feature(description, scenarios)

    def parse_scenarios(self):
        """ Parse a series of scenarios """
        scenarios = []
        while self.peak.startswith('Scenario:'):
            scenarios.append(self.parse_scenario())
        return scenarios

    def parse_scenario(self):
        """ Parse a single scenario """
        line = self.consume('Scenario:')
        description = line.split(':', 1)[1].strip()
        steps = self.parse_steps()
        return Scenario(description, steps)

    def parse_steps(self):
        """ Parse a sequence of steps starting with given, when or then """
        steps = []
        prev_action = None
        while self.peak.startswith(('Given', 'When', 'Then', 'And', 'But')):
            line = self.consume()
            action, line = line.split(' ', 1)
            if action in ['And', 'But']:
                if not prev_action:
                    self.error('No previous action')
                action = prev_action
            step = Step(action, line)
            steps.append(step)
            prev_action = action
        return steps

    def prepare(self, lines):
        def f():
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                yield line

        self.at_end = False
        self._lines = f()
        self._cl = self._lines.__next__()

    @property
    def peak(self):
        """ Take a peak at what the next line is """
        return self._cl

    def consume(self, start=None):
        """ Read the next line starting with start if given """
        line = self._cl
        if start:
            if not line.startswith(start):
                self.error('Exected {}'.format(start))
        if not self.at_end:
            try:
                self._cl = self._lines.__next__()
            except StopIteration:
                self.at_end = True
                self._cl = ''
        return line

    def error(self, msg):
        raise Exception('{}: {}'.format(msg, self._cl))


def parse_feature(feature_file):
    """ Parse a feature from file """
    parser = Parser()
    with open(feature_file, 'r') as f:
        feature = parser.parse(f)
    return feature
