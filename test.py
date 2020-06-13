import unittest
import os
from treg import Treg, Phrase


class TestTreg(unittest.TestCase):
    """ Basic Example Test """

    def tearDown(self) -> None:
        try:
            os.remove('treg_test.pkl')
        except FileNotFoundError:
            pass

    def test_afternoon_tea(self):
        treg = Treg()
        treg.add_phrases([
            Phrase(phrase='afternoon tea', meta={'fun': 1}),
            Phrase(phrase='tea party', meta={'fun': 3}),
        ])
        treg.add_phrase(Phrase(phrase='recipes'))

        # try to search before compiling
        try:
            list(treg.find_iter('...'))
        except TypeError:
            pass
        else:
            self.fail('Attempt to search before compiling did not raise TypeError')

        # compile the pattern
        treg.compile()

        # save the pattern
        treg.save('treg_test.pkl')
        # load the pattern
        treg = Treg.load('treg_test.pkl')

        # try to add a phrase after compiling
        try:
            treg.add_phrase(Phrase('...'))
        except TypeError:
            pass
        else:
            self.fail('Attempt to add a phrase after compiling did not raise TypeError')

        # search
        matches = list(treg.find_iter(
                "A long collection of afternoon tea party recipes ...",
                overlapped=True))

        # a total of 3 matches
        assert len(matches) == 3

        # afternoon tea
        assert len(matches[0].phrases) == 1
        assert matches[0].phrases[0] == Phrase(phrase='afternoon tea', meta={'fun': 1})
        assert matches[0].start == 21
        assert matches[0].end == 34

        # tea party
        assert len(matches[1].phrases) == 1
        second_match = matches[1].phrases[0]
        assert second_match == Phrase(phrase='tea party', meta={'fun': 3})
        assert matches[1].start == 31
        assert matches[1].end == 40

        # recipes
        assert len(matches[2].phrases) == 1
        third_match = matches[2].phrases[0]
        assert third_match == Phrase(phrase='recipes')
        assert matches[2].start == 41
        assert matches[2].end == 48


if __name__ == '__main__':
    unittest.main()
