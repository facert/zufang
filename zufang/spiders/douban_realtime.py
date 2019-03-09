# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zufang.items import ZufangItem
from zufang import settings
import time


class DoubanRealtimeSpider(CrawlSpider):
    name = "douban_realtime"
    allowed_domains = ["douban.com"]
    start_urls = (settings.DOUBAN_GROUP_LIST)

    rules = (
        Rule(LinkExtractor(allow=r"https://www\.douban\.com/group/topic/\d+/$"), callback="parse_topic"),
        # Rule(LinkExtractor(allow=r"https://www\.douban\.com/group/\w+/discussion\?start=[0-9]{0,4}$"), follow=True),
    )

    def start_requests(self):
        while True:
            for base_url in self.start_urls:
                url = base_url
                yield Request(url, dont_filter=True)
            time.sleep(6)

    def parse_topic_list(self, response):
        selector = Selector(response)
        topic_list = selector.xpath('//table[@class="olt"]/tr')
        for topic in topic_list:
            url = topic.xpath('td[@class="title"]/a/@href').extract()
            if url:
                yield Request(url[0], callback=self.parse_topic)

    def parse_topic(self, response):
        # import pdb;pdb.set_trace()
        zufang_item = ZufangItem()
        zufang_item['url'] = response.url
        zufang_item['group_type'] = 'douban'
        zufang_item['title'] = self.get_title(response)
        zufang_item['author'] = self.get_author(response)
        zufang_item['description'] = self.get_description(response)
        zufang_item['create_time'] = self.get_create_time(response)
        yield zufang_item

    def get_title(self, response):
        title = response.xpath("//title/text()").extract()
        return title[0] if title else ''

    def get_author(self, response):
        author = response.xpath("//div[@class='topic-doc']/h3/span[@class='from']/a/text()").extract()
        return author[0] if author else ''

    def get_description(self, response):
        description = response.xpath("//div[@class='topic-content']").extract()
        return description[0] if description else ''

    def get_create_time(self, response):
        create_time = response.xpath("//div[@class='topic-doc']/h3/span[@class='color-green']/text()").extract()
        return create_time[0] if create_time else ''
