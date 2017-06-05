from artistic_video.Video import convert_to_video
import unittest
import os.path

cwd = os.getcwd()


class UtilsTests(unittest.TestCase):
    def test_convert_to_video(self):
        frames = cwd + '/test_input/frames'
        output = cwd + '/test_outputs/out_vid'
        frm = 'dog_frame%05d'
        error_code = convert_to_video(output, '.gif', frames, frm, '.jpg')
        self.assertEqual(error_code, 0)
        self.assertEqual(os.path.isfile(output + '.gif'), True)

    def runTest(self):
        self.test_base_name()


if __name__ == '__main__':
    unittest.main()