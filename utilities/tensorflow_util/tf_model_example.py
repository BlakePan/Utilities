# -*- coding: utf-8 -*-
import tensorflow as tf
from utilities.tensorflow_util.nn_util import get_var_name


class ModelBase(object):
    def __init__(self,
                 thread_index: int,
                 device: str = "/cpu:0"):
        self._thread_index = thread_index
        self._device = device
        self._scope_name = "model_" + str(thread_index)

    def get_vars(self, scope=None):
        if scope is None:
            return tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=self._scope_name)
        else:
            return tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope)

    @property
    def scope_name(self):
        return self._scope_name

    def sync_from(self, src_network, name=None):
        """
        :param src_network:
        :param name:
        
        :return:
        An Operation that executes all its inputs.
        """
        src_vars = src_network.get_vars()
        dst_vars = self.get_vars()
        sync_ops = []
        with tf.device(self._device):
            with tf.name_scope(name, "model", []) as name:
                for (src_var, dst_var) in zip(src_vars, dst_vars):
                    assert get_var_name(src_var.name) == get_var_name(dst_var.name)
                    sync_op = tf.assign(dst_var, src_var)
                    sync_ops.append(sync_op)

                return tf.group(*sync_ops, name=name)
