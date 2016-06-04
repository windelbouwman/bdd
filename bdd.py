""" A library to load BDD features as unittest.TestCase classes. """

import logging
import unittest
import inspect
import os
from collections import namedtuple, defaultdict
import parse


__version__ = '0.3'


def rel(filename):
    """ Return an absolute path relative to the file where this function is
    called from """
    frame = inspect.stack()[1]
    dirname = os.path.dirname(os.path.abspath(frame[1]))
    return os.path.join(dirname, filename)


logger = logging.getLogger(__name__)


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
        """ Load a feature file and convert it to a testcase """
        feature = parse_feature(filename)
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
            logger.debug('Scenario: "%s"', scenario.description)
            for step in scenario.steps:
                logging.debug('%s %s', step.action, step.sentence)
                self.execute_step(step)
        test_impl.__doc__ = scenario.description
        return test_impl


class Context:
    """ This object will be passed to all the steps and can be used to store
        data """
    pass


Feature = namedtuple('Feature', ['description', 'tags', 'scenarios'])
Scenario = namedtuple('Scenario', ['description', 'tags', 'steps'])
Step = namedtuple('Step', ['action', 'sentence'])
StepImpl = namedtuple('StepImpl', ['action', 'pattern', 'func'])


class Parser:
    """ Parses a feature file """
    def __init__(self):
        self._current_line = ''
        self.at_end = False

    def parse(self, lines):
        self.prepare(lines)
        return self.parse_feature()

    def parse_feature(self):
        """ Parse a single feature """
        tags = self.parse_tags()
        line = self.consume('Feature:')
        description = line.split(':', 1)[1].strip()
        while not self.peak.startswith(('Scenario:', '@')):
            self.consume()
        scenarios = self.parse_scenarios()
        assert self.at_end
        return Feature(description, tags, scenarios)

    def parse_scenarios(self):
        """ Parse a series of scenarios """
        scenarios = []
        while not self.at_end:
            scenarios.append(self.parse_scenario())
        return scenarios

    def parse_scenario(self):
        """ Parse a single scenario """
        tags = self.parse_tags()
        line = self.consume('Scenario:')
        description = line.split(':', 1)[1].strip()
        steps = self.parse_steps()
        return Scenario(description, tags, steps)

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

    def parse_tags(self):
        """ Parse an optional set of tags starting with '@' """
        tags = set()
        while self.peak.startswith('@'):
            line = self.consume()
            for tag in line.split(' '):
                if tag.startswith('@') and len(tag) > 1:
                    tags.add(tag[1:])
                else:
                    self.error('Invalid tag "{}"'.format(tag))
        return tags

    def prepare(self, lines):
        def f():
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                yield line

        self.at_end = False
        self._lines = f()
        self._current_line = self._lines.__next__()

    @property
    def peak(self):
        """ Take a peak at what the next line is """
        return self._current_line

    def consume(self, start=None):
        """ Read the next line starting with start if given """
        line = self._current_line
        if start:
            if not line.startswith(start):
                self.error('Exected {}'.format(start))
        if not self.at_end:
            try:
                self._current_line = self._lines.__next__()
            except StopIteration:
                self.at_end = True
                self._current_line = ''
        return line

    def error(self, msg):
        """ Generate an error at the current location """
        raise SyntaxError('{}: {}'.format(msg, self._current_line))


def parse_feature(feature_file):
    """ Parse a feature from file """
    parser = Parser()
    with open(feature_file, 'r') as f:
        feature = parser.parse(f)
    return feature
