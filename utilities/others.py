# -*- coding: utf-8 -*-
import sys
import math
import numpy as np


def get_this_func_name() -> str:
    return sys._getframe(1).f_code.co_name


def get_sigmoid(x: (int, float))->float:
    return 1.0 / (1.0 + math.exp(-x))


def softmax(x: np.array)->np.array:
    """
    Compute softmax values for each sets of scores in x.

    Shifts all of elements in the vector to negative to zero,
    and negatives with large exponents saturate to zero rather than the infinity,
    avoiding overflowing and resulting in nan.
    """
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def cross_entropy(X: np.array, y: np.array)->float:
    """
    X is the output from fully connected layer (num_examples x num_classes)
    y is labels (num_examples x 1)
    Note that y is not one-hot encoded vector.
    It can be computed as y.argmax(axis=1) from one-hot encoded vectors of labels if required.
    """
    m = y.shape[0]
    p = softmax(X)
    # We use multidimensional array indexing to extract
    # softmax probability of the correct label for each sample.
    # Refer to https://docs.scipy.org/doc/numpy/user/basics.indexing.html#indexing-multi-dimensional-arrays
    # for understanding multidimensional array indexing.
    log_likelihood = -np.log(p[range(m), y])
    loss = np.sum(log_likelihood) / m
    return loss


def delta_cross_entropy(X: np.array, y: np.array)->float:
    """
    X is the output from fully connected layer (num_examples x num_classes)
    y is labels (num_examples x 1)
    Note that y is not one-hot encoded vector.
    It can be computed as y.argmax(axis=1) from one-hot encoded vectors of labels if required.
    """
    m = y.shape[0]
    grad = softmax(X)
    grad[range(m), y] -= 1
    grad = grad/m
    return grad


def format_num(s: (float, int), precision: int = 6)->str:
    if isinstance(s, float):
        if np.isnan(s) or np.isinf(s):
            return ""

        format_str = '{:.%sf}' % precision
        return format_str.format(s)
    else:
        return '{}'.format(s)
