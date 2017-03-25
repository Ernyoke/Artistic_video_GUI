
# The pre-trained VGG19 model can be downloaded from:
# http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat

import tensorflow as tf
import numpy as np
import scipy.io
import copy


class VGG19:

    def __init__(self, vgg_path):
        self.vgg_path = vgg_path
        self.LAYERS = (
            'conv1_1', 'relu1_1', 'conv1_2', 'relu1_2', 'pool1',
            'conv2_1', 'relu2_1', 'conv2_2', 'relu2_2', 'pool2',
            'conv3_1', 'relu3_1', 'conv3_2', 'relu3_2', 'conv3_3',
            'relu3_3', 'conv3_4', 'relu3_4', 'pool3',
            'conv4_1', 'relu4_1', 'conv4_2', 'relu4_2', 'conv4_3',
            'relu4_3', 'conv4_4', 'relu4_4', 'pool4',
            'conv5_1', 'relu5_1', 'conv5_2', 'relu5_2', 'conv5_3',
            'relu5_3', 'conv5_4', 'relu5_4'
        )
        self.data = []
        self.weights = []

    def create(self):
        try:
            self.data = scipy.io.loadmat(self.vgg_path)
        except FileNotFoundError as err:
            raise err
        self.weights = self.data['layers'][0]

    def get_layer_tensors(self, input_tensor, id_list):
        tensor_list = {}
        tensor = input_tensor
        for position, layer_id in enumerate(self.LAYERS):
            layer_type = layer_id[:4]
            if layer_type == 'conv':
                kernels, bias = copy.deepcopy(self.weights[position][0][0][0][0])
                # tensorflow: weights are [height, width, in_channels, out_channels]
                kernels = np.transpose(kernels, (1, 0, 2, 3))
                bias = bias.reshape(-1)
                tensor = self.__conv_layer(tensor, kernels, bias)
            elif layer_type == 'relu':
                tensor = tf.nn.relu(tensor)
            elif layer_type == 'pool':
                tensor = self.__pool_layer(tensor)
            if layer_id in id_list:
                tensor_list[layer_id] = tensor
        assert len(tensor_list) == len(id_list)
        return tensor_list

    def get_layer_tensors_all(self, input_tensor):
        return self.get_layer_tensors(input_tensor, self.LAYERS)

    def get_layer_tensor(self, input_tensor, layer_id):
        return self.get_layer_tensors(input_tensor, [layer_id])[layer_id]

    def __conv_layer(self, input, weights, bias):
        conv = tf.nn.conv2d(input, tf.constant(weights), strides=(1, 1, 1, 1),
                padding='SAME')
        return tf.nn.bias_add(conv, bias)

    def __pool_layer(self, input):
        return tf.nn.avg_pool(input, ksize=(1, 2, 2, 1), strides=(1, 2, 2, 1),
                padding='SAME')
