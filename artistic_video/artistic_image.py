from artistic_video.vgg import VGG19

import tensorflow as tf
import numpy as np
from functools import reduce
from operator import mul
# import cv2
import struct

CONTENT_LAYER = ('relu4_2',)
STYLE_LAYERS = ('relu1_1', 'relu2_1', 'relu3_1', 'relu4_1', 'relu5_1')


def _compute_content_features(net, content_image):
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


def _compute_content_loss(all_layers, content_features, content_weight):
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


def _create_gram_matrix(layer):
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


def _compute_style_features(net, style_images):
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
                style_features[i][layer_name] = _create_gram_matrix(layer).\
                    eval(feed_dict={image: style_input})

    return style_features


def _compute_style_loss(all_layers, styles, style_features, style_weight):
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
            gram = _create_gram_matrix(layer)

            # append the gram value to a list
            style_gram = style_features[i][style_layer]

            # compute the style loss for the layer and add it to a list
            style_losses.append(2 * tf.nn.l2_loss(gram - style_gram) / style_gram.size)

        # compute final style loss
        style_loss += style_weight * reduce(tf.add, style_losses)
    return style_loss


def _compute_denoise_loss(image, tv_weight):
    """This function is the implementation of the  Total Variation Denoising algorithm. Essentially it just shifts
    the image one pixel in the x- and y-axis, calculates the difference from the original image.
    Inputs:
    image: a tensor containing the input image
    tv_weight:
    shape: the shape of the input image
    """

    def size_of_tensor(tensor):
        """returns the size of a tensor"""
        return reduce(mul, (d.value for d in tensor.get_shape()), 1)

    # get the shape of the input image
    shape = image.get_shape()

    # compute the denoising loss
    tv_loss = tv_weight * 2 * (
        (tf.nn.l2_loss(image[:, 1:, :, :] - image[:, :shape[1] - 1, :, :]) /
         size_of_tensor(image[:, 1:, :, :])) +
        (tf.nn.l2_loss(image[:, :, 1:, :] - image[:, :, :shape[2] - 1, :]) /
         size_of_tensor(image[:, :, 1:, :])))

    return tv_loss


def _read_flow_file(flow_path):
    """

    :param flow_path:
    :return:
    """
    with open(flow_path, 'rb') as f:
        # read the header (4 bytes)
        struct.unpack('4s', f.read(4))[0]

        # read the with and the height
        width = struct.unpack('i', f.read(4))[0]
        height = struct.unpack('i', f.read(4))[0]

        flow = np.ndarray((2, width, height), dtype=np.float32)
        for y in range(height):
            for x in range(width):
                flow[1, x, y] = struct.unpack('f', f.read(4))[0]
                flow[0, x, y] = struct.unpack('f', f.read(4))[0]
    return flow


def _read_consistency_file(path):
    """
    This function reads the consistency file generated by the deepflow and cosistencychecker algorithms.
    The generated file should be stored as a .txt file.
    The values are stored following this condition: if a read value is < 255 than 0 is stored else 1 is stored.
    :param path: a string which contains the path the the consistency file.
    :return: a 3 dimensional numpy array containing the consistency file values.
    """
    with open(path) as f:
        lines = f.readlines()
        header = list(map(int, lines[0].split(' ')))
        width = header[0]
        height = header[1]
        values = np.zeros((height, width), dtype=np.float32)
        for i in range(1, len(lines)):
            line = lines[i].rstrip().split(' ')
            values[i - 1] = np.array(list(map(np.float32, line)))
            values[i - 1] = list(map(lambda x: 0. if x < 255. else 1., values[i - 1]))

        # expand to 3 channels
        weights = np.dstack([values.astype(np.float32)] * 3)

    return weights


