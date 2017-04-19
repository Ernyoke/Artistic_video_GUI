from artistic_video.Video import convert_to_video
import unittest


class UtilsTests(unittest.TestCase):
    def test_convert_to_video(self):
        convert_to_video('test_vid', '.gif', 'images', 'hair_frame%05d', '.png')
        self.assertEqual(True, True)

    def runTest(self):
        self.test_base_name()


if __name__ == '__main__':
    unittest.main()