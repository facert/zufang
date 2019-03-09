from whoosh.fields import Schema, TEXT, ID, DATETIME
from jieba.analyse import ChineseAnalyzer

analyzer = ChineseAnalyzer()

zufang_schema = Schema(
    url=ID(unique=True, stored=True),
    title=TEXT(stored=True, analyzer=analyzer),
    description=TEXT(analyzer=analyzer),
    address_tag=ID(stored=True),
    create_time=DATETIME(stored=True, sortable=True)
)
