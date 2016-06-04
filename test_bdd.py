import unittest
import bdd
import io


SIMPLE_FEATURE = """ Feature: awesomeness
Scenario: Do some magic
Given some issue
When this and that is done
Then something cool happens
"""


class TestParser(unittest.TestCase):
    """ Check if the parser works correctly """
    def setUp(self):
        self.parser = bdd.Parser()

    def test_a_feature(self):
        feature = self.parser.parse(io.StringIO(SIMPLE_FEATURE))
        self.assertEqual(3, len(feature.scenarios[0].steps))

    def test_a_multiline_feature(self):
        feature = """ Feature: awesomeness
         also considering other cool stuff
         in case of insane nice stuff

        Scenario: Do some magic

        Given some issue
        And something else
        When this
        And that is done
        Then something cool happens
        And also something really cool happens
        But then nothing happens
        """
        self.parser.parse(io.StringIO(feature))

    def test_multi_feature(self):
        """ Test the parsing of multiple features in a single source """
        feature = """ Feature: awesomeness
        Scenario: Do some magic
        Given some issue
        Feature: this feature must be in a seperate file
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(io.StringIO(feature))

    def test_invalid_tag(self):
        feature = """ Feature: awesomeness
        @slow this @is invalid
        Scenario: Do some magic
        Given some issue
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(io.StringIO(feature))

    def test_and_as_first_step(self):
        feature = """ Feature: awesomeness
        Scenario: Do some magic
        And this cannot be
        """
        with self.assertRaises(SyntaxError):
            self.parser.parse(io.StringIO(feature))


class TestUnittestGenerator(unittest.TestCase):
    def test_a_feature(self):
        parser = bdd.Parser()
        feature = parser.parse(io.StringIO(SIMPLE_FEATURE))
        env = bdd.Environment()
        env.make_test_case(feature)


if __name__ == '__main__':
    unittest.main()
