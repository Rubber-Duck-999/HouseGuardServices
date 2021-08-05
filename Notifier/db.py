import logging
import pymongo
import datetime
from pymongo.errors import PyMongoError


class MissingSetup(Exception):
    '''Setup has not completed'''


class Database:
    '''Db interface'''

    def __init__(self):
        '''Constructor'''
        logging.info('__init__()')
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.database_name = 'database'
        self.collection_name = 'collection'
        self.collection = None

    def check(self):
        '''Read data from db'''
        logging.info('# check()')
        try:
            db_list = self.client.list_database_names()
            if self.database_name in db_list:
                logging.info("The database exists")
            db = self.client[self.database_name]
            col_list = db.list_collection_names()
            if self.collection_name in col_list:
                logging.info("The collection exists")
            self.collection = db[self.collection_name]
            for x in self.collection.find():
                if 'temperature' in x:
                    logging.info('Temperature: {}'.format(x['temperature']))
                else:
                    logging.error('Key Missing')
        except PyMongoError as error:
            logging.error('PyMongo Error: {}'.format(error))
        except MissingSetup as error:
            logging.error('Missing Setup Error: {}'.format(error))
        except KeyError as error:
            logging.error('Missing Key Error: {}'.format(error))

    def insert(self, temp):
        '''Add record into mongodb'''
        logging.info('# insert()')
        try:
            self.check()
            created_at = datetime.datetime.now()
            mydict = {"temperature": temp, "created_at": created_at}
            record = self.collection.insert_one(mydict)
            self.check()
        except PyMongoError as error:
            logging.error('PyMongo Error: {}'.format(error))
