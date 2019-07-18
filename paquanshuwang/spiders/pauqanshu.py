# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from paquanshuwang.items import PaquanshuwangItem,PaquanshuwangDetailItem


class PauqanshuSpider(CrawlSpider):
    name = 'pauqanshu'
    allowed_domains = ['quanshuwang.com']
    start_urls = ['http://www.quanshuwang.com/shuku/']


    rules = (
        Rule(LinkExtractor(allow=r'book_.*?', restrict_xpaths="//div[@class='tab-item clearfix']/div[@class='yd-book-item yd-book-item-pull-left']/a"), callback='parse_item', follow=False,),
        Rule(LinkExtractor(allow=r'www.quanshuwang.com.*?', restrict_xpaths='//div[@id="pagelink"]/a'), callback='parse_first', follow=True,),
    )

    def parse_first(self, response):
        pass

    def parse_item(self, response):
        item = PaquanshuwangItem()
        item['book_url'] = response.url
        item['title'] = response.xpath("//div[@class='b-info']/h1/text()").extract_first()
        intro = response.xpath("//div[@id='waa']/text()").extract_first()
        if intro:
            item["intro"] = intro.replace("'", "‘").replace('"', "“")
        else:
            item["intro"] = None
        item['author'] = response.xpath('//div[@class="bookDetail"]/dl[2]/dd/text()').extract_first()
        item['category'] = response.xpath('//a[@class="c009900"]/text()').extract_first()
        item['state'] = response.xpath('//div[@class="bookDetail"]/dl[1]/dd/text()').extract_first()
        item['image_url'] = response.xpath('//a[@class="l mr11"]/img/@src').extract_first()
        item['detail_url'] = response.xpath('//a[@class="reader"]/@href').extract_first()
        # print(item['detail_url'])
        yield scrapy.Request(url=item['detail_url'], callback=self.parse_detail_item)
        yield item



    def parse_detail_item(self, response):
        sql = 'SELECT id FROM tb_book_info WHERE detail_url= "{}"'.format(response.url)
        self.cusr.execute(sql)
        result = self.cusr.fetchone()
        if result:
            next_url_list = response.xpath('//div[@class="clearfix dirconone"]/li/a/@href').extract()
            for next_url in next_url_list:
                yield scrapy.Request(url=next_url, callback=self.parse_chapter, meta={'book_id': str(result[0])})



    def parse_chapter(self, response):
        item = PaquanshuwangDetailItem()
        item['book_id'] = response.meta['book_id']
        chapter_text = ''.join(response.xpath("//div[@id='content']/text()").extract())
        item['chapter_url'] = response.url
        chapter_name = response.xpath("//strong[@class='l jieqi_title']/text()").extract_first()
        title_name = response.xpath("//em[@class='l']/text()").extract_first()
        # 若chapter_text有匹配到数据就替换数据.
        if chapter_text:
            item["chapter_text"] = chapter_text.replace("'", "‘").replace('"', "“")
        else:
            item["chapter_text"] = None

        # 若title_name和chapter_name都会真, 则拼接数据.
        if title_name and chapter_name:
            item["chapter_name"] = title_name + chapter_name
        else:
            if chapter_name:
                item["chapter_name"] = response.xpath("//strong[@class='l jieqi_title']/text()").extract_first()
            else:
                item["chapter_name"] = None
        yield item
