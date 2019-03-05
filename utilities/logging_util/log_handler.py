# -*- coding: utf-8 -*-
import os
import logging


class LoggerHandler(object):
    def __init__(self,
                 fname: str = 'log',
                 path: str = './logs',
                 msg_format: str = '%(message)s',
                 level: str = 'info',
                 stream: (str, None) = None,
                 datetime_format: str = '%Y/%m/%d %H:%M:%S'):
        self.fname = fname
        self.path = path
        self.msg_format = msg_format
        self.level = level
        self.stream = stream
        self.datetime_format = datetime_format
        os.makedirs(self.path, exist_ok=True)

        self.logger = None
        self.fileHandler = None
        self.streamHandler = None
        self.config()

    def config(self):
        self.logger = logging.getLogger()

        formatter = logging.Formatter(self.msg_format, datefmt=self.datetime_format)
        self.fileHandler = logging.FileHandler(self.path + '/' + self.fname, mode='w')
        self.fileHandler.setFormatter(formatter)
        self.streamHandler = logging.StreamHandler(self.stream)
        self.streamHandler.setFormatter(formatter)

        if self.level == 'debug':
            self.logger.setLevel(logging.DEBUG)
        elif self.level == 'info':
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.INFO)

        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.streamHandler)

    def set_level(self, level: str):
        self.logger.setLevel(level)

    def remove_handler(self, handler_list: list, close_handler: bool = True):
        for h in handler_list:
            self.logger.removeHandler(h)
            if close_handler:
                h.close()

    def add_handler(self, handler_list: list):
        for h in handler_list:
            self.logger.addHandler(h)

    def create_new_log(self, org_handlers: list, fname: str = 'log', level: str = 'info'):
        self.remove_handler(org_handlers)
        self.fname = fname
        self.level = level
        self.config()
