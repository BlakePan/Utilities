# -*- coding: utf8 -*-
import logging

from flask import Flask
from flask import jsonify
from flask_restful import Api
from werkzeug.contrib.fixers import ProxyFix  # gunicron

from utilities.logging_util.log_with_cache import api_logger
from utilities.flask_util.api.api_base import ApiBase
from utilities.flask_util.api.api_resource import ApiResourceExample


logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app, prefix='/api_example', catch_all_404s=True)

# turn off flask info log
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# default home page
class ApiHome(ApiBase):
    @api_logger(check_auth=False, cache_data=False)
    def get(self):
        logger.info("HOME")
        return "Api Home"


####################################################
## Set the Api resource routing here
####################################################

# root
api.add_resource(ApiHome, '/')

# api resource
api.add_resource(ApiResourceExample, '/api_resource_example')


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def main():
    app.run(debug=False, host='0.0.0.0', port=5010, threaded=True)
    return 0


app.wsgi_app = ProxyFix(app.wsgi_app)  # gunicorn

if __name__ == '__main__':
    exit(main())
