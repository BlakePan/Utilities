# -*- coding: utf-8 -*-

import json
import logging

from pymongo import MongoClient

logger = logging.getLogger(__name__)


class MongoBase(object):
    """
    Base class for Mongo utility, contains basic functions such as create connection, fetch, etc...
    """

    def __init__(self, config):
        """
        Initialize mongo DB from configuration file
        :param config: configuration from ini file
        :return:
        """
        logger.info("Initializing MongoBase")
        self.ssl = json.loads(config['mongo']['ssl'].lower())
        if self.ssl:
            mongouri = 'mongodb://{}:{}@{}:{}/?ssl=true'.format(
                config['mongo']['user'], config['mongo']['pwd'],
                config['mongo']['host'], config['mongo']['port'])
        else:
            mongouri = 'mongodb://{}:{}@{}:{}/{}'.format(
                config['mongo']['user'], config['mongo']['pwd'],
                config['mongo']['host'], config['mongo']['port'],
                config['mongo']['auth'])

        self.client = MongoClient(mongouri, int(config['mongo']['minPoolSize']))
        self.db = self.client[config['mongo']['db']]
        self.PrintErrorMessage = json.loads(config['mongo']['printMsg'].lower())
        self.collection = None

    def setCollection(self, collection):
        try:
            self.collection = self.db[collection]
            return ""
        except Exception as e:
            logger.error('set Collection(%s) unexpected error: %s.' % (collection, str(e)))

    def find(self, query=None):
        if query is None:
            query = {}
        try:
            result = self.collection.find(query)

        except Exception as e:
            logger.error('some fields name are wrong in ' + query + "," + str(e))
            return None

        return result

    def find(self, query=None, projection=None, sortExpression=None, limitCount=1):
        if query is None:
            query = {}
        try:
            if sortExpression is None:
                if projection is None:
                    result = self.collection.find(query)
                else:
                    result = self.collection.find(query, projection)
            else:
                if projection is None:
                    result = self.collection.find(query).sort(sortExpression).limit(limitCount)
                else:
                    result = self.collection.find(query, projection).sort(sortExpression).limit(limitCount)

        except Exception as e:
            logger.error('some fields name are wrong in ' + str(query) + "," + str(e))
            return None

        return result

    def aggregate_simple(self, query):
        try:
            result = self.collection.aggregate(query)

        except Exception as e:
            logger.error('some fields name are wrong in ' + query + "," + str(e))
            return None

        return list(result)

    def aggregate(self, unwindField, query=None, projection=None, sortExpression=None, limitCount=1):
        if query is None:
            query = {}
        if projection is None:
            projection = {}
        try:
            # type of result: <class 'pymongo.cursor.Cursor'>
            if projection == {}:
                result = self.collection.aggregate(
                    pipeline=[{"$unwind": unwindField}, {"$match": query}, {"$sort": sortExpression},
                              {"$limit": limitCount}])
            else:
                result = self.collection.aggregate(
                    pipeline=[{"$unwind": unwindField}, {"$match": query}, {"$project": projection},
                              {"$sort": sortExpression}, {"$limit": limitCount}])

        except Exception as e:
            logger.error('some fields name are wrong in aggregate,' + str(e))
            return None

        return list(result)

    def find_one(self, query=None, projection=None, sortExpression=None, limitCount=1):
        if query is None:
            query = {}
        try:
            if sortExpression is None:
                result = self.collection.find_one(query, projection)
            else:
                result = self.collection.find_one(query, projection, sort=sortExpression, limit=limitCount)

        except Exception as e:
            logger.error('some fields name are wrong in ' + str(query) + "," + str(e))
            return None

        return result

    def insert(self, data):
        try:
            if type(data) is not dict:
                if self.PrintErrorMessage:
                    print('the type of INSERT data isn\'t dict')
                self.ErrorMessage = 'the type of INSERT data isn\'t dict'
                return -1

            # insert會返回新插入數據的_id
            result = self.collection.insert(data)
            return result  # python use result.modified_count
        except Exception as e:
            if self.PrintErrorMessage:
                print("INSERT unexpected error: " + str(e))
            self.ErrorMessage = "INSERT unexpected error: " + str(e)
            return -1

    def remove(self, data):
        try:
            if type(data) is not dict:
                if self.PrintErrorMessage:
                    print('the type of REMOVE data isn\'t dict')
                self.ErrorMessage = 'the type of REMOVE data isn\'t dict'
                return -1

            result = self.collection.remove(data)
            return result['n']  # python use result.modified_count
        except Exception as e:
            if self.PrintErrorMessage:
                print("REMOVE unexpected error: " + str(e))
            self.ErrorMessage = "REMOVE unexpected error: " + str(e)
            return -1

    def update_simple(self, data, setdata):
        try:
            if type(data) is not dict or type(setdata) is not dict:
                if self.PrintErrorMessage:
                    print('the type of UPDATE data isn\'t dict')
                self.ErrorMessage = 'the type of UPDATE data isn\'t dict'
                return -1

            result = self.collection.update(data, setdata)
            return result['n']  # python use result.modified_count
        except Exception as e:
            if self.PrintErrorMessage:
                print("UPDATE unexpected error: " + str(e))
            self.ErrorMessage = "UPDATE unexpected error: " + str(e)
            return -1

    def update(self, data, setdata, operation):
        try:
            if type(data) is not dict or type(setdata) is not dict:
                if self.PrintErrorMessage:
                    print('the type of UPDATE data isn\'t dict')
                self.ErrorMessage = 'the type of UPDATE data isn\'t dict'
                return -1

            result = self.collection.update(data, {'$' + operation: setdata})
            return result['n']  # python use result.modified_count
        except Exception as e:
            if self.PrintErrorMessage:
                print("UPDATE unexpected error: " + str(e))
            self.ErrorMessage = "UPDATE unexpected error: " + str(e)
            return -1

    def replace(self, data, setdata):
        try:
            if type(data) is not dict or type(setdata) is not dict:
                if self.PrintErrorMessage:
                    print('the type of REPLACE data isn\'t dict')
                self.ErrorMessage = 'the type of REPLACE data isn\'t dict'
                return -1

            result = self.collection.replace_one(data, setdata, True)
            return result['n']  # python use result.modified_count
        except Exception as e:
            if self.PrintErrorMessage:
                print("REPLACE unexpected error: " + str(e))
            self.ErrorMessage = "REPLACE unexpected error: " + str(e)
            return -1
