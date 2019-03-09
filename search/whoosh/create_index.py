import pymongo
import os
from whoosh.index import create_in, open_dir

from index import update_all_index
from schema import zufang_schema

if __name__ == '__main__':
    zufang_collection = pymongo.MongoClient('localhost', 27017).scrapy.zufang
    update_all_index(zufang_collection, zufang_schema)




