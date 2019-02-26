import sys
import math


def get_this_func_name() -> str:
    return sys._getframe(1).f_code.co_name


def get_sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))
