from artistic_video.vgg import VGG19

import tensorflow as tf
import numpy as np
import scipy.misc
from functools import reduce
from operator import mul
import cv2
import struct
import time

from artistic_video.Atomic import AtomicBoolean
from PyQt5.Qt import QObject, pyqtSlot, pyqtSignal

from artistic_video.Image import imread, imsave
from artistic_video.Video import convert_to_frames, convert_to_video, make_opt_flow
from artistic_video.utils import get_input_type, get_separator, get_base_name, InputType

CONTENT_LAYER = ('relu4_2',)
STYLE_LAYERS = ('relu1_1', 'relu2_1', 'relu3_1', 'relu4_1', 'relu5_1')


class FFMPEGException(Exception):
    def __init__(self, error_code):
        self.error_code = error_code

    def get_error_code(self):
        return self.error_code


class ArtisticVideo(QObject):

    def __init__(self, parent=None):
        super(ArtisticVideo, self).__init__(parent)
        self.stop = AtomicBoolean()
        self.log = True
        self.log_dir = 'logs'

    iter_changed = pyqtSignal(int, int)     # emitted when an iteration is done in case of an image
    frame_changed = pyqtSignal(int, int)    # emitted when a frame is completed
    flow_created = pyqtSignal(int, int)     # emitted when the forward and backward flow is created for 2 frames
    set_status = pyqtSignal(str)            # display a status on the progressbar

    @staticmethod
    def size_of_tensor(tensor):
        """returns the size of a tensor"""
        return reduce(mul, (d.value for d in tensor.get_shape()), 1)

    def _compute_content_features(self, net, content_image):
        """Computes the content features by evaluating the content layers.
            Inputs are:
            net: a reference to the VGG19 network
            content: image
        """

        # create an empty dictionary to hold the content feature values
        content_features = {}

        # initialize the graph
        g = tf.Graph()
        with g.as_default(), g.device('/gpu:0'), tf.Session() as sess:
            # create a numpy array with a single element which is the content_image
            content_input = np.array([content_image])

            # create an empty tensor for the input
            image = tf.placeholder('float')

            # get the tensors for the content layers
            content_layers = net.get_layer_tensors(image, CONTENT_LAYER)

            # evaluate the content layers
            for layer_name, layer in content_layers.items():
                content_features[layer_name] = layer.eval(
                    feed_dict={image: content_input})

        return content_features

    def _compute_content_loss(self, all_layers, content_features, content_weight):
        """Computes the content loss for content layers.
        Inputs:
        all_layers: a dictionary containing all layers from a VGG net
        content_features: a dictionary which contains content features.
        They can be calculated by using the _compute_content_features function.
        content_weight: a floating point value between 0 and 1
        """

        # initialize a value which will hold the sum of the content loss values
        content_loss = 0.0

        # compute the content losses
        for layer_name in CONTENT_LAYER:
            content_loss += content_weight * (2 * tf.nn.l2_loss(
                all_layers[layer_name] - content_features[layer_name]) /
                                              content_features[layer_name].size)

        # calculate the average loss by dividing the sum of content losses with the
        # number of content layers
        content_loss /= len(CONTENT_LAYER)

        return content_loss

    def _create_gram_matrix(self, layer):
        """Calculates the Gram-matrix.
        If an entry in the Gram-matrix has a value close to zero then it means the two features in the given layer do not
        activate simultaneously for the given style-image. And vice versa, if an entry in the Gram-matrix has a large value,
        then it means the two features do activate simultaneously for the given style-image.
        """

        # get the number of the channels
        _, height, width, number_of_channels = map(lambda i: i.value, layer.get_shape())

        # compute the size of the tensor
        size = height * width * number_of_channels

        # reshape the tensor to be 2 dimensional
        features = tf.reshape(layer, (-1, number_of_channels))

        # create Gram matrix which basically is the product of the mat with itself
        gram = tf.matmul(tf.transpose(features), features) / size

        return gram

    def _compute_style_features(self, net, style_images):
        """Computes the content features by evaluating the content layers.
        Inputs are:
        net: a reference to the VGG19 network
        style_images: a list containing the style images
        """

        # initialize a list with empty dictionaries
        style_features = [{} for _ in style_images]

        # loop through style images
        for i in range(len(style_images)):

            # initialize the graph
            g = tf.Graph()
            with g.as_default(), g.device('/gpu:0'), tf.Session() as sess:

                # create a numpy array which contains the style images
                style_input = np.array([style_images[i]])

                # create an empty tensor for the input. Although it is not necessary to specify the shape of the
                # tensor, here it is mandatory otherwise the _create_gram_matrix function will not be able to
                # calculate the size of the tensor.
                image = tf.placeholder('float', (1,) + style_images[i].shape)

                # retrieve the style layers from the VGG network
                style_layers = net.get_layer_tensors(image, STYLE_LAYERS)

                # evaluate the layers with the given inputs
                for layer_name, layer in style_layers.items():
                    style_features[i][layer_name] = self._create_gram_matrix(layer). \
                        eval(feed_dict={image: style_input})

        return style_features

    def _compute_style_loss(self, all_layers, styles, style_features, style_weight):
        """Computes the style loss for style layers.
        Inputs:
        all_layers: a dictionary containing all layers from a VGG net
        styles: a list which contains the style images.
        styles_features:
        style_weight:
        style_blend_weight:
        They can be calculated by using the _compute_content_features function.
        content_weight: a floating point value between 0 and 1
        """

        style_loss = 0

        # iterate through style images
        for i in range(len(styles)):
            style_losses = []

            # iterate through style layers
            for style_layer in STYLE_LAYERS:
                # get the style layer
                layer = all_layers[style_layer]

                # compute the Gram matrix for the layer
                gram = self._create_gram_matrix(layer)

                # append the gram value to a list
                style_gram = style_features[i][style_layer]

                # compute the style loss for the layer and add it to a list
                style_losses.append(2 * tf.nn.l2_loss(gram - style_gram) / style_gram.size)

            # compute final style loss
            style_loss += style_weight * reduce(tf.add, style_losses)
        return style_loss

    def _compute_denoise_loss(self, image, tv_weight):
        """This function is the implementation of the  Total Variation Denoising algorithm. Essentially it just shifts
        the image one pixel in the x- and y-axis, calculates the difference from the original image.
        Inputs:
        image: a tensor containing the input image
        tv_weight:
        shape: the shape of the input image
        """

        # get the shape of the input image
        shape = image.get_shape()

        # compute the denoising loss
        tv_loss = tv_weight * 2 * (
            (tf.nn.l2_loss(image[:, 1:, :, :] - image[:, :shape[1] - 1, :, :]) /
             self.size_of_tensor(image[:, 1:, :, :])) +
            (tf.nn.l2_loss(image[:, :, 1:, :] - image[:, :, :shape[2] - 1, :]) /
             self.size_of_tensor(image[:, :, 1:, :])))

        return tv_loss

    def _read_flow_from_file(self, flow_path):
        """
        This method reads the flow (.flo) files into a 3D numpy array.
        :param flow_path: a string containing the path to the flow (.flo) file
        :return: a 3D numpy array with float32 values containing the flow values
        """
        with open(flow_path, 'rb') as f:
            # read the header (4 bytes)
            struct.unpack('4s', f.read(4))[0]

            # read the with and the height
            width = struct.unpack('i', f.read(4))[0]
            height = struct.unpack('i', f.read(4))[0]

            # make a 3 dimensional numpy array and unpack the values
            flow = np.ndarray((2, height, width), dtype=np.float32)
            for i in range(height):
                for j in range(width):
                    flow[1, i, j] = struct.unpack('f', f.read(4))[0]
                    flow[0, i, j] = struct.unpack('f', f.read(4))[0]
        return flow

    def _read_consistency_file(self, path):
        """
        This function reads the consistency file generated by the deepflow and cosistencychecker algorithms.
        The generated file should be stored as a .txt file.
        The values are stored following this condition: if a read value is < 255 than 0 is stored else 1 is stored.
        :param path: a string which contains the path the the consistency file.
        :return: a 3 dimensional numpy array containing the consistency file values.
        """
        with open(path) as f:
            lines = f.readlines()
            width, height = [int(i) for i in lines[0].split(' ')]
            values = np.zeros((height, width), dtype=np.float32)
            for i in range(0, len(lines) - 1):
                line = lines[i + 1].rstrip().split(' ')
                consistency_values = np.array([np.float32(j) for j in line])

                def convert(value):
                    """
                    :param value: a float32 containing a consistency value
                    :return: either 0 or 1
                    """
                    if value < 255:
                        return 0
                    return 1

                values[i] = list(map(convert, consistency_values))

            # expand to 3 channels
            weights = np.dstack([values.astype(np.float32)] * 3)

        return weights

    def _get_warped_image(self, image, flow):
        """
        This function warps the image according to the flow file.
        :param image: a numpy array containing the input image.
        :param flow: a numpy array containing the flow inputs
        :return: a numpy array containing the warped image
        """
        channels, height, width = flow.shape
        flow_map = np.zeros((channels, height, width), dtype=np.float32)
        for i in range(height):
            flow_map[1, i, :] += float(i)
        for i in range(width):
            flow_map[0, :, i] += float(i)

        # remap pixels to optical flow
        warped_image = cv2.remap(
            image, flow_map[0], flow_map[1],
            interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_TRANSPARENT)

        return warped_image

    def _temporal_loss(self, x, w, c):
        """
        This function calculated the temporal loss specified in "Artistic style transfer for videos"
         by Manuel Ruder, Alexey Dosovitskiy, Thomas Brox
        :param x: a numpy array which contains the previous frame
        :param w: a numpy array containing the previous warped frame
        :param c: a numpy 2D array containing the per pixel weighting of the loss (c E [0, 1]^D)
        :return: a tensor with the loss
        """
        c = c[np.newaxis, :, :, :]
        D = float(x.size)
        loss = (1. / D) * tf.reduce_sum(c * tf.nn.l2_loss(x - w))
        return tf.cast(loss, tf.float32)

    def _compute_shortterm_temporal_loss(self, sess, image, content_image, prev_frame, backward_flow_path, forward_weights):
        """
        :param prev_frame: a numpy array containing the previous frame
        :param backward_flow_path: a string containing the path to the backward optical flow file (.flo)
        :param forward_weights: a string containing the path to the consistency check weights file
        :return: a tensor with the loss
        """
        img = sess.run(image.assign(content_image.reshape((1,) + content_image.shape)))
        backward_optical_flow = self._read_flow_from_file(backward_flow_path)
        warped_image = self._get_warped_image(prev_frame, backward_optical_flow).astype(np.float32)
        content_weights = self._read_consistency_file(forward_weights)
        return self._temporal_loss(img, warped_image, content_weights)

    def _print_progress(self, iteration, total_iterations):
        print('Iteration %d/%d' % (iteration, total_iterations))

    def _print_losses(self, content_loss, style_loss, tv_loss, total_loss, temporal_loss):
        """
        Evaluates loss tensors and prints them.
        :param content_loss:
        :param style_loss:
        :param tv_loss:
        :param total_loss:
        :param temporal_loss:
        :return:
        """
        print('Content loss: %g' % content_loss.eval())
        print('Style loss: %g' % style_loss.eval())
        print('Denoising loss: %g' % tv_loss.eval())
        if temporal_loss is not None:
            print('Temporal loss: %g' % temporal_loss.eval())
        print('Total loss: %g' % total_loss.eval())

    def _log_losses(self, losses):
        """
        :param losses:
        :return:
        """
        if self.log:
            time_stamp = time.time()
            if losses:
                log_file_name = self.log_dir + get_separator() + 'log_losses_' + str(time_stamp) + '.txt'
                with open(log_file_name, 'w') as log_file:
                    for loss in losses:
                        log_file.write(str(loss) + ' ')

    def create_image(self,
                     network_path,
                     content_image,
                     styles_images,
                     iterations,
                     content_weight,
                     style_weight,
                     tv_weight,
                     learning_rate,
                     use_deepflow=False,
                     temporal_weight = 0,
                     prev_frame=None,
                     backw_flow_path=None,
                     forw_cons_path=None,
                     checkpoint_iterations=None):
        """
        :param network_path: 
        :param content_image: 
        :param styles_images: 
        :param iterations: 
        :param content_weight: 
        :param style_weight: 
        :param tv_weight: 
        :param learning_rate: 
        :param use_deepflow: 
        :param temporal_weight: 
        :param prev_frame: 
        :param backw_flow_path: 
        :param forw_cons_path: 
        :param checkpoint_iterations: 
        :return: 
        """

        self.stop.set(False)

        # get an instance of the VGG network
        net = VGG19(network_path)
        net.create()

        # compute content features
        content_features = self._compute_content_features(net, content_image)

        # compute style features
        style_features = self._compute_style_features(net, styles_images)

        # retrieve the content_image shape and make it 4 dimensional
        content_image_shape = (1,) + content_image.shape

        # make stylized image using back-propagation
        with tf.Graph().as_default():
            initial = tf.random_normal(content_image_shape) * 0.256

            image = tf.Variable(initial)
            all_layers = net.get_layer_tensors_all(image)

            # content loss
            content_loss = self._compute_content_loss(all_layers, content_features, content_weight)

            # style loss
            style_loss = self._compute_style_loss(all_layers, styles_images, style_features, style_weight)

            # total variation denoising
            tv_loss = self._compute_denoise_loss(image, tv_weight)

            # declare a list for holding all lass values (used for logging and charts)
            loss_values = []

            # optimization
            # a placeholder for the best loss value
            minimum_loss = float('inf')

            # a placeholder for the image which we can get with the best loss value
            best_image = None

            with tf.Session() as sess:

                # temporal loss
                temporal_loss = tf.Variable(0, tf.int32)
                if use_deepflow:
                    temporal_loss = temporal_weight * self._compute_shortterm_temporal_loss(sess, image,
                                                                                            content_image,
                                                                                            prev_frame,
                                                                                            backw_flow_path,
                                                                                            forw_cons_path)

                # overall loss
                loss = content_loss + style_loss + tv_loss + tf.cast(temporal_loss, tf.float32)

                # optimizer setup
                train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)

                sess.run(tf.global_variables_initializer())

                for i in range(iterations):

                    # stop the main loop
                    if self.stop.get():
                        return

                    # print the progress in every iteration
                    self._print_progress(i, iterations)

                    # check if is last step from of the iterations
                    last_step = i == iterations - 1
                    if last_step:
                        self._print_losses(content_loss, style_loss, tv_loss, loss, temporal_loss)
                        self._log_losses(loss_values)

                    # evaluate the optimizer
                    train_step.run()

                    # compute total loss
                    total_loss = loss.eval()
                    loss_values.append(total_loss)

                    # if the total loss is smaller than the minimum loss, keep the artisitc image
                    if total_loss < minimum_loss:
                        minimum_loss = total_loss
                        best_image = image.eval()

                    if (checkpoint_iterations and i % checkpoint_iterations == 0) or last_step:
                        yield (i, best_image.reshape(content_image_shape[1:]))

                    # emit a signal to the UI with the value of current iteration
                    self.iter_changed.emit(i, iterations)

    def stylize(self,
                network_path,
                content_image_path,
                style_images_path,
                output_path,
                iterations,
                content_weight,
                style_weight,
                tv_veight,
                temporal_weight,
                learning_rate,
                use_deepflow=False):

        """
        :param network_path: 
        :param content_image_path: 
        :param style_images_path: 
        :param output_path: 
        :param iterations: 
        :param content_weight: 
        :param style_weight: 
        :param tv_veight: 
        :param temporal_weight: 
        :param learning_rate: 
        :param use_deepflow: 
        :return: 
        """

        self.set_status.emit("Preprocessing...")

        frame = np.zeros([1, 1, 1], dtype=np.float)
        frame_list = []

        # read the input image
        content_type = get_input_type(content_image_path)
        if content_type == InputType.IMAGE:
            frame = imread(content_image_path)
        elif content_type == InputType.VIDEO:

            # frame output folder
            file_name = get_base_name(content_image_path)
            frames_output_folder = 'frames' + get_separator() + file_name

            # try to cut the video intro frames
            error_code, frame_list = convert_to_frames(content_image_path, frames_output_folder, '.jpg')

            if error_code != 0:
                raise FFMPEGException(error_code)

            frame = imread(frame_list[0])

            if error_code == 0:

                # try to create the optical flow for every frame
                if use_deepflow:
                    self.set_status.emit("Creating flow...")
                    forward_flow_list = {}
                    backward_flow_list = {}
                    forward_consistency_list = {}
                    backward_consistency_list = {}
                    # flow_output_folder = get_separator() + 'frames' + get_separator() +
                    for i in range(0, len(frame_list) - 1):
                        if not self.stop.get():
                            forward_flow, backward_flow, forward_consistency, backward_consistency \
                                = make_opt_flow(frame_list[i], frame_list[i + 1], frames_output_folder +
                                                get_separator() + 'flow')
                            forward_flow_list[frame_list[i]] = forward_flow
                            backward_flow_list[frame_list[i]] = backward_flow
                            forward_consistency_list[frame_list[i]] = forward_consistency
                            backward_consistency_list[frame_list[i]] = backward_consistency
                            self.flow_created.emit(i, len(frame_list) - 1)
                        else:
                            return

            else:
                print("Exited with ffmpeg error code: ", error_code)
                return

        # read the style images
        style_images = []
        for style_image in style_images_path:
            style_images.append(imread(style_image))

        content_shape = frame.shape
        for i in range(len(style_images)):
            style_scale = 1.0

            # resize style images
            style_images[i] = scipy.misc.imresize(style_images[i], style_scale *
                                                  content_shape[1] / style_images[i].shape[1])

        if content_type == InputType.IMAGE:
            print("Stylizing image", content_image_path)
            self.set_status.emit("Stylizing image " + content_image_path)
            for iteration, image in self.create_image(
                    network_path=network_path,
                    content_image=frame,
                    styles_images=style_images,
                    iterations=iterations,
                    content_weight=content_weight,
                    style_weight=style_weight,
                    tv_weight=tv_veight,
                    learning_rate=learning_rate,
                    use_deepflow=False
            ):
                imsave(output_path + str('out.jpg') + '.jpg', image)
            self.frame_changed.emit(1, 1)

        elif content_type == InputType.VIDEO:
            for index, frame_name in enumerate(frame_list):
                print('Stylizing frame', frame_name)
                self.set_status.emit("Stylizing frame " + content_image_path)
                if not self.stop.get():
                    frame = imread(frame_name)
                    if index == 0:
                        for iteration, image in self.create_image(
                                network_path=network_path,
                                content_image=frame,
                                styles_images=style_images,
                                iterations=iterations,
                                content_weight=content_weight,
                                style_weight=style_weight,
                                tv_weight=tv_veight,
                                learning_rate=learning_rate,
                                use_deepflow=False
                        ):
                            imsave(output_path + str(index) + '.jpg', image)
                            self.frame_changed.emit(0, len(frame_list))
                    else:
                        prev_frame_name = frame_list[index - 1]
                        current_backward_flow = backward_flow_list[frame_name]
                        current_forward_consistency = forward_consistency_list[frame_name]
                        for iteration, image in self.create_image(
                                network_path=network_path,
                                content_image=frame,
                                styles_images=style_images,
                                iterations=iterations,
                                content_weight=content_weight,
                                style_weight=style_weight,
                                tv_weight=tv_veight,
                                learning_rate=learning_rate,
                                use_deepflow=use_deepflow,
                                temporal_weight=temporal_weight,
                                prev_frame=prev_frame_name,
                                backw_flow_path=current_backward_flow,
                                forw_cons_path=current_forward_consistency
                        ):
                            imsave(output_path + str(index) + '.jpg', image)
                            # convert_to_video("output_ffmpeg", ".mp4", "frames")
                            self.frame_changed.emit(index, len(frame_list))
                else:
                    return

        if not self.stop.get():
            self.set_status.emit("Progress completed!")

    @pyqtSlot()
    def stop_running(self):
        """
        This slot can be called from another thread. This will set a stop flag. The algorith will stop running
        as soon as it wil be safe.
        :return: It has no return value
        """
        self.set_status.emit("Progress closed!")
        self.stop.set(True)
