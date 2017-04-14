from artistic_video.Artistic_image import ArtisticVideo
import unittest
import numpy as np
import os
import artistic_video.Image as image
import cv2

cwd = os.getcwd()


class ArtisticImageTests(unittest.TestCase):
    """These are not really unit tests. I used to test some certain methods before applying them."""

    def setUp(self):
        self.ai = ArtisticVideo()

    @unittest.skip
    def test_read_flow_file(self):
        flow_file = self.ai._read_flow_file(cwd+'/flow_files/overwatch_1_overwatch_1_backward.flo')
        self.assertEqual(np.any(flow_file), not None, "Flow file could not be read!")

    @unittest.skip
    def test_read_weights_file(self):
        weights_file = self.ai._read_weights_file(cwd+'/flow_files/overwatch_1_overwatch_1_backward_reliable.txt')
        self.assertEqual(np.any(weights_file), not None, "Flow file could not be read!")

    @unittest.skip
    def test_get_warped_image(self):
        flow = self.ai._read_flow_file(cwd + '/flow_files/overwatch_1_overwatch_1_backward.flo')
        frame = image.imread(cwd + '/images/overwatch_1.mp4_frame00001.png')
        warped = self.ai._get_warped_image(frame, flow)
        cv2.imwrite(cwd + '/im.png', warped)
        self.assertEqual(True, True, "")

    def test_stylize_video(self):
        for _, im in self.ai.create_image(network_path='../../imagenet-vgg-verydeep-19.mat',
                                          content_image=image.imread(cwd + '/test_input/input_frame00002.jpg'),
                                          styles_images=[image.imread(cwd + '/test_input/style1.jpg')],
                                          iterations=200,
                                          content_weight=5e0,
                                          style_weight=1e2,
                                          tv_weight=1e2,
                                          learning_rate=1e1,
                                          use_deepflow=True,
                                          temporal_weight=2e2,
                                          prev_frame=image.imread(cwd + '/test_input/input_frame00001.jpg'),
                                          backw_flow_path=cwd +
                                                  '/test_input/input_frame00001_input_frame00002_backward.flo',
                                          forw_cons_path=cwd +
                                                  '/test_input/input_frame00001_input_frame00002_backward_reliable.txt'
                                          ):
            image.imsave(cwd + '/test_outputs/result.jpg', im)
        self.assertEqual(True, True, "")


if __name__ == '__main__':
    unittest.main()
