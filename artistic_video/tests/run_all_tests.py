import artistic_video.tests.test_artistic_image as ai
import artistic_video.tests.test_utils as ui

import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(ai.ArtisticImageTests())
    suite.addTest(ui.UtilsTests())

    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    ts = test_suite()
    runner.run(ts)