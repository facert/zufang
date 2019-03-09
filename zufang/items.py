# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    url = scrapy.Field()
    group_type = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    create_time = scrapy.Field()
    description = scrapy.Field()
    picture = scrapy.Field()
    address_tag = scrapy.Field()
    update_time = scrapy.Field()

