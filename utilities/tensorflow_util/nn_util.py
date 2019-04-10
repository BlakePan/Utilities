# -*- coding: utf-8 -*-
import math
import tensorflow as tf


def _variable(name, shape,
              dtype=tf.float32, regularizer=None, initializer=None, trainable=True, collections=None):
    """
    Gets an existing variable with these parameters or create a new one.

    :param  name:
    The name of the new or existing variable.

    :param shape:
    Shape of the new or existing variable.

    :param dtype:
    Type of the new or existing variable (defaults to `DT_FLOAT`).

    :param initializer:
    Initializer for the variable.

    :param regularizer:
    A (Tensor -> Tensor or None) function; the result of
    applying it on a newly created variable will be added to the collection
    GraphKeys.REGULARIZATION_LOSSES and can be used for regularization.

    :param trainable:
    If `True` also add the variable to the graph collection
    `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).

    :param collections:
    List of graph collections keys to add the `Variable` to.

    :return:
    """
    if initializer:
        dtype = None
    return tf.get_variable(name, shape,
                           regularizer=regularizer, initializer=initializer, dtype=dtype,
                           trainable=trainable, collections=collections)


def get_var_name(tf_var_name):
    """
    Return a variable name without symbols

    :param tf_var_name:
    org variable name

    :return:
    clean variable name
    """
    name_start = tf_var_name.find('/') + 1
    name_end = tf_var_name.find(':')
    return tf_var_name[name_start:name_end]


def build_normalization(input_x, D, suffix=''):
    """
    Normalize input_x with mean and std

    :param input_x:
    A input tensor

    :param D:
    Dimension of depth

    :param suffix:
    Suffix to normalization scope

    :return:
    A normalized tensor
    """
    with tf.variable_scope("normalization" + suffix):
        x_mean = _variable("x_mean", [1, 1, D], trainable=False,
                           collections=[tf.GraphKeys.GLOBAL_VARIABLES, tf.GraphKeys.MODEL_VARIABLES])
        x_std = _variable("x_std", [1, 1, D], trainable=False,
                          collections=[tf.GraphKeys.GLOBAL_VARIABLES, tf.GraphKeys.MODEL_VARIABLES])

        # Normalize input_x.
        std_x = tf.div(tf.subtract(input_x, x_mean), x_std)

        return std_x


def build_conv_bn(input_tensor, batch_size, width, height, num_channel,
                  max_pool_size, l1_reg_weight, l2_reg_weight, is_training,
                  prefix='', suffix=''):
    """
    Build a convolutional layer with batch normalization and l1/l2 regularization

    :param input_tensor:
    :param batch_size:
    :param width:
    :param height:
    :param num_channel:
    :param max_pool_size:
    :param l1_reg_weight:
    :param l2_reg_weight:
    :param is_training:
    :param prefix:
    :param suffix:
    :return:
    """
    # L1 regularization
    l1_regularizer = tf.contrib.layers.l1_regularizer(scale=l1_reg_weight)
    l1_weights = []

    # L2 regularization
    l2_regularizer = tf.contrib.layers.l2_regularizer(scale=l2_reg_weight)
    l2_weights = []

    conv_scope = "{}_conv_{}".format(prefix, suffix)
    with tf.variable_scope(conv_scope):
        # Init weight in a distribution ,activation: relu
        # Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification
        # (ICCV, K He, 2015)
        w_stddev = math.sqrt(2.0 / float((batch_size * height)))
        filter_shape = [batch_size, width, height, num_channel]
        w = _variable("{}_w".format(conv_scope), filter_shape,
                      initializer=tf.truncated_normal_initializer(stddev=w_stddev, dtype=tf.float32))
        b = _variable("{}_b".format(conv_scope), [num_channel],
                      initializer=tf.constant_initializer(0.0))

        # conv
        conv = tf.nn.conv2d(input_tensor, w, strides=[1, 1, 1, 1], padding='VALID')
        out_tensor = tf.nn.bias_add(conv, b)

        # L1/L2 regularization
        l1_weights.append(w)
        l2_weights.append(w)

        # batch normalization
        out_tensor = tf.contrib.layers.batch_norm(out_tensor, scale=False, center=True, is_training=is_training)

        # non-linear
        out_tensor = tf.nn.elu(out_tensor)

        # max pool
        if max_pool_size != -1:
            out_tensor = tf.nn.max_pool(out_tensor,
                                        ksize=[1, max_pool_size, max_pool_size, 1],
                                        strides=[1, 1, 1, 1],
                                        padding='SAME')
        else:
            out_tensor = out_tensor

        # make output tensor as an op in graph
        out_tensor = tf.identity(out_tensor, name='{}_out'.format(conv_scope))

    # L1/L2 regularization
    l1_loss = tf.contrib.layers.apply_regularization(l1_regularizer, l1_weights)
    l2_loss = tf.contrib.layers.apply_regularization(l2_regularizer, l2_weights)

    return out_tensor, l1_loss, l2_loss


