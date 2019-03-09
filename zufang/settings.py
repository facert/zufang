# -*- coding: utf-8 -*-

# Scrapy settings for zufang project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zufang'

SPIDER_MODULES = ['zufang.spiders']
NEWSPIDER_MODULE = 'zufang.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zufang (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 6
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# from scrapy import log

ITEM_PIPELINES = {
    # 'zufang.pipelines.ElasticSearchPipeline': 300,
    # 'zufang.mongo_pipelines.MongoDBPipeline': 100,
    'zufang.index_pipelines.IndexPipeline': 200
}


DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 300,
    # 'zufang.download_middlewares.RotateUserAgentMiddleware': 400
}

LOG_FORMATTER = 'zufang.drop_formatter.PoliteLogFormatter'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'


MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'zufang'
MONGODB_UNIQUE_KEY = 'url'

WHOOSH_INDEX = 'indexes'


# START_URL = 'https://www.douban.com/group/26926/'

LOG_LEVEL = 'INFO'
# DUPEFILTER_DEBUG = True
# HTTPCACHE_ENABLED = False

# 豆瓣小组URL
DOUBAN_GROUP_LIST = (
    # 北京租房豆瓣
    "https://www.douban.com/group/26926/",
    # 北京租房（非中介）
    "https://www.douban.com/group/279962/",
    # 北京租房房东联盟(中介勿扰)
    "https://www.douban.com/group/257523/",
    # 北京租房
    "https://www.douban.com/group/beijingzufang/",
    # 北京租房小组
    "https://www.douban.com/group/xiaotanzi/",
    # 北京无中介租房
    "https://www.douban.com/group/zhufang/",
    # 北漂爱合租
    "https://www.douban.com/group/aihezu/",
    # 北京同志们来租房
    "https://www.douban.com/group/325060/",
    # 北京个人租房
    "https://www.douban.com/group/opking/",
    # 北京租房小组!
    "https://www.douban.com/group/374051/",
    # # 深圳租房团
    # "https://www.douban.com/group/106955/",
    # # 深圳福田租房
    # "https://www.douban.com/group/futianzufang/",
    # # 深圳南山租房
    # "https://www.douban.com/group/nanshanzufang/",
    # # 上海租房
    # "https://www.douban.com/group/shzf/",
    # # 豆瓣租房小组
    # "https://www.douban.com/group/fangzi/",
    # # 上海租房
    # "https://www.douban.com/group/homeatshanghai/",
    # # 上海租房
    # "https://www.douban.com/group/shanghaizufang/",
)
