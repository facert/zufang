import os
import sys
import datetime
from scrapy import log
from whoosh.index import create_in, open_dir, exists_in
from whoosh.filedb.filestore import FileStorage
from whoosh.writing import AsyncWriter

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search.whoosh.index import update_index, get_index
from search.whoosh.schema import zufang_schema


class IndexPipeline(object):

    def __init__(self, index):
        self.index = index

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            index=crawler.settings.get('WHOOSH_INDEX', 'indexes')
        )

    def process_item(self, item, spider):
        self.writer = AsyncWriter(get_index(self.index, zufang_schema))
        create_time = datetime.datetime.strptime(item['create_time'], "%Y-%m-%d %H:%M:%S")
        self.writer.update_document(
            url=item['url'].decode('utf-8'),
            title=item['title'],
            description=item['description'],
            create_time=create_time
        )
        self.writer.commit()
        return item





