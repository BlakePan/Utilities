# -*- coding: utf-8 -*-
import sys
import math
import numpy as np


def get_this_func_name() -> str:
    return sys._getframe(1).f_code.co_name


def get_sigmoid(x: (int, float))->float:
    return 1.0 / (1.0 + math.exp(-x))


def format_num(s: (float, int), precision: int = 6)->str:
    if isinstance(s, float):
        if np.isnan(s) or np.isinf(s):
            return ""

        format_str = '{:.%sf}' % precision
        return format_str.format(s)
    else:
        return '{}'.format(s)