def _get_warped_image(image, flow):
    """
    This function warps the image according to the flow file.
    :param image: a numpy array containing the input image.
    :param flow: a numpy array containing the flow inputs
    :return: a numpy array containing the warped image
    """
    channels, width, height = flow.shape
    print(flow.shape)
    flow_map = np.zeros((channels, height, width), dtype=np.float32)
    for y in range(height):
        flow_map[1, y, :] = float(y) + flow[1, :, y]
    for x in range(width):
        flow_map[0, :, x] = float(x) + flow[0, x, :]

    # remap pixels to optical flow
    #warped_image = cv2.remap(
    #    image, flow_map[0], flow_map[1],
    #    interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_TRANSPARENT)

    #return warped_image


def _temporal_loss(x, w, c):
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


def _compute_shortterm_temporal_loss(prev_frame, backward_flow_path, forward_weights):
    """
    :param prev_frame: a numpy array containing the previous frame
    :param backward_flow_path: a string containing the path to the backward optical flow file (.flo)
    :param forward_weights: a string containing the path to the consistency check weights file
    :return: a tensor with the loss
    """
    backward_optical_flow = _read_flow_file(backward_flow_path)
    warped_image = _get_warped_image(prev_frame, backward_optical_flow)
    content_weights = _read_consistency_file(forward_weights)
    return _temporal_loss(prev_frame, warped_image, content_weights)


def _print_progress(iteration, total_iterations):
    print('Iteration %d/%d' % (iteration, total_iterations))


def _print_losses(content_loss, style_loss, tv_loss, total_loss, temporal_loss):
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


def create_image(network_path, content_image, styles_images, iterations,
                 content_weight, style_weight, tv_weight, learning_rate,
                 use_deepflow, prev_frame, backw_flow_path, forw_cons_path,
                 checkpoint_iterations=None):
    """
    Inputs:
    network_path (string): the path of the VGG network from the hard drive
    content_image (): the content of the image which will be stylized
    style_images (list[]): a list with the style images
    iterations (int): number of iteration for the training optimization
    content_weight (int):
    style_weight (int):
    style_blend_weight (list[int]):
    tv_weight (int):
    learning_rate (int): learning rate
    checkpoint_iteration (int): every time when the iterator hits a multiple of this value, an image is yielded back
    """

    # get an instance of the VGG network
    net = VGG19(network_path)
    net.create()

    # compute content features
    content_features = _compute_content_features(net, content_image)

    # compute style features
    style_features = _compute_style_features(net, styles_images)

    # retrieve the content_image shape and make it 4 dimensional
    content_image_shape = (1,) + content_image.shape

    # make stylized image using back-propagation
    with tf.Graph().as_default():
        initial = tf.random_normal(content_image_shape) * 0.256

        image = tf.Variable(initial)
        all_layers = net.get_layer_tensors_all(image)

        # content loss
        content_loss = _compute_content_loss(all_layers, content_features, content_weight)

        # style loss
        style_loss = _compute_style_loss(all_layers, styles_images, style_features, style_weight)

        # total variation denoising
        tv_loss = _compute_denoise_loss(image, tv_weight)

        # temporal loss
        temporal_loss = tf.Variable(0, tf.int32)
        if use_deepflow:
            temporal_loss = _compute_shortterm_temporal_loss(prev_frame, backw_flow_path, forw_cons_path)

        # overall loss
        loss = content_loss + style_loss + tv_loss + temporal_loss

        # optimizer setup
        train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)

        # optimization
        # a placeholder for the best loss value
        minimum_loss = float('inf')

        # a placeholder for the image which we can get with the best loss value
        best_image = None

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            for i in range(iterations):

                # print the progress in every iteration
                _print_progress(i, iterations)

                # check if is last step from of the iterations
                last_step = i == iterations - 1
                if last_step:
                    _print_losses(content_loss, style_loss, tv_loss, loss, temporal_loss)

                # evaluate the optimizer
                train_step.run()

                # compute total loss
                total_loss = loss.eval()

                # if the total loss is smaller than the minimum loss, keep the artisitc image
                if total_loss < minimum_loss:
                    minimum_loss = total_loss
                    best_image = image.eval()

                if (checkpoint_iterations and i % checkpoint_iterations == 0) or last_step:
                    yield (i, best_image.reshape(content_image_shape[1:]))

    def stop():
        pass
