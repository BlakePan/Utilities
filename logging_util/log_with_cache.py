# -*- coding: utf-8 -*-
import logging
import time

from flask import request, Response
from werkzeug.contrib.cache import SimpleCache

CACHE_DEFAULT_TIMEOUT = 180
logger = logging.getLogger(__name__)


class api_logger(object):
    """
    The logger for api method
    """

    def __init__(self, check_auth=True, cache_data=True, show_args=False, timeout=CACHE_DEFAULT_TIMEOUT):
        """
        :param check_auth:
        If check authorization or not

        :param cache_data:
        If cache_data is True, this api method will use cache
        If 'nocache=1' in request url, this param has no effect

        :param show_args:
        If show_args is True, the input args will be show and save to log

        :param timeout:
        Timeout setting for caching
        """
        logger.debug("Initializing api_logger")
        self.show_args = show_args
        self.check_auth = check_auth
        self.cache_data = cache_data
        self.cache = SimpleCache()
        self.timeout = timeout

    def __call__(self, f):
        def decorator(*args, **kwargs):
            st = time.time()

            data = None
            # check authorization
            if self.check_auth:
                auth = request.authorization
                if not auth or not self.verify(auth.username, auth.password):
                    return Response('UNAUTHORIZED!', 401, {'WWW-Authenticate': 'Basic realm="Login!"'})

            # check if this method need to implement caching
            if self.cache_data:
                cacheKey = request.full_path.replace('nocache=1', '')

                # if nocache=1, don't check the cache
                if request.args.get('nocache') != '1':
                    data = self.cache.get(cacheKey)

                if data is None:
                    data = f(*args, **kwargs)
                    self.cache.set(cacheKey, data, self.timeout)
                    logger.debug('[CACHE_SET] cacheKey:[%s] timeout(seconds):[%i]', cacheKey, self.timeout)
                else:
                    logger.debug('[CACHE_HIT] cacheKey:[%s]', cacheKey)
            else:
                data = f(*args, **kwargs)

            # cal how much time is spend on this method
            timediff = int((time.time() - st) * 1000)

            # logging
            if self.show_args:
                logger.info('[APILOGGER] ip:[%s] full_path:[%s] time(ms):[%s] args:[%s] kwargs:[%s]',
                            request.remote_addr, request.full_path, timediff, args[1:], kwargs)
            else:
                logger.info('[APILOGGER] ip:[%s] full_path:[%s] time(ms):[%s]', request.remote_addr,
                            request.full_path, timediff)

            return data

        return decorator

    def verify(self, username, password):
        from . import config

        if not (username and password):
            return False
        return config['login'].get(username) == password


class method_logger(object):
    """
    the logger for methods in a class
    """

    def __init__(self, cache_data=False, show_args=False, timeout=CACHE_DEFAULT_TIMEOUT, tag="METHOD_LOGGER"):
        logger.debug("Initializing method_logger")
        self.show_args = show_args
        self.cache_data = cache_data
        self.cache = SimpleCache()
        self.timeout = timeout
        self.tag = tag

    def __call__(self, f):
        def decorator(*args, **kwargs):
            st = time.time()

            # check if this method need to implement caching
            if self.cache_data:
                cacheKey = self.get_cachekey(f, args, kwargs)
                data = self.cache.get(cacheKey)

                if data is None:
                    data = f(*args, **kwargs)
                    self.cache.set(cacheKey, data, self.timeout)
                    logger.debug('[CACHE_SET] cacheKey:[%s] timeout(seconds):[%i]', cacheKey, self.timeout)
                else:
                    logger.debug('[CACHE_HIT] cacheKey:[%s]', cacheKey)

            else:
                data = f(*args, **kwargs)

            # cal how much time is spend on this method
            timediff = int((time.time() - st) * 1000)

            # logging
            if self.show_args:
                logger.info('[%s] time(ms):[%s] method:[%s] args:[%s] kwargs:[%s]',
                            self.tag, timediff, str(f.__name__), args[1:], kwargs)
            else:
                logger.info('[%s] time(ms):[%s] method:[%s]',
                            self.tag, timediff, str(f.__name__))
            return data

        return decorator

    def get_cachekey(self, f, args, kwargs):
        cacheKey = "%s|%s|%s" % (str(f.__name__), str(args[1:]), str(kwargs))
        return cacheKey


class function_logger(method_logger):
    """
    the logger for functions
    """

    def __init__(self, cache_data=False, show_args=False, timeout=CACHE_DEFAULT_TIMEOUT, tag="FUNCTION_LOGGER"):
        super().__init__()
        logger.debug("Initializing function_logger")
        self.show_args = show_args
        self.cache_data = cache_data
        self.cache = SimpleCache()
        self.timeout = timeout
        self.tag = tag

    def get_cachekey(self, f, args, kwargs):
        cacheKey = "%s|%s|%s" % (str(f.__name__), str(args), str(kwargs))
        return cacheKey
