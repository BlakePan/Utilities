# -*- coding: utf8 -*-
import traceback
from flask import request
from utilities.flask_util.api.api_base import ApiBase
from utilities.logging_util.log_with_cache import api_logger


class ApiResourceExample(ApiBase):
    """
    Api Example
    """

    @api_logger()
    def get(self):
        # args from request
        try:
            args = self.parse_request_args(request)
            res = {
                'status': 'success',
                'args': args
            }
        except Exception as e:
            self.logger.debug(str(e))
            self.logger.debug(traceback.format_exc())
            res = {
                'error': str(e),
                'trace': traceback.format_exc()
            }
        return res
