from artistic_video.Utils import get_base_name
import unittest


class UtilsTests(unittest.TestCase):
    def test_base_name(self):
        path = '/asd/asdwww/basename.ext'
        basename = get_base_name(path)
        self.assertEqual('basename', basename, "The returned basename is not correct!")

    def runTest(self):
        self.test_base_name()


if __name__ == '__main__':
    unittest.main()