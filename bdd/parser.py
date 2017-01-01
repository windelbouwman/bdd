""" Functionality to parse feature files """

from .nodes import Feature, Scenario, Step


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


def load_feature(feature_file):
    """ Load a feature from file """
    parser = Parser()
    with open(feature_file, 'r') as f:
        feature = parser.parse(f)
    return feature
