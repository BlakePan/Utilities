# -*- coding: utf8 -*-
import pprint
import logging
from enum import Enum
from flask_restful import Resource, inputs

# from . import config
# from howhowalgo.api import config
# from howhowalgo.common import mongo_util
# from howhowalgo.common import mysql_util
# from howhowalgo.common import utility
#
# from howhowalgo.common.fibonacci_lib.fibonacci_params import findmin_ratio, view_init_days, view_tune_days

# logger = logging.getLogger(__name__)


class ApiBase(Resource):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialize ApiBase")

    @staticmethod
    def parse_request_args(request):
        """
        Parse request args

        :param request:
        http request

        :return:
        """

        args = dict()
        args['arg_str'] = request.args.get('arg_str', type=str, default='arg_str_default')
        args['arg_int'] = request.args.get('arg_int', type=int, default=1)
        args['arg_bool'] = request.args.get('arg_bool', type=inputs.boolean, default=True)

        return args
