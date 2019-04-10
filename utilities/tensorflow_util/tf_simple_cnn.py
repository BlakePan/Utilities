# -*- coding: utf-8 -*-
import tensorflow as tf

from utilities.tensorflow_util.tf_model_example import ModelBase


class SimpleCNN(ModelBase):
    def __init__(self,
                 batch_size: int,
                 thread_index: int,
                 device: str = "/cpu:0"
                 ):
        super(SimpleCNN, self).__init__(thread_index, device)

        with tf.device(self._device), tf.variable_scope(self._scope_name) as scope:
            # Placeholders
            # input_x: [N, T, Dx, Wx]
            self.input_x = tf.placeholder(tf.float32, [batch_size, None, Dx, Wx], name="input_x")
