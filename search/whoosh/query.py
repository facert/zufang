import os
import datetime
from whoosh.qparser import QueryParser
from whoosh import query
from whoosh.qparser import MultifieldParser
from index import get_index
from schema import zufang_schema


def zufang_query(keywords, limit=100):
    ix = get_index('indexes', zufang_schema)
    content = ["title", "description"]
    query = MultifieldParser(content, ix.schema).parse(keywords)

    result_list = []
    with ix.searcher() as searcher:
        results = searcher.search(query, sortedby="create_time", reverse=True, limit=limit)
        for i in results:
            result_list.append({'url': i['url'], 'title': i['title'], 'create_time': i['create_time']})
    return result_list


#