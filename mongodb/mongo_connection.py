import logging
import datetime
from pprint import pformat
from pymongo import MongoClient

def mongo_connect():
    host = '127.0.0.1'
    client = MongoClient(host=host)
    db = client.test_database
    list_db_collections(db)
    results_collection = db.results
    res = {'model': 'model_id_1',
           'dataset': 'dataset_id_1',
           'result': 'X% acc',
           'timestamp': str(datetime.datetime.now())
           }
    results_collection.insert_one(res)
    list_db_collections(db)


def list_db_collections(db):
    logger = logging.getLogger('list_db_collections')
    collection_list = db.list_collection_names()
    logger.info('collections:\n%s', ', '.join(collection_list))
    for col_id in collection_list:
        collection = db[col_id]
        logger.info('collection: %s', col_id)
        for entry in collection.find():
            logger.info('\n%s', pformat(entry))
        logger.info('-')

if __name__ == "__main__":    
    LOGGING_FORMAT = '%(asctime)-15s: [%(name)s] %(message)s'
    # LOGGING_FORMAT = '[%(name)s] %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=LOGGING_FORMAT)
    mongo_connect()
