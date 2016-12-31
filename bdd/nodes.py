""" Module with entities that can be loaded from feature files """

from collections import namedtuple


Feature = namedtuple('Feature', ['description', 'tags', 'scenarios'])
Scenario = namedtuple('Scenario', ['description', 'tags', 'steps'])
Step = namedtuple('Step', ['action', 'sentence'])
