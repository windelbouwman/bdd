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
    def test_a_feature(self):
        parser = bdd.Parser()
        feature = parser.parse(io.StringIO(SIMPLE_FEATURE))
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
        parser = bdd.Parser()
        parser.parse(io.StringIO(feature))


class TestUnittestGenerator(unittest.TestCase):
    def test_a_feature(self):
        parser = bdd.Parser()
        feature = parser.parse(io.StringIO(SIMPLE_FEATURE))
        ctx = bdd.Context()
        ctx.make_test_case(feature)


if __name__ == '__main__':
    unittest.main()