def build_fc(input_x, fc_dim, is_training, l2_reg=0.0003, drop_prob=0, prefix='', suffix=''):
    """
    Build a fully-connected layer with l2 regularization and drop out

    :param input_x:
    :param fc_dim:
    :param is_training:
    :param l2_reg:
    :param drop_prob:
    :param prefix:
    :param suffix:
    :return:
    """
    # L2 regularization
    l2_regularizer = tf.contrib.layers.l2_regularizer(scale=l2_reg)
    l2_weights = []

    fc_scope = '{}_fc_{}'.format(prefix, suffix)
    with tf.variable_scope(fc_scope):
        fc_w_shape = [input_x.get_shape()[-1], fc_dim]
        fc_b_shape = [fc_dim]

        fc_w = _variable("{}_w".format(fc_scope), shape=fc_w_shape,
                         initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        fc_b = _variable("{}_b".format(fc_scope), shape=fc_b_shape,
                         initializer=tf.zeros_initializer)
        fc_out = tf.nn.xw_plus_b(input_x, fc_w, fc_b, name="{}_o".format(fc_scope))

        # L2 regularization
        l2_weights.append(fc_w)

        # non-linear
        fc_out = tf.nn.elu(fc_out)

        # dropout
        fc_out = tf.layers.dropout(fc_out, rate=drop_prob, training=is_training)

        # make output tensor as an op in graph
        fc_out = tf.identity(fc_out, name='{}_out'.format(fc_scope))

    # L2 regularization
    l2_loss = tf.contrib.layers.apply_regularization(l2_regularizer, l2_weights)

    return fc_out, l2_loss


def build_single_output(input_neuron):
    with tf.variable_scope("single_output"):
        input_neuron_last_dim = input_neuron.get_shape()[-1].value
        s_o_w = _variable("s_o_w", shape=[input_neuron_last_dim, 1],
                          initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        return tf.reshape(tf.matmul(input_neuron, s_o_w), [-1]), s_o_w


def build_logits_output(input_neuron, n_logits):
    with tf.variable_scope("logits_output"):
        input_neuron_last_dim = input_neuron.get_shape()[-1].value
        l_o_w = _variable("l_o_w", shape=[input_neuron_last_dim, n_logits],
                          initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        return tf.matmul(input_neuron, l_o_w), l_o_w


def build_rnn_regressor(x, num_units, suffix=''):
    with tf.variable_scope("rnn" + suffix):
        sub_cells = []
        for n in num_units:
            sub_cells.append(tf.contrib.rnn.LSTMCell(n, forget_bias=1.0))
        cell = tf.contrib.rnn.MultiRNNCell(sub_cells)

        # outputs, new_state = tf.nn.dynamic_rnn(cell, x, dtype=tf.float32, time_major=False)
        layer = tf.keras.layers.RNN(cell, return_state=True)
        outputs, new_state = layer(x)
        outputs = tf.reshape(outputs[:, -1, :], [-1, num_units[-1]])
        o_w = _variable("o_w", shape=[num_units[-1], 1],
                        initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        final_outputs = tf.reshape(tf.matmul(outputs, o_w), [-1])

    return final_outputs
