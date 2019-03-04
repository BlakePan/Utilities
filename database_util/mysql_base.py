# -*- coding: utf-8 -*-
import logging

import pandas as pd
import sqlalchemy

logger = logging.getLogger(__name__)


class MySQLBase:
    """
    Base class for MySQL utility, contains basic functions such as create connection, fetch, etc...
    """

    def __init__(self, config):
        """
        class initialization
        :param config:
        """
        logger.info("Initializing MySQLBase")
        mysqluri = 'mysql://{}:{}@{}:{}/{}?charset={}'.format(
            config['mysql']['user'], config['mysql']['pwd'],
            config['mysql']['host'], config['mysql']['port'],
            config['mysql']['db'], config['mysql']['charset'])
        self.engine = sqlalchemy.create_engine(mysqluri)
        self.connection = None

    def connect(self):
        """
        create connection
        :return:
        """
        self.connection = self.engine.connect()

    def close(self):
        """
        close connection
        :return:
        """
        self.connection.close()

    def fetchone(self, sql, params=()):
        """
        basic function to fetch one result
        :param sql: sql statment
        :param params: sql parameters
        :return: result set
        """
        try:
            self.connect()
            result = self.connection.execute(sql, params).fetchone()

        finally:
            self.close()

        return result

    def fetchall(self, sql, params=()):
        """
        basic function to fetch result set
        :param sql: sql statment
        :param params: sql parameters
        :return: result set
        """
        try:
            self.connect()
            result = self.connection.execute(sql, params).fetchall()
        finally:
            self.close()

        return result

    def insert(self, sql, params=()):
        """
        basic function to insert data
        :param sql: insert statement
        :param params: statement parameters
        :return: None
        """
        try:
            self.connect()
            res = self.connection.execute(sql, params)
            return res.lastrowid
        finally:
            self.close()

    def read_sql(self, sqlstr, params=(), index_col=None):
        """
        basic function to retrieve data and return as dataframe
        :param sqlstr:
        :param params:
        :param index_col:
        :return:
        """
        try:
            result = pd.read_sql(sqlstr, self.engine, params=params, index_col=index_col)
        except Exception as e:
            result = None
            logger.error("read_sql exception: " + str(e))

        return result
